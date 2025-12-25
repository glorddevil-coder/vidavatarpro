-- Seed data for default effects
INSERT INTO effect_library (name, type, pitch_multiplier, formant_shift, tempo_rate, description)
VALUES
    ('Trickster (Default)', 'trickster', 1.0, 0.65, 1.1, 'Viral Trickster effect - Pitch +4, Formant 0.65x, Tempo 1.1x'),
    ('Deep Bass', 'deepbass', 0.5, 1.2, 1.0, 'Deep bass enhancement'),
    ('Chipmunk', 'custom', 2.0, 1.0, 1.0, 'High pitch cartoon effect'),
    ('Slow Motion', 'custom', 1.0, 1.0, 0.7, 'Slow down tempo without pitch change');

-- Seed data for supported translation languages
-- This is metadata for the translator module
INSERT INTO translation_cache (source_text, source_language, target_language, translated_text, confidence_score)
VALUES
    ('Hello', 'en', 'es', 'Hola', 0.99),
    ('Hello', 'en', 'fr', 'Bonjour', 0.99),
    ('Good morning', 'en', 'ta', 'Kalai Vanakkam', 0.95),
    ('Thank you', 'en', 'de', 'Danke', 0.99),
    ('Thank you', 'en', 'ja', 'ありがとうございます', 0.98);

