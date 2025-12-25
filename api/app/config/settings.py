"""
Application Configuration Settings
AuraStudio Omni - v3.0+
"""

from pydantic_settings import BaseSettings
from typing import Optional, List
from enum import Enum


class Environment(str, Enum):
    """Environment types"""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class VectorDBType(str, Enum):
    """Vector database types"""
    PGVECTOR = "pgvector"
    PINECONE = "pinecone"
    WEAVIATE = "weaviate"


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    Supports .env files for different environments
    """
    
    # ==========================================
    # API Configuration
    # ==========================================
    app_name: str = "AuraStudio Omni"
    app_version: str = "3.0.0"
    api_env: str = "development"
    api_host: str = "localhost"
    api_port: int = 8000
    api_workers: int = 1
    api_debug: bool = False
    
    # ==========================================
    # Database Configuration
    # ==========================================
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_role_key: str = ""
    database_url: str = "postgresql://postgres:postgres@localhost:5432/auraudio_dev"
    database_pool_size: int = 5
    database_echo: bool = False
    
    # ==========================================
    # Vector Database Configuration
    # ==========================================
    vector_db_type: str = "pgvector"
    vector_db_mock: bool = False
    
    # Pinecone
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    pinecone_index_name: str = "auraudio-embeddings"
    
    # Weaviate
    weaviate_url: Optional[str] = None
    weaviate_api_key: Optional[str] = None
    
    # ==========================================
    # OpenAI & LLM Configuration
    # ==========================================
    openai_api_key: str = ""
    openai_model_embeddings: str = "text-embedding-3-small"
    openai_model_chat: str = "gpt-4-turbo"
    openai_embedding_dimension: int = 1536
    
    # ==========================================
    # Translation Services
    # ==========================================
    google_translate_api_key: Optional[str] = None
    deepl_api_key: Optional[str] = None
    deepl_api_type: str = "free"
    
    # ==========================================
    # Redis Configuration
    # ==========================================
    redis_url: str = "redis://localhost:6379/0"
    redis_cache_ttl: int = 86400
    redis_enabled: bool = False
    
    # ==========================================
    # Audio Processing
    # ==========================================
    librosa_cache_dir: str = "./cache/librosa"
    audio_sample_rate: int = 22050
    audio_max_duration: int = 600
    
    # ==========================================
    # Memory & Storage
    # ==========================================
    memory_vector_dimension: int = 1536
    memory_similarity_threshold: float = 0.75
    memory_consolidation_days: int = 30
    
    # ==========================================
    # Security & Blockchain
    # ==========================================
    web3_provider_url: str = "http://localhost:8545"
    ethereum_chain_id: int = 31337
    ethereum_contract_address: str = "0x0000000000000000000000000000000000000000"
    blockchain_enabled: bool = False
    
    # ==========================================
    # JWT & Authentication
    # ==========================================
    jwt_secret_key: str = "your_secret_key_change_in_production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # ==========================================
    # Logging & Monitoring
    # ==========================================
    log_level: str = "INFO"
    sentry_dsn: Optional[str] = None
    sentry_enabled: bool = False
    
    # ==========================================
    # CORS & Security
    # ==========================================
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    cors_allow_headers: List[str] = ["Content-Type", "Authorization"]
    
    # ==========================================
    # Feature Flags
    # ==========================================
    feature_memory_engine: bool = True
    feature_translator: bool = True
    feature_bonding_system: bool = True
    feature_health_monitor: bool = True
    feature_autonomous_agents: bool = True
    feature_voice_dna_nft: bool = True
    feature_ai_watermarking: bool = True
    
    # ==========================================
    # Development Tools
    # ==========================================
    pytest_enabled: bool = False
    mock_external_apis: bool = False
    database_reset_on_start: bool = False
    seed_sample_data: bool = False
    
    class Config:
        """Pydantic config"""
        env_file = ".env.development"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @property
    def is_development(self) -> bool:
        """Check if development environment"""
        return self.api_env == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if production environment"""
        return self.api_env == "production"
    
    @property
    def is_testing(self) -> bool:
        """Check if testing environment"""
        return self.api_env == "testing"


# Create global settings instance
settings = Settings()
