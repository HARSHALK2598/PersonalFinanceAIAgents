import React, { useState, useEffect, useRef } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

interface Message {
  id: string;
  timestamp: string;
  role: 'user' | 'assistant';
  content: string;
  metadata?: any;
}

interface ChatInterfaceProps {
  onPlanGenerated?: (plan: any) => void;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ onPlanGenerated }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { sendMessage, lastMessage, connectionStatus } = useWebSocket();

  useEffect(() => {
    // Initialize session
    const initSession = async () => {
      try {
        const response = await fetch('/api/sessions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        setSessionId(data.session_id);
      } catch (error) {
        console.error('Failed to initialize session:', error);
      }
    };

    initSession();
  }, []);

  useEffect(() => {
    if (lastMessage) {
      const message = JSON.parse(lastMessage);
      if (message.success) {
        const newMessage: Message = {
          id: Date.now().toString(),
          timestamp: new Date().toISOString(),
          role: 'assistant',
          content: message.data.plan,
          metadata: message.data,
        };
        setMessages(prev => [...prev, newMessage]);
        
        if (onPlanGenerated) {
          onPlanGenerated(message.data.plan);
        }
      }
    }
  }, [lastMessage, onPlanGenerated]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !sessionId) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      role: 'user',
      content: input,
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');

    await sendMessage({
      session_id: sessionId,
      text: input,
    });
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-[70%] rounded-lg p-3 ${
                message.role === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              <p className="text-sm">{message.content}</p>
              <p className="text-xs mt-1 opacity-70">
                {new Date(message.timestamp).toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your financial goal..."
            className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={connectionStatus !== 'connected'}
          />
          <button
            type="submit"
            disabled={!input.trim() || connectionStatus !== 'connected'}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
}; 