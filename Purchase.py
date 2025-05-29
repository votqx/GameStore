from customtkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import *
from PIL import Image
from SQL_Functions import *

class Purchase:
    def btnCloseClick(self):
        self.root.destroy()
    
    def selection(self,event):
        selected = self.table.selection()
        data = self.table.item(selected[0])["values"]

        if not selected:
            messagebox.showinfo("Error","Please selecte something first!!")
        
        self.game_name.set(data[0])
    
    def PayOption(self):

        self.selected = str(self.Option.get())

        if self.selected == "Kpay":
            # Create a CTkToplevel window
            win1 = CTkToplevel(self.root)
            win1.resizable(0,0)
            win1.grab_set()  # Make it modal
            win1.title("QR Code")
            
            # Load and display the image
            imgpath = r"Image/QRcodes/bing_generated_qrcode.png"
            img = CTkImage(Image.open(imgpath), size=(500, 500))
            imglabel = CTkLabel(win1, image=img, text="")
            imglabel.grid(row=0, column=0, padx=20, pady=20)

            # Add a close button
            close_button = CTkButton(win1, text="Close", command=win1.destroy)
            close_button.grid(row=1, column=0, padx=20, pady=20)

        elif self.selected == "Wave pay":
            # Create a CTkToplevel window
            win1 = CTkToplevel(self.root)
            win1.resizable(0,0)
            win1.grab_set()  # Make it modal
            win1.title("QR Code")
         
            # Load and display the image
            imgpath = r"Image/QRcodes/wavepay.png"
            img = CTkImage(Image.open(imgpath), size=(500, 500))
            imglabel = CTkLabel(win1, image=img, text="")
            imglabel.grid(row=0, column=0, padx=20, pady=20)

            # Add a close button
            close_button = CTkButton(win1, text="Close", command=win1.destroy)
            close_button.grid(row=1, column=0, padx=20, pady=20)


        elif self.selected == "Aya Pay":
            # Create a CTkToplevel window
            win1 = CTkToplevel(self.root)
            win1.resizable(0,0)
            win1.grab_set()  # Make it modal
            win1.title("QR Code")
         
            # Load and display the image
            imgpath = r"Image/QRcodes/ayapay.png"
            img = CTkImage(Image.open(imgpath), size=(500, 500))
            imglabel = CTkLabel(win1, image=img, text="")
            imglabel.grid(row=0, column=0, padx=20, pady=20)

            # Add a close button
            close_button = CTkButton(win1, text="Close", command=win1.destroy)
            close_button.grid(row=1, column=0, padx=20, pady=20)

        elif self.selected == "Cash":
         
            messagebox.showinfo("Gamestore","Cash Payment Selected.")

        elif self.selected == "Credit Card":
         
            messagebox.showinfo("Gamestore","Credit Card Payment Selected.")


        elif self.selected == "Visa":
            # Create a CTkToplevel window
            win1 = CTkToplevel(self.root)
            win1.resizable(0,0)
            win1.grab_set()  # Make it modal
            win1.title("QR Code")
         
            # Load and display the image
            imgpath = r"Image/QRcodes/visa.png"
            img = CTkImage(Image.open(imgpath), size=(500, 500))
            imglabel = CTkLabel(win1, image=img, text="")
            imglabel.grid(row=0, column=0, padx=20, pady=20)

            # Add a close button
            close_button = CTkButton(win1, text="Close", command=win1.destroy)
            close_button.grid(row=1, column=0, padx=20, pady=20)

            self.Option.set("------Select------")


    def validate_entry(self, new_value):
        if new_value == "":
            return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    def calculateTotal(self):
        game_data = Select("SELECT Price, Quantity FROM game WHERE Name='" + str(self.game_name.get()) + "'")
        quantity = self.quantity.get()

        for gameData in game_data:
            if (quantity == "") or (quantity.isdigit()==False):
                messagebox.showinfo("Error", "Invalid Game Quantity")
            elif (int(quantity) > int(gameData[1])) or (int(quantity) <= 0):
                self.totalAmount.delete(0, END)
                messagebox.showinfo("Error", "Invalid Game Quantity")
            else:
                self.totalAmount.delete(0, END)
                self.totalAmount.insert(0, int(gameData[0]) * int(quantity))            

    def decreacseGameQty(self,gName,decQty):
        RD = Select("select Quantity from game where Name='"+str(gName)+"'")
        BR = RD[0]
        
        Execute("Update game set Quantity= "+str(int(BR[0])-int(decQty))+" where Name='"+str(gName)+"'")
        self.Refresh()
    
    def sell_game(self):
        #retrieve from daata

        game_name = self.game_name.get()
        total = self.totalAmount.get()
        quantity = self.quantity.get()
        saleDate = self.date_entry.get()
        payment = str(self.Option.get())

        if(len(game_name)<2 or (game_name)==""):
            messagebox.showinfo("Error","Invalid Game Name!!\nRefill and Try again!!")
        elif(len(total)<2 or total=="" or (self.quantity.get().isdigit())==False):
            messagebox.showinfo("Error","Invalid Total Amount!!\nRefill and Try again!!")
        elif(len(quantity)<1 or quantity=="" or quantity==0 or (self.quantity.get().isdigit())==False):
            messagebox.showinfo("Error","Invalid Quantity!!\nRefill and Try again.")
        elif(saleDate==""):
            messagebox.showinfo("Error","Invalid Sale Date!!\nPlease Try again")
        elif(payment=="------Select------"):
            messagebox.showinfo("Error","Invalid Payment Option!!\nPlease Try again")
        else:
            self.PayOption()
            '''RD = Select("Select GameID from game Where Name='"+str(game_name)+"'")
            BR=RD[0]'''

            Execute("insert into salerecord(SaleID, GName, SaleQty,TotalAmount,Payment, SaleDate) values('"+str(AutoID('SaleID','salerecord','S'))+"','"+str(game_name)+"','"+str(quantity)+"','"+str(total)+"','"+str(payment)+"','"+str(saleDate)+"')")
            
            self.decreacseGameQty(game_name,quantity)

            #display success message
            messagebox.showinfo("Game Store","Successfully bought ")
            
            #clear from fileds

            self.game_name.set("------Select-----")
            self.totalAmount.delete(0,END)
            self.quantity.delete(0,END)
            self.Option.set("------Select------")
    
    def Add_Cart(self):

        payment = str(self.Option.get())
        selected = ""

        if(self.quantity.get()=="" or self.quantity.get().isdigit()==False):
            messagebox.showinfo("Error","There is nothing in Quantity Entry\nRefill and Try again")
        elif(self.totalAmount.get()==""):
            messagebox.showinfo("Error","Total Amount hasn't calculated yet!!\nPlease Re Fill again!!")
        elif(str(self.Option.get())=="------Select------"):
            messagebox.showinfo("Error","Please Select Payment Option and Try again!!")
        else:
            selected == payment
            if(selected!=payment):
                messagebox.showinfo("Error","Recommened for using the same payment for the items in the cart.")
           
            self.PayOption()
            name = self.game_name.get()
            price = self.totalAmount.get()
            qty = self.quantity.get()
            payment = str(self.Option.get())
                
            #Insert to cart table
            self.ctable.insert(parent='',index="end",text='',values=[name,price,qty,payment])

            #Clear fields
            self.game_name.set("------Select-----")
            self.totalAmount.delete(0, END)
            self.quantity.delete(0, END)
            self.Option.set("------Select------")
        
    def calculate_cart_total(self):
        cart_total = 0
        
        # Iterate over each item in the cart table and sum up the prices
        for line in self.ctable.get_children():
            item_data = self.ctable.item(line)['values']
            price = float(item_data[1])
            quantity = int(item_data[2])
            cart_total += price * quantity

        # Show total as a message
        messagebox.showinfo("Cart Total", f"Total Amount for Cart: ${cart_total:.2f}")

    def buy_cart(self):
        # Sale date entry
        sale_date = self.date_entry.get()
        if not sale_date:
            messagebox.showinfo("Error", "Please select a sale date.")
            return
        
        cart_item = list(self.ctable.get_children())

        if not cart_item :
            messagebox.showinfo("Error","There is nothing in the cart. Please add something first!!")

        #Getting Items in the cart
        for line in cart_item:
            self.item_data = self.ctable.item(line)['values']
            game_name = self.item_data[0]
            price = float(self.item_data[1])
            quantity = int(self.item_data[2])
            payment = self.item_data[3]
                
            # Get GameID from the database using the game name
            game_data = Select(f"SELECT GameID FROM game WHERE Name='{game_name}'")
            if not game_data:
                messagebox.showinfo("Error", f"Game '{game_name}' not found in the database.")
                continue
                
            '''RD = Select("Select GameID from game Where Name='"+str(game_name)+"'")
            BR=RD[0]'''
                                
            # Calculate total amount for this item
            total_amount = price * quantity
                
            # Insert each item as a new record in the salerecord table
            Execute("insert into salerecord(SaleID, GName, SaleQty,TotalAmount,Payment, SaleDate) values('"+str(AutoID('SaleID','salerecord','S'))+"','"+str(game_name)+"','"+str(quantity)+"','"+str(total_amount)+"','"+str(payment)+"','"+str(sale_date)+"')")
            # Update the stock by decreasing the quantity in the game table
            self.decreacseGameQty(game_name, quantity)

        # Display success message
        messagebox.showinfo("Success", "All items in the cart have been purchased successfully!")

        # Clear the cart table
        self.Clear_Cart()
        # Clear input fields
        self.game_name.set("------Select-----")
        self.totalAmount.delete(0, END)
        self.quantity.delete(0, END)

    def Cart(self):
        cframe = CTkFrame(self.root,width=350,height=200)
        cframe.grid(row=0,column=0,padx=5,pady=5,sticky="nswe")

        #Frame for cart table
        ctframe = CTkFrame(cframe)
        ctframe.grid(row=0,column=0,padx=10,pady=10,sticky="nswe")

        #Cart Table
        self.column1 = ("Name","Price","Quantity","Payment")
        self.ctable = ttk.Treeview(master=ctframe,columns=self.column1,height=14,selectmode="browse",show="headings")

        #Formatting
        self.ctable.column("#1",width=100,anchor='w')
        self.ctable.column("#2",width=100,anchor='center')
        self.ctable.column("#3",width=77,anchor='center')
        self.ctable.column("#4",width=100,anchor="center")

        #Heading
        self.ctable.heading("Name",text="Name")
        self.ctable.heading("Price",text="Price")
        self.ctable.heading("Quantity",text="Quantity")
        self.ctable.heading("Payment",text="Payment")

        self.ctable.grid(row=0,column=0,sticky="nswe")

        #Bind table to interact with double click
        self.ctable.bind("<Double-1>",self.single_clear)

        #Buy Button
        buy_button = CTkButton(ctframe,text="Buy",font=("League Gothic", 12, "bold"), fg_color="transparent", border_color="green", corner_radius=8, hover_color="#1ccb1e", border_width=2, command=self.buy_cart)
        buy_button.grid(row=1,column=0,padx=10,pady=10,sticky="w")

        #Clear Button
        clear_button = CTkButton(ctframe,text="Clear Items",font=("League Gothic", 12, "bold"), fg_color="transparent", border_color="red", corner_radius=8, hover_color="#dd2828", border_width=2, command=self.Clear_Cart)
        clear_button.grid(row=1,column=0,padx=10,pady=10,sticky="e")

    def Table(self):
        self.tbframe = CTkFrame(self.root,width=850,height=200)
        self.tbframe.grid(row=0,column=1,padx=10,pady=10,sticky="nswe")

        #Frame for table
        tframe = CTkFrame(self.tbframe)
        tframe.grid(row=0,column=0,padx=10,pady=10,sticky="nswe")

        #Data Table
        self.columns = ("Name","Platform Type","Price","Quantity")
        self.table = ttk.Treeview(master=tframe,columns=self.columns,height=9,selectmode="browse",show="headings")

        #Formatting
        self.table.column("#1",width=230,anchor="w")
        self.table.column("#2",width=220,anchor="center")
        self.table.column("#3",width=200,anchor="center")
        self.table.column("#4",width=200,anchor='center')

        #Heading
        self.table.heading("Name",text="Name")
        self.table.heading("Platform Type",text="Platform Type")
        self.table.heading("Price",text="Price")
        self.table.heading("Quantity",text="Quantity")

        self.table.grid(row=0,column=0,sticky="nswe")

        #Bind table to interact with double click
        self.table.bind("<Double-1>",self.selection)

        #Adding data into table
        game_data = Select("Select Name,gType,Price,Quantity From game")
        
        for record in game_data:
            self.table.insert(parent='',index='end',text='',values=[record[0],record[1],record[2],record[3]])

    #Refresh Table
    def Refresh(self):
        for data in self.table.get_children():
            self.table.delete(data)
       
        #Adding data into table
        game_data = Select("Select Name,gType,Price,Quantity From game")
        
        for record in game_data:
            self.table.insert(parent='',index='end',text='',values=[record[0],record[1],record[2],record[3]])
    
    def Clear_Cart(self):

        for data in self.ctable.get_children():
            self.ctable.delete(data)
    
    #Double click to clear items in cart
    def single_clear(self,event):
        selected = self.ctable.selection()

        if not selected:
            messagebox.showinfo("Error","You can not select a blank place!!")
        else:
            item = self.ctable.item(selected[0])["values"]
            self.ctable.delete(selected[0])
            messagebox.showinfo("Notice",f"{item} have been deleted!!")

    def __init__(self):
        self.root = CTkToplevel()
        self.root.title("Purchase")
        self.root.resizable(0,0)

        # Configure root grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)
        self.root.grid_rowconfigure(0, weight=1)

        # Initialize Table and Cart
        self.Table()
        self.Cart()

        # Button Frame
        bframe = CTkFrame(self.tbframe)
        bframe.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")
        bframe.grid_columnconfigure((0, 1, 2, 3), weight=1)  # Distribute columns evenly

        # Game Name
        CTkLabel(bframe, text="Game Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.game_name = CTkComboBox(bframe, width=200)
        self.game_name.grid(row=0, column=1, padx=5, pady=5,sticky="w")
        self.game_name.set("------Select-----")

        # Load game names
        game_data = Select("SELECT Name FROM game")
        self.game_name.configure(values=[record[0] for record in game_data])

        # Quantity
        CTkLabel(bframe, text="Enter Quantities:").grid(row=0, column=2, padx=2, pady=2, sticky="w")
        self.quantity = CTkEntry(bframe,width=200)
        self.quantity.grid(row=0, column=3,padx=2, pady=2,sticky="w")

        # Total Amount
        CTkLabel(bframe, text="Total Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.totalAmount = CTkEntry(bframe, width=200, validate="key",
                                    validatecommand=(self.root.register(self.validate_entry), '%P'))
        self.totalAmount.grid(row=1, column=1, padx=5, pady=5,sticky="w")

        # Sale Date
        CTkLabel(bframe, text="Sale Date:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.date_entry = DateEntry(bframe, width=20, background="darkblue", foreground="white", borderwidth=2)
        self.date_entry.grid(row=1, column=3, padx=1, pady=5,sticky="w")

        # Buttons
        btn_frame = CTkFrame(bframe)
        btn_frame.grid(row=2, column=1, columnspan=4, pady=10,sticky="w")
        btn_frame.grid_columnconfigure((0, 1, 2, 3,4), weight=1)

        CTkButton(btn_frame, text="Confirm Quantity", command=self.calculateTotal).grid(row=0, column=1, padx=5)
        CTkButton(btn_frame, text="Add to Cart", command=self.Add_Cart).grid(row=0, column=2, padx=5)
        CTkButton(btn_frame, text="Buy", command=self.sell_game).grid(row=0, column=3, padx=5)
        CTkButton(btn_frame, text="Exit", command=self.btnCloseClick).grid(row=0, column=4, padx=5)
        
        #Payment Option
        CTkLabel(bframe,text="Payment Option : ").grid(row=2,column=0,padx=5,pady=5,sticky='w')
        self.Option = CTkComboBox(btn_frame,width=130)
        self.Option.grid(row=0,column=0,padx=5,pady=2)
        self.opt = ['Kpay','Wave pay','Aya Pay','Cash','Credit Card','Visa']
        
        self.Option.set("------Select------")
        self.Option.configure(values=self.opt)

        self.root.mainloop()


#Purchase()