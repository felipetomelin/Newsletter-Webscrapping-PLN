from datetime import datetime
from typing import Any, Dict

from EconomicNewsletterAgent import EconomicNewsletterAgent

class Agent5_TopicSummarizer(EconomicNewsletterAgent):
    # Agente 5: Resume informações em tópicos concisos

    def __init__(self):
        super().__init__("AGENT_5", "Resumidor em Tópicos",
                         "Cria resumos em tópicos únicos por tema para o newsletter")

    def create_topic_summaries(self, standardized_data: Dict[str, Any]) -> Dict[str, Any]:
        # Cria resumos em tópicos únicos por tema
        self.log_activity("Iniciando criação de tópicos resumidos...")

        # Seções para o newsletter
        topics = {
            'principais_destaques': [],
            'mercado_hoje': [],
            'politicas_economicas': [],
            'cenario_internacional': [],
            'alerta_investidores': []
        }

        content = standardized_data.get('content', {})

        # Mapear categorias para tópicos do newsletter
        category_mapping = {
            'tensao_geopolitica': 'cenario_internacional',
            'politica_fiscal': 'politicas_economicas',
            'mercado_capitais': 'mercado_hoje',
            'inflacao_juros': 'principais_destaques',
            'commodities': 'mercado_hoje',
            'empresas_resultados': 'mercado_hoje'
        }

        # Processar cada categoria
        for category, data in content.items():
            target_topic = category_mapping.get(category, 'principais_destaques')

            if data['news_count'] > 0:
                # Criar tópico único resumindo a categoria
                topic_summary = {
                    'topic_title': f"{data['category_name']} - {data['news_count']} notícias",
                    'priority': data['priority_level'],
                    'main_points': [],
                    'key_developments': [],
                    'impact_level': self._calculate_impact_level(data['relevance_score'])
                }

                # Extrair pontos principais (top 3 notícias)
                for news_item in data['news_items'][:3]:
                    point = {
                        'headline': news_item['title'],
                        'brief': news_item['summary'][:100] + '...',
                        'relevance': news_item['relevance_score'],
                        'url': news_item['url']
                    }
                    topic_summary['main_points'].append(point)

                # Identificar desenvolvimento principal
                if data['news_items']:
                    top_news = data['news_items'][0]
                    topic_summary['key_developments'].append({
                        'headline': top_news['title'],
                        'importance': 'alta' if data['priority_level'] == 'alta' else 'média',
                        'summary': top_news['summary']
                    })

                topics[target_topic].append(topic_summary)

        # Estatísticas dos tópicos
        topic_stats = {
            'total_topics': sum(len(topic_list) for topic_list in topics.values()),
            'high_impact_topics': sum(1 for topic_list in topics.values()
                                      for topic in topic_list if topic['impact_level'] == 'alto'),
            'newsletter_sections': len([k for k, v in topics.items() if v]),
            'largest_section': max([(k, len(v)) for k, v in topics.items()], key=lambda x: x[1])[0]
        }

        result = {
            'timestamp': datetime.now().isoformat(),
            'newsletter_topics': topics,
            'topic_statistics': topic_stats,
            'ready_for_newsletter': True
        }

        self.processed_count += topic_stats['total_topics']
        self.log_activity(f"Criados {topic_stats['total_topics']} tópicos para newsletter")

        return result

    def _calculate_impact_level(self, relevance_score: int) -> str:
        # Calcula nível de impacto baseado no score de relevância
        if relevance_score >= 8:
            return 'alto'
        elif relevance_score >= 4:
            return 'médio'
        else:
            return 'baixo'