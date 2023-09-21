import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import shutil

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Manager")
        self.create_ui()

    def create_ui(self):
        self.file_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.file_listbox.pack(pady=10)
        self.refresh_file_list()

        self.create_button = tk.Button(self.root, text="Create", command=self.create_item)
        self.create_button.pack()
        self.rename_button = tk.Button(self.root, text="Rename", command=self.rename_item)
        self.rename_button.pack()
        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_item)
        self.delete_button.pack()
        self.copy_button = tk.Button(self.root, text="Copy", command=self.copy_item)
        self.copy_button.pack()
        self.move_button = tk.Button(self.root, text="Move", command=self.move_item)
        self.move_button.pack()
        self.search_button = tk.Button(self.root, text="Search", command=self.search_files)
        self.search_button.pack()
        self.properties_button = tk.Button(self.root, text="Properties", command=self.display_properties)
        self.properties_button.pack()

    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        current_dir = os.getcwd()
        items = os.listdir(current_dir)
        for item in items:
            self.file_listbox.insert(tk.END, item)

    def create_item(self):
        current_dir = os.getcwd()
        item_name = filedialog.askstring("Create", "Enter a name for the new item:")
        if item_name:
            try:
                os.mkdir(os.path.join(current_dir, item_name))
                self.refresh_file_list()
            except FileExistsError:
                messagebox.showerror("Error", f"'{item_name}' already exists.")

    def rename_item(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            current_dir = os.getcwd()
            selected_item = self.file_listbox.get(selected_index)
            new_name = filedialog.askstring("Rename", f"Rename '{selected_item}' to:")
            if new_name:
                try:
                    os.rename(os.path.join(current_dir, selected_item), os.path.join(current_dir, new_name))
                    self.refresh_file_list()
                except FileNotFoundError:
                    messagebox.showerror("Error", f"'{selected_item}' not found.")

    def delete_item(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            current_dir = os.getcwd()
            selected_item = self.file_listbox.get(selected_index)
            if os.path.isdir(os.path.join(current_dir, selected_item)):
                try:
                    os.rmdir(os.path.join(current_dir, selected_item))
                    self.refresh_file_list()
                except FileNotFoundError:
                    messagebox.showerror("Error", f"'{selected_item}' not found.")
            else:
                try:
                    os.remove(os.path.join(current_dir, selected_item))
                    self.refresh_file_list()
                except FileNotFoundError:
                    messagebox.showerror("Error", f"'{selected_item}' not found.")

    def copy_item(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            current_dir = os.getcwd()
            selected_item = self.file_listbox.get(selected_index)
            destination = filedialog.askdirectory(title="Select Destination Directory")
            if destination:
                try:
                    if os.path.isdir(os.path.join(current_dir, selected_item)):
                        shutil.copytree(os.path.join(current_dir, selected_item), os.path.join(destination, selected_item))
                    else:
                        shutil.copy(os.path.join(current_dir, selected_item), os.path.join(destination, selected_item))
                    self.refresh_file_list()
                except FileNotFoundError:
                    messagebox.showerror("Error", f"'{selected_item}' not found.")

    def move_item(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            current_dir = os.getcwd()
            selected_item = self.file_listbox.get(selected_index)
            destination = filedialog.askdirectory(title="Select Destination Directory")
            if destination:
                try:
                    os.rename(os.path.join(current_dir, selected_item), os.path.join(destination, selected_item))
                    self.refresh_file_list()
                except FileNotFoundError:
                    messagebox.showerror("Error", f"'{selected_item}' not found.")

    def search_files(self):
        search_term = filedialog.askstring("Search", "Enter search term:")
        if search_term:
            current_dir = os.getcwd()
            matching_files = []
            for root, dirs, files in os.walk(current_dir):
                for file in files:
                    if search_term in file:
                        matching_files.append(os.path.join(root, file))
            if matching_files:
                messagebox.showinfo("Search Results", "\n".join(matching_files))
            else:
                messagebox.showinfo("Search Results", "No matching files found.")

    def display_properties(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            current_dir = os.getcwd()
            selected_item = self.file_listbox.get(selected_index)
            item_path = os.path.join(current_dir, selected_item)
            if os.path.exists(item_path):
                item_properties = []
                item_properties.append(f"Name: {selected_item}")
                item_properties.append(f"Path: {item_path}")
                item_properties.append(f"Size: {os.path.getsize(item_path)} bytes")
                item_properties.append(f"Last Modified: {datetime.fromtimestamp(os.path.getmtime(item_path))}")
                messagebox.showinfo("File Properties", "\n".join(item_properties))
            else:
                messagebox.showerror("Error", f"'{selected_item}' not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
