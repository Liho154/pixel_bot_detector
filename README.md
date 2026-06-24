##  ESPAÑOL
# Bot de Pesca Pro v1.0

¡Bienvenido al **Bot Pescador Pro**! La solución definitiva para cuando tienes mejores cosas que hacer que mirar fijamente una barrita de progreso en la pantalla. Este script utiliza visión por computadora (OpenCV) y captura de pantalla ultrarrápida para automatizar el minijuego de pesca en tus juegos favoritos.

Tú le das al _Play_, te vas a hacer tus cosas, y él se encarga de sacar el loot.

## 🚀 Características Principales

-   **Visión por Computadora en Tiempo Real:** Utiliza `OpenCV` y `mss` para analizar el monitor secundario a la velocidad del rayo, detectando los rangos de color HSV del objetivo.
    
-   **Interfaz Gráfica (GUI) Elegante:** Nada de usar solo la consola oscura. Incluye una ventana siempre visible para controlar el estado del bot.
    
-   **Control Predictivo Inteligente:** Calcula el margen de error entre la zona segura (verde) y el marcador (amarillo) y simula pulsaciones de las teclas **A** y **D** para mantener la barra centrada.
    
-   **Sistema Anti-Temblores (Zona Muerta):** Implementa un margen de tolerancia (15% del ancho de la barra) para evitar que el bot espamee teclas como un desquiciado.
    
-   **Automatización de Acciones (Macros):** Pulsa la tecla **F** cada 3 segundos y ejecuta un clic izquierdo en zonas estratégicas cada 5 segundos de forma autónoma.
    
-   **Botón del Pánico (Hotkey):** Toca la tecla **Q** en cualquier momento para iniciar o detener la carnicería pesquera sin tener que hacer Alt-Tab.
    

## 🎮 Cómo se usa

Tienes dos formas de hacer funcionar esta bestia, dependiendo de si quieres ir a lo rápido o si te gusta trastear con el código.

### Opción A: Modo Fácil (Usando el `.exe`)

Para los que quieren farmear ya y dejarse de líos:

1.  Asegúrate de que el juego se está ejecutando (por defecto, el bot mira tu pantalla principal/secundaria según la configuración).
    
2.  Entra en la carpeta `dist`.
    
3.  Haz doble clic en el archivo **`bot_pesca.exe`**. _(Nota: Ejecútalo como Administrador si el juego no detecta los clics)._
    
4.  Se abrirá la ventana de control. Pulsa **▶ INICIAR** o toca la tecla **Q**.
    
5.  ¡A recolectar!
    

### Opción B: Modo Desarrollador (Desde el código fuente)

Si quieres modificar las variables, los tiempos o compilarlo tú mismo, necesitas tener instalado **Python 3.x**.

1.  Instala las dependencias necesarias. Abre tu terminal y lanza:
    
    Bash
    
    ```
    pip install opencv-python numpy mss pydirectinput keyboard
    ```
    
2.  Ejecuta el script desde la consola (preferiblemente como Administrador):
    
    Bash
    
    ```
    python bot_pesca.py
    ```
    
3.  Controla el bot desde su interfaz o usando la tecla **Q**.
    

## 🧠 ¿Cómo funciona por debajo?

El núcleo del bot crea un área de recorte (ROI - _Region of Interest_) en la zona superior central de la pantalla para ahorrar recursos y ganar FPS de procesado.

Convierte la imagen capturada a espacio de color HSV y aplica dos máscaras:

1.  **Máscara Verde:** Busca la barra de pesca (la zona segura).
    
2.  **Máscara Amarilla:** Busca el indicador de tensión/posición.
    

Calcula los centros geométricos de ambas máscaras. Si el centro amarillo se desvía más allá de la "zona muerta" permitida, el bot envía comandos por hardware (`pydirectinput.keyDown`) para corregir la trayectoria instantáneamente. Todo esto corre en un hilo paralelo (`threading`) para que la interfaz gráfica no se quede congelada.

---
---

## ENGLISH
# Pro Fishing Bot v1.0

Welcome to the **Pro Fishing Bot**! The ultimate solution for when you have better things to do than stare at a progress bar on your screen. This script uses computer vision (OpenCV) and lightning-fast screen capture to automate the fishing minigame in your favorite games.

You hit _Play_, go do your thing, and it takes care of farming the loot.

## 🚀 Main Features

-   **Real-Time Computer Vision:** Uses `OpenCV` and `mss` to analyze your secondary monitor at lightning speed, detecting the target's HSV color ranges.
    
-   **Elegant Graphical Interface (GUI):** No more staring at a dark console. Includes an always-on-top window to easily control the bot's status.
    
-   **Smart Predictive Control:** Calculates the margin of error between the safe zone (green) and the marker (yellow), simulating **A** and **D** keystrokes to keep the bar perfectly centered.
    
-   **Anti-Jitter System (Deadzone):** Implements a tolerance margin (15% of the bar's width) to prevent the bot from spamming keys like a maniac.
    
-   **Action Automation (Macros):** Presses the **F** key every 3 seconds and autonomously performs a left-click in strategic areas every 5 seconds.
    
-   **Panic Button (Hotkey):** Tap the **Q** key at any time to start or stop the fishing carnage without having to Alt-Tab.
    

## 🎮 How to Use It

You have two ways to get this beast running, depending on whether you want the fast track or if you like messing around with code.

### Option A: Easy Mode (Using the `.exe`)

For those who want to start farming right away and skip the hassle:

1.  Make sure the game is running (by default, the bot looks at your primary/secondary screen depending on the setup).
    
2.  Go into the `dist` folder.
    
3.  Double-click the **`bot_pesca.exe`** file. _(Note: Run it as Administrator if the game doesn't detect the clicks)._
    
4.  The control window will pop up. Click **▶ START** or tap the **Q** key.
    
5.  Let the farming begin!
    

### Option B: Developer Mode (From source code)

If you want to tweak variables, adjust timings, or compile it yourself, you'll need **Python 3.x** installed.

1.  Install the necessary dependencies. Open your terminal and run:
    
    Bash
    
    Bash
    
    ```
    pip install opencv-python numpy mss pydirectinput keyboard
    ```
    
2.  Run the script from the console (preferably as Administrator):
    
    Bash
    
    Bash
    
    ```
    python bot_pesca.py
    ```
    
3.  Control the bot from its interface or by using the **Q** key.
    

## 🧠 Under the Hood

The bot's core creates a cropping area (ROI - _Region of Interest_) in the top-center part of the screen to save resources and boost processing FPS.

It converts the captured image to the HSV color space and applies two masks:

1.  **Green Mask:** Looks for the fishing bar (the safe zone).
    
2.  **Yellow Mask:** Looks for the tension/position indicator.
    

It calculates the geometric centers of both masks. If the yellow center drifts beyond the allowed "deadzone", the bot sends hardware-level commands (`pydirectinput.keyDown`) to correct the trajectory instantly. All of this runs on a parallel thread (`threading`) so the graphical interface doesn't freeze up.