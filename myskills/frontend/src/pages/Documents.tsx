import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Upload, Trash2, FileText, Database, RefreshCw } from 'lucide-react';
import documentService from '../services/document';

interface Document {
  id: string;
  name: string;
  document_type: string;
  size: number;
  chunk_count: number;
  vector_count: number;
  created_at: string;
}

const Documents: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedKnowledgeBase, setSelectedKnowledgeBase] = useState<string>('');

  useEffect(() => {
    if (selectedKnowledgeBase) {
      fetchDocuments();
    } else {
      setIsLoading(false);
      setDocuments([]);
    }
  }, [selectedKnowledgeBase]);

  const fetchDocuments = async () => {
    try {
      setIsLoading(true);
      const data = await documentService.getDocuments(selectedKnowledgeBase);
      setDocuments(data);
    } catch (error) {
      console.error('获取文档列表失败:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteDocument = async (id: string) => {
    if (confirm('确定要删除这个文档吗？')) {
      try {
        await documentService.deleteDocument(id);
        fetchDocuments();
      } catch (error) {
        console.error('删除文档失败:', error);
      }
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0 && selectedKnowledgeBase) {
      for (const file of files) {
        try {
          await documentService.uploadDocument(selectedKnowledgeBase, file);
        } catch (error) {
          console.error('上传文档失败:', error);
        }
      }
      fetchDocuments();
    }
  };

  if (isLoading) {
    return <div className="p-6">加载中...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">文档管理</h1>
          <p className="text-gray-600 mt-2">管理您的文档</p>
        </div>
        <div className="flex space-x-2">
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
          <div className="relative">
            <input 
              type="file" 
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              onChange={handleFileUpload}
              multiple
            />
            <button className="flex items-center px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors">
              <Upload className="mr-2 h-4 w-4" />
              上传文档
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {documents.map((doc) => (
          <Card key={doc.id} className="overflow-hidden">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <div>
                <CardTitle className="text-xl">{doc.name}</CardTitle>
                <p className="text-sm text-gray-500">类型: {doc.document_type}</p>
              </div>
              <button 
                className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                onClick={() => handleDeleteDocument(doc.id)}
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-4">
                <div className="flex items-center">
                  <FileText className="h-4 w-4 mr-2 text-gray-500" />
                  <span className="text-sm">大小: {doc.size} bytes</span>
                </div>
                <div className="flex items-center">
                  <Database className="h-4 w-4 mr-2 text-gray-500" />
                  <span className="text-sm">{doc.chunk_count} 分块, {doc.vector_count} 向量</span>
                </div>
                <div className="flex items-center">
                  <RefreshCw className="h-4 w-4 mr-2 text-gray-500" />
                  <span className="text-sm">创建于 {new Date(doc.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Documents;