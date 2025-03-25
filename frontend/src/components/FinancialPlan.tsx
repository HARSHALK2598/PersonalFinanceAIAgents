import React from 'react';

interface FinancialPlanProps {
  plan: {
    goal: string;
    steps: string[];
    timeline: string;
    estimated_costs: string;
    risks: string[];
    recommendations: string[];
  };
}

export const FinancialPlan: React.FC<FinancialPlanProps> = ({ plan }) => {
  return (
    <div className="space-y-6">
      {/* Main Goal */}
      <section>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Main Goal</h3>
        <p className="text-gray-700">{plan.goal}</p>
      </section>

      {/* Steps */}
      <section>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Action Steps</h3>
        <ol className="list-decimal list-inside space-y-2">
          {plan.steps.map((step, index) => (
            <li key={index} className="text-gray-700">
              {step}
            </li>
          ))}
        </ol>
      </section>

      {/* Timeline */}
      <section>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Timeline</h3>
        <p className="text-gray-700">{plan.timeline}</p>
      </section>

      {/* Estimated Costs */}
      <section>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Estimated Costs</h3>
        <p className="text-gray-700">{plan.estimated_costs}</p>
      </section>

      {/* Risks */}
      <section>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Potential Risks</h3>
        <ul className="list-disc list-inside space-y-2">
          {plan.risks.map((risk, index) => (
            <li key={index} className="text-gray-700">
              {risk}
            </li>
          ))}
        </ul>
      </section>

      {/* Recommendations */}
      <section>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Recommendations</h3>
        <ul className="list-disc list-inside space-y-2">
          {plan.recommendations.map((recommendation, index) => (
            <li key={index} className="text-gray-700">
              {recommendation}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}; 