export const createMessage = (text, sender, plotData = null) => ({
  id: Date.now() + Math.random(),
  text,
  sender,
  timestamp: new Date(),
  plotData
});
