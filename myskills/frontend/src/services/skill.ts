import api from './api';

interface SkillConfig {
  function_calling: {
    description: string;
    parameters: {
      type: string;
      properties: {
        query: {
          type: string;
          description: string;
        };
        knowledge_base_id: {
          type: string;
          description: string;
        };
      };
      required: string[];
    };
  };
  retrieval: {
    top_k: number;
    similarity_threshold: number;
  };
}

interface SkillMetadata {
  name: string;
  description: string;
  parameters: {
    type: string;
    properties: {
      query: {
        type: string;
        description: string;
      };
      knowledge_base_id: {
        type: string;
        description: string;
      };
    };
    required: string[];
  };
}

interface SkillTestResult {
  query: string;
  results: Array<{
    content: string;
    similarity: number;
  }>;
}

class SkillService {
  async getSkillConfig(): Promise<SkillConfig> {
    return api.get('/skill/config');
  }

  async updateSkillConfig(config: Partial<SkillConfig>): Promise<{ message: string }> {
    return api.put('/skill/config', config);
  }

  async getSkillMetadata(): Promise<SkillMetadata> {
    return api.get('/skill/metadata');
  }

  async testSkill(query: string, kbId?: string): Promise<SkillTestResult> {
    return api.post('/skill/test', { query, knowledge_base_id: kbId });
  }
}

export default new SkillService();
