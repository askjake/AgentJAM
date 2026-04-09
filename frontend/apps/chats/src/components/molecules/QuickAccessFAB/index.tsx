'use client';

import { FloatButton } from 'antd';
import { SettingOutlined, FileTextOutlined, BulbOutlined, RobotOutlined, BookOutlined } from '@ant-design/icons';
import { useRouter } from 'next/navigation';

export default function QuickAccessFAB() {
  const router = useRouter();

  return (
    <FloatButton.Group
      trigger="click"
      type="primary"
      style={{ right: 24, bottom: 24 }}
      icon={<SettingOutlined />}
    >
      <FloatButton
        icon={<RobotOutlined />}
        tooltip="LLM Configuration"
        onClick={() => router.push('/settings/llm')}
      />
      <FloatButton
        icon={<FileTextOutlined />}
        tooltip="Learning Journal"
        onClick={() => router.push('/chat-tools/journals')}
      />
      <FloatButton
        icon={<BulbOutlined />}
        tooltip="Thought Visualizer"
        onClick={() => router.push('/chat-tools/thought-visualizer')}
      />
      <FloatButton
        icon={<BookOutlined />}
        tooltip="Methodology"
        onClick={() => router.push('/chat-tools/methodology')}
      />
      <FloatButton
        icon={<SettingOutlined />}
        tooltip="Settings"
        onClick={() => router.push('/settings')}
      />
    </FloatButton.Group>
  );
}