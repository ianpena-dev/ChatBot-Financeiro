#!/usr/bin/env python3
"""
Financial Relationship Chatbot - Main Application
An AI-powered chatbot for financial relationship experiences
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.modules.chatbot_engine import FinancialChatbot


def main():
    """Main application entry point"""
    print("\n" + "="*70)
    print("  💰 ASSISTENTE FINANCEIRO PESSOAL - IA")
    print("="*70 + "\n")
    
    try:
        # Create and start chatbot
        chatbot = FinancialChatbot()
        chatbot.start()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Chatbot encerrado pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        print("\nVerifique:")
        print("  • Se as dependências estão instaladas: pip install -r requirements.txt")
        print("  • Se o arquivo .env está configurado corretamente")
        print("  • Se a API key do OpenAI está válida")
        sys.exit(1)


if __name__ == '__main__':
    main()
