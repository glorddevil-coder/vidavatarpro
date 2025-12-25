from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.advanced_features import (
    MemoryCreate, MemoryResponse, MemoryRecall,
    PersonaSyncResponse, PersonaSyncUpdate, BondingStatus,
    TranslationRequest, TranslationResponse,
    SpeechToSpeechRequest, SpeechToSpeechResponse,
    SentimentAnalysisRequest, SentimentResponse, EmotionDetection,
    ModeSwitchRequest, ModeState,
    AvatarResponse
)
from app.services.memory_engine import memory_engine
from app.services.translator import translator
from datetime import datetime

router = APIRouter(prefix="/api/advanced", tags=["advanced-features"])

# ===== Memory Routes =====

@router.post("/memory/store")
async def store_memory(user_id: str, memory: MemoryCreate):
    """
    Store a memory in the AI's long-term memory
    The AI will recall this memory contextually in future conversations
    """
    try:
        stored_memory = await memory_engine.store_memory(
            user_id=user_id,
            text=memory.full_text or memory.summary,
            memory_type=memory.memory_type,
            emotion=memory.emotion_detected
        )
        return {
            "success": True,
            "memory_id": stored_memory.id,
            "summary": stored_memory.summary,
            "emotion": stored_memory.emotion_detected
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory/recall")
async def recall_memory(
    user_id: str,
    query: str,
    top_k: int = Query(5, ge=1, le=20)
):
    """
    Recall relevant memories based on a query
    Uses semantic similarity to find contextually relevant memories
    """
    try:
        memories = await memory_engine.recall_memory(user_id, query, top_k=top_k)
        return {
            "query": query,
            "memories": [
                {
                    "memory_id": mem.id,
                    "summary": mem.summary,
                    "relevance_score": float(score),
                    "emotion": mem.emotion_detected,
                    "created_at": mem.created_at.isoformat()
                }
                for mem, score in memories
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory/proactive-recall")
async def proactive_recall(user_id: str):
    """
    Get memories that should be proactively recalled
    E.g., birthdays, important events coming up
    """
    try:
        memories = await memory_engine.proactive_recall(user_id)
        return {
            "proactive_memories": [
                {
                    "id": mem.id,
                    "summary": mem.summary,
                    "type": mem.memory_type,
                    "suggested_action": f"Remind about {mem.summary}"
                }
                for mem in memories
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/memory/consolidate")
async def consolidate_memories(user_id: str):
    """
    Consolidate and merge related memories
    Improves storage efficiency and recall accuracy
    """
    try:
        count = await memory_engine.consolidate_memories(user_id)
        return {
            "success": True,
            "memories_consolidated": count,
            "message": f"Successfully consolidated {count} memory groups"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== Translation Routes =====

@router.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """
    Translate text from one language to another
    Supports 100+ languages with sentiment preservation
    """
    try:
        translated, confidence, cache_hit = await translator.translate(
            text=request.text,
            source_language=request.source_language,
            target_language=request.target_language,
            preserve_sentiment=request.maintain_tone
        )
        
        return TranslationResponse(
            original_text=request.text,
            translated_text=translated,
            source_language=request.source_language,
            target_language=request.target_language,
            confidence_score=confidence,
            cache_hit=cache_hit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/speech-to-speech", response_model=SpeechToSpeechResponse)
async def speech_to_speech_translate(request: SpeechToSpeechRequest):
    """
    Real-time Speech-to-Speech translation
    Pipeline: Speech Recognition → Translation → Voice Synthesis
    Target latency: < 500ms for natural conversation
    """
    try:
        result = await translator.speech_to_speech(
            audio_url=request.audio_url,
            source_language=request.source_language,
            target_language=request.target_language,
            preserve_voice_characteristics=request.preserve_voice_characteristics,
            timeout_ms=request.latency_requirement_ms
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Translation failed"))
        
        return SpeechToSpeechResponse(
            original_audio_url=request.audio_url,
            translated_audio_url=result["translated_audio_url"],
            source_language=request.source_language,
            target_language=request.target_language,
            processing_time_ms=0,  # Would measure actual time
            latency_met=result["latency_met"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/languages")
async def get_supported_languages():
    """Get all supported languages for translation"""
    try:
        languages = await translator.get_supported_languages()
        return {
            "supported_languages": languages,
            "total_count": len(languages)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== Sentiment & Emotion Analysis =====

@router.post("/analyze-sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentAnalysisRequest):
    """
    Analyze sentiment and emotions from text or voice
    Used to make Avatar's emotional responses appropriate
    """
    try:
        # Placeholder implementation
        # In production: Use sentiment API + voice analysis
        
        emotions = [
            EmotionDetection(
                emotion="calm",
                confidence=0.85,
                voice_tone="neutral",
                suggested_avatar_expression={
                    "eyes": "relaxed",
                    "mouth": "neutral",
                    "eyebrows": "neutral"
                }
            )
        ]
        
        return SentimentResponse(
            sentiment="neutral",
            sentiment_score=0.0,
            emotions_detected=emotions,
            overall_mood="calm"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== Persona / Bonding Routes =====

@router.get("/bonding-status")
async def get_bonding_status(user_id: str) -> BondingStatus:
    """
    Get current friendship/bonding level with Avatar
    Level 1: Stranger → Level 10: Best Friend
    """
    try:
        # Placeholder - would fetch from database
        relationship_level = 3  # Example
        
        level_names = {
            1: "Stranger",
            2: "New Friend",
            3: "Acquaintance",
            4: "Friend",
            5: "Close Friend",
            6: "Very Close Friend",
            7: "Best Friend",
            8: "Inseparable",
            9: "Soul Twin",
            10: "Perfect Match"
        }
        
        return BondingStatus(
            relationship_level=relationship_level,
            level_name=level_names[relationship_level],
            next_milestone="Reach 50 more interactions",
            interactions_to_next_level=50
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/bonding-status")
async def update_bonding_preferences(user_id: str, update: PersonaSyncUpdate):
    """
    Update bonding preferences and Avatar personality
    """
    try:
        return {
            "success": True,
            "updated_fields": update.dict(exclude_unset=True),
            "new_relationship_level": update.relationship_level or 3
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== Mode Switching Routes =====

@router.post("/mode/switch")
async def switch_mode(user_id: str, request: ModeSwitchRequest):
    """
    Switch between three modes:
    - studio: Video creation (Actor)
    - companion: Emotional bonding (Friend/Diary)
    - assistant: Task management (Pro Assistant)
    """
    try:
        mode = request.new_mode
        
        mode_descriptions = {
            'studio': 'Studio Mode: Create videos with AI actors',
            'companion': 'Companion Mode: Bond with your AI friend',
            'assistant': 'Assistant Mode: Task management & translation'
        }
        
        return {
            "success": True,
            "current_mode": mode,
            "mode_description": mode_descriptions[mode],
            "context": request.context or {},
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mode/current")
async def get_current_mode(user_id: str):
    """Get current active mode and state"""
    try:
        return {
            "current_mode": "companion",  # Placeholder
            "mode_features": {
                "companion": {
                    "memory_access": True,
                    "emotional_responses": True,
                    "bonding_enabled": True
                },
                "studio": {
                    "video_creation": True,
                    "effects_library": True
                },
                "assistant": {
                    "translation": True,
                    "reminders": True,
                    "calendar_access": False
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== Integrated Avatar Response =====

@router.post("/avatar-response")
async def get_avatar_response(user_id: str, user_message: str):
    """
    Get Avatar's response considering:
    - Memories (past interactions)
    - Bonding level
    - Emotional context
    - Current mode
    """
    try:
        # Recall relevant memories
        memories = await memory_engine.recall_memory(user_id, user_message, top_k=3)
        
        # Analyze sentiment
        emotion = "neutral"
        
        # Generate emotional response
        emotional_response = await memory_engine.emotional_response_synthesis(
            user_id, emotion
        )
        
        return AvatarResponse(
            text_response=f"Avatar response to: {user_message}",
            audio_response_url="https://s3.amazonaws.com/avatar_response.wav",
            suggested_emotion=EmotionDetection(
                emotion=emotional_response["tone"],
                confidence=0.85
            ),
            remembered_context=None,  # Would include if relevant memory
            mode="companion",
            bonding_update=None,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== System Status & Info =====

@router.get("/features")
async def get_available_features():
    """Get all advanced features available"""
    return {
        "features": {
            "long_term_memory": {
                "enabled": True,
                "storage_size_mb": 500,
                "max_memories": 10000
            },
            "translator": {
                "enabled": True,
                "supported_languages": 100,
                "latency_target_ms": 500
            },
            "emotional_intelligence": {
                "enabled": True,
                "emotions_recognized": 8,
                "voice_analysis": True
            },
            "bonding_system": {
                "enabled": True,
                "max_relationship_level": 10
            },
            "modes": ["studio", "companion", "assistant"]
        }
    }
