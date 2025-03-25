import { useState, useEffect, useCallback } from 'react';

interface FinancialPlan {
  goal: string;
  steps: string[];
  timeline: string;
  estimated_cost: string;
  risks: string[];
  recommendations: string[];
}

interface WebSocketResponse {
  success: boolean;
  message: string;
  data?: FinancialPlan;
  error?: string;
}

export const useWebSocket = () => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');

    ws.onopen = () => {
      setIsConnected(true);
      setError(null);
    };

    ws.onclose = () => {
      setIsConnected(false);
    };

    ws.onerror = (event) => {
      setError('WebSocket error occurred');
      console.error('WebSocket error:', event);
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, []);

  const sendMessage = useCallback((message: string): Promise<WebSocketResponse> => {
    return new Promise((resolve, reject) => {
      if (!socket || !isConnected) {
        reject(new Error('WebSocket is not connected'));
        return;
      }

      const handleMessage = (event: MessageEvent) => {
        try {
          const response = JSON.parse(event.data);
          socket.removeEventListener('message', handleMessage);
          resolve(response);
        } catch (error) {
          socket.removeEventListener('message', handleMessage);
          reject(error);
        }
      };

      socket.addEventListener('message', handleMessage);
      socket.send(message);
    });
  }, [socket, isConnected]);

  return {
    isConnected,
    error,
    sendMessage,
  };
}; 