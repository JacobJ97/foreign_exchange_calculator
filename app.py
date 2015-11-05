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
    country_name_codes = ([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.trip_details = Details()
        # main window widget build
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file('gui.kv')
        Window.size = (500, 700)

        # text input disable
        # self.root.ids.input_country_amount.disabled = True
        # self.root.ids.input_home_country_amount.disabled = True

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
        for countries in range(len(sorted_country_names)):
            a += 1
            sorted_country_name = sorted_country_names[a]
            sorted_country_name_split = sorted_country_name.rstrip("\n").split(",")
            country_list_dictionary = currency.get_all_details(sorted_country_name_split[0])
            country_name_codes = sorted(country_list_dictionary.keys())
            print(country_list_dictionary.items())
        self.root.ids.country_selection.values = country_name_codes

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
            country_details_separated = country_details[b]
            country_details_split = country_details_separated.rstrip("\n").split(",")
            self.trip_details.add(country_details_split[0], country_details_split[1], country_details_split[2])
        current_location = self.trip_details.current_country(current_time)
        self.root.ids.current_destination_label.text += current_location
        return self.root

    # def change_state(self):
    #     """ handle change of spinner selection, output result to label widget """
    #     self.root.ids.country_selection.text = country_list_dictionary[self.country_name_code]
    #     print("changed to", self.country_list_dictionary[self.country_name_code])

    def button_press(self):
        # text input enable
        # self.root.ids.input_country_amount.disabled = False
        # self.root.ids.input_home_country_amount.disabled = False

        # currency exchange
        currency1 = self.root.ids.input_home_country_amount.text
        currency2 = self.root.ids.input_country_amount.text

        # spinner / home information grabbing
        country1 = self.root.ids.home_country_label.text
        country2 = self.root.ids.country_selection.text
        country_details1 = currency.get_details(country1)
        country_details2 = currency.get_details(country2)

        if currency1 is "":
            amount2 = currency.convert(currency2, country_details2[1], country_details1[1])
            print(amount2)
            self.root.ids.status.text = "{}({}) -> {}({})".format(country_details2[1],  country_details2[2], country_details1[1], country_details1[2])
            self.root.ids.input_home_country_amount.text = str(amount2)
            # currency_amount_difference1 = currency.convert(1, country_details2[1], country_details1[1])
            # self.root.ids.input_home_country_amount.text = amount2 * currency_amount_difference1

        elif currency2 is "":
            amount1 = currency.convert(currency1, country_details1[1], country_details2[1])
            print(amount1)
            self.root.ids.input_country_amount.text = str(amount1)
            self.root.ids.status.text = "{}({}) -> {}({})".format(country_details1[1],  country_details2[2],  country_details2[1], country_details2[2])
            # currency_amount_difference2 = currency.convert(1, country_details1[1], country_details2[1])
            # self.root.ids.input_country_amount.text = amount1 * currency_amount_difference2










ForeignExchangeCalculator().run()
