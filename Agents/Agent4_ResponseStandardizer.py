from datetime import datetime
from typing import Dict, Any

from EconomicNewsletterAgent import EconomicNewsletterAgent

class Agent4_ResponseStandardizer(EconomicNewsletterAgent):
    # Agente 4: Padroniza as respostas e formato de saída

    def __init__(self):
        super().__init__("AGENT_4", "Padronizador de Respostas",
                         "Padroniza formato e estrutura das respostas dos agentes anteriores")

    def standardize_output(self, classified_data: Dict[str, Any]) -> Dict[str, Any]:
        # Padroniza a saída em formato consistente
        self.log_activity("Iniciando padronização de respostas...")

        standardized = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'processing_date': datetime.now().strftime("%Y-%m-%d"),
                'version': '1.0',
                'total_categories': len(classified_data.get('classified_categories', {}))
            },
            'content': {},
            'statistics': {}
        }

        # Padronizar conteúdo por categoria
        for category, data in classified_data.get('classified_categories', {}).items():
            standardized['content'][category] = {
                'category_name': category.replace('_', ' ').title(),
                'priority_level': data.get('priority', 'média'),
                'relevance_score': data.get('relevance_score', 0),
                'news_count': len(data.get('news', [])),
                'news_items': []
            }

            # Limitar a 5 notícias mais relevantes por categoria
            sorted_news = sorted(data.get('news', []),
                                 key=lambda x: x.get('relevance_score', 0), reverse=True)

            # Padronizar cada notícia
            for item in sorted_news[:5]:
                news = item.get('news', {})
                standardized_news = {
                    'title': news.get('title', 'Título não disponível'),
                    'summary': news.get('content', '')[:200] + '...' if len(
                        news.get('content', '')) > 200 else news.get('content', ''),
                    'relevance_score': item.get('relevance_score', 0),
                    'source_theme': item.get('original_theme', 'outros'),
                    'url': news.get('url', '#'),
                    'timestamp': news.get('timestamp', datetime.now().isoformat())
                }
                standardized['content'][category]['news_items'].append(standardized_news)

        # Estatísticas gerais
        standardized['statistics'] = {
            'total_news_processed': sum(cat['news_count'] for cat in standardized['content'].values()),
            'high_priority_categories': len([cat for cat in standardized['content'].values()
                                             if cat['priority_level'] == 'alta']),
            'top_category': max(standardized['content'].items(),
                                key=lambda x: x[1]['relevance_score'])[0] if standardized['content'] else None,
            'processing_time_ms': (datetime.now() - datetime.fromisoformat(
                standardized['metadata']['timestamp'])).total_seconds() * 1000
        }

        self.processed_count += standardized['statistics']['total_news_processed']
        self.log_activity(f"Padronizadas {standardized['statistics']['total_news_processed']} notícias")

        return standardized