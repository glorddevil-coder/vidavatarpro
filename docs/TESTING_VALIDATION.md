# Testing & Validation Guide - AuraStudio AI v2.0

Comprehensive testing procedures to ensure all advanced features work correctly.

---

## Unit Tests

### Memory Engine Tests

**File:** `api/tests/test_memory_engine.py`

```python
import pytest
from app.services.memory_engine import MemoryEngine
from app.models.advanced_features import MemoryCreate

@pytest.fixture
def memory_engine():
    return MemoryEngine()

@pytest.mark.asyncio
async def test_store_memory(memory_engine):
    """Test storing a memory."""
    payload = MemoryCreate(
        user_id="test-user-1",
        summary="Test memory",
        full_text="This is a test memory",
        memory_type="note",
        emotion_detected="neutral"
    )
    
    result = await memory_engine.store_memory(payload)
    
    assert result["user_id"] == "test-user-1"
    assert result["summary"] == "Test memory"
    assert "memory_vector" in result
    assert len(result["memory_vector"]) == 1536  # OpenAI embedding size

@pytest.mark.asyncio
async def test_recall_memory(memory_engine):
    """Test recalling memories by semantic search."""
    # Store a memory first
    payload = MemoryCreate(
        user_id="test-user-2",
        summary="User loves pizza",
        full_text="Mentioned they enjoy pepperoni pizza",
        memory_type="preference"
    )
    await memory_engine.store_memory(payload)
    
    # Recall similar memories
    results = await memory_engine.recall_memory(
        user_id="test-user-2",
        query="food preferences",
        top_k=5
    )
    
    assert len(results) > 0
    assert results[0]["summary"] == "User loves pizza"
    assert "similarity_score" in results[0]

@pytest.mark.asyncio
async def test_emotion_detection(memory_engine):
    """Test emotion detection accuracy."""
    test_cases = [
        ("I'm so happy!", "happy"),
        ("I'm devastated", "sad"),
        ("This is infuriating!", "angry"),
        ("How interesting", "neutral"),
        ("I'm so excited!", "excited"),
    ]
    
    for text, expected_emotion in test_cases:
        emotion, confidence = memory_engine._detect_emotion(text)
        assert emotion.lower() == expected_emotion
        assert 0 <= confidence <= 1

@pytest.mark.asyncio
async def test_memory_consolidation(memory_engine):
    """Test consolidating similar memories."""
    user_id = "test-user-3"
    
    # Store multiple related memories
    for text in [
        "User loves pizza",
        "Pepperoni is their favorite",
        "They enjoy Italian food"
    ]:
        await memory_engine.store_memory(MemoryCreate(
            user_id=user_id,
            summary=text,
            full_text=text,
            memory_type="preference"
        ))
    
    # Consolidate
    result = await memory_engine.consolidate_memories(user_id)
    
    assert "consolidated_count" in result
    assert result["consolidated_count"] >= 1

@pytest.mark.asyncio
async def test_proactive_recall(memory_engine):
    """Test proactive recall of important dates."""
    from datetime import datetime, timedelta
    
    user_id = "test-user-4"
    
    # Store a birthday reminder (tomorrow)
    tomorrow = (datetime.now() + timedelta(days=1)).isoformat()
    await memory_engine.store_memory(MemoryCreate(
        user_id=user_id,
        summary=f"Birthday on {tomorrow}",
        full_text="User's friend John has a birthday tomorrow",
        memory_type="birthday"
    ))
    
    # Get proactive recall
    result = await memory_engine.proactive_recall(user_id)
    
    assert "upcoming_memories" in result
    assert len(result["upcoming_memories"]) > 0

@pytest.mark.asyncio
async def test_bonding_progression(memory_engine):
    """Test bonding level increases with interactions."""
    user_id = "test-user-5"
    
    initial = await memory_engine.get_bonding_status(user_id)
    initial_level = initial.get("relationship_level", 1)
    
    # Simulate interactions
    for i in range(10):
        await memory_engine.store_memory(MemoryCreate(
            user_id=user_id,
            summary=f"Interaction {i}",
            full_text=f"Conversation #{i}",
            memory_type="note"
        ))
    
    updated = await memory_engine.get_bonding_status(user_id)
    
    # Bonding should increase with more interactions
    assert updated.get("relationship_level", 1) >= initial_level
```

### Translator Tests

**File:** `api/tests/test_translator.py`

```python
import pytest
from app.services.translator import GlobalTranslator

@pytest.fixture
def translator():
    return GlobalTranslator()

@pytest.mark.asyncio
async def test_detect_language(translator):
    """Test language detection."""
    test_cases = [
        ("Hello, how are you?", "en"),
        ("Hola, ¿cómo estás?", "es"),
        ("Bonjour, comment allez-vous?", "fr"),
        ("Hallo, wie geht es dir?", "de"),
    ]
    
    for text, expected_lang in test_cases:
        detected = await translator.detect_language(text)
        assert detected == expected_lang

@pytest.mark.asyncio
async def test_translate_text(translator):
    """Test text translation."""
    result = await translator.translate(
        text="Hello, how are you?",
        source_language="en",
        target_language="es"
    )
    
    assert "translated_text" in result
    assert result["source_language"] == "en"
    assert result["target_language"] == "es"
    assert "confidence_score" in result
    assert 0 <= result["confidence_score"] <= 1

@pytest.mark.asyncio
async def test_translation_cache(translator):
    """Test translation caching."""
    text = "Hello, world!"
    
    # First translation (cache miss)
    result1 = await translator.translate(
        text=text,
        source_language="en",
        target_language="fr"
    )
    assert result1["from_cache"] == False
    
    # Second translation (cache hit)
    result2 = await translator.translate(
        text=text,
        source_language="en",
        target_language="fr"
    )
    assert result2["from_cache"] == True
    assert result1["translated_text"] == result2["translated_text"]

@pytest.mark.asyncio
async def test_sentiment_preservation(translator):
    """Test that sentiment is preserved in translation."""
    test_cases = [
        "I love this!",      # Positive
        "I hate this.",      # Negative
        "This is okay.",     # Neutral
    ]
    
    for text in test_cases:
        result = await translator.translate(
            text=text,
            source_language="en",
            target_language="es",
            maintain_tone=True
        )
        
        assert "detected_sentiment" in result
        assert result["detected_sentiment"] in ["positive", "negative", "neutral"]

@pytest.mark.asyncio
async def test_batch_translate(translator):
    """Test batch translation."""
    texts = [
        "Hello",
        "How are you?",
        "Nice to meet you"
    ]
    
    results = await translator.batch_translate(
        texts=texts,
        target_language="fr"
    )
    
    assert len(results) == len(texts)
    for result in results:
        assert "translated_text" in result
        assert result["target_language"] == "fr"

@pytest.mark.asyncio
async def test_speech_to_speech_latency(translator):
    """Test speech-to-speech translation latency."""
    result = await translator.speech_to_speech(
        audio_url="https://example.com/audio.wav",
        source_language="en",
        target_language="es"
    )
    
    assert "latency_ms" in result
    assert result["latency_ms"] < 500  # Must be < 500ms
    assert "output_audio_url" in result
```

---

## Integration Tests

### API Endpoint Tests

**File:** `api/tests/test_advanced_routes.py`

```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_memory_store_endpoint(client):
    """Test POST /api/advanced/memory/store"""
    response = client.post(
        "/api/advanced/memory/store",
        json={
            "user_id": "test-user-1",
            "summary": "Test memory",
            "full_text": "This is a test",
            "memory_type": "note",
            "emotion_detected": "neutral"
        }
    )
    
    assert response.status_code == 200
    assert response.json()["summary"] == "Test memory"
    assert "id" in response.json()

def test_memory_recall_endpoint(client):
    """Test GET /api/advanced/memory/recall"""
    # Store a memory first
    client.post(
        "/api/advanced/memory/store",
        json={
            "user_id": "test-user-2",
            "summary": "Test memory",
            "full_text": "Test content",
            "memory_type": "note"
        }
    )
    
    # Recall memories
    response = client.get(
        "/api/advanced/memory/recall",
        params={
            "user_id": "test-user-2",
            "query": "test",
            "top_k": 5
        }
    )
    
    assert response.status_code == 200
    assert "memories" in response.json()
    assert len(response.json()["memories"]) > 0

def test_translate_endpoint(client):
    """Test POST /api/advanced/translate"""
    response = client.post(
        "/api/advanced/translate",
        json={
            "text": "Hello",
            "source_language": "en",
            "target_language": "es"
        }
    )
    
    assert response.status_code == 200
    assert "translated_text" in response.json()
    assert response.json()["source_language"] == "en"

def test_bonding_status_endpoint(client):
    """Test GET /api/advanced/bonding-status"""
    response = client.get(
        "/api/advanced/bonding-status",
        params={"user_id": "test-user-3"}
    )
    
    assert response.status_code == 200
    assert "relationship_level" in response.json()
    assert 1 <= response.json()["relationship_level"] <= 10

def test_mode_switch_endpoint(client):
    """Test POST /api/advanced/mode/switch"""
    response = client.post(
        "/api/advanced/mode/switch",
        json={
            "user_id": "test-user-4",
            "new_mode": "companion",
            "context": {}
        }
    )
    
    assert response.status_code == 200
    assert response.json()["new_mode"] == "companion"

def test_languages_endpoint(client):
    """Test GET /api/advanced/languages"""
    response = client.get("/api/advanced/languages")
    
    assert response.status_code == 200
    assert "languages" in response.json()
    assert len(response.json()["languages"]) >= 30
```

---

## Performance Tests

### Load Testing

**File:** `api/tests/test_performance.py`

```python
import pytest
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

@pytest.mark.performance
async def test_memory_store_latency(client):
    """Test memory storage latency (<300ms)."""
    start = time.time()
    
    response = client.post(
        "/api/advanced/memory/store",
        json={
            "user_id": "perf-test-1",
            "summary": "Performance test",
            "full_text": "Testing latency",
            "memory_type": "note"
        }
    )
    
    elapsed = (time.time() - start) * 1000  # Convert to ms
    
    assert response.status_code == 200
    assert elapsed < 300  # Must be < 300ms

@pytest.mark.performance
async def test_memory_recall_latency(client):
    """Test memory recall latency (<200ms)."""
    # Store a memory first
    client.post(
        "/api/advanced/memory/store",
        json={
            "user_id": "perf-test-2",
            "summary": "Performance test",
            "full_text": "Testing recall latency",
            "memory_type": "note"
        }
    )
    
    # Time the recall
    start = time.time()
    
    response = client.get(
        "/api/advanced/memory/recall",
        params={"user_id": "perf-test-2", "query": "test", "top_k": 5}
    )
    
    elapsed = (time.time() - start) * 1000
    
    assert response.status_code == 200
    assert elapsed < 200  # Must be < 200ms

@pytest.mark.performance
def test_translation_latency(client):
    """Test translation latency (<500ms)."""
    start = time.time()
    
    response = client.post(
        "/api/advanced/translate",
        json={
            "text": "Hello, how are you?",
            "source_language": "en",
            "target_language": "es"
        }
    )
    
    elapsed = (time.time() - start) * 1000
    
    assert response.status_code == 200
    assert elapsed < 500  # Must be < 500ms

@pytest.mark.performance
def test_concurrent_memory_operations(client):
    """Test handling 100 concurrent memory operations."""
    def store_memory():
        return client.post(
            "/api/advanced/memory/store",
            json={
                "user_id": "concurrent-test",
                "summary": f"Memory {time.time()}",
                "full_text": "Concurrent test",
                "memory_type": "note"
            }
        )
    
    # Execute 100 concurrent requests
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(store_memory) for _ in range(100)]
        results = [f.result() for f in futures]
    
    # All should succeed
    assert all(r.status_code == 200 for r in results)
    assert len(results) == 100
```

---

## End-to-End Tests

### Complete User Journey

**File:** `api/tests/test_e2e.py`

```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_complete_companion_mode_journey(client):
    """Test a complete user journey in Companion mode."""
    user_id = "e2e-user-1"
    
    # Step 1: Switch to Companion mode
    response = client.post(
        "/api/advanced/mode/switch",
        json={
            "user_id": user_id,
            "new_mode": "companion",
            "context": {}
        }
    )
    assert response.status_code == 200
    
    # Step 2: Store initial memory (user preference)
    response = client.post(
        "/api/advanced/memory/store",
        json={
            "user_id": user_id,
            "summary": "User loves coffee",
            "full_text": "Mentioned they love coffee with almond milk",
            "memory_type": "preference",
            "emotion_detected": "happy"
        }
    )
    assert response.status_code == 200
    memory_id = response.json()["id"]
    
    # Step 3: Check bonding status
    response = client.get(
        "/api/advanced/bonding-status",
        params={"user_id": user_id}
    )
    assert response.status_code == 200
    assert response.json()["relationship_level"] == 1
    
    # Step 4: Simulate more interactions (store more memories)
    for i in range(5):
        response = client.post(
            "/api/advanced/memory/store",
            json={
                "user_id": user_id,
                "summary": f"Interaction {i}",
                "full_text": f"Conversation {i}",
                "memory_type": "note"
            }
        )
        assert response.status_code == 200
    
    # Step 5: Recall a memory
    response = client.get(
        "/api/advanced/memory/recall",
        params={
            "user_id": user_id,
            "query": "coffee",
            "top_k": 3
        }
    )
    assert response.status_code == 200
    memories = response.json()["memories"]
    assert any("coffee" in m["summary"].lower() for m in memories)
    
    # Step 6: Check bonding level increased
    response = client.get(
        "/api/advanced/bonding-status",
        params={"user_id": user_id}
    )
    assert response.status_code == 200
    assert response.json()["interaction_count"] > 1

def test_complete_assistant_mode_journey(client):
    """Test a complete user journey in Assistant mode."""
    # Step 1: Switch to Assistant mode
    response = client.post(
        "/api/advanced/mode/switch",
        json={
            "user_id": "e2e-user-2",
            "new_mode": "assistant",
            "context": {}
        }
    )
    assert response.status_code == 200
    
    # Step 2: Translate text
    response = client.post(
        "/api/advanced/translate",
        json={
            "text": "Good morning, how can I help you?",
            "source_language": "en",
            "target_language": "es"
        }
    )
    assert response.status_code == 200
    assert "translated_text" in response.json()
    
    # Step 3: Get supported languages
    response = client.get("/api/advanced/languages")
    assert response.status_code == 200
    assert len(response.json()["languages"]) >= 30
    
    # Step 4: Translate to multiple languages
    for target_lang in ["fr", "de", "it"]:
        response = client.post(
            "/api/advanced/translate",
            json={
                "text": "Hello",
                "source_language": "en",
                "target_language": target_lang
            }
        )
        assert response.status_code == 200
```

---

## Testing Checklist

### Before Deployment

- [ ] All unit tests pass (`pytest api/tests/`)
- [ ] All integration tests pass (`pytest api/tests/ -m integration`)
- [ ] Performance benchmarks met:
  - [ ] Memory store < 300ms
  - [ ] Memory recall < 200ms
  - [ ] Translation < 500ms
  - [ ] Bonding status < 100ms
- [ ] Load test passes (100 concurrent requests)
- [ ] End-to-end journey tests pass
- [ ] No memory leaks (monitor RAM)
- [ ] Database migrations successful
- [ ] All API endpoints documented
- [ ] Error handling works correctly
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] Logging configured
- [ ] Security checklist passed

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest api/tests/ -v

# Run with coverage
pytest api/tests/ --cov=app --cov-report=html

# Run only performance tests
pytest api/tests/ -m performance

# Run specific test file
pytest api/tests/test_memory_engine.py -v
```

---

## Continuous Integration

**File:** `.github/workflows/test.yml`

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14-alpine
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: aurastudio_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          cd api
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov
      
      - name: Run tests
        run: |
          cd api
          pytest tests/ --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Success Criteria

✅ **Functional:**
- All 15+ API endpoints working
- Memory storage and recall accurate
- Translation working across 100+ languages
- Bonding progression working correctly
- Mode switching seamless

✅ **Performance:**
- Memory operations < 300ms
- Translation < 500ms
- All bonding operations < 100ms
- Can handle 100 concurrent users

✅ **Quality:**
- 80%+ test coverage
- No memory leaks
- Error messages helpful
- Logging comprehensive

✅ **Security:**
- API keys not exposed
- User data encrypted
- Rate limiting enabled
- CORS configured

---

**All tests passing = Ready for production!** 🚀
