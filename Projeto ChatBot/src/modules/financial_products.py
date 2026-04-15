"""
Financial Products Database
Provides information about financial products
"""

from typing import Dict, List, Optional


class FinancialProductsDB:
    """Database of financial products with explanations"""
    
    def __init__(self):
        """Initialize products database"""
        self.products = {
            'cdb': {
                'name': 'CDB (Certificado de Depósito Bancário)',
                'category': 'Renda Fixa',
                'risk_level': 'Baixo',
                'description': 'O CDB é um título de renda fixa emitido por bancos. Ao investir em um CDB, você está emprestando dinheiro ao banco em troca de rentabilidade.',
                'how_it_works': 'Você investe um valor e o banco paga juros em períodos definidos. No vencimento, você recebe o valor investido mais os rendimentos.',
                'minimum_investment': 'Varia de R$ 30 a R$ 1.000 dependendo do banco',
                'liquidity': 'Diária, mensal ou no vencimento (depende do produto)',
                'taxation': 'Imposto de Renda regressivo: 22,5% (até 180 dias), 20% (181-360 dias), 17,5% (361-720 dias), 15% (acima de 720 dias)',
                'guarantee': 'Garantido pelo FGC (Fundo Garantidor de Créditos) até R$ 250.000 por CPF e instituição',
                'good_for': 'Investidores conservadores que buscam segurança e liquidez',
                'examples': [
                    'CDB Pré-fixado: taxa fixa de 12% ao ano',
                    'CDB Pós-fixado: rende 100% do CDI',
                    'CDB de Liquidez Diária: resgate a qualquer momento'
                ]
            },
            'tesouro_direto': {
                'name': 'Tesouro Direto',
                'category': 'Renda Fixa',
                'risk_level': 'Muito Baixo',
                'description': 'O Tesouro Direto é um programa do governo federal que permite que pessoas físicas invistam em títulos públicos federais.',
                'how_it_works': 'Você empresta dinheiro ao governo em troca de rentabilidade. É considerado o investimento mais seguro do país.',
                'minimum_investment': 'A partir de R$ 30',
                'liquidity': 'D+1 (um dia útil após a solicitação)',
                'taxation': 'Imposto de Renda regressivo (igual ao CDB): 22,5% a 15% conforme o prazo',
                'guarantee': 'Garantido pelo Tesouro Nacional (governo federal)',
                'good_for': 'Iniciantes e investidores conservadores',
                'types': [
                    'Tesouro Selic: acompanha a taxa Selic (ideal para reserva de emergência)',
                    'Tesouro Prefixado: taxa fixa (você sabe exatamente quanto vai receber)',
                    'Tesouro IPCA+: protege contra a inflação (garante ganho real)',
                    'Tesouro RendA+: focado em aposentadoria'
                ]
            },
            'poupanca': {
                'name': 'Poupança',
                'category': 'Renda Fixa',
                'risk_level': 'Muito Baixo',
                'description': 'A poupança é a forma mais tradicional de investimento no Brasil, mas nem sempre a mais vantajosa.',
                'how_it_works': 'Rende 70% da taxa Selic + TR (Taxa Referencial) quando a Selic está acima de 8,5% ao ano. Se a Selic estiver em 8,5% ou menos, rende 0,5% ao mês + TR.',
                'minimum_investment': 'Qualquer valor',
                'liquidity': 'Imediata',
                'taxation': 'Isenta de Imposto de Renda para pessoas físicas',
                'guarantee': 'Garantida pelo FGC até R$ 250.000',
                'good_for': 'Reserva de emergência ou quem não quer correr nenhum risco',
                'disadvantage': 'Geralmente rende menos que outras opções de renda fixa como CDB e Tesouro Direto',
                'comparison': 'Se a Selic está em 10,5% ao ano, a poupança rende cerca de 7,35% ao ano (70% de 10,5%). Um CDB a 100% do CDI renderia os 10,5% completos (menos IR).'
            },
            'consorcio': {
                'name': 'Consórcio',
                'category': 'Financiamento Coletivo',
                'risk_level': 'Baixo',
                'description': 'O consórcio é uma modalidade de compra em grupo onde os participantes contribuem mensalmente para formar um fundo comum.',
                'how_it_works': 'Todo mês, um ou mais participantes são contemplados (por sorteio ou lance) e recebem o crédito para comprar o bem. Não há juros, mas há taxa de administração.',
                'minimum_investment': 'Depende do bem (carro, imóvel, serviço)',
                'advantages': [
                    'Sem juros (apenas taxa de administração)',
                    'Planejamento financeiro disciplinado',
                    'Pode usar FGTS para imóveis',
                    'Possibilidade de dar lance para antecipar'
                ],
                'disadvantages': [
                    'Não tem urgência (pode demorar para ser contemplado)',
                    'Taxa de administração pode ser alta',
                    'Multas por desistência',
                    'Não pode usar o bem antes da contemplação'
                ],
                'good_for': 'Quem planeja uma compra futura e não tem urgência'
            },
            'seguro': {
                'name': 'Seguro',
                'category': 'Proteção Financeira',
                'risk_level': 'N/A (Proteção)',
                'description': 'O seguro é um produto financeiro que oferece proteção contra riscos e imprevistos.',
                'how_it_works': 'Você paga um prêmio (valor periódico) e a seguradora se compromete a indenizar perdas conforme as condições do contrato.',
                'types': [
                    'Seguro de Vida: proteção para família em caso de falecimento',
                    'Seguro Auto: proteção contra danos ao veículo',
                    'Seguro Residencial: proteção ao imóvel e bens',
                    'Seguro Saúde: cobertura para despesas médicas',
                    'Seguro de Acidentes Pessoais: cobertura para invalidez/morte por acidente'
                ],
                'good_for': 'Proteção patrimonial e familiar',
                'tip': 'O seguro não é investimento, é proteção. Não espere retorno financeiro, mas tranquilidade.'
            },
            'previdencia': {
                'name': 'Previdência Privada',
                'category': 'Investimento de Longo Prazo',
                'risk_level': 'Variável (depende do tipo)',
                'description': 'A previdência privada é um produto financeiro voltado para acumulação de capital no longo prazo, geralmente para aposentadoria.',
                'types': [
                    'PGBL (Plano Gerador de Benefício Livre): Ideal para quem faz declaração completa do IR. Permite dedução de até 12% da renda bruta.',
                    'VGBL (Vida Gerador de Benefício Livre): Ideal para quem faz declaração simplificada. IR incide apenas sobre rendimentos.'
                ],
                'taxation': [
                    'Tabela Progressiva: 27,5% a 0% (conforme tempo)',
                    'Tabela Regressiva: 35% a 10% (10 anos mínimo para alíquota mínima)'
                ],
                'advantages': [
                    'Benefício fiscal (no PGBL)',
                    'Acumulação no longo prazo',
                    'Possibilidade de aposentadoria complementar',
                    'Pode ter cobertura de riscos (morte/invalidez)'
                ],
                'disadvantages': [
                    'Liquidez reduzida (resgate geralmente após 10 anos)',
                    'Taxas de administração e carregamento',
                    'Imposto de Renda nos resgates',
                    'Complexidade dos produtos'
                ],
                'good_for': 'Quem busca aposentadoria complementar ou planejamento sucessório'
            },
            'credito_imobiliario': {
                'name': 'Crédito Imobiliário / Financiamento de Imóvel',
                'category': 'Financiamento',
                'risk_level': 'N/A (Crédito)',
                'description': 'O crédito imobiliário permite financiar a compra de um imóvel com pagamento parcelado.',
                'how_it_works': 'O banco financia parte do valor do imóvel (geralmente até 80%) e você paga parcelas mensais com juros.',
                'systems': [
                    'SAC (Sistema de Amortização Constante): Parcelas decrescentes, mais juros no início',
                    'Price: Parcelas fixas durante todo o financiamento'
                ],
                'interest_rates': 'Varia de 7% a 12% ao ano dependendo do banco e perfil',
                'requirements': [
                    'Renda comprovada',
                    'Relação comprometimento de renda máximo de 30%',
                    'Valor mínimo do imóvel',
                    'Idade máxima no final do contrato'
                ],
                'costs': [
                    'Taxa de avaliação do imóvel',
                    'Custas cartoriais (registro)',
                    'Seguros (morte/invalidez, dano físico)',
                    'Taxa de administração'
                ],
                'tip': 'Simule em múltiplos bancos e compare o CET (Custo Efetivo Total), não apenas a taxa de juros.'
            },
            'cartao_credito': {
                'name': 'Cartão de Crédito',
                'category': 'Crédito',
                'risk_level': 'Alto (se mal utilizado)',
                'description': 'O cartão de crédito é uma ferramenta de pagamento que permite compras a prazo, mas requer gestão financeira responsável.',
                'how_it_works': 'O banco paga suas compras e você paga o banco na data de vencimento. Se não pagar o total, incidem juros rotativos (os mais altos do mercado).',
                'interest_rates': 'Juros rotativos podem chegar a 400% ao ano (uma das maiores taxas)',
                'good_use': [
                    'Pagar a fatura TOTAL em dia (evita juros)',
                    'Usar como meio de pagamento (não como crédito)',
                    'Aproveitar benefícios (milhas, cashback, pontos)',
                    'Construir histórico de crédito positivo'
                ],
                'bad_use': [
                    'Pagar mínimo da fatura (juros acumulam rapidamente)',
                    'Usar para compras que não pode pagar',
                    'Ter múltiplos cartões sem controle',
                    'Sacar dinheiro (juros imediatos e altíssimos)'
                ],
                'tip': 'O cartão de crédito é uma ferramenta poderosa se usado com disciplina. Se está tendo dificuldades, considere cancelar e usar apenas débito.'
            },
            'fundo_investimento': {
                'name': 'Fundos de Investimento',
                'category': 'Investimento Coletivo',
                'risk_level': 'Variável (depende do tipo)',
                'description': 'Fundos de investimento são condomínios onde vários investidores pooled resources para investir coletivamente sob gestão profissional.',
                'types': [
                    'Fundo de Renda Fixa: Investe em títulos de renda fixa (CDBs, Tesouro, debêntures)',
                    'Fundo de Ações: Investe minimum 67% em ações',
                    'Fundo Multimercado: Investe em diversas classes (renda fixa, ações, câmbio)',
                    'Fundo Cambial: Investe em moedas estrangeiras',
                    'Fundo de Previdência: Vinculado a planos de previdência'
                ],
                'costs': [
                    'Taxa de Administração: remunera o gestor (0,5% a 2% ao ano)',
                    'Taxa de Performance: se superar benchmark (geralmente 20% do que superar)',
                    'Come-cotas: antecipação semestral de IR (maio e novembro)'
                ],
                'advantages': [
                    'Gestão profissional',
                    'Diversificação automática',
                    'Acesso a investimentos complexos',
                    'Praticidade'
                ],
                'disadvantages': [
                    'Custos mais altos que investimentos diretos',
                    'Menor controle sobre a carteira',
                    'Variedade pode ser confusa',
                    'Alguns têm liquidez restrita'
                ],
                'good_for': 'Quem não tem tempo ou conhecimento para gerir própria carteira'
            },
            'acoes': {
                'name': 'Ações',
                'category': 'Renda Variável',
                'risk_level': 'Alto',
                'description': 'Ações representam uma fração do capital social de uma empresa. Ao comprar ações, você se torna sócio (acionista) da empresa.',
                'how_it_works': 'Você compra ações na bolsa de valores (B3) e pode ganhar com valorização e/ou dividendos.',
                'types': [
                    'Ações Ordinárias (ON): dão direito a voto em assembleias',
                    'Ações Preferenciais (PN): têm prioridade na distribuição de lucros'
                ],
                'ways_to_profit': [
                    'Valorização: vender por preço maior que pagou',
                    'Dividendos: parte do lucro distribuída aos acionistas',
                    'Juros sobre Capital Próprio (JCP): similar a dividendos'
                ],
                'risks': [
                    'Volatilidade: preços oscilam bastante',
                    'Risco específico da empresa',
                    'Risco sistêmico (crises econômicas)',
                    'Possibilidade de perder todo o investimento'
                ],
                'good_for': 'Investidores com perfil arrojado e horizonte de longo prazo',
                'tip': 'Nunca invista em ações dinheiro que vai precisar no curto prazo. Diversifique e estude antes de investir.'
            }
        }
    
    def get_product(self, product_key: str) -> Optional[Dict]:
        """
        Get product information
        
        Args:
            product_key: Product identifier
        
        Returns:
            Product information dictionary
        """
        return self.products.get(product_key)
    
    def search_products(self, query: str) -> List[Dict]:
        """
        Search products by query
        
        Args:
            query: Search term
        
        Returns:
            List of matching products
        """
        query_lower = query.lower()
        results = []
        
        for key, product in self.products.items():
            # Search in name, description, and category
            if (query_lower in product['name'].lower() or
                query_lower in product['description'].lower() or
                query_lower in product['category'].lower() or
                query_lower in key.lower()):
                results.append({
                    'key': key,
                    'name': product['name'],
                    'category': product['category'],
                    'risk_level': product['risk_level']
                })
        
        return results
    
    def get_all_products(self) -> List[Dict]:
        """Get summary of all products"""
        return [
            {
                'key': key,
                'name': product['name'],
                'category': product['category'],
                'risk_level': product['risk_level']
            }
            for key, product in self.products.items()
        ]
    
    def format_product_explanation(self, product_key: str) -> str:
        """
        Format complete product explanation
        
        Args:
            product_key: Product identifier
        
        Returns:
            Formatted explanation
        """
        product = self.products.get(product_key)
        if not product:
            return f"Produto '{product_key}' não encontrado."
        
        explanation = f"## {product['name']}\n\n"
        explanation += f"**Categoria**: {product['category']}\n"
        explanation += f"**Nível de Risco**: {product['risk_level']}\n\n"
        explanation += f"{product['description']}\n\n"
        
        if 'how_it_works' in product:
            explanation += f"### Como Funciona\n{product['how_it_works']}\n\n"
        
        if 'minimum_investment' in product:
            explanation += f"### Investimento Mínimo\n{product['minimum_investment']}\n\n"
        
        if 'liquidity' in product:
            explanation += f"### Liquidez\n{product['liquidity']}\n\n"
        
        if 'taxation' in product:
            tax_info = product['taxation']
            if isinstance(tax_info, list):
                explanation += "### Tributação\n"
                for item in tax_info:
                    explanation += f"• {item}\n"
                explanation += "\n"
            else:
                explanation += f"### Tributação\n{tax_info}\n\n"
        
        if 'guarantee' in product:
            explanation += f"### Garantia\n{product['guarantee']}\n\n"
        
        if 'good_for' in product:
            explanation += f"### Indicado Para\n{product['good_for']}\n\n"
        
        if 'types' in product:
            explanation += "### Tipos\n"
            types = product['types']
            if isinstance(types, list):
                for t in types:
                    explanation += f"• {t}\n"
                explanation += "\n"
        
        if 'advantages' in product:
            explanation += "### Vantagens\n"
            for adv in product['advantages']:
                explanation += f"• {adv}\n"
            explanation += "\n"
        
        if 'disadvantages' in product:
            explanation += "### Desvantagens\n"
            for dis in product['disadvantages']:
                explanation += f"• {dis}\n"
            explanation += "\n"
        
        if 'tip' in product:
            explanation += f"### 💡 Dica\n{product['tip']}\n\n"
        
        return explanation
