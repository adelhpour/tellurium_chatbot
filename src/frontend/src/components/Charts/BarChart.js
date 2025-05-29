import React from 'react';
import { BarChart as RechartsBarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { BaseChart } from './BaseChart';
import { CustomTooltip } from './CustomToolTip';
import { theme } from '../../styles';

export const BarChart = ({ data }) => (
  <BaseChart>
    <RechartsBarChart data={data}>
      <CartesianGrid strokeDasharray="3 3" stroke={theme.colors.border} />
      <XAxis dataKey="name" stroke={theme.colors.textSecondary} fontSize={12} />
      <YAxis stroke={theme.colors.textSecondary} fontSize={12} />
      <Tooltip content={<CustomTooltip />} />
      <Bar dataKey="value" fill="url(#barGradient)" radius={[4, 4, 0, 0]} />
      <defs>
        <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={theme.colors.primary} />
          <stop offset="100%" stopColor={theme.colors.secondary} />
        </linearGradient>
      </defs>
    </RechartsBarChart>
  </BaseChart>
);