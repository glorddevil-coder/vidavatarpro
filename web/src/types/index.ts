// User & Authentication
export interface User {
  id: string;
  email: string;
  name?: string;
  subscription_tier: 'free' | 'pro' | 'enterprise';
  credits_remaining: number;
  created_at: string;
  updated_at: string;
}

// Project Management
export interface Project {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  script_text: string;
  actor_id: string;
  status: 'draft' | 'processing' | 'completed' | 'failed';
  duration_seconds?: number;
  created_at: string;
  last_synced: string;
  updated_at: string;
}

// Avatar & Actor Engine
export interface Avatar {
  id: string;
  name: string;
  type: 'stock' | 'custom';
  user_id?: string;
  base_voice: string;
  default_mood: string;
  mesh_path: string;
  blend_shapes: Record<string, number>;
  thumbnail_url?: string;
  created_at: string;
}

// Asset Vault
export interface Asset {
  id: string;
  user_id: string;
  type: 'image' | 'voice' | 'audio';
  name: string;
  s3_url: string;
  is_custom_avatar: boolean;
  metadata?: Record<string, any>;
  created_at: string;
}

// Audio Effects
export interface AudioEffect {
  id: string;
  name: string;
  type: 'trickster' | 'deepbass' | 'custom';
  pitch_multiplier: number;
  formant_shift: number;
  tempo_rate: number;
  description?: string;
  user_id?: string;
  created_at: string;
}

// Export Job
export interface ExportJob {
  id: string;
  project_id: string;
  user_id: string;
  format: 'mp4' | 'mov' | 'fbx';
  resolution: '1080p' | '2k' | '4k';
  status: 'queued' | 'processing' | 'completed' | 'failed';
  output_url?: string;
  error_message?: string;
  created_at: string;
  completed_at?: string;
}

// Script Analysis
export interface ScriptAnalysis {
  text: string;
  emotion_tags: Array<{
    timestamp: number;
    emotion: 'happy' | 'sad' | 'angry' | 'surprised' | 'neutral';
    confidence: number;
  }>;
  lip_sync_points?: Array<{
    time: number;
    phoneme: string;
  }>;
}
