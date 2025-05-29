import React from 'react';
import { Bot, User } from 'lucide-react';
import { globalStyles } from '../../styles';
import { MESSAGE_TYPES } from '../../constants';

export const Avatar = ({ type, size = 32 }) => {
  const isUser = type === MESSAGE_TYPES.USER;

  const style = {
    ...globalStyles.avatar,
    width: `${size}px`,
    height: `${size}px`,
    ...(isUser ? globalStyles.userAvatar : globalStyles.botAvatar)
  };

  return (
    <div style={style}>
      {isUser ? (
        <User size={size * 0.5} color="white" />
      ) : (
        <Bot size={size * 0.5} color="white" />
      )}
    </div>
  );
};