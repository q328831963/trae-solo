export interface ChatMessage {
  id?: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;
  sources?: Array<{
    id: string;
    name: string;
  }>;
}

export interface ChatConfig {
  llm_api_url?: string;
  llm_model: string;
  temperature: number;
  max_tokens: number;
}
