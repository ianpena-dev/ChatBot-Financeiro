# 🚀 Guia Rápido de Início

## Instalação e Execução

### 1️⃣ Instalar Dependências

```bash
cd "D:\Programação\Projeto Chatbot"
pip install -r requirements.txt
```

### 2️⃣ (Opcional) Configurar IA OpenAI

Para usar a IA generativa (recomendado):

1. Obtenha sua chave API em: https://platform.openai.com/api-keys
2. Edite o arquivo `.env` e substitua `your_api_key_here` pela sua chave:
   ```
   OPENAI_API_KEY=sk-your_actual_key_here
   ```

**Nota**: O chatbot funciona perfeitamente sem API key! No modo offline, ele usa cálculos locais e explicações de produtos financeiros.

### 3️⃣ Executar o Chatbot

```bash
python main.py
```

## 💡 Exemplos de Uso

### Cálculos Financeiros

```
Você: Quanto rende R$ 10000 a 10% ao ano por 5 anos?

🤖 Assistente: [Mostra simulação completa com juros compostos]
```

```
Você: Calcular parcela de empréstimo de R$ 50000 em 48 meses a 9% ao ano

🤖 Assistente: [Mostra simulação de empréstimo com valor da parcela]
```

### Educação Financeira

```
Você: O que é CDB?

🤖 Assistente: [Explicação completa sobre CDB, incluindo:
  - Como funciona
  - Investimento mínimo
  - Liquidez
  - Tributação
  - Garantia FGC
  - Quando é indicado]
```

```
Você: Como funciona o Tesouro Direto?

🤖 Assistente: [Explicação completa sobre Tesouro Direto]
```

### Planejamento Financeiro

```
Você: Quero juntar R$ 100000 em 5 anos, quanto devo guardar por mês?

🤖 Assistente: [Cálculo de meta de economia]
```

### Comandos do Sistema

| Comando | Função |
|---------|--------|
| `ajuda` | Mostra ajuda completa |
| `limpar` | Limpa a conversa e começa de novo |
| `exportar` | Exporta conversa em arquivo JSON |
| `sair` | Encerra o chatbot |

## 🎯 Recursos Principais

### ✅ Inteligência Artificial
- **Com IA OpenAI**: Conversas naturais com contexto financeiro
- **Sem IA**: Respostas baseadas em cálculos e banco de produtos

### ✅ Cálculos Disponíveis
- 💵 Juros compostos e simples
- 🏦 Empréstimos (SAC/Price)
- 📊 Valor presente e futuro
- 💰 ROI (Retorno sobre investimento)
- 🎯 Metas de economia
- 📉 Ajuste por inflação
- ⚖️ Relação dívida/renda

### ✅ Produtos Financeiros Explicados
- CDB
- Tesouro Direto (Selic, Prefixado, IPCA+)
- Poupança
- Consórcio
- Seguros
- Previdência (PGBL/VGBL)
- Crédito Imobiliário
- Cartão de Crédito
- Fundos de Investimento
- Ações

### ✅ Persistência
- 💾 Histórico de conversas salvo em SQLite
- 📁 Exportação de conversas
- 🎯 Metas financeiras do usuário
- 👤 Perfis de usuários

## 🎨 Interface

O chatbot usa formatação rica para uma experiência premium:

- **Painéis coloridos** para mensagens
- **Markdown** para explicações
- **Tabelas financeiras** para resultados
- **Formatação em R$** para valores
- **Percentual** para taxas

## 🔧 Personalização

### Adicionar Novos Cálculos

Edite `src/modules/financial_calculator.py`:

```python
@staticmethod
def meu_calculo(param1, param2):
    # Sua lógica
    return resultado
```

### Adicionar Produtos

Edite `src/modules/financial_products.py` e adicione ao dicionário `self.products`.

### Customizar IA

Edite `self.system_prompt` em `src/modules/ai_engine.py`.

## 📁 Estrutura

```
Projeto Chatbot/
├── main.py                 # Executar este arquivo
├── requirements.txt        # Dependências
├── .env                    # Configurações
├── README.md               # Documentação completa
├── src/                    # Código fonte
│   ├── modules/            # Módulos principais
│   ├── utils/              # Utilitários
│   └── ui/                 # Interface
├── tests/                  # Testes
└── data/                   # Banco de dados
```

## 🧪 Testes

Para executar os testes:

```bash
pytest tests/ -v
```

Todos os 38 testes devem passar ✅

## 🆘 Solução de Problemas

### Erro: "OpenAI API key not configured"
- **Solução**: O chatbot funciona sem API key! Apenas ignore ou configure no `.env`.

### Erro de importação
- **Solução**: Execute `pip install -r requirements.txt` novamente

### Interface não aparece colorida
- **Solução**: Verifique se `rich` e `colorama` estão instalados

## 🎉 Pronto!

Agora você tem um assistente financeiro completo com:
- ✅ IA generativa (opcional)
- ✅ Cálculos financeiros
- ✅ Educação financeira
- ✅ Interface premium
- ✅ Persistência de dados

**Divirta-se com seu relacionamento financeiro! 💰**
