import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { BarChart3, BookOpen, FileText, Database, MessageSquare, TrendingUp } from 'lucide-react';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState({
    knowledgeBases: 0,
    documents: 0,
    vectors: 0,
    chats: 0
  });

  useEffect(() => {
    // 模拟数据获取
    setTimeout(() => {
      setStats({
        knowledgeBases: 5,
        documents: 23,
        vectors: 156,
        chats: 42
      });
    }, 500);
  }, []);

  const statCards = [
    {
      title: '知识库',
      value: stats.knowledgeBases,
      icon: BookOpen,
      color: 'bg-primary/10 text-primary'
    },
    {
      title: '文档',
      value: stats.documents,
      icon: FileText,
      color: 'bg-secondary/10 text-secondary'
    },
    {
      title: '向量',
      value: stats.vectors,
      icon: Database,
      color: 'bg-accent/10 text-accent'
    },
    {
      title: '对话',
      value: stats.chats,
      icon: MessageSquare,
      color: 'bg-purple/10 text-purple'
    }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">仪表盘</h1>
        <p className="text-gray-600 mt-2">系统概览和快速访问</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card, index) => {
          const Icon = card.icon;
          return (
            <Card key={index} className="overflow-hidden">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-500">{card.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div className="text-3xl font-bold">{card.value}</div>
                  <div className={`p-3 rounded-full ${card.color}`}>
                    <Icon className="h-6 w-6" />
                  </div>
                </div>
                <div className="mt-4 flex items-center text-sm">
                  <TrendingUp className="h-4 w-4 mr-1 text-green-500" />
                  <span className="text-green-500">+12% 较上周</span>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>最近活动</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[1, 2, 3, 4].map((item) => (
                <div key={item} className="flex items-start space-x-3">
                  <div className="w-2 h-2 rounded-full bg-primary mt-2"></div>
                  <div>
                    <p className="text-sm font-medium">上传了新文档</p>
                    <p className="text-xs text-gray-500">2小时前</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>快速访问</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-3">
              {[
                { label: '创建知识库', href: '/knowledge-bases' },
                { label: '上传文档', href: '/documents' },
                { label: 'AI对话', href: '/chat' },
                { label: 'Skill配置', href: '/skill' }
              ].map((item, index) => (
                <a
                  key={index}
                  href={item.href}
                  className="flex items-center justify-center p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                >
                  {item.label}
                </a>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
