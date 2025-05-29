import React, { useEffect } from 'react';
import { globalStyles, theme } from '../../styles';
import { MessageAvatar } from './MessageAvatar';
import { MESSAGE_TYPES } from '../../constants';

export const TypingIndicator = () => {
  const containerStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: theme.spacing.md
  };

  const bubbleStyle = {
    background: theme.colors.white,
    padding: `${theme.spacing.md} ${theme.spacing.lg}`,
    borderRadius: theme.borderRadius.lg,
    boxShadow: theme.shadows.sm,
    border: `1px solid ${theme.colors.border}`
  };

  const dotsStyle = {
    display: 'flex',
    gap: theme.spacing.xs
  };

  const dotStyle = {
    width: '8px',
    height: '8px',
    backgroundColor: theme.colors.textSecondary,
    borderRadius: theme.borderRadius.full,
    animation: 'bounce 1.4s infinite ease-in-out'
  };

  // Add keyframes for animation
  useEffect(() => {
    const styleSheet = document.createElement('style');
    styleSheet.textContent = `
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
      if (document.head.contains(styleSheet)) {
        document.head.removeChild(styleSheet);
      }
    };
  }, []);

  return (
    <div style={containerStyle}>
      <MessageAvatar sender={MESSAGE_TYPES.BOT} />
      <div style={bubbleStyle}>
        <div style={dotsStyle}>
          <div style={dotStyle}></div>
          <div style={dotStyle} className="dot-delay-1"></div>
          <div style={dotStyle} className="dot-delay-2"></div>
        </div>
      </div>
    </div>
  );
};