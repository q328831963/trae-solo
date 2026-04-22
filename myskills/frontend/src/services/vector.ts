import api from './api';

interface Vector {
  id: string;
  document_id: string;
  chunk_id: string;
  content: string;
  embedding_dimension: number;
  created_at: string;
}

interface RetrieveResult {
  id: string;
  content: string;
  similarity: number;
  document_id: string;
}

class VectorService {
  async getVectors(kbId: string): Promise<Vector[]> {
    return api.get(`/knowledge-bases/${kbId}/vectors`);
  }

  async rebuildVectors(kbId: string): Promise<{ message: string }> {
    return api.post(`/knowledge-bases/${kbId}/vectors/rebuild`);
  }

  async retrieveVectors(query: string, kbId?: string): Promise<RetrieveResult[]> {
    return api.post('/vectors/retrieve', { query, knowledge_base_id: kbId });
  }
}

export default new VectorService();
