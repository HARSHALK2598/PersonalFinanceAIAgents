import { useState } from 'react';
import { ChatInterface } from '../components/ChatInterface';
import { FinancialPlan } from '../components/FinancialPlan';

export default function Home() {
  const [currentPlan, setCurrentPlan] = useState<any>(null);

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Financial Coach
          </h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Chat with Your Financial Coach</h2>
            <div className="h-[600px]">
              <ChatInterface onPlanGenerated={setCurrentPlan} />
            </div>
          </div>

          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Your Financial Plan</h2>
            <div className="h-[600px] overflow-y-auto">
              {currentPlan ? (
                <FinancialPlan plan={currentPlan} />
              ) : (
                <p className="text-gray-500 text-center mt-8">
                  Start a conversation to generate your personalized financial plan
                </p>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
} 