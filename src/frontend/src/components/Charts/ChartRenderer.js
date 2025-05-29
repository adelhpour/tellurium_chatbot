import React from 'react';
import { ChartContainer } from './ChartContainer';
import { LineChart } from './LineChart';
import { BarChart } from './BarChart';
import { ScatterChart } from './ScatterChart';
import { CHART_TYPES } from '../../constants';

export const ChartRenderer = ({ plotData }) => {
  if (!plotData) return null;

  const { type, data } = plotData;

  const renderChart = () => {
    switch (type) {
      case CHART_TYPES.BAR:
        return <BarChart data={data} />;
      case CHART_TYPES.SCATTER:
        return <ScatterChart data={data} />;
      case CHART_TYPES.LINE:
      default:
        return <LineChart data={data} />;
    }
  };

  return (
    <ChartContainer>
      {renderChart()}
    </ChartContainer>
  );
};