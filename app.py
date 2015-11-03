__author__ = 'Jake'
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.core.window import Window
from trip import Details
import time


class ForeignExchangeCalculator(App):
    sorted_dateless_country_names = ListProperty()

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
        self.root.ids.country_selection.values = sorted_dateless_country_names

        #date
        self.root.ids.date.text = self.root.ids.date.text + time.strftime("%Y/%m/%d")

        # current location
        file = open('config.txt', encoding='utf-8')
        country_details = file.readlines()
        current_time = time.strftime("%Y/%m/%d")
        b = -1
        for i in range(len(country_details)):
            b += 1
            if
            country_details = country_details[b]
            country_details_split = country_details.split(",")
            if country_details_split[1] <= current_time <= country_details_split[2]:
                self.root.ids.current_destination_label.text += country_details_split[0]
                return self.root.ids.current_destination_label.text

        return self.root
















ForeignExchangeCalculator().run()
