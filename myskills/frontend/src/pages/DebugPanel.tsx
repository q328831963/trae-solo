import React from 'react';

const DebugPanel: React.FC = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">调试面板</h1>
      <div className="bg-card rounded-lg p-6">
        <h2 className="text-lg font-medium mb-4">在线测试</h2>
        <div className="text-muted-foreground">调试面板功能开发中...</div>
      </div>
    </div>
  );
};

export default DebugPanel;