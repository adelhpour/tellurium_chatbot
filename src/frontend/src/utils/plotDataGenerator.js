export const generatePlotData = (plotType = 'line') => {
  const data = [];
  for (let i = 0; i < 10; i++) {
    data.push({
      x: i,
      y: Math.floor(Math.random() * 100) + 10,
      name: `Point ${i + 1}`,
      value: Math.floor(Math.random() * 100) + 10
    });
  }
  return { type: plotType, data };
};