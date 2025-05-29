import React from 'react';
import { globalStyles } from '../../styles';
import { formatTime } from '../../utils';
import { ChartRenderer } from '../Charts';
import { MESSAGE_TYPES } from '../../constants';

export const MessageBubble = ({ message }) => {
  const { text, sender, timestamp, plotData } = message;
  const isUser = sender === MESSAGE_TYPES.USER;

  const bubbleStyle = {
    ...globalStyles.messageBubble,
    ...(plotData ? globalStyles.messageBubbleWithPlot : {}),
    ...(isUser ? globalStyles.userBubble : globalStyles.botBubble)
  };

  return (
    <div style={bubbleStyle}>
      <p style={globalStyles.messageText}>{text}</p>

      {plotData && <ChartRenderer plotData={plotData} />}

      <p style={globalStyles.timestamp}>
        {formatTime(timestamp)}
      </p>
    </div>
  );
};