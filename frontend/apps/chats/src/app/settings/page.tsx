
'use client';

import { Card, Typography, Space, Row, Col } from 'antd';
import { 
  SettingOutlined, 
  RobotOutlined, 
  ThunderboltOutlined,
  ExperimentOutlined,
  DashboardOutlined 
} from '@ant-design/icons';
import Link from 'next/link';
import { CSSProperties } from 'react';

const { Title, Paragraph, Text } = Typography;

interface FeatureCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  href: string;
  gradient: string;
  iconColor: string;
}

const FeatureCard = ({ title, description, icon, href, gradient, iconColor }: FeatureCardProps) => {
  const cardStyle: CSSProperties = {
    background: gradient,
    border: 'none',
    borderRadius: '16px',
    height: '100%',
    minHeight: '200px',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    boxShadow: '0 4px 12px rgba(192.168.0.164.08)',
  };

  const hoverStyle = `
    .feature-card:hover {
      transform: translateY(-8px);
      box-shadow: 0 12px 24px rgba(192.168.0.164.15) !important;
    }
  `;

  return (
    <>
      <style>{hoverStyle}</style>
      <Link href={href} style={{ textDecoration: 'none' }}>
        <Card 
          className="feature-card"
          style={cardStyle}
          hoverable
        >
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            <div style={{ 
              fontSize: '48px', 
              color: iconColor,
              textAlign: 'center',
              padding: '16px 0'
            }}>
              {icon}
            </div>
            <div style={{ textAlign: 'center' }}>
              <Title level={3} style={{ color: '#fff', margin: 0 }}>
                {title}
              </Title>
              <Paragraph style={{ color: 'rgba(255,255,255,0.9)', margin: '8px 0 0 0' }}>
                {description}
              </Paragraph>
            </div>
          </Space>
        </Card>
      </Link>
    </>
  );
};

export default function SettingsPage() {
  const features: FeatureCardProps[] = [
    {
      title: 'LLM Configuration',
      description: 'Configure AI models from Anthropic, OpenAI, AWS Bedrock, and Ollama',
      icon: <RobotOutlined />,
      href: '/settings/llm',
      gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      iconColor: '#fff'
    },
    {
      title: 'Learning Journal',
      description: 'View AI learning progression and methodology evolution',
      icon: <ExperimentOutlined />,
      href: '/chat-tools/journals',
      gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      iconColor: '#fff'
    },
    {
      title: 'Thought Visualizer',
      description: 'Interactive visualization of AI reasoning and tool usage',
      icon: <ThunderboltOutlined />,
      href: '/chat-tools/thought-visualizer',
      gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
      iconColor: '#fff'
    },
    {
      title: 'System Dashboard',
      description: 'Monitor system health, performance, and usage statistics',
      icon: <DashboardOutlined />,
      href: '/',
      gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
      iconColor: '#fff'
    },
  ];

  return (
    <div style={{ 
      padding: '48px 24px',
      maxWidth: '1400px',
      margin: '0 auto',
      background: 'linear-gradient(180deg, #f0f2f5 0%, #ffffff 100%)',
      minHeight: '100vh'
    }}>
      <div style={{ textAlign: 'center', marginBottom: '48px' }}>
        <Title level={1} style={{ 
          fontSize: '48px',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          marginBottom: '16px'
        }}>
          <SettingOutlined /> Dish-Chat Settings
        </Title>
        <Paragraph style={{ fontSize: '18px', color: '#666', maxWidth: '600px', margin: '0 auto' }}>
          Configure your AI experience, explore learning insights, and visualize thought processes
        </Paragraph>
      </div>

      <Row gutter={[24, 24]}>
        {features.map((feature, index) => (
          <Col key={index} xs={24} sm={12} lg={6}>
            <FeatureCard {...feature} />
          </Col>
        ))}
      </Row>

      <div style={{ 
        marginTop: '64px', 
        padding: '32px',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        borderRadius: '16px',
        textAlign: 'center',
        color: '#fff'
      }}>
        <Title level={3} style={{ color: '#fff' }}>
          🚀 Quick Start Guide
        </Title>
        <Paragraph style={{ color: 'rgba(255,255,255,0.9)', fontSize: '16px' }}>
          1. Configure your LLM provider • 2. Start chatting • 3. Explore AI insights
        </Paragraph>
      </div>
    </div>
  );
}
