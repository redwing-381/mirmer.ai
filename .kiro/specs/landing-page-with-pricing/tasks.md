# Implementation Plan

- [ ] 1. Set up routing infrastructure
  - Install react-router-dom package
  - Create routing configuration in main.jsx to handle `/` (landing) and `/app` (authenticated app) routes
  - Implement redirect logic: authenticated users visiting `/` redirect to `/app`
  - _Requirements: 3.4, 6.4_

- [ ] 2. Create core landing page structure and navigation
  - [ ] 2.1 Implement LandingPage root component
    - Create `frontend/src/pages/LandingPage.jsx` with state management for auth modal, mobile menu, and scroll position
    - Add scroll event listener to track navigation bar state changes
    - Integrate Firebase auth state listener to detect authenticated users
    - _Requirements: 1.1, 3.1, 6.1_
  
  - [ ] 2.2 Build Navigation component with responsive behavior
    - Create `frontend/src/components/landing/Navigation.jsx` with fixed positioning
    - Implement desktop horizontal menu and mobile hamburger menu with slide-out drawer
    - Add dynamic styling based on scroll state (transparent → white background with shadow)
    - Implement conditional rendering: show "Go to App" for authenticated users, "Sign In" and "Get Started" for guests
    - Add smooth scroll navigation to page sections
    - _Requirements: 3.1, 4.3, 6.1, 6.2, 6.3, 6.5_

- [ ] 3. Build hero section with value proposition
  - Create `frontend/src/components/landing/HeroSection.jsx` with gradient background
  - Implement headline "Get Better Answers from Multiple AI Minds" and subheadline explaining the 3-stage process
  - Add primary CTA button "Start Free - 10 Queries/Day" that triggers auth modal
  - Create visual illustration of the 3-stage council process using CSS and emojis
  - Ensure responsive typography (3.5rem desktop, 2.5rem mobile for headline)
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 4.4_

- [ ] 4. Implement features section
  - Create `frontend/src/components/landing/FeaturesSection.jsx` with 2x2 grid layout (desktop) and single column (mobile)
  - Build reusable `FeatureCard.jsx` component with icon, title, and description props
  - Implement four feature cards: "4 AI Models Respond", "Models Rank Each Other", "Chairman Synthesizes", and "Collective Intelligence"
  - Add hover effects with scale and shadow transitions (200ms duration)
  - _Requirements: 5.1, 5.2, 5.3, 4.1, 4.2_

- [ ] 5. Create pricing section with three tiers
  - [ ] 5.1 Build PricingSection component and card layout
    - Create `frontend/src/components/landing/PricingSection.jsx` with 3-column grid (desktop) and stacked layout (mobile)
    - Build reusable `PricingCard.jsx` component accepting tier data as props
    - Implement responsive layout that stacks cards vertically on mobile
    - _Requirements: 2.1, 4.2_
  
  - [ ] 5.2 Implement pricing tier data and cards
    - Define pricing tier data model with Free ($0, 10/day), Pro ($19, 100/day, highlighted), and Enterprise (Custom, Unlimited)
    - Render three pricing cards with prices, query limits, feature lists, and CTAs
    - Add visual emphasis to Pro tier (border, badge, scale effect)
    - Wire up CTA buttons to trigger auth modal or appropriate action
    - _Requirements: 2.2, 2.3, 2.4, 2.5, 2.6_

- [ ] 6. Add social proof and footer sections
  - Create `frontend/src/components/landing/SocialProofSection.jsx` displaying three statistics with large numbers and labels
  - Create `frontend/src/components/landing/Footer.jsx` with four columns: Product, Company, Legal, and Social links
  - Add copyright notice and version info to footer bottom
  - Ensure footer links are properly styled and accessible (minimum 44x44px touch targets)
  - _Requirements: 5.4, 5.5, 4.5_

- [ ] 7. Implement authentication modal integration
  - Create `frontend/src/components/landing/AuthModal.jsx` wrapper component with modal overlay
  - Integrate existing `Auth.jsx` component inside modal with close button
  - Implement modal open/close state management and backdrop click handling
  - Add fade-in animation for overlay and slide-down animation for content (300ms duration)
  - Handle successful authentication: close modal and redirect to `/app`
  - _Requirements: 3.2, 3.3, 3.4, 3.5_

- [ ] 8. Add responsive design and mobile optimizations
  - Implement responsive breakpoints (mobile <768px, tablet 768-1024px, desktop >1024px)
  - Ensure all text maintains minimum 14px font size on mobile devices
  - Verify all interactive elements have minimum 44x44px touch targets on mobile
  - Test layout from 320px to 2560px screen widths
  - Add mobile-specific spacing adjustments (py-12 instead of py-16)
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 9. Refactor App.jsx to work with routing
  - Move existing App.jsx content to `frontend/src/pages/AppPage.jsx`
  - Update App.jsx to be a router wrapper that renders LandingPage or AppPage based on route
  - Ensure auth state is properly shared between landing page and app page
  - Test navigation flow: landing → auth → app and direct `/app` access
  - _Requirements: 3.4, 3.5, 6.4_

- [ ] 10. Add SEO and meta tags
  - Add document title, meta description, and Open Graph tags to index.html
  - Implement semantic HTML structure (header, main, section, footer tags)
  - Add alt text for any images or visual elements
  - Include JSON-LD structured data for organization
  - _Requirements: 1.5_

- [ ]* 11. Performance optimization
  - Implement lazy loading for below-the-fold sections
  - Add Intersection Observer for scroll-triggered animations
  - Optimize images and use appropriate formats
  - Verify page load time is under 2 seconds
  - Run Lighthouse audit and achieve target scores (Performance >90, Accessibility 100)
  - _Requirements: 1.5_

- [ ]* 12. Accessibility enhancements
  - Add ARIA labels to all interactive elements
  - Implement keyboard navigation for modal and mobile menu
  - Verify color contrast ratios meet WCAG AA standards
  - Add focus indicators to all focusable elements
  - Test with screen reader for proper announcement flow
  - _Requirements: 4.5_
