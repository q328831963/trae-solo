import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { BookOpen, FileText, Database, Settings, Bug, BarChart3, MessageSquare, FileSpreadsheet, Brain, Database as DatabaseIcon } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import KnowledgeBases from './pages/KnowledgeBases';
import Documents from './pages/Documents';
import Chat from './pages/Chat';
import ExcelDocuments from './pages/ExcelDocuments';
import VectorManagement from './pages/VectorManagement';
import SkillConfig from './pages/SkillConfig';
import DebugPanel from './pages/DebugPanel';
import AgentTemplates from './pages/AgentTemplates';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/knowledge-bases" element={<KnowledgeBases />} />
            <Route path="/documents" element={<Documents />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/excel-documents" element={<ExcelDocuments />} />
            <Route path="/vector" element={<VectorManagement />} />
            <Route path="/skill" element={<SkillConfig />} />
            <Route path="/debug" element={<DebugPanel />} />
            <Route path="/agent-templates" element={<AgentTemplates />} />
          </Routes>
        </Layout>
      </div>
    </Router>
  );
}

function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation();
  
  const navItems = [
    { path: '/', icon: BarChart3, label: '仪表盘' },
    { path: '/knowledge-bases', icon: BookOpen, label: '知识库管理' },
    { path: '/documents', icon: FileText, label: '文档管理' },
    { path: '/excel-documents', icon: FileSpreadsheet, label: 'Excel文档' },
    { path: '/vector', icon: DatabaseIcon, label: '向量管理' },
    { path: '/chat', icon: MessageSquare, label: 'AI对话' },
    { path: '/skill', icon: Settings, label: 'Skill配置' },
    { path: '/debug', icon: Bug, label: '调试面板' },
    { path: '/agent-templates', icon: Brain, label: '智能体模板' },
  ];
  
  return (
    <div className="flex">
      <aside className="w-64 border-r bg-card h-screen fixed left-0 top-0">
        <div className="p-6 border-b">
          <h2 className="text-xl font-bold text-primary">📚 私有文档 Skill</h2>
        </div>
        <nav className="p-4 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <a
                key={item.path}
                href={item.path}
                className={`flex items-center px-4 py-2 rounded-lg transition-all ${location.pathname === item.path 
                  ? 'bg-primary/10 text-primary font-medium' 
                  : 'hover:bg-gray-100 text-gray-600'}`}
              >
                <Icon className="mr-2 h-4 w-4" />
                {item.label}
              </a>
            );
          })}
        </nav>
      </aside>
      
      <main className="flex-1 ml-64 p-8">
        {children}
      </main>
    </div>
  );
}

export default App;
