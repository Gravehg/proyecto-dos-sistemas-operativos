from tkinter import Tk, filedialog
import shutil
import os

def copiar_archivo():
    # Crear la ventana de diálogo para seleccionar el archivo original
    Tk().withdraw()  # Ocultar la ventana principal de tkinter
    archivo_original = filedialog.askopenfilename(title="Seleccionar archivo original", filetypes=[("Archivos de texto", "*.txt")])

    if archivo_original:
        # Pedir al usuario la ruta y el nombre del archivo de destino
        ruta_completa_destino = filedialog.asksaveasfilename(
            title="Seleccionar carpeta y nombre para la copia",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")]
        )

        # Copiar el archivo seleccionado al destino especificado
        shutil.copy(archivo_original, ruta_completa_destino)

        print(f"Archivo copiado exitosamente a {ruta_completa_destino}")
    else:
        print("No se seleccionó ningún archivo.")

# Ejemplo de uso del método
copiar_archivo()
