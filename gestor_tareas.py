import tkinter as tk
from tkinter import messagebox
import json
import sqlite3

#nombre de la base de datos
DB_NAME= "tareas.db"


#creacion de la base de datos, creacion de la tabla con SQL
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'pendiente')''')
conn.commit()


def agregar_tarea():
    titulo = entry_titulo.get()
    descripcion =entry_descripcion.get("1.0", tk.END).strip()

    if not titulo or not descripcion:
        messagebox.showwarning("Campos vacios", "Debe llenar todos los campos.")
        return
    
    c.execute("INSERT INTO tareas (titulo, descripcion) VALUES (?, ?)", (titulo, descripcion))
    conn.commit()
    listar_tareas()
    entry_titulo.delete(0, tk.END)
    entry_descripcion.delete("1.0", tk.END)

def listar_tareas():
    for widget in frame_tareas.winfo_children():
        widget.destroy()

    c.execute("SELECT * FROM tareas")
    tareas = c.fetchall()

    for tarea in tareas:
        id_tarea, titulo, _, estado = tarea
        color = "green" if estado == "completada" else "red"
        tarea_label = tk.Label(frame_tareas, text=f"{id_tarea}. {titulo} - {estado}", fg=color)
        tarea_label.pack(anchor="w")

        btn_completar = tk.Button(frame_tareas, text="Completar", command=lambda t=id_tarea: completar_tarea(t))
        btn_completar.pack()

        btn_eliminar = tk.Button(frame_tareas, text="Eliminar", command=lambda t=id_tarea: eliminar_tarea(t))
        btn_eliminar.pack()


def completar_tarea(id_tarea):
    c.execute("UPDATE tareas SET estado='completada' WHERE id=?", (id_tarea,))
    conn.commit()
    listar_tareas()

def eliminar_tarea(id_tarea):
    c.execute("DELETE FROM tareas WHERE id=?", (id_tarea,))
    conn.commit()
    listar_tareas()

def guardar_tareas():
    c.execute("SELECT * FROM tareas")
    tareas = c.fetchall()
    with open("tareas.json", "w") as f:
        json.dump(tareas, f)
    messagebox.showinfo("Guardado", "Tareas guardadas en tareas.json")

def cargar_tareas():
    try:
        with open("tareas.json", "r") as f:
            tareas = json.load(f)
        c.executemany("INSERT INTO tareas (id, titulo, descripcion, estado) VALUES (?, ?, ?, ?)", tareas)
        conn.commit()
        listar_tareas()
        messagebox.showinfo("Cargado", "Tareas cargadas desde tareas.json")
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontro el archivo tareas.json")


#interfaz grafica

root = tk.Tk()
root.title('Gestion de Tareas')


frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

label_titulo = tk.Label(frame_inputs, text="Titulo:")
label_titulo.grid(row=0, column=0)
entry_titulo = tk.Entry(frame_inputs)
entry_titulo.grid(row=0, column=1)

label_descripcion = tk.Label(frame_inputs, text="Descripcion:")
label_descripcion.grid(row=1, column=0)
entry_descripcion = tk.Text(frame_inputs, height=5, width=40)
entry_descripcion.grid(row=1, column=1)

btn_agregar = tk.Button(frame_inputs, text="Agregar Tarea", command=agregar_tarea)
btn_agregar.grid(row=2, column=0, columnspan=2, pady=10)

frame_tareas = tk.Frame(root)
frame_tareas.pack(pady=10)

frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

btn_guardar = tk.Button(frame_botones, text="Guardar Tareas", command=guardar_tareas)
btn_guardar.grid(row=0, column=0, padx=5)

btn_guardar = tk.Button(frame_botones, text="Cargar Tareas", command=cargar_tareas)
btn_guardar.grid(row=0, column=1, padx=5)

listar_tareas()

root.mainloop()

conn.close()

