export interface KnowledgeBase {
  id: string;
  name: string;
  description: string;
  document_count: number;
  vector_count: number;
  summary?: string;
  created_at: string;
  updated_at?: string;
}

export interface CreateKnowledgeBaseData {
  name: string;
  description: string;
}
