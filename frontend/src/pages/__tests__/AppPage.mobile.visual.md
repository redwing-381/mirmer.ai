# AppPage Mobile Responsive - Visual Test Guide

## Task 1: Mobile Hamburger Menu and Responsive Header

### Test Scenarios

#### 1. Mobile View (< 768px)

**Hamburger Menu Button:**
- [ ] Hamburger menu button is visible in the header
- [ ] Button has proper touch target size (min 44px)
- [ ] Button has brutalist styling (border, shadow)
- [ ] Clicking button opens the sidebar overlay

**Header Layout:**
- [ ] Header stacks vertically on mobile
- [ ] Logo and title are visible and properly sized
- [ ] User info card displays correctly with smaller text
- [ ] Logout button is full-width or properly sized
- [ ] All elements have adequate spacing

**Sidebar Overlay:**
- [ ] Sidebar slides in from left when hamburger is clicked
- [ ] Backdrop appears behind sidebar (semi-transparent black)
- [ ] Clicking backdrop closes the sidebar
- [ ] Sidebar is full-screen overlay (z-index: 50)
- [ ] Selecting a conversation closes the mobile menu
- [ ] Creating new conversation closes the mobile menu

#### 2. Tablet View (768px - 1024px)

**Header:**
- [ ] Header uses horizontal layout (flex-row)
- [ ] Hamburger menu is hidden
- [ ] Desktop toggle button is visible
- [ ] Elements are properly spaced

**Sidebar:**
- [ ] Sidebar behaves like desktop (fixed position)
- [ ] No overlay/backdrop on tablet
- [ ] Toggle button works to collapse/expand

#### 3. Desktop View (> 1024px)

**Header:**
- [ ] Full horizontal layout
- [ ] All elements at full size
- [ ] Hamburger menu hidden
- [ ] Desktop toggle button visible

**Sidebar:**
- [ ] Standard fixed sidebar behavior
- [ ] Toggle button works normally

### Manual Testing Steps

1. **Start the application:**
   ```bash
   cd frontend
   npm run dev
   ```

2. **Open browser DevTools:**
   - Press F12 or right-click → Inspect
   - Toggle device toolbar (Ctrl+Shift+M or Cmd+Shift+M)

3. **Test Mobile (375px width):**
   - Set viewport to iPhone SE (375x667)
   - Verify hamburger menu is visible
   - Click hamburger menu
   - Verify sidebar slides in
   - Verify backdrop appears
   - Click backdrop to close
   - Verify header stacks vertically
   - Check touch target sizes

4. **Test Tablet (768px width):**
   - Set viewport to iPad (768x1024)
   - Verify hamburger menu is hidden
   - Verify desktop toggle button appears
   - Verify header is horizontal
   - Test sidebar toggle

5. **Test Desktop (1440px width):**
   - Set viewport to desktop size
   - Verify full desktop layout
   - Test all functionality

### Expected Results

✅ **Mobile:**
- Hamburger menu visible and functional
- Header stacks vertically
- Sidebar as overlay with backdrop
- Touch-friendly sizes (min 44px)

✅ **Tablet:**
- Hamburger hidden
- Desktop toggle visible
- Horizontal header layout
- Fixed sidebar behavior

✅ **Desktop:**
- Full desktop experience
- No hamburger menu
- Standard sidebar toggle

### Requirements Validated

- **Requirement 1.5:** Mobile header shows essential elements and collapses secondary info
- Header stacks vertically on mobile ✓
- User info and logout properly displayed ✓
- Hamburger menu for sidebar access ✓

### Notes

- This is a visual/manual test document
- Automated tests for responsive behavior are in task 11 and 12
- Focus on visual appearance and interaction feel
- Test on actual devices if possible for best results
