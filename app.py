__author__ = 'Jake'
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.core.window import Window
from trip import Details
import currency
import time
import os.path


class ForeignExchangeCalculator(App):
    sorted_dateless_country_names = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.trip_details = Details()
        # main window widget build
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file('gui.kv')
        Window.size = (350, 700)

        # text input disable
        self.root.ids.input_country_amount.disabled = True
        self.root.ids.input_home_country_amount.disabled = True

        # status label - config file
        if not os.path.isfile('config.txt'):
            self.root.ids.status.text = "The config file cannot be loaded"
            pass
        else:
            self.root.ids.status.text = "The config file successfully loaded"

        # retrieving home country
        file = open('config.txt', encoding='utf-8')
        home_country = file.readline()
        home_country = home_country.rstrip("\n")
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
        b = -1
        for i in range(len(country_details)):
            b += 1
            country_details_seperated = country_details[b]
            country_details_split = country_details_seperated.rstrip("\n").split(",")
            self.trip_details.add(country_details_split[0], country_details_split[1], country_details_split[2])
        current_location = self.trip_details.current_country(current_time)
        self.root.ids.current_destination_label.text += current_location
        return self.root

    def button_press(self):
        # text input enable
        self.root.ids.input_country_amount.disabled = False
        self.root.ids.input_home_country_amount.disabled = False

        # currency exchange
        currency1 = self.root.ids.input_home_country_amount.text
        currency2 = self.root.ids.input_country_amount.text

        # spinner / home information grabbing
        country1 = self.root.ids.home_country_label.text
        country2 = self.root.ids.country_selection.text
        country_dic_details1 = currency.get_all_details(country1)
        country_dic_details2 = currency.get_all_details(country2)
        amount1 = currency.convert(currency1, country_dic_details1, country_dic_details2)

        print(amount1)
        print(amount2)






ForeignExchangeCalculator().run()
