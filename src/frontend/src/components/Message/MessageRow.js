import React from 'react';
import { globalStyles } from '../../styles';
import { MessageAvatar } from './MessageAvatar';
import { MessageBubble } from './MessageBubble';
import { MESSAGE_TYPES } from '../../constants';

export const MessageRow = ({ message }) => {
  const isUser = message.sender === MESSAGE_TYPES.USER;

  const rowStyle = {
    ...globalStyles.messageRow,
    ...(isUser ? globalStyles.messageRowUser : {})
  };

  return (
    <div style={rowStyle}>
      <MessageAvatar sender={message.sender} />
      <MessageBubble message={message} />
    </div>
  );
};