import cv2
import numpy as np
import mss
import pydirectinput
import keyboard
import time
import threading
import tkinter as tk
from tkinter import font

bot_corriendo = False # Variable global para encender/apagar

# Rangos HSV (Ajustados según tu código)
LOWER_GREEN  = np.array([75, 180, 180]) 
UPPER_GREEN  = np.array([95, 255, 255])
LOWER_YELLOW = np.array([20, 100, 100])
UPPER_YELLOW = np.array([35, 255, 255])

def obtener_datos_contorno(mask):
    """
    Devuelve el centro X y el ancho del contorno más grande encontrado.
    """
    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contornos:
        mayor = max(contornos, key=cv2.contourArea)
        if cv2.contourArea(mayor) > 30: # Reducido ligeramente para detectar el amarillo más rápido
            x, y, w, h = cv2.boundingRect(mayor)
            centro_x = x + (w // 2)
            return centro_x, w
    return None, None

def liberar_tecla(tecla):
    """Función auxiliar para limpiar el estado de las teclas de forma segura"""
    if tecla:
        pydirectinput.keyUp(tecla)
    return None

# =====================================
# EL VIGÍA DEL TECLADO (HILO TERCERO)
# =====================================
def vigia_teclas():
    while True:
        if keyboard.is_pressed('q'):
            # Esperamos pacientemente a que vuesa merced levante el dedo de la tecla
            while keyboard.is_pressed('q'):
                time.sleep(0.01)
                
            # Una vez suelta, miramos cómo está el chiringuito y lo cambiamos
            if bot_corriendo:
                ventana.after(0, detener_bot) 
            else:
                ventana.after(0, iniciar_bot)
                
        time.sleep(0.05) # El descanso del guerrero

def bucle_bot():
    global bot_corriendo
    print("Iniciando bot en 3 segundos... Mantén presionada la tecla 'Q' para detener.")
    time.sleep(3)

    ahora = time.time()
    tiempo_ultima_f    = ahora
    tiempo_ultimo_clic = ahora
    tecla_actual       = None

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        ancho   = monitor["width"]
        alto    = monitor["height"]

        roi_width  = int(ancho * 0.40)
        roi_height = int(alto  * 0.18)
        roi_left   = int((ancho - roi_width) / 2)
        roi_top    = int(alto  * 0.07)

        monitor_roi = {
            "top": roi_top, "left": roi_left,
            "width": roi_width, "height": roi_height
        }

        # Coordenadas estáticas precalculadas fuera del bucle para mayor rendimiento
        x_texto = ancho // 2
        y_texto = int(alto * 0.88)
        x_centro_pantalla = ancho // 2
        y_centro_pantalla = alto // 2

        sct_grab = sct.grab

        while bot_corriendo:
            ahora = time.time()
            print(f"Cronómetro para la F: {ahora - tiempo_ultima_f:.2f} segundos")
            # Lógica de acciones periódicas del juego (F y Clics)
            if ahora - tiempo_ultima_f >= 3.0:
                print("Pulsando F...")
                pydirectinput.press('f')
                tiempo_ultima_f = ahora

            if ahora - tiempo_ultimo_clic >= 5.0:
                print("Usando el click...")
                pydirectinput.moveTo(x_texto, y_texto)
                pydirectinput.mouseDown()
                time.sleep(0.05)
                pydirectinput.mouseUp()
                pydirectinput.moveTo(x_centro_pantalla, y_centro_pantalla)
                tiempo_ultimo_clic = ahora

            # ------------------------------------
            # NÚCLEO DE VISIÓN POR COMPUTADORA
            # ------------------------------------
            img = np.array(sct_grab(monitor_roi))
            hsv = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2HSV)

            mask_green  = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
            mask_yellow = cv2.inRange(hsv, LOWER_YELLOW, UPPER_YELLOW)

            centro_verde, ancho_verde     = obtener_datos_contorno(mask_green)
            centro_amarillo, _            = obtener_datos_contorno(mask_yellow)

            # SISTEMA DE SEGURIDAD: Si no hay barras en pantalla
            if centro_verde is None or centro_amarillo is None:
                tecla_actual = liberar_tecla(tecla_actual)
                continue

            # ---------------------------------------------------------
            # NÚCLEO DE CONTROL PREDICTIVO (Seguimiento de Centro)
            # ---------------------------------------------------------
            # Calculamos la distancia entre nuestro marcador y el centro ideal
            error = centro_verde - centro_amarillo 

            zona_muerta = ancho_verde * 0.15 

            if error > zona_muerta:
                # El centro verde está a la derecha del amarillo. Hay que moverse a la DERECHA.
                if tecla_actual != 'd':
                    tecla_actual = liberar_tecla(tecla_actual)
                    pydirectinput.keyDown('d')
                    tecla_actual = 'd'

            elif error < -zona_muerta:
                # El centro verde está a la izquierda del amarillo. Hay que moverse a la IZQUIERDA.
                if tecla_actual != 'a':
                    tecla_actual = liberar_tecla(tecla_actual)
                    pydirectinput.keyDown('a')
                    tecla_actual = 'a'

            else:
                # Estamos dentro de la zona central segura de la barra verde.
                if tecla_actual is not None:
                    tecla_actual = liberar_tecla(tecla_actual)

# ======================================
# CONTROLES DE LA INTERFAZ Y VENTANA
# ======================================
def iniciar_bot():
    global bot_corriendo
    if not bot_corriendo:
        bot_corriendo = True
        estado_label.config(text="ESTADO: PESCANDO...", fg="#00b894")
        btn_iniciar.config(state=tk.DISABLED)
        btn_detener.config(state=tk.NORMAL)
        
        hilo = threading.Thread(target=bucle_bot)
        hilo.daemon = True 
        hilo.start()

def detener_bot():
    global bot_corriendo
    bot_corriendo = False
    estado_label.config(text="ESTADO: DETENIDO", fg="#d63031")
    btn_iniciar.config(state=tk.NORMAL)
    btn_detener.config(state=tk.DISABLED)

# Asegura que pydirectinput no tenga pausas
pydirectinput.PAUSE = 0.0 

# Forjamos la ventana
ventana = tk.Tk()
ventana.title("Bot Pescador Pro")
ventana.geometry("300x200")
ventana.configure(bg="#2d3436")
ventana.resizable(False, False)

fuente_titulo = font.Font(family="Helvetica", size=14, weight="bold")
fuente_botones = font.Font(family="Helvetica", size=10, weight="bold")

titulo = tk.Label(ventana, text="Auto-Pesca v1.0", bg="#2d3436", fg="#dfe6e9", font=fuente_titulo)
titulo.pack(pady=15)

estado_label = tk.Label(ventana, text="ESTADO: DETENIDO", bg="#2d3436", fg="#d63031", font=fuente_botones)
estado_label.pack(pady=5)

frame_botones = tk.Frame(ventana, bg="#2d3436")
frame_botones.pack(pady=15)

btn_iniciar = tk.Button(frame_botones, text="▶ INICIAR", font=fuente_botones, bg="#00b894", fg="white", 
                        activebackground="#55efc4", width=10, command=iniciar_bot)
btn_iniciar.grid(row=0, column=0, padx=10)

btn_detener = tk.Button(frame_botones, text="■ DETENER", font=fuente_botones, bg="#d63031", fg="white", 
                        activebackground="#ff7675", width=10, state=tk.DISABLED, command=detener_bot)
btn_detener.grid(row=0, column=1, padx=10)

consejo = tk.Label(ventana, text="Toque 'Q' para Iniciar | Toque 'Q' para Detener", 
                   bg="#2d3436", fg="#b2bec3", font=("Helvetica", 8))
consejo.pack(side=tk.BOTTOM, pady=10)

ventana.attributes("-topmost", True)

hilo_vigia = threading.Thread(target=vigia_teclas)
hilo_vigia.daemon = True
hilo_vigia.start()

# Arrancamos la ventana
ventana.mainloop()