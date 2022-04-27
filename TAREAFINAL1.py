from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def focus_next(event):
    event.widget.tk_focusNext().focus()

raiz=Tk()
raiz.config(width=600, height=400)
raiz.title("App inventario")
raiz.iconbitmap("ICONO.ico")
miframe=Frame(raiz)
miframe.config(width=100,height=50)
miframe.pack()

menubar= Menu(raiz)
raiz.config(menu=menubar)

#labelsss--------------------------
#producto

nombre=Label(miframe,text="Ingrese Producto :")
nombre.grid(row=0,column=0,sticky= E + W)

nombreentry=Entry(miframe,justify=CENTER)
nombreentry.grid(row=0,column=1,sticky= E + W)
nombreentry.focus()

#costo---------------------------
costo=Label(miframe,text="Ingrese costo :")
costo.grid(row=1,column=0,sticky= E + W)

costoentry=Entry(miframe,justify=CENTER)
costoentry.grid(row=1,column=1,sticky= E + W)
costoentry.tk_focusNext()#.focus()

#precio-------------------------
precio=Label(miframe,text="Ingrese Precio :")
precio.grid(row=2,column=0,sticky= E + W)

precioentry=Entry(miframe,justify=CENTER)
precioentry.grid(row=2,column=1,sticky= E + W)

#stock--------------------
Stock=Label(miframe,text="Ingrese Stock :")
Stock.grid(row=3,column=0,sticky= E + W)

Stockentry=Entry(miframe,justify=CENTER)
Stockentry.grid(row=3,column=1,sticky= E + W)

raiz.bind("<Return>", focus_next)

#mensaje----------------------------------
mensaje=Label(miframe)
mensaje.grid(row=5,columnspan=2,sticky=E+W)

#tabla--------------------

cantcol=('#1','#2','#3')
tabla= ttk.Treeview(miframe,height=10,columns=cantcol)

tabla.heading('#0',text="Producto",anchor=CENTER)
tabla.heading('#1',text="Costo",anchor=CENTER)
tabla.heading('#2',text="Precio",anchor=CENTER)
tabla.heading('#3',text="Stock",anchor=CENTER)
tabla.grid(row=6,columnspan=2,sticky=E+W)


scrollbar = ttk.Scrollbar(miframe,orient="vertical",command=tabla.yview)
scrollbar.grid(row=6,column=3,sticky=N+S)
tabla.configure(yscrollcommand=scrollbar.set)

#conexion y consultas bb.oo------------------------------------------

conn=sqlite3.connect("TAREAFINAL.db")


def seleccion():
	if (tabla.get_children()) != "":
		tabla.delete(*tabla.get_children())

	micursor=conn.cursor()
	sql="SELECT * FROM TAREAFINAL ORDER BY PRODUCTO DESC"
	micursor.execute(sql)
	resultado=micursor.fetchall()	

	for row in resultado:
		
		tabla.insert("",0,text=row[1],values=(row[2],row[3],row[4]))
	
def insertdato():
	micursor=conn.cursor()
	datos=(nombreentry.get(),costoentry.get(),precioentry.get(),Stockentry.get())
	sql="INSERT INTO TAREAFINAL VALUES(null,?,?,?,?)"
	micursor.execute(sql,datos)
	conn.commit()
	mensaje.config(text= "<<El Producto {} se ingreso con exito>>".format(nombreentry.get()))
	nombreentry.delete(0,END)
	costoentry.delete(0,END)
	precioentry.delete(0,END)
	Stockentry.delete(0,END)
	seleccion()

def delete():
	mensaje.config(text="")
	
	micursor=conn.cursor()
	dato=(tabla.item(tabla.selection())['text'])

	if dato =="":
		mensaje.config(text="<< Seleccione Producto o Actualice la tabla >>",fg="blue")
		
		return

	valor=messagebox.askquestion("Borrar","Seguro desea borrar")
	if valor=='yes':
		sql="DELETE FROM TAREAFINAL WHERE PRODUCTO = ?"
		micursor.execute(sql,[dato])
		conn.commit()
		mensaje.config(text="El Producto {} se elimino satifactoriamente".format(dato),fg="red")
		seleccion()

#toplevel----------------------------------
def Edicion():
	dato=(tabla.item(tabla.selection())['text'])
	if dato=="":
		mensaje.config(text="<< Seleccione Producto que desea actualizar >>",fg="blue")
		return
	else:
		editwin=Toplevel()
		editwin.title("Edicion")
		editwin.iconbitmap("ICONO.ico")
		Label(editwin,text="Ingrese nuevo nombre").grid(row=0,column=0)
		newname=Entry(editwin)
		newname.grid(row=0,column=1)

		Label(editwin,text="Ingrese nuevo costo").grid(row=1,column=0)
		newcost=Entry(editwin)
		newcost.grid(row=1,column=1)

		Label(editwin,text="Ingrese nuevo precio").grid(row=2,column=0)
		newprice=Entry(editwin)
		newprice.grid(row=2,column=1)

		Label(editwin,text="Ingrese nuevo stock").grid(row=3,column=0)
		newstock=Entry(editwin)
		newstock.grid(row=3,column=1)

	def recordedit():
		micursor=conn.cursor()
		mensaje.config(text="")
		dato=newname.get()
		dato1=newcost.get()
		dato2=newprice.get()
		dato3=newstock.get()
		dato4=tabla.item(tabla.selection())['text']
		dato5=tabla.item(tabla.selection())['values'][0]
		dato6=tabla.item(tabla.selection())['values'][1]
		dato7=tabla.item(tabla.selection())['values'][2]
		
		
		sql= "UPDATE TAREAFINAL SET PRODUCTO=?, COSTO=?, PRECIO =?, STOCK=? WHERE PRODUCTO=? AND COSTO=? AND PRECIO=? AND STOCK=?" 
		micursor.execute(sql,[dato,dato1,dato2,dato3,dato4,dato5,dato6,dato7])
		conn.commit()
		editwin.destroy()
		mensaje.config(text="<<El Producto {} se actualizo satifactoriamente>>".format(dato),fg="red")

	editbutton=Button(editwin,text="Guardar cambios",command=recordedit)
	editbutton.grid(row=4,column=0,columnspan=2)

#BOTONES-------------------------------
	
ingresobd=Button(miframe,text="Agregar Producto",command=insertdato)
ingresobd.grid(row=4,columnspan=2,sticky=E+W)

botondel=Button(miframe,text="Delete",command=delete)
botondel.grid(row=7,column=0,sticky=E+W)

botondelete=Button(miframe,text="Update",command=Edicion)
botondelete.grid(row=7,column=1,sticky=E+W)

actualizarbd=Button(miframe,text="Actualizar Tabla",command=seleccion)
actualizarbd.grid(row=8,column=0,columnspan=2,sticky=E+W)

def salir():
	raiz.destroy()

archivomenu=Menu(menubar,tearoff=0)
archivomenu.add_command(label= "Connect",command=seleccion)
archivomenu.add_separator()
archivomenu.add_command(label= "Salir",command= salir)
menubar.add_cascade(label="Archivo",menu=archivomenu)

raiz.mainloop()  
 