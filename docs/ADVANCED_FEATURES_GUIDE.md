# Advanced Features Implementation Guide

## Quick Start: Three Modes

### 1. Database Setup

Add vector support to Supabase (pgvector):

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- The user_memory table already has vector column
-- Verify it exists:
ALTER TABLE user_memory ADD COLUMN IF NOT EXISTS memory_vector vector(1536);

-- Create vector index for fast semantic search
CREATE INDEX ON user_memory USING ivfflat (memory_vector vector_cosine_ops) WITH (lists = 100);
```

### 2. Environment Setup

Add new API keys to `.env` and `.env.local`:

```env
# Vector Database (Pinecone)
PINECONE_API_KEY=your_api_key
PINECONE_ENVIRONMENT=your_environment
PINECONE_INDEX_NAME=aurastudio-memories

# OpenAI (Embeddings & Chat)
OPENAI_API_KEY=sk-...
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Translation APIs
GOOGLE_TRANSLATE_API_KEY=your_key
GOOGLE_CLOUD_SPEECH_API_KEY=your_key

# Voice & Audio
ELEVENLABS_API_KEY=your_key
RESPEECHER_API_KEY=your_key  # For voice cloning

# Sentiment Analysis
HUGGINGFACE_API_KEY=your_key
```

### 3. Install New Python Dependencies

```bash
cd api
pip install pinecone-client openai google-cloud-translate google-cloud-speech
pip install transformers torch  # For local sentiment analysis
pip install elevenlabs  # Voice synthesis
pip install python-dotenv
pip install asyncio
```

### 4. Test the Endpoints

#### Test 1: Store a Memory

```bash
curl -X POST http://localhost:8000/api/advanced/memory/store \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "summary": "User loves pizza",
    "full_text": "The user mentioned they love pizza, especially with pepperoni and extra cheese",
    "memory_type": "preference",
    "emotion_detected": "happy"
  }'
```

#### Test 2: Recall a Memory

```bash
curl -X GET "http://localhost:8000/api/advanced/memory/recall?user_id=user_123&query=food%20preferences&top_k=3"
```

#### Test 3: Translate Text

```bash
curl -X POST http://localhost:8000/api/advanced/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you?",
    "source_language": "en",
    "target_language": "es",
    "maintain_tone": true
  }'
```

#### Test 4: Get Bonding Status

```bash
curl -X GET "http://localhost:8000/api/advanced/bonding-status?user_id=user_123"
```

#### Test 5: Switch Mode

```bash
curl -X POST http://localhost:8000/api/advanced/mode/switch \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "new_mode": "companion",
    "context": {}
  }'
```

---

## Component Integration

### Using Mode Switcher in Your App

```typescript
import { ModeSwitcher } from '@/components/ModeSwitcher';

export default function Home() {
  return (
    <main>
      <ModeSwitcher />
    </main>
  );
}
```

### Using Memory Hook

```typescript
import { useMemory } from '@/hooks/useMemory';

export function MyComponent() {
  const { memories, storeMemory, recallMemory } = useMemory('user_123');

  const handleStoreMemory = async () => {
    await storeMemory({
      summary: "User mentioned their birthday",
      full_text: "It's December 25th",
      memory_type: "birthday"
    });
  };

  return (
    <button onClick={handleStoreMemory}>
      Save Memory
    </button>
  );
}
```

### Using Translator Hook

```typescript
import { useTranslator } from '@/hooks/useTranslator';

export function TranslatorComponent() {
  const { translate, supported_languages } = useTranslator();

  const handleTranslate = async () => {
    const result = await translate({
      text: "Hello world",
      source_language: "en",
      target_language: "fr"
    });
    console.log(result.translated_text);
  };

  return (
    <>
      <button onClick={handleTranslate}>Translate</button>
    </>
  );
}
```

---

## Key Implementation Details

### Memory Engine Flow

```
1. User Input
   ↓
2. Emotion Detection (via tone analysis)
   ↓
3. Text Summarization
   ↓
4. Vector Embedding (OpenAI API)
   ↓
5. Store in Supabase + Pinecone
   ↓
6. Index for semantic search
   ↓
7. Ready for recall
```

### Translation Flow

```
1. Input Audio/Text
   ↓
2. Language Detection (auto-detect or specified)
   ↓
3. Check Translation Cache (Redis)
   ↓
4. If cache miss: Call Translation API
   ↓
5. Extract sentiment/tone from original
   ↓
6. Apply sentiment to translation
   ↓
7. Generate voice with tone (if S2S)
   ↓
8. Cache result for future use
```

### Bonding Progression

```
Interaction 1-10:     Stranger → Acquaintance
Interaction 10-50:    Acquaintance → Friend
Interaction 50-100:   Friend → Close Friend
Interaction 100-200:  Close Friend → Best Friend
Interaction 200+:     Best Friend → Soul Twin
```

**Bonding increases faster with:**
- More frequent interactions
- Longer conversations
- Emotional engagement (sad/happy moments)
- Successful memory recalls

---

## Performance Optimization Tips

### 1. Caching Strategy

```python
# Cache translations for 24 hours
TRANSLATION_CACHE_TTL = 86400  # seconds

# Cache most frequent language pairs
PRIORITY_LANGUAGE_PAIRS = [
    ('en', 'es'),
    ('en', 'fr'),
    ('en', 'de'),
    ('ta', 'en'),
    ('en', 'ta'),
]
```

### 2. Vector Search Optimization

```python
# Use filtered search when possible
memories = await memory_engine.recall_memory(
    user_id=user_id,
    query="food preferences",
    top_k=5,
    time_weight=0.1  # Prioritize recent memories
)
```

### 3. Speech Processing Parallelization

```python
# Run ASR and analysis in parallel
tasks = [
    speech_recognition(audio_url),
    voice_profile_extraction(audio_url),
    emotion_detection_from_tone(audio_url)
]
results = await asyncio.gather(*tasks)
```

---

## Troubleshooting

### Issue: Vector Embedding Fails

**Solution:**
```python
# Check OpenAI API key
import os
assert os.getenv('OPENAI_API_KEY'), "Missing OPENAI_API_KEY"

# Verify embedding dimension matches
assert len(embedding) == 1536, f"Expected 1536 dims, got {len(embedding)}"
```

### Issue: Translation Cache Not Working

**Solution:**
```python
# Ensure Redis is running
redis-cli ping  # Should return PONG

# Clear cache if needed
redis-cli FLUSHALL
```

### Issue: Memory Recall Returns Poor Results

**Solution:**
```python
# Check similarity threshold
# Lower threshold = more results, but less relevant
SIMILARITY_THRESHOLD = 0.7  # Try 0.5 for more results

# Add more time weight to get recent memories
time_weight=0.3  # Higher = prioritize recent
```

---

## Testing Checklist

### Unit Tests
- [ ] Memory storage works
- [ ] Vector embedding generation
- [ ] Semantic search accuracy
- [ ] Translation cache hit/miss
- [ ] Emotion detection accuracy

### Integration Tests
- [ ] End-to-end memory recall
- [ ] Mode switching preserves state
- [ ] Translation with voice cloning
- [ ] Bonding level progression

### Performance Tests
- [ ] Translation latency < 500ms
- [ ] Memory recall latency < 200ms
- [ ] Mode switch latency < 500ms
- [ ] Database query times < 100ms

### User Experience Tests
- [ ] UI responds smoothly to mode switches
- [ ] Chat feels natural in Companion mode
- [ ] Translation maintains tone
- [ ] Memories feel relevant when recalled

---

## Next Steps

1. **Set up Pinecone account** (or use Supabase pgvector)
2. **Get OpenAI API key** for embeddings
3. **Configure translation API** (Google/DeepL)
4. **Test memory endpoints** (curl commands above)
5. **Build memory UI** using ModeSwitcher as template
6. **Integrate voice cloning** for S2S translation
7. **Deploy and scale**

---

## Resources

- [Pinecone Documentation](https://docs.pinecone.io)
- [OpenAI Embeddings](https://platform.openai.com/docs/api-reference/embeddings)
- [Google Cloud Translation](https://cloud.google.com/translate/docs)
- [ElevenLabs Voice Cloning](https://elevenlabs.io/voice-cloning)
- [Supabase pgvector](https://supabase.com/docs/guides/database/vector)

---

**Implementation Status: Ready for Integration**  
**Estimated Time: 1-2 weeks for full integration**  
**Complexity: Medium (mostly API integrations)**
