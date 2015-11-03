__author__ = 'Jake'
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.core.window import Window


class ForeignExchangeCalculator(App):
    sorted_country_names = ListProperty()
    current_country = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        # main window widget build
        self.title = "Foreign Exhange Calculator"
        self.root = Builder.load_file('gui.kv')
        Window.size = (350, 700)

        # retrieving home country
        file = open('config.txt', encoding='utf-8')
        home_country = file.readline()
        self.root.ids.home_country_label.text = home_country
        file.close()

        # retrieving values for the spinner
        file = open('config.txt', encoding='utf-8')
        country_names = file.readlines()
        file.close()
        del(country_names[0])
        sorted_country_names = sorted(country_names)
        # removes date details from the country list
        a = -1
        sorted_dateless_country_names = []
        for countries in range(len(sorted_country_names)):
            a += 1
            sorted_country_name = sorted_country_names[a]
            sorted_country_name_split = sorted_country_name.split(",")
            sorted_dateless_country_names.append(sorted_country_name_split[0])
        current_country = sorted_dateless_country_names[0]
        self.root.ids.country_selection.values = sorted_dateless_country_names
        self.root.ids.country_selection.text = current_country
        return self.root

    # def change_country(self):
    #     self.root.ids.output_label.text = sorted_country_codes
    #     print "changed to", state_code









ForeignExchangeCalculator().run()
