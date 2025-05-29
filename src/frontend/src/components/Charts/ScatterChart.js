import React from 'react';
import { ScatterChart as RechartsScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { BaseChart } from './BaseChart';
import { CustomTooltip } from './CustomToolTip';
import { theme } from '../../styles';

export const ScatterChart = ({ data }) => (
  <BaseChart>
    <RechartsScatterChart data={data}>
      <CartesianGrid strokeDasharray="3 3" stroke={theme.colors.border} />
      <XAxis dataKey="x" stroke={theme.colors.textSecondary} fontSize={12} />
      <YAxis dataKey="y" stroke={theme.colors.textSecondary} fontSize={12} />
      <Tooltip content={<CustomTooltip />} />
      <Scatter dataKey="y" fill={theme.colors.success} />
    </RechartsScatterChart>
  </BaseChart>
);