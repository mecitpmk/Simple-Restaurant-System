"""
Created on Tue Feb 25 22:52:44 2020

@author: Mecit
"""


"""
Resources:
    -- from functools import partial --

    When the create buttons with for loop, ( command= lambda : *args ) is not working.
    There is 2 ways to handle it.
    One of them is .bind method other one is partial method.
    Partial method works like that -> partial(function_name,parameeter)
    As a result program can underestand easily which button pressed.
"""


from tkinter import *
# import msgpack
import pickle
import dbm
from functools import partial
from tkinter import ttk


class RestaurantSystem(Frame):
    all_rest=[]
    def __init__(self,parent):
        """
        
        Arguments:
            Frame {Root} -- tkinter Frame
            parent {frame Root} -- frame Root

            all_rest {list} -- it storage all the restaurant object
            database {dbm} -- database file
    
        Returns:
            None

        """        
        Frame.__init__(self,parent)
        self.parent=parent
        self.pack()
        self.database=dbm.open('RestaurantSystemm.db',"c")
        if len(self.database) != 0:
            get_list=self.database['System']
            get_converted_list=pickle.loads(get_list)
            for get_objects in get_converted_list:
                self.all_rest.append(get_objects)
        else:
            empty_list=[] 
            convert=pickle.dumps(empty_list)
            self.database["System"]=convert
        self.initGUI()
    

    def initGUI(self):
        """
        Labels:
            BIG_TEXT - RESTURANT RESERVATION SYSTEM
            rest_name_label - RESTAURANT NAME LABEL
            num_of_tables_label - NUM OF TABLES LABEL
            rst - RESTAURANT LABEL FOR COMBOBOX
            table_label - WHICH TABLE SELECTED LABEL
            cust_name_label - CUSTOMER NAME LABEL
            cust_phone_label - CUSTOMER PHONE  NUMBER LABEL
            test_delete - WARNING LABEL (INCOMPLETE INFORMATIN , SELECTED TABLE FIRST  ETC .. )
            table_must_int  -  WARNING LABEL (TABLE NUMBER MUST BE INTEGER OR TABLE NUM 6 OR 24 ETC.. )
            are_you_sure_label  - ARE YOU SURE LABEL IF THE DELETE RESTAURANT CLICKED.

        Entries:
            rest_name_entry - RESTAURANT NAME ENTRY
            num_of_tables_entry - NUM OF TABLES ENTRY
            cust_name_entry -  CUSTOMER NAME ENTRY
            cust_phone_entry  - CUSTOMER PHONE NUMBER ENTRY

        Buttons:
            create_rest_button - CREATE RESTAURANT BUTTON 
            save_button -  SAVE (RESERVE) BUTTON
            delete_reserv - DELETE RESERVATION BUTTON
            delete_from_combobox - DELETE RESTAURANT BUTTON

        """        
        self.BIG_TEXT=Label(self,text="Restaurant Reservation System",bg="blue",fg="white",font=("Helvetica",14,"bold"),anchor=CENTER)
        self.BIG_TEXT.grid(row=0,column=0,columnspan=8,sticky=E+W+S+N)
        
        self.rest_name_label=Label(self,text="Restaurant Name:")
        self.rest_name_label.grid(row=1,column=0,sticky=E+W+S+N,padx=20,pady=10)

        self.rest_name_entry=Entry(self)
        self.rest_name_entry.grid(row=1,column=1,sticky=E+W+S+N,pady=10)


        self.num_of_tables_label=Label(self,text="Number Of Tables:")
        self.num_of_tables_label.grid(row=1,column=2,sticky=E+W+S+N,pady=10)


        self.num_of_tables_entry=Entry(self)
        self.num_of_tables_entry.grid(row=1,column=3,sticky=E+W+S+N,pady=10)

        self.create_rest_button=Button(self,text="Create New Restaurant",command=self.create_new_restaurant)
        self.create_rest_button.grid(row=1,column=4,sticky=E+W+S+N,padx=30,pady=10)

        self.rst=Label(self,text="Restaurant:")
        self.rst.grid(row=2,column=0,sticky=E+W+S+N,pady=10)
        self.select_combobox=ttk.Combobox(self,values=self.all_rest) 
        self.select_combobox.grid(row=2,column=1)
        self.select_combobox.bind("<<ComboboxSelected>>",self.create_tables_frame)
        
        self.delete_from_combobox=Button(self,text="Delete Restaurant" , command=self.delete_combobox ,padx=1,pady=1)
        self.delete_from_combobox.grid(row=2,column=2 ,sticky=E+W+S+N, padx= 20 ,pady = 5)
        
        self.are_you_sure_label=Label(self,text="")
        self.are_you_sure_label.grid(row=2,column=3, sticky=E+W+S+N)

        self.table_label_variable=StringVar()
        self.table_label_variable.set("Table: [NOT SELECTED]")
        self.table_label=Label(self,textvariable=self.table_label_variable)
        self.table_label.grid(row=3,column=0,padx=20,sticky=E+W+S+N)

        self.cust_name_label=Label(self,text="Customer Name:")
        self.cust_name_label.grid(row=3,column=1,sticky=E+W+S+N)

        self.cust_name_entry=Entry(self)
        self.cust_name_entry.grid(row=3,column=2,padx=20,sticky=E+W+S+N)

        self.cust_phone_label=Label(self,text="Customer Phone Number:")
        self.cust_phone_label.grid(row=3,column=3,sticky=E+W+S+N)

        self.cust_phone_entry=Entry(self)
        self.cust_phone_entry.grid(row=3,column=4,sticky=E+W+S+N)
        
        self.save_button=Button(self,text="Save/Update Changes",command=self.control_entries)
        self.save_button.grid(row=3,column=5,padx=20,sticky=E+W+S+N)

        self.delete_reserv=Button(self,text="Delete Reservation",command=self.delete_reserve)
        self.delete_reserv.grid(row=3,column=6,padx=20,sticky=E+W+S+N)
        self.test_delete=Label(self,text="")
        self.test_delete.grid(row=3,column=7)

        self.table_must_int=Label(self,text="",anchor=CENTER)
        self.table_must_int.grid(row=1,column=5,sticky=S+W+E+N,columnspan=2,pady=10)

        self.tables_numb=0
    def originals_settings_buttons(self,buttons_name):
        """
        
        Arguments:
            buttons_name {tkinter.Button} -- buttons widget
        Notes:
            This function after the give information to Admin,
            Destroy text in 1.5 seconds with background SystemButtonFace which is Default.
        """        
        self.after(1500,lambda: buttons_name.configure(text="" , bg = "SystemButtonFace"))
    def create_new_restaurant(self):
        """
        Notes:
            If the conditions is True which are Restaurant Name Cannot be empty,
            Also restaurant tables should be integer. If those conditions are True;
            Restaurant will be created as a type of object.
        """        
        if self.rest_name_entry.get() != '':
            try:
                self.convert_int=int(self.num_of_tables_entry.get())
            except:
                self.table_must_int.configure(text="Table Number Must Number!",bg="red",fg="white")
                self.originals_settings_buttons(self.table_must_int)
            else:
                if self.convert_int > 24 or self.convert_int < 6 :
                    self.table_must_int.configure(text="Num. of Tables May Be Between 6 and 24!",bg="red")
                    self.originals_settings_buttons(self.table_must_int)
                else:
                    self.new_rest=self.rest_name_entry.get()
                    self.table_must_int.configure(text="Restaurant Created",bg="green")
                    self.originals_settings_buttons(self.table_must_int)
                    rest_name=self.rest_name_entry.get()
                    self.test_rest_name=rest_name
                    self.test_rest_name=NewRestaurant(rest_name,self.convert_int,{})
                    self.select_combobox.configure(values=self.all_rest)
                    self.convert_to_dumps()
        else:
            self.table_must_int.configure(text="Incomplete Information." , bg = "red")
            self.originals_settings_buttons(self.table_must_int)
    def create_tables_frame(self,event):
        """
        
        Arguments:
            event {class} -- Check The Combobox selected or not?
        
        Notes:
            Create a frame for the restaurant tables.
        """        
        self.new_frame=Frame(self,borderwidth=3,relief=GROOVE)
        self.new_frame.grid(row=4,column=0,columnspan=7,pady=20,sticky=E+W+N+S,padx=20)
        self.create_tables()

    def find_combo(self,find):
        """
        
        Arguments:
            find {str} -- check Combobox.get()
        
        Returns:
            object -- Returns current combobox selected object.
        """        
        for obj_find in self.all_rest:
            if obj_find.rest_name == find:
                self.founded=obj_find
                return self.founded

    def delete_combobox(self):
        """
        Notes:
            This Function When de Admin Click Delete Restaurant Button will Run after that that function create
            One Label
            Two Buttons  which are "Yes" and "No"
            if the Admin click "Yes" :
                get_delete_from_combobox function will run.
            else :
                not_delete_combobox function will run.

        """        
        self.are_you_sure_label.configure(text="Are You Sure?")
        self.yes=Button(self,text="Yes",command=self.get_delete_from_combobox,padx=20)
        self.yes.grid(row=2,column=4)
        self.no=Button(self,text="No",command=self.not_delete_combobox , padx=20)
        self.no.grid(row=2,column=5)

    def get_delete_from_combobox(self):
        """
        Notes:
            If the Admin wants to delete Restaurant , This function provide to delete Restaurant from
            Combobox. Also it's delete from Databases.
        """        
        get_restaurant=self.find_combo(find=self.select_combobox.get())
        if get_restaurant is not None:
            for a in self.all_rest:
                if a == get_restaurant:
                    self.all_rest.remove(get_restaurant)
                    self.test_delete.configure(text="Restaurant Removed." , bg="yellow")
                    self.originals_settings_buttons(self.test_delete)
                    self.select_combobox.configure(values=self.all_rest)
                    self.not_delete_combobox()
                    self.new_frame.destroy()
        else:
            self.test_delete.configure(text="Select Restaurant to Remove!",bg="yellow")
            self.originals_settings_buttons(self.test_delete)
        self.convert_to_dumps()
    def not_delete_combobox(self):
        """
        Notes:
            If The admin wants to delete  Restaurant but after that admin give up from the deleting decision
            this function useful for preventing to delete Restaurant.
        """        
        self.are_you_sure_label.config(text="")
        self.yes.destroy()
        self.no.destroy()
    def create_tables(self):
        """
        Notes:
            It will  create tables automatically with for loop.
            It automatically find tables number from the NewRestaurant object 'num_of_tables' arguments.
        """        
        rowy=4
        columnx=5
        self.all_buttons=[]
        text_numb=1
        variables_test=1
        restaurant_nam=self.find_combo(find=self.select_combobox.get())
        for a in range(restaurant_nam.num_of_tables):
            string=str(text_numb)
            string=Button(self.new_frame,text=text_numb,padx=20,pady=20,bg="green",command=partial(self.tables_selected,text_numb),anchor=CENTER)
            string.grid(row=rowy,column=columnx,padx=40,pady=15,sticky=E+W+N+S)
            if variables_test%8 == 0:
                rowy+=1
                variables_test=0
                columnx=4
            columnx+=1
            variables_test+=1
            text_numb+=1
            self.all_buttons.append(string)

        self.check_reserved_before()
    def tables_selected(self,tables_number):
        """
        
        Arguments:
            tables_number {int} -- Tables Number From The Button Command
        
        Notes:
            If the Tables Selected This function automatically will run.
            Because of the 'command' parameeter.
            It will return Customer Name and Customer Phone information to the Entries.
        """        
        self.table_label_variable.set(f'Table:{tables_number}')
        self.tables_numb=tables_number
        get_obj=self.find_combo(self.select_combobox.get())
        get_cst=get_obj.restaurant_details.get(self.tables_numb)
        get_info=get_cst.get('Customer')
        if get_info == '':
            self.cust_name_entry.delete(0,END)
            self.cust_phone_entry.delete(0,END)
        else:
            self.cust_name_entry.delete(0,END)
            self.cust_phone_entry.delete(0,END)
            self.cust_name_entry.insert(0,get_info.cust_name)
            self.cust_phone_entry.insert(0,get_info.cust_phone)

    def control_entries(self):
        """
        
        Notes:
            Check Customer Name, Customer Phone Entries are succesfully correct
            in terms of phone number [int].
            Also tables not selected. If other entries completed but tables not selected
            ...error will shown in the Frame.
        """        
        if self.tables_numb == 0:
            self.test_delete.configure(text="Select Table First",bg="yellow")
            self.originals_settings_buttons(self.test_delete)
        else:
            if self.cust_name_entry.get() != '':
                try:
                    phone_int=int(self.cust_phone_entry.get())
                except:
                    self.test_delete.configure(text="MUST ONLY INTEGER",bg="red")
                    self.originals_settings_buttons(self.test_delete)
                else:
                    self.get_reserve()
            else:
                self.test_delete.configure(text="INCOMPLETE INFO",bg="red")
                self.originals_settings_buttons(self.test_delete)

    def get_reserve(self):
        """
        Notes:
            If the all Conditions are True which are 'control_entires' and etc..
            Tables will reserved and it will be saved on current restaurant object dictionary.

        """        
        create_cust_obj_name=self.cust_name_entry.get()
        create_cust_obj_phone=int(self.cust_phone_entry.get())
        customer=Customer(create_cust_obj_name,create_cust_obj_phone)
        current_rest=self.find_combo(find=self.select_combobox.get())
        current_rest.restaurant_details.update({self.tables_numb:{'Customer':customer}})
        self.all_buttons[self.tables_numb-1].configure(bg="red")
        self.test_delete.configure(text="Reservation created",bg="green")
        self.originals_settings_buttons(self.test_delete)
        self.convert_to_dumps()

    def check_reserved_before(self):
        """
        Notes:
            When the combobox change, it will identify automatically from the Restaurant Object Dictionary
            Tables are reserved or not?
            If Tables are reserved:
                change tables color and fill with the customer information.
        """        
        rest_name=self.find_combo(self.select_combobox.get())
        for roam in rest_name.restaurant_details:
            get_current_table=rest_name.restaurant_details.get(roam)
            get_cust_name=get_current_table.get('Customer')
            if get_cust_name != '':
                self.all_buttons[roam-1].configure(bg="red")
    def delete_reserve(self):
        """
        Notes:
            It will remove reserved tables from the current Restaurant Object dictionary.

        """        
        current_res=self.find_combo(find=self.select_combobox.get())
        if self.tables_numb != 0:
            current_res.restaurant_details.update({self.tables_numb:{'Customer':''}})
            self.all_buttons[self.tables_numb-1].configure(bg="green")
            self.test_delete.configure(text="Reservation Deleted",bg="blue")
            self.originals_settings_buttons(self.test_delete)
            self.convert_to_dumps()
        else:
            self.test_delete.configure(text="Select Table First.",bg="Yellow")
            self.originals_settings_buttons(self.test_delete)
    
    def convert_to_dumps(self):
        """
        Notes:
            This function make our system Real-Time Based.
            It will automatically save all motion step by step.
            When the restaurant created it will save.
            When the customer reserve a table it will automatically update system.
        """        
        get_noncv_list=self.database['System']
        get_converted=pickle.loads(get_noncv_list)
        get_converted=[]
        for a in self.all_rest:
            get_converted.append(a)
        get_dumps=pickle.dumps(get_converted)
        self.database['System']=get_dumps

class NewRestaurant:
    def __init__(self,rest_name,num_of_tables,restaurant_details):
        """
        
        Arguments:
            rest_name {str} -- Restaurant Name
            num_of_tables {int} -- How much tables belong to this restaurant.
            restaurant_details {dict} -- it Storage Tables , Also Customers.
        """        
        self.rest_name=rest_name
        self.num_of_tables=int(num_of_tables)
        self.restaurant_details=restaurant_details
        self.make_dictionary()
        RestaurantSystem.all_rest.append(self)
    def make_dictionary(self):
        for k in range(self.num_of_tables):
            self.restaurant_details[k+1]={'Customer':''}

    def __str__(self):
        return self.rest_name

class Customer:
    def __init__(self,cust_name,cust_phone):
        """
        
        Arguments:
            cust_name {str} -- Customer Name
            cust_phone {int} -- Customer Phone Number
        """        
        self.cust_name=cust_name
        self.cust_phone=cust_phone




if __name__ == "__main__":
    root = Tk()
    root.title("Restaurant System")
    System=RestaurantSystem(root)
    root.mainloop()

