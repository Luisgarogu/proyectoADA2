import math
import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ─────────────── Algoritmos ─────────────────
import fuerzabruta
import voraz

# ────────────────────────────────────────────


# =============================================================================
# Clases de Datos y Lógica del Problema
# =============================================================================
class GrupoAgente:
    def __init__(self, n, op1, op2, rig):
        self.n   = n
        self.op1 = op1
        self.op2 = op2
        self.rig = rig

    def __str__(self):
        return (f"Agentes: {self.n}, Op1: {self.op1}, "
                f"Op2: {self.op2}, Rigidez: {self.rig}")


class RedSocial:
    def __init__(self, grupos, R_max):
        self.grupos = grupos
        self.R_max  = R_max

    # ---------- métricas del problema ----------
    def calcular_conflicto_interno(self):
        if not self.grupos:
            return 0
        num = sum(g.n * (g.op1 - g.op2) ** 2 for g in self.grupos)
        return num / len(self.grupos)

    def calcular_esfuerzo(self, estrategia):
        esfuerzo = 0
        for i, e in enumerate(estrategia):
            if e:
                g = self.grupos[i]
                esfuerzo += math.ceil(abs(g.op1 - g.op2) * g.rig * e)
        return esfuerzo

    def aplicar_estrategia(self, estrategia):
        nuevos = []
        for i, g in enumerate(self.grupos):
            e = estrategia[i]
            nuevo_n = max(g.n - e, 0)
            nuevos.append(GrupoAgente(nuevo_n, g.op1, g.op2, g.rig))
        return RedSocial(nuevos, self.R_max)


# =============================================================================
# Funciones de archivo
# =============================================================================
def cargar_datos(ruta):
    if not os.path.exists(ruta):
        raise FileNotFoundError(ruta)
    with open(ruta, encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    n = int(lines[0])
    grupos = []
    for i in range(1, n + 1):
        n_ag, op1, op2, rig = lines[i].split(",")
        grupos.append(GrupoAgente(int(n_ag), int(op1), int(op2), float(rig)))
    R_max = int(lines[n + 1])
    return RedSocial(grupos, R_max)


def guardar_resultados(ruta, estrategia, esfuerzo, conflicto):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"{conflicto}\n{esfuerzo}\n")
        f.writelines(f"{e}\n" for e in estrategia)


# =============================================================================
# Interfaz
# =============================================================================
class ModeracionApp:
    def __init__(self, master):
        self.master = master
        master.title("Moderación de Conflicto Interno")
        master.geometry("1100x700")

        ttk.Style().theme_use("clam")

        # variables UI
        self.entrada_var   = tk.StringVar()
        self.salida_var    = tk.StringVar()
        self.algoritmo_var = tk.StringVar(value="Fuerza Bruta")
        self.resultado_var = tk.StringVar()

        self.crear_widgets()

    # ---------- widgets ----------
    def crear_widgets(self):
        main = ttk.Frame(self.master); main.pack(fill="both", expand=True)

        # Algoritmos
        lf_alg = ttk.LabelFrame(main, text="Algoritmo")
        lf_alg.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        for alg in ("Fuerza Bruta", "Voraz", "Programación Dinámica"):
            ttk.Radiobutton(lf_alg, text=alg,
                            variable=self.algoritmo_var,
                            value=alg).pack(anchor="w", padx=20, pady=2)

        # Archivos
        lf_arc = ttk.LabelFrame(main, text="Archivos")
        lf_arc.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ttk.Label(lf_arc, text="Entrada (Archivo de Entrada):").grid(row=0, column=0, sticky="w")
        ttk.Entry(lf_arc, textvariable=self.entrada_var, width=50)\
            .grid(row=0, column=1, padx=5)
        ttk.Button(lf_arc, text="…", command=self.sel_entrada)\
            .grid(row=0, column=2)

        ttk.Label(lf_arc, text="Salida (Escriba y seleccione el lugar donde desea guardar el archivo de salida):").grid(row=1, column=0, sticky="w")
        ttk.Entry(lf_arc, textvariable=self.salida_var, width=50)\
            .grid(row=1, column=1, padx=5)
        ttk.Button(lf_arc, text="…", command=self.sel_salida)\
            .grid(row=1, column=2)

        # Ejecutar
        ttk.Button(main, text="Ejecutar", command=self.ejecutar)\
            .grid(row=1, column=0, columnspan=2, pady=10)

        # Resultados
        lf_res = ttk.LabelFrame(main, text="Resultados")
        lf_res.grid(row=2, column=0, columnspan=2, sticky="nsew",
                    padx=10, pady=10)
        self.txt = tk.Text(lf_res, wrap="word"); self.txt.pack(fill="both", expand=True)
        self.resultado_var.trace_add("write", self.mostrar_resultado)

        # expansión
        main.grid_columnconfigure((0, 1), weight=1)
        main.grid_rowconfigure(2, weight=1)

    # ---------- file‑dialogs ----------
    def sel_entrada(self):
        ruta = filedialog.askopenfilename(title="Entrada",
                filetypes=[("txt", "*.txt"), ("todos", "*.*")])
        if ruta: self.entrada_var.set(ruta)

    def sel_salida(self):
        ruta = filedialog.asksaveasfilename(title="Salida", defaultextension=".txt",
                filetypes=[("txt", "*.txt"), ("todos", "*.*")])
        if ruta: self.salida_var.set(ruta)

    # ---------- lógica principal ----------
    def ejecutar(self):
        if not self.entrada_var.get() or not self.salida_var.get():
            messagebox.showerror("Faltan datos", "Seleccione archivos de entrada y salida")
            return
        try:
            rs  = cargar_datos(self.entrada_var.get())
            alg = self.algoritmo_var.get()

            t0 = time.time()
            if alg == "Fuerza Bruta":
                estrategia, esfuerzo, CI, stats = fuerzabruta.modciFuerzaBruta(rs)

            elif alg == "Voraz":
                estrategia, esfuerzo, CI, stats = voraz.modciV(rs)

            elif alg == "Programación Dinámica":
                if dinamica is None:
                    raise RuntimeError("Módulo dinamica no disponible.")
            else:
                raise ValueError("Algoritmo no reconocido")

            dt = time.time() - t0
            guardar_resultados(self.salida_var.get(), estrategia, esfuerzo, CI)

            # construir texto
            msg = (f"Algoritmo : {alg}\n"
                   f"Tiempo    : {dt*1000:.6f} ms\n"
                   f"CI final  : {CI}\n"
                   f"Esfuerzo  : {esfuerzo}\n\n"
                   "Estrategia:\n")
            for i, e in enumerate(estrategia):
                msg += f"  Grupo {i+1}: {e} moderados\n"

            if stats:
                msg += "\n─ Estadísticas ─\n"
                msg += "\n".join(f"{k}: {v}" for k, v in stats.items())

            self.resultado_var.set(msg)
            messagebox.showinfo("OK", "Proceso finalizado; resultados guardados.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- actualización del Text ----------
    def mostrar_resultado(self, *_):
        self.txt.delete("1.0", "end")
        self.txt.insert("end", self.resultado_var.get())


# =============================================================================
# Ejecutar
# =============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    ModeracionApp(root)
    root.mainloop()
