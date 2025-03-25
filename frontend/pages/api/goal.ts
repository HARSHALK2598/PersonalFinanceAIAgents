export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { message } = req.body;
    const apiRes = await fetch('http://localhost:8000/submit-goal/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: message })
    });
    const json = await apiRes.json();
    res.status(200).json({ reply: 'Got it! I'm generating your plan...' });
  } else {
    res.status(405).json({ message: 'Method Not Allowed' });
  }
}
