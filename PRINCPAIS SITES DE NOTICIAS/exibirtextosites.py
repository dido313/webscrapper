import scrapy

class ContentSpider(scrapy.Spider):
    name = "content_spider"
    start_urls = ['https://www.cnnbrasil.com.br/']  # URL inicial

    def parse(self, response):
        # Captura todos os elementos que contêm notícias na página inicial
        articles = response.css('article')  # Supondo que cada notícia está dentro de um <article>

        if not articles:
            self.logger.warning("Nenhum artigo encontrado na página inicial.")

        # Lista para armazenar as notícias organizadas
        noticias = []

        for article in articles:
            # Captura o título da notícia
            title = article.css('h2::text').get(default='Título não encontrado').strip()

            # Captura o link da notícia
            link = article.css('a::attr(href)').get()

            # Se o link for relativo, adiciona a URL base
            if link and not link.startswith('http'):
                link = response.urljoin(link)

            # Captura o conteúdo resumido ou introdução da notícia (se existir)
            summary = article.css('p::text').get(default='Resumo não encontrado').strip()

            # Armazena os dados em um dicionário
            noticias.append({
                'title': title,
                'link': link,
                'summary': summary
            })

            # Segue o link da notícia, se for válido, para capturar a página interna
            if link:
                yield response.follow(link, self.parse_inner_page, meta={'title': title})

        # Exibe as notícias organizadas
        self.exibir_noticias(noticias)

    def exibir_noticias(self, noticias):
        print("\n--- Notícias Capturadas ---")
        for noticia in noticias:
            print(f"Título: {noticia['title']}\nLink: {noticia['link']}\nResumo: {noticia['summary']}\n")

    def parse_inner_page(self, response):
        # Captura o título da página interna
        title = response.meta['title']  # Obtém o título passado pela função anterior

        # Captura o conteúdo textual relevante da página interna
        inner_text_content = response.css('p::text').getall()  # Captura os parágrafos de texto
        inner_full_text = " ".join(inner_text_content).strip()  # Junta todos os textos em uma única string

        # Exibe o conteúdo da página interna (ou armazena para uso posterior)
        print(f"\n--- Conteúdo da Notícia: {title} ---\n")
        print(inner_full_text)

        # Aqui você pode adicionar lógica adicional para salvar ou processar o conteúdo da página interna
