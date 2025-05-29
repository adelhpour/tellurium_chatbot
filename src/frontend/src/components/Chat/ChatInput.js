import React from 'react';
import { globalStyles, theme } from '../../styles';
import { Button } from '../UI/Button';
import { Send } from 'lucide-react';

export const ChatInput = ({
  inputText,
  setInputText,
  handleSend,
  handleKeyPress,
  disabled
}) => {
  // full‐width sticky footer
  const containerStyle = {
    ...globalStyles.glassmorphism,
    borderTop: `1px solid ${theme.colors.border}`,
    padding: theme.spacing.lg,
    position: 'sticky',
    bottom: 0,
    zIndex: 10
  };

  // inner row: centered, max 50% width of its parent (relative), shrinks down on small screens
  const innerStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: theme.spacing.md,
    width: '100%',
    maxWidth: '60%',
    margin: '0 auto'
  };

  // textarea fills remaining space in the row
  const textareaStyle = {
    flex: 1,
    padding: `${theme.spacing.sm} ${theme.spacing.md}`,
    border: `1px solid ${theme.colors.borderLight}`,
    borderRadius: theme.borderRadius.sm,
    height: '3rem',
    outline: 'none',
    resize: 'none',
    fontSize: theme.fontSize.md,
    fontFamily: 'inherit',
    boxSizing: 'border-box'
  };

  return (
    <div style={containerStyle}>
      <div style={innerStyle}>
        <textarea
          value={inputText}
          onChange={e => setInputText(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message…"
          rows={1}
          style={textareaStyle}
        />
        <Button
          onClick={handleSend}
          disabled={!inputText.trim() || disabled}
        >
          <Send size={20} />
        </Button>
      </div>
    </div>
  );
};
