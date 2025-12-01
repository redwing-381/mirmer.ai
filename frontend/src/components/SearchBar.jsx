import { useState, useEffect, useRef } from 'react'
import { Search, X } from 'lucide-react'
import { Input } from './ui/Input'

export default function SearchBar({ onSearch, onClear }) {
  const [query, setQuery] = useState('')
  const [isSearching, setIsSearching] = useState(false)
  const debounceTimer = useRef(null)

  // Debounced search - wait 300ms after user stops typing
  useEffect(() => {
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current)
    }

    if (query.trim()) {
      setIsSearching(true)
      debounceTimer.current = setTimeout(() => {
        onSearch(query)
        setIsSearching(false)
      }, 300)
    } else {
      onClear()
      setIsSearching(false)
    }

    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current)
      }
    }
  }, [query, onSearch, onClear])

  const handleClear = () => {
    setQuery('')
    onClear()
  }

  return (
    <div className="relative">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
        <Input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search conversations..."
          className="pl-10 pr-10"
        />
        {query && (
          <button
            onClick={handleClear}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
            aria-label="Clear search"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>
      {isSearching && (
        <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
          <div className="animate-spin rounded-full h-4 w-4 border-2 border-[#4ECDC4] border-t-transparent"></div>
        </div>
      )}
    </div>
  )
}
