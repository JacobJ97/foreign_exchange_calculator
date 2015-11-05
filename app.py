__author__ = 'Jake'
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from trip import Details
import currency
import time
import os.path


class ForeignExchangeCalculator(App):
    country_name_codes = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.trip_details = Details()
        # main window widget build
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file('gui.kv')
        Window.size = (500, 700)

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
        self.current_location = self.trip_details.current_country(current_time)
        self.root.ids.current_destination_label.text += self.current_location
        return self.root

    def update_currency(self):
        # text input enable
        if self.root.ids.input_country_amount.disabled is True and self.root.ids.input_home_country_amount.disabled is True:
            self.root.ids.input_country_amount.disabled = False
            self.root.ids.input_home_country_amount.disabled = False
            self.root.ids.input_country_amount.text = ''
            self.root.ids.input_home_country_amount.text = ''
            return

        self.root.ids.input_country_amount.focus = False
        self.root.ids.input_home_country_amount.focus = False

        # currency exchange
        self.currency1 = self.root.ids.input_home_country_amount.text
        self.currency2 = self.root.ids.input_country_amount.text

        # spinner / home information grabbing
        self.country1 = self.root.ids.home_country_label.text
        self.country2 = self.root.ids.country_selection.text

        if self.country2 is "":
            self.country2 = self.root.ids.country_selection.text = self.current_location

        self.country_details1 = currency.get_details(self.country1)
        self.country_details2 = currency.get_details(self.country2)

        if self.currency1 is "":
            self.amount2 = currency.convert(self.currency2, self.country_details2[1], self.country_details1[1])
            print(self.amount2)
            self.amount2 = round(self.amount2, 3)
            if self.amount2 is -1:
                self.root.ids.input_country_amount.disabled = True
                self.root.ids.input_home_country_amount.disabled = True
            self.root.ids.input_home_country_amount.text = str(self.amount2)
            current_time = time.strftime("%H:%M:%S")
            self.root.ids.status.text = "updated at {}".format(current_time)

        elif self.currency2 is "":
            self.amount1 = currency.convert(self.currency1, self.country_details1[1], self.country_details2[1])
            self.amount1 = round(self.amount1, 3)
            print(self.amount1)
            if self.amount1 is -1:
                self.root.ids.input_country_amount.disabled = True
                self.root.ids.input_home_country_amount.disabled = True
            self.root.ids.input_country_amount.text = str(self.amount1)
            current_time = time.strftime("%H:%M:%S")
            self.root.ids.status.text = "updated at {}".format(current_time)

    def change_amount(self):
        self.currency1 = self.root.ids.input_home_country_amount.text
        self.currency2 = self.root.ids.input_country_amount.text

        self.root.ids.input_country_amount.focus = False
        self.root.ids.input_home_country_amount.focus = False

        if self.currency1 is "":
            self.amount2 = currency.convert(self.currency2, self.country_details2[1], self.country_details1[1])
            self.amount2 = round(self.amount2, 3)
            print(self.amount2)
            if self.amount2 is -1:
                self.root.ids.input_country_amount.disabled = True
                self.root.ids.input_home_country_amount.disabled = True
            self.root.ids.input_home_country_amount.text = str(self.amount2)
            self.root.ids.status.text = "{}({}) -> {}({})".format(self.country_details2[1],  self.country_details2[2], self.country_details1[1], self.country_details1[2])

        elif self.currency2 is "":
            self.amount1 = currency.convert(self.currency1, self.country_details1[1], self.country_details2[1])
            self.amount1 = round(self.amount1, 3)
            print(self.amount1)
            if self.amount1 is -1:
                self.root.ids.input_country_amount.disabled = True
                self.root.ids.input_home_country_amount.disabled = True
            self.root.ids.input_country_amount.text = str(self.amount1)
            self.root.ids.status.text = "{}({}) -> {}({})".format(self.country_details1[1],  self.country_details1[2],  self.country_details2[1], self.country_details2[2])

    def clear_textinput(self):
        if self.root.ids.input_country_amount.focus is True:
            self.root.ids.input_home_country_amount.text = ''
        elif self.root.ids.input_home_country_amount.focus is True:
            self.root.ids.input_country_amount.text = ''










ForeignExchangeCalculator().run()
