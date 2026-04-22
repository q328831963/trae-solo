import api from './api';

interface Document {
  id: string;
  name: string;
  document_type: string;
  size: number;
  chunk_count: number;
  vector_count: number;
  created_at: string;
}

interface CreateDocumentData {
  name: string;
  document_type: string;
  content: string;
}

class DocumentService {
  async getDocuments(kbId: string): Promise<Document[]> {
    return api.get(`/knowledge-bases/${kbId}/documents`);
  }

  async createDocument(kbId: string, data: CreateDocumentData): Promise<Document> {
    return api.post(`/knowledge-bases/${kbId}/documents`, data);
  }

  async uploadDocument(kbId: string, file: File): Promise<Document> {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/knowledge-bases/${kbId}/documents/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  async getDocument(id: string): Promise<Document> {
    return api.get(`/documents/${id}`);
  }

  async deleteDocument(id: string): Promise<{ message: string }> {
    return api.delete(`/documents/${id}`);
  }
}

export default new DocumentService();
