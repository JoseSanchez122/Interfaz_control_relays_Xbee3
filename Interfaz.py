import customtkinter as ctk
import threading
from PIL import Image

RESIZE_SIZE = 1.0   #en caso que la interfaz se vea muy pequeña o grande con solo aumentar o disminuir
                    #este parametro (RESIZE_SIZE) se puede aumentar o disminuir el tamaño de toda la 
                    #interfaz. 
                    #Agrandar: RESIZE_SIZE = 1.1, RESIZE_SIZE = 1.2, RESIZE_SIZE = 1.3 ... RESIZE_SIZE = n
                    #hacer pequeño: RESIZE_SIZE = 0.9, RESIZE_SIZE = 0.8, RESIZE_SIZE = 0.7 ... RESIZE_SIZE = n

def resize(size):
    global RESIZE_SIZE
    return int(size*RESIZE_SIZE)

app = ctk.CTk()
app.title("Banco de pruebas MAU")
app.title_color = "black"
app.geometry(str(resize(865)) + "x" + str(resize(520)))
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
    "corner_radius": 10,
    "width": 150,
    "height": 200,
    "anchor": "center",
    "cursor": "hand2" 
}

def manejar_click(relay_id):
    if relay_id == 1:
        Relay_NC_Array[1].grid(row=1, column=0, padx=10, pady=10)
    

for i in range(4):
    texto = f"Switch\nRelay {i+1}"
    boton = ctk.CTkButton(main_frame, 
                          text=texto, 
                          command=lambda i=i: manejar_click(i+1),
                          **estilo_botones)
    boton.grid(row=0, column=i, padx=30, pady=30)

#--------------------------------------Relay images-----------------------------------------#

Relay_Na = Image.open("NA.png")
Relay_Nc = Image.open("NC.png")

Relay_Na_image = ctk.CTkImage(light_image=Relay_Na.resize((170, 170)), size=(170, 170))
Relay_Nc_image = ctk.CTkImage(light_image=Relay_Nc.resize((170, 170)), size=(170, 170))

Relay_NA_Array = {}
Relay_NC_Array = {}

for i in range(4):
    label = ctk.CTkLabel(main_frame, image=Relay_Na_image, text="")
    label.grid(row=1, column=i, padx=10, pady=10)
    Relay_NA_Array.append(label)
    label2 = ctk.CTkLabel(main_frame, image=Relay_Nc_image, text="")
    Relay_NC_Array.append(label2)


app.mainloop()