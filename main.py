import math
import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import fuerzaBruta

# =============================================================================
# Clases de Datos y Lógica del Problema
# =============================================================================

class GrupoAgente:
    def __init__(self, n, op1, op2, rig):
        self.n = n
        self.op1 = op1
        self.op2 = op2
        self.rig = rig
    
    def __str__(self):
        return f"Agentes: {self.n}, Opinión 1: {self.op1}, Opinión 2: {self.op2}, Rigidez: {self.rig}"

class RedSocial:
    def __init__(self, grupos, R_max):
        self.grupos = grupos
        self.R_max = R_max
    
    def calcular_conflicto_interno(self):
        if not self.grupos:
            return 0
        numerador = sum(grupo.n * (grupo.op1 - grupo.op2)**2 for grupo in self.grupos)
        return numerador / len(self.grupos)
        
    def calcular_esfuerzo(self, estrategia):
        esfuerzo = 0
        for i, e in enumerate(estrategia):
            if e > 0:
                grupo = self.grupos[i]
                esfuerzo += math.ceil(abs(grupo.op1 - grupo.op2) * grupo.rig * e)
        return esfuerzo
    
    def aplicar_estrategia(self, estrategia):
        nuevos_grupos = []
        for i, grupo in enumerate(self.grupos):
            e = estrategia[i]
            nuevo_n = max(grupo.n - e, 0)
            nuevos_grupos.append(GrupoAgente(nuevo_n, grupo.op1, grupo.op2, grupo.rig))
        return RedSocial(nuevos_grupos, self.R_max)

# =============================================================================
# Funciones para manejo de archivos
# =============================================================================

def cargar_datos(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")
    
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()
        n = int(lineas[0].strip())
        grupos = []
        for i in range(1, n+1):
            datos = lineas[i].strip().split(',')
            n_agentes = int(datos[0])
            op1 = int(datos[1])
            op2 = int(datos[2])
            rig = float(datos[3])
            grupos.append(GrupoAgente(n_agentes, op1, op2, rig))
        R_max = int(lineas[n+1].strip())
        return RedSocial(grupos, R_max)

def guardar_resultados(ruta_archivo, estrategia, esfuerzo, conflicto):
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(f"{conflicto}\n")
        archivo.write(f"{esfuerzo}\n")
        for e in estrategia:
            archivo.write(f"{e}\n")

# =============================================================================
# Clase de la Interfaz Gráfica
# =============================================================================

class ModeracionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Moderación de Conflicto Interno en Red Social")
        self.master.geometry("800x600")

        # (Opcional) Cambiar icono si lo deseas
        # try:
        #     self.master.iconbitmap("icon.ico")
        # except:
        #     pass

        # (Opcional) Establecer un estilo TTK
        style = ttk.Style(self.master)
        style.theme_use("clam")
        
        self.entrada_var = tk.StringVar()
        self.salida_var = tk.StringVar()
        self.algoritmo_var = tk.StringVar(value="Fuerza Bruta")
        self.resultado_texto = tk.StringVar()

        self.crear_widgets()

    def crear_widgets(self):
        # Frame principal para usar grid
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill="both", expand=True)
        
        # =========================================
        # 1) LabelFrame de ALGORTIMOS (col=0)
        # =========================================
        frame_algoritmos = ttk.LabelFrame(self.main_frame, text="Algoritmo a utilizar")
        frame_algoritmos.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        algoritmos = ["Fuerza Bruta", "Voraz", "Programación Dinámica"]
        for alg in algoritmos:
            ttk.Radiobutton(
                frame_algoritmos, 
                text=alg, 
                variable=self.algoritmo_var, 
                value=alg
            ).pack(anchor="w", padx=20, pady=2)

        # =========================================
        # 2) LabelFrame de ARCHIVOS (col=1)
        # =========================================
        frame_archivos = ttk.LabelFrame(self.main_frame, text="Archivos")
        frame_archivos.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # -- Archivo de Entrada
        ttk.Label(frame_archivos, text="Archivo de entrada:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entrada_entry = ttk.Entry(frame_archivos, textvariable=self.entrada_var, width=50)
        entrada_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_archivos, text="Seleccionar", command=self.seleccionar_entrada).grid(row=0, column=2, padx=5, pady=5)

        # -- Archivo de Salida
        ttk.Label(frame_archivos, text="Archivo de salida:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        salida_entry = ttk.Entry(frame_archivos, textvariable=self.salida_var, width=50)
        salida_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame_archivos, text="Seleccionar", command=self.seleccionar_salida).grid(row=1, column=2, padx=5, pady=5)

        # =========================================
        # 3) Botón "Ejecutar Algoritmo" (fila=1, col=0..1)
        # =========================================
        ejecutar_btn = ttk.Button(self.main_frame, text="Ejecutar Algoritmo", command=self.ejecutar_algoritmo)
        ejecutar_btn.grid(row=1, column=0, columnspan=2, pady=10)

        # =========================================
        # 4) LabelFrame de RESULTADOS (fila=2, col=0..1)
        # =========================================
        frame_resultados = ttk.LabelFrame(self.main_frame, text="Resultados")
        frame_resultados.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        # -- Caja de texto para resultados
        self.texto_resultado = tk.Text(frame_resultados, wrap="word", width=80, height=15)
        self.texto_resultado.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Al cambiar la variable resultado_texto, actualiza el Text
        self.resultado_texto.trace_add("write", self.actualizar_texto)

        # Ajuste de columnas y filas para que se expandan
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

    def seleccionar_entrada(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona el archivo de entrada",
            filetypes=(("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if ruta:
            self.entrada_var.set(ruta)

    def seleccionar_salida(self):
        ruta = filedialog.asksaveasfilename(
            title="Selecciona el archivo de salida",
            defaultextension=".txt",
            filetypes=(("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if ruta:
            self.salida_var.set(ruta)

    def ejecutar_algoritmo(self):
        ruta_entrada = self.entrada_var.get()
        ruta_salida = self.salida_var.get()
        if not ruta_entrada or not ruta_salida:
            messagebox.showerror("Error", "Por favor, seleccione archivos de entrada y salida")
            return
        
        try:
            red_social = cargar_datos(ruta_entrada)
            algoritmo = self.algoritmo_var.get()
            tiempo_inicio = time.time()
            
            if algoritmo == "Fuerza Bruta":
                resultado = fuerzaBruta.modciFuerzaBruta(red_social)
            elif algoritmo == "Voraz":
                messagebox.showwarning("No Implementado", "La función Voraz aún no está implementada.")
                return
            elif algoritmo == "Programación Dinámica":
                messagebox.showwarning("No Implementado", "La función de Programación Dinámica aún no está implementada.")
                return
            
            tiempo_fin = time.time()
            tiempo_ejecucion = tiempo_fin - tiempo_inicio
            
            estrategia, esfuerzo, conflicto = resultado
            guardar_resultados(ruta_salida, estrategia, esfuerzo, conflicto)
            
            mensaje = (
                f"Algoritmo: {algoritmo}\n"
                f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos\n\n"
                f"Conflicto Interno: {conflicto}\n"
                f"Esfuerzo: {esfuerzo}\n\n"
                "Estrategia de moderación:\n"
            )
            for i, e in enumerate(estrategia):
                grupo = red_social.grupos[i]
                mensaje += f"  • Grupo {i+1} ({grupo.n} agentes): {e} agentes moderados\n"
            
            self.resultado_texto.set(mensaje)
            messagebox.showinfo("Éxito", f"El algoritmo {algoritmo} se ejecutó correctamente.\nResultados guardados en {ruta_salida}")
            
        except Exception as error:
            messagebox.showerror("Error", f"Error al ejecutar el algoritmo:\n{str(error)}")

    def actualizar_texto(self, *args):
        self.texto_resultado.delete("1.0", tk.END)
        self.texto_resultado.insert(tk.END, self.resultado_texto.get())

# =============================================================================
# Ejecución de la aplicación
# =============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = ModeracionApp(root)
    root.mainloop()
