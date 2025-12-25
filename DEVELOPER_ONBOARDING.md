# Developer Onboarding Checklist - AuraStudio AI v2.0

**Purpose:** Get a new developer up to speed on the advanced features architecture

**Estimated Time:** 2-3 hours

---

## Pre-Work (30 minutes)

### Environment Setup
- [ ] Clone the repository
- [ ] Create Python virtual environment
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```
- [ ] Install Python dependencies
  ```bash
  cd api
  pip install -r requirements.txt
  ```
- [ ] Install Node.js dependencies
  ```bash
  cd ../web
  npm install
  ```
- [ ] Create `.env` and `.env.local` files
- [ ] Verify database connection

### Verify Everything Works
- [ ] Start backend: `python -m uvicorn main:app --reload`
- [ ] Start frontend: `npm run dev`
- [ ] Visit http://localhost:3000 in browser
- [ ] Backend should respond at http://localhost:8000/api/advanced/features

---

## Part 1: Understanding the Architecture (45 minutes)

### Read the Documentation (30 minutes)
1. [ ] Read [ADVANCED_FEATURES.md](../docs/ADVANCED_FEATURES.md)
   - Focus on: Three Modes overview, Memory Engine, Translator module
2. [ ] Skim [MASTER_SPECIFICATION_V2.md](../docs/MASTER_SPECIFICATION_V2.md)
   - Focus on: Architecture diagrams, data flow

### Watch/Understand the Code (15 minutes)
1. [ ] Open `api/app/models/advanced_features.py`
   - Understand: All Pydantic models and their relationships
2. [ ] Open `web/src/components/ModeSwitcher.tsx`
   - Understand: How modes are structured and what each contains

---

## Part 2: Backend Services Deep Dive (60 minutes)

### Study Memory Engine (20 minutes)

**File:** `api/app/services/memory_engine.py`

- [ ] Understand the `Memory` dataclass structure
- [ ] Trace the flow of `store_memory()` method
- [ ] Trace the flow of `recall_memory()` method
- [ ] Find where vector embeddings would come in
- [ ] Understand `emotional_response_synthesis()`

**Key Questions to Answer:**
- How is a memory stored?
- How are similar memories found?
- What happens when bonding level increases?

### Study Translator Service (20 minutes)

**File:** `api/app/services/translator.py`

- [ ] Understand the `Language` enum
- [ ] Trace the flow of `translate()` method
- [ ] Trace the flow of `speech_to_speech()` method
- [ ] Find where actual API calls go
- [ ] Understand latency optimization strategy

**Key Questions to Answer:**
- How many languages are supported?
- What's the S2S pipeline?
- Where would Google Translate API integrate?

### Study API Routes (20 minutes)

**File:** `api/app/routes/advanced.py`

- [ ] Count all endpoints (should be 15+)
- [ ] For each endpoint, understand:
  - Input parameters
  - Response format
  - Error handling
  - Mock implementation
- [ ] Trace one complete example (store + recall memory)

**Key Questions to Answer:**
- What data does each endpoint accept?
- What does each endpoint return?
- Which endpoints are critical for each mode?

---

## Part 3: Frontend Integration (45 minutes)

### Study ModeSwitcher Component (15 minutes)

**File:** `web/src/components/ModeSwitcher.tsx`

- [ ] Understand the `MODES` constant
- [ ] Trace state management (useState for currentMode)
- [ ] Understand Studio mode content
- [ ] Understand Companion mode content
- [ ] Understand Assistant mode content
- [ ] Understand API integration points

**Key Questions to Answer:**
- How are modes switched?
- What UI appears in each mode?
- Where would real API calls go?

### Study Frontend Hooks (20 minutes)

**File:** `web/src/hooks/useMemory.ts`, `useTranslator.ts`, `useBonding.ts`

For each hook:
- [ ] Understand the state variables
- [ ] Trace each method (store, recall, translate, etc.)
- [ ] Find API call locations
- [ ] Understand error handling

**Key Questions to Answer:**
- What does each hook do?
- How would you use it in a component?
- Where would actual API integration happen?

### Try Building a Component (10 minutes)

Create a simple component that uses the hooks:

```typescript
// web/src/components/MemoryTest.tsx
'use client'

import { useMemory } from '@/hooks/useMemory';

export function MemoryTest() {
  const { memories, storeMemory, loading } = useMemory('test-user');

  return (
    <div>
      <button 
        onClick={() => storeMemory({
          summary: 'Test',
          full_text: 'Testing the memory hook',
          memory_type: 'note'
        })}
        disabled={loading}
      >
        Save Test Memory
      </button>
      
      {memories.map(m => (
        <div key={m.id}>{m.summary}</div>
      ))}
    </div>
  );
}
```

---

## Part 4: Database Understanding (30 minutes)

### Study Database Schema (20 minutes)

**File:** `db/migrations/001_initial_schema.sql`

- [ ] Find the 5 new tables for v2.0:
  1. [ ] `user_memory` - memory storage with vectors
  2. [ ] `persona_sync` - bonding levels
  3. [ ] `conversation_history` - chat logs
  4. [ ] `translation_cache` - cached translations
  5. [ ] Verify relationships between tables
- [ ] Understand the vector column (1536 dimensions)
- [ ] Understand the indexing strategy

**Key Questions to Answer:**
- What gets stored in each table?
- How are tables related?
- Why is the vector column 1536 dimensions?

### Verify Migrations (10 minutes)

```bash
# Check migration status
psql -h localhost -U postgres -d aurastudio -c "SELECT * FROM information_schema.tables WHERE table_schema = 'public';"

# Verify pgvector extension
psql -h localhost -U postgres -d aurastudio -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Check new tables exist
psql -h localhost -U postgres -d aurastudio -c "\dt public.user_memory public.persona_sync public.conversation_history public.translation_cache;"
```

---

## Part 5: Testing (30 minutes)

### Manual API Testing (20 minutes)

Run these curl commands and understand the responses:

1. [ ] Store a memory
   ```bash
   curl -X POST http://localhost:8000/api/advanced/memory/store \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "dev-test-1",
       "summary": "Test memory",
       "full_text": "This is a test",
       "memory_type": "note"
     }'
   ```

2. [ ] Recall memories
   ```bash
   curl -X GET "http://localhost:8000/api/advanced/memory/recall?user_id=dev-test-1&query=test&top_k=5"
   ```

3. [ ] Translate text
   ```bash
   curl -X POST http://localhost:8000/api/advanced/translate \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Hello",
       "source_language": "en",
       "target_language": "es"
     }'
   ```

4. [ ] Get bonding status
   ```bash
   curl -X GET "http://localhost:8000/api/advanced/bonding-status?user_id=dev-test-1"
   ```

5. [ ] Get languages
   ```bash
   curl -X GET http://localhost:8000/api/advanced/languages
   ```

### Unit Test Understanding (10 minutes)

- [ ] Look at `api/tests/test_memory_engine.py` (if it exists)
- [ ] Understand the test structure
- [ ] Know how to run tests: `pytest api/tests/ -v`

---

## Part 6: Integration Tasks (Understand What's Needed)

### Vector Database Integration (5 min read)

**Current Status:** Placeholder using PostgreSQL pgvector
**Next Step:** Connect to Pinecone or Weaviate
**Where:** `api/app/services/memory_engine.py`

Methods to update:
- [ ] `_generate_embedding()` - Call OpenAI API
- [ ] `recall_memory()` - Use Pinecone vector search

```python
# Example (not real code)
async def _generate_embedding(self, text: str) -> list[float]:
    # TODO: Call OpenAI API
    # return embedding  # 1536-dim vector
```

### Translation API Integration (5 min read)

**Current Status:** Placeholder methods
**Next Step:** Connect to Google Translate or DeepL
**Where:** `api/app/services/translator.py`

Methods to update:
- [ ] `_call_translation_api()` - Call translation service
- [ ] `_speech_recognition()` - Call Whisper API
- [ ] `_text_to_speech()` - Call ElevenLabs API

### Voice Cloning Integration (5 min read)

**Current Status:** Voice profile extraction stubbed
**Next Step:** Integrate ElevenLabs
**Where:** `api/app/services/translator.py`

---

## Part 7: Knowledge Check (15 minutes)

Can you answer these without looking at code?

### Architecture Questions
1. [ ] What are the three modes and what do they do?
2. [ ] How does the memory system work?
3. [ ] What's the target latency for translation?
4. [ ] How many bonding levels are there?
5. [ ] What database tables store memories?

### Code Questions
6. [ ] Where would you store a memory from the frontend?
7. [ ] Where would you recall a memory?
8. [ ] How would you translate text?
9. [ ] How would you check bonding status?
10. [ ] What hook would you use for translation?

### Integration Questions
11. [ ] Which service needs Pinecone integration?
12. [ ] Which API would you use for translation?
13. [ ] Which API would you use for voice cloning?
14. [ ] Where would you call the OpenAI embeddings API?
15. [ ] How would you test your API integration?

---

## Part 8: Your First Task

Now that you understand the architecture, here's your first task:

### Task: Create a Memory Browser Component

**Objective:** Build a simple component that displays stored memories

**Steps:**
1. Create `web/src/components/MemoryBrowser.tsx`
2. Use `useMemory` hook
3. Display:
   - List of stored memories
   - Search bar to find memories
   - Memory type badge (note, reminder, etc.)
   - Emotion indicator
4. Add buttons to:
   - Store new memory
   - Delete memory (optional)

**Expected Output:**
```
[Search box]

Memories:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 "User loves coffee"
   Type: preference | Emotion: 😊 happy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 "Mentioned birthday Dec 25"
   Type: birthday | Emotion: 😄 excited
```

**Time Estimate:** 30-45 minutes
**Difficulty:** Easy → Medium

---

## Part 9: Learning Resources

### Files to Study in Order
1. **Start Here:** [ADVANCED_FEATURES.md](../docs/ADVANCED_FEATURES.md)
2. **Then:** [QUICKSTART_ADVANCED.md](../docs/QUICKSTART_ADVANCED.md)
3. **Deep Dive:** [MASTER_SPECIFICATION_V2.md](../docs/MASTER_SPECIFICATION_V2.md)
4. **Integration:** [ADVANCED_FEATURES_GUIDE.md](../docs/ADVANCED_FEATURES_GUIDE.md)
5. **Testing:** [TESTING_VALIDATION.md](../docs/TESTING_VALIDATION.md)

### Code Files to Study in Order
1. Backend Models: `api/app/models/advanced_features.py`
2. Memory Service: `api/app/services/memory_engine.py`
3. Translator Service: `api/app/services/translator.py`
4. API Routes: `api/app/routes/advanced.py`
5. Frontend Component: `web/src/components/ModeSwitcher.tsx`
6. Frontend Hooks: `web/src/hooks/useMemory.ts`, etc.

### External Resources
- [OpenAI Embeddings](https://platform.openai.com/docs/api-reference/embeddings)
- [Pinecone Documentation](https://docs.pinecone.io)
- [Google Cloud Translation](https://cloud.google.com/translate/docs)
- [ElevenLabs Voice Cloning](https://elevenlabs.io/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## Common Commands Reference

```bash
# Start backend
cd api && python -m uvicorn main:app --reload

# Start frontend
cd web && npm run dev

# Run tests
cd api && pytest tests/ -v

# Check database connection
psql -h localhost -U postgres -d aurastudio -c "\dt"

# Reset database (⚠️ caution: deletes data)
psql -h localhost -U postgres -d aurastudio < db/migrations/001_initial_schema.sql

# Check API status
curl http://localhost:8000/api/advanced/features
```

---

## Getting Help

1. **Documentation Questions:** Check the docs folder
2. **Code Questions:** Look at the service files
3. **API Questions:** See the routes file
4. **Architecture Questions:** Read MASTER_SPECIFICATION_V2.md
5. **Integration Help:** Check ADVANCED_FEATURES_GUIDE.md

---

## Success Criteria

After completing this checklist, you should be able to:

- ✅ Explain the three modes (Studio, Companion, Assistant)
- ✅ Describe how the memory engine works
- ✅ Understand the translation pipeline
- ✅ Navigate the codebase
- ✅ Make a simple API call
- ✅ Use a frontend hook
- ✅ Build a React component with the hooks
- ✅ Understand what API integrations are needed
- ✅ Know where to start with your first task

---

## Timeline

| Checkpoint | Time | What You'll Know |
|-----------|------|------------------|
| Pre-Work Done | 30 min | Environment is working |
| Architecture Read | 45 min | The big picture |
| Backend Deep Dive | 60 min | How services work |
| Frontend Done | 45 min | How UI integrates |
| Database Understood | 30 min | Data structure |
| Tests Run | 30 min | Endpoints work |
| Knowledge Check | 15 min | Can teach someone else |
| **Total** | **~4 hours** | **Ready to contribute** |

---

## Next Steps

1. ✅ Complete this checklist (2-3 hours)
2. 📋 Start your first task (Memory Browser component)
3. 🔧 Pick an API integration to work on
4. 🚀 Deploy your changes

---

**Welcome to the AuraStudio AI team!** 🚀

If you get stuck, refer back to this checklist or ask for help in the team channel.

Good luck! 💪
