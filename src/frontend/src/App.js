import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User } from 'lucide-react';

const ModernChatbot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your AI assistant. How can I help you today?",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
  const text = inputText.trim();
  if (!text) return;

  // 1) add the user message
  const userMessage = {
    id: Date.now(),
    text,
    sender: 'user',
    timestamp: new Date(),
  };
  setMessages(prev => [...prev, userMessage]);
  setInputText('');
  setIsTyping(true);

  try {
    // 2) call your Flask API
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
    });
    const payload = await res.json();

    // 3) add the bot’s response
    const botMessage = {
      id: Date.now() + 1,
      text: payload.message,
      sender: 'bot',
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, botMessage]);
  } catch (err) {
    console.error('chat error', err);
    // you could push an error message here
  } finally {
    setIsTyping(false);
  }
};

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Styles
  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    },
    header: {
      background: 'rgba(255, 255, 255, 0.8)',
      backdropFilter: 'blur(10px)',
      borderBottom: '1px solid #e2e8f0',
      padding: '16px',
      boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)'
    },
    headerContent: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px'
    },
    avatar: {
      width: '40px',
      height: '40px',
      background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
      borderRadius: '50%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    },
    headerText: {
      margin: 0
    },
    title: {
      fontSize: '18px',
      fontWeight: '600',
      color: '#1e293b',
      margin: 0
    },
    subtitle: {
      fontSize: '14px',
      color: '#64748b',
      margin: 0
    },
    messagesContainer: {
      flex: 1,
      overflowY: 'auto',
      padding: '16px',
      display: 'flex',
      flexDirection: 'column',
      gap: '16px'
    },
    messageRow: {
      display: 'flex',
      alignItems: 'flex-start',
      gap: '12px',
      animation: 'slideIn 0.3s ease-out'
    },
    messageRowUser: {
      flexDirection: 'row-reverse'
    },
    messageAvatar: {
      width: '32px',
      height: '32px',
      borderRadius: '50%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0
    },
    botAvatar: {
      background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)'
    },
    userAvatar: {
      background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
    },
    messageBubble: {
      maxWidth: '70%',
      padding: '12px 16px',
      borderRadius: '18px',
      position: 'relative'
    },
    userBubble: {
      background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
      color: 'white'
    },
    botBubble: {
      background: 'white',
      color: '#1e293b',
      boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
      border: '1px solid #e2e8f0'
    },
    messageText: {
      fontSize: '14px',
      lineHeight: '1.5',
      margin: 0
    },
    timestamp: {
      fontSize: '12px',
      marginTop: '4px',
      opacity: 0.7
    },
    typingContainer: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px'
    },
    typingBubble: {
      background: 'white',
      padding: '12px 16px',
      borderRadius: '18px',
      boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
      border: '1px solid #e2e8f0'
    },
    typingDots: {
      display: 'flex',
      gap: '4px'
    },
    dot: {
      width: '8px',
      height: '8px',
      backgroundColor: '#64748b',
      borderRadius: '50%',
      animation: 'bounce 1.4s infinite ease-in-out'
    },
    inputArea: {
      background: 'rgba(255, 255, 255, 0.8)',
      backdropFilter: 'blur(10px)',
      borderTop: '1px solid #e2e8f0',
      padding: '16px'
    },
    inputContainer: {
      display: 'flex',
      alignItems: 'flex-end',
      gap: '12px',
      maxWidth: '1200px',
      margin: '0 auto'
    },
    inputWrapper: {
      flex: 1,
      position: 'relative'
    },
    textarea: {
      width: '100%',
      padding: '12px 16px',
      borderRadius: '18px',
      border: '1px solid #cbd5e1',
      outline: 'none',
      resize: 'none',
      minHeight: '48px',
      maxHeight: '120px',
      background: 'rgba(255, 255, 255, 0.8)',
      backdropFilter: 'blur(10px)',
      fontSize: '14px',
      fontFamily: 'inherit',
      transition: 'all 0.2s ease',
      boxSizing: 'border-box'
    },
    textareaFocus: {
      borderColor: '#3b82f6',
      boxShadow: '0 0 0 2px rgba(59, 130, 246, 0.2)'
    },
    sendButton: {
      width: '48px',
      height: '48px',
      background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
      color: 'white',
      border: 'none',
      borderRadius: '50%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      cursor: 'pointer',
      transition: 'all 0.2s ease',
      boxShadow: '0 4px 12px rgba(59, 130, 246, 0.3)'
    },
    sendButtonHover: {
      transform: 'scale(1.05)',
      boxShadow: '0 6px 16px rgba(59, 130, 246, 0.4)'
    },
    sendButtonDisabled: {
      background: 'linear-gradient(135deg, #cbd5e1 0%, #94a3b8 100%)',
      cursor: 'not-allowed',
      transform: 'none',
      boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
    }
  };

  // Add keyframes for animations
  useEffect(() => {
    const styleSheet = document.createElement('style');
    styleSheet.textContent = `
      @keyframes slideIn {
        from {
          opacity: 0;
          transform: translateY(10px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }
      
      @keyframes bounce {
        0%, 80%, 100% {
          transform: scale(0);
        }
        40% {
          transform: scale(1);
        }
      }
      
      .dot-delay-1 {
        animation-delay: -0.32s;
      }
      
      .dot-delay-2 {
        animation-delay: -0.16s;
      }
    `;
    document.head.appendChild(styleSheet);

    return () => {
      document.head.removeChild(styleSheet);
    };
  }, []);

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <div style={styles.headerContent}>
          <div style={styles.avatar}>
            <Bot size={20} color="white" />
          </div>
          <div style={styles.headerText}>
            <h1 style={styles.title}>AI Assistant</h1>
            <p style={styles.subtitle}>Always here to help</p>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div style={styles.messagesContainer}>
        {messages.map((message) => (
          <div
            key={message.id}
            style={{
              ...styles.messageRow,
              ...(message.sender === 'user' ? styles.messageRowUser : {})
            }}
          >
            {/* Avatar */}
            <div style={{
              ...styles.messageAvatar,
              ...(message.sender === 'user' ? styles.userAvatar : styles.botAvatar)
            }}>
              {message.sender === 'user' ? (
                <User size={16} color="white" />
              ) : (
                <Bot size={16} color="white" />
              )}
            </div>

            {/* Message Bubble */}
            <div style={{
              ...styles.messageBubble,
              ...(message.sender === 'user' ? styles.userBubble : styles.botBubble)
            }}>
              <p style={styles.messageText}>{message.text}</p>
              <p style={styles.timestamp}>
                {formatTime(message.timestamp)}
              </p>
            </div>
          </div>
        ))}

        {/* Typing Indicator */}
        {isTyping && (
          <div style={styles.typingContainer}>
            <div style={{ ...styles.messageAvatar, ...styles.botAvatar }}>
              <Bot size={16} color="white" />
            </div>
            <div style={styles.typingBubble}>
              <div style={styles.typingDots}>
                <div style={styles.dot}></div>
                <div style={{ ...styles.dot }} className="dot-delay-1"></div>
                <div style={{ ...styles.dot }} className="dot-delay-2"></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div style={styles.inputArea}>
        <div style={styles.inputContainer}>
          <div style={styles.inputWrapper}>
            <textarea
              ref={inputRef}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              onFocus={(e) => {
                e.target.style.borderColor = '#3b82f6';
                e.target.style.boxShadow = '0 0 0 2px rgba(59, 130, 246, 0.2)';
              }}
              onBlur={(e) => {
                e.target.style.borderColor = '#cbd5e1';
                e.target.style.boxShadow = 'none';
              }}
              placeholder="Type your message..."
              style={styles.textarea}
              rows="1"
            />
          </div>

          <button
            onClick={handleSend}
            disabled={!inputText.trim() || isTyping}
            onMouseEnter={(e) => {
              if (!e.target.disabled) {
                Object.assign(e.target.style, styles.sendButtonHover);
              }
            }}
            onMouseLeave={(e) => {
              if (!e.target.disabled) {
                e.target.style.transform = 'scale(1)';
                e.target.style.boxShadow = '0 4px 12px rgba(59, 130, 246, 0.3)';
              }
            }}
            style={{
              ...styles.sendButton,
              ...(!inputText.trim() || isTyping ? styles.sendButtonDisabled : {})
            }}
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ModernChatbot;