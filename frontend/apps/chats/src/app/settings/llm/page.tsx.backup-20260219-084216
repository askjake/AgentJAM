
"use client";

import React, { useState, useEffect } from "react";
import {
  App,
  Card,
  Button,
  Modal,
  Form,
  Select,
  Input,
  Switch,
  message,
  Slider,
  Tag,
  Tooltip
} from "antd";
import {
  PlusOutlined,
  DeleteOutlined,
  CheckCircleOutlined,
  ThunderboltOutlined,
  CrownOutlined,
  RocketOutlined,
  FireOutlined,
  InfoCircleOutlined
} from "@ant-design/icons";

const { Option, OptGroup } = Select;
const { TextArea } = Input;

// Types
interface Provider {
  id: number;
  name: string;
  display_name: string;
  provider_type: string;
}

interface Model {
  id: number;
  provider_id: number;
  model_name: string;
  model_id: string;
  display_name: string;
  description?: string;
  context_length: number;
  custom_model_arn?: string;
}

interface UserConfig {
  id: number;
  user_email: string;
  provider_id: number;
  model_id: number;
  custom_model_arn?: string;
  use_custom_arn?: boolean;
  custom_arn?: string;
  api_base?: string;
  region?: string;
  is_default: boolean;
  temperature?: number;
  max_tokens?: number;
  custom_config?: any;
  has_api_key: boolean;
}

interface SuccessState {
  show: boolean;
  modelName: string;
}

// Model metadata for visual enhancements
const getModelMetadata = (modelName: string, displayName: string) => {
  const name = (modelName + displayName).toLowerCase();
  
  if (name.includes("4.6") || name.includes("4-6")) {
    return {
      emoji: "🌟",
      gradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      speed: "Fastest",
      intelligence: 99,
      cost: "$$$",
      specialty: "Latest & Greatest"
    };
  }
  if (name.includes("sonnet-4") || name.includes("sonnet 4")) {
    return {
      emoji: "🚀",
      gradient: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
      speed: "Fast",
      intelligence: 98,
      cost: "$$$",
      specialty: "Next-Gen Power"
    };
  }
  if (name.includes("opus")) {
    return {
      emoji: "👑",
      gradient: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
      speed: "Balanced",
      intelligence: 97,
      cost: "$$$",
      specialty: "Maximum Intelligence"
    };
  }
  if (name.includes("sonnet") && name.includes("3.5")) {
    return {
      emoji: "🎵",
      gradient: "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
      speed: "Fast",
      intelligence: 95,
      cost: "$$",
      specialty: "Best Balance"
    };
  }
  if (name.includes("haiku")) {
    return {
      emoji: "⚡",
      gradient: "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
      speed: "Fastest",
      intelligence: 85,
      cost: "$",
      specialty: "Lightning Speed"
    };
  }
  if (name.includes("gpt-4o")) {
    return {
      emoji: "🌟",
      gradient: "linear-gradient(135deg, #52a5ff 0%, #5ce1e6 100%)",
      speed: "Fast",
      intelligence: 96,
      cost: "$$",
      specialty: "OpenAI Flagship"
    };
  }
  if (name.includes("gpt-4")) {
    return {
      emoji: "🤖",
      gradient: "linear-gradient(135deg, #30cfd0 0%, #330867 100%)",
      speed: "Medium",
      intelligence: 94,
      cost: "$$",
      specialty: "Reliable"
    };
  }
  
  return {
    emoji: "🔮",
    gradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    speed: "Medium",
    intelligence: 90,
    cost: "$$",
    specialty: "Versatile"
  };
};

export default function LLMSettingsPage() {
  const { message } = App.useApp(); // FIX: Use Ant Design context API
  const [providers, setProviders] = useState<Provider[]>([]);
  const [models, setModels] = useState<Model[]>([]);
  const [userConfigs, setUserConfigs] = useState<UserConfig[]>([]);
  const [selectedModel, setSelectedModel] = useState<number | null>(null);
  const [selectedProvider, setSelectedProvider] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showSuccess, setShowSuccess] = useState<SuccessState>({ show: false, modelName: "" });
  const [form] = Form.useForm();
  
  // Advanced settings
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [temperature, setTemperature] = useState(0.7);
  const [maxTokens, setMaxTokens] = useState(4096);
  
  const BASE_URL = "http://0.0.0.0:8000/rest/api/v1";
  const userEmail = "jacob.montjac@dish.com";

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    console.log("Fetching LLM data...");
    
    try {
      const headers = { "X-User-Email": userEmail };
      
      const [providersRes, modelsRes, configsRes] = await Promise.all([
        fetch(`${BASE_URL}/llm/providers`, { headers }),
        fetch(`${BASE_URL}/llm/models`, { headers }),
        fetch(`${BASE_URL}/llm/my-configs`, { headers })
      ]);

      if (providersRes.ok && modelsRes.ok && configsRes.ok) {
        const providersData = await providersRes.json();
        const modelsData = await modelsRes.json();
        const configsData = await configsRes.json();
        
        setProviders(providersData);
        setModels(modelsData);
        setUserConfigs(configsData);
        
        console.log("Providers loaded:", providersData.length);
        console.log("Models loaded:", modelsData.length);
        console.log("User configs loaded:", configsData.length);
        
        // Find active config
        const activeConfig = configsData.find((c: UserConfig) => c.is_default);
        if (activeConfig) {
          setSelectedModel(activeConfig.model_id);
          setSelectedProvider(activeConfig.provider_id);
          setTemperature(activeConfig.temperature || 0.7);
          setMaxTokens(activeConfig.max_tokens || 4096);
          console.log("Active config found:", activeConfig);
        }
      }
    } catch (error) {
      console.error("Error fetching LLM data:", error);
      message.error("Failed to load LLM configuration");
    } finally {
      setLoading(false);
    }
  };

  const handleSelectModel = async (modelId: number, providerId: number) => {
    console.log("Selecting model:", { modelId, providerId, temperature, maxTokens });
    
    const selectedModelData = models.find(m => m.id === modelId);
    
    try {
      // FIX: Check if config already exists for this model/provider combo
      const existingConfig = userConfigs.find(c => 
        c.model_id === modelId && c.provider_id === providerId
      );

      if (existingConfig) {
        // UPDATE existing config to make it default
        console.log("Found existing config, updating to default:", existingConfig.id);
        
        const response = await fetch(`${BASE_URL}/llm/my-configs/${existingConfig.id}`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            "X-User-Email": userEmail
          },
          body: JSON.stringify({
            is_default: true,
            temperature: temperature,
            max_tokens: maxTokens
          })
        });

        console.log("Update response status:", response.status);
        
        if (response.ok) {
          const result = await response.json();
          console.log("Update successful:", result);
          
          setSelectedModel(modelId);
          setSelectedProvider(providerId);
          
          // Show success animation
          setShowSuccess({
            show: true,
            modelName: selectedModelData?.display_name || "Model"
          });
          
          setTimeout(() => {
            setShowSuccess({ show: false, modelName: "" });
          }, 2000);
          
          message.success(`Selected ${selectedModelData?.display_name}!`);
          await fetchData();
        } else {
          const errorText = await response.text();
          console.error("Update failed:", errorText);
          message.error("Failed to select model");
        }
      } else {
        // CREATE new config
        console.log("No existing config found, creating new one");
        
        const response = await fetch(`${BASE_URL}/llm/my-configs`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-User-Email": userEmail
          },
          body: JSON.stringify({
            provider_id: providerId,
            model_id: modelId,
            is_default: true,
            temperature: temperature,
            max_tokens: maxTokens
          })
        });

        console.log("Creation response status:", response.status);
        
        if (response.ok) {
          const result = await response.json();
          console.log("Creation successful:", result);
          
          setSelectedModel(modelId);
          setSelectedProvider(providerId);
          
          // Show success animation
          setShowSuccess({
            show: true,
            modelName: selectedModelData?.display_name || "Model"
          });
          
          setTimeout(() => {
            setShowSuccess({ show: false, modelName: "" });
          }, 2000);
          
          message.success(`Selected ${selectedModelData?.display_name}!`);
          await fetchData();
        } else {
          const errorText = await response.text();
          console.error("Creation failed:", errorText);
          message.error("Failed to select model");
        }
      }
    } catch (error) {
      console.error("Error selecting model:", error);
      message.error("Error selecting model");
    }
  };

  const handleAddCustomLLM = async (values: any) => {
    console.log("Adding custom LLM:", values);
    
    try {
      const payload: any = {
        provider_id: values.provider_id,
        model_id: values.model_id,
        is_selected: values.set_as_active || false,
        temperature: temperature,
        max_tokens: maxTokens
      };
      
      // Add custom ARN if provided
      if (values.custom_arn && values.custom_arn.trim()) {
        payload.custom_model_arn = values.custom_arn.trim();
        payload.use_custom_arn = true;
      }
      
      if (values.api_key) payload.api_key = values.api_key;
      if (values.region) payload.region = values.region;
      if (values.api_base) payload.api_base = values.api_base;

      const response = await fetch(`${BASE_URL}/llm/my-configs`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-User-Email": userEmail
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        message.success("Custom LLM added successfully!");
        setShowAddModal(false);
        form.resetFields();
        await fetchData();
      } else {
        const error = await response.json();
        message.error(error.detail || "Failed to add custom LLM");
      }
    } catch (error) {
      console.error("Error adding custom LLM:", error);
      message.error("Error adding custom LLM");
    }
  };

  const handleDeleteConfig = async (configId: number) => {
    try {
      const response = await fetch(`${BASE_URL}/llm/my-configs/${configId}`, {
        method: "DELETE",
        headers: { "X-User-Email": userEmail }
      });

      if (response.ok) {
        message.success("Configuration deleted");
        await fetchData();
      } else {
        message.error("Failed to delete configuration");
      }
    } catch (error) {
      console.error("Error deleting config:", error);
      message.error("Error deleting configuration");
    }
  };

  const getProviderName = (providerId: number) => {
    const provider = providers.find(p => p.id === providerId);
    return provider?.display_name || provider?.name || "Unknown";
  };

  const getProviderEmoji = (providerType: string) => {
    const emojiMap: { [key: string]: string } = {
      "aws-bedrock": "☁️",
      "anthropic": "🔮",
      "openai": "🎯",
      "ollama": "🏠"
    };
    return emojiMap[providerType] || "🤖";
  };

  // Group models by provider
  const modelsByProvider: { [key: number]: Model[] } = {};
  models.forEach(model => {
    if (!modelsByProvider[model.provider_id]) {
      modelsByProvider[model.provider_id] = [];
    }
    modelsByProvider[model.provider_id].push(model);
  });

  return (
    <div style={{ 
      minHeight: "100vh",
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)",
      padding: "40px 20px"
    }}>
      {/* Success Overlay */}
      {showSuccess.show && (
        <div style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: "rgba(0, 0, 0, 0.7)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 10000,
          animation: "fadeIn 0.3s ease-in"
        }}>
          <div style={{
            background: "white",
            borderRadius: "20px",
            padding: "40px",
            textAlign: "center",
            animation: "successPop 0.5s ease-out"
          }}>
            <CheckCircleOutlined style={{ fontSize: 64, color: "#52c41a", marginBottom: 20 }} />
            <h2 style={{ margin: 0, marginBottom: 10 }}>Perfect Choice! 🎉</h2>
            <p style={{ fontSize: 18, color: "#666", margin: 0 }}>
              {showSuccess.modelName} is ready to go!
            </p>
          </div>
        </div>
      )}

      <div style={{ maxWidth: 1400, margin: "0 auto" }}>
        {/* Hero Section */}
        <div style={{ 
          textAlign: "center", 
          marginBottom: 40,
          animation: "fadeIn 0.6s ease-in"
        }}>
          <h1 style={{ 
            fontSize: 48, 
            fontWeight: "bold", 
            color: "white",
            textShadow: "0 2px 4px rgba(192.168.0.164.2)",
            marginBottom: 10
          }}>
            Choose Your AI Companion
          </h1>
          <p style={{ fontSize: 18, color: "rgba(255,255,255,0.9)", marginBottom: 20 }}>
            Select the perfect model for your needs
          </p>
          
          {/* Active Model Badge */}
          {selectedModel && (
            <div style={{
              display: "inline-block",
              background: "rgba(255,255,255,0.2)",
              backdropFilter: "blur(10px)",
              padding: "10px 20px",
              borderRadius: "25px",
              marginBottom: 20
            }}>
              <CheckCircleOutlined style={{ color: "#52c41a", marginRight: 8 }} />
              <span style={{ color: "white", fontWeight: 500 }}>
                Currently Active: {models.find(m => m.id === selectedModel)?.display_name}
              </span>
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div style={{ 
          display: "flex", 
          justifyContent: "space-between", 
          marginBottom: 30,
          gap: 20,
          flexWrap: "wrap"
        }}>
          <Button 
            type="primary" 
            size="large"
            icon={<PlusOutlined />}
            onClick={() => setShowAddModal(true)}
            style={{
              background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              border: "none",
              height: 48,
              borderRadius: 24,
              fontSize: 16,
              fontWeight: 600,
              boxShadow: "0 4px 15px rgba(102, 126, 234, 0.4)"
            }}
          >
            Add Custom LLM
          </Button>
          
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ color: "white", fontWeight: 500 }}>Advanced Mode</span>
            <Switch 
              checked={showAdvanced}
              onChange={setShowAdvanced}
              style={{ 
                background: showAdvanced ? "#52c41a" : "rgba(255,255,255,0.3)"
              }}
            />
          </div>
        </div>

        {/* Advanced Settings Panel */}
        {showAdvanced && (
          <Card
            style={{
              marginBottom: 30,
              borderRadius: 16,
              overflow: "hidden",
              animation: "expandDown 0.3s ease-out",
              background: "linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.9) 100%)"
            }}
          >
            <h3 style={{ marginTop: 0 }}>⚙️ Advanced Settings</h3>
            
            <div style={{ marginBottom: 24 }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                <span style={{ fontWeight: 500 }}>Temperature: {temperature}</span>
                <div style={{ fontSize: 12, color: "#666" }}>
                  <span style={{ marginRight: 16 }}>Precise</span>
                  <span style={{ marginRight: 16 }}>Balanced</span>
                  <span>Creative</span>
                </div>
              </div>
              <Slider 
                min={0}
                max={1}
                step={0.1}
                value={temperature}
                onChange={setTemperature}
                marks={{
                  0: "0",
                  0.5: "0.5",
                  1: "1"
                }}
              />
            </div>

            <div style={{ marginBottom: 24 }}>
              <span style={{ fontWeight: 500 }}>Max Tokens:</span>
              <Input 
                type="number"
                value={maxTokens}
                onChange={(e) => setMaxTokens(Number(e.target.value))}
                min={100}
                max={200000}
                style={{ marginTop: 8 }}
              />
            </div>

            <div>
              <span style={{ fontWeight: 500, display: "block", marginBottom: 8 }}>
                Quick Select (All Available Models):
              </span>
              <Select
                showSearch
                style={{ width: "100%" }}
                placeholder="Search and select any model..."
                optionFilterProp="children"
                onChange={(value) => {
                  const [modelId, providerId] = value.split("-");
                  handleSelectModel(Number(modelId), Number(providerId));
                }}
                filterOption={(input, option: any) =>
                  option?.children?.toLowerCase().indexOf(input.toLowerCase()) >= 0
                }
              >
                {providers.map(provider => {
                  const providerModels = modelsByProvider[provider.id] || [];
                  if (providerModels.length === 0) return null;
                  
                  return (
                    <OptGroup 
                      key={provider.id} 
                      label={`${getProviderEmoji(provider.provider_type)} ${provider.display_name || provider.name}`}
                    >
                      {providerModels.map(model => (
                        <Option 
                          key={model.id} 
                          value={`${model.id}-${model.provider_id}`}
                        >
                          {getModelMetadata(model.model_name, model.display_name).emoji} {model.display_name} 
                          <span style={{ fontSize: 12, color: "#999", marginLeft: 8 }}>
                            ({model.context_length.toLocaleString()} tokens)
                          </span>
                        </Option>
                      ))}
                    </OptGroup>
                  );
                })}
              </Select>
            </div>
          </Card>
        )}

        {/* Model Cards by Provider */}
        {providers.map(provider => {
          const providerModels = modelsByProvider[provider.id] || [];
          if (providerModels.length === 0) return null;

          return (
            <div 
              key={provider.id}
              style={{ 
                marginBottom: 40,
                animation: "slideUp 0.6s ease-out"
              }}
            >
              <h2 style={{ 
                color: "white", 
                fontSize: 28,
                marginBottom: 20,
                textShadow: "0 2px 4px rgba(192.168.0.164.2)"
              }}>
                {getProviderEmoji(provider.provider_type)} {provider.display_name || provider.name}
              </h2>
              
              <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))",
                gap: 20
              }}>
                {providerModels.map(model => {
                  const metadata = getModelMetadata(model.model_name, model.display_name);
                  const isSelected = model.id === selectedModel;
                  
                  return (
                    <Card
                      key={model.id}
                      hoverable
                      onClick={() => handleSelectModel(model.id, model.provider_id)}
                      style={{
                        borderRadius: 16,
                        overflow: "hidden",
                        cursor: "pointer",
                        transition: "all 0.3s ease",
                        border: isSelected ? "3px solid #52c41a" : "none",
                        background: isSelected ? metadata.gradient : "white",
                        color: isSelected ? "white" : "inherit",
                        position: "relative",
                        transform: isSelected ? "scale(1.02)" : "scale(1)",
                        boxShadow: isSelected 
                          ? "0 8px 30px rgba(82, 196, 26, 0.3)"
                          : "0 4px 15px rgba(192.168.0.164.1)"
                      }}
                    >
                      {isSelected && (
                        <div style={{
                          position: "absolute",
                          top: 10,
                          right: 10,
                          background: "rgba(82, 196, 26, 0.9)",
                          borderRadius: "50%",
                          width: 40,
                          height: 40,
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          zIndex: 10
                        }}>
                          <CheckCircleOutlined style={{ fontSize: 24, color: "white" }} />
                        </div>
                      )}
                      
                      <div style={{ fontSize: 48, marginBottom: 12 }}>
                        {metadata.emoji}
                      </div>
                      
                      <h3 style={{ 
                        fontSize: 22, 
                        fontWeight: "bold",
                        marginBottom: 8,
                        color: isSelected ? "white" : "inherit"
                      }}>
                        {model.display_name}
                      </h3>
                      
                      {model.description && (
                        <p style={{ 
                          fontSize: 14, 
                          marginBottom: 16,
                          color: isSelected ? "rgba(255,255,255,0.9)" : "#666"
                        }}>
                          {model.description}
                        </p>
                      )}
                      
                      <div style={{ 
                        display: "flex", 
                        gap: 8, 
                        flexWrap: "wrap",
                        marginBottom: 16
                      }}>
                        <Tag color={isSelected ? "success" : "default"}>
                          ⚡ {metadata.speed}
                        </Tag>
                        <Tag color={isSelected ? "success" : "default"}>
                          🧠 {metadata.intelligence}/100
                        </Tag>
                        <Tag color={isSelected ? "success" : "default"}>
                          💰 {metadata.cost}
                        </Tag>
                      </div>
                      
                      <Tag 
                        color={isSelected ? "success" : "processing"}
                        style={{ marginBottom: 12 }}
                      >
                        {metadata.specialty}
                      </Tag>
                      
                      <div style={{ 
                        fontSize: 12,
                        color: isSelected ? "rgba(255,255,255,0.8)" : "#999",
                        marginTop: 12
                      }}>
                        📝 {model.context_length.toLocaleString()} tokens
                      </div>
                      
                      <div style={{ 
                        marginTop: 16,
                        paddingTop: 16,
                        borderTop: `1px solid ${isSelected ? "rgba(255,255,255,0.3)" : "#f0f0f0"}`,
                        textAlign: "center",
                        fontWeight: 600,
                        fontSize: 14
                      }}>
                        {isSelected ? "✓ ACTIVE" : "Click to select"}
                      </div>
                    </Card>
                  );
                })}
              </div>
            </div>
          );
        })}

        {/* Custom Configurations */}
        {userConfigs.length > 0 && (
          <Card
            title="Your Custom Configurations"
            style={{
              marginTop: 40,
              borderRadius: 16,
              background: "white",
              animation: "slideUp 0.8s ease-out"
            }}
          >
            {userConfigs.map(config => {
              const model = models.find(m => m.id === config.model_id);
              const isActive = config.is_default;
              
              return (
                <div
                  key={config.id}
                  style={{
                    padding: 16,
                    marginBottom: 12,
                    borderRadius: 8,
                    background: isActive ? "#f6ffed" : "#fafafa",
                    border: isActive ? "2px solid #52c41a" : "1px solid #d9d9d9",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center"
                  }}
                >
                  <div>
                    <div style={{ fontWeight: 600, fontSize: 16, marginBottom: 4 }}>
                      {getProviderEmoji(providers.find(p => p.id === config.provider_id)?.provider_type || "")}
                      {" "}
                      {model?.display_name}
                      {isActive && (
                        <CheckCircleOutlined style={{ color: "#52c41a", marginLeft: 8 }} />
                      )}
                    </div>
                    <div style={{ fontSize: 12, color: "#666" }}>
                      {getProviderName(config.provider_id)}
                      {config.has_api_key && " • API Key configured"}
                      {config.custom_model_arn && " • Custom ARN"}
                    </div>
                  </div>
                  <div style={{ display: "flex", gap: 8 }}>
                    {!isActive && (
                      <Button
                        type="primary"
                        size="small"
                        onClick={() => handleSelectModel(config.model_id, config.provider_id)}
                      >
                        Select
                      </Button>
                    )}
                    <Button
                      danger
                      size="small"
                      icon={<DeleteOutlined />}
                      onClick={() => handleDeleteConfig(config.id)}
                    >
                      Delete
                    </Button>
                  </div>
                </div>
              );
            })}
          </Card>
        )}

        {/* Quick Tips */}
        <Card
          style={{
            marginTop: 40,
            borderRadius: 16,
            background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            border: "none",
            color: "white"
          }}
        >
          <h3 style={{ color: "white", marginTop: 0 }}>💡 Quick Tips</h3>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", gap: 16 }}>
            <div>
              <ThunderboltOutlined style={{ fontSize: 24, marginBottom: 8 }} />
              <div style={{ fontWeight: 600 }}>Need Speed?</div>
              <div style={{ fontSize: 14, opacity: 0.9 }}>Choose Haiku for instant responses</div>
            </div>
            <div>
              <CrownOutlined style={{ fontSize: 24, marginBottom: 8 }} />
              <div style={{ fontWeight: 600 }}>Maximum Power?</div>
              <div style={{ fontSize: 14, opacity: 0.9 }}>Opus 4 for complex reasoning</div>
            </div>
            <div>
              <RocketOutlined style={{ fontSize: 24, marginBottom: 8 }} />
              <div style={{ fontWeight: 600 }}>Best Balance?</div>
              <div style={{ fontSize: 14, opacity: 0.9 }}>Sonnet 4.6 for everything</div>
            </div>
          </div>
        </Card>
      </div>

      {/* Add Custom LLM Modal */}
      <Modal
        title={<span style={{ fontSize: 20, fontWeight: 600 }}>Add Custom LLM</span>}
        open={showAddModal}
        onCancel={() => {
          setShowAddModal(false);
          form.resetFields();
        }}
        footer={null}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleAddCustomLLM}
        >
          <Form.Item
            label="Provider"
            name="provider_id"
            rules={[{ required: true, message: "Please select a provider" }]}
          >
            <Select
              placeholder="Select provider"
              onChange={(value) => {
                form.setFieldsValue({ model_id: undefined });
              }}
            >
              {providers.map(p => (
                <Option key={p.id} value={p.id}>
                  {getProviderEmoji(p.provider_type)} {p.display_name || p.name}
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            noStyle
            shouldUpdate={(prevValues, currentValues) => 
              prevValues.provider_id !== currentValues.provider_id
            }
          >
            {({ getFieldValue }) => {
              const selectedProviderId = getFieldValue("provider_id");
              const availableModels = selectedProviderId 
                ? modelsByProvider[selectedProviderId] || []
                : [];

              return (
                <Form.Item
                  label="Model"
                  name="model_id"
                  rules={[{ required: true, message: "Please select a model" }]}
                >
                  <Select placeholder="Select model" disabled={!selectedProviderId}>
                    {availableModels.map(m => (
                      <Option key={m.id} value={m.id}>
                        {m.display_name}
                      </Option>
                    ))}
                  </Select>
                </Form.Item>
              );
            }}
          </Form.Item>

          <Form.Item
            label={
              <span>
                Custom Bedrock ARN (Optional){" "}
                <Tooltip title="Paste a Bedrock inference profile ARN here to use a specific cross-region endpoint">
                  <InfoCircleOutlined style={{ color: "#1890ff" }} />
                </Tooltip>
              </span>
            }
            name="custom_arn"
          >
            <TextArea
              rows={3}
              placeholder="arn:aws:bedrock:us::233532778289:inference-profile/us.anthropic.claude-sonnet-4-6-v1:0"
              style={{ fontFamily: "monospace", fontSize: 12 }}
            />
          </Form.Item>

          <Form.Item
            label="API Key (if required)"
            name="api_key"
          >
            <Input.Password placeholder="Enter API key" />
          </Form.Item>

          <Form.Item
            label="Region (for AWS Bedrock)"
            name="region"
          >
            <Input placeholder="us-west-2" />
          </Form.Item>

          <Form.Item
            label="API Base URL (for custom endpoints)"
            name="api_base"
          >
            <Input placeholder="https://..." />
          </Form.Item>

          <Form.Item
            name="set_as_active"
            valuePropName="checked"
          >
            <Switch /> Set as active model
          </Form.Item>

          <Form.Item style={{ marginBottom: 0, marginTop: 24 }}>
            <div style={{ display: "flex", gap: 12, justifyContent: "flex-end" }}>
              <Button onClick={() => {
                setShowAddModal(false);
                form.resetFields();
              }}>
                Cancel
              </Button>
              <Button type="primary" htmlType="submit">
                Add LLM
              </Button>
            </div>
          </Form.Item>
        </Form>
      </Modal>

      <style jsx global>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        @keyframes successPop {
          0% {
            opacity: 0;
            transform: scale(0.5);
          }
          50% {
            transform: scale(1.05);
          }
          100% {
            opacity: 1;
            transform: scale(1);
          }
        }
        
        @keyframes expandDown {
          from {
            opacity: 0;
            max-height: 0;
          }
          to {
            opacity: 1;
            max-height: 1000px;
          }
        }
        
        .ant-card {
          transition: all 0.3s ease;
        }
        
        .ant-card:hover {
          transform: translateY(-4px);
          box-shadow: 0 6px 20px rgba(192.168.0.164.15) !important;
        }
      `}</style>
    </div>
  );
}
