import os

def mantener_archivo_mas_reciente(ruta):
    archivos = os.listdir(ruta)
    if not archivos:
        print("No hay archivos en la carpeta.")
        return
    
    archivo_mas_reciente = max(archivos, key=lambda x: os.path.getmtime(os.path.join(ruta, x)))

    for archivo in archivos:
        ruta_absoluta = os.path.join(ruta, archivo)
        if archivo != archivo_mas_reciente:
            os.remove(ruta_absoluta)

if __name__ == "__main__":
    ruta_carpeta = r'D:\\BKBD_S\\SIGE_TSC'
    mantener_archivo_mas_reciente(ruta_carpeta)