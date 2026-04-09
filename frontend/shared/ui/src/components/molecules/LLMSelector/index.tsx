// shared/ui/src/components/molecules/LLMSelector/index.tsx
import React, { useEffect, useState } from 'react';
import { Select, message, Spin } from 'antd';
import { RobotOutlined } from '@ant-design/icons';
import styled from 'styled-components';

const { Option, OptGroup } = Select;

interface LLMModel {
  id: number;
  provider_id: number;
  model_name: string;
  display_name: string;
  description: string;
  is_active: boolean;
  is_default: boolean;
}

interface LLMProvider {
  id: number;
  name: string;
  display_name: string;
  is_active: boolean;
}

const StyledSelect = styled(Select)`
  min-width: 250px;
  
  .ant-select-selector {
    border-radius: 8px !important;
  }
`;

const LLMSelector: React.FC = () => {
  const [models, setModels] = useState<LLMModel[]>([]);
  const [providers, setProviders] = useState<Record<number, LLMProvider>>({});
  const [selectedModel, setSelectedModel] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchModels();
    fetchProviders();
  }, []);

  const fetchProviders = async () => {
    try {
      const response = await fetch('/rest/api/v1/llm/providers');
      const data = await response.json();
      const providerMap = data.reduce((acc: Record<number, LLMProvider>, p: LLMProvider) => {
        acc[p.id] = p;
        return acc;
      }, {});
      setProviders(providerMap);
    } catch (error) {
      console.error('Failed to fetch providers:', error);
    }
  };

  const fetchModels = async () => {
    try {
      setLoading(true);
      const response = await fetch('/rest/api/v1/llm/models');
      const data = await response.json();
      
      // Filter only active models
      const activeModels = data.filter((m: LLMModel) => m.is_active);
      setModels(activeModels);
      
      // Set default model as selected
      const defaultModel = activeModels.find((m: LLMModel) => m.is_default);
      if (defaultModel) {
        setSelectedModel(defaultModel.id);
      }
    } catch (error) {
      message.error('Failed to load LLM models');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleModelChange = async (modelId: number) => {
    try {
      const response = await fetch('/rest/api/v1/llm/select', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model_id: modelId }),
      });
      
      if (response.ok) {
        setSelectedModel(modelId);
        const model = models.find(m => m.id === modelId);
        message.success(`Switched to ${model?.display_name}`);
      } else {
        message.error('Failed to switch model');
      }
    } catch (error) {
      message.error('Failed to switch model');
      console.error(error);
    }
  };

  // Group models by provider
  const modelsByProvider = models.reduce((acc, model) => {
    const providerId = model.provider_id;
    if (!acc[providerId]) {
      acc[providerId] = [];
    }
    acc[providerId].push(model);
    return acc;
  }, {} as Record<number, LLMModel[]>);

  if (loading) {
    return <Spin size="small" />;
  }

  return (
    <StyledSelect
      value={selectedModel}
      onChange={handleModelChange}
      placeholder="Select AI Model"
      suffixIcon={<RobotOutlined />}
      showSearch
      optionFilterProp="children"
    >
      {Object.entries(modelsByProvider).map(([providerId, providerModels]) => {
        const provider = providers[Number(providerId)];
        if (!provider) return null;

        return (
          <OptGroup key={providerId} label={provider.display_name}>
            {providerModels.map((model) => (
              <Option key={model.id} value={model.id}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>{model.display_name}</span>
                  {model.is_default && (
                    <span style={{ color: '#1890ff', fontSize: '12px' }}>(Default)</span>
                  )}
                </div>
                <div style={{ fontSize: '12px', color: '#888' }}>
                  {model.description}
                </div>
              </Option>
            ))}
          </OptGroup>
        );
      })}
    </StyledSelect>
  );
};

export default LLMSelector;

