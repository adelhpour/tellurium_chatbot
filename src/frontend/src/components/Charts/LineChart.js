import React from 'react';
import { LineChart as RechartsLineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { BaseChart } from './BaseChart';
import { CustomTooltip } from './CustomToolTip';
import { theme } from '../../styles';

export const LineChart = ({ data }) => (
  <BaseChart>
    <RechartsLineChart data={data}>
      <CartesianGrid strokeDasharray="3 3" stroke={theme.colors.border} />
      <XAxis dataKey="x" stroke={theme.colors.textSecondary} fontSize={12} />
      <YAxis stroke={theme.colors.textSecondary} fontSize={12} />
      <Tooltip content={<CustomTooltip />} />
      <Line
        type="monotone"
        dataKey="y"
        stroke={theme.colors.primary}
        strokeWidth={3}
        dot={{ fill: theme.colors.primary, strokeWidth: 2, r: 6 }}
        activeDot={{ r: 8, stroke: theme.colors.primary, strokeWidth: 2, fill: theme.colors.white }}
      />
    </RechartsLineChart>
  </BaseChart>
);