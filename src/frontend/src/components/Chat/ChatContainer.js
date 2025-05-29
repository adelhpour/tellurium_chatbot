import React from 'react';
import { globalStyles } from '../../styles';
import { useChat } from '../../hooks/useChat';
import { useScrollToBottom } from '../../hooks/useScrollToBottom';
import { ChatHeader } from './ChatHeader';
import { ChatMessages } from './ChatMessages';
import { ChatInput } from './ChatInput';

export const ChatContainer = () => {
  const {
    messages,
    inputText,
    setInputText,
    isTyping,
    handleSend,
    handleKeyPress
  } = useChat();

  // Automatically scroll when `messages` changes
  const [messagesEndRef] = useScrollToBottom([messages]);

  return (
    <div style={globalStyles.container}>
      <ChatHeader title="AI Assistant" subtitle="Always here to help" />
      <ChatMessages
        messages={messages}
        isTyping={isTyping}
        messagesEndRef={messagesEndRef}
      />
      <ChatInput
        inputText={inputText}
        setInputText={setInputText}
        handleSend={handleSend}
        handleKeyPress={handleKeyPress}
        disabled={isTyping}
      />
    </div>
  );
};
