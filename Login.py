from customtkinter import *
from Main import GUI
from PIL import Image
from tkinter import messagebox

app = CTk()
app.geometry("600x480")
app.resizable(0,0)
app.title("Login")

def Login():

    username = "user123"
    password = "pw123"

    u_input = UEntry.get()
    p_input = PEntry.get()

    gui = GUI()
   
    if(username==u_input and password==p_input):
        UEntry.delete(0, END)
        PEntry.delete(0, END)
        app.destroy()
        gui.showForm()
        
    else:
        messagebox.showinfo("Error","Your username or password is not correct\nTry Again!!")


side_img_data = Image.open("Image/side-img.png")
email_icon_data = Image.open("Image/email-icon.png")
password_icon_data = Image.open("Image/password-icon.png")

side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20,20))
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17,17))

CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = CTkFrame(master=app, width=300, height=480, fg_color="#FFFFFF")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

CTkLabel(master=frame, text="EDGE", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 30)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
CTkLabel(master=frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Username:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
UEntry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
UEntry.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
PEntry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
PEntry.pack(anchor="w", padx=(25, 0))

CTkButton(master=frame, text="Login",text_color="#601E88",fg_color="transparent", hover_color="#8544ad",font=("Arial Bold", 12),border_width=3,border_color="#601E88",corner_radius=8.4,width=225,command=Login).pack(anchor="w", pady=(38, 0), padx=(25, 0))

app.mainloop()