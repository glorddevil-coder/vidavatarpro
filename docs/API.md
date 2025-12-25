# API Documentation - AuraStudio AI

## Base URL
```
http://localhost:8000
```

## Authentication
All endpoints (except `/health`) require Bearer token in header:
```
Authorization: Bearer {supabase_jwt_token}
```

---

## Endpoints

### Projects

#### List Projects
```http
GET /api/projects?user_id={user_id}
```
**Response:**
```json
[
  {
    "id": "proj_123",
    "user_id": "user_456",
    "title": "My First Video",
    "script_text": "Hello world!",
    "actor_id": "actor_luna",
    "status": "draft",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### Create Project
```http
POST /api/projects
Content-Type: application/json

{
  "user_id": "user_456",
  "title": "New Project",
  "script_text": "Your script here",
  "actor_id": "actor_luna"
}
```

#### Get Project
```http
GET /api/projects/{project_id}
```

#### Update Project
```http
PUT /api/projects/{project_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "status": "processing"
}
```

#### Delete Project
```http
DELETE /api/projects/{project_id}
```

---

### Audio Processing

#### Apply Trickster Effect
```http
POST /api/audio/trickster
Content-Type: application/json

{
  "audio_url": "/path/to/audio.wav",
  "pitch_shift": 4.0,
  "formant_shift": 0.65,
  "tempo_rate": 1.1
}
```

**Response:**
```json
{
  "success": true,
  "processed_url": "https://s3.amazonaws.com/processed_audio.wav",
  "processing_time_ms": 2500
}
```

#### Upload Audio
```http
POST /api/audio/upload
Content-Type: multipart/form-data

[binary audio file]
```

**Response:**
```json
{
  "filename": "voice.wav",
  "path": "/tmp/voice_123.wav",
  "size": 250000
}
```

---

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Error Handling

All errors return appropriate HTTP status codes:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Status Codes:**
- `200` – Success
- `201` – Created
- `400` – Bad request (invalid input)
- `401` – Unauthorized (invalid token)
- `404` – Not found
- `500` – Server error

---

## Rate Limiting

- **Free tier**: 100 requests/minute
- **Pro tier**: 1000 requests/minute
- **Enterprise**: Unlimited

Limits enforced via `X-RateLimit-*` headers.

---

## Example: Complete Script-to-Video Flow

```python
import requests
import json

API_BASE = "http://localhost:8000"
token = "your_supabase_jwt"

headers = {"Authorization": f"Bearer {token}"}

# 1. Create project
project = requests.post(
    f"{API_BASE}/api/projects",
    json={
        "user_id": "user_123",
        "title": "Commercial",
        "script_text": "Buy our product!",
        "actor_id": "actor_zara"
    },
    headers=headers
).json()

print(f"Created project: {project['id']}")

# 2. Process audio with Trickster effect
audio_result = requests.post(
    f"{API_BASE}/api/audio/trickster",
    json={
        "audio_url": "https://s3.amazonaws.com/voice.wav",
        "pitch_shift": 4.0,
        "formant_shift": 0.65,
        "tempo_rate": 1.1
    },
    headers=headers
).json()

print(f"Processed audio: {audio_result['processed_url']}")

# 3. Update project status to processing
requests.put(
    f"{API_BASE}/api/projects/{project['id']}",
    json={"status": "processing"},
    headers=headers
)

print("Project status: processing")
```

---

## Trickster Audio Engine Specification

### Default Presets

**Trickster (Viral Effect)**
- Pitch: +4 semitones
- Formant: 0.65x (lower voice)
- Tempo: 1.1x (10% faster)

**Deep Bass**
- Pitch: -6 semitones
- Formant: 1.2x (resonance boost)
- Tempo: 1.0x

**Chipmunk**
- Pitch: +12 semitones
- Formant: 1.0x
- Tempo: 1.0x

### Custom Effect Creation

Users can create custom effects by setting their own parameters:

```json
{
  "name": "My Effect",
  "type": "custom",
  "pitch_multiplier": 1.5,
  "formant_shift": 0.8,
  "tempo_rate": 0.95
}
```

---

## WebSocket Real-time Updates (Future)

For real-time project sync, use Supabase Realtime directly (not via this API):

```javascript
const subscription = supabase
  .from('projects')
  .on('*', (payload) => {
    console.log('Project updated:', payload);
  })
  .subscribe();
```
