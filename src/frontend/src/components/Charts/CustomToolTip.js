import React from 'react';
import { theme } from '../../styles';

export const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload || !payload.length) return null;

  const style = {
    background: 'rgba(255, 255, 255, 0.95)',
    border: `1px solid ${theme.colors.border}`,
    borderRadius: theme.borderRadius.sm,
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
    padding: theme.spacing.sm
  };

  return (
    <div style={style}>
      <p style={{ margin: 0, fontSize: theme.fontSize.sm }}>
        {`${label}: ${payload[0].value}`}
      </p>
    </div>
  );
};