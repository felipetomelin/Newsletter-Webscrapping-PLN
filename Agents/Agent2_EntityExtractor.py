from datetime import datetime
import re
from typing import Dict, Any


from EconomicNewsletterAgent import EconomicNewsletterAgent

class Agent2_EntityExtractor(EconomicNewsletterAgent):
    """Agente 2: Extrai entidades nomeadas das notícias"""

    def __init__(self):
        super().__init__("AGENT_2", "Extrator de Entidades",
                         "Extrai entidades como empresas, pessoas, localidades e valores")

        # Listas de entidades conhecidas
        self.known_companies = [
            'petrobras', 'vale', 'itau', 'bradesco', 'banco do brasil',
            'magazine luiza', 'ambev', 'jbs', 'natura', 'gerdau', 'embraer',
            'localiza', 'weg', 'b3', 'eletrobras', 'santander', 'nubank',
            'inter', 'xp', 'btg', 'cvc', 'sabesp', 'marfrig', 'carrefour', 'cnn'
        ]

        self.known_people = [
            'lula', 'haddad', 'campos neto', 'galípolo', 'tebet', 'tarcísio', 'costa',
            'bolsonaro', 'meirelles', 'guedes', 'arminio fraga', 'mantega', 'levy'
        ]

        self.known_locations = [
            'brasil', 'são paulo', 'rio de janeiro', 'brasília', 'estados unidos',
            'china', 'europa', 'ásia', 'eua', 'oriente médio', 'irã', 'argentina'
        ]

    def extract_entities(self, summarized_themes: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai entidades relevantes das notícias"""
        self.log_activity("Iniciando extração de entidades...")

        entities = {
            'companies': set(),
            'people': set(),
            'locations': set(),
            'values': [],
            'dates': []
        }

        # Processar cada notícia para extrair entidades
        for theme, news_list in summarized_themes['main_themes'].items():
            for news in news_list:
                text = (news.get('title', '') + ' ' + news.get('content', '')).lower()

                # Extrair empresas
                for company in self.known_companies:
                    if company in text:
                        entities['companies'].add(company.title())

                # Extrair pessoas
                for person in self.known_people:
                    if person in text:
                        entities['people'].add(person.title())

                # Extrair localizações
                for location in self.known_locations:
                    if location in text:
                        entities['locations'].add(location.title())

                # Extrair valores monetários
                money_pattern = r'r\$\s*[\d.,]+(?:\s*(?:milhões?|bilhões?|trilhões?))?'
                values = re.findall(money_pattern, text)
                entities['values'].extend(values)

                # Extrair datas
                date_pattern = r'\d{1,2}\s+de\s+(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\s+de\s+\d{4}'
                dates = re.findall(date_pattern, text)
                entities['dates'].extend(dates)

        # Converter sets para listas para serialização
        entities['companies'] = list(entities['companies'])
        entities['people'] = list(entities['people'])
        entities['locations'] = list(entities['locations'])

        self.processed_count += len([item for sublist in summarized_themes['main_themes'].values() for item in sublist])

        # Estatísticas das entidades extraídas
        result = {
            'timestamp': datetime.now().isoformat(),
            'entities': entities,
            'entity_count': {
                'companies': len(entities['companies']),
                'people': len(entities['people']),
                'locations': len(entities['locations']),
                'values': len(entities['values']),
                'dates': len(entities['dates'])
            },
            'top_entities': {
                'companies': entities['companies'][:5],
                'people': entities['people'][:5],
                'locations': entities['locations'][:5]
            }
        }

        self.log_activity(f"Extraídas {sum(result['entity_count'].values())} entidades")
        return result