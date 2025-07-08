from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Dict, Any
import datetime

class KnowledgeBaseArticle(BaseModel):
    """
    Pydantic model for a knowledge base article to be stored in the vector database.
    """
    id: str = Field(..., description="Unique identifier for the knowledge base article.")
    source: str = Field(..., description="Source of the article, e.g., 'Confluence', 'Google Docs'.")
    url: Optional[HttpUrl] = Field(None, description="URL to the original article.")
    title: str = Field(..., description="Title of the article.")
    content: str = Field(..., description="Content of the article, which will be vectorized.")
    service: Optional[str] = Field(None, description="The service this article is related to.")
    tags: List[str] = Field(default_factory=list, description="Tags for filtering and categorization.")
    owner_team: Optional[str] = Field(None, description="The team that owns this article.")
    last_updated: Optional[datetime.datetime] = Field(None, description="When the article was last updated.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Any other metadata.")
