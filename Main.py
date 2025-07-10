from PIL import Image
from tkinter import messagebox
import Entry
import os
import sys
from editGame import *
from Purchase import *
from PurchaseList import *
import customtkinter

class GUI:
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path,relative_path)

    def showForm(self):
        self.root = customtkinter.CTk()
        self.root.title("Game Store Management System")
        self.root.geometry("850x450")
        self.root.resizable(0,0)
        self.root.quit()

        #self.root.state("zoomed")

        # Widgets
        self.create_label()
        self.create_menu()
        self.create_button()
        self.create_image()
        self.create_switch()
        self.root.mainloop()

    def btnClose(self):
        self.root.destroy()

    # Option Menu    
    def create_menu(self):
        # Entry Menu for "Stock Up Games"
        Entry_menu = customtkinter.CTkOptionMenu(self.root, values=["Stock Up Games"], width=200, command=self.GameEntry)
        Entry_menu.set("Stock")
        Entry_menu.grid(row=0, column=0, pady=10, padx=10)

        # Listing Menu
        List_menu = customtkinter.CTkOptionMenu(self.root, values=["Edit Game List", "Purchase List"], width=200, command=self.handle_list_menu)
        List_menu.set("List")
        List_menu.grid(row=0, column=1, pady=10, padx=10)

    # Buttons
    def create_button(self):
        self.buy_button = customtkinter.CTkButton(self.root, text="Games", font=("League Gothic", 20, "bold"), fg_color="transparent", border_color="green", corner_radius=9, hover_color="#1ccb1e", border_width=2, command=self.Buy)
        self.buy_button.place(x=40, y=300)

        self.close_button = customtkinter.CTkButton(self.root, text="Exit", font=("League Gothic", 20, "bold"), fg_color="transparent", border_color="red", corner_radius=9, hover_color="#dd2828", border_width=2, command=self.btnClose)
        self.close_button.place(x=200, y=300)

    # Labels
    def create_label(self):
        self.label = customtkinter.CTkLabel(self.root, text="EDGE", font=("League Spartan", 98, "bold"), text_color="#FFFFFF")
        self.label.place(x=40, y=175)

    # Images (Side, etc.)
    def create_image(self):
        imgpath = r"Image/wawa.png"
        self.myImage = customtkinter.CTkImage(Image.open(imgpath), size=(413, 604))
        imageLabel = customtkinter.CTkLabel(self.root, image=self.myImage, text="")
        imageLabel.place(x=513, y=0)

    # Switch
    def create_switch(self):
        self.switch_var = customtkinter.StringVar(value="off")
        switch = customtkinter.CTkSwitch(self.root, text="", width=80, command=self.switch_event, variable=self.switch_var, onvalue="on", offvalue="off")
        switch.place(x=40, y=400)

        # Changing Label
        self.label1 = customtkinter.CTkLabel(self.root, text="Light Mode", font=("Arial Bold", 14))
        self.label1.place(x=90, y=397)

    # Switch function
    def switch_event(self):
        if self.switch_var.get() == "on":
            self.label.configure(text_color="#000000")
            self.buy_button.configure(text_color="#000000")
            self.close_button.configure(text_color="#000000")
            customtkinter.set_appearance_mode("light")
        else:
            self.label1.configure(text="Light Mode")
            self.label.configure(text_color="#FFFFFF")
            self.buy_button.configure(text_color="#FFFFFF")
            self.close_button.configure(text_color="#FFFFFF")
            customtkinter.set_appearance_mode("dark")

    # Selecting Option
    def handle_list_menu(self, selected_option):
        if selected_option == "Edit Game List":
            editGame()
            eg = True
        elif selected_option == "Purchase List":
            PurchaseList()
    # Game Entry Form
    def GameEntry(self, value=None):
        ge = Entry.GameEntry()
        ge.ShowForm() 

    def Buy(self):
        Purchase()

    
def run_main_gui():
    gui = GUI()
    gui.showForm()

# Running the GUI
gui = GUI()
#gui.showForm()
