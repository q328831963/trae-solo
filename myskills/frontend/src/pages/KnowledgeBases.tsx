import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Plus, Edit, Trash2, BookOpen, FileText, Database, RefreshCw } from 'lucide-react';

const KnowledgeBases: React.FC = () => {
  const [knowledgeBases, setKnowledgeBases] = useState([
    {
      id: '1',
      name: '技术文档',
      description: '包含技术相关文档',
      documentCount: 8,
      vectorCount: 45,
      createdAt: '2024-01-01'
    },
    {
      id: '2',
      name: '产品文档',
      description: '产品需求和设计文档',
      documentCount: 12,
      vectorCount: 87,
      createdAt: '2024-01-02'
    },
    {
      id: '3',
      name: '营销资料',
      description: '营销相关文档',
      documentCount: 5,
      vectorCount: 23,
      createdAt: '2024-01-03'
    }
  ]);

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
                <button className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors">
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-4">
                <div className="flex items-center">
                  <FileText className="h-4 w-4 mr-2 text-gray-500" />
                  <span className="text-sm">{kb.documentCount} 文档</span>
                </div>
                <div className="flex items-center">
                  <Database className="h-4 w-4 mr-2 text-gray-500" />
                  <span className="text-sm">{kb.vectorCount} 向量</span>
                </div>
                <div className="flex items-center">
                  <RefreshCw className="h-4 w-4 mr-2 text-gray-500" />
                  <span className="text-sm">创建于 {kb.createdAt}</span>
                </div>
              </div>
              <div className="mt-4 flex space-x-2">
                <button className="px-3 py-1 text-sm border rounded-lg hover:bg-gray-50 transition-colors">
                  查看文档
                </button>
                <button className="px-3 py-1 text-sm border rounded-lg hover:bg-gray-50 transition-colors">
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
