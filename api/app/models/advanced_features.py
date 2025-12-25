"""
Advanced AI Features Models
- Memory management
- Persona bonding
- Translation
- Sentiment analysis
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Literal
from datetime import datetime

# ===== Memory Models =====

class MemoryCreate(BaseModel):
    summary: str
    full_text: Optional[str] = None
    memory_type: Literal['note', 'reminder', 'birthday', 'event', 'preference'] = 'note'
    emotion_detected: Optional[str] = None
    
    class Config:
        from_attributes = True

class MemoryResponse(BaseModel):
    id: str
    user_id: str
    summary: str
    full_text: Optional[str] = None
    emotion_detected: Optional[str] = None
    emotion_confidence: float
    memory_type: str
    recalled_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MemoryRecall(BaseModel):
    """Response when the AI recalls a memory"""
    memory_id: str
    recalled_memory: str
    relevance_score: float
    suggested_action: Optional[str] = None

# ===== Persona / Bonding Models =====

class PersonaSyncUpdate(BaseModel):
    relationship_level: Optional[int] = Field(None, ge=1, le=10)
    preferred_tone: Optional[Literal['professional', 'friendly', 'humorous', 'supportive', 'energetic']] = None
    user_preferences: Optional[Dict] = None

class PersonaSyncResponse(BaseModel):
    id: str
    user_id: str
    relationship_level: int
    preferred_tone: str
    interaction_count: int
    total_conversation_minutes: int
    avatar_personality_traits: Optional[Dict] = None
    user_preferences: Optional[Dict] = None
    last_interaction: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class BondingStatus(BaseModel):
    """Current bonding status with the Avatar"""
    relationship_level: int  # 1-10
    level_name: str  # "Stranger", "Acquaintance", "Friend", etc.
    next_milestone: Optional[str] = None
    interactions_to_next_level: int

# ===== Translation Models =====

class TranslationRequest(BaseModel):
    text: str
    source_language: str = "en"
    target_language: str
    maintain_tone: bool = True  # Preserve emotional tone

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence_score: float
    cache_hit: bool  # Was this from cache?

class SpeechToSpeechRequest(BaseModel):
    """Real-time voice translation"""
    audio_url: str
    source_language: str = "en"
    target_language: str
    preserve_voice_characteristics: bool = True
    latency_requirement_ms: int = 500

class SpeechToSpeechResponse(BaseModel):
    original_audio_url: str
    translated_audio_url: str
    source_language: str
    target_language: str
    processing_time_ms: float
    latency_met: bool  # Did it meet the requirement?

# ===== Sentiment & Emotion Analysis =====

class SentimentAnalysisRequest(BaseModel):
    text: str
    audio_url: Optional[str] = None  # For voice tone analysis

class EmotionDetection(BaseModel):
    emotion: str  # happy, sad, angry, surprised, calm, anxious, etc.
    confidence: float
    voice_tone: Optional[str] = None
    suggested_avatar_expression: Optional[Dict] = None

class SentimentResponse(BaseModel):
    sentiment: Literal['positive', 'negative', 'neutral']
    sentiment_score: float  # -1 to 1
    emotions_detected: List[EmotionDetection]
    overall_mood: str

# ===== Conversation History Models =====

class ConversationMessage(BaseModel):
    user_message: str
    avatar_response: str
    mode: Literal['studio', 'companion', 'assistant']
    language_detected: Optional[str] = None
    sentiment_score: Optional[float] = None

class ConversationHistoryResponse(BaseModel):
    id: str
    user_id: str
    user_message: str
    avatar_response: str
    mode: str
    language_detected: Optional[str]
    sentiment_score: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ===== Mode-Specific Models =====

class StudioModeState(BaseModel):
    """Studio Mode (Actor): Video creation"""
    current_project_id: Optional[str] = None
    selected_actor_id: str
    script: str
    effects_applied: List[str] = []
    export_settings: Dict = {}

class CompanionModeState(BaseModel):
    """Companion Mode (Friend/Diary): Emotional bonding"""
    bonding_status: BondingStatus
    recent_memories: List[MemoryResponse] = []
    emotion_context: Optional[EmotionDetection] = None
    personality_traits: Dict = {}
    conversation_style: str  # How the avatar should interact

class AssistantModeState(BaseModel):
    """Assistant Mode (Pro): Task management"""
    pending_tasks: List[str] = []
    calendar_access: bool = False
    weather_enabled: bool = False
    reminders_set: List[Dict] = []
    supported_languages: List[str] = []

# ===== Mode Switcher Models =====

class ModeSwitchRequest(BaseModel):
    new_mode: Literal['studio', 'companion', 'assistant']
    context: Optional[Dict] = None

class ModeState(BaseModel):
    """Combined state for all modes"""
    current_mode: Literal['studio', 'companion', 'assistant']
    studio_state: Optional[StudioModeState] = None
    companion_state: Optional[CompanionModeState] = None
    assistant_state: Optional[AssistantModeState] = None
    last_mode_switch: datetime

# ===== Integrated Response Models =====

class AvatarResponse(BaseModel):
    """Avatar's comprehensive response across all modes"""
    text_response: str
    audio_response_url: Optional[str] = None
    suggested_emotion: Optional[EmotionDetection] = None
    remembered_context: Optional[MemoryRecall] = None
    mode: Literal['studio', 'companion', 'assistant']
    bonding_update: Optional[int] = None  # Relationship level change
    timestamp: datetime

class AIPersonalityConfig(BaseModel):
    """Configure the AI Avatar's personality"""
    name: str
    base_personality: str
    voice_characteristics: Dict
    preferred_languages: List[str]
    emotional_responsiveness: float = 0.7  # 0-1
    memory_retention_days: int = 365
    adaptive_learning: bool = True
