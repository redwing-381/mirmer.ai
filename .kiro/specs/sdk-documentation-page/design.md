# Design Document

## Overview

This design creates a comprehensive SDK documentation page for the Mirmer AI Python SDK. The page will be integrated into the existing landing site with a new route `/docs`, accessible from the main navigation. It will follow the neobrutalist design aesthetic established in the landing page while providing clear, developer-friendly documentation with interactive code examples.

## Architecture

The documentation page consists of:

1. **Route Configuration** - New `/docs` route in React Router
2. **Documentation Page Component** - Main page container with sections
3. **Code Block Component** - Reusable component for syntax-highlighted code with copy functionality
4. **Table of Contents Component** - Navigation sidebar for quick section access
5. **Navigation Updates** - Add "DOCS" link to existing Navigation component

### Page Structure

```
DocsPage
├── Navigation (updated with DOCS link)
├── Hero Section (SDK title and description)
├── Table of Contents (sidebar on desktop, collapsible on mobile)
└── Content Sections
    ├── Installation
    ├── Authentication
    ├── Quick Start
    ├── Basic Usage
    ├── Streaming
    ├── Async Usage
    ├── Conversation Management
    ├── Usage Statistics
    ├── Error Handling
    ├── Configuration
    └── API Reference
```

## Components and Interfaces

### 1. DocsPage Component (`frontend/src/pages/DocsPage.jsx`)

**Purpose**: Main documentation page container

**Interface**:
```javascript
export default function DocsPage()
```

**Responsibilities**:
- Render navigation with DOCS link highlighted
- Display hero section with SDK title
- Render table of contents
- Display all documentation sections
- Handle scroll-based section highlighting
- Maintain responsive layout

### 2. CodeBlock Component (`frontend/src/components/ui/CodeBlock.jsx`)

**Purpose**: Display syntax-highlighted code with copy functionality

**Interface**:
```javascript
export default function CodeBlock({ 
  code: string,
  language: string,
  title?: string,
  showLineNumbers?: boolean
})
```

**Responsibilities**:
- Syntax highlight code based on language
- Display copy button on hover (always visible on mobile)
- Copy code to clipboard on button click
- Show visual confirmation after copy
- Apply neobrutalist styling with borders and shadows

### 3. TableOfContents Component (`frontend/src/components/docs/TableOfContents.jsx`)

**Purpose**: Navigation sidebar for quick section access

**Interface**:
```javascript
export default function TableOfContents({ 
  sections: Array<{id: string, title: string}>,
  activeSection: string
})
```

**Responsibilities**:
- Display list of documentation sections
- Highlight currently active section
- Smooth scroll to section on click
- Collapse/expand on mobile
- Sticky positioning on desktop

### 4. Updated Navigation Component (`frontend/src/components/landing/Navigation.jsx`)

**Purpose**: Add DOCS link to existing navigation

**Changes**:
- Add "DOCS" link between "PRICING" and auth buttons
- Highlight DOCS link when on `/docs` route
- Include DOCS link in mobile menu
- Navigate to `/docs` on click

## Data Models

### Documentation Section

```typescript
interface DocSection {
  id: string;           // URL hash anchor (e.g., "installation")
  title: string;        // Display title (e.g., "Installation")
  content: ReactNode;   // Section content
}
```

### Code Example

```typescript
interface CodeExample {
  code: string;         // Code content
  language: string;     // Programming language (e.g., "python", "bash")
  title?: string;       // Optional title for the code block
  description?: string; // Optional description before code
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property Reflection

After reviewing the prework, several observations:

- Most requirements are example-based (testing specific content exists) rather than properties
- Properties focus on consistent behavior across all instances (all code blocks, all methods, all TOC links)
- Visual design requirements (7.1-7.3, 7.5) are not programmatically testable
- Mobile-specific behavior (8.5) is an edge case handled by generators

Consolidated properties:
- Code formatting properties (2.3, 4.4, 4.5, 5.5) can be combined into comprehensive code block formatting
- Method documentation properties (6.2-6.5) can be combined into comprehensive API reference formatting
- Copy button properties (8.1-8.4) can be combined into comprehensive copy functionality

### Correctness Properties

Property 1: Installation commands are in code blocks
*For any* installation command displayed on the page, it should be formatted as a copyable code block with syntax highlighting
**Validates: Requirements 2.3**

Property 2: Code examples include comments and output
*For any* code example displayed on the page, it should include explanatory comments and show expected output or response format
**Validates: Requirements 4.4, 4.5**

Property 3: Conversation examples show response structure
*For any* conversation management example, it should display the response structure for that operation
**Validates: Requirements 5.5**

Property 4: API methods are fully documented
*For any* client method in the API reference, it should show the method signature with parameter types, a description, parameter descriptions, and return type
**Validates: Requirements 6.2, 6.3, 6.4, 6.5**

Property 5: Code blocks have consistent styling
*For any* code block displayed on the page, it should have borders and shadows matching the neobrutalist design system
**Validates: Requirements 7.4**

Property 6: Code blocks show copy button on interaction
*For any* code block, hovering (desktop) or viewing (mobile) should display a copy button positioned in the top-right corner
**Validates: Requirements 8.1, 8.4**

Property 7: Copy button copies code to clipboard
*For any* copy button click, the associated code should be copied to the clipboard and visual confirmation should be shown
**Validates: Requirements 8.2, 8.3**

Property 8: TOC links navigate to sections
*For any* table of contents link click, the page should smooth scroll to the corresponding section
**Validates: Requirements 9.2**

Property 9: Scroll position highlights TOC item
*For any* scroll position on the page, the table of contents should highlight the currently visible section
**Validates: Requirements 9.3**

## Error Handling

### Navigation Errors

**Scenario**: User navigates to `/docs` but page fails to load
- **Response**: Display error message with retry button
- **Logging**: Console error log
- **User Impact**: User sees error, can retry or navigate back

**Scenario**: User clicks TOC link but section doesn't exist
- **Response**: Scroll to top of page
- **Logging**: Console warning
- **User Impact**: Page scrolls but not to expected section

### Copy Functionality Errors

**Scenario**: Clipboard API not available (old browser)
- **Response**: Fall back to manual selection prompt
- **Logging**: Console warning about clipboard unavailability
- **User Impact**: User must manually copy code

**Scenario**: Copy operation fails
- **Response**: Show error message "Failed to copy"
- **Logging**: Console error
- **User Impact**: User sees error, can try again

### Responsive Design Errors

**Scenario**: Page renders incorrectly on small screens
- **Response**: Ensure minimum readable layout
- **Logging**: None (CSS handles responsiveness)
- **User Impact**: Content may be cramped but readable

## Testing Strategy

### Unit Testing

**Component Tests**:
- Test CodeBlock component renders code correctly
- Test CodeBlock copy button functionality
- Test TableOfContents renders all sections
- Test TableOfContents click navigation
- Test DocsPage renders all sections
- Test Navigation component includes DOCS link

**Integration Tests**:
- Test navigation from landing page to docs page
- Test navigation from docs page back to landing
- Test scroll-based TOC highlighting
- Test mobile menu includes docs link

### Property-Based Testing

Since this is primarily a UI/content feature, property-based testing is less applicable. However, we can test:

**Frontend Property Tests** (if using a testing library that supports it):
- Property 1: Generate random code snippets, verify they render in code blocks
- Property 7: Generate random code blocks, verify copy functionality works
- Property 8: Generate random TOC items, verify navigation works

Most testing will be example-based unit tests and manual testing.

### Manual Testing Checklist

- [ ] Navigate to `/docs` from landing page
- [ ] Verify all sections are present and readable
- [ ] Test copy button on each code block
- [ ] Verify clipboard contains correct code after copy
- [ ] Test TOC navigation for each section
- [ ] Verify TOC highlights correct section on scroll
- [ ] Test responsive design on mobile device
- [ ] Verify mobile TOC is collapsible
- [ ] Test navigation back to landing page
- [ ] Verify DOCS link is highlighted on docs page
- [ ] Test all code examples are syntax highlighted
- [ ] Verify all installation commands are in code blocks
- [ ] Check that all API methods are documented

## Implementation Notes

### Syntax Highlighting

Use a lightweight syntax highlighting library:
- **Option 1**: `react-syntax-highlighter` - Popular, well-maintained
- **Option 2**: `prism-react-renderer` - Smaller bundle size
- **Recommendation**: Use `react-syntax-highlighter` for ease of use

```javascript
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
```

### Clipboard API

Use modern Clipboard API with fallback:

```javascript
const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    // Fallback for older browsers
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    try {
      document.execCommand('copy');
      return true;
    } catch (err) {
      return false;
    } finally {
      document.body.removeChild(textArea);
    }
  }
};
```

### Scroll-based TOC Highlighting

Use Intersection Observer API for efficient scroll detection:

```javascript
useEffect(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          setActiveSection(entry.target.id);
        }
      });
    },
    { threshold: 0.5, rootMargin: '-100px 0px -50% 0px' }
  );

  sections.forEach((section) => {
    const element = document.getElementById(section.id);
    if (element) observer.observe(element);
  });

  return () => observer.disconnect();
}, []);
```

### Smooth Scrolling

Use native smooth scroll with fallback:

```javascript
const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
};
```

## Content Structure

### Documentation Sections

1. **Hero Section**
   - Title: "Mirmer AI Python SDK"
   - Subtitle: "A Python client library for the Mirmer AI multi-LLM consultation system"
   - Quick links: Installation, Quick Start, API Reference

2. **Installation**
   - pip installation command
   - uv installation command
   - Python version requirement (3.8+)
   - Link to PyPI package

3. **Authentication**
   - CLI authentication (`mirmer login`)
   - Programmatic authentication
   - Credential storage location (~/.mirmer/credentials.json)
   - Environment variable option (MIRMER_API_KEY)

4. **Quick Start**
   - Basic synchronous query example
   - Accessing stage1, stage2, stage3 data
   - Complete working example

5. **Basic Usage**
   - Synchronous client usage
   - Asynchronous client usage
   - Streaming responses
   - Error handling

6. **Conversation Management**
   - Creating conversations
   - Listing conversations
   - Searching conversations
   - Getting conversation details
   - Deleting conversations

7. **Usage Statistics**
   - Checking usage limits
   - Monitoring consumption
   - Understanding tiers

8. **Error Handling**
   - Exception hierarchy
   - AuthenticationError
   - RateLimitError
   - APIError
   - Best practices

9. **Configuration**
   - Client initialization options
   - Custom base URL
   - Timeout settings
   - Retry configuration

10. **API Reference**
    - Client class methods
    - AsyncClient class methods
    - Model classes (Response, Stage1Data, etc.)
    - Exception classes

### Code Examples

All code examples should be extracted from the existing SDK README and examples directory:
- `sdk/README.md` - Main examples
- `sdk/examples/basic_usage.py` - Basic usage
- `sdk/examples/streaming_example.py` - Streaming
- `sdk/examples/async_example.py` - Async usage
- `sdk/examples/conversation_management.py` - Conversations

## Design System Integration

### Colors

Use existing landing page colors:
- Primary: `#4ECDC4` (teal)
- Secondary: `#FFE66D` (yellow)
- Accent: `#FF6B6B` (red)
- Background: `#f5f5f5` (light gray)
- Text: `#000000` (black)
- Borders: `#000000` (black, 4px)

### Typography

- Headings: `font-black` (900 weight)
- Body: `font-bold` (700 weight)
- Code: `font-mono`

### Shadows

Neobrutalist shadows:
- Small: `shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]`
- Medium: `shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]`
- Large: `shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]`

### Code Block Styling

```css
.code-block {
  border: 4px solid black;
  background: #f5f5f5;
  box-shadow: 4px 4px 0px 0px rgba(0,0,0,1);
  font-family: 'Courier New', monospace;
  padding: 1rem;
  position: relative;
}

.copy-button {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  border: 2px solid black;
  background: #FFE66D;
  box-shadow: 2px 2px 0px 0px rgba(0,0,0,1);
  padding: 0.5rem 1rem;
  font-weight: 700;
}

.copy-button:hover {
  box-shadow: 4px 4px 0px 0px rgba(0,0,0,1);
  transform: translate(-2px, -2px);
}
```

## Responsive Design

### Desktop (≥1024px)
- TOC sidebar: Fixed position, 250px width
- Content: Max width 800px, centered
- Code blocks: Full width with horizontal scroll if needed

### Tablet (768px - 1023px)
- TOC: Collapsible at top of page
- Content: Full width with padding
- Code blocks: Full width with horizontal scroll

### Mobile (<768px)
- TOC: Collapsible menu button
- Content: Full width with minimal padding
- Code blocks: Full width, smaller font size
- Copy button: Always visible (no hover required)

## Performance Considerations

### Code Splitting

Load syntax highlighter lazily:
```javascript
const SyntaxHighlighter = lazy(() => 
  import('react-syntax-highlighter').then(module => ({
    default: module.Prism
  }))
);
```

### Image Optimization

No images required for this page (code-only documentation).

### Bundle Size

- Syntax highlighter: ~50KB gzipped
- Total page size: <100KB (excluding shared components)

## SEO Considerations

### Meta Tags

```html
<title>Mirmer AI Python SDK Documentation</title>
<meta name="description" content="Official Python SDK documentation for Mirmer AI multi-LLM consultation system. Installation, usage examples, and API reference." />
<meta name="keywords" content="Mirmer AI, Python SDK, API, documentation, multi-LLM, AI consultation" />
```

### Structured Data

Add JSON-LD structured data for documentation:
```json
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "Mirmer AI Python SDK Documentation",
  "description": "Official Python SDK documentation",
  "author": {
    "@type": "Organization",
    "name": "Mirmer AI"
  }
}
```

## Accessibility

### Keyboard Navigation

- All TOC links must be keyboard accessible
- Copy buttons must be keyboard accessible (Enter/Space)
- Skip to content link for screen readers
- Proper heading hierarchy (h1 → h2 → h3)

### Screen Readers

- Code blocks should have `aria-label` describing content
- Copy buttons should have descriptive `aria-label`
- TOC should have `nav` role with `aria-label="Table of Contents"`

### Color Contrast

- Ensure all text meets WCAG AA standards (4.5:1 ratio)
- Code syntax highlighting should maintain readability
- Focus indicators must be visible

## Deployment Considerations

### Route Configuration

Add route to `frontend/src/App.jsx`:
```javascript
<Route path="/docs" element={<DocsPage />} />
```

### Build Process

No changes to build process required. Standard Vite build handles new route.

### Analytics

Track documentation page views and section interactions:
- Page view: `/docs`
- Section view: `/docs#installation`, `/docs#quick-start`, etc.
- Copy button clicks
- TOC link clicks
