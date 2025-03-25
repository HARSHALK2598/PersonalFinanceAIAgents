import { useState, useEffect, useCallback } from 'react';

type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error';

export const useWebSocket = () => {
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [lastMessage, setLastMessage] = useState<string | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('disconnected');

  useEffect(() => {
    const connect = () => {
      const websocket = new WebSocket('ws://localhost:8000/ws');

      websocket.onopen = () => {
        console.log('WebSocket connected');
        setConnectionStatus('connected');
      };

      websocket.onclose = () => {
        console.log('WebSocket disconnected');
        setConnectionStatus('disconnected');
      };

      websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionStatus('error');
      };

      websocket.onmessage = (event) => {
        setLastMessage(event.data);
      };

      setWs(websocket);
    };

    connect();

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);

  const sendMessage = useCallback(
    async (message: any) => {
      if (ws && connectionStatus === 'connected') {
        ws.send(JSON.stringify(message));
      } else {
        console.error('WebSocket is not connected');
      }
    },
    [ws, connectionStatus]
  );

  return {
    sendMessage,
    lastMessage,
    connectionStatus,
  };
}; 