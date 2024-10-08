from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import random

class NewsApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Campo de texto
        self.text_input = TextInput(size_hint_y=None, height=40, hint_text='Digite aqui...')
        self.layout.add_widget(self.text_input)

        # Opções de categorias
        self.checkboxes = {
            "Política": CheckBox(),
            "Financeiro": CheckBox(),
            "Tecnologia": CheckBox(),
            "Geral": CheckBox(),
        }

        for label, checkbox in self.checkboxes.items():
            box = BoxLayout(size_hint_y=None, height=40)
            box.add_widget(checkbox)
            box.add_widget(Label(text=label))
            self.layout.add_widget(box)

        # Botão OK
        self.ok_button = Button(text='OK', size_hint_y=None, height=40)
        self.ok_button.bind(on_press=self.generate_random_news)
        self.layout.add_widget(self.ok_button)

        # Área para exibir o texto gerado
        self.news_label = Label(size_hint_y=None, height=200, text='Notícias aparecerão aqui...', halign='left', text_size=(self.layout.width, None))
        self.layout.add_widget(self.news_label)

        return self.layout

    def generate_random_news(self, instance):
        categories = [label for label, checkbox in self.checkboxes.items() if checkbox.active]
        if categories:
            # Texto aleatório simulado (pode ser substituído por uma chamada a uma API ou banco de dados)
            random_news = f"Notícia aleatória sobre {' e '.join(categories)}: {random.choice(['Evento 1', 'Evento 2', 'Evento 3'])}"
            self.news_label.text = random_news
        else:
            self.news_label.text = "Selecione pelo menos uma categoria."

if __name__ == '__main__':
    NewsApp().run()