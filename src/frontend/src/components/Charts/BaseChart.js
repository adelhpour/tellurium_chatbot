import React from 'react';
import { ResponsiveContainer } from 'recharts';

export const BaseChart = ({ children }) => (
  <ResponsiveContainer width="100%" height="100%">
    {children}
  </ResponsiveContainer>
);