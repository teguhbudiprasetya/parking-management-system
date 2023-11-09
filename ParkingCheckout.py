from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
import sqlite3
from datetime import datetime
from config import *

class ParkingCheckoutClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x500+400+150")
        self.root.title("Parking Management System | Checkout Parking")
        self.root.config(bg="white")
        self.root.focus_force()

        #ANCHOR - ALL VARIABLES
        self.var_parking_id = StringVar()
        self.var_plat = StringVar()
        self.var_pegawai = StringVar()
        self.var_pegawai_out = StringVar()
        self.var_waktu = StringVar()
        self.var_waktu_out = StringVar()
        self.var_nama_stnk = StringVar()
        self.var_merek = StringVar()
        self.var_biaya = IntVar()
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()



        #ANCHOR - SEARCH BAR
        searchFrame = LabelFrame(self.root, text="Search", bg="white")
        searchFrame.place(x=50, y=40, width=600, height=60)

        #ANCHOR - OPTIONS
        cmb_search=ttk.Combobox(searchFrame, textvariable=self.var_searchby,values=("Parking ID", "Plat Nomer"), state='readonly', justify=CENTER)
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(searchFrame, textvariable=self.var_searchtxt,bg='yellow').place(x=200, y=10, width=200)
        btn_search = Button(searchFrame, command=self.search,text="Search", bg='#4caf50', fg='white', cursor='hand2').place(x=410, y=10, width=150, height=20)

        #ANCHOR - TITLE
        title = Label(self.root, text="Checkout Parking", font=("goudy old style", 15), bg="#0f4d7d", fg="white").place(x=0, y=0, relwidth=1)

        #ANCHOR - CONTENT

        #SECTION - ROW 1
        lbl_parking_id = Label(self.root, text="Parking ID", font=("goudy old style", 12), bg="white").place(x=50, y=120)
        lbl_plat = Label(self.root, text="Plat nomer", font=("goudy old style", 12), bg="white").place(x=350, y=120)

        txt_parking_id = Entry(self.root, textvariable=self.var_parking_id,font=("goudy old style", 12),bg='light yellow', state="readonly").place(x=150, y=120, width=180)
        txt_plat = Entry(self.root, textvariable=self.var_plat,font=("goudy old style", 12), bg='light yellow', state="readonly").place(x=450, y=120, width=180)

        #SECTION - ROW 2
        lbl_waktu = Label(self.root, text="Waktu masuk", font=("goudy old style", 12), bg="white").place(x=50, y=160)
        lbl_waktu_out = Label(self.root, text="Waktu keluar", font=("goudy old style", 12), bg="white").place(x=350, y=160)

        txt_waktu = Entry(self.root, textvariable=self.var_waktu,font=("goudy old style", 12), bg='light yellow', state="readonly").place(x=150, y=160, width=180)
        txt_waktu_out = Entry(self.root, textvariable=self.var_waktu_out,font=("goudy old style", 12), bg='light yellow', state="readonly").place(x=450, y=160, width=180)

        #SECTION - ROW 3
        lbl_nama_stnk = Label(self.root, text="Nama STNK", font=("goudy old style", 12), bg="white").place(x=50, y=230)
        lbl_pegawai = Label(self.root, text="Pegawai", font=("goudy old style", 12), bg="white").place(x=350, y=230)

        txt_nama_stnk = Entry(self.root, textvariable=self.var_nama_stnk,font=("goudy old style", 12),bg='light yellow').place(x=150, y=230, width=180)
        # txt_pegawai = Entry(self.root, textvariable=self.var_pegawai,font=("goudy old style", 12), bg='light yellow').place(x=450, y=230, width=180)
        txt_pegawai=ttk.Combobox(self.root, textvariable=self.var_pegawai_out,values=getNamaPegawai(), state='readonly', justify=CENTER)
        txt_pegawai.place(x=450, y=230, width=180, height=25)
        txt_pegawai.current(0)

        separator = ttk.Separator(root, orient='horizontal')
        separator.place(x=0, y=210, relwidth=1)

        # #SECTION - ROW 4
        lbl_merek = Label(self.root, text="Merk", font=("goudy old style", 12), bg="white").place(x=50, y=270)
        lbl_rp = Label(self.root, text="Rp.",font=("goudy old style", 18), bg="white").place(x=500, y=270)
        lbl_biaya = Label(self.root, textvariable=self.var_biaya,font=("goudy old style", 18), bg="white").place(x=535, y=270)

        txt_merek = Entry(self.root, textvariable=self.var_merek,font=("goudy old style", 12),bg='light yellow').place(x=150, y=270, width=180)

        #SECTION - BUTTONS
        
        btn_update = Button(self.root, text="Checkout", command=self.get_password,font=("goudy old style", 15), bg='green', fg='white', cursor='hand2').place(x=520, y=310, width=110, height=30)
        


        #ANCHOR - EMPLOYEE DETAILS / RESULT
        park_frame = Frame(self.root, bd=3, relief=RIDGE)
        park_frame.place(x=-1, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(park_frame, orient=VERTICAL)
        scrollx = Scrollbar(park_frame, orient=HORIZONTAL)

        self.ParkingTable = ttk.Treeview(park_frame, columns=("parking_id", "plat", "masuk", "keluar", "biaya", 'pegawai masuk', 'pegawai keluar'), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ParkingTable.xview)
        scrolly.config(command=self.ParkingTable.yview)

        self.ParkingTable.heading("parking_id", text="Parking ID")
        self.ParkingTable.heading("plat", text="Plat Nomor")
        self.ParkingTable.heading("masuk", text="Masuk")
        self.ParkingTable.heading("keluar", text="Keluar")
        self.ParkingTable.heading("biaya", text="Biaya")
        self.ParkingTable.heading("pegawai masuk", text="Pegawai Masuk")
        self.ParkingTable.heading("pegawai keluar", text="Pegawai Keluar")

        self.ParkingTable["show"] = "headings"

        self.ParkingTable.column("parking_id", width=10)
        self.ParkingTable.column("plat", width=70)
        self.ParkingTable.column("masuk", width=110)
        self.ParkingTable.column("keluar", width=110)
        self.ParkingTable.column("biaya", width=80)
        self.ParkingTable.column("pegawai masuk", width=10)
        self.ParkingTable.column("pegawai keluar", width=10)

        self.ParkingTable.pack(fill=BOTH, expand=1)
        self.ParkingTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def show(self):
        con = sqlite3.connect(database = "parking-system/parking.db")
        cur = con.cursor()
        try:
            cur.execute('select * from parking where biaya != 0 order by waktu_out desc')
            rows = cur.fetchall()
            self.ParkingTable.delete(*self.ParkingTable.get_children())
            rows = [(t[0], t[1], t[2], t[5], t[3], t[4], t[6]) for t in rows]
            for row in rows:
                print(row)
                self.ParkingTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self,ev):
        f = self.ParkingTable.focus()
        content = (self.ParkingTable.item(f))
        row = content['values']
        print(row)
        if row[4] < 0.1:
            self.var_parking_id.set(row[0]),
            self.var_plat.set(row[1]),
            self.var_waktu.set(row[2]),

            now = datetime.now()
            formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S')

            self.var_waktu_out.set(formatted_datetime),
            biaya = getKalkulasiBiaya(self.var_parking_id.get(), self.var_waktu_out.get())
            self.var_biaya.set(biaya)
        else:
            messagebox.showerror("Error", "Telah melakukan checkout!", parent=self.root)

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
        con = sqlite3.connect(database = "parking-system/parking.db")
        cur = con.cursor()
        try:
            if self.var_nama_stnk.get() == "" or self.var_merek.get() == "" or self.var_pegawai_out.get() == "":
                messagebox.showerror("Error", "Masih ada kolom yang kosong!", parent=root)
            else:
                id_pegawai = getIdByName(self.var_pegawai_out.get())
                biaya = getKalkulasiBiaya(self.var_parking_id.get(), self.var_waktu_out.get())
                cur.execute("Update parking set biaya=?, waktu_out=?, pegawai_id_out=?, nama_stnk=?, merk=? where parking_id=?",(
                    biaya,
                    self.var_waktu_out.get(),
                    id_pegawai,
                    self.var_nama_stnk.get(),
                    self.var_merek.get(),
                    self.var_parking_id.get(),
                    
                ))
                con.commit()
                messagebox.showinfo("Success", "Checkout Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def get_password(self):
        password_inp = askstring("Password Prompt", "Enter your password:", parent=self.root, show="*")
        inputPegawai = self.var_pegawai_out.get()
        pass_db = getPasswordByName(inputPegawai)
        if password_inp == pass_db:
            print("Entered Correct:", password_inp)
            self.update()
        else:
            print("Password input canceled")
            messagebox.showerror("Error", f"Password Salah")

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
        self.var_parking_id.set(""),
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
        con = sqlite3.connect(database = "parking-system/parking.db")
        cur = con.cursor()
        print(self.var_searchtxt.get())
        print(self.var_searchby.get())
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)

            else:
                if self.var_searchby.get() == "Parking ID":
                    self.var_searchby.set("parking_id")
                elif self.var_searchby.get() == "Plat Nomer":
                    self.var_searchby.set("plat")

                cur.execute("select * from parking where "+self.var_searchby.get()+ " LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ParkingTable.delete(*self.ParkingTable.get_children())
                    rows = [(t[0], t[1], t[2], t[5], t[3], t[4], t[6]) for t in rows]
                    for row in rows:
                        self.ParkingTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__== "__main__":
    root = Tk()
    obj = ParkingCheckoutClass(root)
    root.mainloop()