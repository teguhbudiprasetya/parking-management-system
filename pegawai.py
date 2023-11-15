from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
import sqlite3
from datetime import datetime
from config import *

class PegawaiClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x500+400+150")
        self.root.title("Parking Management System | Pegawai")
        self.root.config(bg="white")
        self.root.focus_force()

        #ANCHOR - ALL VARIABLES
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
        title = Label(self.root, text="Pegawai", font=("goudy old style", 15), bg="#0f4d7d", fg="white").place(x=0, y=0, relwidth=1)

        #ANCHOR - EMPLOYEE DETAILS / RESULT
        park_frame = Frame(self.root, bd=3, relief=RIDGE)
        park_frame.place(x=-1, y=150, relwidth=1, height=350)

        scrolly = Scrollbar(park_frame, orient=VERTICAL)
        scrollx = Scrollbar(park_frame, orient=HORIZONTAL)

        self.PegawaiTable = ttk.Treeview(park_frame, columns=("Pegawai ID", "Nama", "Aktif", "Lihat", "Hapus"), show="headings", yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.PegawaiTable.xview)
        scrolly.config(command=self.PegawaiTable.yview)

        self.PegawaiTable.heading("Pegawai ID", text="Pegawai ID")
        self.PegawaiTable.heading("Nama", text="Nama Nomor")
        self.PegawaiTable.heading("Aktif", text="Aktif")
        self.PegawaiTable.heading("Lihat", text="Lihat")
        self.PegawaiTable.heading("Hapus", text="Hapus")


        self.PegawaiTable.column("Pegawai ID", width=10)
        self.PegawaiTable.column("Nama", width=70)
        self.PegawaiTable.column("Aktif", width=110)
        self.PegawaiTable.column("Lihat", width=110)
        self.PegawaiTable.column("Hapus", width=80)

        self.PegawaiTable.pack(fill=BOTH, expand=1)
        # self.PegawaiTable.bind("<ButtonRelease-1>", self.get_data)
        self.PegawaiTable.bind("<ButtonRelease-1>", lambda event: self.on_pegawai_click(event, self.PegawaiTable, self.detail_pegawai, self.get_password_delete))

        self.show()

        self.root.after(1000, self.update_time())

    def show(self):
        con = sqlite3.connect(database = "D:\PBO\PROJECT\parking-management-system\parking.db")
        cur = con.cursor()
        try:
            cur.execute('select * from pegawai')
            rows = cur.fetchall()
            self.PegawaiTable.delete(*self.PegawaiTable.get_children())
            for employee_data in rows:
                pegawai_id, nama, _, aktif = employee_data
                self.PegawaiTable.insert("", "end", values=(pegawai_id, nama, aktif, "Lihat", "Delete"))
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    #!SECTION FITUR
    def get_password_delete(self, pegawai_id):
        password_inp = askstring("Password Prompt", "Hanya admin yang dapat menghapus\nEnter your password:", parent=self.root, show="*")
        if password_inp == getAdminPassword():
            print("Entered Correct:", password_inp)
            self.delete(pegawai_id)
        else:
            print("Password input canceled")
            messagebox.showerror("Error", f"Password Salah")

    def delete(self, pegawai_id):
        con = sqlite3.connect(database="D:\PBO\PROJECT\parking-management-system\parking.db")
        cur = con.cursor()
        try:
            op = messagebox.askyesno("Confirm", "Dou you really want to delete?", parent=self.root)
            if op == True:
                cur.execute("DELETE FROM pegawai WHERE pegawai_id=?", (pegawai_id,))
                con.commit()
                messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
    

    def search(self):
        con = sqlite3.connect(database = "D:\PBO\PROJECT\parking-management-system\parking.db")
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
                    self.PegawaiTable.delete(*self.ParkingTable.get_children())
                    rows = [(t[0], t[1], t[2], t[5], t[3], t[4], t[6]) for t in rows]
                    for row in rows:
                        self.ParkingTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def detail_pegawai(self, pegawai_id):
        self.new_win = Toplevel(self.root)
        self.new_obj=DetailPegawaiClass(self.new_win, pegawai_id)


    def on_pegawai_click(self, event, tree, open_func, delete_func):
    # Function to handle button clicks in the treeview
        item_id = tree.identify_row(event.y)
        if item_id:
            item = tree.item(item_id)
            column = tree.identify_column(event.x)
            col_name = tree.heading(column)["text"]

            if col_name == "Lihat":
                pegawai_id = item["values"][0]
                print(f'Lihat : {pegawai_id}')
                open_func(pegawai_id)
            elif col_name == "Hapus":
                pegawai_id = item["values"][0]
                print(pegawai_id)
                delete_func(pegawai_id)


    def update_time(self):
        self.show()
        self.root.after(1000, self.update_time)


class DetailPegawaiClass (PegawaiClass):
    def __init__(self, root, pegawai_id):
        # super().__init__(root)
        self.root = root
        self.root.geometry("700x500+400+150")
        self.root.title("Parking Management System | Tambah Pegawai")
        self.root.config(bg="white")
        self.root.focus_force()
        self.pegawai_id = pegawai_id

        lbl_plat = Label(self.root, text=self.pegawai_id, font=("goudy old style", 12), bg="white").place(x=350, y=120)
        print(f'pegawai id nya nih {pegawai_id}')

        title = Label(self.root, text="Checkout Parking", font=("goudy old style", 15), bg="#0f4d7d", fg="white").place(x=0, y=0, relwidth=1)
    
if __name__== "__main__":
    root = Tk()
    obj = PegawaiClass(root)
    root.mainloop()
