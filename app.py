__author__ = 'Jake'
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window


class ForeignExchangeCalculator(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = "Foreign Exhange Calculator"
        self.root = Builder.load_file('gui.kv')
        Window.size = (350, 700)
        return self.root

    def current_trip_location(self, label):
        from trip import Details
        import datetime
        self.root.ids.date = datetime.time()





ForeignExchangeCalculator().run()
