import os
from datetime import datetime, timedelta
from typing import Dict, Any
from Agents.Agent2_EntityExtractor import Agent2_EntityExtractor
from Agents.Agent3_NewsClassifier import Agent3_NewsClassifier
from Agents.Agent4_ResponseStandardizer import Agent4_ResponseStandardizer
from Agents.Agent5_TopicSummarizer import Agent5_TopicSummarizer
from Agents.Agent6_ContentValidator import Agent6_ContentValidator
from Agents.Agent7_TemporalPredictor import Agent7_TemporalPredictor

from Agents.Agent1_ThemeSummarizer import Agent1_ThemeSummarizer
from CNNBrasilScrapper import CNNBrasilScraper
from EconomicNewsletterAgent import EconomicNewsletterAgent
from logger_config import logger

class EconomicNewsletterSystem:

    def __init__(self):
        self.agents = self._initialize_agents()
        self.scraper = CNNBrasilScraper()
        self.data_pipeline = []
        self.is_running = False

    def _initialize_agents(self) -> Dict[str, EconomicNewsletterAgent]:
        # Inicializa todos os 7 agentes
        return {
            'theme_summarizer': Agent1_ThemeSummarizer(),
            'entity_extractor': Agent2_EntityExtractor(),
            'news_classifier': Agent3_NewsClassifier(),
            'response_standardizer': Agent4_ResponseStandardizer(),
            'topic_summarizer': Agent5_TopicSummarizer(),
            'content_validator': Agent6_ContentValidator(),
            'temporal_predictor': Agent7_TemporalPredictor()
        }

    def run_pipeline(self, news_data=None) -> Dict[str, Any]:
        # Executa o pipeline completo de processamento
        logger.info("Iniciando pipeline de newsletter econômico")

        try:
            # Passo 1: Web Scraping (se não recebeu dados)
            if news_data is None:
                raw_news = self.scraper.scrape_economia_news()
                if not raw_news:
                    logger.error("Falha ao obter notícias - pipeline interrompido")
                    return {'error': 'Nenhuma notícia encontrada', 'status': 'failed'}
            else:
                raw_news = news_data

            # Passo 2: Pipeline de processamento dos 7 agentes
            logger.info(f"Iniciando processamento com {len(raw_news)} notícias")

            # Agente 1: Sumarização de temas
            step1_themes = self.agents['theme_summarizer'].process_news(raw_news)

            # Agente 2: Extração de entidades
            step2_entities = self.agents['entity_extractor'].extract_entities(step1_themes)

            # Agente 3: Classificação de notícias
            step3_classified = self.agents['news_classifier'].classify_news(step1_themes)

            # Agente 4: Padronização de respostas
            step4_standardized = self.agents['response_standardizer'].standardize_output(step3_classified)

            # Agente 5: Resumos em tópicos
            step5_topics = self.agents['topic_summarizer'].create_topic_summaries(step4_standardized)

            # Agente 6: Validação de conteúdo
            step6_validated = self.agents['content_validator'].validate_content(step5_topics)

            # Agente 7: Predições temporais
            step7_predictions = self.agents['temporal_predictor'].generate_predictions(step6_validated)

            # Passo 3: Geração do newsletter final
            newsletter_html = self.generate_newsletter(step7_predictions, step6_validated)

            # Passo 4: Salvar resultados
            self.save_newsletter(newsletter_html)

            # Estatísticas do pipeline
            pipeline_stats = {
                'timestamp': datetime.now().isoformat(),
                'news_processed': len(raw_news),
                'total_entities': sum(step2_entities['entity_count'].values()),
                'topics_created': step5_topics['topic_statistics']['total_topics'],
                'topics_approved': sum(
                    check['approved_count'] for check in step6_validated['validation_checks'].values()),
                'predictions_confidence': step7_predictions['predictions']['confidence_levels']['overall_confidence']
            }

            logger.info(f"Pipeline concluído com sucesso: {pipeline_stats['news_processed']} notícias processadas")

            return {
                'status': 'success',
                'stats': pipeline_stats,
                'newsletter': 'newsletter_economia.html',
                'pipeline_data': {
                    'themes': step1_themes,
                    'entities': step2_entities,
                    'classifications': step3_classified,
                    'standardized': step4_standardized,
                    'topics': step5_topics,
                    'validation': step6_validated,
                    'predictions': step7_predictions
                }
            }

        except Exception as e:
            logger.error(f"Erro no pipeline: {str(e)}")
            return {'error': str(e), 'status': 'failed'}

    def generate_newsletter(self, predictions_data: Dict[str, Any], validated_content: Dict[str, Any]) -> str:
        # Gera HTML do newsletter final
        logger.info("Gerando HTML do newsletter final")

        predictions = predictions_data.get('predictions', {})

        newsletter_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Newsletter Econômico Automático</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>📈 Newsletter Econômico Automático</h1>
    <h2>Análise Automática | {datetime.now().strftime('%d de %B de %Y')}</h2>

    <h3>🔥 Principais Destaques</h3>
"""

        # Adicionar tópicos aprovados
        approved_topics = validated_content.get('approved_topics', {})

        for section_name, topics in approved_topics.items():
            if topics:
                newsletter_html += f"<h4>{section_name.replace('_', ' ').title()}</h4>\n"

                for topic in topics[:3]:  # Limitar a 3 tópicos por seção
                    newsletter_html += f"<p><strong>{topic['topic_title'].split(' - ')[0]}:</strong> "
                    if topic.get('main_points'):
                        newsletter_html += f"{topic['main_points'][0].get('brief', '')}</p>\n"

        # Adicionar predições
        newsletter_html += f"""
    <h3>🔮 Predições para as Próximas Semanas</h3>
    <h4>Indicadores Econômicos:</h4>
    <ul>
"""

        for indicator, data in predictions.get('economic_indicators', {}).items():
            newsletter_html += f"<li><strong>{indicator.title()}:</strong> {data.get('prediction_3weeks', 'N/A')} (Confiança: {int(data.get('confidence', 0) * 100)}%)</li>\n"

        newsletter_html += """
    </ul>

    <h4>Setores em Destaque:</h4>
    <ul>
"""

        for sector, data in predictions.get('sector_predictions', {}).items():
            newsletter_html += f"<li><strong>{sector.replace('_', ' ').title()}:</strong> {data.get('outlook', 'N/A')} (Confiança: {int(data.get('confidence', 0) * 100)}%)</li>\n"

        newsletter_html += f"""
    </ul>

    <hr>
    <p><strong>Metodologia:</strong> {predictions_data.get('methodology', 'Análise de tendências')}</p>
    <p><strong>Confiança geral das predições:</strong> {int(predictions.get('confidence_levels', {}).get('overall_confidence', 0) * 100)}%</p>
    <p><strong>Disclaimer:</strong> {predictions_data.get('disclaimer', 'Predições baseadas em análise de tendências.')}</p>

    <footer>
        <p><small>Newsletter gerada automaticamente por sistema multi-agente</small></p>
        <p><small>Próxima edição: {(datetime.now().replace(hour=8, minute=0) + timedelta(days=1)).strftime('%d/%m/%Y às %H:%M')}</small></p>
    </footer>
</body>
</html>
"""

        return newsletter_html

    def save_newsletter(self, newsletter_html: str) -> None:
        # Salva o newsletter em arquivo HTML
        try:
            # Criar diretório outputs se não existir
            os.makedirs('outputs', exist_ok=True)

            filename = f"outputs/newsletter_economia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(newsletter_html)

            logger.info(f"Newsletter salvo em: {filename}")

        except Exception as e:
            logger.error(f"Erro ao salvar newsletter: {str(e)}")