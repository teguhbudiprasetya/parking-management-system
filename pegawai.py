from tkinter import *
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
import sqlite3
from config import *

def getAdminPassword():
    return "admin"

class PegawaiClass(ConfigClass):
    def __init__(self):
        self.root = Tk()
        
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x500+400+150")
        self.root.title("Parking Management System | Pegawai")
        self.root.config(bg="white")
        self.root.focus_force()

        # ANCHOR - ALL VARIABLES
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        # ANCHOR - SEARCH BAR
        searchFrame = LabelFrame(self.root, text="Search", bg="white")
        searchFrame.place(x=50, y=40, width=600, height=60)

        # ANCHOR - OPTIONS
        cmb_search = ttk.Combobox(searchFrame, textvariable=self.var_searchby, values=("Nama", "ID Pegawai"),
                                  state='readonly', justify=CENTER)
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(searchFrame, textvariable=self.var_searchtxt, bg='yellow')
        txt_search.place(x=200, y=10, width=200)
        btn_search = Button(searchFrame, command=self.search, text="Search", bg='#4caf50', fg='white', cursor='hand2')
        btn_search.place(x=410, y=10, width=150, height=20)

        # ANCHOR - TITLE
        title = Label(self.root, text="Pegawai", font=("goudy old style", 15), bg="#0f4d7d", fg="white").place(x=0, y=0,
                                                                                                            relwidth=1)

        # ANCHOR - EMPLOYEE DETAILS / RESULT
        park_frame = Frame(self.root, bd=3, relief=RIDGE)
        park_frame.place(x=-1, y=150, relwidth=1, height=350)

        scrolly = Scrollbar(park_frame, orient=VERTICAL)
        scrollx = Scrollbar(park_frame, orient=HORIZONTAL)

        self.PegawaiTable = ttk.Treeview(park_frame, columns=("Pegawai ID", "Nama", "Aktif", "Hapus", "Edit"),
                                         show="headings", yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.PegawaiTable.xview)
        scrolly.config(command=self.PegawaiTable.yview)

        self.PegawaiTable.heading("Pegawai ID", text="Pegawai ID")
        self.PegawaiTable.heading("Nama", text="Nama Nomor")
        self.PegawaiTable.heading("Aktif", text="Aktif")
        self.PegawaiTable.heading("Hapus", text="Hapus")
        self.PegawaiTable.heading("Edit", text="Edit")

        self.PegawaiTable.column("Pegawai ID", width=10)
        self.PegawaiTable.column("Nama", width=300)
        self.PegawaiTable.column("Aktif", width=10)
        self.PegawaiTable.column("Hapus", width=10)
        self.PegawaiTable.column("Edit", width=10)

        self.PegawaiTable.pack(fill=BOTH, expand=1)
        self.PegawaiTable.bind("<ButtonRelease-1>", lambda event: self.on_pegawai_click(event))

        btn_tambah = Button(self.root, command=self.tambah_pegawai, text="Tambah Pegawai", bg='#2196f3', fg='white',
                            cursor='hand2')
        btn_tambah.place(x=180, y=110, width=130, height=30, anchor="ne")

        btn_refresh = Button(self.root, command=self.show, text="Refresh", bg='#4caf50', fg='white', cursor='hand2')
        btn_refresh.place(x=560, y=110, width=100, height=25)

        self.show()


    def show(self):
        con = sqlite3.connect(database="parking.db")
        cur = con.cursor()
        try:
            cur.execute('select * from pegawai')
            rows = cur.fetchall()
            self.PegawaiTable.delete(*self.PegawaiTable.get_children())
            for employee_data in rows:
                pegawai_id, nama, _, aktif = employee_data
                self.PegawaiTable.insert("", "end", values=(pegawai_id, nama, aktif, "Delete", "Edit"))
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # !SECTION FITUR
    def get_password_delete(self, pegawai_id):
        password_inp = askstring("Password Prompt",
                                 "Hanya admin yang dapat menghapus\nEnter your password:", parent=self.root, show="*")
        if password_inp == getAdminPassword():
            print("Entered Correct:", password_inp)
            self.delete(pegawai_id)
        else:
            print("Password input canceled")
            messagebox.showerror("Error", f"Password Salah")

    def delete(self, pegawai_id):
        con = sqlite3.connect(database="parking.db")
        cur = con.cursor()
        try:
            op = messagebox.askyesno("Confirm", "Dou you really want to delete?", parent=self.root)
            if op == True:
                cur.execute("DELETE FROM pegawai WHERE pegawai_id=?", (pegawai_id,))
                con.commit()
                messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def edit_pegawai(self, pegawai_id):
        self.new_win_edit = Toplevel(self.root)
        self.new_obj_edit = EditPegawaiClass(self.new_win_edit, pegawai_id, self.show)


    def search(self):
        con = sqlite3.connect(database="parking.db")
        cur = con.cursor()
        
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)

            else:
                if self.var_searchby.get() == "Nama":
                    self.var_searchby.set("nama_pegawai")
                elif self.var_searchby.get() == "ID Pegawai":
                    self.var_searchby.set("pegawai_id")
                print(self.var_searchtxt.get())
                print(self.var_searchby.get())
                cur.execute(
                    "select * from pegawai where " + self.var_searchby.get()+ " LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    print(rows)
                    self.PegawaiTable.delete(*self.PegawaiTable.get_children())
                    rows = [(t[0], t[1], t[3], "Delete", "Edit") for t in rows]
                    for row in rows:
                        self.PegawaiTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


    def tambah_pegawai(self):
        self.new_win_tambah = Toplevel(self.root)
        self.new_obj_tambah = TambahPegawaiClass(self.new_win_tambah, self.show)

    def on_pegawai_click(self, event):
        item_id = self.PegawaiTable.identify_row(event.y)
        if item_id:
            item = self.PegawaiTable.item(item_id)
            column = self.PegawaiTable.identify_column(event.x)
            col_name = self.PegawaiTable.heading(column)["text"]

            if col_name == "Lihat":
                pegawai_id = item["values"][0]
                print(f'Lihat : {pegawai_id}')
                self.detail_pegawai(pegawai_id)
            elif col_name == "Hapus":
                pegawai_id = item["values"][0]
                print(pegawai_id)
                self.get_password_delete(pegawai_id)
            elif col_name == "Edit":
                pegawai_id = item["values"][0]
                print(f'Edit : {pegawai_id}')
                self.edit_pegawai(pegawai_id)

class EditPegawaiClass:
    def __init__(self, root, pegawai_id, refresh_func):
        self.root = root
        self.root.geometry("400x300+500+200")
        self.root.title("Edit Pegawai")
        self.root.config(bg="white")
        self.root.focus_force()

        self.refresh_func = refresh_func
        self.pegawai_id = pegawai_id

        # Variables
        self.var_nama = StringVar()
        self.var_password = StringVar()

        # Fetch data for the selected employee
        self.fetch_data()

        # Label and Entry for Name
        lbl_nama = Label(self.root, text="Nama Pegawai:", font=("goudy old style", 12), bg="white").place(x=50, y=50)
        txt_nama = Entry(self.root, textvariable=self.var_nama, font=("goudy old style", 12), bg='lightgray').place(x=200, y=50)

        # Label and Entry for Password
        lbl_password = Label(self.root, text="Password:", font=("goudy old style", 12), bg="white").place(x=50, y=100)
        txt_password = Entry(self.root, textvariable=self.var_password, show="*", font=("goudy old style", 12), bg='lightgray').place(x=200, y=100)

        # Button to Update
        btn_simpan = Button(self.root, command=self.update_pegawai, text="Update", bg='#4caf50', fg='white', cursor='hand2')
        btn_simpan.place(x=150, y=200, width=100, height=25)

        

    def fetch_data(self):
        try:
            con = sqlite3.connect(database="parking.db")
            cur = con.cursor()
            cur.execute("SELECT nama_pegawai, password FROM pegawai WHERE pegawai_id=?", (self.pegawai_id,))
            row = cur.fetchone()
            if row:
                self.var_nama.set(row[0])
                self.var_password.set(row[1])
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def update_pegawai(self):
        try:
            con = sqlite3.connect(database="parking.db")
            cur = con.cursor()
            cur.execute("UPDATE pegawai SET nama_pegawai=?, password=? WHERE pegawai_id=?",
                        (self.var_nama.get(), self.var_password.get(), self.pegawai_id))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Pegawai Updated Successfully", parent=self.root)
            self.refresh_func()
            self.root.destroy()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

class TambahPegawaiClass:
    def __init__(self, root, refresh_func):
        self.root = root
        self.root.geometry("400x300+500+200")
        self.root.title("Tambah Pegawai")
        self.root.config(bg="white")
        self.root.focus_force()

        self.refresh_func = refresh_func

        # Variable
        self.var_nama = StringVar()
        self.var_password = StringVar()

        # Label dan Entry
        lbl_nama = Label(self.root, text="Nama Pegawai:", font=("goudy old style", 12), bg="white").place(x=50, y=50)
        txt_nama = Entry(self.root, textvariable=self.var_nama, font=("goudy old style", 12), bg='lightgray').place(
            x=200, y=50)

        lbl_password = Label(self.root, text="Password:", font=("goudy old style", 12), bg="white").place(x=50, y=100)
        txt_password = Entry(self.root, textvariable=self.var_password, show="*", font=("goudy old style", 12),
                             bg='lightgray').place(x=200, y=100)

        # Tombol Simpan
        btn_simpan = Button(self.root, command=self.simpan_pegawai, text="Simpan", bg='#4caf50', fg='white',
                            cursor='hand2')
        btn_simpan.place(x=150, y=250, width=100, height=25)

    def simpan_pegawai(self):
        try:
            con = sqlite3.connect(database="parking.db")
            cur = con.cursor()
            cur.execute("INSERT INTO pegawai (nama_pegawai, password, aktif) VALUES (?, ?, ?)",
                        (self.var_nama.get(), self.var_password.get(), "Aktif"))
            con.commit()
            con.close()
            messagebox.showinfo("Sukses", "Pegawai Ditambahkan", parent=self.root)
            self.refresh_func()
            self.root.destroy()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = PegawaiClass(root)
    root.mainloop()
