import React from 'react';
import { globalStyles, theme } from '../../styles';
import { Avatar } from '../UI';
import { MESSAGE_TYPES } from '../../constants';

export const ChatHeader = ({ title, subtitle }) => {
  const style = {
    ...globalStyles.glassmorphism,
    borderBottom: `1px solid ${theme.colors.border}`,
    padding: theme.spacing.lg,
    boxShadow: theme.shadows.sm,
    position: 'sticky',
    top: 0,
    zIndex: 10
  };

  return (
    <div style={style}>
      <div style={{ display: 'flex', alignItems: 'center', gap: theme.spacing.md }}>
        {/* Bot avatar */}
        <Avatar type={MESSAGE_TYPES.BOT} size={40} />
        <div>
          <h1 style={{ margin: 0, fontSize: theme.fontSize.lg, color: theme.colors.text }}>
            {title}
          </h1>
          <p style={{ margin: 0, fontSize: theme.fontSize.sm, color: theme.colors.textSecondary }}>
            {subtitle}
          </p>
        </div>
      </div>
    </div>
  );
};
