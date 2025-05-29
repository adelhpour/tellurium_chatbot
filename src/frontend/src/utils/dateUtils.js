export const formatTime = (timestamp) => {
  return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

export const createTimestamp = () => new Date();