from tkinter import *
from ParkingCheckin import ParkingCheckinClass
from ParkingCheckout import ParkingCheckoutClass
from config import *
class IMS:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Parking Management System")

        #ANCHOR Title
        title = Label(self.root, text="Parking Management System", font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)

        #ANCHOR btn logout
        # btn_logout = Button(self.root, text="Logout", font=("times new roman", 20, "bold"), bg="yellow").place(x=1150, y=10, height=50, width=150)
        #ANCHOR - CLOCK
        self.lbl_clock = Label(self.root, text="Welcome to IMS\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS", font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        #ANCHOR -  LEFT MENU
        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        LeftMenu.place(x=0, y=100, width=200, height=565)

        lbl_menu = Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="#009688").pack(side=TOP, fill=X)
        btn_checkin = Button(LeftMenu, text="Check In",command=self.checkinParking, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_checkout = Button(LeftMenu, text="Check Out",command=self.checkoutParking, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_category = Button(LeftMenu, text="category", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_product = Button(LeftMenu, text="product", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_sales = Button(LeftMenu, text="sales", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_exit = Button(LeftMenu, text="exit", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)

        #ANCHOR - CONTENT

        self.lbl_checkin = Label(self.root, text=f"Total Parkir Terisi\n[ {getParkirTerisi()} ]",font=("times new roman", 20), bd=5, relief=RIDGE, bg="#33bbf9", fg="white")
        self.lbl_checkin.place(x=300, y=120, height=150, width=300)

        self.lbl_supplier = Label(self.root, text=f'Total supplier\n[ 0 ]',font=("times new roman", 20), bd=5, relief=RIDGE, bg="#ff5722", fg="white")
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)

        self.lbl_category = Label(self.root, text="Total category\n[ 0 ]",font=("times new roman", 20), bd=5, relief=RIDGE, bg="#009688", fg="white")
        self.lbl_category.place(x=1000, y=120, height=150, width=300)

        self.lbl_product = Label(self.root, text="Total product\n[ 0 ]",font=("times new roman", 20), bd=5, relief=RIDGE, bg="#607d8b", fg="white")
        self.lbl_product.place(x=300, y=300, height=150, width=300)

        self.lbl_sales = Label(self.root, text="Total sales\n[ 0 ]",font=("times new roman", 20), bd=5, relief=RIDGE, bg="#ffc107", fg="white")
        self.lbl_sales.place(x=650, y=300, height=150, width=300)
    
    def checkinParking(self):
        self.new_win = Toplevel(self.root)
        self.new_obj=ParkingCheckinClass(self.new_win)

    def checkoutParking(self):
        self.new_win = Toplevel(self.root)
        self.new_obj=ParkingCheckoutClass(self.new_win)

        
root=Tk()
obj=IMS(root)
root.mainloop()