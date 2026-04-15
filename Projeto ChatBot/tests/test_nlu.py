"""
Tests for NLU Module
"""

import pytest
from src.modules.nlu import NaturalLanguageUnderstanding


class TestNaturalLanguageUnderstanding:
    """Test NLU functionality"""
    
    def setup_method(self):
        """Setup test instances"""
        self.nlu = NaturalLanguageUnderstanding()
    
    def test_detect_loan_intent(self):
        """Test loan calculation intent detection"""
        message = "Quanto ficaria a parcela de um empréstimo de R$ 10000?"
        intent = self.nlu.detect_intent(message)
        assert intent['primary_intent'] == 'loan_calculation'
        assert intent['confidence'] > 0.5
    
    def test_detect_investment_intent(self):
        """Test investment intent detection"""
        message = "Quanto rende um investimento de R$ 5000?"
        intent = self.nlu.detect_intent(message)
        assert intent['primary_intent'] == 'investment_calculation'
    
    def test_detect_product_intent(self):
        """Test product explanation intent"""
        message = "O que é CDB?"
        intent = self.nlu.detect_intent(message)
        assert intent['primary_intent'] == 'product_explanation'
    
    def test_detect_greeting(self):
        """Test greeting detection"""
        message = "Olá"
        intent = self.nlu.detect_intent(message)
        assert intent['primary_intent'] == 'greeting'
    
    def test_detect_thanks(self):
        """Test thanks detection"""
        message = "Obrigado pela ajuda"
        intent = self.nlu.detect_intent(message)
        assert intent['primary_intent'] == 'thanks'
    
    def test_extract_monetary_values(self):
        """Test monetary value extraction"""
        message = "Quero investir R$ 10000"
        context = self.nlu.extract_context(message)
        assert 'monetary_values' in context
        assert 10000.0 in context['monetary_values']
    
    def test_extract_percentages(self):
        """Test percentage extraction"""
        message = "A taxa é de 10% ao ano"
        context = self.nlu.extract_context(message)
        assert 'percentages' in context
        assert 0.10 in context['percentages']
    
    def test_extract_time_periods(self):
        """Test time period extraction"""
        message = "Por 12 meses"
        context = self.nlu.extract_context(message)
        assert 'months' in context
        assert 12 in context['months']
    
    def test_detect_products(self):
        """Test product detection"""
        message = "Quero saber sobre CDB e Tesouro Direto"
        context = self.nlu.extract_context(message)
        assert 'products' in context
        assert 'cdb' in context['products']
    
    def test_detect_question(self):
        """Test question detection"""
        message = "Como funciona o CDB?"
        context = self.nlu.extract_context(message)
        assert context.get('is_question') == True
    
    def test_extract_financial_data(self):
        """Test financial data extraction"""
        message = "Investir R$ 5000 a 10% ao ano por 3 anos"
        data = self.nlu.extract_financial_data(message)
        assert data is not None
        # Should extract rate and time at minimum
        assert 'annual_rate' in data or 'years' in data
    
    def test_context_summary(self):
        """Test context summary formatting"""
        context = {
            'monetary_values': [1000.0, 5000.0],
            'products': ['cdb'],
            'is_question': True
        }
        summary = self.nlu.format_context_summary(context)
        assert 'R$' in summary
        assert 'cdb' in summary.lower()
