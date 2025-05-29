import React from 'react';
import { Avatar } from '../UI';

export const MessageAvatar = ({ sender }) => (
  <Avatar type={sender} size={32} />
);