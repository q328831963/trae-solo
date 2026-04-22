export interface ExcelDocument {
  id: string;
  knowledge_base_id: string;
  name: string;
  file_path?: string;
  size?: number;
  sheet_count: number;
  chunk_mode: string;
  chunk_count: number;
  vector_count: number;
  created_at: string;
  updated_at?: string;
}

export interface ExcelChunkData {
  file: File;
  chunk_mode: string;
  include_header?: boolean;
  semantic_threshold?: number;
}
