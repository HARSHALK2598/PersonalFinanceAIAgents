import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { method } = req;

  switch (method) {
    case 'POST':
      try {
        const response = await fetch('http://localhost:8000/sessions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        res.status(200).json(data);
      } catch (error) {
        console.error('Error creating session:', error);
        res.status(500).json({ error: 'Failed to create session' });
      }
      break;

    case 'GET':
      try {
        const response = await fetch('http://localhost:8000/sessions');
        const data = await response.json();
        res.status(200).json(data);
      } catch (error) {
        console.error('Error fetching sessions:', error);
        res.status(500).json({ error: 'Failed to fetch sessions' });
      }
      break;

    case 'DELETE':
      try {
        const { sessionId } = req.query;
        const response = await fetch(`http://localhost:8000/sessions/${sessionId}`, {
          method: 'DELETE',
        });
        const data = await response.json();
        res.status(200).json(data);
      } catch (error) {
        console.error('Error deleting session:', error);
        res.status(500).json({ error: 'Failed to delete session' });
      }
      break;

    default:
      res.setHeader('Allow', ['POST', 'GET', 'DELETE']);
      res.status(405).end(`Method ${method} Not Allowed`);
  }
} 