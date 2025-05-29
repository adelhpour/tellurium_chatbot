import React, { useState } from 'react';
import { theme } from '../../styles';

export const Button = ({
  children,
  onClick,
  disabled = false,
  variant = 'primary',
  size = 'md',
  ...props
}) => {
  const [isHovered, setIsHovered] = useState(false);

  const baseStyle = {
    border: 'none',
    borderRadius: theme.borderRadius.full,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: disabled ? 'not-allowed' : 'pointer',
    transition: 'all 0.2s ease',
    fontFamily: 'inherit',
  };

  const sizeStyles = {
    sm: { width: '32px', height: '32px' },
    md: { width: '48px', height: '48px' },
    lg: { width: '56px', height: '56px' },
  };

  const variantStyles = {
    primary: {
      background: disabled ? theme.gradients.disabled : theme.gradients.primary,
      color: theme.colors.white,
      boxShadow: disabled ? theme.shadows.sm : theme.shadows.md,
    },
    secondary: {
      background: theme.colors.white,
      color: theme.colors.text,
      border: `1px solid ${theme.colors.border}`,
      boxShadow: theme.shadows.sm,
    },
  };

  const hoverStyle = !disabled && isHovered ? {
    transform: 'scale(1.05)',
    boxShadow: variant === 'primary' ? theme.shadows.lg : theme.shadows.md,
  } : {};

  const style = {
    ...baseStyle,
    ...sizeStyles[size],
    ...variantStyles[variant],
    ...hoverStyle,
  };

  return (
    <button
      style={style}
      onClick={onClick}
      disabled={disabled}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      {...props}
    >
      {children}
    </button>
  );
};
