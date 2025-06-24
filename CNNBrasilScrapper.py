import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import re
import sqlite3
from datetime import datetime
import time


class CNNBrasilScraper:
    CATEGORIAS = {
        "mercado": ["bolsa", "ibovespa", "dólar", "ações", "mercado financeiro", "b3"],
        "política": ["governo", "ministro", "presidente", "congresso", "reforma"],
        "empresas": ["empresa", "companhia", "empresarial", "lucro", "balanço"],
        "internacional": ["global", "exterior", "china", "eua", "europa", "exportação"],
        "commodities": ["petróleo", "soja", "milho", "boi gordo", "commodity", "minério"],
        "juros": ["juros", "selic", "bc", "copom", "taxa"],
        "inflação": ["inflação", "ipca", "preços"],
        "energia": ["energia", "eletricidade", "petróleo", "gasolina", "combustível"],
        "tecnologia": ["tecnologia", "inovação", "digital", "startup", "aplicativo"],
        "emprego": ["emprego", "desemprego", "desempregado", "trabalho", "caged"]
    }

    def __init__(self, db_path='news.db'):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_database()

    def _create_database(self):
        """Cria a tabela de notícias se não existir"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS noticias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fonte TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                titulo TEXT NOT NULL,
                texto TEXT NOT NULL,
                data TEXT,
                sentimento REAL,
                categoria TEXT,
                data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def classificar_categoria(self, texto):
        """Classifica a notícia em uma categoria com base em palavras-chave"""
        texto = texto.lower()
        for categoria, palavras in self.CATEGORIAS.items():
            if any(palavra in texto for palavra in palavras):
                return categoria
        return "outras"

    def analisar_sentimento(self, texto):
        """Analisa o sentimento do texto usando TextBlob"""
        blob = TextBlob(texto)
        return blob.sentiment.polarity

    def extrair_conteudo_noticia(self, url):
        """Extrai o conteúdo completo de uma notícia"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extrair título
            title = soup.find('h1')
            title_text = title.get_text(strip=True) if title else "Título não encontrado"

            # Extrair conteúdo principal
            content_div = soup.find('div', class_='post__content')
            if not content_div:
                content_div = soup.find('article')

            content_text = ""
            if content_div:
                paragraphs = content_div.find_all('p')
                content_text = " ".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

            # Extrair data de publicação
            date_element = soup.find('time')
            date = date_element['datetime'] if date_element and date_element.has_attr(
                'datetime') else "Data não encontrada"

            return {
                'title': title_text,
                'content': content_text,
                'date': date
            }
        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")
            return {'title': '', 'content': '', 'date': ''}

    def scrape_economia_news(self):
        """Coleta notícias de economia da CNN Brasil"""
        base_url = "https://www.cnnbrasil.com.br/economia/"
        try:
            response = requests.get(base_url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Estratégia 1: Procurar por elementos de notícia em <article>
            news_items = []
            articles = soup.find_all('article')

            for article in articles:
                link = article.find('a', href=True)
                if link and link['href']:
                    title = article.find(['h2', 'h3', 'h4'])
                    if title:
                        news_items.append({
                            'title': title.get_text(strip=True),
                            'url': link['href']
                        })

            # Estratégia 2: Procurar por títulos que parecem notícias
            if len(news_items) < 5:
                for heading in soup.find_all(['h2', 'h3', 'h4']):
                    if heading.get_text(strip=True) and len(heading.get_text(strip=True)) > 20:
                        parent_link = heading.find_parent('a', href=True)
                        if parent_link and parent_link['href']:
                            news_items.append({
                                'title': heading.get_text(strip=True),
                                'url': parent_link['href']
                            })

            # Remover duplicados
            unique_news = {}
            for item in news_items:
                if item['title'] and item['url']:
                    # Normalizar URL
                    if not item['url'].startswith('http'):
                        if item['url'].startswith('/'):
                            item['url'] = f"https://www.cnnbrasil.com.br{item['url']}"
                        else:
                            item['url'] = f"https://www.cnnbrasil.com.br/{item['url']}"

                    # Usar URL como chave para evitar duplicatas
                    unique_news[item['url']] = item

            # Processar cada notícia
            full_news = []
            for url, item in unique_news.items():
                try:
                    # Extrair conteúdo completo
                    news_details = self.extrair_conteudo_noticia(url)

                    if news_details['content'] and len(news_details['content']) > 100:
                        # Analisar sentimento e categoria
                        sentiment = self.analisar_sentimento(news_details['content'])
                        category = self.classificar_categoria(news_details['content'])

                        # Adicionar à lista de notícias
                        news_data = {
                            'fonte': 'CNN Brasil',
                            'url': url,
                            'titulo': item['title'],
                            'texto': news_details['content'],
                            'data': news_details['date'],
                            'sentimento': sentiment,
                            'categoria': category
                        }
                        full_news.append(news_data)

                        # Salvar no banco de dados
                        try:
                            self.cursor.execute(
                                """INSERT INTO noticias 
                                (fonte, url, titulo, texto, data, sentimento, categoria) 
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                                ON CONFLICT(url) DO NOTHING""",
                                (news_data['fonte'], news_data['url'], news_data['titulo'],
                                 news_data['texto'], news_data['data'], news_data['sentimento'],
                                 news_data['categoria'])
                            )
                            self.conn.commit()
                        except sqlite3.Error as e:
                            print(f"Erro no banco de dados: {e}")

                    # Delay para evitar bloqueio
                    time.sleep(1)

                except Exception as e:
                    print(f"Erro ao processar {url}: {e}")

            return full_news

        except Exception as e:
            print(f"Erro ao acessar o site: {e}")
            return []

    def close(self):
        """Fecha a conexão com o banco de dados"""
        self.conn.close()

    def sumarizar_noticias_simples(self, noticias):
        """Sumariza notícias usando uma abordagem simplificada"""
        if not noticias:
            return "Nenhuma notícia relevante foi coletada."

        # Extrair frases manualmente
        textos = " ".join([noticia['texto'] for noticia in noticias])
        frases = re.split(r'(?<=[.!?])\s+', textos)

        # Verificar se há frases suficientes
        if len(frases) < 5:
            return textos

        # Selecionar algumas frases importantes
        indices = [0, len(frases) // 4, len(frases) // 2, 3 * len(frases) // 4, min(len(frases) - 1, 10)]
        resumo = " ".join([frases[i] for i in indices])

        return resumo
