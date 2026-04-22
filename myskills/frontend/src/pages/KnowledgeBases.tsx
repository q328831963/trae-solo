import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Plus, Edit, Trash2, BookOpen, FileText, Database, RefreshCw } from 'lucide-react';
import knowledgeBaseService from '../services/knowledgeBase';

interface KnowledgeBase {
  id: string;
  name: string;
  description: string;
  document_count: number;
  vector_count: number;
  created_at: string;
}

const KnowledgeBases: React.FC = () => {
  const [knowledgeBases, setKnowledgeBases] = useState<KnowledgeBase[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchKnowledgeBases();
  }, []);

  const fetchKnowledgeBases = async () => {
    try {
      setIsLoading(true);
      const data = await knowledgeBaseService.getKnowledgeBases();
      setKnowledgeBases(data);
    } catch (error) {
      console.error('获取知识库列表失败:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteKnowledgeBase = async (id: string) => {
    if (confirm('确定要删除这个知识库吗？')) {
      try {
        await knowledgeBaseService.deleteKnowledgeBase(id);
        fetchKnowledgeBases();
      } catch (error) {
        console.error('删除知识库失败:', error);
      }
    }
  };

  const handleGenerateSummary = async (id: string) => {
    try {
      await knowledgeBaseService.generateSummary(id);
      alert('摘要生成任务已启动');
    } catch (error) {
      console.error('生成摘要失败:', error);
    }
  };

  if (isLoading) {
    return <div className="p-6">加载中...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">知识库管理</h1>
          <p className="text-gray-600 mt-2">管理您的知识库和文档</p>
        </div>
        <button className="flex items-center px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors">
          <Plus className="mr-2 h-4 w-4" />
          创建知识库
        </button>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {knowledgeBases.map((kb) => (
          <Card key={kb.id} className="overflow-hidden">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <div>
                <CardTitle className="text-xl">{kb.name}</CardTitle>
                <p className="text-sm text-gray-500">{kb.description}</p>
              </div>
              <div className="flex space-x-2">
                <button className="p-2 text-gray-500 hover:bg-gray-100 rounded-lg transition-colors">
                  <Edit className="h-4 w-4" />
                </button>
                <button 
                  className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                  onClick={() => handleDeleteKnowledgeBase(kb.id)}
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-4">
                <div className="flex items-center">
                  <FileText className="h-4 w-4 mr-2 text-gray-500" />
                  <span className="text-sm">{kb.document_count} 文档</span>
                </div>
                <div className="flex items-center">
                  <Database className="h-4 w-4 mr-2 text-gray-500" />
                  <span className="text-sm">{kb.vector_count} 向量</span>
                </div>
                <div className="flex items-center">
                  <RefreshCw className="h-4 w-4 mr-2 text-gray-500" />
                  <span className="text-sm">创建于 {new Date(kb.created_at).toLocaleDateString()}</span>
                </div>
              </div>
              <div className="mt-4 flex space-x-2">
                <button className="px-3 py-1 text-sm border rounded-lg hover:bg-gray-50 transition-colors">
                  查看文档
                </button>
                <button 
                  className="px-3 py-1 text-sm border rounded-lg hover:bg-gray-50 transition-colors"
                  onClick={() => handleGenerateSummary(kb.id)}
                >
                  生成摘要
                </button>
                <button className="px-3 py-1 text-sm border rounded-lg hover:bg-gray-50 transition-colors">
                  重建索引
                </button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default KnowledgeBases;
