import { theme } from './theme';

export const globalStyles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    background: theme.gradients.background,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
  },

  glassmorphism: {
    background: 'rgba(255, 255, 255, 0.8)',
    backdropFilter: 'blur(10px)',
  },

  messageRow: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: theme.spacing.md,
    animation: 'slideIn 0.3s ease-out'
  },

  messageRowUser: {
    flexDirection: 'row-reverse'
  },

  messageBubble: {
    maxWidth: '70%',
    padding: `${theme.spacing.md} ${theme.spacing.lg}`,
    borderRadius: theme.borderRadius.lg,
    position: 'relative'
  },

  messageBubbleWithPlot: {
    maxWidth: '85%',
  },

  userBubble: {
    background: theme.gradients.primary,
    color: theme.colors.white
  },

  botBubble: {
    background: theme.colors.white,
    color: theme.colors.text,
    boxShadow: theme.shadows.sm,
    border: `1px solid ${theme.colors.border}`
  },

  messageText: {
    fontSize: theme.fontSize.sm,
    lineHeight: '1.5',
    margin: 0
  },

  timestamp: {
    fontSize: theme.fontSize.xs,
    marginTop: theme.spacing.xs,
    opacity: 0.7
  },

  avatar: {
    width: '32px',
    height: '32px',
    borderRadius: theme.borderRadius.full,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0
  },

  botAvatar: {
    background: theme.gradients.primary
  },

  userAvatar: {
    background: theme.gradients.success
  }
};