import tkinter as tk
from tkinter import filedialog
import pickle
import os

class FolderSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Selector App")
        
        # Cargar la carpeta seleccionada desde la memoria de la aplicación
        self.folder_path = self.load_folder_path()

        # Crear el botón para seleccionar la carpeta
        self.select_button = tk.Button(root, text="Seleccionar Carpeta", command=self.select_folder)
        self.select_button.pack(pady=10)

        # Etiqueta para mostrar la carpeta seleccionada
        self.folder_label = tk.Label(root, text=self.folder_path)
        self.folder_label.pack(pady=5)


    def select_folder(self):
        # Abrir el cuadro de diálogo para seleccionar una carpeta
        folder_path = filedialog.askdirectory()

        if folder_path:
            # Actualizar la etiqueta con la nueva carpeta seleccionada
            self.folder_path = folder_path
            self.folder_label.config(text=self.folder_path)

            # Guardar la carpeta seleccionada en la memoria de la aplicación
            self.save_folder_path(self.folder_path)

    def save_folder_path(self, folder_path):
        # Guardar la carpeta seleccionada usando el módulo pickle
        with open("folder_path.pkl", "wb") as file:
            pickle.dump(folder_path, file)

    def load_folder_path(self):
        # Cargar la carpeta seleccionada desde la memoria de la aplicación, si existe
        if os.path.exists("folder_path.pkl"):
            with open("folder_path.pkl", "rb") as file:
                return pickle.load(file)
        else:
            return "Ninguna carpeta seleccionada"


if __name__ == "__main__":
    root = tk.Tk()
    app = FolderSelectorApp(root)
    root.mainloop()