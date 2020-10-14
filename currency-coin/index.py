import tkinter as tk
from tkinter import Text, StringVar, Label, RAISED, CENTER, S
import os
import requests
import xml.sax
import xml.etree.ElementTree as ET
from datetime import date
import threading


root = tk.Tk()

root.title("Global currency to ILS")
root.geometry("450x300")
root.configure(background="#263D42")

USD_VAL = 0
EUR_VAL = 0
USD = StringVar()
EUR = StringVar()
label = Label(root, textvariable=USD, width=20)
label2 = Label(root, textvariable=EUR, width=20)

today = date.today()
d1 = today.strftime("%Y%m%d")
currecny_endpoint = "https://www.boi.org.il/currency.xml?rdate="+d1


def fetchCurrencies():
    resp = requests.get(url=currecny_endpoint)
    tree = ET.ElementTree(ET.fromstring(resp.content))
    return tree


def checkDecreaseValue():

    # check if the dollar or euro value decreasd from the current state variables
    tree = fetchCurrencies()
    for currency in tree.findall('CURRENCY'):
        coin = currency.find('CURRENCYCODE').text
        if coin == "USD":
            if USD_VAL > float(currency.find('RATE').text):
                print("Decreased USD!!!")


def refreshCurrency():
    tree = fetchCurrencies()

    for currency in tree.findall('CURRENCY'):
        coin = currency.find('CURRENCYCODE').text
        if coin == "USD":
            USD_VAL = float(currency.find('RATE').text)
            USD.set("USD: "+str(USD_VAL))
        elif coin == "EUR":
            EUR_VAL = float(currency.find('RATE').text)
            EUR.set("EUR: "+str(EUR_VAL))


def on_closing():
    print("destroying...")
    checkDecreaseValue_timer.cancel()
    root.destroy()


label.pack()
label2.pack()
refresh = tk.Button(root, text="Refresh", padx=10, pady=5, anchor=S,
                    fg="black", command=refreshCurrency).place(x=190,  y=150)

root.protocol("WM_DELETE_WINDOW", on_closing)
seconds = 3
checkDecreaseValue_timer = threading.Timer(seconds, checkDecreaseValue)
checkDecreaseValue_timer.run()
root.mainloop()
