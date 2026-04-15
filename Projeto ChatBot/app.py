"""
Financial Chatbot - Vault Theme Web Interface v3.0
Thematic, immersive, and professional chat application using Streamlit Native Chat
Powered by Google Gemini
"""

import os
import uuid
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

# Add project root to path
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.modules.ai_engine import AIEngine
from src.modules.nlu import NaturalLanguageUnderstanding
from src.modules.financial_calculator import FinancialCalculator
from src.modules.financial_products import FinancialProductsDB
from src.utils.context_manager import ContextManager

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Cofre Financeiro AI",
    page_icon="🏦",
    layout="centered"
)

# Custom CSS for the Vault / Safe Theme
st.markdown("""
<style>
    /* Import Fonts: Tech Mono for headings/input, Inter for reading text */
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Inter:wght@400;500;600&display=swap');
    
    /* Global App Background - Dark Metallic Radial */
    .stApp {
        background: radial-gradient(circle at 50% 30%, #2c3e50 0%, #0a0a0a 100%) !important;
        color: #e0e0e0;
    }

    /* Metallic Grid Overlay (Simulating steel plates) */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: 
            linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px) 0 0 / 40px 40px,
            linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px) 0 0 / 40px 40px;
        pointer-events: none;
        z-index: 0;
    }

    /* Hide standard Streamlit header/footer */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Pull content up */
    .stApp > div:first-child {
        margin-top: -2rem;
        z-index: 1;
        position: relative;
    }

    /* Typography */
    h1 {
        font-family: 'Share Tech Mono', monospace !important;
        color: #f1c40f !important; /* Gold */
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 0 0 10px rgba(241, 196, 15, 0.4), 0 2px 4px rgba(0,0,0,0.8);
        border-bottom: 2px solid #34495e;
        padding-bottom: 10px;
        margin-bottom: 0.5rem !important;
    }
    
    h3 {
        font-family: 'Share Tech Mono', monospace !important;
        color: #bdc3c7 !important; /* Silver */
        text-align: center;
        font-size: 1.2rem !important;
        letter-spacing: 1px;
    }
    
    /* Subtitle paragraph */
    .stMarkdown p:first-of-type {
        text-align: center;
        color: #95a5a6;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
    }

    /* Chat Message Containers - Simulating metal boxes */
    [data-testid="stChatMessage"] {
        background: linear-gradient(145deg, #1e272e, #2c3e50) !important;
        border: 1px solid #455a64;
        border-radius: 6px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 
            inset 0 0 15px rgba(0,0,0,0.9), /* Inner depth */
            0 8px 20px rgba(0,0,0,0.6);      /* Outer drop shadow */
        position: relative;
        z-index: 1;
        border-top: 1px solid #7f8c8d; /* Highlight edge */
    }

    /* Rivets on the corners of the chat messages */
    [data-testid="stChatMessage"]::before,
    [data-testid="stChatMessage"]::after {
        content: "";
        position: absolute;
        width: 6px; height: 6px;
        background: radial-gradient(circle, #bdc3c7 0%, #7f8c8d 100%);
        border-radius: 50%;
        box-shadow: inset 0 -1px 1px rgba(0,0,0,0.5), 0 1px 1px rgba(255,255,255,0.2);
    }
    
    [data-testid="stChatMessage"]::before { top: 8px; left: 8px; }
    [data-testid="stChatMessage"]::after { top: 8px; right: 8px; }

    /* Chat Content Text */
    [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] {
        font-family: 'Inter', sans-serif !important;
        color: #ecf0f1 !important;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* Bold text in chat */
    [data-testid="stChatMessage"] strong {
        color: #f1c40f; /* Gold accent for important terms */
    }

    /* User specific avatar background (Green glow) */
    [data-testid="stChatMessageAvatarUser"] {
        background-color: #27ae60 !important;
        box-shadow: 0 0 10px #27ae60;
    }
    
    /* Assistant specific avatar background (Gold glow) */
    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #f39c12 !important;
        box-shadow: 0 0 10px #f39c12;
    }

    /* Remove white background from the bottom chat container */
    [data-testid="stBottomBlockContainer"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottom"] {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* Chat Input Area */
    [data-testid="stChatInput"] {
        background: #111418 !important;
        border: 2px solid #34495e !important;
        border-radius: 4px !important;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.8), 0 0 15px rgba(0,0,0,0.5) !important;
        padding-right: 1rem;
    }
    
    /* Input text field */
    [data-testid="stChatInput"] textarea {
        color: #2ecc71 !important; /* Hacker terminal green */
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 1rem;
    }
    
    /* Placeholder text */
    [data-testid="stChatInput"] textarea::placeholder {
        color: #2ecc71 !important;
        opacity: 0.5;
    }

    /* Divider */
    hr {
        border-top: 2px solid #34495e !important;
        border-bottom: 1px solid #111 !important;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)


class ProfessionalChatbot:
    """Professional web chatbot integration"""
    
    def __init__(self):
        try:
            self.ai_engine = AIEngine()
            self.ai_available = self.ai_engine.is_configured()
        except Exception as e:
            self.ai_engine = None
            self.ai_available = False
            st.error(f"Erro de Sistema no Cofre: {e}")
        
        self.nlu = NaturalLanguageUnderstanding()
        self.financial_calculator = FinancialCalculator()
        self.products_db = FinancialProductsDB()
        self.context_manager = ContextManager()
        
        self.session_id = str(uuid.uuid4())
        self.context_manager.create_session(self.session_id)


def get_professional_response(chatbot, user_input):
    """Get professional response from AI or local modules"""
    intent_data = chatbot.nlu.detect_intent(user_input)
    context = chatbot.nlu.extract_context(user_input)
    intent = intent_data['primary_intent']
    
    if chatbot.ai_available:
        ai_response = chatbot.ai_engine.get_response(user_input, context)
        if ai_response['success']:
            return ai_response['response']
        else:
            return ai_response.get('response', "⚠️ Falha de segurança na comunicação com a central de IA.")
            
    # Fallback to local processing if AI is off
    if intent == 'product_explanation' or context.get('products'):
        products = context.get('products', [])
        if products:
            return chatbot.products_db.format_product_explanation(products[0])
            
    if intent == 'greeting':
        return "🛡️ **Acesso Liberado!**\n\nBem-vindo ao **Cofre Financeiro AI**. Sou o guardião das suas finanças e inteligência analítica.\n\nEstou autorizado a ajudar você com:\n\n- Análise de produtos de investimento\n- Simulações e cálculos de rendimento\n- Estratégias blindadas de planejamento financeiro"
        
    return "Comando recebido. Para otimizar seus ativos, posso executar as seguintes rotinas:\n\n- Detalhar ativos financeiros\n- Executar cálculos complexos (empréstimos, juros compostos)\n- Traçar projeções para suas metas\n\nQual é a sua diretriz operacional?"


def main():
    st.markdown("<h1>🏦 COFRE FINANCEIRO AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Terminal de Consultoria Blindada</h3>", unsafe_allow_html=True)
    st.markdown("Acesse inteligência de mercado, simule investimentos e proteja seu patrimônio com análises precisas e seguras.")
    st.divider()
    
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ProfessionalChatbot()
        st.session_state.messages = [
            {"role": "assistant", "content": "🛡️ **Sistema Online.** Bem-vindo ao Cofre Financeiro AI. Como posso auxiliar na proteção e crescimento do seu patrimônio hoje?", "avatar": "🛡️"}
        ]
        
    chatbot = st.session_state.chatbot
    
    # Display chat messages
    for msg in st.session_state.messages:
        # Default avatars
        avatar = msg.get("avatar")
        if not avatar:
            avatar = "🧑‍💻" if msg["role"] == "user" else "🛡️"
            
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            
    # Chat input
    if prompt := st.chat_input(">_ Insira seu comando financeiro..."):
        # Add user message to state and display it
        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "🧑‍💻"})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)
            
        # Get AI response with a loading spinner
        with st.chat_message("assistant", avatar="🛡️"):
            with st.spinner("Descriptografando dados de mercado..."):
                response = get_professional_response(chatbot, prompt)
                st.markdown(response)
                
        # Add bot response to state
        st.session_state.messages.append({"role": "assistant", "content": response, "avatar": "🛡️"})
        
        # Save to DB
        try:
            chatbot.context_manager.save_message(chatbot.session_id, 'user', prompt)
            chatbot.context_manager.save_message(chatbot.session_id, 'assistant', response)
        except:
            pass

if __name__ == "__main__":
    main()
