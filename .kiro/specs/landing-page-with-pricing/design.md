# Landing Page Design Document

## Overview

The landing page serves as the public-facing entry point for Mirmer AI, designed to convert visitors into users through clear value proposition communication, transparent pricing display, and frictionless authentication. The page will be built as a React component that integrates with the existing Firebase authentication system and routing structure.

## Architecture

### Component Structure

```
LandingPage (new)
├── Navigation
│   ├── Logo
│   ├── NavLinks (Features, Pricing, Docs)
│   └── AuthButtons (Sign In, Get Started)
├── HeroSection
│   ├── Headline
│   ├── Subheadline
│   ├── CTAButton
│   └── HeroVisual
├── FeaturesSection
│   ├── FeatureCard (3-Stage Process)
│   ├── FeatureCard (Multiple Models)
│   ├── FeatureCard (Peer Review)
│   └── FeatureCard (Synthesis)
├── PricingSection
│   ├── PricingCard (Free)
│   ├── PricingCard (Pro) - highlighted
│   └── PricingCard (Enterprise)
├── SocialProofSection
│   ├── StatsDisplay
│   └── TestimonialCarousel (future)
└── Footer
    ├── FooterLinks
    ├── SocialLinks
    └── Copyright
```

### Routing Integration

The application will use React Router to handle navigation between the landing page and the authenticated app:

- `/` - Landing page (public)
- `/app` - Main application (authenticated)
- Redirect logic: If user is authenticated and visits `/`, redirect to `/app`

### State Management

- **Authentication State**: Shared via Firebase `onAuthStateChanged` listener
- **Modal State**: Local state for authentication modal visibility
- **Scroll State**: Track scroll position for sticky navigation effects
- **Mobile Menu State**: Toggle state for responsive hamburger menu

## Components and Interfaces

### 1. LandingPage Component

**Purpose**: Root component for the public landing page

**Props**: None (reads auth state from Firebase context)

**State**:
```javascript
{
  showAuthModal: boolean,
  mobileMenuOpen: boolean,
  scrolled: boolean
}
```

**Key Methods**:
- `handleGetStarted()`: Opens auth modal
- `handleSignIn()`: Opens auth modal
- `handleScroll()`: Updates sticky nav state

### 2. Navigation Component

**Purpose**: Fixed top navigation bar with responsive behavior

**Props**:
```javascript
{
  isScrolled: boolean,
  user: User | null,
  onSignIn: () => void,
  onGetStarted: () => void
}
```

**Responsive Behavior**:
- Desktop (≥768px): Horizontal menu with all links visible
- Mobile (<768px): Hamburger menu with slide-out drawer

**Visual States**:
- Default: Transparent background with white text
- Scrolled: White background with shadow and dark text
- Authenticated: Shows "Go to App" button instead of auth buttons

### 3. HeroSection Component

**Purpose**: Above-the-fold section with primary value proposition

**Content**:
- **Headline**: "Get Better Answers from Multiple AI Minds"
- **Subheadline**: "Mirmer AI consults 4 leading AI models, ranks their responses, and synthesizes the best answer for you"
- **CTA Button**: "Start Free - 10 Queries/Day"
- **Visual**: Animated illustration showing the 3-stage council process

**Design Pattern**: Full-width section with centered content, gradient background

### 4. FeaturesSection Component

**Purpose**: Explain the 3-stage council process and key benefits

**Layout**: 2x2 grid on desktop, single column on mobile

**Feature Cards**:

1. **Stage 1: Individual Responses**
   - Icon: 🤖
   - Title: "4 AI Models Respond"
   - Description: "GPT-4, Claude, Gemini, and Llama each provide their unique perspective"

2. **Stage 2: Peer Review**
   - Icon: ⚖️
   - Title: "Models Rank Each Other"
   - Description: "Each AI evaluates and ranks the other responses for quality and accuracy"

3. **Stage 3: Final Synthesis**
   - Icon: 🎯
   - Title: "Chairman Synthesizes"
   - Description: "A lead model combines the best insights into one comprehensive answer"

4. **Benefit: Better Decisions**
   - Icon: ✨
   - Title: "Collective Intelligence"
   - Description: "Get more balanced, well-reasoned answers than any single AI can provide"

### 5. PricingSection Component

**Purpose**: Display pricing tiers with clear feature comparison

**Layout**: 3-column grid on desktop, stacked cards on mobile

**Pricing Tiers**:

#### Free Tier
- **Price**: $0/month
- **Queries**: 10 per day
- **Features**:
  - 3-stage council process
  - 4 AI models
  - Conversation history
  - Google Sign-In
- **CTA**: "Get Started Free"
- **Style**: Standard card

#### Pro Tier (Recommended)
- **Price**: $19/month
- **Queries**: 100 per day
- **Features**:
  - Everything in Free
  - Priority processing
  - Extended history (90 days)
  - Email support
- **CTA**: "Start Pro Trial"
- **Style**: Highlighted with border and badge

#### Enterprise Tier
- **Price**: Custom
- **Queries**: Unlimited
- **Features**:
  - Everything in Pro
  - Custom model selection
  - API access
  - Dedicated support
  - SLA guarantee
- **CTA**: "Contact Sales"
- **Style**: Standard card

**Interaction**:
- Clicking any CTA triggers authentication flow
- After auth, Free users go directly to app
- Pro/Enterprise users see upgrade flow (future implementation)

### 6. SocialProofSection Component

**Purpose**: Build trust with statistics and social proof

**Content**:
- **Stat 1**: "10,000+ Queries Processed"
- **Stat 2**: "4 AI Models Consulted"
- **Stat 3**: "95% User Satisfaction" (placeholder)

**Future Enhancement**: Add testimonial carousel

### 7. Footer Component

**Purpose**: Provide secondary navigation and legal links

**Content**:
- **Column 1**: Product links (Features, Pricing, Docs)
- **Column 2**: Company links (About, Blog, Careers)
- **Column 3**: Legal links (Privacy, Terms, Security)
- **Column 4**: Social links (Twitter, GitHub, Discord)
- **Bottom**: Copyright and version info

### 8. AuthModal Component (Enhanced)

**Purpose**: Reuse existing Auth component in modal overlay

**Enhancement**: Wrap existing `Auth.jsx` component in a modal overlay that can be triggered from landing page CTAs

**Props**:
```javascript
{
  isOpen: boolean,
  onClose: () => void,
  onSuccess: () => void
}
```

## Data Models

### Pricing Tier Model

```javascript
{
  id: string,              // 'free', 'pro', 'enterprise'
  name: string,            // Display name
  price: number | string,  // Monthly price or 'Custom'
  queryLimit: string,      // '10/day', '100/day', 'Unlimited'
  features: string[],      // List of features
  highlighted: boolean,    // Show as recommended
  ctaText: string,         // Button text
  ctaAction: string        // 'signup', 'upgrade', 'contact'
}
```

### Feature Model

```javascript
{
  id: string,
  icon: string,           // Emoji or icon component
  title: string,
  description: string,
  order: number
}
```

## Styling and Design System

### Color Palette

- **Primary**: Blue (#3B82F6) - CTAs and accents
- **Secondary**: Indigo (#6366F1) - Gradients and highlights
- **Success**: Green (#10B981) - Pro tier highlight
- **Neutral**: Gray scale (#F9FAFB to #111827)
- **Background**: White (#FFFFFF) and light gray (#F9FAFB)

### Typography

- **Headings**: Inter font family, bold weights (600-800)
  - H1: 3.5rem (56px) on desktop, 2.5rem (40px) on mobile
  - H2: 2.5rem (40px) on desktop, 2rem (32px) on mobile
  - H3: 1.5rem (24px)
- **Body**: Inter font family, regular (400) and medium (500)
  - Base: 1rem (16px)
  - Small: 0.875rem (14px)

### Spacing System

- Use Tailwind's spacing scale (4px base unit)
- Section padding: py-16 (64px) on desktop, py-12 (48px) on mobile
- Container max-width: 1280px
- Content max-width: 768px for text-heavy sections

### Responsive Breakpoints

- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Animation and Transitions

- **Scroll Animations**: Fade-in and slide-up on scroll (using Intersection Observer)
- **Hover Effects**: Scale and shadow transitions on cards (duration: 200ms)
- **Navigation**: Smooth scroll to sections (behavior: smooth)
- **Modal**: Fade-in overlay with slide-down content (duration: 300ms)

## Error Handling

### Authentication Errors

- **Network Error**: Display toast notification "Connection failed. Please check your internet."
- **Auth Popup Blocked**: Display inline message "Please allow popups to sign in"
- **Auth Cancelled**: Silent handling, no error message
- **Unknown Error**: Display generic message "Sign in failed. Please try again."

### Loading States

- **Initial Page Load**: Show nothing (instant render)
- **Auth in Progress**: Show spinner on CTA button
- **Redirect**: Show full-page loading spinner during navigation

## Testing Strategy

### Unit Tests

- Component rendering tests for each major component
- Props validation and default values
- Event handler invocation
- Conditional rendering based on auth state

### Integration Tests

- Navigation flow from landing to authenticated app
- Authentication modal open/close behavior
- Responsive layout changes at breakpoints
- Scroll-triggered navigation style changes

### Visual Regression Tests

- Screenshot comparison for each section
- Mobile vs desktop layouts
- Hover states on interactive elements
- Modal overlay appearance

### Accessibility Tests

- Keyboard navigation through all interactive elements
- Screen reader compatibility (ARIA labels)
- Color contrast ratios (WCAG AA compliance)
- Focus indicators on all focusable elements
- Touch target sizes (minimum 44x44px)

### Performance Tests

- Lighthouse score targets:
  - Performance: > 90
  - Accessibility: 100
  - Best Practices: > 90
  - SEO: > 90
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.0s
- Cumulative Layout Shift: < 0.1

## Implementation Notes

### Integration with Existing App

1. **Routing Setup**: Add React Router to handle `/` and `/app` routes
2. **Auth Check**: Wrap App component with route protection
3. **Redirect Logic**: Authenticated users visiting `/` redirect to `/app`
4. **Shared Components**: Reuse existing Auth component with modal wrapper

### Third-Party Dependencies

- **React Router**: For routing (`react-router-dom`)
- **Lucide React**: For icons (optional, can use emojis)
- **Framer Motion**: For scroll animations (optional)
- **React Intersection Observer**: For scroll-triggered animations

### SEO Considerations

- Add `<title>` and meta tags for social sharing
- Include structured data (JSON-LD) for organization
- Add Open Graph tags for social media previews
- Ensure semantic HTML structure (h1, h2, nav, main, footer)
- Add alt text for all images

### Future Enhancements

1. **Testimonials**: Add user testimonials with photos
2. **Video Demo**: Embed product demo video in hero section
3. **Live Chat**: Add support chat widget
4. **A/B Testing**: Test different headlines and CTAs
5. **Analytics**: Track conversion funnel (view → signup → first query)
6. **Blog Integration**: Add recent blog posts section
7. **Comparison Table**: Detailed feature comparison matrix
8. **FAQ Section**: Common questions accordion
