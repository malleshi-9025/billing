from tkinter import*
from tkinter.font import BOLD  
from PIL import Image,ImageTk #pip install pillow.
from tkinter import ttk,messagebox
import sqlite3
class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="gray")
        self.cart_list=[]


        #===Title=====
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="lightblue",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #===btn_logout=====
        btn_logout=Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1100,y=10,height=50,width=150)

        #===clock===
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15,),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        
        #=======Product Search Frame===
        self.var_search=StringVar()
        ProductFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame.place(x=6,y=110,width=410,height=550)

        pTitle=Label(ProductFrame,text="All Products",font=("goudy old style",20,"bold"),bg="#262026",fg="white").pack(side=TOP,fill=X)

        ProductFrame2=Frame(ProductFrame,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        
        lbl_search=Label(ProductFrame2,text="Search Product | by name",font=("times new roman",15,"bold"),bg="white",fg="lightgreen").place(x=2,y=5)
        lbl_serach=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=5,y=45)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=130,y=47,width=150,height=22)
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",12),bg="#2196f3",fg="white",cursor="hand2").place(x=280,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",12),bg="#083531",fg="white",cursor="hand2").place(x=285,y=10,width=100,height=25)

        #======Product Frame================
        productframe3=Frame(ProductFrame,bd=3,relief=RIDGE) 
        productframe3.place(x=2,y=130,width=398,height=385)

        scrolly=Scrollbar(productframe3,orient=VERTICAL)
        scrollx=Scrollbar(productframe3,orient=HORIZONTAL)

        self.Product_Table=ttk.Treeview(productframe3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.Product_Table.xview)
        scrolly.config(command=self.Product_Table.yview)

        self.Product_Table.heading("pid",text="PID")
        self.Product_Table.heading("name",text="Name")
        self.Product_Table.heading("price",text="Price")
        self.Product_Table.heading("qty",text="Qty")
        self.Product_Table.heading("status",text="Status")
        self.Product_Table["show"]="headings"
        self.Product_Table.column("pid",width=50)
        self.Product_Table.column("name",width=100)
        self.Product_Table.column("price",width=100)
        self.Product_Table.column("qty",width=100)
        self.Product_Table.column("status",width=50)
        self.Product_Table.pack(fill=BOTH,expand=1)
        self.Product_Table.bind("<ButtonRelease-1>",self.get_data)
        lbl_note=Label(ProductFrame,text="Note: Enter '0' qty to Remove the product from cart",font=("goudy old style",12),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)

        #===CustomerFrame===
        self.var_name=StringVar()
        self.var_cantact=StringVar()
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white") 
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        cTitle=Label(CustomerFrame,text="Customer Detail",font=("goudy old style",15),bg="lightgray",fg="white").pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15,),bg="white").place(x=4,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_name,font=("times new roman",15),bg="lightyellow").place(x=80,y=35,width=180)
        
        lbl_contact=Label(CustomerFrame,text="Contact",font=("times new roman",15,),bg="white").place(x=270,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_cantact,font=("times new roman",15),bg="lightyellow").place(x=340,y=35,width=180)

        #======Calc Cart Frame================
        Cal_cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white") 
        Cal_cart_Frame.place(x=420,y=190,width=530,height=370)

        #======Calculator Frame================
        self.var_cal_input=StringVar()
        Cal_Frame=Frame(Cal_cart_Frame,bd=2,relief=RIDGE,bg="white") 
        Cal_Frame.place(x=5,y=10,width=268,height=340)

        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(Cal_Frame,text='7',font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text='8',font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text='9',font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=3)
        
        btn_4=Button(Cal_Frame,text='4',font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text='5',font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text='6',font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=3)
        
        btn_1=Button(Cal_Frame,text='1',font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=15,cursor='hand2').grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text='2',font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=15,cursor='hand2').grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text='3',font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=15,cursor='hand2').grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=15,cursor='hand2').grid(row=3,column=3)
        
        btn_0=Button(Cal_Frame,text='0',font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text='c',font=('arial',15,'bold'),command=self.clear_calc,bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform_calc,bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=3)


        cart_frame=Frame(Cal_cart_Frame,bd=3,relief=RIDGE) 
        cart_frame.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(cart_frame,text="Cart \t Total Product: [0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(cart_frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_frame,orient=HORIZONTAL)

        self.CartTable=ttk.Treeview(cart_frame,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid",text="PID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Amount")
        self.CartTable.heading("qty",text="Qty")
        self.CartTable.heading("status",text="Status")
        self.CartTable["show"]="headings"
        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=200)
        self.CartTable.column("price",width=70)
        self.CartTable.column("qty",width=50)
        self.CartTable.column("status",width=90)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        #===Add Cart Widgets Frame============
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_qty=StringVar()
        self.var_price=StringVar()
        self.var_stock=StringVar()

        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white") 
        Add_CartWidgetsFrame.place(x=420,y=550,width=530,height=110)

        lbl_p_name=Label(Add_CartWidgetsFrame,text="Product name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightgray",state='readonly').place(x=5,y=35,width=190,height=22)
        
        lbl_p_price=Label(Add_CartWidgetsFrame,text="Price per Qty",font=("times new roman",15),bg="white").place(x=210,y=5)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("times new roman",15),bg="lightgray",state='readonly').place(x=210,y=35,width=130,height=22)
        
        lbl_p_qty=Label(Add_CartWidgetsFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=380,y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=380,y=35,width=130,height=22)

        self.lbl_instock=Label(Add_CartWidgetsFrame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=5,y=70)

        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",font=("times new roman",15,BOLD),bg="lightgray",cursor="hand2").place(x=180,y=70,width=140,height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",15),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)
        
        #======Billing Area========
        BillFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        BillFrame.place(x=950,y=110,width=410,height=410)
        
        BTitle=Label(BillFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(BillFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(BillFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #=========Billing buttons============
        BillMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        BillMenuFrame.place(x=950,y=520,width=410,height=140)

        self.lbl_amt=Label(BillMenuFrame,text='Bill Amount\n[0]',font=("goudy old style",15,'bold'),bg="#3f51b5",fg="white")
        self.lbl_amt.place(x=2,y=5,width=120,height=70)
        
        self.lbl_disamt=Label(BillMenuFrame,text='Discount \n[5%]',font=("goudy old style",15,'bold'),bg="#8bc34a",fg="white")
        self.lbl_disamt.place(x=124,y=5,width=120,height=70)
        
        self.lbl_net_pay=Label(BillMenuFrame,text='Net Amount\n[0]',font=("goudy old style",15,'bold'),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=245,y=5,width=160,height=70)
        
        
        btn_print=Button(BillMenuFrame,text='Print Bill ',cursor='hand2',font=("goudy old style",15,'bold'),bg="lightgreen",fg="white")
        btn_print.place(x=2,y=80,width=120,height=50)
        
        btn_clear_all=Button(BillMenuFrame,text='Clear All',cursor='hand2',font=("goudy old style",15,'bold'),bg="gray",fg="white")
        btn_clear_all.place(x=124,y=80,width=120,height=50)
        
        btn_genrate=Button(BillMenuFrame,text='Genrate/Save Bill',cursor='hand2',font=("goudy old style",15,'bold'),bg="olive",fg="white")
        btn_genrate.place(x=245,y=80,width=160,height=50)

        #=========footer=============
        footer=Label(self.root,text="IMS- Inventory Management System | Developed by Coder \n"+"For any technical issue call by 984xxxxxxx \n",font=("times new roman",9),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)

        self.show()
        #=================Functions==============
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)
    
    def clear_calc(self):
        self.var_cal_input.set('')

    def perform_calc(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))


    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            #self.Product_Table=ttk.Treeview(productframe3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
            cur.execute("select itemid,product,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.Product_Table.delete(*self.Product_Table.get_children())
            for row in rows:
                self.Product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)



    #======================Search Procedure==========================================
    def search(self):
            con=sqlite3.connect(database=r'ims.db')
            cur=con.cursor()
            try:
                if self.var_search.get()=="":
                    messagebox.showerror("Error","Search input should be required",parent=self.root)
                else:
                    cur.execute("Select itemid,product,price,qty,status from product WHERE product LIKE '%"+str(self.var_search.get())+"%' and status='Active'")
                    rows=cur.fetchall()
                    if len(rows)!=0:
                        self.Product_Table.delete(*self.Product_Table.get_children())
                        for row in rows:
                            self.Product_Table.insert('',END,values=row)
                    else:
                        messagebox.showerror("Error","Record is not found...!",parent=self.root)
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)    


    def get_data(self,ev):
        f=self.Product_Table.focus()
        content=(self.Product_Table.item(f))
        row=content['values']    
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock[{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']    
        #itemid,product,price,qty,stock
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock[{str(row[4])}]")
        self.var_stock.set(row[4])
        

    def add_update_cart(self):
        if  self.var_pid.get()=='':
            messagebox.showerror('Error',"Please select product from the list",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror('Error',"quantity is Required",parent=self.root)
        else:
            #price_cal=int(self.var_qty.get())*float(self.var_price.get())
            #price_cal=float(price_cal)
            price_cal=self.var_price.get()

            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            # ===== Update cart===
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                 op=messagebox.askyesno('Confirm',"Product allready present\nDo you want to update | Remove from the cart list",parent=self.root)
                 if op==True:
                    if self.var_qty.get()=="0":
                       self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal #price
                        self.cart_list[index_][3]=self.var_qty.get()  #qty
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()
    
    def bill_updates(self):
        bill_amt=0
        net_pay=0
        for row in self.cart_list:
            #itemid,product,price,qty,stock
            bill_amt=bill_amt+(float(row[2])*int(row[3]))
            net_pay=bill_amt-((bill_amt*5)/100)
            self.lbl_amt.config(text=f'Bill Amount(Rs.)\n[{str(bill_amt)}]')
            self.lbl_net_pay.config(text=f'Net Pay(Rs.)\n[{str(net_pay)}]')
            self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")
    
    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


if __name__== "__main__":
    root=Tk()
    obj=BillClass(root)
    root.mainloop()