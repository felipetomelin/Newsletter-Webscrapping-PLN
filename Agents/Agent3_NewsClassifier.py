from datetime import datetime
from typing import Dict, Any, List

from EconomicNewsletterAgent import EconomicNewsletterAgent


class Agent3_NewsClassifier(EconomicNewsletterAgent):
    # Agente 3: Classifica notícias por temas específicos

    def __init__(self):
        super().__init__("AGENT_3", "Classificador de Notícias",
                         "Classifica notícias em categorias específicas do momento econômico")

        # Categorias específicas e palavras-chave correspondentes
        self.current_categories = {
            'tensao_geopolitica': {
                'keywords': ['irã', 'israel', 'petróleo', 'conflito', 'ormuz', 'guerra', 'oriente médio', 'ataque'],
                'priority': 'alta'
            },
            'politica_fiscal': {
                'keywords': ['fiscal', 'meta', 'orçamento', 'deficit', 'superavit', 'ldo', 'receita', 'despesa',
                             'inss'],
                'priority': 'alta'
            },
            'mercado_capitais': {
                'keywords': ['bolsa', 'ações', 'ibovespa', 'investimento', 'b3', 'ações', 'índice', 'pontos'],
                'priority': 'média'
            },
            'inflacao_juros': {
                'keywords': ['inflação', 'juros', 'selic', 'focus', 'copom', 'ipca', 'igpm', 'preços'],
                'priority': 'alta'
            },
            'commodities': {
                'keywords': ['petróleo', 'ouro', 'soja', 'minério', 'commodity', 'barril', 'café', 'agrícola'],
                'priority': 'média'
            },
            'empresas_resultados': {
                'keywords': ['lucro', 'receita', 'resultado', 'balanço', 'trimestre', 'earnings', 'prejuízo',
                             'demonstração'],
                'priority': 'baixa'
            }
        }

    def classify_news(self, themes_and_entities: Dict[str, Any]) -> Dict[str, Any]:
        # Classifica notícias em categorias específicas
        self.log_activity("Iniciando classificação de notícias...")

        classified_news = {}

        # Inicializar estrutura de categorias
        for category, config in self.current_categories.items():
            classified_news[category] = {
                'news': [],
                'priority': config['priority'],
                'relevance_score': 0
            }

        # Classificar notícias por categorias
        themes = themes_and_entities.get('main_themes', {})

        for theme_name, news_list in themes.items():
            for news in news_list:
                text = (news.get('title', '') + ' ' + news.get('content', '')).lower()

                # Verificar correspondência com cada categoria
                for category, config in self.current_categories.items():
                    keyword_matches = sum(1 for keyword in config['keywords'] if keyword in text)
                    if keyword_matches > 0:
                        classified_news[category]['news'].append({
                            'news': news,
                            'relevance_score': keyword_matches,
                            'original_theme': theme_name
                        })

        # Calcular scores de relevância total por categoria
        for category in classified_news:
            total_score = sum(item['relevance_score'] for item in classified_news[category]['news'])
            classified_news[category]['relevance_score'] = total_score

        self.processed_count += sum(len(cat['news']) for cat in classified_news.values())

        # Resultados da classificação
        result = {
            'timestamp': datetime.now().isoformat(),
            'classified_categories': classified_news,
            'category_distribution': {cat: len(data['news']) for cat, data in classified_news.items()},
            'high_priority_count': sum(len(data['news']) for cat, data in classified_news.items()
                                       if data['priority'] == 'alta'),
            'top_categories': sorted([(cat, data['relevance_score']) for cat, data in classified_news.items()
                                      if len(data['news']) > 0], key=lambda x: x[1], reverse=True)[:3]
        }

        self.log_activity(f"Classificadas notícias em {len(self.current_categories)} categorias")
        return result