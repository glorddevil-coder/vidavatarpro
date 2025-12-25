import { useState, useCallback } from 'react';
import { apiClient } from '@/lib/api/client';

export interface TranslationRequest {
  text: string;
  source_language: string;
  target_language: string;
  maintain_tone?: boolean;
}

export interface TranslationResponse {
  original_text: string;
  translated_text: string;
  source_language: string;
  target_language: string;
  confidence_score: number;
  from_cache: boolean;
  detected_sentiment?: string;
}

export interface SpeechToSpeechRequest {
  audio_url: string;
  source_language: string;
  target_language: string;
  voice_profile?: {
    pitch: number;
    speed: number;
    emotion: string;
  };
}

export interface SpeechToSpeechResponse {
  output_audio_url: string;
  translated_text: string;
  source_language: string;
  target_language: string;
  latency_ms: number;
  voice_cloning_applied: boolean;
}

export interface Language {
  code: string;
  name: string;
  native_name: string;
  family: string;
  supported_voices?: string[];
}

export function useTranslator() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [supportedLanguages, setSupportedLanguages] = useState<Language[]>([]);

  // Translate text
  const translate = useCallback(async (payload: TranslationRequest) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.post<TranslationResponse>(
        '/api/advanced/translate',
        {
          ...payload,
          maintain_tone: payload.maintain_tone ?? true,
        }
      );
      
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to translate';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Perform speech-to-speech translation
  const speechToSpeech = useCallback(async (payload: SpeechToSpeechRequest) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.post<SpeechToSpeechResponse>(
        '/api/advanced/speech-to-speech',
        payload
      );
      
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to perform speech-to-speech translation';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Get list of supported languages
  const getLanguages = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get<{ languages: Language[] }>(
        '/api/advanced/languages'
      );
      
      setSupportedLanguages(response.languages);
      return response.languages;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch languages';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Batch translate multiple texts
  const batchTranslate = useCallback(async (texts: string[], targetLanguage: string) => {
    setLoading(true);
    setError(null);
    try {
      const requests = texts.map(text => ({
        text,
        target_language: targetLanguage,
      }));
      
      const responses = await Promise.all(
        requests.map(req => translate({ ...req, source_language: 'auto' }))
      );
      
      return responses;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to batch translate';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [translate]);

  return {
    translate,
    speechToSpeech,
    getLanguages,
    batchTranslate,
    supportedLanguages,
    loading,
    error,
  };
}
