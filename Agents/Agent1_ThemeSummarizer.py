from datetime import datetime

from EconomicNewsletterAgent import EconomicNewsletterAgent


class Agent1_ThemeSummarizer(EconomicNewsletterAgent):
    """Agente 1: Sumariza os temas principais das notícias"""

    def __init__(self):
        super().__init__("AGENT_1", "Sumarizador de Temas",
                         "Identifica e sumariza os temas principais das notícias econômicas")

    def process_news(self, raw_news_list):
        """Sumariza temas principais das notícias"""
        self.log_activity("Iniciando sumarização de temas principais...")

        themes = {
            'mercado_financeiro': [],
            'politica_economica': [],
            'empresas': [],
            'internacional': [],
            'commodities': [],
            'outros': []
        }

        # Simular análise de temas principais
        for news in raw_news_list:
            title = news.get('title', '').lower()
            content = news.get('content', '').lower()

            # Classificação básica por palavras-chave
            if any(word in title + content for word in ['bolsa', 'ibovespa', 'ações', 'investimento']):
                themes['mercado_financeiro'].append(news)
            elif any(word in title + content for word in ['governo', 'ministério', 'política']):
                themes['politica_economica'].append(news)
            elif any(word in title + content for word in ['empresa', 'corporação', 'negócios']):
                themes['empresas'].append(news)
            elif any(word in title + content for word in ['internacional', 'global', 'mundial']):
                themes['internacional'].append(news)
            elif any(word in title + content for word in ['petróleo', 'ouro', 'commodities']):
                themes['commodities'].append(news)
            else:
                themes['outros'].append(news)

        self.processed_count += len(raw_news_list)
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_news': len(raw_news_list),
            'themes_distribution': {k: len(v) for k, v in themes.items()},
            'main_themes': themes
        }

        self.log_activity(f"Processadas {len(raw_news_list)} notícias em {len(themes)} temas")
        return summary