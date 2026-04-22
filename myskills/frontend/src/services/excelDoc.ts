import api from './api';

interface ExcelDocument {
  id: string;
  name: string;
  sheet_count: number;
  chunk_mode: string;
  chunk_count: number;
  vector_count: number;
  created_at: string;
}

interface ChunkPreviewResponse {
  chunks: Array<{
    id: string;
    content: string;
  }>;
}

class ExcelDocumentService {
  async getExcelDocuments(kbId: string): Promise<ExcelDocument[]> {
    return api.get(`/knowledge-bases/${kbId}/excel-documents`);
  }

  async uploadExcelDocument(kbId: string, file: File): Promise<ExcelDocument> {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/knowledge-bases/${kbId}/excel-documents/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  async chunkAndStoreExcel(id: string, data: {
    chunk_mode: string;
    include_header: boolean;
  }): Promise<{
    id: string;
    chunk_count: number;
    vector_count: number;
  }> {
    return api.post(`/excel-documents/${id}/chunk-and-store`, data);
  }

  async previewChunk(data: {
    file: File;
    chunk_mode: string;
  }): Promise<ChunkPreviewResponse> {
    const formData = new FormData();
    formData.append('file', data.file);
    formData.append('chunk_mode', data.chunk_mode);
    return api.post('/excel-documents/chunk-preview', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  async deleteExcelDocument(id: string): Promise<{ message: string }> {
    return api.delete(`/excel-documents/${id}`);
  }
}

export default new ExcelDocumentService();
