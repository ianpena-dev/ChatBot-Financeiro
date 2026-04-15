"""
Chat Interface Module
Provides a beautiful, user-friendly console interface
"""

import uuid
from datetime import datetime
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.prompt import Prompt
    from rich.rule import Rule
    from rich.box import ROUNDED
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from colorama import init, Fore, Style

# Initialize colorama for Windows
init(autoreset=True)


class ChatInterface:
    """User-friendly chat interface with rich formatting"""
    
    def __init__(self, use_rich: bool = True):
        """
        Initialize chat interface
        
        Args:
            use_rich: Use rich formatting if available
        """
        self.use_rich = use_rich and RICH_AVAILABLE
        self.console = Console() if self.use_rich else None
        self.session_active = False
        self.session_id = None
    
    def display_welcome(self):
        """Display welcome message"""
        if self.use_rich:
            welcome_text = """
# 💰 Bem-vindo ao seu Assistente Financeiro Pessoal

Estou aqui para ajudar você a ter um **relacionamento mais saudável** com suas finanças!

## O que posso fazer por você:

• 💵 **Cálculos Financeiros**: Empréstimos, investimentos, juros compostos
• 📊 **Simulações**: Projeções de investimentos e planejamento
• 📚 **Educação Financeira**: Explicar conceitos e produtos financeiros
• 🎯 **Metas Financeiras**: Ajudar a planejar seus objetivos
• 💡 **Orientações**: Dicas personalizadas de gestão financeira

**Como usar**: Basta digitar sua pergunta ou pedido em linguagem natural!
            """
            self.console.print(Panel(
                Markdown(welcome_text),
                title="🤖 Assistente Financeiro IA",
                subtitle="Powered by AI",
                box=ROUNDED,
                border_style="blue",
                padding=(1, 2)
            ))
            self.console.print()
        else:
            print(f"\n{Fore.CYAN}{'='*70}")
            print(f"{Fore.CYAN}🤖  BEM-VINDO AO SEU ASSISTENTE FINANCEIRO PESSOAL")
            print(f"{Fore.CYAN}{'='*70}\n")
            print(f"{Fore.YELLOW}Estou aqui para ajudar você com suas finanças!")
            print(f"{Fore.GREEN}\nPosso ajudar com:")
            print(f"  • Cálculos financeiros (empréstimos, investimentos)")
            print(f"  • Simulações e projeções")
            print(f"  • Educação financeira")
            print(f"  • Planejamento de metas")
            print(f"  • Explicações sobre produtos financeiros\n")
    
    def display_message(self, role: str, message: str, is_markdown: bool = True):
        """
        Display a message with proper formatting
        
        Args:
            role: Message role (user/assistant/system)
            message: Message content
            is_markdown: Format as markdown if using rich
        """
        if self.use_rich:
            if role == 'user':
                self.console.print(Panel(
                    message,
                    title="👤 Você",
                    title_align="left",
                    box=ROUNDED,
                    border_style="green",
                    padding=(0, 1)
                ))
            elif role == 'assistant':
                content = Markdown(message) if is_markdown else message
                self.console.print(Panel(
                    content,
                    title="🤖 Assistente",
                    title_align="left",
                    box=ROUNDED,
                    border_style="blue",
                    padding=(1, 2)
                ))
            elif role == 'system':
                self.console.print(Panel(
                    message,
                    box=ROUNDED,
                    border_style="yellow",
                    padding=(0, 1)
                ))
        else:
            if role == 'user':
                print(f"\n{Fore.GREEN}{'─'*70}")
                print(f"{Fore.GREEN}👤 Você:")
                print(f"{Fore.WHITE}{message}")
            elif role == 'assistant':
                print(f"\n{Fore.BLUE}{'─'*70}")
                print(f"{Fore.BLUE}🤖 Assistente:")
                print(f"{Fore.WHITE}{message}")
    
    def display_financial_result(self, title: str, data: dict):
        """
        Display financial calculation results
        
        Args:
            title: Result title
            data: Calculation results
        """
        if self.use_rich:
            result_text = f"### {title}\n\n"
            for key, value in data.items():
                # Format key labels
                label = key.replace('_', ' ').title()
                
                # Format values
                if isinstance(value, float):
                    if 'rate' in key.lower() or 'percentage' in key.lower():
                        formatted_value = f"{value:.2f}%"
                    elif 'amount' in key.lower() or 'payment' in key.lower() or 'value' in key.lower():
                        formatted_value = f"R$ {value:,.2f}"
                    else:
                        formatted_value = f"{value:.2f}"
                else:
                    formatted_value = value
                
                result_text += f"• **{label}**: {formatted_value}\n"
            
            self.console.print(Panel(
                Markdown(result_text),
                title="📊 Resultado do Cálculo",
                box=ROUNDED,
                border_style="cyan",
                padding=(1, 2)
            ))
        else:
            print(f"\n{Fore.CYAN}{'─'*70}")
            print(f"{Fore.CYAN}📊 {title}")
            print(f"{Fore.CYAN}{'─'*70}")
            for key, value in data.items():
                label = key.replace('_', ' ').title()
                if isinstance(value, float):
                    if 'rate' in key.lower() or 'percentage' in key.lower():
                        formatted_value = f"{value:.2f}%"
                    elif 'amount' in key.lower() or 'payment' in key.lower():
                        formatted_value = f"R$ {value:,.2f}"
                    else:
                        formatted_value = f"{value:.2f}"
                else:
                    formatted_value = value
                print(f"{Fore.WHITE}  {label}: {Fore.YELLOW}{formatted_value}")
    
    def get_user_input(self, prompt: str = "Você: ") -> str:
        """
        Get user input
        
        Args:
            prompt: Input prompt text
        
        Returns:
            User input
        """
        if self.use_rich:
            return Prompt.ask(f"\n{prompt}")
        else:
            try:
                return input(f"\n{Fore.GREEN}{prompt}{Fore.WHITE}")
            except (EOFError, KeyboardInterrupt):
                return 'sair'
    
    def display_separator(self):
        """Display a visual separator"""
        if self.use_rich:
            self.console.print(Rule(style="dim"))
        else:
            print(f"\n{Fore.WHITE}{'─'*70}")
    
    def display_error(self, message: str):
        """Display error message"""
        if self.use_rich:
            self.console.print(Panel(
                f"❌ {message}",
                title="Erro",
                border_style="red",
                padding=(0, 1)
            ))
        else:
            print(f"\n{Fore.RED}❌ Erro: {message}")
    
    def display_success(self, message: str):
        """Display success message"""
        if self.use_rich:
            self.console.print(Panel(
                f"✅ {message}",
                border_style="green",
                padding=(0, 1)
            ))
        else:
            print(f"\n{Fore.GREEN}✅ {message}")
    
    def display_help(self):
        """Display help information"""
        if self.use_rich:
            help_text = """
## 📖 Como usar o Assistente

**Comandos disponíveis:**

• Digite sua pergunta ou pedido normalmente
• `ajuda` - Mostra esta ajuda
• `limpar` - Limpa a conversa
• `exportar` - Exporta a conversa
• `sair` - Encerra o chat

**Exemplos do que você pode perguntar:**

• "Quanto vou ter se investir R$ 1000 por mês a 10% ao ano por 5 anos?"
• "O que é CDB?"
• "Como funciona um empréstimo com juros compostos?"
• "Quero economizar R$ 50000 em 2 anos, quanto devo guardar por mês?"
• "Me explique sobre Tesouro Direto"
            """
            self.console.print(Panel(
                Markdown(help_text),
                title="❓ Ajuda",
                box=ROUNDED,
                border_style="yellow",
                padding=(1, 2)
            ))
        else:
            print(f"\n{Fore.YELLOW}{'='*70}")
            print(f"{Fore.YELLOW}📖 COMO USAR O ASSISTENTE")
            print(f"{Fore.YELLOW}{'='*70}")
            print(f"{Fore.WHITE}\nComandos:")
            print(f"  ajuda    - Mostra esta ajuda")
            print(f"  limpar   - Limpa a conversa")
            print(f"  exportar - Exporta a conversa")
            print(f"  sair     - Encerra o chat")
            print(f"\n{Fore.WHITE}Exemplos:")
            print(f"  • Quanto vou ter se investir R$ 1000 por mês?")
            print(f"  • O que é CDB?")
            print(f"  • Como funciona empréstimo com juros compostos?")
            print(f"  • Quero economizar R$ 50000 em 2 anos\n")
    
    def start_session(self) -> str:
        """
        Start a new chat session
        
        Returns:
            Session ID
        """
        self.session_id = str(uuid.uuid4())
        self.session_active = True
        return self.session_id
    
    def end_session(self):
        """End current chat session"""
        self.session_active = False
        self.session_id = None
    
    def display_goodbye(self):
        """Display goodbye message"""
        if self.use_rich:
            goodbye_text = """
Obrigado por usar o **Assistente Financeiro**! 

Lembre-se: uma boa relação com suas finanças começa com **educação** e **planejamento**.

Volte sempre! 💰✨
            """
            self.console.print(Panel(
                Markdown(goodbye_text),
                box=ROUNDED,
                border_style="green",
                padding=(1, 2)
            ))
        else:
            print(f"\n{Fore.CYAN}{'='*70}")
            print(f"{Fore.CYAN}Obrigado por usar o Assistente Financeiro!")
            print(f"{Fore.WHITE}Volte sempre! 💰")
            print(f"{Fore.CYAN}{'='*70}\n")
