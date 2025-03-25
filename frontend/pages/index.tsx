import { useState } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

export default function Home() {
  const [goal, setGoal] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const { isConnected, sendMessage } = useWebSocket();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const result = await sendMessage(goal);
      if (result.success) {
        setResponse(result.data);
      } else {
        setError(result.error || 'Failed to generate plan');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <div className="max-w-md mx-auto">
            <div className="divide-y divide-gray-200">
              <div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                <h1 className="text-3xl font-bold text-center mb-8">Financial Coach</h1>
                
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label htmlFor="goal" className="block text-sm font-medium text-gray-700">
                      What's your financial goal?
                    </label>
                    <textarea
                      id="goal"
                      value={goal}
                      onChange={(e) => setGoal(e.target.value)}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      rows={4}
                      placeholder="e.g., I want to save $10,000 for a down payment on a house in 2 years"
                      required
                    />
                  </div>
                  
                  <button
                    type="submit"
                    disabled={loading || !isConnected}
                    className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
                      loading || !isConnected
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
                    }`}
                  >
                    {loading ? 'Generating Plan...' : 'Get Financial Plan'}
                  </button>
                </form>

                {error && (
                  <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-md">
                    {error}
                  </div>
                )}

                {response && (
                  <div className="mt-8 space-y-6">
                    <h2 className="text-xl font-semibold">Your Financial Plan</h2>
                    
                    <div className="space-y-4">
                      <div>
                        <h3 className="font-medium">Goal</h3>
                        <p className="mt-1">{response.goal}</p>
                      </div>
                      
                      <div>
                        <h3 className="font-medium">Steps</h3>
                        <ul className="mt-1 list-disc list-inside">
                          {response.steps.map((step: string, index: number) => (
                            <li key={index}>{step}</li>
                          ))}
                        </ul>
                      </div>
                      
                      <div>
                        <h3 className="font-medium">Timeline</h3>
                        <p className="mt-1">{response.timeline}</p>
                      </div>
                      
                      <div>
                        <h3 className="font-medium">Estimated Cost</h3>
                        <p className="mt-1">{response.estimated_cost}</p>
                      </div>
                      
                      <div>
                        <h3 className="font-medium">Potential Risks</h3>
                        <ul className="mt-1 list-disc list-inside">
                          {response.risks.map((risk: string, index: number) => (
                            <li key={index}>{risk}</li>
                          ))}
                        </ul>
                      </div>
                      
                      <div>
                        <h3 className="font-medium">Recommendations</h3>
                        <ul className="mt-1 list-disc list-inside">
                          {response.recommendations.map((rec: string, index: number) => (
                            <li key={index}>{rec}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
