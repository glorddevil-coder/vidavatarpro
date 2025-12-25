'use client';

import React, { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api/client';

type Mode = 'studio' | 'companion' | 'assistant';

interface ModeConfig {
  id: Mode;
  name: string;
  description: string;
  icon: string;
  color: string;
  features: string[];
}

const MODES: ModeConfig[] = [
  {
    id: 'studio',
    name: 'Studio Mode',
    description: 'The Actor: Create videos with AI actors',
    icon: '🎬',
    color: 'from-purple-500 to-pink-500',
    features: ['Video Creation', 'Script Editor', 'Effects Library', '4K Export']
  },
  {
    id: 'companion',
    name: 'Companion Mode',
    description: 'The Friend: Bond with your AI companion',
    icon: '❤️',
    color: 'from-blue-500 to-cyan-500',
    features: ['Memory Recall', 'Emotional Support', 'Diary Keeper', 'Personal Bonding']
  },
  {
    id: 'assistant',
    name: 'Assistant Mode',
    description: 'The Pro: Real-time translation & task management',
    icon: '🚀',
    color: 'from-green-500 to-emerald-500',
    features: ['100+ Languages', 'Live Translation', 'Reminders', 'Voice Commands']
  }
];

export function ModeSwitcher() {
  const [currentMode, setCurrentMode] = useState<Mode>('companion');
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    // Get user ID from session/auth
    const user = localStorage.getItem('user_id');
    setUserId(user);
  }, []);

  const switchMode = async (mode: Mode) => {
    if (mode === currentMode) return;

    setIsTransitioning(true);
    try {
      await apiClient.post(`/api/advanced/mode/switch?user_id=${userId}`, {
        new_mode: mode,
        context: {}
      });
      setCurrentMode(mode);
    } catch (error) {
      console.error('Failed to switch mode:', error);
    } finally {
      setIsTransitioning(false);
    }
  };

  const currentModeConfig = MODES.find(m => m.id === currentMode);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      {/* Mode Switcher Bar */}
      <div className="sticky top-0 z-50 bg-slate-800/95 backdrop-blur-sm border-b border-slate-700">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-white">AuraStudio AI</h1>
            <div className="flex gap-2">
              {MODES.map(mode => (
                <button
                  key={mode.id}
                  onClick={() => switchMode(mode.id)}
                  disabled={isTransitioning}
                  className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                    currentMode === mode.id
                      ? `bg-gradient-to-r ${mode.color} text-white shadow-lg`
                      : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                  } disabled:opacity-50`}
                >
                  <span className="mr-2">{mode.icon}</span>
                  {mode.name}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Mode Content Area */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        {currentModeConfig && (
          <div className="mb-12">
            <div className={`bg-gradient-to-r ${currentModeConfig.color} rounded-2xl p-8 text-white shadow-2xl`}>
              <h2 className="text-4xl font-bold mb-2">{currentModeConfig.name}</h2>
              <p className="text-lg opacity-90 mb-6">{currentModeConfig.description}</p>
              
              {/* Features Grid */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {currentModeConfig.features.map(feature => (
                  <div key={feature} className="bg-white/20 backdrop-blur rounded-lg p-4">
                    <p className="font-semibold text-sm">{feature}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Mode-Specific Content */}
        {currentMode === 'studio' && <StudioModeContent />}
        {currentMode === 'companion' && <CompanionModeContent />}
        {currentMode === 'assistant' && <AssistantModeContent />}
      </div>
    </div>
  );
}

// ===== Studio Mode Component =====
function StudioModeContent() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div className="md:col-span-2 bg-slate-800 rounded-xl p-8">
        <h3 className="text-xl font-bold text-white mb-6">Create Video</h3>
        <textarea
          className="w-full h-48 bg-slate-700 text-white rounded-lg p-4 mb-4 focus:outline-none focus:ring-2 focus:ring-purple-500"
          placeholder="Enter your script here..."
        />
        <div className="flex gap-4">
          <button className="flex-1 bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-lg transition">
            Generate Video
          </button>
          <button className="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-bold py-2 px-4 rounded-lg transition">
            Preview
          </button>
        </div>
      </div>

      <div className="bg-slate-800 rounded-xl p-8">
        <h3 className="text-xl font-bold text-white mb-6">Quick Actions</h3>
        <div className="space-y-3">
          <button className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold py-2 px-4 rounded-lg hover:from-purple-700 hover:to-pink-700 transition">
            Select Avatar
          </button>
          <button className="w-full bg-slate-700 hover:bg-slate-600 text-white font-bold py-2 px-4 rounded-lg transition">
            Apply Effects
          </button>
          <button className="w-full bg-slate-700 hover:bg-slate-600 text-white font-bold py-2 px-4 rounded-lg transition">
            Export 4K
          </button>
        </div>
      </div>
    </div>
  );
}

// ===== Companion Mode Component =====
function CompanionModeContent() {
  const [message, setMessage] = useState('');
  const [bondingLevel, setBondingLevel] = useState(3);
  const [memories, setMemories] = useState<any[]>([]);

  const sendMessage = async () => {
    if (!message.trim()) return;
    
    try {
      // Would call avatar-response endpoint
      setMemories([...memories, {
        type: 'message',
        content: message,
        timestamp: new Date()
      }]);
      setMessage('');
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const levelNames = ['Stranger', 'New Friend', 'Acquaintance', 'Friend', 'Close Friend'];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
      {/* Chat Area */}
      <div className="md:col-span-2 bg-slate-800 rounded-xl p-8">
        <h3 className="text-xl font-bold text-white mb-6">Chat with Your Friend</h3>
        
        {/* Chat Messages */}
        <div className="bg-slate-900 rounded-lg p-6 mb-4 h-96 overflow-y-auto space-y-4">
          <div className="text-slate-400 text-center py-8">
            {memories.length === 0 ? 'Start chatting with your AI friend!' : null}
          </div>
          {memories.map((mem, idx) => (
            <div key={idx} className="flex justify-end">
              <div className="bg-blue-600 text-white rounded-lg p-3 max-w-xs">
                {mem.content}
              </div>
            </div>
          ))}
        </div>

        {/* Input */}
        <div className="flex gap-2">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            className="flex-1 bg-slate-700 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Share your thoughts..."
          />
          <button
            onClick={sendMessage}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition"
          >
            Send
          </button>
        </div>
      </div>

      {/* Bonding Panel */}
      <div className="bg-slate-800 rounded-xl p-8">
        <h3 className="text-xl font-bold text-white mb-6">Your Bond</h3>
        
        {/* Relationship Level */}
        <div className="mb-8">
          <p className="text-slate-400 text-sm mb-2">Relationship Level</p>
          <div className="flex items-center gap-2 mb-4">
            <div className="text-4xl font-bold text-blue-400">{bondingLevel}</div>
            <div className="text-sm text-slate-300">/10</div>
          </div>
          <p className="text-slate-300 font-semibold">{levelNames[bondingLevel - 1]}</p>
        </div>

        {/* Progress Bar */}
        <div className="bg-slate-700 rounded-lg p-4 mb-6">
          <div className="flex justify-between mb-2">
            <p className="text-sm text-slate-400">Progress to Next Level</p>
            <p className="text-sm text-slate-300">+35 interactions</p>
          </div>
          <div className="w-full bg-slate-600 rounded-full h-2">
            <div
              className="bg-gradient-to-r from-blue-500 to-cyan-500 h-2 rounded-full"
              style={{ width: `${(bondingLevel / 10) * 100}%` }}
            />
          </div>
        </div>

        {/* Recent Memories */}
        <div>
          <p className="text-slate-400 text-sm mb-3">Remembered Moments</p>
          <div className="space-y-2">
            <div className="bg-slate-700 rounded p-3 text-sm text-slate-300">
              ✨ You love pizza with pepperoni
            </div>
            <div className="bg-slate-700 rounded p-3 text-sm text-slate-300">
              🎂 Friend's birthday is Friday
            </div>
            <div className="bg-slate-700 rounded p-3 text-sm text-slate-300">
              😊 You felt happy yesterday
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ===== Assistant Mode Component =====
function AssistantModeContent() {
  const [sourceLanguage, setSourceLanguage] = useState('en');
  const [targetLanguage, setTargetLanguage] = useState('es');
  const [inputText, setInputText] = useState('');
  const [translatedText, setTranslatedText] = useState('');

  const translate = async () => {
    try {
      const response = await apiClient.post<any>('/api/advanced/translate', {
        text: inputText,
        source_language: sourceLanguage,
        target_language: targetLanguage,
        maintain_tone: true
      });
      if (typeof response === 'object' && response !== null && 'translated_text' in response) {
        setTranslatedText((response as any).translated_text);
      }
    } catch (error) {
      console.error('Translation failed:', error);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      {/* Translation Interface */}
      <div className="bg-slate-800 rounded-xl p-8">
        <h3 className="text-xl font-bold text-white mb-6">Live Translator</h3>
        
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-slate-400 text-sm mb-2">From</label>
              <select
                value={sourceLanguage}
                onChange={(e) => setSourceLanguage(e.target.value)}
                className="w-full bg-slate-700 text-white rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="en">English</option>
                <option value="ta">Tamil</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
                <option value="ja">Japanese</option>
              </select>
            </div>
            <div>
              <label className="block text-slate-400 text-sm mb-2">To</label>
              <select
                value={targetLanguage}
                onChange={(e) => setTargetLanguage(e.target.value)}
                className="w-full bg-slate-700 text-white rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="en">English</option>
                <option value="ta">Tamil</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
                <option value="ja">Japanese</option>
              </select>
            </div>
          </div>

          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            className="w-full h-32 bg-slate-700 text-white rounded-lg p-4 focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="Enter text to translate..."
          />

          <button
            onClick={translate}
            className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition"
          >
            Translate
          </button>

          {translatedText && (
            <div className="bg-slate-700 rounded-lg p-4">
              <p className="text-slate-400 text-sm mb-2">Translation</p>
              <p className="text-white">{translatedText}</p>
            </div>
          )}
        </div>
      </div>

      {/* Tasks & Reminders */}
      <div className="bg-slate-800 rounded-xl p-8">
        <h3 className="text-xl font-bold text-white mb-6">My Tasks</h3>
        
        <div className="space-y-3 mb-6">
          <div className="flex items-center gap-3 bg-slate-700 rounded-lg p-4">
            <input type="checkbox" className="w-5 h-5" defaultChecked />
            <span className="text-white">Call mom (Tamil)</span>
          </div>
          <div className="flex items-center gap-3 bg-slate-700 rounded-lg p-4">
            <input type="checkbox" className="w-5 h-5" />
            <span className="text-white">Translate email from client (French→English)</span>
          </div>
          <div className="flex items-center gap-3 bg-slate-700 rounded-lg p-4">
            <input type="checkbox" className="w-5 h-5" />
            <span className="text-white">Set reminder for meeting at 3 PM</span>
          </div>
        </div>

        <button className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition">
          Add Task
        </button>
      </div>
    </div>
  );
}
