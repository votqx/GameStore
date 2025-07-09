from SQL_Functions import *
from customtkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import csv

class editGame:
    def selection(self,event):
        selected = self.table.selection()
        data = self.table.item(selected[0])['values']
        name = str(self.game_name.get())
        if not selected:
            messagebox.showinfo("Error","You can't select a blank place!!")

        if name == "-----Select-----" :
            self.game_name.set(data[0])
            self.GName.insert(0,data[0])
            self.platform.set(data[1])
            self.GPrice.insert(0,data[2])
            self.GQty.insert(0,data[3])
            self.select_data()
        else:
            self.clear_fun()
            self.game_name.set(data[0])
            self.GName.insert(0,data[0])
            self.platform.set(data[1])
            self.GPrice.insert(0,data[2])
            self.GQty.insert(0,data[3])
            self.select_data()

    def print_file(self):
        desktop = os.path.join(os.path.expanduser("~"),"Desktop")
        folder_name = "Records"
        folder_path = os.path.join(desktop,folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            messagebox.showinfo("Reminder",f"Record folder created at : {folder_path}")
        else:
            messagebox.showinfo("Reminder",f"Record already exists at : {folder_path}")

        file_path = os.path.join(folder_path,"Game Records.csv")

        Data = Select("SELECT Name, gType, Price, Quantity from game")
        #Header
        with open(file_path,"w") as file:
            file.write("Game Name, Platform Type, Price, Quantity\n")
        #Append data
        with open(file_path,"a") as file:
            for records in Data:
                file.write(f"{records[0]}, {records[1]}, {records[2]}, {records[3]}\n")

    def btnCloseClick(self):
        self.Window.destroy()
    
    def update(s):
        if(s.GName.get()=="-----Select-----"):
            messagebox.showwarning("Message","Enter Game Name and try agian!!")
        elif(s.platform.get()==""):
            messagebox.showwarning("Message","Change platform type and try again!!")
        elif((s.GPrice.get().isdigit()==False)or(s.GPrice.get()=="")):
            messagebox.showwarning("Message","Price must be a digit!!\nEntery Price and try again")
        elif((s.GQty.get().isdigit()==False)or(s.GQty.get()=="")):
            messagebox.showwarning("Message","Quantity must be a digit!!\nEnter Quantity and try again")
        else:
            Execute("Update game set Name='"+str(s.GName.get()).strip()+"', gType='"+str(s.platform.get()).strip()+"', Price='"+str(s.GPrice.get()).strip()+"',Quantity='"+str(s.GQty.get()).strip()+"' Where GameID='"+str(s.Gid)+"'")
            s.clear_fun()
            s.refresh_table()
            messagebox.showinfo("Game Store","Game Data Updated Successfully")

    def delete_Fun(s):
        if s.game_name.get()=="":
            messagebox.showinfo("Worn","Please Choose Your Game Name and Try again!!")
        else:
            r = Select("Select Quantity from game where GameID='"+s.Gid+"';")
            if(r[0][0]>0):
                messagebox.showinfo("Worn","Quantity isn't Zero!!\nCan't be Delete!!")
            else:
                Execute("Delete From game where GameID='"+s.Gid+"'")
                messagebox.showinfo("Worn","Delete Process Complete.")
                s.clear_fun()
                s.game_name["value"]=Select("Select Name from game")
                s.refresh_table()
            
    def select_data(s):
        if s.game_name.get()=="":
            messagebox.showinfo("Error","Plese Choose Your Game Name and Try Again!!")
        else:
            gname = s.game_name.get()

            data = Select("Select * from game where Name ='"+gname+"'")
            row=data[0]

            s.Gid = str(row[0])
            s.GName.delete(0,END)
            s.GName.insert(0,row[1])

            s.GPrice.delete(0,END)
            s.GPrice.insert(0,row[2])

            s.GQty.delete(0,END)
            s.GQty.insert(0,row[3])

            s.platform.set("")
            s.platform.set(row[4])

    def clear_fun(self):
        self.game_name.set("-----Select-----")
        self.GName.delete(0,END)
        self.platform.set("")
        self.GQty.delete(0,END)
        self.GPrice.delete(0,END)      

    def refresh_table(self):
        #Combo box data
        gamedata = Select("Select Name from game")

        GameNameList=[]

        for gamerecord in gamedata:
            GameNameList.append(gamerecord[0])
        
        self.game_name.configure(values=GameNameList)

        #Clear table
        for data in self.table.get_children():
            self.table.delete(data)

        #Adding data in to table
        game_data = Select("Select Name, gType, Price, Quantity From game")

        #Add data in to table
        for game in game_data:
            self.table.insert(parent='',index='end', text="",values=(game[0],game[1],game[2],game[3]))
        

    def DataTable(self):
        #Top Right Frame
        toprightframe = CTkFrame(master=self.Window,width=900,height=200)
        toprightframe.grid(row=0,column=1,padx=5,pady=5,sticky="nswe")

        tfra = CTkFrame(master=toprightframe,corner_radius=10)
        tfra.grid(row=0,column=0,padx=10,pady=10,sticky="nswe")
        
        #Creating Table for Data Display
        self.columns = ("Name", "Platform Type", "Price", "Quantity")
        self.table = ttk.Treeview(master=tfra,columns=self.columns,height=17,selectmode="browse",show="headings")

        #Format
        self.table.column("#1",width=140,minwidth=5,anchor="center")
        self.table.column("#2",width=140,minwidth=5,anchor="center")
        self.table.column("#3",width=100,minwidth=5,anchor="center")
        self.table.column("#4",width=100,minwidth=5,anchor="center")

        #Headings
        self.table.heading("Name",text="Name")
        self.table.heading("Platform Type",text="Platform Type")
        self.table.heading("Price",text="Price")
        self.table.heading("Quantity",text="Quantity")

        self.table.grid(row=0,column=0,padx=10,pady=10)
        
        #Binding table to interact with mouse click
        self.table.bind("<Double-1>",self.selection)

         #Adding data in to table
        game_data = Select("Select Name, gType, Price, Quantity From game")

        #Add data in to table
        for game in game_data:
            self.table.insert(parent='',index='end', text="",values=(game[0],game[1],game[2],game[3]))
    
    def __init__(self):
        self.Window = CTk()
        self.Window.title("Edit Games")
        #self.Window.geometry("900x500")
        self.Window.resizable(0,0)

        self.DataTable()

        #Top Left frame
        topleftframe = CTkFrame(master=self.Window,width=175)
        topleftframe.grid(row=0,column=0,padx=5,pady=5,sticky="nswe")

        
        #Selecting game Name
        game_data = Select("Select Name From game")

        CTkLabel(topleftframe, text="Game Name :").grid(row=0,column=0,padx='0.5c',pady='0.5c')

        self.game_name = CTkComboBox(topleftframe,width=175)
        self.game_name.set("-----Select-----")
        
        GameNameList=[]

        for gamerecord in game_data:
            GameNameList.append(gamerecord[0])
        
        self.game_name.configure(values=GameNameList)
        self.game_name.grid(row=0,column=1,padx='0.5c',pady=1)

        #Select Button
        CTkButton(topleftframe, text="Select Game",width=100,command=self.select_data).grid(row=1,column=0,columnspan=2,padx='0.5c',pady='0.5c')

        #Labels and Entries

        CTkLabel(topleftframe, text="Game Name : ").grid(row=2,column=0,padx="0.5c",pady='0.5c')
        self.GName = CTkEntry(topleftframe,width=175)
        self.GName.grid(row=2,column=1,pady="0.5c")
        
        CTkLabel(topleftframe, text="Price : ").grid(row=4,column=0,padx="0.5c",pady='0.5c')
        self.GPrice = CTkEntry(topleftframe,width=175)
        self.GPrice.grid(row=4,column=1,pady="0.5c")

        CTkLabel(topleftframe, text="Quantity : ").grid(row=5,column=0,padx="0.5c",pady='0.5c')
        self.GQty = CTkEntry(topleftframe,width=175)
        self.GQty.grid(row=5,column=1,pady="0.5c")

        #Combobox and Label for 

        CTkLabel(topleftframe, text="Platform Type : ").grid(row=3,column=0,padx="0.5c",pady='0.5c')

        self.platform = CTkComboBox(topleftframe,width=175)
        self.platform.set("")
        
        PlatFormList=["Pc","Phone","All","Console"]

        self.platform.configure(values=PlatFormList)
        self.platform.grid(row=3,column=1,padx='0.5c',pady='0.5c')
        

        #Bottom Left Frame
        bottomleftframe = CTkFrame(master=self.Window)
        bottomleftframe.grid(row=1,column=0,padx=5,pady=5,sticky="nsew",columnspan=2)
        bottomleftframe.grid_columnconfigure((0,1,2,3,4,5),weight=1)

        # Configure column expansion
        #self.Window.grid_columnconfigure(0, weight=1)  # Left bottom frame expands
        #self.Window.grid_columnconfigure(1, weight=1)  # Right bottom frame expands

        #Buttons

        #Clear
        self.btnClear = CTkButton(bottomleftframe,text="Clear",width=90,command=self.clear_fun).grid(row=0,column=0,padx=15,pady=15)
        
        #Delete
        self.btnDelete = CTkButton(bottomleftframe,text="Delete",width=90,command=self.delete_Fun).grid(row=0,column=1,padx=15,pady=15)

        #Update
        self.btnUpdate = CTkButton(bottomleftframe,text="Update",width=90,command=self.update).grid(row=0,column=2,padx=15,pady=15)

        #File output
        self.btnOutput = CTkButton(bottomleftframe,text="File Output",width=90,command=self.print_file).grid(row=0,column=3,padx=15,pady=15)

        #Refresh
        self.rButton = CTkButton(bottomleftframe, text="Refresh",width=90, command=self.refresh_table).grid(row=0,column=4,padx=15,pady=15)     
    
        #Close
        self.cButton = CTkButton(bottomleftframe, text="Exit",width=90,command=self.btnCloseClick).grid(row=0,column=5,padx=15,pady=15)

        self.Window.mainloop()

editGame()