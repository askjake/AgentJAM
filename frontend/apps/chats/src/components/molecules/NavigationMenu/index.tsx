'use client';

import { Menu, Dropdown, Button, Space } from 'antd';
import { MenuOutlined, SettingOutlined, FileTextOutlined, BulbOutlined, RobotOutlined, BookOutlined } from '@ant-design/icons';
import Link from 'next/link';
import type { MenuProps } from 'antd';

export default function NavigationMenu() {
  const items: MenuProps['items'] = [
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: <Link href="/settings">Settings</Link>,
    },
    {
      key: 'llm',
      icon: <RobotOutlined />,
      label: <Link href="/settings/llm">LLM Configuration</Link>,
    },
    {
      type: 'divider',
    },
    {
      key: 'tools',
      label: 'Chat Tools',
      icon: <MenuOutlined />,
      children: [
        {
          key: 'journals',
          icon: <FileTextOutlined />,
          label: <Link href="/chat-tools/journals">Learning Journal</Link>,
        },
        {
          key: 'visualizer',
          icon: <BulbOutlined />,
          label: <Link href="/chat-tools/thought-visualizer">Thought Visualizer</Link>,
        },
        {
          key: 'methodology',
          icon: <BookOutlined />,
          label: <Link href="/chat-tools/methodology">Methodology</Link>,
        },
      ],
    },
  ];

  return (
    <Dropdown menu={{ items }} placement="bottomRight">
      <Button icon={<MenuOutlined />} type="text">
        Menu
      </Button>
    </Dropdown>
  );
}