from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from config import *

class RiwayatClass(ConfigClass):
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x500+400+150")
        self.root.title("Parking Management System | Riwayat")
        self.root.config(bg="white")
        self.root.focus_force()

        #ANCHOR - EMPLOYEE DETAILS / RESULT
        park_frame = Frame(self.root, bd=3, relief=RIDGE)
        park_frame.place(x=-1, y=0, relwidth=1, height=500)

        scrolly = Scrollbar(park_frame, orient=VERTICAL)
        scrollx = Scrollbar(park_frame, orient=HORIZONTAL)

        self.ParkingTable = ttk.Treeview(park_frame, columns=("id_riwayat", "bagian", "pic", "target", "aksi", 'waktu'), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ParkingTable.xview)
        scrolly.config(command=self.ParkingTable.yview)

        self.ParkingTable.heading("id_riwayat", text="ID riwayat")
        self.ParkingTable.heading("bagian", text="Bagian")
        self.ParkingTable.heading("pic", text="PIC")
        self.ParkingTable.heading("target", text="Target")
        self.ParkingTable.heading("aksi", text="Aksi")
        self.ParkingTable.heading("waktu", text="Waktu")

        self.ParkingTable["show"] = "headings"

        self.ParkingTable.column("id_riwayat", width=10)
        self.ParkingTable.column("bagian", width=60)
        self.ParkingTable.column("pic", width=10)
        self.ParkingTable.column("target", width=10)
        self.ParkingTable.column("aksi", width=80)
        self.ParkingTable.column("waktu", width=100)

        self.ParkingTable.pack(fill=BOTH, expand=1)

        self.show()

    def show(self):
        con = sqlite3.connect(database = "parking.db")
        cur = con.cursor()
        try:
            cur.execute('select * from riwayat order by id_riwayat desc')
            rows = cur.fetchall()
            self.ParkingTable.delete(*self.ParkingTable.get_children())
            for row in rows:
                self.ParkingTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

if __name__== "__main__":
    root = Tk()
    obj = RiwayatClass(root)
    root.mainloop()