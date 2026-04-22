import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Upload, Trash2, FileText, Database, RefreshCw } from 'lucide-react';
import excelDocService from '../services/excelDoc';

interface ExcelDocument {
  id: string;
  name: string;
  sheet_count: number;
  chunk_mode: string;
  chunk_count: number;
  vector_count: number;
  created_at: string;
}

const ExcelDocuments: React.FC = () => {
  const [documents, setDocuments] = useState<ExcelDocument[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedKnowledgeBase, setSelectedKnowledgeBase] = useState<string>('');

  useEffect(() => {
    if (selectedKnowledgeBase) {
      fetchExcelDocuments();
    }
  }, [selectedKnowledgeBase]);

  const fetchExcelDocuments = async () => {
    try {
      setIsLoading(true);
      const data = await excelDocService.getExcelDocuments(selectedKnowledgeBase);
      setDocuments(data);
    } catch (error) {
      console.error('获取Excel文档列表失败:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteExcelDocument = async (id: string) => {
    if (confirm('确定要删除这个Excel文档吗？')) {
      try {
        await excelDocService.deleteExcelDocument(id);
        fetchExcelDocuments();
      } catch (error) {
        console.error('删除Excel文档失败:', error);
      }
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0 && selectedKnowledgeBase) {
      for (const file of files) {
        if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
          try {
            await excelDocService.uploadExcelDocument(selectedKnowledgeBase, file);
          } catch (error) {
            console.error('上传Excel文档失败:', error);
          }
        } else {
          alert('请上传Excel文件(.xlsx或.xls)');
        }
      }
      fetchExcelDocuments();
    }
  };

  const handleChunkAndStore = async (id: string) => {
    try {
      await excelDocService.chunkAndStoreExcel(id, {
        chunk_mode: 'row_level',
        include_header: true
      });
      fetchExcelDocuments();
    } catch (error) {
      console.error('分块并存储Excel文档失败:', error);
    }
  };

  if (isLoading) {
    return <div className="p-6">加载中...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Excel文档管理</h1>
          <p className="text-gray-600 mt-2">管理您的Excel文档</p>
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
              accept=".xlsx,.xls"
            />
            <button className="flex items-center px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors">
              <Upload className="mr-2 h-4 w-4" />
              上传Excel
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
                <p className="text-sm text-gray-500">{doc.sheet_count} 个Sheet</p>
              </div>
              <button 
                className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                onClick={() => handleDeleteExcelDocument(doc.id)}
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-4">
                <div className="flex items-center">
                  <FileText className="h-4 w-4 mr-2 text-gray-500" />
                  <span className="text-sm">分块模式: {doc.chunk_mode || '未分块'}</span>
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
              {!doc.chunk_count && (
                <button 
                  className="mt-4 px-3 py-1 text-sm border rounded-lg hover:bg-gray-50 transition-colors"
                  onClick={() => handleChunkAndStore(doc.id)}
                >
                  分块并存储
                </button>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default ExcelDocuments;