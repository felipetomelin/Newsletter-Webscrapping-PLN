from typing import Any, Dict, List

from EconomicNewsletterAgent import EconomicNewsletterAgent

class Agent6_ContentValidator(EconomicNewsletterAgent):
    """Agente 6: Valida se os resumos são adequados para leitores"""

    def __init__(self):
        super().__init__("AGENT_6", "Validador de Conteúdo",
                         "Valida qualidade e adequação do conteúdo para leitores")

    def validate_content(self, topic_summaries: Dict[str, Any]) -> Dict[str, Any]:
        """Valida se o conteúdo está adequado para publicação"""
        self.log_activity("Iniciando validação de conteúdo...")

        validation_results = {
            'overall_quality': 'aprovado',
            'validation_checks': {},
            'recommendations': [],
            'approved_topics': {},
            'rejected_topics': {}
        }

        newsletter_topics = topic_summaries.get('newsletter_topics', {})

        # Validar cada seção do newsletter
        for section_name, topics in newsletter_topics.items():
            section_validation = {
                'topics_count': len(topics),
                'approved_count': 0,
                'quality_score': 0,
                'issues_found': []
            }

            approved_topics = []
            rejected_topics = []

            # Validar cada tópico da seção
            for topic in topics:
                topic_validation = self._validate_topic(topic)

                if topic_validation['approved']:
                    approved_topics.append(topic)
                    section_validation['approved_count'] += 1
                    section_validation['quality_score'] += topic_validation['quality_score']
                else:
                    rejected_topics.append({
                        'topic': topic,
                        'rejection_reasons': topic_validation['issues']
                    })
                    section_validation['issues_found'].extend(topic_validation['issues'])

            # Calcular score médio da seção
            if section_validation['approved_count'] > 0:
                section_validation['quality_score'] /= section_validation['approved_count']

            validation_results['validation_checks'][section_name] = section_validation
            validation_results['approved_topics'][section_name] = approved_topics
            validation_results['rejected_topics'][section_name] = rejected_topics

        # Validação geral
        total_approved = sum(check['approved_count'] for check in validation_results['validation_checks'].values())
        total_topics = sum(check['topics_count'] for check in validation_results['validation_checks'].values())

        # Se menos de 70% aprovados, requer revisão
        if total_topics > 0 and total_approved / total_topics < 0.7:
            validation_results['overall_quality'] = 'revisão_necessária'
            validation_results['recommendations'].append('Menos de 70% dos tópicos foram aprovados - revisar critérios')

        # Recomendações baseadas na validação
        validation_results['recommendations'].extend(self._generate_recommendations(validation_results))

        self.processed_count += total_topics
        self.log_activity(f"Validados {total_topics} tópicos - {total_approved} aprovados")

        return validation_results

    def _validate_topic(self, topic: Dict[str, Any]) -> Dict[str, Any]:
        """Valida um tópico individual"""
        validation = {
            'approved': True,
            'quality_score': 0,
            'issues': []
        }

        # Verificar título
        if len(topic.get('topic_title', '')) < 10:
            validation['issues'].append('Título muito curto')
            validation['approved'] = False
        else:
            validation['quality_score'] += 20

        # Verificar pontos principais
        main_points = topic.get('main_points', [])
        if len(main_points) == 0:
            validation['issues'].append('Nenhum ponto principal encontrado')
            validation['approved'] = False
        else:
            validation['quality_score'] += len(main_points) * 15

        # Verificar qualidade do conteúdo
        for point in main_points:
            if len(point.get('brief', '')) < 20:
                validation['issues'].append('Resumo muito superficial')
                validation['quality_score'] -= 10

        # Score máximo de 100
        validation['quality_score'] = min(validation['quality_score'], 100)

        return validation

    def _generate_recommendations(self, validation_results: Dict[str, Any]) -> List[str]:
        """Gera recomendações baseadas na validação"""
        recommendations = []

        # Analisar cada seção para recomendações
        for section, check in validation_results['validation_checks'].items():
            if check['quality_score'] < 50 and check['topics_count'] > 0:
                recommendations.append(f'Seção "{section}" precisa de mais conteúdo de qualidade')

            if check['approved_count'] == 0 and check['topics_count'] > 0:
                recommendations.append(f'Seção "{section}" não tem tópicos aprovados - considerar remover')

        return recommendations