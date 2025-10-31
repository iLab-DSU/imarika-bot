# Imarika AI - React Frontend

Modern, responsive ChatGPT-style web interface for the Imarika Agricultural AI Assistant.

## Features

- 🎨 **Modern Design**: Clean, ChatGPT-inspired interface
- 🌙 **Dark Mode**: Built-in dark mode support
- 📱 **Responsive**: Works perfectly on mobile and desktop
- ⚡ **Fast**: Built with React 18 and TypeScript
- 🎭 **Animations**: Smooth Framer Motion animations
- 💾 **Persistence**: LocalStorage for chat history
- 🔧 **TypeScript**: Full type safety

## Tech Stack

- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Lucide React** for icons
- **LocalStorage** for data persistence

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

```bash
# Navigate to React app directory
cd frontend/react-app

# Install dependencies
npm install

# Start development server
npm start
```

The app will open at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

## Project Structure

```
src/
├── components/          # React components
│   ├── Header.tsx      # Top header bar
│   ├── Sidebar.tsx     # Chat history sidebar
│   ├── ChatArea.tsx    # Main chat interface
│   ├── ChatMessage.tsx # Individual message component
│   ├── ChatInput.tsx   # Message input with auto-resize
│   └── TypingIndicator.tsx # Animated typing dots
├── hooks/              # Custom React hooks
│   └── useLocalStorage.ts # LocalStorage persistence
├── types.ts            # TypeScript type definitions
├── App.tsx            # Main app component
├── index.tsx          # React entry point
└── index.css          # Tailwind CSS imports
```

## Key Components

### ChatMessage
- User and bot message bubbles
- Avatars and timestamps
- Smooth animations

### ChatInput
- Auto-resizing textarea
- Quick suggestion chips
- Enter to send, Shift+Enter for new line

### Sidebar
- Chat history with LocalStorage
- New chat functionality
- Responsive mobile drawer

### TypingIndicator
- Animated dots when AI is responding
- Matches ChatGPT behavior

## API Integration

The frontend is prepared to integrate with your backend:

```typescript
// In App.tsx - sendMessage function
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: content }),
});
```

Update the API endpoint to match your backend URL.

## Customization

### Colors
Edit `tailwind.config.js` to change the color scheme:

```javascript
colors: {
  primary: {
    500: '#22c55e', // Change primary color
    // ... other shades
  }
}
```

### Animations
Modify animations in components using Framer Motion:

```typescript
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
```

## Features Implemented

✅ ChatGPT-style layout  
✅ Dark mode support  
✅ Responsive design  
✅ Message animations  
✅ Typing indicator  
✅ Auto-resizing input  
✅ Chat history sidebar  
✅ LocalStorage persistence  
✅ TypeScript support  
✅ Production ready  

## Next Steps

1. Connect to your Python backend API
2. Add authentication if needed
3. Implement real-time features with WebSockets
4. Add more agricultural-specific features
5. Deploy to production

---

**Built for showcase and production use**