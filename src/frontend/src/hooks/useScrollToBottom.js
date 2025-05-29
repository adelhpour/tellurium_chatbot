import { useRef, useEffect } from 'react';

export const useScrollToBottom = (dependencies = []) => {
  const ref = useRef(null);

  const scrollToBottom = () => {
    ref.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, dependencies);

  return [ref, scrollToBottom];
};