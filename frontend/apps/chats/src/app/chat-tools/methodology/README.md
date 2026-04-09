# Methodology Page

## Overview
A comprehensive page showing Dish-Chat's methodology, evolution, implementation details, and user preferences.

## Features

### 1. Overview Tab
- Core principles (Transparency, Tool-Augmented Intelligence, Extended Thinking, etc.)
- How it works (step-by-step process)
- Visual timeline of operation

### 2. Evolution Tab
- Historical timeline of development phases
- Status indicators (completed, in-progress, planned)
- Future roadmap

### 3. Implementation Tab
- Technical architecture details
- Frontend/Backend structure
- LLM integration specifics
- Tool system overview
- Data flow diagram

### 4. Preferences Tab
- User-customizable settings stored in localStorage
- Reasoning depth preference
- Tool usage preference
- Response style preference
- Custom instructions (free-form textarea)
- Save/Reset functionality

## User Experience

### Customization
Users can:
- View their current preferences
- Edit each preference individually
- Save changes to localStorage
- Reset to defaults if needed

### Preferences Schema
```json
{
  "reasoning_depth": "balanced|quick|deep|comprehensive",
  "tool_preference": "always_ask|ask_first|auto_approve|fully_automatic",
  "response_style": "concise|balanced|detailed|comprehensive",
  "custom_instructions": "free-form text"
}
```

## Navigation
- Accessible from main chat interface
- Back button returns to chat
- All content is client-side rendered for instant loading

## Technical Details
- **Framework**: Next.js 16 App Router
- **UI Library**: Ant Design 6.x
- **Storage**: Browser localStorage for preferences
- **State Management**: React hooks (useState, useEffect)
- **Styling**: Inline styles + Ant Design theme

## File Structure
```
apps/chats/src/app/chat-tools/methodology/
└── page.tsx (592 lines, ~23KB)
```

## Testing Checklist
- [ ] Page renders without errors
- [ ] All 4 tabs are accessible
- [ ] Timeline displays correctly
- [ ] Preference editing works
- [ ] Save preferences persists to localStorage
- [ ] Reset preferences clears localStorage
- [ ] Back button navigates correctly
- [ ] Responsive on different screen sizes
- [ ] No console errors
- [ ] TypeScript compiles successfully

## Integration Points
- Uses same navigation pattern as journals/visualizer
- Shares layout components with other chat-tools
- Follows existing Next.js app structure
- Compatible with current authentication flow
