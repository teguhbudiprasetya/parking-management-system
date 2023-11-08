from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class ParkingCheckoutClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Parking Management System | Checkout Parking")
        self.root.config(bg="white")
        self.root.focus_force()

        #ANCHOR - ALL VARIABLES
        # self.con = sqlite3.connect(database = "ims.db")
        self.var_emp_id = StringVar()
        self.var_name = StringVar()
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_email = StringVar()
        self.var_contact = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_gender = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()
        # self.var_address = StringVar()

        #ANCHOR - SEARCH BAR
        searchFrame = LabelFrame(self.root, text="Search", bg="white")
        searchFrame.place(x=250, y=20, width=600, height=70)

        #ANCHOR - OPTIONS
        cmb_search=ttk.Combobox(searchFrame, textvariable=self.var_searchby,values=("Select", "Email", "Name", "Contact"), state='readonly', justify=CENTER)
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(searchFrame, textvariable=self.var_searchtxt,bg='yellow').place(x=200, y=10, width=200)
        btn_search = Button(searchFrame, command=self.search,text="Search", bg='#4caf50', fg='white', cursor='hand2').place(x=410, y=10, width=150, height=20)

        #ANCHOR - TITLE
        title = Label(self.root, text="Employee Details", font=("goudy old style", 15), bg="#0f4d7d", fg="white").place(x=50, y=100, width=1000)

        #ANCHOR - CONTENT

        #SECTION - ROW 1
        lbl_empid = Label(self.root, text="Emp ID", font=("goudy old style", 12), bg="white").place(x=50, y=150)
        lbl_gender = Label(self.root, text="Gender", font=("goudy old style", 12), bg="white").place(x=350, y=150)
        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 12), bg="white").place(x=750, y=150)

        txt_empid = Entry(self.root, textvariable=self.var_emp_id,font=("goudy old style", 12),bg='light yellow').place(x=150, y=150, width=180)
        # txt_gender = Entry(self.root, textvariable=self.var_gender,font=("goudy old style", 12), bg='white').place(x=500, y=150, width=180)
        txt_gender=ttk.Combobox(self.root, textvariable=self.var_gender,values=("Male", "Female"), state='readonly', justify=CENTER)
        txt_gender.place(x=500, y=150, width=180)
        txt_gender.current(0)
        txt_contact = Entry(self.root, textvariable=self.var_contact,font=("goudy old style", 12), bg='light yellow').place(x=850, y=150, width=180)

        #SECTION - ROW 2
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 12), bg="white").place(x=50, y=190)
        lbl_dob = Label(self.root, text="D.O.B", font=("goudy old style", 12), bg="white").place(x=350, y=190)
        lbl_doj = Label(self.root, text="D.O.J", font=("goudy old style", 12), bg="white").place(x=750, y=190)

        txt_name = Entry(self.root, textvariable=self.var_name,font=("goudy old style", 12),bg='light yellow').place(x=150, y=190, width=180)
        txt_dob = Entry(self.root, textvariable=self.var_dob,font=("goudy old style", 12), bg='light yellow').place(x=500, y=190, width=180)
        txt_doj = Entry(self.root, textvariable=self.var_doj,font=("goudy old style", 12), bg='light yellow').place(x=850, y=190, width=180)

        #SECTION - ROW 3
        lbl_email = Label(self.root, text="Email", font=("goudy old style", 12), bg="white").place(x=50, y=230)
        lbl_pass = Label(self.root, text="Password", font=("goudy old style", 12), bg="white").place(x=350, y=230)
        lbl_utype = Label(self.root, text="User Type", font=("goudy old style", 12), bg="white").place(x=750, y=230)

        txt_email = Entry(self.root, textvariable=self.var_email,font=("goudy old style", 12),bg='light yellow').place(x=150, y=230, width=180)
        txt_pass = Entry(self.root, textvariable=self.var_pass,font=("goudy old style", 12), bg='light yellow').place(x=500, y=230, width=180)
        # txt_utype = Entry(self.root, textvariable=self.var_utype,font=("goudy old style", 12), bg='light yellow')
        txt_utype = ttk.Combobox(self.root, textvariable=self.var_utype,values=("Admin", "Employee"), state='readonly', justify=CENTER)
        txt_utype.place(x=850, y=230, width=180)
        txt_utype.current(0)

        #SECTION - ROW 4
        lbl_address = Label(self.root, text="Address", font=("goudy old style", 12), bg="white").place(x=50, y=270)
        lbl_salary = Label(self.root, text="Salary", font=("goudy old style", 12), bg="white").place(x=500, y=270)

        self.txt_address = Text(self.root,font=("goudy old style", 12),bg='light yellow')
        self.txt_address.place(x=150, y=270, width=300, height=60)
        txt_salary = Entry(self.root, textvariable=self.var_salary,font=("goudy old style", 12), bg='light yellow').place(x=600, y=270, width=180)

        #SECTION - BUTTONS
        btn_add = Button(self.root, text="Save", command=self.add, font=("goudy old style", 15), bg='blue', fg='white', cursor='hand2').place(x=500, y=300, width=110, height=30)
        btn_update = Button(self.root, text="Update", command=self.update,font=("goudy old style", 15), bg='green', fg='white', cursor='hand2').place(x=620, y=300, width=110, height=30)
        btn_delete = Button(self.root, text="Delete",command=self.delete ,font=("goudy old style", 15), bg='red', fg='white', cursor='hand2').place(x=740, y=300, width=110, height=30)
        # btn_clear = Button(self.root, text="Clear", command=self.clear,font=("goudy old style", 15), bg='gray', fg='white', cursor='hand2').place(x=860, y=300, width=110, height=30)
        


        #ANCHOR - EMPLOYEE DETAILS / RESULT
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=-1, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("eid", "name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address", "salary"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("eid", text="EMP ID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="Dob")
        self.EmployeeTable.heading("doj", text="Doj")
        self.EmployeeTable.heading("pass", text="Pass")
        self.EmployeeTable.heading("utype", text="Utype")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")

        self.EmployeeTable["show"] = "headings"

        self.EmployeeTable.column("eid", width=90)
        self.EmployeeTable.column("name", width=100)
        self.EmployeeTable.column("email", width=100)
        self.EmployeeTable.column("gender", width=100)
        self.EmployeeTable.column("contact", width=100)
        self.EmployeeTable.column("dob", width=100)
        self.EmployeeTable.column("doj", width=100)
        self.EmployeeTable.column("pass", width=100)
        self.EmployeeTable.column("utype", width=100)
        self.EmployeeTable.column("address", width=100)
        self.EmployeeTable.column("salary", width=100)

        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def show(self):
        con = sqlite3.connect(database = "ims.db")
        cur = con.cursor()
        try:
            cur.execute('select * from employee')
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self,ev):
        f = self.EmployeeTable.focus()
        content = (self.EmployeeTable.item(f))
        row = content['values']
        print(row)
        self.var_emp_id.set(row[0]),
        self.var_name.set(row[1]),
        self.var_email.set(row[2]),
        self.var_gender.set(row[3]),
        self.var_contact.set(row[4]),
        self.var_dob.set(row[5]),
        self.var_doj.set(row[6]),
        self.var_pass.set(row[7]),
        self.var_utype.set(row[8]),
        self.txt_address.delete('1.0', END),
        self.txt_address.insert(END, row[9]),
        self.var_salary.set(row[10])

    #!SECTION FITUR
    def add(self):
        con = sqlite3.connect(database = "ims.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required!", parent=root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "This Employee ID already assigned, try different", parent=self.root)
                else:
                    cur.execute("Insert into employee (eid, name, email, gender, contact, dob, doj, pass, utype, address, salary) values (?,?,?,?,?,?,?,?,?,?,?)",(
                        self.var_emp_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0', END),
                        self.var_salary.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Addedd Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
    
    def update(self):
        con = sqlite3.connect(database = "ims.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required!", parent=root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "This Employee ID is not registered!", parent=self.root)
                else:
                    cur.execute("Update employee set name=?, email=?, gender=?, contact=?, dob=?, doj=?, pass=?, utype=?, address=?, salary=? where eid=?",(
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0', END),
                        self.var_salary.get(),
                        self.var_emp_id.get()
                        
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
    
    def delete(self):
        con = sqlite3.connect(database = "ims.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required!", parent=root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "This Employee ID is not registered!", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Dou you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute('delete from employee where eid=?',(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
    
    def clear(self):
        self.var_name.set(""),
        self.var_email.set(""),
        self.var_gender.set("Male"),
        self.var_contact.set(""),
        self.var_dob.set(""),
        self.var_doj.set(""),
        self.var_pass.set(""),
        self.var_utype.set("Admin"),
        self.txt_address.delete(""'1.0', END),
        self.var_salary.set(""),
        self.var_emp_id.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con = sqlite3.connect(database = "ims.db")
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "" or self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By Option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)

            else:
                cur.execute("select * from employee where "+self.var_searchby.get()+ " LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__== "__main__":
    root = Tk()
    obj = ParkingCheckoutClass(root)
    root.mainloop()