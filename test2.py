import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
from datetime import datetime

class FileTransferApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Transfer App")
        
        self.local_folder = tk.StringVar(value="")  # Variable para la carpeta local
        self.network_folder = tk.StringVar(value="")  # Variable para la carpeta en red
        self.destination_folder = tk.StringVar(value="")  # Variable para la carpeta destino
        self.log_text = tk.StringVar(value="")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Botones para seleccionar carpetas
        self.select_local_button = tk.Button(self, text="Carpeta Origen", command=self.select_local_folder)
        self.select_local_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.local_folder_entry = tk.Entry(self, textvariable=self.local_folder, width=50)
        self.local_folder_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.select_network_button = tk.Button(self, text="Carpeta Red", command=self.select_network_folder)
        self.select_network_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.network_folder_entry = tk.Entry(self, textvariable=self.network_folder, width=50)
        self.network_folder_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.select_destination_button = tk.Button(self, text="Carpeta Destino", command=self.select_destination_folder)
        self.select_destination_button.grid(row=2, column=0, padx=5, pady=5)
        
        self.destination_folder_entry = tk.Entry(self, textvariable=self.destination_folder, width=50)
        self.destination_folder_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Resto de los widgets
        # Etiqueta e indicador de conexión
        self.connection_label = tk.Label(self, text="Conexión:")
        self.connection_label.grid(row=3, column=0, sticky="w")
        
        self.connection_indicator = tk.Label(self, bg="red", width=10, height=1)
        self.connection_indicator.grid(row=3, column=1, sticky="w")
        
        # Botón de prueba de conexión
        self.test_connection_button = tk.Button(self, text="Test de Conexión", command=self.test_connection)
        self.test_connection_button.grid(row=3, column=2, padx=5, pady=5)
        
        # Botón de enviar archivos
        self.send_files_button = tk.Button(self, text="Enviar Archivos", command=self.send_files)
        self.send_files_button.grid(row=3, column=3, padx=5, pady=5)
        
        # Log
        self.log_label = tk.Label(self, text="Log:")
        self.log_label.grid(row=4, column=0, sticky="w")
        
        self.log_textbox = tk.Text(self, height=10, width=60)
        self.log_textbox.grid(row=5, column=0, columnspan=4, padx=5, pady=5)
        
        self.log_textbox.insert(tk.END, self.log_text.get())
        
    def select_local_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.local_folder.set(folder_selected)
        
    def select_network_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.network_folder.set(folder_selected)
        
    def select_destination_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.destination_folder.set(folder_selected)
    
    def test_connection(self):
        # Aquí deberías agregar la lógica para probar la conexión a la carpeta en red
        # Puedes usar sockets, ping, u otras formas dependiendo de tu red y restricciones
        # Por ahora, simplemente cambiamos el indicador a verde
        self.connection_indicator.config(bg="green")
    
    def send_files(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        zip_filename = f"files_{timestamp}.zip"
        log_entry = f"{timestamp}: "
        
        try:
            # Comprimir archivos
            shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', self.local_folder.get())
            
            # Copiar archivos comprimidos
            shutil.copy(zip_filename, self.destination_folder.get())
            shutil.copy(zip_filename, self.network_folder.get())
            
            # Agregar entrada de log exitosa
            log_entry += f"Envío exitoso. Tamaño: {os.path.getsize(zip_filename)} bytes. Origen: {self.local_folder.get()}. Destino: {self.destination_folder.get()}, {self.network_folder.get()}."
            self.log_textbox.insert(tk.END, log_entry + "\n")
            self.log_textbox.tag_add("success", "1.0", "1.end")
            self.log_textbox.tag_config("success", underline=True, foreground="green")
        except Exception as e:
            # Agregar entrada de log de error
            log_entry += f"Error al enviar: {str(e)}"
            self.log_textbox.insert(tk.END, log_entry + "\n")
            self.log_textbox.tag_add("error", "1.0", "1.end")
            self.log_textbox.tag_config("error", underline=True, foreground="red")
        
        self.log_textbox.see(tk.END)  # Desplazar hacia abajo para mostrar la última entrada

if __name__ == "__main__":
    app = FileTransferApp()
    app.mainloop()