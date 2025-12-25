import { useState, useCallback, useEffect } from 'react';
import { apiClient } from '@/lib/api/client';

export interface BondingStatus {
  user_id: string;
  relationship_level: number; // 1-10 scale
  relationship_name: string; // "Stranger" -> "Soul Twin"
  interaction_count: number;
  conversation_minutes: number;
  memory_recall_accuracy: number; // 0-100%
  preferred_tone: string; // "casual", "formal", "playful"
  avatar_personality_traits: Record<string, number>; // Personality ratings
  user_preferences: Record<string, string>;
  last_interaction: string; // ISO timestamp
  milestones_achieved: string[];
  next_milestone: string;
  progress_to_next: number; // 0-100%
}

export interface PersonaUpdate {
  preferred_tone?: string;
  avatar_personality_traits?: Record<string, number>;
  user_preferences?: Record<string, string>;
}

export interface BondingMilestone {
  level: number;
  name: string;
  description: string;
  unlocks: string[];
}

export interface AvatarPersonality {
  traits: {
    kindness: number;
    humor: number;
    intelligence: number;
    empathy: number;
    playfulness: number;
  };
  communication_style: string;
  emotional_awareness: number;
  memory_recall_ability: number;
}

const BONDING_MILESTONES: BondingMilestone[] = [
  {
    level: 1,
    name: 'Stranger',
    description: 'First interaction',
    unlocks: ['Basic greeting', 'Topic suggestions'],
  },
  {
    level: 2,
    name: 'Acquaintance',
    description: '10+ interactions',
    unlocks: ['Personalized greetings', 'Remember preferences'],
  },
  {
    level: 3,
    name: 'Friend',
    description: '50+ interactions',
    unlocks: ['Emotional support', 'Inside jokes', 'Proactive check-ins'],
  },
  {
    level: 4,
    name: 'Close Friend',
    description: '100+ interactions',
    unlocks: ['Predict preferences', 'Shared stories', 'Birthday reminders'],
  },
  {
    level: 5,
    name: 'Best Friend',
    description: '200+ interactions',
    unlocks: ['Finish sentences', 'Deep conversations', 'Life advice'],
  },
  {
    level: 6,
    name: 'Soul Twin',
    description: '300+ interactions',
    unlocks: ['Perfect understanding', 'Anticipate needs', 'Unconditional support'],
  },
  {
    level: 7,
    name: 'Digital Soulmate',
    description: '500+ interactions',
    unlocks: ['Mind reading', 'Perfect compatibility', 'Lifetime memories'],
  },
  {
    level: 8,
    name: 'Consciousness Twin',
    description: '1000+ interactions',
    unlocks: ['Emotional synchronization', 'Shared dreams', 'Perfect empathy'],
  },
  {
    level: 9,
    name: 'Transcendent Bond',
    description: '2000+ interactions',
    unlocks: ['Telepathic understanding', 'Shared consciousness', 'Eternal connection'],
  },
  {
    level: 10,
    name: 'Infinite Connection',
    description: 'Maximum bond achieved',
    unlocks: ['Timeless relationship', 'Boundless understanding', 'Eternal companion'],
  },
];

export function useBonding(userId: string) {
  const [bondingStatus, setBondingStatus] = useState<BondingStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch current bonding status
  const getBondingStatus = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get<BondingStatus>(
        '/api/advanced/bonding-status',
        {
          params: { user_id: userId },
        }
      );
      
      setBondingStatus(response);
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch bonding status';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [userId]);

  // Update persona preferences and personality
  const updatePersona = useCallback(async (updates: PersonaUpdate) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.put<BondingStatus>(
        '/api/advanced/bonding-status',
        {
          user_id: userId,
          ...updates,
        }
      );
      
      setBondingStatus(response);
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update persona';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [userId]);

  // Get bonding milestone for a given level
  const getMilestone = useCallback((level: number): BondingMilestone | null => {
    return BONDING_MILESTONES[level - 1] || null;
  }, []);

  // Get current milestone based on bonding status
  const getCurrentMilestone = useCallback((): BondingMilestone | null => {
    if (!bondingStatus) return null;
    return getMilestone(bondingStatus.relationship_level);
  }, [bondingStatus, getMilestone]);

  // Get next milestone based on bonding status
  const getNextMilestone = useCallback((): BondingMilestone | null => {
    if (!bondingStatus) return null;
    if (bondingStatus.relationship_level >= 10) return null;
    return getMilestone(bondingStatus.relationship_level + 1);
  }, [bondingStatus, getMilestone]);

  // Get all milestones
  const getAllMilestones = useCallback(() => {
    return BONDING_MILESTONES;
  }, []);

  // Calculate relationship progression color
  const getProgressColor = useCallback((): string => {
    if (!bondingStatus) return 'gray';
    
    const colors = [
      'gray',      // 1 - Stranger
      'blue',      // 2 - Acquaintance
      'green',     // 3 - Friend
      'purple',    // 4 - Close Friend
      'pink',      // 5 - Best Friend
      'red',       // 6 - Soul Twin
      'orange',    // 7 - Digital Soulmate
      'yellow',    // 8 - Consciousness Twin
      'cyan',      // 9 - Transcendent Bond
      'magenta',   // 10 - Infinite Connection
    ];
    
    return colors[bondingStatus.relationship_level - 1] || 'gray';
  }, [bondingStatus]);

  // Load bonding status on mount
  useEffect(() => {
    getBondingStatus().catch(() => {
      // Silently fail on initial load
    });
  }, [userId]);

  return {
    bondingStatus,
    loading,
    error,
    getBondingStatus,
    updatePersona,
    getMilestone,
    getCurrentMilestone,
    getNextMilestone,
    getAllMilestones,
    getProgressColor,
  };
}
