from tkinter import *
import tkinter as tk
from ventas import Ventas
from inventario import Inventario
from PIL import Image, ImageTk
import sys
import os


class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=800, height=400)
        #color de la ventana
        self.config(bg="#C6D9E3")
        self.widgets()
    
    def rutas(self, ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase,ruta)    

    def show_frames(self, container):
        top_level = tk.Toplevel(self)
        frame = container(top_level)
        frame.config(bg="#C6D9E3")
        frame.pack(fill="both", expand=True)
        top_level.geometry("1100x650+120+20")
        top_level.resizable(False, False)
        ruta=self.rutas(r"icono.ico")
        top_level.iconbitmap(ruta)

        top_level.transient(self.master)
        top_level.grab_set()
        top_level.focus_set()
        top_level.lift()

    def ventas(self):
        self.show_frames(Ventas)

    def inventario(self):
        self.show_frames(Inventario)

    def widgets(self):
        
        frame1 = tk.Frame(self, bg="#C6D9E3")
        frame1.pack()
        frame1.place(x=0, y=0, width=800, height=400)

        ruta=self.rutas(r"icono/btnventas.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((50,50))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        btnventas = Button(frame1, bg="#f4b400", fg="white", font="sans 18 bold", text="ir a ventas", command=self.ventas)
        btnventas.config(image=imagen_tk, compound=LEFT, padx=50)
        btnventas.image = imagen_tk
        btnventas.place(x=500, y=30, width=240, height=60)

        ruta=self.rutas(r"icono/btninventario.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((50,50))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        btninventario = Button(frame1, bg="#c62e26", fg="white", font="sans 18 bold" ,text="ir a invertario", command=self.inventario)
        btninventario.config(image=imagen_tk, compound=LEFT, padx=50)
        btninventario.image = imagen_tk
        btninventario.place(x=500, y=130, width=240, height=60)

        ruta=self.rutas(r"imagenes/images.png")
        self.logo_image = Image.open(ruta)
        self.logo_image = self.logo_image.resize((280,280))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(frame1, image=self.logo_image, bg="#C6D9E3")
        self.logo_label.place(x=100, y=30)


        copyright_label = tk.Label(frame1, text="© 2024 Lima technology corporation. Todos los derechos Reservado", font="sans 12 bold", bg="#C6D9E3", fg="gray")
        copyright_label.place(x=180, y=350)

  