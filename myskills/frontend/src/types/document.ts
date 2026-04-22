export interface Document {
  id: string;
  knowledge_base_id: string;
  name: string;
  document_type: string;
  file_path?: string;
  size?: number;
  content?: string;
  chunk_count: number;
  vector_count: number;
  created_at: string;
  updated_at?: string;
}

export interface CreateDocumentData {
  name: string;
  document_type: string;
  content: string;
}
