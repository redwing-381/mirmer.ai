import { describe, it, expect } from 'vitest'
import fc from 'fast-check'

/**
 * Utility function to highlight matching text in a string
 * This will be used by the search results display
 * 
 * @param {string} text - The text to search in
 * @param {string} query - The search query
 * @returns {Array<{text: string, highlighted: boolean}>} - Array of text segments with highlight flags
 */
export function highlightMatches(text, query) {
  if (!query || !query.trim() || !text) {
    return [{ text, highlighted: false }]
  }

  const queryLower = query.toLowerCase().trim()
  
  // If query becomes empty after trimming, return no highlights
  if (!queryLower) {
    return [{ text, highlighted: false }]
  }
  
  const textLower = text.toLowerCase()
  
  const segments = []
  let lastIndex = 0
  let matchIndex = textLower.indexOf(queryLower)

  while (matchIndex !== -1) {
    // Add non-highlighted text before match
    if (matchIndex > lastIndex) {
      segments.push({
        text: text.substring(lastIndex, matchIndex),
        highlighted: false
      })
    }

    // Add highlighted match
    segments.push({
      text: text.substring(matchIndex, matchIndex + query.length),
      highlighted: true
    })

    lastIndex = matchIndex + query.length
    matchIndex = textLower.indexOf(queryLower, lastIndex)
  }

  // Add remaining non-highlighted text
  if (lastIndex < text.length) {
    segments.push({
      text: text.substring(lastIndex),
      highlighted: false
    })
  }

  return segments
}

/**
 * Property-Based Tests for Search Highlighting
 * 
 * Feature: enterprise-features, Property 7: Matching text is highlighted
 * Validates: Requirements 2.2
 */
describe('Search Highlighting Property Tests', () => {
  it('Property 7: All highlighted segments contain the query (case-insensitive)', () => {
    fc.assert(
      fc.property(
        fc.string({ minLength: 1, maxLength: 200 }), // Random text
        fc.string({ minLength: 1, maxLength: 20 }),  // Random query
        (text, query) => {
          const segments = highlightMatches(text, query)
          const queryLower = query.toLowerCase().trim()

          // For any highlighted segment, it should contain the query (case-insensitive)
          const highlightedSegments = segments.filter(s => s.highlighted)
          
          return highlightedSegments.every(segment => 
            segment.text.toLowerCase().includes(queryLower)
          )
        }
      ),
      { numRuns: 100 }
    )
  })

  it('Property 7: Highlighted segments preserve original case', () => {
    fc.assert(
      fc.property(
        fc.string({ minLength: 1, maxLength: 200 }),
        fc.string({ minLength: 1, maxLength: 20 }),
        (text, query) => {
          const segments = highlightMatches(text, query)
          
          // Reconstructing the text from segments should give us the original text
          const reconstructed = segments.map(s => s.text).join('')
          return reconstructed === text
        }
      ),
      { numRuns: 100 }
    )
  })

  it('Property 7: Empty query returns no highlights', () => {
    fc.assert(
      fc.property(
        fc.string({ minLength: 0, maxLength: 200 }),
        (text) => {
          const emptyQueries = ['', '  ', '\t', '\n']
          
          return emptyQueries.every(query => {
            const segments = highlightMatches(text, query)
            return segments.every(s => !s.highlighted)
          })
        }
      ),
      { numRuns: 100 }
    )
  })

  it('Property 7: All occurrences are highlighted', () => {
    fc.assert(
      fc.property(
        fc.string({ minLength: 1, maxLength: 20 }), // query
        fc.integer({ min: 1, max: 5 }),              // number of repetitions
        (query, repetitions) => {
          // Create text with multiple occurrences of the query
          const text = Array(repetitions).fill(query).join(' filler ')
          const segments = highlightMatches(text, query)
          
          // Count highlighted segments
          const highlightedCount = segments.filter(s => s.highlighted).length
          
          // Should have as many highlighted segments as repetitions
          return highlightedCount === repetitions
        }
      ),
      { numRuns: 100 }
    )
  })

  it('Property 7: Case-insensitive matching works correctly', () => {
    fc.assert(
      fc.property(
        fc.constantFrom('hello', 'HELLO', 'Hello', 'HeLLo'),
        fc.constantFrom('hello', 'HELLO', 'Hello', 'HeLLo'),
        (text, query) => {
          const segments = highlightMatches(text, query)
          
          // Should find a match regardless of case
          const hasHighlight = segments.some(s => s.highlighted)
          return hasHighlight
        }
      ),
      { numRuns: 100 }
    )
  })

  it('Property 7: No false positives - only actual matches are highlighted', () => {
    fc.assert(
      fc.property(
        fc.string({ minLength: 1, maxLength: 200 }),
        fc.string({ minLength: 1, maxLength: 20 }),
        (text, query) => {
          const segments = highlightMatches(text, query)
          const queryLower = query.toLowerCase().trim()
          const textLower = text.toLowerCase()

          // If text doesn't contain query, there should be no highlights
          if (!textLower.includes(queryLower)) {
            return segments.every(s => !s.highlighted)
          }
          
          return true
        }
      ),
      { numRuns: 100 }
    )
  })

  it('Property 7: Segments are in correct order', () => {
    fc.assert(
      fc.property(
        fc.string({ minLength: 1, maxLength: 200 }),
        fc.string({ minLength: 1, maxLength: 20 }),
        (text, query) => {
          const segments = highlightMatches(text, query)
          
          // Joining segments should reconstruct original text
          const reconstructed = segments.map(s => s.text).join('')
          return reconstructed === text
        }
      ),
      { numRuns: 100 }
    )
  })
})

/**
 * Unit Tests for specific edge cases
 */
describe('Search Highlighting Edge Cases', () => {
  it('handles exact match', () => {
    const result = highlightMatches('hello', 'hello')
    expect(result).toEqual([
      { text: 'hello', highlighted: true }
    ])
  })

  it('handles partial match at start', () => {
    const result = highlightMatches('hello world', 'hello')
    expect(result).toEqual([
      { text: 'hello', highlighted: true },
      { text: ' world', highlighted: false }
    ])
  })

  it('handles partial match at end', () => {
    const result = highlightMatches('hello world', 'world')
    expect(result).toEqual([
      { text: 'hello ', highlighted: false },
      { text: 'world', highlighted: true }
    ])
  })

  it('handles multiple matches', () => {
    const result = highlightMatches('hello world hello', 'hello')
    expect(result).toEqual([
      { text: 'hello', highlighted: true },
      { text: ' world ', highlighted: false },
      { text: 'hello', highlighted: true }
    ])
  })

  it('handles case-insensitive matching', () => {
    const result = highlightMatches('Hello World', 'hello')
    expect(result).toEqual([
      { text: 'Hello', highlighted: true },
      { text: ' World', highlighted: false }
    ])
  })

  it('handles no match', () => {
    const result = highlightMatches('hello world', 'xyz')
    expect(result).toEqual([
      { text: 'hello world', highlighted: false }
    ])
  })

  it('handles empty text', () => {
    const result = highlightMatches('', 'query')
    expect(result).toEqual([
      { text: '', highlighted: false }
    ])
  })

  it('handles empty query', () => {
    const result = highlightMatches('hello world', '')
    expect(result).toEqual([
      { text: 'hello world', highlighted: false }
    ])
  })

  it('handles whitespace-only query', () => {
    const result = highlightMatches('hello world', '   ')
    expect(result).toEqual([
      { text: 'hello world', highlighted: false }
    ])
  })
})
