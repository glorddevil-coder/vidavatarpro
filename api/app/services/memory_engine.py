"""
Memory Engine - Neural Long-Term Memory (LTM)
Integrates with Pinecone/Weaviate for vector similarity search
Enables the Avatar to "remember" and bond with users
"""

from typing import Dict, List, Optional, Tuple
import asyncio
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class Memory:
    id: str
    user_id: str
    summary: str
    full_text: str
    emotion_detected: str
    emotion_confidence: float
    memory_type: str
    created_at: datetime
    recalled_count: int = 0

class MemoryEngine:
    """
    Neural Long-Term Memory System
    
    Features:
    - Vector embedding for semantic search
    - Emotional context preservation
    - Proactive recall (birthdays, important dates)
    - Memory consolidation (merging related memories)
    """

    def __init__(self):
        self.memories: Dict[str, List[Memory]] = {}  # user_id -> [memories]
        self.embedding_dimension = 1536  # OpenAI embedding size
        self.max_memories_per_user = 10000
        self.importance_threshold = 0.5
        
        # Proactive recall triggers
        self.recall_triggers = {
            'birthday': 24,  # Remind 24 hours before
            'anniversary': 48,  # Remind 48 hours before
            'event': 168,  # Remind 7 days before
            'reminder': 24,
        }

    async def store_memory(
        self,
        user_id: str,
        text: str,
        memory_type: str = 'note',
        emotion: Optional[str] = None,
        emotion_confidence: float = 0.0,
    ) -> Memory:
        """
        Store a memory in the neural network
        
        Process:
        1. Extract key facts from text
        2. Generate vector embedding
        3. Detect emotion
        4. Store with metadata
        5. Check for consolidation opportunities
        """
        
        # Extract key information
        summary = await self._extract_summary(text)
        
        # Generate embedding for semantic search
        embedding = await self._generate_embedding(text)
        
        # Detect emotion if not provided
        if emotion is None:
            emotion, emotion_confidence = await self._detect_emotion(text)
        
        # Create memory object (would save to database)
        memory = Memory(
            id=f"mem_{user_id}_{datetime.now().timestamp()}",
            user_id=user_id,
            summary=summary,
            full_text=text,
            emotion_detected=emotion,
            emotion_confidence=emotion_confidence,
            memory_type=memory_type,
            created_at=datetime.now(),
        )
        
        # Store in memory
        if user_id not in self.memories:
            self.memories[user_id] = []
        self.memories[user_id].append(memory)
        
        # Check for consolidation with existing memories
        await self._consolidate_memories(user_id, memory)
        
        return memory

    async def recall_memory(
        self,
        user_id: str,
        query: str,
        top_k: int = 5,
        time_weight: float = 0.1,
    ) -> List[Tuple[Memory, float]]:
        """
        Retrieve memories using semantic similarity
        
        Uses vector embeddings to find contextually relevant memories
        
        Args:
            user_id: User ID
            query: Natural language query
            top_k: Number of memories to retrieve
            time_weight: How much to prioritize recent memories (0-1)
            
        Returns:
            List of (Memory, relevance_score) tuples
        """
        
        if user_id not in self.memories:
            return []
        
        # Generate embedding for query
        query_embedding = await self._generate_embedding(query)
        
        # Find similar memories using vector similarity
        memories = self.memories[user_id]
        scored_memories = []
        
        for memory in memories:
            # Vector similarity (cosine)
            similarity = await self._cosine_similarity(
                query_embedding,
                memory.id  # Would get from vector DB
            )
            
            # Time decay (older = lower score)
            days_old = (datetime.now() - memory.created_at).days
            time_score = 1.0 / (1.0 + (time_weight * days_old))
            
            # Combined score
            final_score = (similarity * 0.7) + (time_score * 0.3)
            
            scored_memories.append((memory, final_score))
        
        # Sort by relevance and return top K
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        return scored_memories[:top_k]

    async def proactive_recall(self, user_id: str) -> List[Memory]:
        """
        Proactively recall important memories
        
        Triggers:
        - Birthdays (24 hours before)
        - Anniversaries (48 hours before)
        - Important events (7 days before)
        
        Example: If user mentioned friend's birthday on Monday,
        Friday morning Avatar says: "Don't forget to call your friend!"
        """
        
        if user_id not in self.memories:
            return []
        
        important_memories = []
        now = datetime.now()
        
        for memory in self.memories[user_id]:
            if memory.memory_type in self.recall_triggers:
                # Check if should be recalled
                hours_until_trigger = self.recall_triggers[memory.memory_type]
                
                # Parse date from memory if available
                # (In production, would extract dates more intelligently)
                
                # For now, include high-importance recent memories
                if memory.emotion_confidence > 0.8:
                    important_memories.append(memory)
        
        return important_memories[:5]  # Top 5 most important

    async def consolidate_memories(self, user_id: str) -> int:
        """
        Consolidate related memories to reduce storage
        
        Example:
        - Memory 1: "User loves pizza"
        - Memory 2: "User had pizza yesterday"
        - Memory 3: "User's favorite pizza topping is pepperoni"
        
        Consolidate into: "User loves pizza, especially with pepperoni"
        """
        
        if user_id not in self.memories:
            return 0
        
        consolidated_count = 0
        memories = self.memories[user_id]
        
        # Find groups of similar memories
        i = 0
        while i < len(memories) - 1:
            current = memories[i]
            similar_memories = []
            
            for j in range(i + 1, len(memories)):
                similarity = await self._check_memory_similarity(current, memories[j])
                if similarity > 0.8:  # High similarity threshold
                    similar_memories.append(memories[j])
            
            # If found similar memories, consolidate
            if similar_memories:
                consolidated = await self._merge_memories(
                    [current] + similar_memories
                )
                # Replace in memory list (would update DB)
                consolidated_count += 1
            
            i += 1
        
        return consolidated_count

    async def emotional_response_synthesis(
        self,
        user_id: str,
        current_emotion: str,
    ) -> Dict:
        """
        Generate emotionally appropriate avatar response
        
        Uses:
        - User's emotional history
        - Relationship level
        - Previous interactions
        
        Returns:
            Dict with avatar expression, tone, and verbal response
        """
        
        if user_id not in self.memories:
            return {
                "avatar_expression": "neutral",
                "tone": "friendly",
                "suggested_response": "I'm here to listen.",
            }
        
        # Analyze user's emotional patterns
        memories = self.memories[user_id]
        emotion_history = {}
        
        for memory in memories:
            emotion = memory.emotion_detected
            if emotion not in emotion_history:
                emotion_history[emotion] = 0
            emotion_history[emotion] += 1
        
        # Generate response based on emotion
        return {
            "avatar_expression": self._get_avatar_expression(current_emotion),
            "tone": self._get_appropriate_tone(emotion_history, current_emotion),
            "suggested_response": await self._generate_empathetic_response(
                user_id, current_emotion
            ),
        }

    async def _extract_summary(self, text: str) -> str:
        """Extract key summary from full text"""
        # In production: Use abstractive summarization
        return text[:100] if len(text) > 100 else text

    async def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate vector embedding for text
        Uses: OpenAI Embeddings API or similar
        """
        # Placeholder - would call actual embedding API
        import hashlib
        hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
        return [float((hash_val >> (i % 128)) % 256) / 256.0 for i in range(self.embedding_dimension)]

    async def _detect_emotion(self, text: str) -> Tuple[str, float]:
        """Detect emotion from text"""
        emotions = ['happy', 'sad', 'angry', 'afraid', 'surprised', 'calm']
        # Placeholder
        return 'calm', 0.85

    async def _cosine_similarity(self, vec1: List[float], vec_id: str) -> float:
        """Calculate cosine similarity between vectors"""
        # Placeholder
        return 0.85

    async def _check_memory_similarity(self, mem1: Memory, mem2: Memory) -> float:
        """Check semantic similarity between two memories"""
        # Placeholder
        return 0.5

    async def _merge_memories(self, memories: List[Memory]) -> Memory:
        """Merge multiple similar memories into one"""
        merged_text = " ".join([m.full_text for m in memories])
        return await self.store_memory(
            memories[0].user_id,
            merged_text,
            memory_type=memories[0].memory_type
        )

    def _get_avatar_expression(self, emotion: str) -> Dict:
        """Map emotion to avatar facial expression"""
        expressions = {
            'happy': {'eyes': 'smiling', 'mouth': 'smile', 'eyebrows': 'raised'},
            'sad': {'eyes': 'tearful', 'mouth': 'frown', 'eyebrows': 'lowered'},
            'angry': {'eyes': 'narrow', 'mouth': 'tense', 'eyebrows': 'furrowed'},
            'afraid': {'eyes': 'wide', 'mouth': 'open', 'eyebrows': 'raised'},
            'calm': {'eyes': 'relaxed', 'mouth': 'neutral', 'eyebrows': 'neutral'},
        }
        return expressions.get(emotion, expressions['calm'])

    def _get_appropriate_tone(self, emotion_history: Dict, current_emotion: str) -> str:
        """Determine appropriate tone based on history and current emotion"""
        if current_emotion == 'sad':
            return 'supportive'
        elif current_emotion == 'happy':
            return 'enthusiastic'
        elif current_emotion == 'angry':
            return 'calm'
        return 'friendly'

    async def _generate_empathetic_response(self, user_id: str, emotion: str) -> str:
        """Generate contextually appropriate empathetic response"""
        responses = {
            'happy': "I'm happy to see you smiling!",
            'sad': "I'm here for you. Do you want to talk about it?",
            'angry': "Take a deep breath. How can I help?",
            'afraid': "It's okay. I'm right here with you.",
            'calm': "You seem peaceful. Enjoying the moment?",
        }
        return responses.get(emotion, "I'm listening.")

# Singleton instance
memory_engine = MemoryEngine()
