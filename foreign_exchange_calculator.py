__author__ = 'Jake'
from kivy.app import App
from kivy.lang import Builder


class ForeignExchangeCalculator(App):
    def build(self):
        self.title = "Foreign Exhange Calculator"
        self.root = Builder.load_file('foreign_exchange_calculator.kv')
        return self.root

ForeignExchangeCalculator().run()
