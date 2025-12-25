from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime

# User Models
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    subscription_tier: Literal['free', 'pro', 'enterprise'] = 'free'
    credits_remaining: int = 100
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Project Models
class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    script_text: str
    actor_id: str

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    script_text: Optional[str] = None
    actor_id: Optional[str] = None
    status: Optional[Literal['draft', 'processing', 'completed', 'failed']] = None

class ProjectResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    script_text: str
    actor_id: str
    status: Literal['draft', 'processing', 'completed', 'failed'] = 'draft'
    duration_seconds: Optional[int] = None
    created_at: datetime
    last_synced: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Avatar Models
class AvatarResponse(BaseModel):
    id: str
    name: str
    type: Literal['stock', 'custom']
    user_id: Optional[str] = None
    base_voice: str
    default_mood: str
    mesh_path: str
    blend_shapes: dict
    thumbnail_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Audio Effect Models
class AudioEffectCreate(BaseModel):
    name: str
    type: Literal['trickster', 'deepbass', 'custom'] = 'custom'
    pitch_multiplier: float = 1.0
    formant_shift: float = 1.0
    tempo_rate: float = 1.0
    description: Optional[str] = None

class AudioEffectResponse(BaseModel):
    id: str
    name: str
    type: Literal['trickster', 'deepbass', 'custom']
    pitch_multiplier: float
    formant_shift: float
    tempo_rate: float
    description: Optional[str] = None
    user_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Asset Models
class AssetResponse(BaseModel):
    id: str
    user_id: str
    type: Literal['image', 'voice', 'audio']
    name: str
    s3_url: str
    is_custom_avatar: bool
    metadata: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Export Job Models
class ExportJobCreate(BaseModel):
    project_id: str
    format: Literal['mp4', 'mov', 'fbx'] = 'mp4'
    resolution: Literal['1080p', '2k', '4k'] = '1080p'

class ExportJobResponse(BaseModel):
    id: str
    project_id: str
    user_id: str
    format: Literal['mp4', 'mov', 'fbx']
    resolution: Literal['1080p', '2k', '4k']
    status: Literal['queued', 'processing', 'completed', 'failed']
    output_url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Audio Processing Models
class TricksterEffectRequest(BaseModel):
    audio_url: str
    pitch_shift: float = 4.0
    formant_shift: float = 0.65
    tempo_rate: float = 1.1

class AudioProcessingResponse(BaseModel):
    success: bool
    processed_url: Optional[str] = None
    error: Optional[str] = None
    processing_time_ms: float
