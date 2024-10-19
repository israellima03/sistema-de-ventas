import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox


class Inventario(tk.Frame):

    db_name = "database.db"

    def __init__(self, padre):
        super().__init__(padre)
        self.pack()
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.widgets()

    def widgets(self):

        frame1 = tk.Frame(self, bg="#dddddd", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0 , y=0, width=1100, height=100)

        titulo = tk.Label(self, text="INVENTARIOS", bg="#dddddd", font="sans 30 bold", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)
        
        frame2 = tk.Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)

        labelframe = LabelFrame(frame2, text="productos", font="sans 22 bold", bg="#C6D9E3")
        labelframe.place(x=20, y=30, width=400, height=500)

        lblnombre = Label(labelframe, text="nombre: ", font="sans 14 bold", bg="#C6D9E3")
        lblnombre.place(x=10, y=20)
        self.nombre = ttk.Entry(labelframe, font="sans 14 bold")
        self.nombre.place(x=140, y=20, width=240, height=40)

        lblproveedor = Label(labelframe, text="proveedor", font="sans 14 bold", bg="#C6D9E3")
        lblproveedor.place(x=10, y=80)
        self.proveedor = ttk.Entry(labelframe, font="sans 14 bold")
        self.proveedor.place(x=140, y=80, width=240, height=40)

        lblprecio = Label(labelframe, text="precio: ", font="sans 14 bold", bg="#C6D9E3")
        lblprecio.place(x=10, y=140)
        self.precio = ttk.Entry(labelframe, font="sans 14 bold")
        self.precio.place(x=140, y=140, width=240, height=40)

        lblcosto = Label(labelframe, text="costo: ", font="sans 14 bold", bg="#C6D9E3")
        lblcosto.place(x=10, y=200)
        self.costo = ttk.Entry(labelframe, font="sans 14 bold")
        self.costo.place(x=140, y=200, width=240, height=40)

        lblstock = Label(labelframe, text="stock: ", font="sans 14 bold", bg="#C6D9E3")
        lblstock.place(x=10, y=260)
        self.stock = ttk.Entry(labelframe, font="sans 14 bold")
        self.stock.place(x=140, y=260, width=240, height=40)

        boton_agregar = tk.Button(labelframe, text="ingresar", font="sans 14 bold", bg="#dddddd", command=self.registrar)
        boton_agregar.place(x=80, y=340, width=240, height=40)       

        boton_editar = tk.Button(labelframe, text="editar", font="sans 14 bold", bg="#dddddd", command=self.editar_producto)
        boton_editar.place(x=80, y=400, width=240, height=40)
        

        #Tabla
        treFrame = Frame(frame2, bg="white")
        treFrame.place(x=440, y=50, width=620, height=400)

        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40, columns=("id", "producto", "proveedor", "precio", "costo", "stock"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        self.tre.heading("id", text="id")
        self.tre.heading("producto", text="producto")
        self.tre.heading("proveedor", text="proveedor")
        self.tre.heading("precio", text="precio")
        self.tre.heading("costo", text="costo")
        self.tre.heading("stock", text="stock")

        self.tre.column("id", width=70, anchor="center")
        self.tre.column("producto", width=100, anchor="center")
        self.tre.column("proveedor", width=100, anchor="center")
        self.tre.column("precio", width=100, anchor="center")
        self.tre.column("costo", width=100, anchor="center")
        self.tre.column("stock", width=70, anchor="center")

        self.mostrar()

        btn_actualizar = Button(frame2, text="Actualizar Inventario", font="sans 14 bold", command=self.actualizar_inventario)
        btn_actualizar.place(x=440, y=480, width=260, height=50)
    
    def eje_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(consulta, parametros)
            conn.commit()
        return result
    
    def validacion(self, nombre, prov, precio, costo, stock):
        if not (nombre and prov and precio and costo and stock):
            return False
        try:
            float(precio)
            float(costo)
            int(stock)
        except ValueError:
            return False
        return True
    
    def mostrar(self):
        consulta = "SELECT * FROM inventario ORDER BY id DESC"
        result = self.eje_consulta(consulta)
        for elem in result:
            try:
                precio_Bs = "{:,.0f} Bs".format(float(elem[3])) if elem[3] else ""
                costo_Bs = "{:,.0f} Bs".format(float(elem[4])) if elem[4] else ""
            except ValueError:
                precio_Bs = elem[3]
                costo_Bs = elem[4]
            self.tre.insert("", 0, text=elem[0], values=(elem[0], elem[1], elem[2], precio_Bs, costo_Bs, elem[5]))

    def actualizar_inventario(self):
        for item in self.tre.get_children():
            self.tre.delete(item)
        
        self.mostrar()

        messagebox.showinfo("Actualizacion","El inventario ha sido actualizado correctamente.") 

    def registrar(self):
        result = self.tre.get_children()
        for i in result:
            self.tre.delete(i)
        nombre = self.nombre.get()
        prov = self.proveedor.get()
        precio = self.precio.get()
        costo = self.costo.get()
        stock = self.stock.get()
        if self.validacion(nombre, prov, precio, costo, stock):
            try:
                consulta = "INSERT INTO inventario VALUES(?,?,?,?,?,?)"
                parametros = (None, nombre, prov, precio, costo, stock)
                self.eje_consulta(consulta, parametros)
                self.mostrar()
                self.nombre.delete(0, END)
                self.proveedor.delete(0, END)
                self.precio.delete(0, END)
                self.costo.delete(0, END)
                self.stock.delete(0, END)
            except Exception as e:
                messagebox.showwarning(title="Error", message=f"Error al registrar el producto: {e}")
        else:
            messagebox.showwarning(title="Error", message="Rellene todos los campos correctamente")
            self.mostrar()
    
    def editar_producto(self):
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning("Editar producto","Seleccione un producto para editar.")
            return
    
        item_id = self.tre.item(seleccion)["text"]
        item_values = self.tre.item(seleccion)["values"]

        ventana_editar = Toplevel(self)
        ventana_editar.title("Editar producto")
        ventana_editar.geometry("400x400")
        ventana_editar.config(bg="#C6D9E3")

        lbl_nombre = Label(ventana_editar, text="Nombre:", font="sans 14 bold", bg="#C6D9E3")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = Entry(ventana_editar, font="sans 14 bold")
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        entry_nombre.insert(0, item_values[1])

        lbl_proveedor = Label(ventana_editar, text="Proveedor:", font="sans 14 bold", bg="#C6D9E3")
        lbl_proveedor.grid(row=1, column=0, padx=10, pady=10)
        entry_proveedor = Entry(ventana_editar, font="sans 14 bold")
        entry_proveedor.grid(row=1, column=1, padx=10, pady=10)
        entry_proveedor.insert(0, item_values[2])

        lbl_precio = Label(ventana_editar, text="Precio:", font="sans 14 bold", bg="#C6D9E3")
        lbl_precio.grid(row=2, column=0, padx=10, pady=10)
        entry_precio = Entry(ventana_editar, font="sans 14 bold")
        entry_precio.grid(row=2, column=1, padx=10, pady=10)
        entry_precio.insert(0, item_values[3].split()[0].replace(",",""))

        lbl_costo = Label(ventana_editar, text="Costo:", font="sans 14 bold", bg="#C6D9E3")
        lbl_costo.grid(row=3, column=0, padx=10, pady=10)
        entry_costo = Entry(ventana_editar, font="sans 14 bold")
        entry_costo.grid(row=3, column=1, padx=10, pady=10)
        entry_costo.insert(0, item_values[4].split()[0].replace(",",""))

        lbl_stock = Label(ventana_editar, text="Stock:", font="sans 14 bold", bg="#C6D9E3")
        lbl_stock.grid(row=4, column=0, padx=10, pady=10)
        entry_stock = Entry(ventana_editar, font="sans 14 bold")
        entry_stock.grid(row=4, column=1, padx=10, pady=10)
        entry_stock.insert(0, item_values[5])

        def guardar_cambios():
            nombre = entry_nombre.get()
            proveedor = entry_proveedor.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_costo.get()

            if not (nombre and proveedor and precio and costo and stock):
                messagebox.showwarning("Guardar cambios", "Rellene todos los campos.")
                return
            
            try:
                precio = float(precio.replace(",", "")) 
                costo = float(costo.replace(",", ""))
            except ValueError:
                messagebox.showwarning("Guardar cambios", "Ingrese valores numericos validos para precio y costo.")
                return
            
            consulta = "UPDATE inventario SET nombre=?, proveedor=?, precio=?, costo=?, stock=? WHERE id=?"
            parametros = (nombre, proveedor, precio, costo, stock, item_id)
            self.eje_consulta(consulta, parametros)

            self.actualizar_inventario()

            ventana_editar.destroy()

        btn_guardar = Button(ventana_editar, text="Guardar cambios", font="sans 14 bold", command=guardar_cambios)
        btn_guardar.place(x=80, y=250, width=240, height=40)


