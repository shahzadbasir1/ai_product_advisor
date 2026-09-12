from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from enum import Enum

class AgentStatus(Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    SKIPPED = 'SKIPPED'
    PROCESSING = 'PROCESSING'

class ProductAIMetadata(BaseModel):

    #Added 07/07/26
    description_source: Optional[str] = None

    description_generated_at: Optional[datetime] = None

    description_version: Optional[int] = None

    review_score: Optional[int] = None

    last_review_at: Optional[datetime] = None

    seo_source: str

    seo_generated_at: datetime

    last_agent_run: Optional[datetime] = None

    missing_image_flag: bool

    last_product_hash: Optional[str] = None

    description_model: Optional[str] = None

    review_model: Optional[str] = None

    seo_model: Optional[str] = None

    agent_status: str

    last_error: Optional[str] = None

    retry_count: int = 0

    description_approved: bool = False

    agent_status = AgentStatus.PENDING

    last_change_type: Optional[str] = None

