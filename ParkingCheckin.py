from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, filedialog
from tkinter.simpledialog import askstring
import tkinter as tk
import sqlite3
from config import *
from datetime import datetime

class ParkingCheckinClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x500+400+150")
        self.root.title("Parking Management System | Checkin Parking")
        self.root.config(bg="white")
        self.root.focus_force()

        #ANCHOR - ALL VARIABLES
        self.var_parking_id = StringVar()
        self.var_plat = StringVar()
        self.var_pegawai = StringVar()

        #ANCHOR - TITLE
        title = Label(self.root, text="Checkin Parking", font=("goudy old style", 15), bg="#0f4d7d", fg="white").place(x=0, y=0, relwidth=1)

        #ANCHOR - CONTENT

        #SECTION - ROW 1
        lbl_pegawai = Label(self.root, text="Pegawai", font=("goudy old style", 12),bg="white").place(x=200, y=100)
        lbl_parkid = Label(self.root, text="Parking ID", font=("goudy old style", 12),bg="white").place(x=200, y=150)
        lbl_plat = Label(self.root, text="Plat Nomor", font=("goudy old style", 12), bg="white").place(x=200, y=200)

        txt_pegawai=ttk.Combobox(self.root, textvariable=self.var_pegawai,values=getNamaPegawai(), state='readonly', justify=CENTER)
        txt_pegawai.place(x=330, y=100, width=180, height=25)
        txt_pegawai.current(0)
        txt_parkid = Entry(self.root, textvariable=self.var_parking_id,font=("goudy old style", 12), bg='light yellow')
        txt_parkid.place(x=330, y=150, width=180)
        txt_parkid.insert(0, getHighestIdParking()+1) 
        txt_plat = Entry(self.root, textvariable=self.var_plat,font=("goudy old style", 12), bg='light yellow').place(x=330, y=200, width=120)

        #SECTION - BUTTONS
        btn_upload = Button(self.root, text="Up",command=self.upload_image, font=("goudy old style", 12), bg='green', fg='white', cursor='hand2').place(x=460, y=200, width=50, height=25)
        btn_add = Button(self.root, text="Check In",command=self.get_password, font=("goudy old style", 15), bg='blue', fg='white', cursor='hand2').place(x=200, y=250, width=310, height=30)


        #ANCHOR - EMPLOYEE DETAILS / RESULT
        park_frame = Frame(self.root, bd=3, relief=RIDGE)
        park_frame.place(x=-1, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(park_frame, orient=VERTICAL)
        scrollx = Scrollbar(park_frame, orient=HORIZONTAL)

        self.ParkingTable = ttk.Treeview(park_frame, columns=("parking_id", "plat", "waktu", 'pegawai'), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ParkingTable.xview)
        scrolly.config(command=self.ParkingTable.yview)

        self.ParkingTable.heading("parking_id", text="Parking ID")
        self.ParkingTable.heading("plat", text="Plat Nomor")
        self.ParkingTable.heading("waktu", text="Waktu")
        self.ParkingTable.heading("pegawai", text="Pegawai")

        self.ParkingTable["show"] = "headings"

        self.ParkingTable.column("parking_id", width=90)
        self.ParkingTable.column("plat", width=100)
        self.ParkingTable.column("waktu", width=100)
        self.ParkingTable.column("pegawai", width=100)

        self.ParkingTable.pack(fill=BOTH, expand=1)
        self.show()
    
    #!SECTION FITUR
    def add(self, namaParam):
        con = sqlite3.connect(database = "parking.db")
        cur = con.cursor()

        now = datetime.now()
        formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            if self.var_plat.get() == "":
                messagebox.showerror("Error", "Plat nomor must be required!", parent=root)
            else:
                id_pegawai = getIdByName(namaParam)
                cur.execute("Insert into parking (parking_id, plat, waktu, biaya, pegawai_id, waktu_out, pegawai_id_out) values (?,?,?,0,?,0,0)",(
                    self.var_parking_id.get(),
                    self.var_plat.get(),
                    formatted_datetime,
                    id_pegawai,
                ))
                con.commit()
                messagebox.showinfo("Success", "New Parking Addedd Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
    
    def show(self):
        con = sqlite3.connect(database = "parking.db")
        cur = con.cursor()
        try:
            cur.execute('select parking_id, plat, waktu, pegawai_id from parking order by waktu desc')
            rows = cur.fetchall()
            self.ParkingTable.delete(*self.ParkingTable.get_children())
            for row in rows:
                self.ParkingTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

   
    def get_password(self):
        password_inp = askstring("Password Prompt", "Enter your password:", parent=self.root, show="*")
        inputPegawai = self.var_pegawai.get()
        pass_db = getPasswordByName(inputPegawai)
        if password_inp == pass_db:
            print("Entered Correct:", password_inp)
            self.add(inputPegawai)
        else:
            print("Password input canceled")
            messagebox.showerror("Error", f"Password Salah")

    def upload_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

        if file_path:
            print("Selected Image:", file_path)
            plat = deteksi_plat(file_path)
            print(plat)

            self.var_plat.set(plat)

if __name__== "__main__":
    root = Tk()
    obj = ParkingCheckinClass(root)
    root.mainloop()