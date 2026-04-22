import api from './api';

interface ChatMessage {
  id?: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;
}

interface ChatResponse {
  message: string;
  sources: Array<{
    id: string;
    name: string;
  }>;
}

class ChatService {
  async sendMessage(message: string, kbId?: string): Promise<ChatResponse> {
    return api.post('/chat', { query: message, knowledge_base_id: kbId });
  }

  async streamMessage(message: string, kbId?: string): Promise<ReadableStream<string>> {
    const response = await fetch(`${api.defaults.baseURL}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: message, knowledge_base_id: kbId }),
    });

    if (!response.body) {
      throw new Error('No response body');
    }

    return response.body;
  }
}

export default new ChatService();
