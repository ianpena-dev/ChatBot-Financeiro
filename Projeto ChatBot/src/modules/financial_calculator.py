"""
Financial Calculator Module
Provides financial calculation functions for the chatbot
"""

import math
from typing import Dict, Optional


class FinancialCalculator:
    """Core financial calculations"""
    
    @staticmethod
    def compound_interest(principal: float, rate: float, time: float, frequency: str = "annual") -> Dict:
        """
        Calculate compound interest
        
        Args:
            principal: Initial amount
            rate: Annual interest rate (decimal, e.g., 0.05 for 5%)
            time: Time in years
            frequency: Compounding frequency ('annual', 'semi-annual', 'quarterly', 'monthly')
        
        Returns:
            Dictionary with calculation results
        """
        freq_map = {
            'annual': 1,
            'semi-annual': 2,
            'quarterly': 4,
            'monthly': 12
        }
        
        n = freq_map.get(frequency, 1)
        amount = principal * (1 + rate/n)**(n*time)
        interest_earned = amount - principal
        
        return {
            'principal': principal,
            'final_amount': round(amount, 2),
            'interest_earned': round(interest_earned, 2),
            'rate': rate * 100,
            'time_years': time,
            'frequency': frequency,
            'effective_rate': ((1 + rate/n)**n - 1) * 100
        }
    
    @staticmethod
    def simple_interest(principal: float, rate: float, time: float) -> Dict:
        """
        Calculate simple interest
        
        Args:
            principal: Initial amount
            rate: Annual interest rate (decimal)
            time: Time in years
        
        Returns:
            Dictionary with calculation results
        """
        interest = principal * rate * time
        total = principal + interest
        
        return {
            'principal': principal,
            'interest': round(interest, 2),
            'total': round(total, 2),
            'rate': rate * 100,
            'time_years': time
        }
    
    @staticmethod
    def loan_payment(principal: float, annual_rate: float, years: int) -> Dict:
        """
        Calculate loan monthly payment (amortization)
        
        Args:
            principal: Loan amount
            annual_rate: Annual interest rate (decimal)
            years: Loan term in years
        
        Returns:
            Dictionary with calculation results
        """
        monthly_rate = annual_rate / 12
        num_payments = years * 12
        
        if monthly_rate == 0:
            monthly_payment = principal / num_payments
        else:
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        
        total_payment = monthly_payment * num_payments
        total_interest = total_payment - principal
        
        return {
            'principal': principal,
            'monthly_payment': round(monthly_payment, 2),
            'total_payment': round(total_payment, 2),
            'total_interest': round(total_interest, 2),
            'annual_rate': annual_rate * 100,
            'term_years': years,
            'num_payments': num_payments
        }
    
    @staticmethod
    def present_value(future_value: float, rate: float, time: float) -> Dict:
        """
        Calculate present value
        
        Args:
            future_value: Future amount
            rate: Discount rate (decimal)
            time: Time in years
        
        Returns:
            Dictionary with calculation results
        """
        pv = future_value / (1 + rate)**time
        
        return {
            'future_value': future_value,
            'present_value': round(pv, 2),
            'discount_rate': rate * 100,
            'time_years': time
        }
    
    @staticmethod
    def future_value(present_value: float, rate: float, time: float) -> Dict:
        """
        Calculate future value
        
        Args:
            present_value: Current amount
            rate: Interest rate (decimal)
            time: Time in years
        
        Returns:
            Dictionary with calculation results
        """
        fv = present_value * (1 + rate)**time
        
        return {
            'present_value': present_value,
            'future_value': round(fv, 2),
            'interest_rate': rate * 100,
            'time_years': time
        }
    
    @staticmethod
    def roi(investment: float, return_value: float) -> Dict:
        """
        Calculate Return on Investment
        
        Args:
            investment: Amount invested
            return_value: Value returned
        
        Returns:
            Dictionary with calculation results
        """
        profit = return_value - investment
        roi_percentage = (profit / investment) * 100
        
        return {
            'investment': investment,
            'return_value': return_value,
            'profit': round(profit, 2),
            'roi_percentage': round(roi_percentage, 2)
        }
    
    @staticmethod
    def inflation_adjusted(amount: float, inflation_rate: float, years: int) -> Dict:
        """
        Calculate inflation-adjusted value
        
        Args:
            amount: Current amount
            inflation_rate: Annual inflation rate (decimal)
            years: Number of years
        
        Returns:
            Dictionary with calculation results
        """
        future_purchasing_power = amount / (1 + inflation_rate)**years
        
        return {
            'current_amount': amount,
            'inflation_rate': inflation_rate * 100,
            'years': years,
            'future_purchasing_power': round(future_purchasing_power, 2),
            'purchasing_power_loss': round(amount - future_purchasing_power, 2)
        }
    
    @staticmethod
    def savings_goal(goal_amount: float, monthly_contribution: float, annual_rate: float, years: int) -> Dict:
        """
        Calculate if savings goal is achievable
        
        Args:
            goal_amount: Target amount
            monthly_contribution: Monthly savings
            annual_rate: Annual interest rate (decimal)
            years: Time to reach goal
        
        Returns:
            Dictionary with calculation results
        """
        monthly_rate = annual_rate / 12
        num_months = years * 12
        
        if monthly_rate == 0:
            future_value = monthly_contribution * num_months
        else:
            future_value = monthly_contribution * ((1 + monthly_rate)**num_months - 1) / monthly_rate
        
        difference = future_value - goal_amount
        
        return {
            'goal_amount': goal_amount,
            'monthly_contribution': monthly_contribution,
            'projected_savings': round(future_value, 2),
            'difference': round(difference, 2),
            'goal_achievable': difference >= 0,
            'annual_rate': annual_rate * 100,
            'years': years
        }
    
    @staticmethod
    def debt_to_income(monthly_debt_payments: float, monthly_gross_income: float) -> Dict:
        """
        Calculate debt-to-income ratio
        
        Args:
            monthly_debt_payments: Total monthly debt payments
            monthly_gross_income: Monthly gross income
        
        Returns:
            Dictionary with calculation results
        """
        dti_ratio = (monthly_debt_payments / monthly_gross_income) * 100
        
        # DTI assessment
        if dti_ratio <= 20:
            assessment = "Excelente - Saúde financeira ótima"
        elif dti_ratio <= 36:
            assessment = "Bom - Dentro do limite aceitável"
        elif dti_ratio <= 43:
            assessment = "Atenção - Limite máximo recomendado"
        else:
            assessment = "Crítico - Risco financeiro elevado"
        
        return {
            'monthly_debt_payments': monthly_debt_payments,
            'monthly_gross_income': monthly_gross_income,
            'dti_ratio': round(dti_ratio, 2),
            'assessment': assessment
        }
