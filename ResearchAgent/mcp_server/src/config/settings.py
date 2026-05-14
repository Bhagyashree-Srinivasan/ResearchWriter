"""Server configuration settings."""

import logging
from typing import Any, Dict

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """Application settings for Research MCP server"""
    
    model_config: SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    
    #server settings
    server_name: str = Field("Research MCP Server", description="The name of the server.")
    version: str = Field("1.0.0", description="The version of the server.")
    log_level: int = Field(default=logging.INFO, alias = "LOG_LEVEL", description="Logging level for the server.")
    log_level_dependencies: int = Field(default=logging.WARNING, alias = "LOG_LEVEL_DEPENDENCIES", description="Logging level for dependencies.")
    
    #LLM configuration
    youtube_transcription_model: str = Field(default="gemini-2.5-flash", description="The model used for YouTube transcription.")
    scraping_model: str = Field(default="gemini-2.5-flash", description="The model used for web scraping.")
    query_generation_model: str = Field(default="gemini-2.5-pro", description="The model used for query generation.")
    source_selection_model: str = Field(default="gemini-2.5-flash", description="The model used for source selection.")
    
    #API keys and secrets
    google_api_key: SecretStr | None = Field(default=None, alias="GOOGLE_API_KEY", description="Google API key for accessing Google services.")
    openai_api_key: SecretStr | None = Field(default=None, alias="OPENAI_API_KEY", description="OpenAI API key for accessing OpenAI services.")
    perplexity_api_key: SecretStr | None = Field(default=None, alias="PPLX_API_KEY", description="Perplexity API key for accessing Perplexity services.")
    firecrawl_api_key: SecretStr | None = Field(default=None, alias="FIRECRAWL_API_KEY", description="Firecrawl API key for accessing Firecrawl services.")
    github_token: SecretStr | None = Field(default=None, alias="GITHUB_TOKEN", description="GitHub token.")
    #Opik Monitoring Configuration
    opik_api_key: SecretStr | None = Field(default=None, alias="OPIK_API_KEY", description=" API key for Opik Authentication.")
    opik_workspace: str | None = Field(default=None, alias="OPIK_WORKSPACE", description="Opik workspace name. If not set, the default workspace will be used.")
    opik_project_name: str | None = Field(default="ResearchAgent", alias="OPIK_PROJECT_NAME", description="Opik project name.")
    
    @property
    def llm_configs(self) -> Dict[str, Dict[str, Any]]:
        """Get the LLM configurations."""
        return {
            "gemini-2.5-pro":{
                "identifier": "google_genai:gemini-2.5-pro",
                "api_key_env_var": "GOOGLE_API_KEY",
                "params":
                    {
                        "temperature": 0.7,
                        "thinking_budget": 1000,
                        "include_thoughts": False,
                        "max_retries": 3,
                    },
            },
            "gemini-2.5-flash":{
                "identifier": "google_genai:gemini-2.5-flash",
                "api_key_env_var": "GOOGLE_API_KEY",
                "params":
                    {
                        "temperature": 1,
                        "thinking_budget": 1000,
                        "include_thoughts": False,
                        "max_retries": 3,
                    },
            },
            "gpt-5":{
                "identifier": "openai:gpt-5",
                "api_key_env_var": "OPENAI_API_KEY",
                "params":
                    {
                        "temperature": 1,
                    },
            },
            "gpt-5-mini":{
                "identifier": "openai:gpt-5-mini",
                "api_key_env_var": "OPENAI_API_KEY",
                "params":
                    {
                        "temperature": 1,
                    },
            },
            "perplexity":{
                "identifier": "perplexity:sonar-pro",
                "api_key_env_var": "PPLX_API_KEY",
                "params":
                    {
                        "temperature": 0.7,
                        "max_retries": 3,
                    },
            },
        }
        

#Global settings instance
settings = Settings()