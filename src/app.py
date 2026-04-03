"""
Library Management System (LMS)
Tech: Python + Tkinter + JSON
"""

import json
import os
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "library.json"

# -----------------------------
# Data Handling
# -----------------------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except:
            return []


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def generate_id(data):
    if not data:
        return 1
    return max(book['id'] for book in data) + 1

# -----------------------------
# Core Functions
# -----------------------------

def add_book():
    data = load_data()

    title = entry_title.get()
    author = entry_author.get()
    year = entry_year.get()

    if not title or not author or not year:
        messagebox.showerror("Error", "All fields are required")
        return

    book = {
        "id": generate_id(data),
        "title": title,
        "author": author,
        "year": year
    }

    data.append(book)
    save_data(data)

    messagebox.showinfo("Success", "Book added successfully")
    clear_fields()
    view_books()


def view_books():
    listbox.delete(0, tk.END)
    data = load_data()

    for book in data:
        listbox.insert(tk.END, f"{book['id']} | {book['title']} | {book['author']} | {book['year']}")


def delete_book():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Select a book first")
        return

    data = load_data()
    index = selected[0]
    book_id = data[index]['id']

    new_data = [b for b in data if b['id'] != book_id]
    save_data(new_data)

    messagebox.showinfo("Success", "Book deleted")
    view_books()


def update_book():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Select a book first")
        return

    data = load_data()
    index = selected[0]

    title = entry_title.get()
    author = entry_author.get()
    year = entry_year.get()

    if not title or not author or not year:
        messagebox.showerror("Error", "All fields are required")
        return

    data[index]['title'] = title
    data[index]['author'] = author
    data[index]['year'] = year

    save_data(data)

    messagebox.showinfo("Success", "Book updated")
    view_books()


def fill_fields(event):
    selected = listbox.curselection()
    if not selected:
        return

    data = load_data()
    book = data[selected[0]]

    clear_fields()
    entry_title.insert(0, book['title'])
    entry_author.insert(0, book['author'])
    entry_year.insert(0, book['year'])


def clear_fields():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_year.delete(0, tk.END)

# -----------------------------
# GUI
# -----------------------------

root = tk.Tk()
root.title("Library Management System")
root.geometry("600x400")

# Labels

tk.Label(root, text="Title").pack()
entry_title = tk.Entry(root, width=40)
entry_title.pack()

tk.Label(root, text="Author").pack()
entry_author = tk.Entry(root, width=40)
entry_author.pack()

tk.Label(root, text="Year").pack()
entry_year = tk.Entry(root, width=40)
entry_year.pack()

# Buttons

tk.Button(root, text="Add Book", command=add_book).pack(pady=5)
tk.Button(root, text="Update Book", command=update_book).pack(pady=5)
tk.Button(root, text="Delete Book", command=delete_book).pack(pady=5)
tk.Button(root, text="View Books", command=view_books).pack(pady=5)

# Listbox

listbox = tk.Listbox(root, width=80)
listbox.pack(pady=10)
listbox.bind('<<ListboxSelect>>', fill_fields)

view_books()

root.mainloop()
