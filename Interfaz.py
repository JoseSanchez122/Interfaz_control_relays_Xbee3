import customtkinter as ctk
import threading
from PIL import Image
import serial
import time
from tkinter import messagebox

RESIZE_SIZE = 1.0   #en caso que la interfaz se vea muy pequeña o grande con solo aumentar o disminuir
                    #este parametro (RESIZE_SIZE) se puede aumentar o disminuir el tamaño de toda la 
                    #interfaz. 
                    #Agrandar: RESIZE_SIZE = 1.1, RESIZE_SIZE = 1.2, RESIZE_SIZE = 1.3 ... RESIZE_SIZE = n
                    #hacer pequeño: RESIZE_SIZE = 0.9, RESIZE_SIZE = 0.8, RESIZE_SIZE = 0.7 ... RESIZE_SIZE = n

def Resize(size):
    global RESIZE_SIZE
    return int(size*RESIZE_SIZE)

app = ctk.CTk()
app.title("Banco de pruebas MAU")
app.title_color = "black"
app.geometry(str(Resize(865)) + "x" + str(Resize(520)))
app.configure(fg_color="white")

#--------------------------------------main frame-----------------------------------------#
main_frame = ctk.CTkFrame(app, fg_color="transparent", height=200,
                             border_width=2,
                            border_color="black")

main_frame.pack(fill="both", expand=True)

for i in range(4):
    main_frame.grid_columnconfigure(i, weight=1)

#--------------------------------------Buttons-----------------------------------------#
estilo_botones = {
    "font": ctk.CTkFont(size=16, weight="bold"),
    "fg_color": "#2C3E50",
    "hover_color": "#34495E",
    "text_color": "white",
    "corner_radius": Resize(10),
    "width": Resize(150),
    "height": Resize(200),
    "anchor": "center",
    "cursor": "hand2" 
}

def Enable_Relay(Relay):
    Write_message(f"+O{Relay}")

def Disable_Relay(Relay):
    Write_message(f"+o{Relay}")

def manejar_click(relay_id):
    if Relay_states["Relays NA"][f"Relay {relay_id}"]["State"] == True:
        Enable_Relay(relay_id)
    elif Relay_states["Relays NA"][f"Relay {relay_id}"]["State"] == False:
        Disable_Relay(relay_id)
    
for i in range(4):
    texto = f"Switch\nRelay {i+1}"
    boton = ctk.CTkButton(main_frame, 
                          text=texto, 
                          command=lambda i=i: manejar_click(i+1),
                          **estilo_botones)
    boton.grid(row=0, column=i, padx=Resize(30), pady=Resize(30))

#--------------------------------------Relay images-----------------------------------------#
Relay_Na = Image.open("NA.png")
Relay_Nc = Image.open("NC.png")

Relay_Na_image = ctk.CTkImage(light_image=Relay_Na.resize((Resize(170), Resize(170))), 
                              size=(Resize(170), Resize(170)))
Relay_Nc_image = ctk.CTkImage(light_image=Relay_Nc.resize((Resize(170), Resize(170))),
                              size=(Resize(170), Resize(170)))

Relay_states = {
    "Relays NA": {},
    "Relays NC": {}
}

for i in range(4):
    name = f"Relay {i+1}"

    label_na = ctk.CTkLabel(main_frame, image=Relay_Na_image, text="")
    label_na.grid(row=1, column=i, padx=Resize(10), pady=Resize(10))

    label_nc = ctk.CTkLabel(main_frame, image=Relay_Nc_image, text="")
    #label_nc.grid(row=1, column=i, padx=Resize(10), pady=Resize(10))

    # Agregar al subdiccionario existente
    Relay_states["Relays NA"][name] = {
        "Image": label_na,
        "State": True
    }

    Relay_states["Relays NC"][name] = {
        "Image": label_nc,
    }

#--------------------------------------Funciones para imagenes-----------------------------------------#
def Show_NA_Relay(relay_id):
    Relay_states["Relays NA"][f"Relay {relay_id}"]["State"] = True
    Relay_states["Relays NC"][f"Relay {relay_id}"]["Image"].grid_forget()
    Relay_states["Relays NA"][f"Relay {relay_id}"]["Image"].grid(row=1, column=relay_id-1, padx=Resize(10), pady=Resize(10))

def Show_NC_Relay(relay_id):
    Relay_states["Relays NA"][f"Relay {relay_id}"]["State"] = False
    Relay_states["Relays NA"][f"Relay {relay_id}"]["Image"].grid_forget()
    Relay_states["Relays NC"][f"Relay {relay_id}"]["Image"].grid(row=1, column=relay_id-1, padx=Resize(10), pady=Resize(10))

def Show_Relay_State(index, Comand):
    if Comand[index] == '0':
        Show_NA_Relay(index-1)
    elif Comand[index] == '1':
        print(Comand[index])
        Show_NC_Relay(index-1)

#--------------------------------------Funciones para mensajes por USB-----------------------------------------#
ser = None

def initialize_serial(port, baudrate=19200):
    global ser
    try:
        ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
    except serial.SerialException:
        ser = None
        return False

    return ser.is_open

def Write_message(message):
    if ser and ser.is_open:
        ser.write((message + "\r\n").encode('utf-8'))

def get_initial_states(relay_num):
    task_tries = 5
    state_found = False
    while(task_tries > 0):
        Enable_Relay(relay_num)
        Disable_Relay(relay_num)
        time.sleep(0.1)

        if ser.in_waiting > 0:
            state = ser.readline().decode('utf-8').strip()  # Lee una línea y la decodifica
            Show_Relay_State(index=relay_num+1, Comand=state)
            state_found = True
            break

        task_tries = task_tries-1

    if not state_found:
        messagebox.showwarning("Advertencia", f"No se pudo encontrar el estado inicial del relevador {relay_num}.")
    
def Relay_states_func():
    while(not initialize_serial("COM10")):
        messagebox.showwarning("Advertencia", "No se pudo abrir el puerto COM.")
    # for num in range(4):
    #     get_initial_states(num+1)

    state_valid_indexes = [2, 3, 4, 5]

    while(True):
        if ser.in_waiting > 0:
            state = ser.readline().decode('utf-8').strip() 
            for index in state_valid_indexes:
                Show_Relay_State(index= index, Comand=state)
                print(state[index])


    
hilo = threading.Thread(target=Relay_states_func, daemon=True)
hilo.start()

app.mainloop()