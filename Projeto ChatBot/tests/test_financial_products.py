"""
Tests for Financial Products Database
"""

import pytest
from src.modules.financial_products import FinancialProductsDB


class TestFinancialProductsDB:
    """Test financial products database"""
    
    def setup_method(self):
        """Setup test instances"""
        self.db = FinancialProductsDB()
    
    def test_get_product(self):
        """Test retrieving a product"""
        product = self.db.get_product('cdb')
        assert product is not None
        assert 'name' in product
        assert 'description' in product
    
    def test_get_nonexistent_product(self):
        """Test retrieving a nonexistent product"""
        product = self.db.get_product('nonexistent')
        assert product is None
    
    def test_search_products(self):
        """Test searching products"""
        results = self.db.search_products('CDB')
        assert len(results) > 0
        assert any(r['key'] == 'cdb' for r in results)
    
    def test_search_by_category(self):
        """Test searching by category"""
        results = self.db.search_products('Renda Fixa')
        assert len(results) > 0
    
    def test_get_all_products(self):
        """Test getting all products"""
        all_products = self.db.get_all_products()
        assert len(all_products) > 5  # Should have multiple products
    
    def test_format_product_explanation(self):
        """Test formatting product explanation"""
        explanation = self.db.format_product_explanation('cdb')
        assert len(explanation) > 50
        assert 'CDB' in explanation
    
    def test_format_nonexistent_product(self):
        """Test formatting nonexistent product"""
        explanation = self.db.format_product_explanation('fake_product')
        assert 'não encontrado' in explanation
    
    def test_product_structure(self):
        """Test that products have required fields"""
        for key, product in self.db.products.items():
            assert 'name' in product
            assert 'category' in product
            assert 'risk_level' in product
            assert 'description' in product
    
    def test_specific_products_exist(self):
        """Test that specific products exist"""
        expected_products = ['cdb', 'tesouro_direto', 'poupanca', 'consorcio']
        for product_key in expected_products:
            assert self.db.get_product(product_key) is not None
