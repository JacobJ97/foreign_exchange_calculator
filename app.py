__author__ = 'Jake'
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.core.window import Window
from trip import Details
import time
import os.path


class ForeignExchangeCalculator(App):
    sorted_dateless_country_names = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        # main window widget build
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file('gui.kv')
        Window.size = (350, 700)

        # text input disable
        self.root.ids.input_country_amount.disabled = True
        self.root.ids.input_home_country_amount.disabled = True

        # status label - config file
        # if not os.path.isfile('config.txt'):
        #     self.root.ids.status.text = "The config file cannot be loaded"
        #     pass
        # else:
        #     file = open('config.txt', encoding='utf-8')
        #     file_details = file.readlines()
        #     file_specific_details = file_details[0]
        #     file_details_specific_split = file_specific_details.split(",")
        #     if file_details_specific_split[1] in file_details_specific_split:
        #         self.root.ids.status.text = "The config file loaded but contains invalid data"
        #         pass
        #     else:
        #         file_specific_details = file_details[1]
        #         file_details_specific_split = file_specific_details.split(",")
        #         if file_details_specific_split[1] is False or file_details_specific_split[3] is True:
        #             self.root.ids.status.text = "The config file loaded but contains invalid data"
        #             pass
        #         else:
        #             self.root.ids.status.text = "The config file has successfully loaded"

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
        del(country_details[0])
        current_time = time.strftime("%Y/%m/%d")
        self.trip_details = Details()
        b = -1
        for i in range(len(country_details)):
            b += 1
            country_details_seperated = country_details[b]
            country_details_split = country_details_seperated.split(",")
            self.trip_details.add(country_details_split[0], country_details_split[1], country_details_split[2])
        current_location = self.trip_details.current_country(current_time)
        self.root.ids.current_destination_label.text += current_location
        #     if country_details_split[1] <= current_time <= country_details_split[2]:
        #         self.root.ids.current_destination_label.text += country_details_split[0]
        return self.root

    def button_press(self):
        self.root.ids.input_country_amount.disabled = False
        self.root.ids.input_home_country_amount.disabled = False

ForeignExchangeCalculator().run()
