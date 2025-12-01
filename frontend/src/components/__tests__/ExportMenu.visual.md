# ExportMenu Visual Test Guide

## Manual Visual Testing Checklist

### 1. Initial State
- [ ] Export button has 3px black border
- [ ] Export button has 4px shadow (bottom-right)
- [ ] Button text is bold and uppercase
- [ ] Download icon is visible and bold

### 2. Button Hover State
- [ ] Shadow reduces to 2px
- [ ] Button moves 2px down and right
- [ ] Transition is smooth (100ms)
- [ ] Cursor changes to pointer

### 3. Button Active State
- [ ] Shadow disappears completely
- [ ] Button moves 4px down and right
- [ ] Feels like pressing a physical button

### 4. Dropdown Open
- [ ] Dropdown has 3px black border
- [ ] Dropdown has 6px shadow (bottom-right)
- [ ] Header is yellow with black text
- [ ] Header text is bold and uppercase
- [ ] Dropdown animates in smoothly

### 5. Export Options
- [ ] Markdown option has emerald green background
- [ ] PDF option has amber yellow background
- [ ] JSON option has blue background
- [ ] Each option has 3px black border
- [ ] Icons are in white bordered boxes
- [ ] Labels are bold and uppercase
- [ ] Descriptions are visible and bold

### 6. Option Hover
- [ ] Background color lightens
- [ ] Option moves 1px to the right
- [ ] Transition is smooth
- [ ] Cursor changes to pointer

### 7. Loading State
- [ ] Icon box pulses
- [ ] Spinner appears next to label
- [ ] Spinner has black border
- [ ] Other options are disabled
- [ ] Disabled options have reduced opacity

### 8. Error State
- [ ] Error box appears at top of dropdown
- [ ] Error box has red background
- [ ] Error box has 2px black border
- [ ] Error message is bold and clear
- [ ] Dismiss button is visible
- [ ] Dropdown stays open for retry

### 9. Footer
- [ ] Footer has gray background
- [ ] Footer has 3px top border (black)
- [ ] Footer text is bold
- [ ] "💡 All 3 stages included" is visible

### 10. Backdrop
- [ ] Clicking backdrop closes dropdown
- [ ] Backdrop covers entire screen
- [ ] Backdrop is invisible but functional

## Color Verification

### Borders
- All borders should be: `#000000` (pure black)
- Border width should be: `3px` (except error: 2px)

### Shadows
- Button shadow: `4px 4px 0px 0px rgba(0,0,0,1)`
- Button hover: `2px 2px 0px 0px rgba(0,0,0,1)`
- Dropdown shadow: `6px 6px 0px 0px rgba(0,0,0,1)`

### Backgrounds
- Markdown: `#34d399` (emerald-400)
- PDF: `#fbbf24` (amber-400)
- JSON: `#60a5fa` (blue-400)
- Header: `#fde047` (yellow-300)
- Error: `#f87171` (red-400)
- Footer: `#f3f4f6` (gray-100)

## Accessibility Testing

### Keyboard Navigation
- [ ] Tab key focuses button
- [ ] Enter/Space opens dropdown
- [ ] Tab navigates through options
- [ ] Enter/Space activates option
- [ ] Escape closes dropdown

### Screen Reader
- [ ] Button has proper aria-label
- [ ] Options are announced correctly
- [ ] Loading state is announced
- [ ] Error state is announced

## Browser Testing

### Desktop
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)

### Mobile
- [ ] iOS Safari
- [ ] Android Chrome
- [ ] Touch interactions work

## Performance Testing

- [ ] Animations are smooth (60fps)
- [ ] No layout shifts
- [ ] No console errors
- [ ] No console warnings

## Edge Cases

### Long Conversation Titles
- [ ] Filename generation works
- [ ] No UI overflow

### Network Errors
- [ ] Error displays correctly
- [ ] Retry works after error
- [ ] Loading state resets

### Rapid Clicks
- [ ] No duplicate downloads
- [ ] Loading state prevents double-click
- [ ] UI remains stable

## Screenshot Checklist

Take screenshots of:
1. Initial button state
2. Button hover state
3. Dropdown open (all options)
4. Option hover state
5. Loading state
6. Error state
7. Mobile view

---

**Test Date:** _____________
**Tester:** _____________
**Browser:** _____________
**Result:** ☐ Pass ☐ Fail
**Notes:** _____________
