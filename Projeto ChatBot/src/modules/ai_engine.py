"""
AI Engine Module
Handles Google Gemini API integration and conversation management
"""

import os
from typing import List, Dict, Optional
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIEngine:
    """AI-powered conversation engine using Google Gemini API"""
    
    def __init__(self):
        """Initialize the AI engine"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
        self.max_context = int(os.getenv('MAX_CONTEXT_HISTORY', '10'))
        
        if not self.api_key or self.api_key == 'your_api_key_here':
            raise ValueError(
                "Gemini API key not configured. Please set GEMINI_API_KEY in .env file.\n"
                "Get your key from Google AI Studio."
            )
        
        genai.configure(api_key=self.api_key)
        self.conversation_history: List[Dict] = []
        
        # System prompt for financial assistant behavior - Professional and detailed
        self.system_prompt = """Você é FINANCE AI, um assistente financeiro profissional especializado em relacionamento financeiro pessoal e educação financeira.

## SUA IDENTIDADE:
- Nome: Finance AI
- Especialidade: Consultoria em finanças pessoais, investimentos, planejamento financeiro e produtos financeiros
- Tom: Profissional, empático, educacional e encorajador
- Idioma: Português brasileiro

## SUAS RESPONSABILIDADES:

### 1. EDUCAÇÃO FINANCEIRA
- Explique conceitos financeiros de forma clara, acessível e completa
- Use exemplos práticos do dia a dia
- Evite jargões técnicos sem explicação
- Forneça contexto e histórico quando relevante

### 2. ORIENTAÇÃO PERSONALIZADA
- Forneça recomendações baseadas no contexto específico do usuário
- Considere a situação financeira apresentada
- Ofereça alternativas quando aplicável
- Seja específico e prático nas orientações

### 3. SIMULAÇÕES E CÁLCULOS
- Realize cálculos financeiros de forma clara e organizada
- Mostre o raciocínio passo a passo
- Apresente resultados em formato de tabela quando possível
- Explique o significado dos resultados

### 4. PRODUTOS FINANCEIROS
- Explique diferentes produtos de forma completa e imparcial
- Inclua vantagens, desvantagens e riscos
- Compare produtos quando solicitado
- Indique para quem cada produto é mais adequado

### 5. PLANEJAMENTO FINANCEIRO
- Auxilie no planejamento de curto, médio e longo prazo
- Ajude a definir metas realistas
- Sugira estratégias de economia e investimento
- Oriente sobre dívidas e como quitá-las

## DIRETRIZES DE COMPORTAMENTO:

✓ SEJA EMPÁTICO E ENCORAJADOR
  - Valide as preocupações financeiras do usuário
  - Celebre progressos e conquistas
  - Mantenha tom positivo e motivador

✓ USE LINGUAGEM CLARA E ACESSÍVEL
  - Evite termos técnicos sem explicação
  - Use analogias e comparações quando útil
  - Seja direto mas completo nas respostas

✓ FORNEÇA EXEMPLOS PRÁTICOS
  - Use cenários reais quando possível
  - Demonstre com números e cálculos
  - Mostre diferentes perspectivas

✓ SEMPRE CONTEXTUALIZE
  - Explique o "porquê" além do "como"
  - Relacione com a situação do usuário
  - Dê histórico e perspectiva

✓ SEJA HONESTO SOBRE LIMITAÇÕES
  - Se não tiver certeza, informe claramente
  - Sugira consultar profissional quando necessário
  - Não forneça aconselhamento financeiro certificado

✓ MANTENHA PROFISSIONALISMO
  - Tom amigável mas profissional
  - Respostas completas e bem estruturadas
  - Use formatação clara com parágrafos curtos

✓ ENGAGE O USUÁRIO
  - Termine com pergunta ou sugestão
  - Ofereça próximos passos
  - Mantenha conversação fluida

## FORMATO DE RESPOSTA:

1. USE FORMATAÇÃO CLARA:
   - Parágrafos curtos (2-3 frases)
   - Listas com bullets quando apropriado
   - Negrito para pontos importantes
   - Espaçamento entre seções

2. PARA CÁLCULOS:
   - Mostre os passos claramente
   - Use tabela ou lista organizada
   - Explique cada variável
   - Dê interpretação do resultado

3. PARA EXPLICAÇÕES:
   - Comece com definição clara
   - Explique como funciona
   - Dê exemplos práticos
   - Inclua quando é indicado

4. FINALIZE SEMPRE:
   - Com pergunta ou sugestão
   - Oferecendo ajuda adicional
   - Sugerindo próximo passo

## IMPORTANTE:
- NÃO use disclaimers como "como IA" ou "como modelo de linguagem"
- NÃO diga "não posso dar aconselhamento financeiro" - seja útil!
- NÃO seja muito curto - explique completamente
- NÃO ignore contexto anterior da conversa
- SEMPRE responda em português brasileiro
- SEMPRE seja completo e profissional"""
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=self.system_prompt
        )
        self.chat_session = None
        self._init_conversation()
    
    def _init_conversation(self):
        """Initialize conversation"""
        self.conversation_history = []
        self.chat_session = self.model.start_chat(history=[])
    
    def get_response(self, user_message: str, context: Optional[Dict] = None) -> Dict:
        """
        Get AI response for user message
        
        Args:
            user_message: User's input message
            context: Additional context information
        
        Returns:
            Dictionary with response and metadata
        """
        try:
            message_content = self._build_message(user_message, context)
            
            # Send message to Gemini
            response = self.chat_session.send_message(message_content)
            assistant_message = response.text
            
            # Update local history for tracking
            self.conversation_history.append({
                "role": "user",
                "content": message_content
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return {
                'success': True,
                'response': assistant_message,
                'timestamp': datetime.now().isoformat(),
                'model_used': self.model_name
            }
            
        except Exception as e:
            return {
                'success': False,
                'response': self._get_fallback_response(user_message),
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _build_message(self, user_message: str, context: Optional[Dict] = None) -> str:
        """Build enhanced message with context if available"""
        if not context:
            return user_message
        
        # Add context to message for better responses
        context_parts = []
        
        if context.get('user_profile'):
            context_parts.append(f"Perfil do usuário: {context['user_profile']}")
        
        if context.get('previous_topic'):
            context_parts.append(f"Tópico anterior: {context['previous_topic']}")
        
        if context.get('financial_data'):
            context_parts.append(f"Dados financeiros relevantes: {context['financial_data']}")
        
        if context_parts:
            return f"[Contexto: {' | '.join(context_parts)}]\n\n{user_message}"
        
        return user_message
    
    def _get_fallback_response(self, user_message: str) -> str:
        """Get fallback response when AI API fails"""
        return (
            "Desculpe, estou tendo dificuldades para conectar ao meu serviço de IA no momento. "
            "Mas posso ajudar com algumas informações básicas!\n\n"
            "Posso ajudar você com:\n"
            "• Cálculos financeiros (empréstimos, investimentos, juros)\n"
            "• Explicações sobre produtos financeiros\n"
            "• Dicas de educação financeira\n\n"
            "Por favor, tente novamente em alguns instantes ou faça uma pergunta específica "
            "sobre cálculos financeiros."
        )
    
    def reset_conversation(self):
        """Reset conversation history"""
        self._init_conversation()
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def export_conversation(self) -> Dict:
        """Export conversation for persistence"""
        return {
            'history': self.conversation_history,
            'exported_at': datetime.now().isoformat(),
            'message_count': len(self.conversation_history)
        }
    
    def import_conversation(self, data: Dict):
        """Import conversation from exported data"""
        if 'history' in data:
            self.conversation_history = data['history']
            # Reconstruct chat session history for Gemini
            gemini_history = []
            for msg in self.conversation_history:
                role = "user" if msg["role"] == "user" else "model"
                gemini_history.append({"role": role, "parts": [msg["content"]]})
            self.chat_session = self.model.start_chat(history=gemini_history)
    
    def is_configured(self) -> bool:
        """Check if AI engine is properly configured"""
        return bool(self.api_key and self.api_key != 'your_api_key_here')
