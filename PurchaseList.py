from customtkinter import *
from SQL_Functions import *
from tkinter import messagebox
from tkinter import ttk 
from tkcalendar import DateEntry
from datetime import datetime
import csv
import os

class PurchaseList:
    def btnClose(self):
        self.Window.destroy()

    def print_file(self):
        desktop = os.path.join(os.path.expanduser("~"),"Desktop")
        folder_name = "Records"
        folder_path = os.path.join(desktop, folder_name)

        #Cerate folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            messagebox.showinfo("Reminder",f"Record folder created at : {folder_path}")
        else:
            messagebox.showinfo("Reminder",f"Record already exists at : {folder_path}")

        #Sale Record CSV file
        file_path = os.path.join(folder_path,"Sale Records.csv")

        Data = Select("SELECT SaleID, GName, SaleQty, TotalAmount, SaleDate, Payment FROM salerecord")

        #Header
        with open(file_path,"w") as file:
            file.write("Sale ID, Game Name, Sale Quantity, Total Amount, Sale Date, Payment\n")
        
        #Append Data into file
        with open(file_path,"a") as file:
            for records in Data:
                file.write(f"{records[0]},{records[1]},{records[2]},{records[3]},{records[4]},{records[5]}\n")


    def search(self):
        
        Sdate = self.search_date.get_date()
        date = Sdate.strftime('%m/%d/%y')
        newdate = date.replace('0','')     

        selected_filter = self.Fliter.get()
        order_filter = self.order.get()

        if selected_filter == "------Select------":
            messagebox.showinfo("Error","Please Select One Option and Try Again.")

        #Determine columnand Order
        if selected_filter == "Sale Quantity":
            order_column = "SaleQty"
        elif selected_filter == "Amount":
            order_column = "TotalAmount"
        else:
            order_column = None

        if order_filter == "Accending":
            order_direction = "ASC"
        elif order_filter == "Decending":
            order_direction = "DESC"
        else:
            order_direction = ""        

        #Build SQL query with ORDER BY
        query = f"SELECT SaleID, GName, SaleQty, TotalAmount, SaleDate, Payment FROM salerecord WHERE SaleDate='{str(newdate)}'"
        if order_column and order_direction:
            query += f"ORDER BY {order_column} {order_direction}"

        SData = Select(query)

        #Clear table
        for data in self.table.get_children():
            self.table.delete(data)
        
        if(selected_filter=="Sale Quantity"):
            #Reordering Titles
            self.table.heading("SaleID", text="Sale Quantities")
            self.table.heading("GName", text="GName")
            self.table.heading("Sale Quantites", text="SaleID")
            self.table.heading("Amount", text="Total Amount")
            self.table.heading("Sale Date", text="Sale Date")
            self.table.heading("Payment Method",text="Payment Method")

            for data1 in SData:
                #Adding Data
                self.table.insert(parent='',index='end',text='',values=[data1[2],data1[1],data1[0],data1[3],data1[4],data1[5]])

        elif(selected_filter=="Amount"):
                   
            #Reording titles
            self.table.heading("SaleID", text="Total Amount")
            self.table.heading("GName", text="GName")
            self.table.heading("Sale Quantites", text="Sale Quantity")
            self.table.heading("Amount", text="SaleID")
            self.table.heading("Sale Date", text="Sale Date")
            self.table.heading("Payment Method",text="Payment Method")
            
            for data4 in SData:
                #Adding Data
                self.table.insert(parent='',index='end', text='',values=(data4[3],data4[1],data4[2],data4[0],data4[4],data4[5]))
        
        #messagebox.showinfo("Request","Please Press The Refresh Button After Searching.")        
    
    def Refresh(self):
        self.table.heading("SaleID",text="SaleID")
        self.table.heading("GName",text="GName")
        self.table.heading("Sale Quantites",text="Sale Quantites")
        self.table.heading("Amount",text="Total Amount")
        self.table.heading("Sale Date",text="Sale Date")
        self.table.heading("Payment Method",text="Payment Method")    

        self.search_date._set_text('----select date----')
        self.Fliter.set("------Select------") 

        for data in self.table.get_children():
            self.table.delete(data)
        
        SData = Select("Select SaleID, GName, SaleQty, TotalAmount, SaleDate, Payment from salerecord")

        for sdata in SData:
            self.table.insert(parent='',index='end',text='',values=(sdata[0],sdata[1],sdata[2],sdata[3],sdata[4],sdata[5]))

    
    def Table(self):
        #Table 
        tframe = CTkFrame(self.Window)
        tframe.grid(row=1,column=0,padx=5,pady=5,sticky="nswe")

        t1frame = CTkFrame(tframe)
        t1frame.grid(row=0,column=0,padx=10,pady=10)

        columns = ("SaleID","GName","Sale Quantites","Amount","Sale Date","Payment Method")

        self.table = ttk.Treeview(master=t1frame,columns=columns,height=10,selectmode="browse",show="headings")

        self.table.column("#1",width=150,anchor='w')
        self.table.column("#2",width=150,anchor="center")
        self.table.column("#3",width=150,anchor='center')
        self.table.column("#4",width=150,anchor="center")
        self.table.column("#5",width=150,anchor="center")
        self.table.column("#6",width=150,anchor="center")


        self.table.heading("SaleID",text="SaleID")
        self.table.heading("GName",text="Game Name")
        self.table.heading("Sale Quantites",text="Sale Quantites")
        self.table.heading("Amount",text="Amount")
        self.table.heading("Sale Date",text="Sale Date")
        self.table.heading("Payment Method",text="Payment Method")

        #Add data
        data = Select("Select SaleID, GName, SaleQty, TotalAmount, SaleDate, Payment from salerecord")

        for record in data:
            self.table.insert(parent='',index='end',text='',values=[record[0],record[1],record[2],record[3],record[4],record[5]])

        self.table.grid(row=0,column=0,padx=10,pady=10,stick="nswe")


    def __init__(self):
        self.Window = CTk()
        self.Window.title("Purchase List")

        self.Window.resizable(0,0)
    
        self.Table()
        
        #Search Area
        sframe = CTkFrame(self.Window)
        sframe.grid(row=0,column=0,padx=5,pady=5,sticky="nswe")

        #Lables and Entries for Search
        #Filter
        CTkLabel(sframe, text="Filter : ").grid(row=0,column=0,padx=5,pady=5)
        self.Fliter = CTkComboBox(sframe,values=["Sale Quantity","Amount"],width=200)
        self.Fliter.grid(row=0,column=1,padx=5,pady=5)
        self.Fliter.set("------Select------")
        
        #Selection
        CTkLabel(sframe, text="Search By Sale Date : ").grid(row=0,column=2,padx=5,pady=5)
        self.search_date = DateEntry(sframe, width=25,background='darkblue',foreground='white', borderwidth=2)
        self.search_date.grid(row=0,column=3,padx=5,pady=5)
        self.search_date._set_text('----select date----') 

        #Accending or Decending Order
        CTkLabel(sframe, text="Order : ").grid(row=0,column=4,padx=5,pady=5)
        self.order = CTkComboBox(sframe,values=["Accending","Decending"] ,width=200)
        self.order.grid(row=0,column=5,padx=5,pady=5)
        self.order.set("------Select------")


        #Button 
        self.search_button = CTkButton(sframe,text="Search",command=self.search)
        self.search_button.grid(row=0,column=6,padx=5,pady=5)

        bframe = CTkFrame(self.Window,height=50)
        bframe.grid(row=2,column=0,padx=5,pady=5,sticky='nswe')
        bframe.grid_columnconfigure((0,1,2),weight=1)

        self.refresh_button = CTkButton(bframe,text="Refresh",command=self.Refresh).grid(row=0,column=0,padx=5,pady=5)

        self.file_button = CTkButton(bframe,text="File Output",command=self.print_file).grid(row=0,column=1,padx=5,pady=5)

        self.close_button = CTkButton(bframe,text="Exit",command=self.btnClose).grid(row=0,column=2,padx=5,pady=5)

        self.Window.mainloop()

PurchaseList()