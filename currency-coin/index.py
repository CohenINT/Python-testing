import tkinter as tk
from tkinter import Text, StringVar, Label, RAISED, CENTER, S
import os
import requests
import xml.sax
import xml.etree.ElementTree as ET

root = tk.Tk()
root.title("Global currency to ILS")
root.geometry("450x300")
root.configure(background="#263D42")

USD = StringVar()
EUR = StringVar()
label = Label(root, textvariable=USD, width=20)
label2 = Label(root, textvariable=EUR, width=20)
currecny_endpoint = "https://www.boi.org.il/currency.xml?rdate=20201013"


def refreshCurrency():
    resp = requests.get(url=currecny_endpoint)
    tree = ET.ElementTree(ET.fromstring(resp.content))
    for currency in tree.findall('CURRENCY'):
        coin = currency.find('CURRENCYCODE').text
        if coin == "USD":
            USD.set("USD: "+currency.find('RATE').text)
        elif coin == "EUR":
            EUR.set("EUR: "+currency.find('RATE').text)


label.pack()
label2.pack()

# canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
# canvas.pack()

refresh = tk.Button(root, text="Refresh", padx=10, pady=5, anchor=S,
                    fg="black", command=refreshCurrency).place(x=190,  y=150)

# refresh.pack()

root.mainloop()
