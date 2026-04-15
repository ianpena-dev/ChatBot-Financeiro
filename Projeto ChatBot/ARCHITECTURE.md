# 🏗️ Arquitetura do Chatbot Financeiro

## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                               │
│                   (Ponto de Entrada)                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              src/modules/chatbot_engine.py                   │
│                 (Motor Principal)                            │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Processar    │→ │ Detectar     │→ │ Gerar        │      │
│  │ Mensagem     │  │ Intenção     │  │ Resposta     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────┬─────────────┬─────────────┬────────────────────────┘
         │             │             │
         ▼             ▼             ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│    NLU       │ │  Financial   │ │   AI Engine  │
│ (Compreensão │ │  Calculator  │ │  (OpenAI)    │
│  Linguagem)  │ │  (Cálculos)  │ │  (Opcional)  │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Detectar:    │ │ - Juros      │ │ - GPT-4o     │
│ - Intenção   │ │ - Empréstimo │ │ - Contexto   │
│ - Contexto   │ │ - Investim.  │ │ - Respostas  │
│ - Dados      │ │ - ROI        │ │   naturais   │
└──────────────┘ │ - Metas      │ └──────────────┘
                 └──────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────┐
│           src/modules/financial_products.py              │
│              (Base de Produtos Financeiros)               │
│                                                          │
│  CDB | Tesouro | Poupança | Consórcio | Seguros         │
│  Previdência | Crédito | Fundos | Ações                  │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│            src/utils/context_manager.py                   │
│              (Persistência - SQLite)                      │
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐        │
│  │ Sessions   │  │ Conversas  │  │ Perfis     │        │
│  │ Tabela     │  │ Tabela     │  │ Tabela     │        │
│  └────────────┘  └────────────┘  └────────────┘        │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│               src/ui/chat_interface.py                    │
│              (Interface do Usuário - Rich)                │
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐        │
│  │ Mensagens  │  │ Resultados │  │ Comandos   │        │
│  │ Formatadas │  │ Financeiros│  │ Ajuda, etc │        │
│  └────────────┘  └────────────┘  └────────────┘        │
└──────────────────────────────────────────────────────────┘
```

## Fluxo de Dados

### 1. Entrada do Usuário
```
Usuário digita: "Quanto rende R$ 10000 a 10% ao ano?"
```

### 2. Processamento NLU
```
NLU detecta:
  - Intenção: investment_calculation (confiança: 0.9)
  - Valores monetários: [10000.0]
  - Percentuais: [0.10]
  - Período: anos: [1]
```

### 3. Tentativa de Resposta Local
```
Chatbot verifica:
  ✓ Intent = investment_calculation
  ✓ Dados financeiros disponíveis
  → Usa FinancialCalculator.compound_interest()
```

### 4. Cálculo Financeiro
```python
FinancialCalculator.compound_interest(
    principal=10000,
    rate=0.10,
    time=1
)
→ Result: {
    'final_amount': 11000.00,
    'interest_earned': 1000.00,
    ...
}
```

### 5. Exibição Formatada
```
UI mostra:
┌─────────────────────────────────┐
│ 📊 Resultado do Cálculo         │
│                                 │
│ • Principal: R$ 10,000.00      │
│ • Montante Final: R$ 11,000.00 │
│ • Juros Ganhos: R$ 1,000.00    │
│ • Taxa: 10.00%                  │
│ • Tempo: 1 ano                  │
└─────────────────────────────────┘
```

### 6. Persistência
```
ContextManager salva:
  - Mensagem do usuário
  - Resposta do assistente
  - Intenção detectada
  - Contexto extraído
  - Timestamp
```

## Camadas da Arquitetura

### Presentation Layer (UI)
- **ChatInterface**: Console rich formatting
- **Painéis coloridos**: User (verde), Assistant (azul)
- **Resultados financeiros**: Formatação especial
- **Markdown**: Explicações formatadas

### Business Logic Layer (Modules)
- **ChatbotEngine**: Orquestrador principal
- **NLU**: Compreensão de linguagem natural
- **FinancialCalculator**: Cálculos matemáticos
- **FinancialProducts**: Base de conhecimento
- **AIEngine**: Integração OpenAI (opcional)

### Data Access Layer (Utils)
- **ContextManager**: SQLite persistence
- **Sessões**: Controle de conversas
- **Perfis**: Dados do usuário
- **Metas**: Objetivos financeiros

## Módulos e Responsabilidades

### src/modules/

| Módulo | Responsabilidade |
|--------|------------------|
| `chatbot_engine.py` | Orquestra todos os módulos |
| `ai_engine.py` | Integração OpenAI API |
| `nlu.py` | Detecção de intenção e contexto |
| `financial_calculator.py` | Cálculos matemáticos |
| `financial_products.py` | Base de produtos |

### src/utils/

| Módulo | Responsabilidade |
|--------|------------------|
| `context_manager.py` | Persistência SQLite |

### src/ui/

| Módulo | Responsabilidade |
|--------|------------------|
| `chat_interface.py` | Interface do usuário |

## Modos de Operação

### Modo 1: Com IA OpenAI (Recomendado)
```
Usuário → NLU → AI Engine → Resposta natural
                  ↓
           Context + Cálculos
```

### Modo 2: Offline (Sem API)
```
Usuário → NLU → Financial Calculator/Products → Resposta
```

## Segurança

- ✅ API key no `.env` (não versionado)
- ✅ SQLite local (sem dados na nuvem)
- ✅ Sem exposição de dados sensíveis
- ✅ Fallback graceful sem API

## Escalabilidade

### Futuras Melhorias:
- [ ] API REST (FastAPI)
- [ ] Interface Web (Streamlit)
- [ ] Múltiplos provedores de IA
- [ ] Cache de respostas
- [ ] Redis para sessões
- [ ] PostgreSQL para dados
- [ ] Webhooks para notificações

## Dependências

```
rich >= 13.7.1         → UI formatting
colorama >= 0.4.6      → Cores no console
openai >= 1.12.0       → IA generativa
python-dotenv >= 1.0.1 → Configuração
sqlite3 (built-in)     → Persistência
pytest >= 8.0.2        → Testes
```

## Test Coverage

```
38 testes passando:
  ✅ 17 testes de cálculos financeiros
  ✅  9 testes de produtos financeiros
  ✅ 12 testes de NLU
```

---

**Arquitetura modular e escalável para um chatbot financeiro inteligente! 🚀**
