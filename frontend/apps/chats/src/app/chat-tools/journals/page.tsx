
'use client';

import { useEffect, useState, Suspense } from 'react';
import { List, Empty, Typography, Card, Spin, Layout, Timeline, Tag, Space, Button, Select, Alert } from 'antd';
import { 
  FileTextOutlined, 
  ClockCircleOutlined, 
  BulbOutlined, 
  ToolOutlined, 
  ArrowLeftOutlined,
  ExperimentOutlined 
} from '@ant-design/icons';
import { useSearchParams, useRouter } from 'next/navigation';
import Link from 'next/link';

const { Title, Text, Paragraph } = Typography;
const { Content } = Layout;
const { Option } = Select;

// ==============================================================================
// TYPE DEFINITIONS
// ==============================================================================

// ==============================================================================
// Chat Interface
// ==============================================================================
// Represents a chat conversation in the system
// IMPORTANT: API returns 'chat_id' but we normalize to 'id' for consistency
// ==============================================================================
interface Chat {
  id: string;              // Normalized from 'chat_id' in API response
  title: string;           // User-defined or auto-generated title
  created_at: string;      // ISO 8601 timestamp
  chat_id?: string;        // Original field from API (optional after mapping)
}

// ==============================================================================
// Journal Entry Interface
// ==============================================================================
// Individual log entry showing AI's thought process
// ==============================================================================
interface JournalEntry {
  timestamp: string;                                          // When this entry occurred
  type: 'thought' | 'action' | 'observation' | 'learning';  // Category of entry
  content: string;                                            // Human-readable description
  metadata?: any;                                             // Additional context data
}

// ==============================================================================
// Journal Metadata Interface
// ==============================================================================
// Container for journal data and associated entries
// ==============================================================================
interface JournalMetadata {
  filename: string;          // Journal file identifier
  description?: string;      // Optional description
  chat_id?: string;          // Associated chat ID
  created_at?: string;       // Journal creation time
  entries?: JournalEntry[];  // Array of journal entries
}

// ==============================================================================
// HELPER FUNCTION: Get API Base URL
// ==============================================================================
// Constructs the base API URL with multiple fallback strategies
// Priority:
//   1. Environment variable (NEXT_PUBLIC_API_BASE_URL)
//   2. Window location (browser context)
//   3. Hardcoded localhost (development)
// ==============================================================================
const getApiBaseUrl = (): string => {
  // Try environment variable first
  if (process.env.NEXT_PUBLIC_API_BASE_URL) {
    return process.env.NEXT_PUBLIC_API_BASE_URL;
  }
  
  // In browser, use current origin with port 8000
  if (typeof window !== 'undefined') {
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;
    return `${protocol}//${hostname}:8000`;
  }
  
  // Fallback for server-side rendering
  return `http://${window.location.hostname}:8000`; // Dynamically use current hostname
};

function JournalsContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const initialChatId = searchParams?.get('chat_id') || '';
  
  // ==============================================================================
  // STATE MANAGEMENT
  // ==============================================================================
  const [chatId, setChatId] = useState(initialChatId);
  const [chats, setChats] = useState<Chat[]>([]);
  const [journals, setJournals] = useState<JournalMetadata[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingChats, setLoadingChats] = useState(true);
  const [selectedJournal, setSelectedJournal] = useState<JournalMetadata | null>(null);
  const [error, setError] = useState<string | null>(null);

  const apiBaseUrl = getApiBaseUrl();

  // ==============================================================================
  // EFFECT: Fetch Available Chats on Mount
  // ==============================================================================
  // Fetches all chats from the API when component first loads
  // Transforms API response to match our interface (chat_id → id)
  // ==============================================================================
  useEffect(() => {
    const fetchChats = async () => {
      try {
        setLoadingChats(true);
        setError(null);
        
        // ==================================================================
        // API CALL: Get Chats List
        // ==================================================================
        // Endpoint: /rest/api/v1/chats
        // Returns: { docs: [{ chat_id, title, created_at, ... }], ... }
        // ==================================================================
        const res = await fetch(`${apiBaseUrl}/rest/api/v1/chats?page=1&limit=100`);
        
        if (!res.ok) {
          throw new Error(`Failed to fetch chats: ${res.status} ${res.statusText}`);
        }
        
        const data = await res.json();
        
        // ==================================================================
        // DATA TRANSFORMATION: chat_id → id
        // ==================================================================
        // The API returns chats with 'chat_id' field
        // But our interface expects 'id' field
        // We map the response to normalize the field name
        // ==================================================================
        const normalizedChats = (data.docs || []).map((chat: any) => ({
          id: chat.chat_id,              // ⚠️ KEY FIX: Map chat_id to id
          chat_id: chat.chat_id,         // Keep original for reference
          title: chat.title,
          created_at: chat.created_at,
        }));
        
        console.log(`✓ Loaded ${normalizedChats.length} chats`);
        setChats(normalizedChats);
        
      } catch (err) {
        console.error('❌ Failed to fetch chats', err);
        setError(err instanceof Error ? err.message : 'Failed to load chats');
      } finally {
        setLoadingChats(false);
      }
    };
    
    fetchChats();
  }, [apiBaseUrl]);

  // ==============================================================================
  // FUNCTION: Fetch Journals for Selected Chat
  // ==============================================================================
  // Retrieves journal entries for a specific chat
  // Currently shows mock data for demonstration purposes
  // TODO: Replace with real journal data when backend is ready
  // ==============================================================================
  const fetchJournals = async (selectedChatId: string) => {
    if (!selectedChatId) {
      console.warn('⚠️ No chat ID provided');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      console.log(`📡 Fetching journals for chat: ${selectedChatId}`);
      
      // ==================================================================
      // API CALL: Get Journal Entries
      // ==================================================================
      // Endpoint: /rest/api/v1/logassist/journals
      // Returns: { items: [...] } or direct array
      // ==================================================================
      const res = await fetch(
        `${apiBaseUrl}/rest/api/v1/logassist/journals?chat_id=${selectedChatId}`,
      );
      
      if (!res.ok) {
        throw new Error(`Failed to fetch journals: ${res.status}`);
      }
      
      const data = await res.json();
      const journalList = data.items ?? data ?? [];
      setJournals(journalList);
      
      // ==================================================================
      // MOCK DATA: Creating Sample Journal Entries
      // ==================================================================
      // This section creates realistic journal entries for demonstration
      // In production, this should come from the backend
      // These entries show different aspects of AI reasoning:
      //   - THOUGHT:      Internal reasoning and analysis
      //   - ACTION:       Tools executed and operations performed
      //   - OBSERVATION:  Results and findings from actions
      //   - LEARNING:     Patterns identified and preferences learned
      // ==================================================================
      const currentTime = new Date().toISOString();
      const mockEntries: JournalEntry[] = [
        {
          timestamp: currentTime,
          type: 'thought',
          content: 'Analyzing user query to determine intent and required tools',
          metadata: { 
            confidence: 0.95, 
            complexity: 'medium',
            query_tokens: 47,
            intent: 'information_retrieval'
          }
        },
        {
          timestamp: currentTime,
          type: 'action',
          content: 'Executing internal search across documentation and knowledge base',
          metadata: { 
            tool: 'internal_search', 
            query: 'user query', 
            sources: ['docs', 'wiki', 'tickets'],
            search_time_ms: 234
          }
        },
        {
          timestamp: currentTime,
          type: 'observation',
          content: 'Found 5 highly relevant documents with 92% average confidence match',
          metadata: { 
            results_count: 5, 
            avg_relevance: 0.92,
            top_sources: ['technical_docs', 'api_reference'],
            filters_applied: 2
          }
        },
        {
          timestamp: currentTime,
          type: 'learning',
          content: 'User consistently prefers detailed technical explanations with code examples',
          metadata: { 
            pattern: 'technical_detail', 
            confidence: 0.88, 
            frequency: 12,
            user_preferences: ['code_examples', 'step_by_step', 'visuals']
          }
        },
        {
          timestamp: currentTime,
          type: 'thought',
          content: 'Synthesizing response with structured breakdown and visual hierarchy',
          metadata: { 
            approach: 'structured', 
            sections: 4,
            estimated_tokens: 450,
            target_audience: 'technical'
          }
        },
        {
          timestamp: currentTime,
          type: 'action',
          content: 'Formatting response with markdown, code blocks, and visual hierarchy',
          metadata: { 
            format: 'technical_guide', 
            code_blocks: 3,
            languages: ['typescript', 'bash'],
            markdown_features: ['tables', 'lists', 'emphasis']
          }
        }
      ];
      
      // If we have any journal data, attach mock entries for demonstration
      if (journalList.length > 0 || selectedChatId) {
        setSelectedJournal({
          filename: `journal_${selectedChatId}`,
          chat_id: selectedChatId,
          created_at: currentTime,
          description: 'AI reasoning and learning progression',
          entries: mockEntries
        });
        
        console.log(`✓ Loaded journal with ${mockEntries.length} entries`);
      } else {
        setSelectedJournal(null);
        console.log('ℹ️ No journal data available');
      }
      
    } catch (err) {
      console.error('❌ Failed to fetch journals', err);
      setError(err instanceof Error ? err.message : 'Failed to load journals');
      setSelectedJournal(null);
    } finally {
      setLoading(false);
    }
  };

  // ==============================================================================
  // EFFECT: Fetch Journals When Chat Selection Changes
  // ==============================================================================
  // Automatically fetch journal data when user selects a different chat
  // ==============================================================================
  useEffect(() => {
    if (chatId) {
      console.log(`🔄 Chat selected: ${chatId}`);
      fetchJournals(chatId);
    }
  }, [chatId]);

  // ==============================================================================
  // HANDLER: Chat Selection
  // ==============================================================================
  // Updates URL and triggers journal fetch when user selects a chat
  // ==============================================================================
  const handleChatSelect = (selectedChatId: string) => {
    console.log(`✓ User selected chat: ${selectedChatId}`);
    setChatId(selectedChatId);
    router.push(`/chat-tools/journals?chat_id=${selectedChatId}`);
  };

  // ==============================================================================
  // HELPER FUNCTIONS: Visual Styling by Entry Type
  // ==============================================================================
  
  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'thought': return <BulbOutlined style={{ fontSize: 20 }} />;
      case 'action': return <ToolOutlined style={{ fontSize: 20 }} />;
      case 'observation': return <ClockCircleOutlined style={{ fontSize: 20 }} />;
      case 'learning': return <ExperimentOutlined style={{ fontSize: 20 }} />;
      default: return <FileTextOutlined style={{ fontSize: 20 }} />;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'thought': return '#667eea';      // Purple - for reasoning
      case 'action': return '#52c41a';       // Green - for execution
      case 'observation': return '#faad14';  // Orange - for findings
      case 'learning': return '#f5576c';     // Red-pink - for insights
      default: return '#1890ff';             // Blue - default
    }
  };

  const getTypeGradient = (type: string) => {
    switch (type) {
      case 'thought': return 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
      case 'action': return 'linear-gradient(135deg, #52c41a 0%, #43e97b 100%)';
      case 'observation': return 'linear-gradient(135deg, #faad14 0%, #ffd700 100%)';
      case 'learning': return 'linear-gradient(135deg, #f5576c 0%, #f093fb 100%)';
      default: return 'linear-gradient(135deg, #1890ff 0%, #4facfe 100%)';
    }
  };

  // ==============================================================================
  // RENDER: Main Component
  // ==============================================================================
  return (
    <Layout style={{ minHeight: '100vh', background: 'linear-gradient(180deg, #f0f2f5 0%, #ffffff 100%)' }}>
      <Content style={{ padding: '24px' }}>
        <div style={{ maxWidth: 1400, margin: '0 auto' }}>
          {/* Navigation Buttons */}
          <Space style={{ marginBottom: 24 }} size="middle">
            <Button 
              icon={<ArrowLeftOutlined />} 
              onClick={() => router.back()}
              size="large"
            >
              Back
            </Button>
            <Link href="/settings">
              <Button size="large">Settings</Button>
            </Link>
            <Link href="/chat-tools/thought-visualizer">
              <Button size="large">Visualizer</Button>
            </Link>
          </Space>

          <Card 
            style={{ 
              borderRadius: '16px',
              boxShadow: '0 4px 12px rgba(192.168.0.164.08)',
              border: 'none',
              marginBottom: 24
            }}
          >
            {/* Page Header */}
            <Title level={2} style={{ 
              background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              marginBottom: 8
            }}>
              <ExperimentOutlined /> AI Learning Journal
            </Title>
            <Paragraph type="secondary" style={{ fontSize: '16px', marginBottom: 24 }}>
              Explore how the AI learns, adapts, and evolves its methodology through conversations
            </Paragraph>

            {/* Error Display */}
            {error && (
              <Alert
                message="Error"
                description={error}
                type="error"
                closable
                onClose={() => setError(null)}
                style={{ marginBottom: 24 }}
              />
            )}

            {/* Chat Selector */}
            <Card 
              size="small" 
              style={{ 
                background: 'linear-gradient(135deg, #e0e7ff 0%, #f0f4ff 100%)',
                border: 'none',
                marginBottom: 24
              }}
            >
              <Space direction="vertical" style={{ width: '100%' }} size="middle">
                <Text strong style={{ fontSize: 16 }}>
                  Select a Conversation ({chats.length} available)
                </Text>
                <Select
                  showSearch
                  placeholder={
                    loadingChats 
                      ? "Loading chats..." 
                      : chats.length === 0 
                        ? "No chats available"
                        : "Choose a chat to view its learning journal"
                  }
                  size="large"
                  style={{ width: '100%' }}
                  value={chatId || undefined}
                  onChange={handleChatSelect}
                  loading={loadingChats}
                  disabled={loadingChats || chats.length === 0}
                  filterOption={(input, option) =>
                    (option?.children as string)?.toLowerCase().includes(input.toLowerCase())
                  }
                >
                  {chats.map(chat => (
                    <Option key={chat.id} value={chat.id}>
                      {chat.title || `Chat ${chat.id.slice(0, 8)}...`}
                    </Option>
                  ))}
                </Select>
                {chats.length === 0 && !loadingChats && (
                  <Text type="secondary" style={{ fontSize: 13 }}>
                    Start a conversation to see AI learning insights
                  </Text>
                )}
              </Space>
            </Card>

            {/* Journal Content */}
            {loading ? (
              <div style={{ textAlign: 'center', padding: 64 }}>
                <Spin size="large" />
                <div style={{ marginTop: 16, color: '#666' }}>Loading journal entries...</div>
              </div>
            ) : !chatId ? (
              <Empty 
                description="Select a chat above to view its learning journal"
                image={Empty.PRESENTED_IMAGE_SIMPLE}
                style={{ padding: 64 }}
              />
            ) : selectedJournal?.entries && selectedJournal.entries.length > 0 ? (
              <>
                <Alert
                  message="Learning Progression"
                  description="This timeline shows how the AI analyzes, learns, and adapts during the conversation"
                  type="info"
                  showIcon
                  style={{ marginBottom: 24, borderRadius: 8 }}
                />
                
                {/* Journal Timeline */}
                <Timeline mode="left">
                  {selectedJournal.entries.map((entry, index) => (
                    <Timeline.Item
                      key={index}
                      dot={getTypeIcon(entry.type)}
                      color={getTypeColor(entry.type)}
                    >
                      <Card 
                        size="small" 
                        style={{ 
                          borderLeft: `4px solid ${getTypeColor(entry.type)}`,
                          marginBottom: 16,
                          boxShadow: '0 2px 8px rgba(192.168.0.164.06)'
                        }}
                      >
                        <Space direction="vertical" style={{ width: '100%' }}>
                          <Space>
                            <div style={{
                              background: getTypeGradient(entry.type),
                              color: '#fff',
                              padding: '4px 12px',
                              borderRadius: 16,
                              fontSize: 12,
                              fontWeight: 600
                            }}>
                              {entry.type.toUpperCase()}
                            </div>
                            <Text type="secondary" style={{ fontSize: 12 }}>
                              {new Date(entry.timestamp).toLocaleTimeString()}
                            </Text>
                          </Space>
                          <Paragraph style={{ margin: 0, fontSize: 15 }}>
                            {entry.content}
                          </Paragraph>
                          {entry.metadata && (
                            <details style={{ marginTop: 8 }}>
                              <summary style={{ cursor: 'pointer', color: '#666', fontSize: 13 }}>
                                View detailed metadata
                              </summary>
                              <pre style={{ 
                                fontSize: 11, 
                                background: '#fafafa', 
                                padding: 12, 
                                borderRadius: 8,
                                marginTop: 8,
                                border: '1px solid #e0e0e0',
                                overflow: 'auto'
                              }}>
                                {JSON.stringify(entry.metadata, null, 2)}
                              </pre>
                            </details>
                          )}
                        </Space>
                      </Card>
                    </Timeline.Item>
                  ))}
                </Timeline>
              </>
            ) : (
              <Empty 
                description="No journal entries available for this conversation yet"
                image={Empty.PRESENTED_IMAGE_SIMPLE}
                style={{ padding: 64 }}
              >
                <Paragraph type="secondary">
                  Journal entries are created as you interact with the AI. Start chatting to see the learning process in action!
                </Paragraph>
              </Empty>
            )}
          </Card>
        </div>
      </Content>
    </Layout>
  );
}

// ==============================================================================
// MAIN EXPORT: Journals Page with Suspense Boundary
// ==============================================================================
// Wraps main component in Suspense for Next.js App Router compatibility
// Shows loading spinner while component and data load
// ==============================================================================
export default function JournalsPage() {
  return (
    <Suspense fallback={
      <div style={{ 
        display: 'flex', 
        flexDirection: 'column',
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '100vh',
        gap: 16
      }}>
        <Spin size="large" />
        <Text type="secondary">Loading Learning Journal...</Text>
      </div>
    }>
      <JournalsContent />
    </Suspense>
  );
}

