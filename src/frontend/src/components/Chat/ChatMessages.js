import React from 'react';
import { MessageRow } from '../Message';
import { TypingIndicator } from '../Message';
import { theme } from '../../styles';

export const ChatMessages = ({ messages, isTyping, messagesEndRef }) => {
  const style = {
    flex: 1,
    overflowY: 'auto',
    padding: theme.spacing.lg,
    display: 'flex',
    flexDirection: 'column',
    gap: theme.spacing.lg
  };

  return (
    <div style={style}>
      {messages.map(msg => (
        <MessageRow key={msg.id} message={msg} />
      ))}

      {isTyping && <TypingIndicator />}

      {/* Anchor for auto-scrolling */}
      <div ref={messagesEndRef} />
    </div>
  );
};
