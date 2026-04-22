import api from './api';

interface KnowledgeBase {
  id: string;
  name: string;
  description: string;
  document_count: number;
  vector_count: number;
  created_at: string;
}

interface CreateKnowledgeBaseData {
  name: string;
  description: string;
}

class KnowledgeBaseService {
  async getKnowledgeBases(): Promise<KnowledgeBase[]> {
    return api.get('/knowledge-bases');
  }

  async createKnowledgeBase(data: CreateKnowledgeBaseData): Promise<KnowledgeBase> {
    return api.post('/knowledge-bases', data);
  }

  async getKnowledgeBase(id: string): Promise<KnowledgeBase> {
    return api.get(`/knowledge-bases/${id}`);
  }

  async updateKnowledgeBase(id: string, data: Partial<CreateKnowledgeBaseData>): Promise<KnowledgeBase> {
    return api.put(`/knowledge-bases/${id}`, data);
  }

  async deleteKnowledgeBase(id: string): Promise<{ message: string }> {
    return api.delete(`/knowledge-bases/${id}`);
  }

  async generateSummary(id: string): Promise<{ message: string }> {
    return api.post(`/knowledge-bases/${id}/generate-summary`);
  }
}

export default new KnowledgeBaseService();
