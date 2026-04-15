# 💰 Assistente Financeiro Pessoal - IA

Um chatbot inteligente para experiências de relacionamento financeiro, potencializado por IA generativa e fundamentado em boas práticas de experiência do usuário.

## 🌟 Features

### 🤖 Inteligência Artificial
- **Compreensão de Linguagem Natural**: Entende perguntas em português brasileiro
- **Respostas Contextualizadas**: IA generativa com contexto financeiro
- **Detecção de Intenção**: Identifica automaticamente o que o usuário precisa
- **Persistência de Contexto**: Mantém histórico e contexto da conversa

### 💵 Cálculos Financeiros
- **Juros Compostos e Simples**: Simulações de investimentos
- **Empréstimos e Financiamentos**: Cálculo de parcelas (SAC/Price)
- **Valor Presente e Futuro**: Projeções financeiras
- **ROI e Metas de Economia**: Planejamento financeiro
- **Relação Dívida/Renda**: Análise de saúde financeira
- **Ajuste por Inflação**: Perda de poder de compra

### 📚 Educação Financeira
- **Produtos Financeiros**: CDB, Tesouro Direto, Poupança, Consórcio, etc.
- **Explicações Detalhadas**: Como funciona, tributação, riscos
- **Dicas e Orientações**: Melhores práticas de gestão financeira

### 💎 UX Premium
- **Interface Rica**: Formatação bonita com Rich/Colorama
- **Formatação Financeira**: Valores em R$, percentuais claros
- **Fluxo Natural**: Conversação em linguagem natural
- **Exportação de Conversas**: Salva suas consultas

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- (Opcional) Chave API OpenAI para IA generativa

### Passo 1: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 2: Configurar API OpenAI (Opcional)

1. Obtenha sua chave API em: https://platform.openai.com/api-keys
2. Copie o arquivo `.env.example` para `.env`:
   ```bash
   copy .env.example .env
   ```
3. Edite o arquivo `.env` e adicione sua chave:
   ```
   OPENAI_API_KEY=sk-your_api_key_here
   ```

**Nota**: O chatbot funciona sem API key (modo offline com cálculos locais), mas com IA fica muito mais poderoso!

## 🎯 Como Usar

### Iniciar o Chatbot

```bash
python main.py
```

### Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `ajuda` | Mostra ajuda completa |
| `limpar` | Limpa a conversa |
| `exportar` | Exporta conversa em JSON |
| `sair` | Encerra o chat |

### Exemplos de Perguntas

#### 💵 Cálculos
- "Quanto rende R$ 10000 a 10% ao ano por 5 anos?"
- "Calcular parcela de empréstimo de R$ 50000 em 48 meses a 9% ao ano"
- "Se eu investir R$ 500 por mês, quanto terei em 10 anos?"

#### 📚 Educação
- "O que é CDB?"
- "Como funciona o Tesouro Direto?"
- "Me explique sobre consórcio"
- "Qual a diferença entre PGBL e VGBL?"

#### 🎯 Planejamento
- "Quero juntar R$ 100000 em 5 anos, quanto guardar por mês?"
- "Como organizar meu orçamento?"
- "Vale a pena pagar antecipado?"

## 📁 Estrutura do Projeto

```
Projeto Chatbot/
├── main.py                     # Ponto de entrada principal
├── requirements.txt            # Dependências Python
├── .env                        # Configurações (não versionar)
├── .env.example                # Template de configurações
├── README.md                   # Este arquivo
├── src/
│   ├── __init__.py
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── ai_engine.py        # Motor de IA (OpenAI)
│   │   ├── nlu.py              # Compreensão de linguagem natural
│   │   ├── financial_calculator.py  # Cálculos financeiros
│   │   ├── financial_products.py    # Base de produtos financeiros
│   │   └── chatbot_engine.py   # Motor principal do chatbot
│   ├── utils/
│   │   ├── __init__.py
│   │   └── context_manager.py  # Persistência de contexto
│   └── ui/
│       ├── __init__.py
│       └── chat_interface.py   # Interface de usuário
├── data/                       # Banco de dados SQLite
└── tests/                      # Testes
```

## 🛠️ Arquitetura

### Módulos Principais

#### 1. AI Engine (`ai_engine.py`)
- Integração com OpenAI GPT-4o-mini
- Gerenciamento de histórico de conversas
- System prompt especializado em finanças
- Fallback para modo offline

#### 2. NLU (`nlu.py`)
- Detecção de intenção do usuário
- Extração de contexto (valores, taxas, períodos)
- Identificação de produtos financeiros mencionados
- Análise de dados financeiros

#### 3. Financial Calculator (`financial_calculator.py`)
- Juros compostos e simples
- Empréstimos (SAC/Price)
- Valor presente/futuro
- ROI e metas de economia
- Ajuste por inflação
- Relação dívida/renda

#### 4. Financial Products (`financial_products.py`)
- Base completa de produtos financeiros
- Explicações detalhadas
- Tributação, riscos, liquidez
- Dicas e comparações

#### 5. Context Manager (`context_manager.py`)
- Persistência SQLite
- Histórico de conversas
- Perfis de usuário
- Metas financeiras
- Exportação de dados

#### 6. Chat Interface (`chat_interface.py`)
- UI rica com Rich/Colorama
- Formatação financeira
- Painéis e markdown
- UX amigável

## 🔧 Personalização

### Adicionar Novos Cálculos

Edite `src/modules/financial_calculator.py`:

```python
@staticmethod
def meu_novo_calculo(param1, param2):
    # Sua lógica aqui
    return resultado
```

### Adicionar Novos Produtos

Edite `src/modules/financial_products.py` e adicione ao dicionário `self.products`:

```python
'novo_produto': {
    'name': 'Nome do Produto',
    'category': 'Categoria',
    'risk_level': 'Nível de Risco',
    'description': 'Descrição...',
    # ... outros campos
}
```

### Customizar System Prompt

Edite `self.system_prompt` em `src/modules/ai_engine.py` para ajustar o comportamento da IA.

## 🧪 Testes

Execute os testes:

```bash
pytest tests/ -v
```

## 📝 Roadmap

- [ ] Interface web (Streamlit/Gradio)
- [ ] Integração com múltiplos provedores de IA
- [ ] Gráficos de projeção financeira
- [ ] Suporte a upload de planilhas
- [ ] API REST
- [ ] Modo assistente avançado
- [ ] Notificações e lembretes
- [ ] Multi-usuário com perfis

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é open-source e disponível para uso educacional e comercial.

## 👥 Suporte

Para dúvidas, sugestões ou reportar bugs:
- Abra uma issue no repositório
- Consulte o README
- Use o comando `ajuda` no chatbot

## 🙏 Agradecimentos

- OpenAI pela API de IA generativa
- Comunidade Python pelas bibliotecas excelentes
- Boa práticas de UX/UI que inspiraram este projeto

---

**Desenvolvido com ❤️ para educação financeira**
