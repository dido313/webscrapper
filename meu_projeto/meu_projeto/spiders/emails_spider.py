import scrapy
import re
import mysql.connector

class EmailSpider(scrapy.Spider):
    name = "emails_spider"
    start_urls = ['https://listadeemailmarketinggratis.blogspot.com/2013/10/lista-1-6857-e-mails.html']  # Substitua pela URL que deseja raspar

    def parse(self, response):
        # Captura todos os textos da página e procura por emails
        page_content = response.css('body').get()
        emails = self.extract_emails(page_content)
        
        # Salvar emails no banco de dados
        self.save_to_db(emails)

    def extract_emails(self, text):
        # Regex para encontrar emails
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_regex, text)
        return list(set(emails))  # Remove duplicatas

    def save_to_db(self, emails):
        # Conectar ao banco de dados MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="3694481",
            database="scrapy_db"
        )

        cursor = conn.cursor()

        # Inserir emails no banco de dados
        for email in emails:
            cursor.execute("INSERT INTO emails (email) VALUES (%s)", (email,))

        # Confirmar as inserções
        conn.commit()

        # Fechar a conexão com o banco
        cursor.close()
        conn.close()

        print("Emails inseridos com sucesso!")

