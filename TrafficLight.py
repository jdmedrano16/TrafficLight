import RPi.GPIO as GPIO
import time

#Nombre: José Daniel Medrano Guadamuz
#Curso: Arquitectura II
#Profesor: José Luis Medrano Cerdas

#Link Video: https://youtu.be/rFMeGrQfliQ

#GPIO ---------------------------------------------
allGPIO = {
    #Pedestrian lights - Semáforo para peatones
    "redLedP": 8,
    "greenLedP": 7,
    #North - South
    "redLedNS": 13,
    "yellowLedNS": 19,
    "greenLedNS": 26,
    #West - East
    "redLedWE": 16,
    "yellowLedWE": 20,
    "greenLedWE": 21,
    #Buzzer - Button
    "button": 22,
    "buzzer": 12
}
#OTHER VARIABLES ----------------------------------
#Tiempo que dura el semáforo en cambiar de luz.
timeLight = 6
#Variable global que cambia a True cuando el botón es presionado.
global pressed 
pressed = False
#Diccionario para guardar el último estado de los LEDs del semáforo.
global state
state = {
    "redLedNS": False,
    "yellowLedNS": False,
    "greenLedNS": False,

    "redLedWE": False,
    "yellowLedWE": False,
    "greenLedWE": False,

    "redLedP": False,
    "greenLedP": False
}
#SETMODE ------------------------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#SETUP --------------------------------------------
#LEDs - Paso Peatonal - redLedP con P de Pedestrians o peatones en español
GPIO.setup(allGPIO["redLedP"], GPIO.OUT)
GPIO.setup(allGPIO["greenLedP"], GPIO.OUT)
GPIO.output(allGPIO["greenLedP"], False)
#LEDS - Cara del semáforo Norte y Sur - North South
GPIO.setup(allGPIO["redLedNS"], GPIO.OUT)
GPIO.setup(allGPIO["yellowLedNS"], GPIO.OUT)
GPIO.setup(allGPIO["greenLedNS"], GPIO.OUT)
#LEDS - Cara del semáforo Oeste y Este - West East
GPIO.setup(allGPIO["redLedWE"], GPIO.OUT)
GPIO.setup(allGPIO["yellowLedWE"], GPIO.OUT)
GPIO.setup(allGPIO["greenLedWE"], GPIO.OUT)
#Buzzer - Button
GPIO.setup(allGPIO["button"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(allGPIO["buzzer"], GPIO.OUT)
GPIO.output(allGPIO["buzzer"], False)

#FUNCIONES DE UTILIDAD ----------------------------
def printTrafficLight():
    print("NS => ROJO: " + str(state["redLedNS"]) + ", AMARILLO: " + str(state["yellowLedNS"]) + ", VERDE: " + str(state["greenLedNS"]) + ".")
    print("NS => ROJO: " + str(state["redLedWE"]) + ", AMARILLO: " + str(state["yellowLedWE"]) + ", VERDE: " + str(state["greenLedWE"]) + ".")
    print("NS => ROJO: " + str(state["redLedP"]) + ", VERDE: " + str(state["greenLedP"]) + ".\n")

#FUNCIONES PRINCIPALES ----------------------------
#Función para reproducir el sonido cuando el paso peatonal está en verde. 
def playSound():
    printTrafficLight()
    #Debido a que cada iteración del "for" toma 2 segundos en completarse, solo se necesita la mitad de segundos de timeLight.
    timeSound = int(timeLight / 2)
    for _ in range(timeSound):
        GPIO.output(allGPIO["buzzer"], True)
        time.sleep(1)
        GPIO.output(allGPIO["buzzer"], False)
        time.sleep(1)

#Función que se utliza como el callback de GPIO.add_event_detect().
def buttonPressed(pin):
    global pressed
    pressed = True
    print("\nButton Pressed\n")

#Función para cambiar las luces de las caras norte y sur del semáforo.
def changeLightNS(redLed, yellowLed, greenLed):
    global state
    state["redLedNS"] = redLed
    state["yellowLedNS"] = yellowLed
    state["greenLedNS"] = greenLed

    GPIO.output(allGPIO["redLedNS"], redLed)
    GPIO.output(allGPIO["yellowLedNS"], yellowLed)
    GPIO.output(allGPIO["greenLedNS"], greenLed)

#Función para cambiar las luces de las caras oeste y este del semáforo.
def changeLightWE(redLed, yellowLed, greenLed):
    global state
    state["redLedWE"] = redLed
    state["yellowLedWE"] = yellowLed
    state["greenLedWE"] = greenLed

    GPIO.output(allGPIO["redLedWE"], redLed)
    GPIO.output(allGPIO["yellowLedWE"], yellowLed)
    GPIO.output(allGPIO["greenLedWE"], greenLed)

#Función para cambiar las luces del semáforo peatonal.
def changeLightP(redLed, greenLed):
    global state
    state["redLedP"] = redLed
    state["greenLedP"] = greenLed

    GPIO.output(allGPIO["redLedP"], redLed)
    GPIO.output(allGPIO["greenLedP"], greenLed)
    #Si la luz es verde, se empieza a reproducir el sonido.
    if greenLed:
        playSound()

#Función con la lógica principal del cambio de luces del semáforo.
def changeColors():
    while True:
        global pressed
        changeLightNS(redLed=False, yellowLed=False, greenLed=True)
        changeLightWE(redLed=True, yellowLed=False, greenLed=False)
        changeLightP(redLed=True, greenLed=False)
        printTrafficLight()
        time.sleep(timeLight)
        
        changeLightNS(redLed=False, yellowLed=True, greenLed=False)
        printTrafficLight()
        time.sleep(timeLight)
        
        changeLightNS(redLed=True, yellowLed=False, greenLed=False)
        changeLightWE(redLed=False, yellowLed=False, greenLed=True)
        #isButtonPressed se crea para que el valor de pressed sea definitivo.
        isButtonPressed = pressed
        #isLightPActive se usa para comprobar de que el paso peatonal se haya puesto en verde.
        isLightPChanged = False
        #Si el botón no ha sido presionado, entonces mantenga el peatonal en rojo por X cantidad de tiempo, siendo X = timeLight. 
        #De lo contrario, cambiar la luz a verde y empezar a repoducir el sonido.
        if not isButtonPressed:
            printTrafficLight()
            time.sleep(timeLight)
        else:
            changeLightP(redLed=False, greenLed=True)
            isLightPChanged = True

        changeLightWE(redLed=False, yellowLed=True, greenLed=False)
        #Si el botón no ha sido presionado, entonces mantenga el peatonal en rojo por X cantidad de tiempo, siendo X = timeLight. 
        #De lo contrario, prolongar el sonido del buzzer.
        if not isButtonPressed:
            printTrafficLight()
            time.sleep(timeLight)
        else:
            playSound()
        isButtonPressed = False
        #Si el botón fue presionado y la luz del semáforo fue cambiada a verde de manera exitosa,
        #entonces se desactiva la variable pressed, para que así, este lista en caso de que se
        #presione el botón otra vez.
        if pressed and isLightPChanged:
            pressed = False

#Función principal.
def main():
    try:
        GPIO.add_event_detect(allGPIO["button"], GPIO.FALLING, callback=buttonPressed)
        changeColors()
    except KeyboardInterrupt:
        print("\nFinished!\n")
    finally:
        GPIO.cleanup()


#Llamado del main.
main()