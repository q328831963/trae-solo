import api from './api';

interface RecommendedKnowledgeBase {
  id: string;
  name: string;
  score: number;
}

interface AgentTemplate {
  id: string;
  name: string;
  type: string;
  description: string;
  status: string;
}

interface AgentTemplateDetail extends AgentTemplate {
  templates: any[];
}

class AgentService {
  async selectKnowledgeBases(query: string): Promise<{
    recommended_knowledge_bases: RecommendedKnowledgeBase[];
  }> {
    return api.post('/agent/select-knowledge-bases', { query });
  }

  async getAgentTemplates(): Promise<AgentTemplate[]> {
    return api.get('/agent-templates');
  }

  async getAgentTemplate(id: string): Promise<AgentTemplateDetail> {
    return api.get(`/agent-templates/${id}`);
  }
}

export default new AgentService();
