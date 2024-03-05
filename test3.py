import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
from datetime import datetime, timedelta
import pickle

class FileTransferApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TEXTILE SOURCING COMPANY - ETON BACKUP")
        self.geometry("550x400")
        self.resizable(False, False)
        self.load_config()
        self.log_entries = []
        self.filter_log_entries()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Botones para seleccionar carpetas
        self.source_folder_button = tk.Button(self, width=15, text="CARPETA ORIGEN", command=self.select_source_folder)
        self.source_folder_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.source_folder_label = tk.Label(self, width=45, text=self.source_folder, state='disabled')
        self.source_folder_label.grid(row=0, column=1, columnspan=3, sticky="e", padx=5, pady=5)
        
        self.dest_folder_button = tk.Button(self, width=15, text="CARPETA DESTINO", command=self.select_dest_folder)
        self.dest_folder_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.dest_folder_label = tk.Label(self, width=45, text=self.dest_folder, state='disabled')
        self.dest_folder_label.grid(row=1, column=1, columnspan=3, sticky="e", padx=5, pady=5)
        
        self.network_folder_button = tk.Button(self, width=15, text="CARPETA RED", command=self.select_network_folder)
        self.network_folder_button.grid(row=2, column=0, padx=5, pady=5)
        
        self.network_folder_label = tk.Label(self, width=45, text=self.network_folder, state='disabled')
        self.network_folder_label.grid(row=2, column=1, columnspan=3, sticky="e", padx=5, pady=5)
        
        # Resto de los widgets
        self.connection_label = tk.Label(self, text="ESTADO:")
        self.connection_label.grid(row=3, column=0, sticky="e")
        
        self.connection_indicator = tk.Label(self, bg="red", width=2, height=1)
        self.connection_indicator.grid(row=3, column=1, sticky="w")
        
        self.test_connection_button = tk.Button(self, text="PROBAR CONEXION", command=self.test_connection)
        self.test_connection_button.grid(row=3, column=2, padx=5, pady=5)
        
        self.send_files_button = tk.Button(self, text="ENVIAR ARCHIVOS", command=self.send_files)
        self.send_files_button.grid(row=3, column=3, padx=5, pady=5)
        
        self.log_label = tk.Label(self, text="REGISTRO DE ENVIOS")
        self.log_label.grid(row=4, column=0, sticky="w")
        
        self.log_textbox = tk.Text(self, height=10, width=60)
        self.log_textbox.grid(row=5, column=0, columnspan=4, padx=5, pady=5)
        
        self.update_log_display()
        
    def load_config(self):
        try:
            with open("config.pickle", "rb") as config_file:
                self.source_folder, self.dest_folder, self.network_folder = pickle.load(config_file)
        except FileNotFoundError:
            self.source_folder = ""
            self.dest_folder = ""
            self.network_folder = ""
    
    def save_config(self):
        with open("config.pickle", "wb") as config_file:
            pickle.dump((self.source_folder, self.dest_folder, self.network_folder), config_file)
    
    def select_source_folder(self):
        folder = tk.filedialog.askdirectory()
        if folder:
            self.source_folder = folder
            self.source_folder_label.config(text=self.source_folder)
            self.save_config()
    
    def select_dest_folder(self):
        folder = tk.filedialog.askdirectory()
        if folder:
            self.dest_folder = folder
            self.dest_folder_label.config(text=self.dest_folder)
            self.save_config()
    
    def select_network_folder(self):
        folder = tk.filedialog.askdirectory()
        if folder:
            self.network_folder = folder
            self.network_folder_label.config(text=self.network_folder)
            self.save_config()
    
    def test_connection(self):
        # Lógica de prueba de conexión aquí
        # Cambiamos el indicador a verde como ejemplo
        self.connection_indicator.config(bg="green")
    
    def send_files(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        zip_filename = f"files_{timestamp}.zip"
        log_entry = f"{timestamp}: "
        
        try:
            shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', self.source_folder)
            shutil.copy(zip_filename, self.dest_folder)
            shutil.copy(zip_filename, self.network_folder)
            
            log_entry += f"Envío exitoso. Tamaño: {os.path.getsize(zip_filename)} bytes. Origen: {self.source_folder}. Destino: {self.dest_folder}, {self.network_folder}."
            self.log_entries.append(log_entry)
            self.save_log()
            self.update_log_display()
        except Exception as e:
            log_entry += f"Error al enviar: {str(e)}"
            self.log_entries.append(log_entry)
            self.save_log()
            self.update_log_display()
        
    def save_log(self):
        with open("log.pickle", "wb") as log_file:
            pickle.dump(self.log_entries, log_file)
    
    def load_log(self):
        try:
            with open("log.pickle", "rb") as log_file:
                self.log_entries = pickle.load(log_file)
        except FileNotFoundError:
            self.log_entries = []
    
    def filter_log_entries(self):
        self.load_log()
        now = datetime.now()
        one_week_ago = now - timedelta(weeks=1)
        self.log_entries = [entry for entry in self.log_entries if datetime.strptime(entry[:19], "%Y-%m-%d_%H-%M-%S") > one_week_ago]
    
    def update_log_display(self):
        self.filter_log_entries()
        self.log_textbox.delete(1.0, tk.END)
        for entry in self.log_entries:
            self.log_textbox.insert(tk.END, entry + "\n")
        self.log_textbox.see(tk.END)

if __name__ == "__main__":
    app = FileTransferApp()
    app.mainloop()