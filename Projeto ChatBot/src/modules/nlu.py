"""
Natural Language Understanding Module
Handles intent detection and context extraction
"""

import re
from typing import Dict, List, Optional


class NaturalLanguageUnderstanding:
    """Process and understand user input"""
    
    def __init__(self):
        """Initialize NLU module"""
        # Intent patterns - order matters for priority
        self.intent_patterns = {
            'greeting': [
                r'^oi$', r'^olá$', r'^bom dia', r'^boa tarde',
                r'^boa noite', r'^hello', r'^hey'
            ],
            'thanks': [
                r'obrigad', r'valeu', r'agradeç', r'thanks'
            ],
            'product_explanation': [
                r'o que é', r'o que significa', r'como funciona',
                r'explique', r'explicar', r'definição', r'conceito',
                r'tipos de', 'tipos de'
            ],
            'loan_calculation': [
                r'empréstimo', r'financiamento', r'parcela', r'prestação',
                r'calcular.*parcela', r'quanto.*parcela', r'simulação.*empréstimo'
            ],
            'investment_calculation': [
                r'investiment', r'rendiment', r'juros', r'aplicação',
                r'poupança', r'cdb', r'tesouro', r'fundos', r'ação',
                r'como.*investir', r'onde.*investir', r'renda.*fixa'
            ],
            'savings_goal': [
                r'economizar', r'poupar', r'guardar dinheiro',
                r'objetivo.*financeiro', r'meta.*financeira',
                r'como.*economizar', r'plano.*economia'
            ],
            'debt_management': [
                r'dívida', r'dividado', r'negociar', r'refinanciar',
                r'consolidação', r'limpar nome', r'spc', r'serasa'
            ],
            'budget_planning': [
                r'orçamento', r'planejamento', r'organizar.*finanças',
                r'controlar.*gastos', r'planilha', r'gestão.*financeira'
            ],
            'calculation': [
                r'calcul', r'quanto.*vai dar', r'simulação',
                r'projeção', r'estimativa', r'juros compostos'
            ]
        }
        
        # Financial product keywords
        self.product_keywords = {
            'cdb': r'\bcdb\b',
            'tesouro_direto': r'tesouro.*direto',
            'poupanca': r'\bpoupança\b',
            'consorcio': r'\bconsórcio\b',
            'seguro': r'\bseguro\b',
            'previdencia': r'\bprevidência\b',
            'credito_imobiliario': r'crédito.*imobiliário|financiamento.*imóvel',
            'cartao_credito': r'cartão.*crédito',
            'conta_digital': r'conta.*digital',
            'fundo_investimento': r'fundo.*investimento'
        }
    
    def detect_intent(self, message: str) -> Dict:
        """
        Detect user intent from message
        
        Args:
            message: User message
        
        Returns:
            Dictionary with detected intent and confidence
        """
        message_lower = message.lower()
        intents_found = []
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    intents_found.append(intent)
                    break
        
        # Determine primary intent
        if intents_found:
            primary_intent = intents_found[0]
            confidence = min(0.9, 0.5 + (len(intents_found) * 0.1))
        else:
            primary_intent = 'general_conversation'
            confidence = 0.5
        
        return {
            'primary_intent': primary_intent,
            'all_intents': intents_found,
            'confidence': confidence
        }
    
    def extract_context(self, message: str) -> Dict:
        """
        Extract contextual information from message
        
        Args:
            message: User message
        
        Returns:
            Dictionary with extracted context
        """
        context = {}
        message_lower = message.lower()
        
        # Extract monetary values
        money_pattern = r'R?\$?\s*(\d+[.,]?\d*)\s*(mil|milhão|bilhão)?'
        money_matches = re.findall(money_pattern, message_lower)
        if money_matches:
            context['monetary_values'] = [
                float(value.replace(',', '.')) for value, _ in money_matches
            ]
        
        # Extract percentages
        percent_pattern = r'(\d+[.,]?\d*)\s*%'
        percent_matches = re.findall(percent_pattern, message_lower)
        if percent_matches:
            context['percentages'] = [
                float(p.replace(',', '.')) / 100 for p in percent_matches
            ]
        
        # Extract time periods
        time_patterns = {
            'months': r'(\d+)\s*(meses|mês)',
            'years': r'(\d+)\s*(anos|ano)',
            'days': r'(\d+)\s*(dias|dia)'
        }
        
        for time_unit, pattern in time_patterns.items():
            matches = re.findall(pattern, message_lower)
            if matches:
                # Handle tuple matches from groups
                context[time_unit] = [int(m[0] if isinstance(m, tuple) else m) for m in matches]
        
        # Detect financial products mentioned
        products_mentioned = []
        for product, pattern in self.product_keywords.items():
            if re.search(pattern, message_lower):
                products_mentioned.append(product)
        
        if products_mentioned:
            context['products'] = products_mentioned
        
        # Detect question
        if '?' in message or message_lower.startswith(('como', 'o que', 'qual', 'quando', 'onde', 'por que')):
            context['is_question'] = True
        
        return context
    
    def extract_financial_data(self, message: str) -> Optional[Dict]:
        """
        Extract specific financial data for calculations
        
        Args:
            message: User message
        
        Returns:
            Dictionary with extracted financial data
        """
        data = {}
        message_lower = message.lower()
        
        # Extract principal/amount
        principal_patterns = [
            r'(?:de|um|em)\s*R?\$?\s*(\d+[.,]?\d*)\s*(?:mil|milhão)?',
            r'R?\$?\s*(\d+[.,]?\d*)\s*(?:mil|milhão)?\s*(?:para|em|investir|aplicar)',
            r'(?:valor|montante|quantia)\s*(?:de\s*)?R?\$?\s*(\d+[.,]?\d*)',
            r'(?:investir|aplicar)\s*R?\$?\s*(\d+[.,]?\d*)'
        ]
        
        for pattern in principal_patterns:
            match = re.search(pattern, message_lower)
            if match:
                value = match.group(1).replace(',', '.')
                data['principal'] = float(value)
                break
        
        # Extract interest rate
        rate_match = re.search(r'(\d+[.,]?\d*)\s*%\s*(?:ao\s*(?:mês|ano|a\.m\.|a\.a\.))', message_lower)
        if rate_match:
            rate_value = float(rate_match.group(1).replace(',', '.'))
            # Check if monthly or annual
            if 'mês' in message_lower or 'a.m' in message_lower:
                data['monthly_rate'] = rate_value / 100
            else:
                data['annual_rate'] = rate_value / 100
        
        # Extract time period
        time_match = re.search(r'(\d+)\s*(?:meses|anos)', message_lower)
        if time_match:
            time_value = int(time_match.group(1))
            if 'meses' in message_lower:
                data['months'] = time_value
                data['years'] = time_value / 12
            else:
                data['years'] = time_value
                data['months'] = time_value * 12
        
        return data if data else None
    
    def format_context_summary(self, context: Dict) -> str:
        """
        Format context for AI prompt
        
        Args:
            context: Extracted context
        
        Returns:
            Formatted context string
        """
        parts = []
        
        if context.get('monetary_values'):
            parts.append(f"Valores mencionados: {', '.join([f'R$ {v:.2f}' for v in context['monetary_values']])}")
        
        if context.get('percentages'):
            parts.append(f"Taxas mencionadas: {', '.join([f'{p*100:.1f}%' for p in context['percentages']])}")
        
        if context.get('products'):
            parts.append(f"Produtos mencionados: {', '.join(context['products'])}")
        
        if context.get('is_question'):
            parts.append("Tipo: Pergunta")
        
        return ' | '.join(parts)
