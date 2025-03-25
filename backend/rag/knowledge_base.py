from typing import List, Dict, Any

class FinancialKnowledgeBase:
    @staticmethod
    def get_initial_advice() -> List[Dict[str, Any]]:
        return [
            # Savings and Budgeting
            {
                "text": "For creating a budget: Start by tracking all income and expenses, categorize spending, identify areas to cut back, and set realistic spending limits for each category.",
                "metadata": {"topic": "budgeting", "category": "savings"}
            },
            {
                "text": "For emergency fund building: Aim to save 3-6 months of living expenses, start with small regular contributions, keep funds in a high-yield savings account, and avoid touching it except for true emergencies.",
                "metadata": {"topic": "emergency_fund", "category": "savings"}
            },
            
            # Investment Planning
            {
                "text": "For stock market investing: Start with index funds for diversification, understand your risk tolerance, invest regularly through dollar-cost averaging, and maintain a long-term perspective.",
                "metadata": {"topic": "stock_investing", "category": "investing"}
            },
            {
                "text": "For retirement planning: Start early with tax-advantaged accounts like 401(k) or IRA, contribute enough to get employer matches, increase contributions gradually, and diversify across asset classes.",
                "metadata": {"topic": "retirement", "category": "investing"}
            },
            
            # Debt Management
            {
                "text": "For credit card debt: Create a debt repayment plan, prioritize high-interest debt first, consider balance transfer options, and avoid taking on new debt while paying off existing debt.",
                "metadata": {"topic": "credit_card_debt", "category": "debt"}
            },
            {
                "text": "For student loan management: Understand your repayment options, consider income-driven repayment plans, explore loan consolidation, and look into loan forgiveness programs if eligible.",
                "metadata": {"topic": "student_loans", "category": "debt"}
            },
            
            # Real Estate
            {
                "text": "For buying a house: Save for a 20% down payment, check your credit score, get pre-approved for a mortgage, compare multiple lenders, and consider all associated costs beyond the purchase price.",
                "metadata": {"topic": "home_buying", "category": "real_estate"}
            },
            {
                "text": "For mortgage management: Choose between fixed and adjustable rates based on your timeline, understand closing costs, consider refinancing when rates drop, and make extra payments when possible.",
                "metadata": {"topic": "mortgage", "category": "real_estate"}
            },
            
            # Tax Planning
            {
                "text": "For tax optimization: Maximize tax-advantaged accounts, keep track of deductible expenses, consider tax-loss harvesting, and plan charitable contributions strategically.",
                "metadata": {"topic": "tax_planning", "category": "taxes"}
            },
            
            # Insurance
            {
                "text": "For insurance planning: Get adequate health insurance coverage, consider term life insurance if you have dependents, maintain appropriate property insurance, and review coverage annually.",
                "metadata": {"topic": "insurance", "category": "protection"}
            },
            
            # Business and Entrepreneurship
            {
                "text": "For starting a business: Create a detailed business plan, estimate startup costs, understand legal requirements, build an emergency fund, and consider starting as a side business first.",
                "metadata": {"topic": "business_startup", "category": "entrepreneurship"}
            }
        ]
    
    @staticmethod
    def get_advice_by_category(category: str) -> List[Dict[str, Any]]:
        all_advice = FinancialKnowledgeBase.get_initial_advice()
        return [advice for advice in all_advice if advice["metadata"]["category"] == category]
    
    @staticmethod
    def get_advice_by_topic(topic: str) -> List[Dict[str, Any]]:
        all_advice = FinancialKnowledgeBase.get_initial_advice()
        return [advice for advice in all_advice if advice["metadata"]["topic"] == topic] 