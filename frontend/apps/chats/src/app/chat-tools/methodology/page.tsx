'use client';

import { useState, useEffect } from 'react';
import { 
  Layout, 
  Typography, 
  Card, 
  Timeline, 
  Tabs, 
  Button, 
  Space, 
  Tag, 
  Alert,
  Input,
  Modal,
  message
} from 'antd';
import { 
  ArrowLeftOutlined,
  BookOutlined,
  RocketOutlined,
  CodeOutlined,
  EditOutlined,
  SaveOutlined,
  ReloadOutlined,
  ExperimentOutlined,
  BulbOutlined,
  ToolOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';
import Link from 'next/link';

const { Title, Text, Paragraph } = Typography;
const { Content } = Layout;
const { TextArea } = Input;
const { TabPane } = Tabs;

// ==============================================================================
// TYPE DEFINITIONS
// ==============================================================================

interface MethodologyStep {
  phase: string;
  date: string;
  title: string;
  description: string;
  status: 'completed' | 'in-progress' | 'planned';
  color: string;
  icon: React.ReactNode;
}

interface UserPreference {
  key: string;
  label: string;
  value: string;
  description: string;
  type: 'text' | 'textarea' | 'select';
  options?: string[];
}

// ==============================================================================
// COMPONENT: MethodologyPage
// ==============================================================================
export default function MethodologyPage() {
  // State for user preferences
  const [preferences, setPreferences] = useState<UserPreference[]>([
    {
      key: 'reasoning_depth',
      label: 'Reasoning Depth',
      value: 'balanced',
      description: 'How deeply should the AI reason before responding?',
      type: 'select',
      options: ['quick', 'balanced', 'deep', 'comprehensive']
    },
    {
      key: 'tool_preference',
      label: 'Tool Usage Preference',
      value: 'ask_first',
      description: 'When should tools be used automatically?',
      type: 'select',
      options: ['always_ask', 'ask_first', 'auto_approve', 'fully_automatic']
    },
    {
      key: 'response_style',
      label: 'Response Style',
      value: 'balanced',
      description: 'How should responses be formatted?',
      type: 'select',
      options: ['concise', 'balanced', 'detailed', 'comprehensive']
    },
    {
      key: 'custom_instructions',
      label: 'Custom Instructions',
      value: '',
      description: 'Any special instructions or preferences for the AI?',
      type: 'textarea'
    }
  ]);

  const [editModalVisible, setEditModalVisible] = useState(false);
  const [editingPreference, setEditingPreference] = useState<UserPreference | null>(null);
  const [tempValue, setTempValue] = useState('');

  // Load preferences from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('methodology_preferences');
    if (saved) {
      try {
        setPreferences(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to load preferences:', e);
      }
    }
  }, []);

  // Save preferences to localStorage
  const savePreferences = () => {
    localStorage.setItem('methodology_preferences', JSON.stringify(preferences));
    message.success('Preferences saved successfully!');
  };

  // Reset preferences to defaults
  const resetPreferences = () => {
    Modal.confirm({
      title: 'Reset Preferences?',
      content: 'This will reset all preferences to their default values.',
      okText: 'Reset',
      okType: 'danger',
      onOk: () => {
        localStorage.removeItem('methodology_preferences');
        window.location.reload();
      }
    });
  };

  // Open edit modal for a preference
  const openEditModal = (pref: UserPreference) => {
    setEditingPreference(pref);
    setTempValue(pref.value);
    setEditModalVisible(true);
  };

  // Save edited preference
  const saveEdit = () => {
    if (editingPreference) {
      setPreferences(preferences.map(p => 
        p.key === editingPreference.key 
          ? { ...p, value: tempValue }
          : p
      ));
      setEditModalVisible(false);
      message.success('Preference updated!');
    }
  };

  // ==============================================================================
  // METHODOLOGY EVOLUTION TIMELINE
  // ==============================================================================
  const evolutionSteps: MethodologyStep[] = [
    {
      phase: 'Phase 1',
      date: '2024 Q1',
      title: 'Foundation: Basic Chat Interface',
      description: 'Simple conversational interface with Claude integration. Direct question-answer format without reasoning visibility.',
      status: 'completed',
      color: '#52c41a',
      icon: <CheckCircleOutlined />
    },
    {
      phase: 'Phase 2',
      date: '2024 Q2',
      title: 'Tool Integration',
      description: 'Added tool calling capabilities: code execution, file operations, and cluster inspection. Tools execute based on context.',
      status: 'completed',
      color: '#52c41a',
      icon: <ToolOutlined />
    },
    {
      phase: 'Phase 3',
      date: '2024 Q3',
      title: 'Thought Visualization',
      description: 'Introduced visual graph of AI reasoning process. Users can see how thoughts flow and connect during problem-solving.',
      status: 'completed',
      color: '#52c41a',
      icon: <BulbOutlined />
    },
    {
      phase: 'Phase 4',
      date: '2024 Q4',
      title: 'Enhanced Reasoning Mode',
      description: 'Added extended thinking capability for complex problems. AI can now think through multiple steps before responding.',
      status: 'completed',
      color: '#52c41a',
      icon: <ExperimentOutlined />
    },
    {
      phase: 'Phase 5',
      date: '2025 Q1',
      title: 'Methodology Transparency',
      description: 'Current phase: Full visibility into AI methodology and decision-making process. Users can customize and guide behavior.',
      status: 'in-progress',
      color: '#1890ff',
      icon: <BookOutlined />
    },
    {
      phase: 'Phase 6',
      date: '2025 Q2',
      title: 'Adaptive Learning',
      description: 'Planned: System learns from user preferences and adapts reasoning strategies based on feedback and usage patterns.',
      status: 'planned',
      color: '#d9d9d9',
      icon: <RocketOutlined />
    }
  ];

  // ==============================================================================
  // RENDER
  // ==============================================================================
  return (
    <Layout style={{ minHeight: '100vh', background: '#f5f5f5' }}>
      <Content style={{ padding: '24px' }}>
        {/* Header */}
        <div style={{ marginBottom: '24px' }}>
          <Space>
            <Link href="/">
              <Button icon={<ArrowLeftOutlined />}>Back to Chat</Button>
            </Link>
            <Title level={2} style={{ margin: 0 }}>
              <BookOutlined /> Methodology & Evolution
            </Title>
          </Space>
        </div>

        {/* Main Content Tabs */}
        <Card>
          <Tabs defaultActiveKey="1" size="large">
            
            {/* TAB 1: Overview */}
            <TabPane tab={<span><BookOutlined /> Overview</span>} key="1">
              <div style={{ maxWidth: '900px' }}>
                <Title level={3}>What is Dish-Chat's Methodology?</Title>
                
                <Alert
                  message="Human-Centered AI Reasoning"
                  description="Dish-Chat is designed to show its work. Unlike traditional black-box AI, you can see how it thinks, what tools it uses, and how it arrives at conclusions."
                  type="info"
                  showIcon
                  style={{ marginBottom: '24px' }}
                />

                <Card title="Core Principles" style={{ marginBottom: '24px' }}>
                  <Space direction="vertical" size="large" style={{ width: '100%' }}>
                    <div>
                      <Title level={5}>🔍 Transparency</Title>
                      <Paragraph>
                        Every step of the reasoning process is visible. You can see what the AI is thinking,
                        which tools it's considering, and how it's processing your request.
                      </Paragraph>
                    </div>

                    <div>
                      <Title level={5}>🛠️ Tool-Augmented Intelligence</Title>
                      <Paragraph>
                        The AI can use real tools to get real information: search internal docs, execute code,
                        inspect cluster state, and more. It doesn't just pretend—it actually does the work.
                      </Paragraph>
                    </div>

                    <div>
                      <Title level={5}>🧠 Extended Thinking</Title>
                      <Paragraph>
                        For complex problems, the AI can enter "reasoning mode" where it thinks through multiple
                        approaches, considers edge cases, and plans its solution before responding.
                      </Paragraph>
                    </div>

                    <div>
                      <Title level={5}>📊 Visual Understanding</Title>
                      <Paragraph>
                        The thought visualizer shows how ideas connect, which paths were explored, and how
                        the final answer emerged from the reasoning graph.
                      </Paragraph>
                    </div>

                    <div>
                      <Title level={5}>⚙️ Customizable Behavior</Title>
                      <Paragraph>
                        You control how deep the AI thinks, when it uses tools, and how it formats responses.
                        Your preferences guide its behavior.
                      </Paragraph>
                    </div>
                  </Space>
                </Card>

                <Card title="How It Works" type="inner">
                  <Timeline>
                    <Timeline.Item color="blue">
                      <Text strong>1. Query Processing</Text>
                      <Paragraph>Your question is analyzed to understand intent, context, and complexity.</Paragraph>
                    </Timeline.Item>
                    <Timeline.Item color="blue">
                      <Text strong>2. Strategy Selection</Text>
                      <Paragraph>Based on the query, the AI chooses between quick response, standard reasoning, or extended thinking.</Paragraph>
                    </Timeline.Item>
                    <Timeline.Item color="blue">
                      <Text strong>3. Tool Planning</Text>
                      <Paragraph>If tools are needed (search, code execution, etc.), they're selected and prepared.</Paragraph>
                    </Timeline.Item>
                    <Timeline.Item color="blue">
                      <Text strong>4. Reasoning Phase</Text>
                      <Paragraph>The AI thinks through the problem, creating a graph of interconnected thoughts.</Paragraph>
                    </Timeline.Item>
                    <Timeline.Item color="blue">
                      <Text strong>5. Response Generation</Text>
                      <Paragraph>The final answer is crafted based on all gathered information and reasoning.</Paragraph>
                    </Timeline.Item>
                    <Timeline.Item color="green">
                      <Text strong>6. Visualization</Text>
                      <Paragraph>You can review the thought process, see tool usage, and understand the reasoning.</Paragraph>
                    </Timeline.Item>
                  </Timeline>
                </Card>
              </div>
            </TabPane>

            {/* TAB 2: Evolution */}
            <TabPane tab={<span><RocketOutlined /> Evolution</span>} key="2">
              <div style={{ maxWidth: '900px' }}>
                <Title level={3}>Methodology Evolution Timeline</Title>
                <Paragraph>
                  Dish-Chat has evolved from a simple chat interface to a sophisticated reasoning system.
                  Here's how we got here and where we're going:
                </Paragraph>

                <Timeline mode="left" style={{ marginTop: '32px' }}>
                  {evolutionSteps.map((step, index) => (
                    <Timeline.Item
                      key={index}
                      color={step.color}
                      dot={step.icon}
                      label={
                        <div>
                          <Tag color={step.color}>{step.phase}</Tag>
                          <br />
                          <Text type="secondary">{step.date}</Text>
                        </div>
                      }
                    >
                      <Card size="small">
                        <Title level={5}>{step.title}</Title>
                        <Paragraph>{step.description}</Paragraph>
                        <Tag color={
                          step.status === 'completed' ? 'success' :
                          step.status === 'in-progress' ? 'processing' :
                          'default'
                        }>
                          {step.status === 'completed' ? '✓ Complete' :
                           step.status === 'in-progress' ? '⋯ In Progress' :
                           '○ Planned'}
                        </Tag>
                      </Card>
                    </Timeline.Item>
                  ))}
                </Timeline>

                <Alert
                  message="Future Directions"
                  description="Next phases will focus on adaptive learning, personalized reasoning strategies, and collaborative problem-solving where multiple AI agents work together."
                  type="info"
                  showIcon
                  icon={<RocketOutlined />}
                  style={{ marginTop: '32px' }}
                />
              </div>
            </TabPane>

            {/* TAB 3: Implementation */}
            <TabPane tab={<span><CodeOutlined /> Implementation</span>} key="3">
              <div style={{ maxWidth: '900px' }}>
                <Title level={3}>Technical Implementation</Title>

                <Card title="Architecture Overview" style={{ marginBottom: '24px' }}>
                  <Paragraph>
                    Dish-Chat is built on a modern, scalable architecture that separates concerns and
                    enables independent evolution of each component.
                  </Paragraph>

                  <Space direction="vertical" size="large" style={{ width: '100%' }}>
                    <div>
                      <Title level={5}>Frontend (Next.js + React)</Title>
                      <Paragraph>
                        • <Text code>apps/chats</Text> - Main chat interface with real-time updates<br />
                        • <Text code>apps/chats/src/app/chat-tools/</Text> - Tool-specific pages (journals, visualizer, methodology)<br />
                        • Uses Ant Design for consistent UI components<br />
                        • Server-side rendering for optimal performance
                      </Paragraph>
                    </div>

                    <div>
                      <Title level={5}>Backend (FastAPI + Python)</Title>
                      <Paragraph>
                        • RESTful API for all chat operations<br />
                        • <Text code>/rest/api/v1/chats</Text> - Chat management<br />
                        • <Text code>/rest/api/v1/viz</Text> - Thought visualization data<br />
                        • <Text code>/rest/api/v1/tools</Text> - Tool execution endpoints<br />
                        • AWS Bedrock integration for Claude 4 access
                      </Paragraph>
                    </div>

                    <div>
                      <Title level={5}>LLM Integration</Title>
                      <Paragraph>
                        • Model: <Text code>Claude Sonnet 4.5</Text> via AWS Bedrock<br />
                        • Inference profile ARN: <Text code>us.anthropic.claude-sonnet-4-5-20250929-v1:0</Text><br />
                        • Supports extended thinking with <Text code>&lt;thinking&gt;</Text> tags<br />
                        • Tool use via Anthropic's function calling API
                      </Paragraph>
                    </div>

                    <div>
                      <Title level={5}>Tool System</Title>
                      <Paragraph>
                        Available tools:<br />
                        • <Text code>internal_search</Text> - Search Confluence, JIRA, Git<br />
                        • <Text code>public_web_search</Text> - External search with privacy safeguards<br />
                        • <Text code>agent_run_python</Text> - Execute Python code in sandbox<br />
                        • <Text code>agent_run_shell</Text> - Run whitelisted shell commands<br />
                        • <Text code>cluster_inspect</Text> - Kubernetes cluster inspection<br />
                        • <Text code>agent_git_clone</Text> - Clone and analyze repositories
                      </Paragraph>
                    </div>
                  </Space>
                </Card>

                <Card title="Data Flow" type="inner">
                  <pre style={{ 
                    background: '#f6f6f6', 
                    padding: '16px', 
                    borderRadius: '4px',
                    overflow: 'auto'
                  }}>
{`User Input
    ↓
Frontend (React/Next.js)
    ↓ HTTP POST /rest/api/v1/chats/{id}/messages
Backend (FastAPI)
    ↓ Bedrock API call
Claude 4 (AWS Bedrock)
    ↓ Reasoning + Tool Selection
Tool Execution (if needed)
    ↓ Results returned
Response Generation
    ↓ Streaming response
Frontend Updates
    ↓
Thought Graph + Journal Entries
    ↓
Visualization & Storage`}
                  </pre>
                </Card>
              </div>
            </TabPane>

            {/* TAB 4: Preferences */}
            <TabPane tab={<span><EditOutlined /> Your Preferences</span>} key="4">
              <div style={{ maxWidth: '900px' }}>
                <Space direction="vertical" size="large" style={{ width: '100%' }}>
                  <div>
                    <Title level={3}>Customize Your Experience</Title>
                    <Paragraph>
                      Configure how Dish-Chat behaves and responds to your needs. These preferences
                      are stored locally in your browser and only affect your experience.
                    </Paragraph>
                  </div>

                  <Alert
                    message="💡 Pro Tip"
                    description="Try different settings to find what works best for your workflow. You can always reset to defaults."
                    type="info"
                    showIcon
                  />

                  {preferences.map((pref, index) => (
                    <Card 
                      key={pref.key}
                      title={
                        <Space>
                          <Text strong>{pref.label}</Text>
                          <Tag color="blue">{pref.value || 'Not Set'}</Tag>
                        </Space>
                      }
                      extra={
                        <Button 
                          icon={<EditOutlined />} 
                          onClick={() => openEditModal(pref)}
                          size="small"
                        >
                          Edit
                        </Button>
                      }
                    >
                      <Paragraph type="secondary">{pref.description}</Paragraph>
                      {pref.value && pref.type === 'textarea' && (
                        <Paragraph>
                          <Text code style={{ whiteSpace: 'pre-wrap' }}>
                            {pref.value.substring(0, 200)}
                            {pref.value.length > 200 && '...'}
                          </Text>
                        </Paragraph>
                      )}
                    </Card>
                  ))}

                  <Space>
                    <Button 
                      type="primary" 
                      icon={<SaveOutlined />}
                      onClick={savePreferences}
                      size="large"
                    >
                      Save All Preferences
                    </Button>
                    <Button 
                      icon={<ReloadOutlined />}
                      onClick={resetPreferences}
                      size="large"
                    >
                      Reset to Defaults
                    </Button>
                  </Space>
                </Space>
              </div>
            </TabPane>

          </Tabs>
        </Card>

        {/* Edit Modal */}
        <Modal
          title={`Edit: ${editingPreference?.label}`}
          open={editModalVisible}
          onOk={saveEdit}
          onCancel={() => setEditModalVisible(false)}
          width={600}
        >
          {editingPreference && (
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <Paragraph type="secondary">
                {editingPreference.description}
              </Paragraph>

              {editingPreference.type === 'select' && editingPreference.options && (
                <Select
                  value={tempValue}
                  onChange={setTempValue}
                  style={{ width: '100%' }}
                  size="large"
                >
                  {editingPreference.options.map(opt => (
                    <Select.Option key={opt} value={opt}>
                      {opt.charAt(0).toUpperCase() + opt.slice(1).replace(/_/g, ' ')}
                    </Select.Option>
                  ))}
                </Select>
              )}

              {editingPreference.type === 'text' && (
                <Input
                  value={tempValue}
                  onChange={(e) => setTempValue(e.target.value)}
                  size="large"
                  placeholder="Enter value..."
                />
              )}

              {editingPreference.type === 'textarea' && (
                <TextArea
                  value={tempValue}
                  onChange={(e) => setTempValue(e.target.value)}
                  rows={6}
                  placeholder="Enter your custom instructions..."
                  size="large"
                />
              )}
            </Space>
          )}
        </Modal>
      </Content>
    </Layout>
  );
}
