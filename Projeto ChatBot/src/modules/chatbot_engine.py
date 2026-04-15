"""
Main Chatbot Engine
Integrates all modules for complete chatbot functionality
"""

import json
from typing import Dict, Optional
from datetime import datetime

from src.modules.ai_engine import AIEngine
from src.modules.nlu import NaturalLanguageUnderstanding
from src.modules.financial_calculator import FinancialCalculator
from src.modules.financial_products import FinancialProductsDB
from src.utils.context_manager import ContextManager
from src.ui.chat_interface import ChatInterface


class FinancialChatbot:
    """Main chatbot engine that integrates all modules"""
    
    def __init__(self):
        """Initialize all chatbot components"""
        print("🔄 Inicializando Assistente Financeiro...")
        
        # Initialize modules
        try:
            self.ai_engine = AIEngine()
            self.ai_available = self.ai_engine.is_configured()
        except ValueError as e:
            print(f"⚠️  {e}")
            print("   Usando modo offline com cálculos locais.")
            self.ai_engine = None
            self.ai_available = False
        
        self.nlu = NaturalLanguageUnderstanding()
        self.financial_calculator = FinancialCalculator()
        self.products_db = FinancialProductsDB()
        self.context_manager = ContextManager()
        self.ui = ChatInterface()
        
        # Session
        self.session_id = None
        self.user_id = None
        
        print("✅ Assistente Financeiro pronto!\n")
    
    def start(self):
        """Start the chatbot"""
        # Create session
        self.session_id = self.ui.start_session()
        self.context_manager.create_session(self.session_id, self.user_id)
        
        # Display welcome
        self.ui.display_welcome()
        
        # Main conversation loop
        self._conversation_loop()
    
    def _conversation_loop(self):
        """Main conversation loop"""
        while True:
            # Get user input
            user_input = self.ui.get_user_input()
            
            # Check for commands
            if user_input.lower() in ['sair', 'exit', 'quit']:
                break
            
            if user_input.lower() in ['ajuda', 'help', '?']:
                self.ui.display_help()
                continue
            
            if user_input.lower() in ['limpar', 'clear']:
                self._clear_conversation()
                continue
            
            if user_input.lower() in ['exportar', 'export']:
                self._export_conversation()
                continue
            
            if not user_input.strip():
                continue
            
            # Process message
            self._process_message(user_input)
        
        # End session
        self.ui.end_session()
        self.ui.display_goodbye()
    
    def _process_message(self, user_input: str):
        """
        Process user message
        
        Args:
            user_input: User's input message
        """
        # Display user message
        self.ui.display_message('user', user_input)
        
        # Detect intent and extract context
        intent_data = self.nlu.detect_intent(user_input)
        context = self.nlu.extract_context(user_input)
        financial_data = self.nlu.extract_financial_data(user_input)
        
        # Save user message
        self.context_manager.save_message(
            self.session_id, 'user', user_input,
            intent=intent_data['primary_intent'],
            context=context
        )
        
        # Try to handle with local modules first
        response = self._try_local_response(intent_data, context, financial_data, user_input)
        
        # If no local response, use AI
        if not response and self.ai_available:
            ai_response = self.ai_engine.get_response(user_input, context)
            if ai_response['success']:
                response = ai_response['response']
            else:
                response = ai_response.get('response', 'Desculpe, não consegui processar sua solicitação.')
        
        # Fallback if nothing worked
        if not response:
            response = (
                "Posso ajudar você com cálculos financeiros! Tente perguntar:\n"
                "• 'Quanto rende R$ 1000 a 10% ao ano?'\n"
                "• 'Calcular parcela de empréstimo de R$ 10000 em 12 meses'\n"
                "• 'O que é CDB?'\n"
                "• 'Me explique sobre Tesouro Direto'"
            )
        
        # Display response
        self.ui.display_message('assistant', response)
        
        # Save assistant message
        self.context_manager.save_message(
            self.session_id, 'assistant', response
        )
    
    def _try_local_response(self, intent_data: Dict, context: Dict, 
                           financial_data: Optional[Dict], user_input: str) -> Optional[str]:
        """
        Try to generate response using local modules
        
        Args:
            intent_data: Detected intent
            context: Extracted context
            financial_data: Extracted financial data
            user_input: Original user input
        
        Returns:
            Response string or None
        """
        intent = intent_data['primary_intent']
        user_lower = user_input.lower()
        
        # Product explanation
        if intent == 'product_explanation' or context.get('products'):
            products = context.get('products', [])
            if products:
                product_key = products[0]
                return self.products_db.format_product_explanation(product_key)
            
            # Try to search
            search_results = self.products_db.search_products(user_input)
            if search_results:
                response = "Encontrei estes produtos:\n\n"
                for product in search_results:
                    response += f"• **{product['name']}** ({product['category']})\n"
                response += "\nSobre qual gostaria de saber mais?"
                return response
        
        # Loan calculation
        if intent == 'loan_calculation' and financial_data:
            if financial_data.get('principal') and financial_data.get('annual_rate') and financial_data.get('years'):
                result = self.financial_calculator.loan_payment(
                    financial_data['principal'],
                    financial_data['annual_rate'],
                    int(financial_data['years'])
                )
                self.ui.display_financial_result("Simulação de Empréstimo", result)
                return f"Com base nos dados fornecidos, sua parcela mensal seria de **R$ {result['monthly_payment']:,.2f}**."
        
        # Investment calculation
        if intent == 'investment_calculation' and financial_data:
            if financial_data.get('principal') and financial_data.get('annual_rate') and financial_data.get('years'):
                result = self.financial_calculator.compound_interest(
                    financial_data['principal'],
                    financial_data['annual_rate'],
                    financial_data['years']
                )
                self.ui.display_financial_result("Simulação de Investimento", result)
                return f"Seu investimento renderia **R$ {result['interest_earned']:,.2f}**, totalizando **R$ {result['final_amount']:,.2f}**."
        
        # Savings goal
        if intent == 'savings_goal' and financial_data:
            if financial_data.get('principal') and financial_data.get('annual_rate') and financial_data.get('years'):
                # Assuming monthly contribution from context
                monthly_contribution = financial_data.get('principal', 1000)
                result = self.financial_calculator.savings_goal(
                    financial_data.get('goal_amount', 50000),
                    monthly_contribution,
                    financial_data.get('annual_rate', 0.10),
                    int(financial_data.get('years', 2))
                )
                self.ui.display_financial_result("Meta de Economia", result)
                if result['goal_achievable']:
                    return f"Parabéns! Com contribuições mensais, você atingirá sua meta com **R$ {result['difference']:,.2f}** acima do objetivo."
                else:
                    return f"Faltariam **R$ {abs(result['difference']):,.2f}** para atingir sua meta. Considere aumentar as contribuições mensais."
        
        # Greeting
        if intent == 'greeting':
            return (
                "Olá! 👋 Que bom ter você aqui!\n\n"
                "Como posso ajudar com suas finanças hoje? "
                "Posso ajudar com cálculos, explicações sobre produtos financeiros, "
                "ou orientação sobre planejamento financeiro."
            )
        
        # Thanks
        if intent == 'thanks':
            return (
                "Por nada! 😊 Fico feliz em ajudar!\n\n"
                "Se tiver mais alguma dúvida sobre finanças, é só perguntar. "
                "Estou sempre aqui para ajudar!"
            )
        
        # General calculation
        if intent == 'calculation' and financial_data:
            if financial_data.get('principal') and financial_data.get('annual_rate'):
                result = self.financial_calculator.compound_interest(
                    financial_data['principal'],
                    financial_data.get('annual_rate', 0.10),
                    financial_data.get('years', 1)
                )
                self.ui.display_financial_result("Cálculo de Juros Compostos", result)
                return f"Seu rendimento seria de **R$ {result['interest_earned']:,.2f}**."
        
        return None
    
    def _clear_conversation(self):
        """Clear current conversation"""
        if self.ai_engine:
            self.ai_engine.reset_conversation()
        self.ui.display_success("Conversa limpa! Vamos começar de novo.")
        
        # Create new session
        self.session_id = self.ui.start_session()
        self.context_manager.create_session(self.session_id, self.user_id)
    
    def _export_conversation(self):
        """Export current conversation"""
        if self.session_id:
            export_data = self.context_manager.export_session(self.session_id)
            filename = f"conversa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            self.ui.display_success(f"Conversa exportada como {filename}")
