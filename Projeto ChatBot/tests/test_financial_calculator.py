"""
Tests for Financial Calculator Module
"""

import pytest
from src.modules.financial_calculator import FinancialCalculator


class TestCompoundInterest:
    """Test compound interest calculations"""
    
    def test_basic_compound_interest(self):
        """Test basic compound interest calculation"""
        result = FinancialCalculator.compound_interest(1000, 0.10, 1)
        assert result['final_amount'] == 1100.00
        assert result['interest_earned'] == 100.00
    
    def test_compound_interest_monthly(self):
        """Test compound interest with monthly compounding"""
        result = FinancialCalculator.compound_interest(1000, 0.12, 1, 'monthly')
        assert result['final_amount'] > 1100  # Should be more than annual
        assert result['frequency'] == 'monthly'
    
    def test_compound_interest_long_term(self):
        """Test long-term compound interest"""
        result = FinancialCalculator.compound_interest(10000, 0.10, 10)
        assert result['final_amount'] > 25000  # Should more than double
        assert result['time_years'] == 10


class TestSimpleInterest:
    """Test simple interest calculations"""
    
    def test_basic_simple_interest(self):
        """Test basic simple interest calculation"""
        result = FinancialCalculator.simple_interest(1000, 0.10, 1)
        assert result['interest'] == 100.00
        assert result['total'] == 1100.00
    
    def test_simple_interest_multiple_years(self):
        """Test simple interest for multiple years"""
        result = FinancialCalculator.simple_interest(1000, 0.10, 3)
        assert result['interest'] == 300.00
        assert result['total'] == 1300.00


class TestLoanPayment:
    """Test loan payment calculations"""
    
    def test_basic_loan(self):
        """Test basic loan payment calculation"""
        result = FinancialCalculator.loan_payment(10000, 0.12, 1)
        assert result['monthly_payment'] > 0
        assert result['total_payment'] > 10000
        assert result['total_interest'] > 0
    
    def test_loan_zero_interest(self):
        """Test loan with zero interest"""
        result = FinancialCalculator.loan_payment(12000, 0.0, 1)
        assert result['monthly_payment'] == 1000.00
    
    def test_loan_long_term(self):
        """Test long-term loan"""
        result = FinancialCalculator.loan_payment(100000, 0.09, 30)
        assert result['num_payments'] == 360
        assert result['term_years'] == 30


class TestPresentValue:
    """Test present value calculations"""
    
    def test_basic_present_value(self):
        """Test basic present value calculation"""
        result = FinancialCalculator.present_value(1100, 0.10, 1)
        assert result['present_value'] == 1000.00


class TestFutureValue:
    """Test future value calculations"""
    
    def test_basic_future_value(self):
        """Test basic future value calculation"""
        result = FinancialCalculator.future_value(1000, 0.10, 1)
        assert result['future_value'] == 1100.00


class TestROI:
    """Test ROI calculations"""
    
    def test_positive_roi(self):
        """Test positive return on investment"""
        result = FinancialCalculator.roi(1000, 1500)
        assert result['profit'] == 500.00
        assert result['roi_percentage'] == 50.00
    
    def test_negative_roi(self):
        """Test negative return on investment"""
        result = FinancialCalculator.roi(1000, 800)
        assert result['profit'] == -200.00
        assert result['roi_percentage'] == -20.00


class TestInflationAdjusted:
    """Test inflation-adjusted calculations"""
    
    def test_basic_inflation(self):
        """Test basic inflation adjustment"""
        result = FinancialCalculator.inflation_adjusted(1000, 0.05, 1)
        assert result['future_purchasing_power'] < 1000
        assert result['purchasing_power_loss'] > 0


class TestSavingsGoal:
    """Test savings goal calculations"""
    
    def test_achievable_goal(self):
        """Test achievable savings goal"""
        result = FinancialCalculator.savings_goal(10000, 1000, 0.10, 1)
        assert result['monthly_contribution'] == 1000
    
    def test_goal_projection(self):
        """Test savings goal projection"""
        result = FinancialCalculator.savings_goal(50000, 500, 0.08, 5)
        assert 'projected_savings' in result
        assert 'goal_achievable' in result


class TestDebtToIncome:
    """Test debt-to-income calculations"""
    
    def test_healthy_dti(self):
        """Test healthy debt-to-income ratio"""
        result = FinancialCalculator.debt_to_income(1000, 5000)
        assert result['dti_ratio'] == 20.00
        assert 'Excelente' in result['assessment']
    
    def test_high_dti(self):
        """Test high debt-to-income ratio"""
        result = FinancialCalculator.debt_to_income(3000, 5000)
        assert result['dti_ratio'] == 60.00
        assert 'Crítico' in result['assessment']
