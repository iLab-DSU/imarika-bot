# 🎨 Frontend - ChatGPT-Style Interface

## Overview
Clean, modern ChatGPT-style interface for the Imarika Agricultural AI Assistant. Designed for showcase and production use with familiar chat experience.

## 🏗️ Architecture

```
frontend/
├── chatgpt_style.py        # Main ChatGPT-style interface
├── components/              # Legacy components (for reference)
├── utils/                  # Utility functions
├── requirements.txt         # Frontend dependencies
└── README.md              # This file
```

## 🎯 Key Features

### 🎨 ChatGPT-Style Design
- **Clean Interface**: Minimalist ChatGPT-inspired design
- **Message Bubbles**: Proper chat bubbles with user/assistant styling
- **Responsive**: Mobile-friendly responsive layout
- **Typing Indicators**: Animated typing dots during processing

### 💬 Simple Chat Experience
- **Single Page**: Focused chat interface
- **Quick Suggestions**: Pre-built agricultural queries
- **Clean Layout**: No distracting sidebars or menus
- **Familiar UX**: ChatGPT-like user experience

### 💬 True Chat Interface
- **Message Bubbles**: User messages on right, AI on left
- **Avatar System**: User and AI avatars for clear identification
- **Typing Animation**: Real typing indicator with animated dots
- **Smooth Scrolling**: Auto-scroll to latest messages

## 🚀 Usage

### Running the Frontend
```bash
# Run the ChatGPT-style interface
streamlit run chatgpt_style.py

# Or from project root
python run_frontend.py
```

## 🎨 Design System

### Color Palette
- **Primary**: #10a37f (ChatGPT Green)
- **User Messages**: #007bff (Blue)
- **Assistant Messages**: #f1f3f4 (Light Gray)
- **Background**: #ffffff (White)
- **Text**: #2d3748 (Dark Gray)

### Message Styling
- **User**: Blue bubbles on the right with user avatar
- **Assistant**: Gray bubbles on the left with AI avatar
- **Rounded Corners**: 18px radius with cut corners
- **Proper Spacing**: 20px between messages

### Responsive Design
- **Desktop**: Full-width chat with 800px max container
- **Mobile**: Optimized for mobile with 85% message width
- **Adaptive**: Suggestions stack vertically on mobile

## 🔧 Features

### Chat Interface
- Clean header with Imarika branding
- Message bubbles with proper alignment
- Typing indicator with animated dots
- Quick suggestion chips
- Sticky input at bottom

### User Experience
- Familiar ChatGPT-style layout
- Smooth animations and transitions
- Auto-scroll to new messages
- Clear visual hierarchy

---

**ChatGPT-inspired design for familiar user experience**