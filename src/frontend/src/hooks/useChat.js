import { useState } from 'react';
import { chatAPI, ChatAPIError } from '../services';
import { createMessage, generatePlotData } from '../utils';
import { MESSAGE_TYPES, CHART_TYPES } from '../constants';

export const useChat = () => {
  const [messages, setMessages] = useState([
    createMessage(
      "Hello! I'm your AI assistant. How can I help you today? Try typing 'plot' to see a sample visualization!",
      MESSAGE_TYPES.BOT
    )
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const addMessage = (message) => {
    setMessages(prev => [...prev, message]);
  };

  const determineChartType = (text) => {
    const lowerText = text.toLowerCase();
    if (lowerText.includes('bar')) return CHART_TYPES.BAR;
    if (lowerText.includes('scatter')) return CHART_TYPES.SCATTER;
    return CHART_TYPES.LINE;
  };

  const handleSend = async () => {
    const text = inputText.trim();
    if (!text) return;

    // Add user message
    const userMessage = createMessage(text, MESSAGE_TYPES.USER);
    addMessage(userMessage);
    setInputText('');
    setIsTyping(true);

    try {
      // Check if user wants a plot (demo logic - you can modify this)
      if (text.toLowerCase().includes('plot')) {
        const chartType = determineChartType(text);
        const plotData = generatePlotData(chartType);

        const botMessage = createMessage(
          "Here is your plot:",
          MESSAGE_TYPES.BOT,
          plotData
        );
        addMessage(botMessage);
      } else {
        // Call actual API
        const response = await chatAPI.sendMessage(text);
        const botMessage = createMessage(
          response.message,
          MESSAGE_TYPES.BOT,
          response.plotData || null
        );
        addMessage(botMessage);
      }
    } catch (error) {
      console.error('Chat error:', error);

      let errorMessage = "Sorry, I encountered an error. Please try again.";
      if (error instanceof ChatAPIError) {
        if (error.status === 0) {
          errorMessage = "Network error. Please check your connection.";
        } else if (error.status >= 500) {
          errorMessage = "Server error. Please try again later.";
        }
      }

      const errorBotMessage = createMessage(errorMessage, MESSAGE_TYPES.BOT);
      addMessage(errorBotMessage);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return {
    messages,
    inputText,
    isTyping,
    setInputText,
    handleSend,
    handleKeyPress
  };
};