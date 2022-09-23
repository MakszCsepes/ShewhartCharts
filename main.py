# pythonXXX,
# REQUIRED: matplotlib, numpy

import csv
from csv import reader, writer
from ReadDataFromFile import GetCSVData

from Card import Card
import matplotlib.pyplot as plt
import numpy as np

Values = []
X_axis = []


card = Card(X_axis, Values)


# RETURNS: list of cards (`Card` class)
def CreateCards():
    CountriesHDI = GetCSVData()

    XAxisValues = list(CountriesHDI[0].keys())
    XAxisValues.remove('Country')
    Years = []
    for i in XAxisValues:
        Years.append(int(i))
    Years.sort()
    XAxisValues.sort()

    Cards = []
    for country in CountriesHDI:
        X = []
        for year in XAxisValues:
            if country[year].replace('.', '', 1).isdigit():
                X.append(float(country[year]))
            else:
                X.append(0.0)

        Cards.append(Card(Years, X, country['Country']))

    return Cards


def CreateAxis():
    cards = CreateCards()

    cards_len = len(cards)

    axs = tuple([] for _ in range(cards_len))

    cards_len = 1

    fig, axes = plt.subplots(1, cards_len, figsize=(100, 100))

    axes.set_xlabel('Years')
    axes.set_ylabel('HDI Value')
    axes.set_title(cards[0].Name + "'s HDI from 1990 to 2019")
    cards[0].plot(axes)
    axes.legend()
    # for i in range(0, cards_len):
    #     axes[i].set_xlabel('Years')
    #     axes[i].set_ylabel('HDI Value')
    #     axes[i].set_title(cards[i].Name + "'s HDI from 1990 to 2019")
    #     cards[i].plot(axes[i])
    #     axes[i].legend()

    plt.show("chart")


# CreateAxis()

print(GetCSVData("HDI_Ukraine.csv"))
