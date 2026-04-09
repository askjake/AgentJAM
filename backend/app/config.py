from typing import Literal, Optional, ClassVar
from functools import lru_cache, cached_property
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, Field


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    NAME: str = "Dish-Chat"
    VERSION: str = "2.1.0"
    AGENT_THOUGHT_CAPTURE_ENABLED: bool = Field(default=False)
    AGENT_VIZ_SERVER_URL: str = Field(default="http://localhost:8000/rest/api/v1/viz/event")
    API_PREFIX: str = "/rest/api/v1"

    # Compatibility env vars (safe to ignore if unused)
    OLLAMA_BASE_URL: Optional[str] = None
    AWS_ENDPOINT_URL: Optional[str] = None

    # Runtime settings
    DEBUG: bool = False
    LOCAL: bool = True
    
    # Authentication Settings
    AUTH_DISABLED: bool = False  # Set to True to disable auth requirement (dev/testing only)
    DEFAULT_USER_EMAIL: str = "test.user@dish.com"  # Default email when auth is disabled
    ECHO_SQL: bool = False
    FASTAPI_HOST: str = "0.0.0.0"
    FASTAPI_PORT: int = 8000
    CLEANUP_TIMEOUT: int = 600
    
    # Idle chat checker settings
    IDLE_CHAT_CHECKER_ENABLED: bool = True
    IDLE_CHAT_CHECK_INTERVAL_MINUTES: int = 10  # How often to check for idle chats
    IDLE_CHAT_THRESHOLD_MINUTES: int = 30  # Minutes of inactivity before triggering journal
    IDLE_CHAT_MIN_MESSAGES: int = 5  # Minimum messages required for journal generation
    SPOOLED_MAX_SIZE: int = 2 * 1024 * 1024
    # Default key is for testing only. Prod key is passed in via env var
    MASTER_KEY: str = "SoWTrLlo3xu1ExZIvSNQMpldDmUHc5cxbmrxlPN2RvI="

    # DB
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5434
    POSTGRES_DB: str = "dishchat"
    POSTGRES_USER: str = "dev_user"
    POSTGRES_PWD: str = "dev123"

    @computed_field
    @cached_property
    def POSTGRES_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PWD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @computed_field
    @cached_property
    def POSTGRES_SQLALCHEMY_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PWD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # LLM Models - P for Power and E for Efficient
    PLLM_PROVIDER: Literal["aws-bedrock", "openai", "anthropic", "ollama"] = "aws-bedrock"
    PLLM_API_BASE: Optional[str] = None
    PLLM_MODEL: str = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
    PLLM_CTX_LEN: int = 200_000
    ELLM_PROVIDER: Optional[Literal["aws-bedrock", "openai", "anthropic", "ollama"]] = (
        "aws-bedrock"
    )
    ELLM_API_BASE: Optional[str] = None
    ELLM_MODEL: Optional[str] = "us.anthropic.claude-3-5-haiku-20241022-v1:0"
    ELLM_CTX_LEN: Optional[int] = 200_000
    LLM_TOKENIZER: Optional[str] = None  # HuggingFace Model ID or OpenAI
    DEFAULT_TEMP: float = 0.6
    DEFAULT_REASONING: bool = False
    REASONING_BUDGET: int = 6000

    # Embeddings
    EMBED_PROVIDER: Literal["aws-bedrock", "openai", "ollama"] = "aws-bedrock"
    EMBED_API_BASE: Optional[str] = None
    EMBED_MODEL: str = "cohere.embed-multilingual-v3"
    EMBED_TOKENIZER: str = "Cohere/Cohere-embed-multilingual-v3.0"
    EMBED_CHUNK_SIZE: int = 300
    EMBED_OVERLAP: int = 0
    EMBED_BATCH_SIZE: int = 96  # Max supported by cohere model
    SUMMARY_LEN: int = 300

    # AWS Settings:
    AWS_REGION: Optional[str] = "us-west-2"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_SESSION_TOKEN: Optional[str] = None
    
    # AWS Bedrock Configuration
    BEDROCK_READ_TIMEOUT: int = 300  # 5 minutes for long streaming responses
    BEDROCK_CONNECT_TIMEOUT: int = 10
    BEDROCK_MAX_RETRIES: int = 3

    # Chat Settings:
    MAX_CHAT_COUNT: int = 9999
    MAX_GROUPS_WITH_CHATS_COUNT: int = 20
    MAX_TITLE_LEN: int = 40
    MAX_TITLE_RETRY: int = 5

    # Message Settings:
    MAX_VERSION_COUNT: int = 10
    MAX_IN_CTX_DOC_LEN: int = 4000
    MAX_OUTPUT_COUNT: int = 12_000

    # Attachment Settings:
    SUPPORTED_DOC_TYPES: list[str] = [
        "application/pdf",
        "text/plain",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]
    SUPPORTED_IMAGE_TYPES: list[str] = [
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
    ]
    MAX_IMAGE_RES: int = 1092 * 1092

    # Vault Settings:
    VAULT_SESSION_DURATION_SEC: int = 3 * 3600
    ARGON2_TIME: int = 3
    ARGON2_MEM: int = 2**16
    ARGON2_PRL: int = 1

    # Context Manager
    MAX_CONTEXT: int = Field(default=200000, description="Max length of core memory + conversation memory")  # Configurable via env
    MAX_CONV_CACHE: float = 0.6  # Max proportion of conversation cache
    SUMMARIZE_WORD_LIMIT: int = 250
    CACHE_EVICT_PROP: float = 0.5  # Amount of conversation cache to evict each time

    # Agent Settings:
    MAX_CACHEPOINT_CNT: int = 4
    # LangGraph recursion limit (for agent tool loops)
    LANGGRAPH_RECURSION_LIMIT: int = 200  # Increased to handle complex agent workflows


    # Beta report agent:
    BETAREPORT_MCP_CONFIG: dict = {
        "beta_report": {
            "transport": "streamable_http",
            "url": "https://7quifnvo576d2m5rhbnguwgvfq0qbivs.lambda-url.us-west-2.on.aws/mcp",
            # "url": "http://127.0.0.1:8001/mcp",
            "headers": {"Authorization": "Bearer yxuRJ1BuBuLRyha57xfmQXUcoWOJ7Tlw"},
        }
    }


    # Viewership measurement MCP (Lambda URL)
    # Viewership MCP config (currently unused - using internal Trino tools instead)
    VIEWERSHIP_MEASUREMENT_MCP_CONFIG: dict = {
        "viewership_measurement": {
            "transport": "streamable_http",
            "url": "https://cy4h556zxlhqyjju5psohdr6ou0scrxj.lambda-url.us-west-2.on.aws/mcp",
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            "timeout": {"seconds": 120},  # 2 minutes for HTTP operations
            "sse_read_timeout": {"seconds": 600}  # 10 minutes for SSE reads
        }
    }

    # Coverity Assist / log analysis MCP:
    LOG_ASSIST_MCP_CONFIG: dict = {
        "log_assist": {
            "transport": "streamable_http",
            "url": "http://127.0.0.1:5000/mcp",
        }
    }

    # Internal micro-tools MCP (SSO-protected):
    INTERNAL_TOOLS_MCP_CONFIG: dict = {
        "internal_tools": {
            "transport": "streamable_http",
            "url": "https://internal-tools.yourdomain/mcp",
        }
    }

    # External service endpoints
    COVERITY_GATEWAY_URL: str = "http://127.0.0.1:5000"

    # Sentry Integration (for cluster inspection and monitoring)
    SENTRY_AUTH_TOKEN: Optional[str] = None
    SENTRY_ORG: str = "dishtv.technology"
    SENTRY_URL: str = "https://ds-testing-sentry"
    SENTRY_PROJECT: Optional[str] = None  # Set if needed for specific project
    INTERNAL_SEARCH_URL: str = "https://internal-search.yourdomain/api/search"
    # Internal search mode and timeout
    INTERNAL_SEARCH_MODE: str = "multi"
    INTERNAL_SEARCH_TIMEOUT: float = 10.0
    INTERNAL_SEARCH_SOURCES: str = "confluence,gitlab,jira"

    # Confluence integration settings
    CONFLUENCE_BASE_URL: str = "https://dishtech-dishtv.atlassian.net/wiki"
    CONFLUENCE_USER_EMAIL: Optional[str] = None
    CONFLUENCE_API_TOKEN: Optional[str] = None

    # GitLab integration settings
    GITLAB_BASE_URL: str = "https://gitlab.com"
    GITLAB_TOKEN: Optional[str] = None
    GITLAB_SEARCH_SCOPES: str = "projects,blobs"

    # Jira integration settings
    JIRA_BASE_URL: str = "https://dishtech-dishtv.atlassian.net"
    JIRA_USER_EMAIL: Optional[str] = None
    JIRA_API_TOKEN: Optional[str] = None

    # Confluence integration settings
    # GitLab integration settings

    # Jira integration settings

    # Multi-source search settings



    # Optional overrides for specialized models
    AGENT_MODE_MODEL: Optional[str] = None
    AGENT_MODE_MAX_ITERS: int = 5
    SUMMARY_MODEL_ARN: Optional[str] = None
    REVIEW_MODEL_ARN: Optional[str] = None


    def model_post_init(self, __context) -> None:
        if self.OLLAMA_BASE_URL:
            if self.PLLM_PROVIDER == "ollama" and not self.PLLM_API_BASE:
                self.PLLM_API_BASE = self.OLLAMA_BASE_URL
            if self.ELLM_PROVIDER == "ollama" and not self.ELLM_API_BASE:
                self.ELLM_API_BASE = self.OLLAMA_BASE_URL
            if self.EMBED_PROVIDER == "ollama" and not self.EMBED_API_BASE:
                self.EMBED_API_BASE = self.OLLAMA_BASE_URL

    # Read from .env
    model_config = SettingsConfigDict(env_file=(".env", ".env.local"), extra="ignore")

    # Enable / disable MCP tool sets (handy for local dev)
    ENABLE_BETAREPORT_MCP: bool = True
    ENABLE_VIEWERSHIP_MCP: bool = True
    ENABLE_LOG_ASSIST_MCP: bool = True
    ENABLE_INTERNAL_TOOLS_MCP: bool = False  # Placeholder endpoint; enable only when configured

    # CORS / frontend origins
    CORS_ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://10.79.83.40:3000",
        "http://10.79.83.40:3001",
        "http://10.79.85.35:3000",
        "http://10.79.85.35:3001",
        "http://dsgpu3090-lambda-vector:3000",
        "http://dsgpu3090-lambda-vector:3001",
        "https://chat-agent.dishtv.technology",
        "http://chat-agent.dishtv.technology"]
