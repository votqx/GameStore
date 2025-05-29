from customtkinter import *
from tkinter import ttk 
from tkinter import messagebox
from SQL_Functions import *

class GameEntry:
    #Close button
    def btnClose(self):
         self.root.destroy()
        
    #Validate_Entry(allow only numbers)
    def validate_entry(self,new_value):
        if new_value=="":
            return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False
        
    def save_data(self):
        #Getting Data
        gameName = self.nEntry.get()
        
        platform = self.tcb.get()
        
        price = self.pEntry.get()
        
        qty = self.qEntry.get()

        if(len(gameName)<2 or gameName==""):
            messagebox.showinfo("Error","Game Name is Empty!!\nPlease Enter and Try again!!")
        elif(platform=="------Select------"):
            messagebox.showinfo("Error","You haven't selected Platform Type!!\nPlease Enter and Try again")
        elif(len(price)<2 or price==""):
            messagebox.showinfo("Error","Price is Empty!!\nPlease Enter and Try again")
        elif(len(qty)<1 or qty==""):
            messagebox.showinfo("Error","Quantity is Empty!!\nPlease Enter and Tryagain")
        else:
                try:
                    price_value = float(price)  # Convert to float to validate it's a number
                    price_with_tax = (price_value + int(price_value * 0.2))  # Assuming you want to add 20% tax
                except ValueError:
                    messagebox.showinfo("Message", "Invalid Price!! Please enter a valid number.")
                    return
                
                Data = Select("Select * from game where Name='" + str(gameName) + "'")
                
                if len(Data) > 0:
                    messagebox.showinfo("Message", "Invalid Game!\n This game Record already exists!")
                else:
                    # Ensure the SQL statement is correctly formed
                    sql = f"INSERT INTO game (GameID, Name, gType, Price, Quantity) VALUES ('{str(AutoID('GameID', 'game', 'G')).strip()}', '{str(gameName).strip()}', '{str(platform)}', {price_with_tax}, '{str(qty)}');"
                    Execute(sql)
                    messagebox.showinfo("Message", "Data is successfully saved.")

                    self.nEntry.delete(0,END)
                    self.tcb.set("------Select------")
                    self.pEntry.delete(0,END)
                    self.qEntry.delete(0,END)

                    self.Refresh()
        
    def Refresh(self):
        for i1 in self.table.get_children():
            self.table.delete(i1)
        
        tData = Select("Select Name,gType,Price,Quantity from game")

        for d1 in tData:
            self.table.insert(parent='',index='end',text='',values=[d1[0],d1[1],d1[2],d1[3]])


    def Add_Cart(self):
        name = self.nEntry.get()
        platform = self.tcb.get()
        price = self.pEntry.get()
        qty = self.qEntry.get()

        if(len(name)<2 or name==""):
            messagebox.showinfo("Error","Game Name is Empty!!\nPlease Enter and Try again!!")
        elif(platform=="------Select------"):
            messagebox.showinfo("Error","You haven't selected Platform Type!!\nPlease Enter and Try again")
        elif(price=="" or len(price)<2):
            messagebox.showinfo("Error","Price is Empty!!\nPlease Enter and Try again")
        elif(qty=="" or len(qty)<1):
            messagebox.showinfo("Error","Quantity is Empty!!\nPlease Enter and Tryagain")
        else:
            self.ctable.insert(parent='',index='end',text='',values=[name,platform,price,qty])

            self.nEntry.delete(0,END)
            self.tcb.set("------Select------")
            self.pEntry.delete(0,END)
            self.qEntry.delete(0,END)

            #Refresh
            self.Refresh()
    
    def Save_All(self):

        for line in self.ctable.get_children():            
            item = self.ctable.item(line)['values']
            game_name = item[0]
            platform = item[1]
            price = float(item[2])
            quantity = item[3]

            game_data = Select("Select Name from game where Name='"+str(game_name).strip()+"'")

            if(game_name == game_data):
                messagebox.showinfo("Error",f"'{game_name}' already exist!!")
                continue

            price_with_tax = 0
            price_with_tax = (price + int(price * 0.2))  # Assuming you want to add 20% tax

            # Ensure the SQL statement is correctly formed
            sql = f"INSERT INTO game (GameID, Name, gType, Price, Quantity) VALUES ('{str(AutoID('GameID', 'game', 'G')).strip()}', '{str(game_name).strip()}', '{str(platform)}', {price_with_tax}, '{str(quantity)}');"
            Execute(sql)
            
            self.nEntry.delete(0,END)
            self.tcb.set("------Select------")
            self.pEntry.delete(0,END)
            self.qEntry.delete(0,END)            

            self.Refresh()
        
        messagebox.showinfo("Message", "Data is successfully saved.")

        return(self.Clear())

    def Clear(self):
        for i in self.ctable.get_children():
            self.ctable.delete(i)

    def Table(self):
        self.tfra = CTkFrame(self.root)
        self.tfra.grid(row=0,column=1,padx=2,pady=2,sticky='ne')

        #Avaliable Label
        CTkLabel(self.tfra,text='Avaliable Games',font=("Arial",13)).grid(row=0,column=0,padx=5,pady=1,sticky='nw')

        #Data Table
        self.columns = ("Name","Platform","Price","Quantity")
        self.table = ttk.Treeview(master=self.tfra,columns=self.columns,height=5,selectmode='browse',show='headings')

        #Formatting Columns
        self.table.column("#1",width=150,anchor='w')
        self.table.column("#2",width=150,anchor='center')
        self.table.column("#3",width=150,anchor='center')
        self.table.column("#4",width=150,anchor='center')

        #Heading
        self.table.heading("Name",text='Name')
        self.table.heading("Platform",text='Platform')
        self.table.heading("Price",text="Price")
        self.table.heading("Quantity",text='Quantity')

        self.table.grid(row=1,column=0,padx=2,pady=2,sticky='nswe')

        #Add Data into Table
        Data = Select("Select Name,gType,Price,Quantity From game")

        for record in Data:
            self.table.insert(parent='',index='end',text='',values=[record[0],record[1],record[2],record[3]])

    def Cart(self):
        #Cart
        self.cfra = CTkFrame(self.tfra)
        self.cfra.grid(row=2,column=0,padx=5,pady=5,sticky='nswe')

        #Label
        mlabel = CTkLabel(self.cfra,text='Listed Items',font=("Arial",13))
        mlabel.grid(row=0,column=0,sticky='nw')

        #Cart Table
        self.Ccolumns = ("Name","Platform","Price","Quantity")
        self.ctable = ttk.Treeview(master=self.cfra,columns=self.Ccolumns,height=5,selectmode='browse',show='headings')

        #Formatting Columns
        self.ctable.column("#1",width=150,anchor='w')
        self.ctable.column("#2",width=150,anchor='center')
        self.ctable.column("#3",width=150,anchor='center')
        self.ctable.column("#4",width=150,anchor='center')

        #Heading
        self.ctable.heading("Name",text='Name')
        self.ctable.heading("Platform",text='Platform')
        self.ctable.heading("Price",text="Price")
        self.ctable.heading("Quantity",text='Quantity')

        self.ctable.grid(row=1,column=0,sticky='nswe')


    def ShowForm(self):
        self.root = CTk()
        self.root.title("Game Entry")
        self.root.resizable(0,0)
        
        self.price_value = StringVar()
        self.qty_value = StringVar()

        self.Table()
        self.Cart()        
        
        #Labels And Entries
        self.fra = CTkFrame(self.root,width=100,height=250)
        self.fra.grid(row=0,column=0,padx=2,pady=2,sticky='nswe')

        entrylab = CTkLabel(self.fra,text="Entry",font=("Arial Bold",30))
        entrylab.grid(row=0,column=0,padx=10,pady=10)

        self.nlabel = CTkLabel(self.fra,text='Name :')
        self.nlabel.grid(row=1,column=0)

        self.nEntry = CTkEntry(self.fra,width=175)
        self.nEntry.grid(row=1,column=1,padx=10,pady=10)

        self.plabel = CTkLabel(self.fra,text="Price")
        self.plabel.grid(row=3,column=0)

        self.pEntry = CTkEntry(self.fra,width=175,textvariable=self.price_value,validate="key",validatecommand=(self.root.register(self.validate_entry),'%P'))
        self.pEntry.grid(row=3,column=1,padx=10,pady=10)

        self.qlabel = CTkLabel(self.fra,text="Quantity")
        self.qlabel.grid(row=4,column=0)

        self.qEntry = CTkEntry(self.fra,width=175,textvariable=self.qty_value,validate="key",validatecommand=(self.root.register(self.validate_entry),'%P'))
        self.qEntry.grid(row=4,column=1,padx=10,pady=10)

        #Combobox for PlatformType

        self.tlable = CTkLabel(self.fra,text="Platform Type :")
        self.tlable.grid(row=2,column=0)

        self.tcb = CTkComboBox(self.fra,values=["PC","Phone","Console","All"],font=("Arial",14),dropdown_font=('Arial',14),width=175)
        self.tcb.set("------Select------")
        self.tcb.grid(row=2,column=1,padx=10,pady=10)

        #Buttons

        smallframe = CTkFrame(self.fra)
        smallframe.grid(row=5,column=0,columnspan=2,sticky='nswe')
        smallframe.grid_columnconfigure((0,1),weight=1)

        self.sButton = CTkButton(smallframe,text='Save',width=100,command=self.save_data).grid(row=0,column=0,padx=10,pady=10)

        self.aButton = CTkButton(smallframe,text='Add',width=100,command=self.Add_Cart).grid(row=0,column=1,padx=10,pady=10)

        CbFrame = CTkFrame(self.root,width=920,height=50)
        CbFrame.grid(row=1,column=0,padx=2,pady=2,sticky='nswe',columnspan=2) 
        CbFrame.grid_columnconfigure((0,1,2,3),weight=1) 

        self.cButton = CTkButton(CbFrame,text='Exit',width=100,command=self.btnClose).grid(row=0,column=0,padx=5,pady=5)

        self.saButton = CTkButton(CbFrame,text='Save All',width=100,command=self.Save_All).grid(row=0,column=1,padx=5,pady=5)

        self.clButton = CTkButton(CbFrame,text="Clear",width=100,command=self.Clear).grid(row=0,column=2,padx=5,pady=5)

        self.rButton = CTkButton(CbFrame,text='Refresh',width=100,command=self.Refresh).grid(row=0,column=3,padx=5,pady=5)

        self.root.mainloop()

#GameEntry().ShowForm()