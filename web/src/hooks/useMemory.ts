import { useState, useCallback, useEffect } from 'react';
import { apiClient } from '@/lib/api/client';

export interface Memory {
  id: string;
  user_id: string;
  summary: string;
  full_text: string;
  emotion_detected: string;
  emotion_confidence: number;
  memory_type: 'note' | 'reminder' | 'birthday' | 'event' | 'preference';
  recalled_count: number;
  created_at: string;
  updated_at: string;
}

export interface MemoryCreatePayload {
  user_id?: string;
  summary: string;
  full_text: string;
  memory_type: 'note' | 'reminder' | 'birthday' | 'event' | 'preference';
  emotion_detected?: string;
}

export interface MemoryRecallResponse {
  memories: Memory[];
  total_count: number;
  search_time_ms: number;
}

export function useMemory(userId: string) {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Store a new memory
  const storeMemory = useCallback(async (payload: MemoryCreatePayload) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.post('/api/advanced/memory/store', {
        user_id: userId,
        ...payload,
      });
      
      // Optionally refresh memories after storing
      await recallMemories('all');
      
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to store memory';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [userId]);

  // Recall memories based on query
  const recallMemories = useCallback(async (query: string, topK: number = 5) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get<MemoryRecallResponse>(
        '/api/advanced/memory/recall',
        {
          params: {
            user_id: userId,
            query: query === 'all' ? '' : query,
            top_k: topK,
          },
        }
      );
      
      setMemories(response.memories);
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to recall memories';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [userId]);

  // Get proactive recall (important upcoming events/reminders)
  const getProactiveRecall = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get<MemoryRecallResponse>(
        '/api/advanced/memory/proactive-recall',
        {
          params: { user_id: userId },
        }
      );
      
      setMemories(response.memories);
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to get proactive recall';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [userId]);

  // Consolidate memories (merge similar ones)
  const consolidateMemories = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.post('/api/advanced/memory/consolidate', {
        user_id: userId,
        similarity_threshold: 0.8,
      });
      
      // Refresh memories after consolidation
      await recallMemories('all');
      
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to consolidate memories';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [userId]);

  // Load initial memories on mount
  useEffect(() => {
    recallMemories('all').catch(() => {
      // Silently fail on initial load
    });
  }, [userId]);

  return {
    memories,
    loading,
    error,
    storeMemory,
    recallMemories,
    getProactiveRecall,
    consolidateMemories,
  };
}
