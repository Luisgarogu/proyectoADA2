==============================
Proyecto ADAII: Moderando el conflicto interno de opiniones en una red social.
==============================

Autores: 
Luis Gabriel Rodriguez - 1943075-3743
Yilver Julian Tello Larrahondo - 2110019-3743
Gilberth Adrian Banguero Serna - 2110010-3743

Fecha de entrega: [25/04/2025]

Descripción:
-------------
Este proyecto implementa tres estrategias para resolver el problema de moderación del conflicto 
interno (ModCI) en una red social, usando tres enfoques de diseño de algoritmos:
- Fuerza bruta
- Algoritmo voraz
- Programación dinámica

Se incluye una interfaz gráfica que permite:
- Cargar archivos de entrada desde el computador
- Seleccionar el algoritmo deseado
- Ejecutar el proceso de moderación
- Guardar los resultados en un archivo de salida

Estructura de carpetas y archivos:
-----------------------------------

/modci_app/
├── main.py                 # Archivo principal que contiene la interfaz gráfica
├── fuerzabruta.py          # Implementación del algoritmo de fuerza bruta
├── voraz.py                # Implementación del algoritmo voraz 
├── dinamica.py             # Implementación del algoritmo usando programación dinámica
└── Readme.txt              # Este archivo con instrucciones de uso


Requisitos:
-------------
- Python 3.8 o superior
- Sistema operativo: Windows, Linux o macOS
- No requiere instalar librerías externas, usa solo módulos estándar como `tkinter`, `math` y `os`.

Instrucciones para ejecutar la aplicación:
-------------------------------------------
1. Asegúrate de tener Python instalado.
2. Abre una terminal o consola de comandos.
3. Navega a la carpeta donde está el archivo `main.py`.
4. Ejecuta el siguiente comando:

   python main.py

5. Se abrirá una ventana con la interfaz gráfica.
6. Selecciona el archivo de entrada (`*.txt`) con el botón de explorador.
7. Selecciona el lugar y nombre del archivo de salida.
8. Elige el algoritmo que deseas aplicar.
9. Haz clic en **Ejecutar**.
10. Al finalizar, el resultado será mostrado en pantalla y guardado en el archivo de salida.

