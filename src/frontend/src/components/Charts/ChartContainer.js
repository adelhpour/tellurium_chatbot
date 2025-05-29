import React from 'react';
import { theme } from '../../styles';

export const ChartContainer = ({ children }) => {
  const style = {
    width: '100%',
    height: '300px',
    marginTop: theme.spacing.md,
    background: 'rgba(248, 250, 252, 0.5)',
    borderRadius: theme.borderRadius.md,
    padding: theme.spacing.lg,
    border: `1px solid ${theme.colors.border}`
  };

  return <div style={style}>{children}</div>;
};