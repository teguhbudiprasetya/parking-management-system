from tkinter import *
from ParkingCheckin import ParkingCheckinClass
from ParkingCheckout import ParkingCheckoutClass
from Pegawai import PegawaiClass
from Kehilangan import KehilanganClass
from Riwayat import RiwayatClass
from config import *
from datetime import datetime

class IMS:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Parking Management System")

        #ANCHOR Title
        title = Label(self.root, text="Parking Management System", font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)

        #ANCHOR - CLOCK
        now = datetime.now()
        date = now.strftime('%Y-%m-%d %H:%M:%S')
        time = now.strftime('%H:%M:%S')
        self.lbl_clock = Label(self.root, text=f"Welcome to PMS\t\t Date: {date}\t\t Time: {time}", font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)


        #ANCHOR -  LEFT MENU
        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        LeftMenu.place(x=0, y=100, width=200, height=565)

        lbl_menu = Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="#009688").pack(side=TOP, fill=X)
        btn_checkin = Button(LeftMenu, text="Check In",command=self.checkinParking, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_checkout = Button(LeftMenu, text="Check Out",command=self.checkoutParking, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_kehilangan = Button(LeftMenu, text="Kehilangan", command=self.Kehilangan, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_riwayat = Button(LeftMenu, text="Riwayat", command=self.Riwayat, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_pegawai = Button(LeftMenu, text="Pegawai",command=self.Pegawai ,font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_exit = Button(LeftMenu, text="exit", command=self.root.destroy, font=("times new roman", 20, "bold"), bg="red", fg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)

        #ANCHOR - CONTENT

        self.lbl_checkin = Label(self.root, text=f"Total Parkir Terisi\n[ {getParkirTerisi()} ]",font=("times new roman", 20), bd=5, relief=RIDGE, bg="#33bbf9", fg="white")
        self.lbl_checkin.place(x=300, y=120, height=150, width=300)

        self.lbl_checkout = Label(self.root, text=f'Parkir Keluar Hari ini\n[ {getParkirKeluar()} ]',font=("times new roman", 20), bd=5, relief=RIDGE, bg="#ff5722", fg="white")
        self.lbl_checkout.place(x=650, y=120, height=150, width=300)

        self.lbl_barang_kehilangan = Label(self.root, text=f'Barang kehilangan\n[{getParkirTerisiNow()}]',font=("times new roman", 20), bd=5, relief=RIDGE, bg="#009688", fg="white")
        self.lbl_barang_kehilangan.place(x=1000, y=120, height=150, width=300)

        self.lbl_inToday = Label(self.root, text=f'Parkir Masuk Hari Ini\n[{getBarangHilang()}]',font=("times new roman", 20), bd=5, relief=RIDGE, bg="#607d8b", fg="white")
        self.lbl_inToday.place(x=300, y=300, height=150, width=300)

        self.update_time()
    
    def checkinParking(self):
        self.new_win = Toplevel(self.root)
        self.new_obj=ParkingCheckinClass(self.new_win)

    def checkoutParking(self):
        self.new_win = Toplevel(self.root)
        self.new_obj=ParkingCheckoutClass(self.new_win)

    def Pegawai(self):
        self.new_win = Toplevel(self.root)
        self.new_obj=PegawaiClass(self.new_win)

    def Kehilangan(self):
        self.new_win = Toplevel(self.root)
        self.new_obj=KehilanganClass(self.new_win)

    def Riwayat(self):
        self.new_win = Toplevel(self.root)
        self.new_obj=RiwayatClass(self.new_win)

    def update_time(self):
        # Get the current time
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')

        # Update the label text
        self.lbl_clock.config(text=f"Welcome to PMS\t\t Date: {date}\t\t Time: {time}")
        self.lbl_checkin.config(text=f"Parkir Terisi\n[ {getParkirTerisi()} ]")
        self.lbl_checkout.config(text=f"Parkir Keluar Hari Ini\n[ {getParkirKeluar()} ]")
        self.lbl_barang_kehilangan.config(text=f"Barang Kehilangan\n[ {getBarangHilang()} ]")
        self.lbl_inToday.config(text=f"Parkir Masuk Hari Ini\n[ {getParkirTerisiNow()} ]")

        # Schedule the update_time function to be called after 1000 milliseconds (1 second)
        self.root.after(1000, self.update_time)
        
root=Tk()
obj=IMS(root)
root.mainloop()