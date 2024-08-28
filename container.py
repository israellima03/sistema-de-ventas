from tkinter import *
import tkinter as tk

class Container(tk.Frame):
    def _init_(self, padre, controlador):
        super()._init_(padre)
        self.pack()
        self.place(x=0, y=0, width=800, height=400)
        #color de la ventana
        self.config(bg="#C6D9E3")