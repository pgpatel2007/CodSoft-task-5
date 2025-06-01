import tkinter as tk
from tkinter import messagebox
import json
import os

FILE = 'contacts.json'

def load():
    if os.path.exists(FILE):
        try:
            with open(FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save(data):
    with open(FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add():
    n = ent_n.get()
    p = ent_p.get()
    e = ent_e.get()
    a = ent_a.get()

    if not n or not p:
        messagebox.showwarning("Missing Info", "Name and Phone are required!")
        return

    data.append({"name": n, "phone": p, "email": e, "address": a})
    save(data)
    refresh()
    clear()

def search():
    q = ent_s.get().lower()
    res = [c for c in data if q in c['name'].lower() or q in c['phone']]
    refresh(res)

def update():
    global sel_idx
    if sel_idx is None:
        messagebox.showwarning("No selection", "Please select a contact to update.")
        return
    data[sel_idx] = {
        "name": ent_n.get(),
        "phone": ent_p.get(),
        "email": ent_e.get(),
        "address": ent_a.get()
    }
    save(data)
    refresh()
    clear()

def delete():
    global sel_idx
    if sel_idx is None:
        messagebox.showwarning("No selection", "Please select a contact to delete.")
        return
    data.pop(sel_idx)
    save(data)
    refresh()
    clear()

def refresh(view=None):
    lst.delete(0, tk.END)
    view = view if view is not None else data
    for c in view:
        lst.insert(tk.END, f"{c['name']} - {c['phone']}")

def clear():
    global sel_idx
    sel_idx = None
    ent_n.delete(0, tk.END)
    ent_p.delete(0, tk.END)
    ent_e.delete(0, tk.END)
    ent_a.delete(0, tk.END)

def select(e):
    global sel_idx
    if not lst.curselection():
        return
    sel_idx = lst.curselection()[0]
    c = data[sel_idx]
    ent_n.delete(0, tk.END)
    ent_p.delete(0, tk.END)
    ent_e.delete(0, tk.END)
    ent_a.delete(0, tk.END)
    ent_n.insert(0, c['name'])
    ent_p.insert(0, c['phone'])
    ent_e.insert(0, c['email'])
    ent_a.insert(0, c['address'])

root = tk.Tk()
root.title("Contact Book")

data = load()
sel_idx = None

tk.Label(root, text="Name").grid(row=0, column=0)
tk.Label(root, text="Phone").grid(row=1, column=0)
tk.Label(root, text="Email").grid(row=2, column=0)
tk.Label(root, text="Address").grid(row=3, column=0)

ent_n = tk.Entry(root)
ent_p = tk.Entry(root)
ent_e = tk.Entry(root)
ent_a = tk.Entry(root)

ent_n.grid(row=0, column=1)
ent_p.grid(row=1, column=1)
ent_e.grid(row=2, column=1)
ent_a.grid(row=3, column=1)

tk.Button(root, text="Add", command=add).grid(row=0, column=2)
tk.Button(root, text="Update", command=update).grid(row=1, column=2)
tk.Button(root, text="Delete", command=delete).grid(row=2, column=2)

ent_s = tk.Entry(root)
ent_s.grid(row=4, column=0)
tk.Button(root, text="Search", command=search).grid(row=4, column=1)

lst = tk.Listbox(root, width=50)
lst.grid(row=5, column=0, columnspan=3)
lst.bind('<<ListboxSelect>>', select)

refresh()
root.mainloop()
