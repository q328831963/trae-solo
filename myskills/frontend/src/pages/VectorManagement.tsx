import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Search, Database, RefreshCw } from 'lucide-react';
import vectorService from '../services/vector';

interface Vector {
  id: string;
  document_id: string;
  chunk_id: string;
  content: string;
  embedding_dimension: number;
  created_at: string;
}

interface RetrievalResult {
  id: string;
  content: string;
  similarity: number;
  document_id: string;
}

const VectorManagement: React.FC = () => {
  const [vectors, setVectors] = useState<Vector[]>([]);
  const [retrievalResults, setRetrievalResults] = useState<RetrievalResult[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedKnowledgeBase, setSelectedKnowledgeBase] = useState<string>('');
  const [query, setQuery] = useState('');

  useEffect(() => {
    if (selectedKnowledgeBase) {
      fetchVectors();
    }
  }, [selectedKnowledgeBase]);

  const fetchVectors = async () => {
    try {
      setIsLoading(true);
      const data = await vectorService.getVectors(selectedKnowledgeBase);
      setVectors(data);
    } catch (error) {
      console.error('获取向量列表失败:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetrieveVectors = async () => {
    if (query) {
      try {
        const results = await vectorService.retrieveVectors({ query, knowledge_base_id: selectedKnowledgeBase });
        setRetrievalResults(results);
      } catch (error) {
        console.error('向量检索失败:', error);
      }
    }
  };

  const handleRebuildVectors = async () => {
    if (selectedKnowledgeBase) {
      try {
        await vectorService.rebuildVectors(selectedKnowledgeBase);
        alert('向量索引重建任务已启动');
      } catch (error) {
        console.error('重建向量索引失败:', error);
      }
    }
  };

  if (isLoading) {
    return <div className="p-6">加载中...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">向量管理</h1>
          <p className="text-gray-600 mt-2">管理和检索向量</p>
        </div>
        <select 
          className="px-4 py-2 border rounded-lg"
          value={selectedKnowledgeBase}
          onChange={(e) => setSelectedKnowledgeBase(e.target.value)}
        >
          <option value="">选择知识库</option>
          <option value="1">技术文档</option>
          <option value="2">产品文档</option>
          <option value="3">营销资料</option>
        </select>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>向量检索测试</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex space-x-2">
              <input 
                type="text" 
                className="flex-1 px-4 py-2 border rounded-lg"
                placeholder="输入查询文本"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              <button 
                className="flex items-center px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
                onClick={handleRetrieveVectors}
              >
                <Search className="mr-2 h-4 w-4" />
                检索
              </button>
            </div>
            <div className="space-y-2">
              {retrievalResults.map((result, index) => (
                <div key={index} className="p-4 border rounded-lg">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">相似度: {result.similarity.toFixed(2)}</span>
                    <span className="text-xs text-gray-500">文档ID: {result.document_id}</span>
                  </div>
                  <div className="mt-2 text-sm">{result.content}</div>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>向量列表</CardTitle>
          <button 
            className="flex items-center px-3 py-1 text-sm border rounded-lg hover:bg-gray-50 transition-colors"
            onClick={handleRebuildVectors}
          >
            <RefreshCw className="mr-2 h-4 w-4" />
            重建索引
          </button>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {vectors.map((vector) => (
              <div key={vector.id} className="p-4 border rounded-lg">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">文档ID: {vector.document_id}</span>
                  <span className="text-xs text-gray-500">维度: {vector.embedding_dimension}</span>
                </div>
                <div className="mt-2 text-sm">{vector.content}</div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default VectorManagement;