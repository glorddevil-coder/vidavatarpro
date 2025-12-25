"""
Neural Persona Service - Bonding & Assistance  
Handles memory with vector database, affective computing via biometrics,
and BCI readiness for future neural integration

v3.0+
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


@dataclass
class MemoryEntry:
    """Long-term memory entry with vector embedding"""
    memory_id: str
    user_id: str
    content: str
    embedding: List[float]  # 1536-dim OpenAI embedding
    timestamp: datetime
    memory_type: str  # "preference", "conversation", "emotional_state", "health"
    importance_score: float = 0.5
    access_count: int = 0
    metadata: Dict = field(default_factory=dict)


@dataclass
class UserBiometrics:
    """User biometric data for affective computing"""
    timestamp: datetime
    heart_rate: float  # BPM
    heart_rate_variability: float  # ms
    skin_color_r: float  # For heart rate detection via camera
    skin_color_g: float
    skin_color_b: float
    pupil_dilation: float  # 0-1 scale
    blink_rate: float  # Blinks per minute
    eye_gaze_direction: Tuple[float, float] = (0, 0)  # x, y angles
    skin_temperature: float = 37.0  # Celsius
    stress_level: float = 0.0  # 0-1 inferred from HR
    

@dataclass
class BCICommand:
    """Brain-Computer Interface command (thought-to-scene)"""
    command_id: str
    timestamp: datetime
    thought_type: str  # "visual_scene", "action", "query", "emotion"
    intention_strength: float  # 0-1
    decoded_meaning: str
    confidence: float


class LongTermMemoryEngine:
    """
    Vector Database for long-term memory storage and retrieval
    Remembers user preferences, conversations, and emotional states
    """
    
    def __init__(self, embedding_dim: int = 1536):
        self.embedding_dim = embedding_dim  # OpenAI embedding size
        self.memories: List[MemoryEntry] = []
        self.user_profiles: Dict[str, Dict] = {}
        logger.info(f"Long-Term Memory Engine initialized ({embedding_dim}-dim vectors)")
    
    def store_memory(
        self,
        user_id: str,
        content: str,
        embedding: List[float],
        memory_type: str = "conversation",
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Store a memory entry with vector embedding
        
        Args:
            user_id: User ID
            content: Memory content/text
            embedding: Vector embedding (1536-dim from OpenAI)
            memory_type: Type of memory
            metadata: Additional metadata
        
        Returns:
            Memory ID
        """
        memory_id = f"mem_{user_id}_{len(self.memories)}"
        
        memory = MemoryEntry(
            memory_id=memory_id,
            user_id=user_id,
            content=content,
            embedding=embedding,
            timestamp=datetime.now(),
            memory_type=memory_type,
            metadata=metadata or {}
        )
        
        self.memories.append(memory)
        
        # Update user profile
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "preferences": [],
                "emotional_arc": [],
                "health_notes": [],
                "interaction_history": []
            }
        
        if memory_type == "preference":
            self.user_profiles[user_id]["preferences"].append(content)
        elif memory_type == "emotional_state":
            self.user_profiles[user_id]["emotional_arc"].append(content)
        elif memory_type == "health":
            self.user_profiles[user_id]["health_notes"].append(content)
        elif memory_type == "conversation":
            self.user_profiles[user_id]["interaction_history"].append(content)
        
        logger.debug(f"Stored memory {memory_id} ({memory_type}) for user {user_id}")
        return memory_id
    
    def retrieve_memories(
        self,
        user_id: str,
        query_embedding: List[float],
        top_k: int = 5,
        memory_type: Optional[str] = None
    ) -> List[Tuple[MemoryEntry, float]]:
        """
        Retrieve similar memories using vector similarity
        
        Args:
            user_id: User ID
            query_embedding: Query vector (1536-dim)
            top_k: Number of results
            memory_type: Filter by type (optional)
        
        Returns:
            List of (memory, similarity_score) tuples
        """
        user_memories = [m for m in self.memories if m.user_id == user_id]
        
        if memory_type:
            user_memories = [m for m in user_memories if m.memory_type == memory_type]
        
        if not user_memories:
            return []
        
        # Calculate cosine similarity
        query_vec = np.array(query_embedding)
        similarities = []
        
        for memory in user_memories:
            mem_vec = np.array(memory.embedding)
            
            # Cosine similarity
            dot_product = np.dot(query_vec, mem_vec)
            magnitude = np.linalg.norm(query_vec) * np.linalg.norm(mem_vec)
            similarity = dot_product / (magnitude + 1e-8)
            
            # Boost score by importance and access frequency
            boosted_score = similarity * (1 + memory.importance_score * 0.5) * (1 + memory.access_count * 0.1)
            
            similarities.append((memory, boosted_score))
            
            # Increment access count
            memory.access_count += 1
        
        # Sort and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        logger.debug(f"Retrieved {len(similarities[:top_k])} memories for user {user_id}")
        return similarities[:top_k]
    
    def get_user_profile(self, user_id: str) -> Dict:
        """Get comprehensive user profile from memories"""
        return self.user_profiles.get(user_id, {
            "preferences": [],
            "emotional_arc": [],
            "health_notes": [],
            "interaction_history": []
        })


class AffectiveComputingEngine:
    """
    Monitors user biometrics to infer emotional state and stress levels
    Provides proactive health/emotional support based on detected conditions
    """
    
    def __init__(self):
        self.baseline_heart_rate = 70  # BPM
        self.baseline_hrv = 50  # ms
        self.stress_threshold = 0.6
        self.alert_threshold = 0.8
        logger.info("Affective Computing Engine initialized (biometric monitoring)")
    
    def infer_heart_rate_from_camera(
        self,
        skin_color: Tuple[float, float, float],
        previous_colors: List[Tuple[float, float, float]]
    ) -> float:
        """
        Infer heart rate from skin color changes (PPG - Photoplethysmography)
        Red channel shows blood volume changes
        """
        if len(previous_colors) < 2:
            return self.baseline_heart_rate
        
        # Get red channel changes (blood flow indicator)
        red_values = [c[0] for c in previous_colors[-30:]]  # Last 30 frames
        
        if len(red_values) < 2:
            return self.baseline_heart_rate
        
        # Calculate variance in red channel
        red_variance = np.var(red_values)
        
        # Convert variance to BPM estimate (simplified)
        # Higher variance = higher heart rate
        estimated_bpm = 60 + (red_variance * 100)  # Range 60-160 BPM
        estimated_bpm = min(200, max(40, estimated_bpm))
        
        logger.debug(f"Inferred heart rate from camera: {estimated_bpm:.0f} BPM")
        return estimated_bpm
    
    def detect_pupil_dilation(
        self,
        previous_pupil_sizes: List[float]
    ) -> float:
        """
        Detect pupil dilation as stress indicator
        Dilated pupils (>1.0) indicate stress, fear, or concentration
        """
        if not previous_pupil_sizes:
            return 0.5
        
        # Calculate dilation trend
        avg_size = np.mean(previous_pupil_sizes[-5:])
        baseline = 0.5
        
        dilation = (avg_size - baseline) / baseline
        dilation = max(-1, min(1, dilation))  # Clamp to [-1, 1]
        
        return dilation
    
    def analyze_biometrics(
        self,
        biometrics: UserBiometrics
    ) -> Dict:
        """
        Analyze biometrics to infer emotional state and health status
        """
        # Stress calculation based on heart rate deviation
        hr_deviation = (biometrics.heart_rate - self.baseline_heart_rate) / self.baseline_heart_rate
        hrv_stress = max(0, (self.baseline_hrv - biometrics.heart_rate_variability) / self.baseline_hrv)
        
        # Pupil dilation indicates stress/attention
        pupil_stress = max(0, biometrics.pupil_dilation * 0.5)
        
        # Combined stress score
        stress_level = (hr_deviation * 0.4 + hrv_stress * 0.4 + pupil_stress * 0.2)
        stress_level = max(0, min(1, stress_level))
        
        # Emotional state mapping
        emotion_map = {
            0.0: "relaxed",
            0.3: "calm",
            0.5: "neutral",
            0.7: "stressed",
            1.0: "panic"
        }
        
        # Find closest emotion
        emotion = "neutral"
        for threshold, emotion_name in sorted(emotion_map.items()):
            if stress_level >= threshold:
                emotion = emotion_name
        
        # Health concerns
        health_alerts = []
        
        if biometrics.heart_rate > 120:
            health_alerts.append("elevated_heart_rate")
        if biometrics.heart_rate < 50:
            health_alerts.append("low_heart_rate")
        if biometrics.heart_rate_variability < 20:
            health_alerts.append("low_hrv_stress_indicator")
        if biometrics.blink_rate < 10:
            health_alerts.append("reduced_blinking_dry_eyes")
        if biometrics.blink_rate > 30:
            health_alerts.append("excessive_blinking_nervousness")
        
        return {
            "stress_level": stress_level,
            "emotion": emotion,
            "heart_rate": biometrics.heart_rate,
            "heart_rate_variability": biometrics.heart_rate_variability,
            "pupil_dilation": biometrics.pupil_dilation,
            "blink_rate": biometrics.blink_rate,
            "health_alerts": health_alerts,
            "proactive_suggestions": self._generate_suggestions(emotion, health_alerts)
        }
    
    def _generate_suggestions(self, emotion: str, alerts: List[str]) -> List[str]:
        """Generate proactive health/wellness suggestions"""
        suggestions = []
        
        if emotion == "stressed" or emotion == "panic":
            suggestions.extend([
                "Take a deep breath - breathing exercise available",
                "Would you like a 5-minute meditation session?",
                "Let's do some stretching exercises"
            ])
        
        if "elevated_heart_rate" in alerts:
            suggestions.append("Your heart rate is elevated. Take it easy and relax.")
        
        if "low_hrv_stress_indicator" in alerts:
            suggestions.append("Low heart rate variability detected. Get more rest.")
        
        if emotion == "relaxed" and not alerts:
            suggestions.append("You're in great shape! Keep up the healthy habits.")
        
        return suggestions


class BCIIntegrationEngine:
    """
    Brain-Computer Interface readiness
    Logic mapping for future Neuralink/Kernel integration
    Allows "Thought-to-Scene" generation and direct neural control
    """
    
    def __init__(self):
        self.bci_commands: List[BCICommand] = []
        self.thought_vocabulary = {
            "visual": ["imagine_scene", "visualize_object", "recall_memory"],
            "action": ["move_hand", "speak", "interact_object"],
            "query": ["ask_question", "search_memory", "analyze_data"],
            "emotion": ["express_feeling", "modulate_tone", "show_reaction"],
        }
        self.neural_patterns: Dict[str, List[float]] = {}
        logger.info("BCI Integration Engine initialized (ready for neural devices)")
    
    def decode_neural_signal(
        self,
        neural_data: np.ndarray,
        sample_rate: float = 1000.0
    ) -> Optional[BCICommand]:
        """
        Decode neural signals from BCI device
        
        Args:
            neural_data: Neural signal data (time_samples, channels)
            sample_rate: Sampling rate in Hz
        
        Returns:
            Decoded BCI command or None
        """
        if neural_data.shape[0] < 100:
            return None
        
        # Simulate signal processing
        # In real implementation, would use ML models trained on calibration data
        
        # Extract features (power spectrum, etc.)
        fft = np.abs(np.fft.fft(neural_data, axis=0))
        
        # Simple threshold-based classification
        dominant_freq = np.argmax(np.mean(fft, axis=1))
        power_level = np.mean(fft)
        
        # Map to command type
        if dominant_freq < 10:
            thought_type = "visual"
        elif dominant_freq < 20:
            thought_type = "action"
        elif dominant_freq < 30:
            thought_type = "query"
        else:
            thought_type = "emotion"
        
        # Confidence based on signal strength
        confidence = min(1.0, power_level / 10.0)
        
        if confidence < 0.3:
            return None
        
        command = BCICommand(
            command_id=f"bci_{len(self.bci_commands)}",
            timestamp=datetime.now(),
            thought_type=thought_type,
            intention_strength=power_level,
            decoded_meaning=f"{thought_type}_command",
            confidence=confidence
        )
        
        self.bci_commands.append(command)
        logger.info(f"Decoded BCI command: {thought_type} (confidence: {confidence:.2f})")
        
        return command
    
    def thought_to_scene(
        self,
        thought_content: str,
        bci_confidence: float
    ) -> Dict:
        """
        Generate scene/action from decoded thought
        
        Args:
            thought_content: Decoded thought content
            bci_confidence: Neural decode confidence (0-1)
        
        Returns:
            Scene/action parameters
        """
        return {
            "thought_input": thought_content,
            "confidence": bci_confidence,
            "execution_mode": "high_precision" if bci_confidence > 0.7 else "low_confidence",
            "scene_parameters": self._generate_scene_params(thought_content),
            "feedback": "Neural command received and executing"
        }
    
    def _generate_scene_params(self, thought: str) -> Dict:
        """Generate scene parameters from thought"""
        return {
            "setting": "determined_by_neural_signal",
            "objects": [],
            "lighting": "adaptive",
            "avatar_pose": "thought_derived"
        }


class NeuralPersonaService:
    """Main service combining memory, affective computing, and BCI"""
    
    def __init__(self):
        self.memory_engine = LongTermMemoryEngine()
        self.affective_engine = AffectiveComputingEngine()
        self.bci_engine = BCIIntegrationEngine()
        logger.info("Neural Persona Service initialized (Memory + Affect + BCI)")
    
    async def store_user_memory(
        self,
        user_id: str,
        content: str,
        embedding: List[float],
        memory_type: str = "conversation"
    ) -> Dict:
        """Store memory with embedding"""
        memory_id = self.memory_engine.store_memory(
            user_id, content, embedding, memory_type
        )
        return {
            "memory_id": memory_id,
            "stored_at": datetime.now().isoformat(),
            "memory_type": memory_type
        }
    
    async def get_proactive_recall(
        self,
        user_id: str,
        query_embedding: List[float],
        context: str = "general"
    ) -> Dict:
        """Get important memories to proactively share with user"""
        memories = self.memory_engine.retrieve_memories(
            user_id, query_embedding, top_k=3
        )
        
        return {
            "user_id": user_id,
            "context": context,
            "recalled_memories": [
                {
                    "content": m.content,
                    "type": m.memory_type,
                    "relevance": score
                }
                for m, score in memories
            ]
        }
    
    async def analyze_user_health(
        self,
        user_id: str,
        biometrics: Dict
    ) -> Dict:
        """Analyze biometrics and provide health insights"""
        bm = UserBiometrics(
            timestamp=datetime.now(),
            heart_rate=biometrics.get("heart_rate", 70),
            heart_rate_variability=biometrics.get("hrv", 50),
            skin_color_r=biometrics.get("skin_r", 0.5),
            skin_color_g=biometrics.get("skin_g", 0.5),
            skin_color_b=biometrics.get("skin_b", 0.5),
            pupil_dilation=biometrics.get("pupil_dilation", 0.5),
            blink_rate=biometrics.get("blink_rate", 20),
            stress_level=0.0
        )
        
        analysis = self.affective_engine.analyze_biometrics(bm)
        
        return {
            "user_id": user_id,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
