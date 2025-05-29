export class ChatAPIError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ChatAPIError';
    this.status = status;
  }
}

export const chatAPI = {
  async sendMessage(message) {
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new ChatAPIError(
          `API request failed with status ${response.status}`,
          response.status
        );
      }

      const data = await response.json();
      return data;
    } catch (error) {
      if (error instanceof ChatAPIError) {
        throw error;
      }
      throw new ChatAPIError('Network error occurred', 0);
    }
  }
};