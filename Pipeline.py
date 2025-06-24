sample_news_data = [
    {
        'title': 'Por que o petróleo caiu 7% após o Irã atacar alvos dos EUA?',
        'content': 'O preço do petróleo Brent recuou cerca de 7% nesta segunda-feira, após os ataques do Irã contra alvos americanos no Iraque. A resposta tímida dos EUA reduziu temores de escalada militar maior no Oriente Médio.',
        'url': 'https://cnnbrasil.com.br/economia/petroleo-caiu-ira-atacou-eua',
        'timestamp': '2025-06-23T17:57:00',
        'category': 'internacional'
    },
    {
        'title': 'Focus: mercado reduz projeção para inflação em 2025 e eleva juros',
        'content': 'O relatório Focus do Banco Central mostrou que analistas reduziram a projeção de inflação para 2025 de 3,9% para 3,85%, mas elevaram a expectativa para a taxa Selic para 12,5% ao final do ano.',
        'url': 'https://cnnbrasil.com.br/economia/focus-inflacao-juros',
        'timestamp': '2025-06-23T16:30:00',
        'category': 'politica_economica'
    },
    {
        'title': 'Restituição do INSS fora da meta fiscal mina credibilidade',
        'content': 'Analistas criticam decisão do governo de tirar as restituições do INSS da meta fiscal, afirmando que a medida compromete a credibilidade da política fiscal brasileira.',
        'url': 'https://cnnbrasil.com.br/economia/inss-meta-fiscal',
        'timestamp': '2025-06-23T19:54:00',
        'category': 'politica_economica'
    },
    {
        'title': 'Bolsas em NY sobem com tensão no Oriente Médio e juros no radar',
        'content': 'As bolsas americanas fecharam em alta, com investidores monitorando os desenvolvimentos geopolíticos no Oriente Médio e aguardando sinais sobre a política monetária do Federal Reserve.',
        'url': 'https://cnnbrasil.com.br/economia/bolsas-ny-sobem',
        'timestamp': '2025-06-23T18:29:00',
        'category': 'mercado_financeiro'
    },
    {
        'title': 'Brasil sente peso de custo na logística com alta do frete',
        'content': 'O aumento dos custos de frete marítimo e os desvios de rotas devido ao conflito no Oriente Médio estão impactando a logística brasileira, elevando custos de importação.',
        'url': 'https://cnnbrasil.com.br/economia/logistica-frete',
        'timestamp': '2025-06-23T20:49:00',
        'category': 'comercio'
    }
]

print("=== EXECUÇÃO COMPLETA DO PIPELINE DE 7 AGENTES ===\n")
print(" DADOS DE ENTRADA: Simulando notícias da CNN Brasil Economia")
print(f"📊 Total de notícias para processar: {len(sample_news_data)}")
print("\n" + "="*60 + "\n")

# PIPELINE COMPLETO - EXECUTAR TODOS OS AGENTES EM SEQUÊNCIA

# AGENTE 1: Sumarização de Temas
print("🤖 EXECUTANDO AGENTE 1 - SUMARIZADOR DE TEMAS")
step1_themes = agent1.process_news(sample_news_data)
print(f" Temas identificados: {list(step1_themes['themes_distribution'].keys())}")
print(f" Distribuição: {step1_themes['themes_distribution']}")
print()

# AGENTE 2: Extração de Entidades
print("🤖 EXECUTANDO AGENTE 2 - EXTRATOR DE ENTIDADES")
step2_entities = agent2.extract_entities(step1_themes)
print(f" Entidades extraídas: {step2_entities['entity_count']}")
print(f" Empresas: {', '.join(step2_entities['entities']['companies'][:3])}...")
print(f"👤 Pessoas: {', '.join(step2_entities['entities']['people'][:3])}...")
print()

# AGENTE 3: Classificação de Notícias
print(" EXECUTANDO AGENTE 3 - CLASSIFICADOR DE NOTÍCIAS")
step3_classified = agent3.classify_news(step1_themes)
print(f" Categorias classificadas: {len(step3_classified['classified_categories'])}")
print(f" Notícias alta prioridade: {step3_classified['high_priority_count']}")
print(f" Distribuição por categoria: {step3_classified['category_distribution']}")
print()

# AGENTE 4: Padronização
print("🤖 EXECUTANDO AGENTE 4 - PADRONIZADOR DE RESPOSTAS")
step4_standardized = agent4.standardize_output(step3_classified)
print(f" Notícias padronizadas: {step4_standardized['statistics']['total_news_processed']}")
print(f" Seções criadas: {step4_standardized['metadata']['total_categories']}")
print(f" Top categoria: {step4_standardized['statistics']['top_category']}")
print()

# AGENTE 5: Resumos em Tópicos
print("🤖 EXECUTANDO AGENTE 5 - RESUMIDOR EM TÓPICOS")
step5_topics = agent5.create_topic_summaries(step4_standardized)
print(f" Tópicos criados: {step5_topics['topic_statistics']['total_topics']}")
print(f" Alto impacto: {step5_topics['topic_statistics']['high_impact_topics']}")
print(f" Seções newsletter: {step5_topics['topic_statistics']['newsletter_sections']}")
print()

# AGENTE 6: Validação de Conteúdo
print("🤖 EXECUTANDO AGENTE 6 - VALIDADOR DE CONTEÚDO")
step6_validated = agent6.validate_content(step5_topics)
total_approved = sum(check['approved_count'] for check in step6_validated['validation_checks'].values())
total_topics = sum(check['topics_count'] for check in step6_validated['validation_checks'].values())
print(f" Qualidade geral: {step6_validated['overall_quality'].upper()}")
print(f" Aprovados: {total_approved}/{total_topics} tópicos")
print(f" Recomendações: {len(step6_validated['recommendations'])}")
print()

# AGENTE 7: Predições Temporais
print("🤖 EXECUTANDO AGENTE 7 - PREDITOR TEMPORAL")
step7_predictions = agent7.generate_predictions(step6_validated)
predictions = step7_predictions['predictions']
print(f" Indicadores analisados: {len(predictions['economic_indicators'])}")
print(f" Setores analisados: {len(predictions['sector_predictions'])}")
print(f" Fatores de risco: {len(predictions['risk_factors'])}")
print(f" Confiança geral: {predictions['confidence_levels']['overall_confidence']:.1%}")
print()

print("="*60)
print(" PIPELINE COMPLETO EXECUTADO COM SUCESSO!")
print(f" Total de processamentos: {sum([a.processed_count for a in [agent1, agent2, agent3, agent4, agent5, agent6, agent7]])}")
print(" Sistema pronto para gerar newsletter!")