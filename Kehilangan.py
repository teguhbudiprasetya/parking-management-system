from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class KehilanganClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x500+300+100")
        self.root.title("Parking Management System | Barang Kehilangan")
        self.root.config(bg="white")
        self.root.focus_force()

        # ALL VARIABLES
        self.var_id_hilang = StringVar()
        self.var_nama = StringVar()
        self.var_kontak = StringVar()
        self.var_waktu = StringVar()
        self.var_nama_barang = StringVar()
        self.var_ciri_barang = StringVar()

        # TITLE
        title = Label(self.root, text="DashBoard Kehilangan", font=("goudy old style", 15), bg="#0f4d7d", fg="white").place(x=0, y=0, relwidth=1)

        # CONTENT
        # ROW 1
        lbl_nama = Label(self.root, text="Nama", font=("goudy old style", 12), bg="white").place(x=50, y=120)
        lbl_kontak = Label(self.root, text="Kontak", font=("goudy old style", 12), bg="white").place(x=350, y=120)

        txt_nama = Entry(self.root, textvariable=self.var_nama, font=("goudy old style", 12), bg='light yellow').place(x=150, y=120, width=180)
        txt_kontak = Entry(self.root, textvariable=self.var_kontak, font=("goudy old style", 12), bg='light yellow').place(x=450, y=120, width=180)

        # ROW 2
        lbl_nama_barang = Label(self.root, text="Nama Barang", font=("goudy old style", 12), bg="white").place(x=50, y=160)
        lbl_ciri_barang = Label(self.root, text="Ciri Barang", font=("goudy old style", 12), bg="white").place(x=350, y=160)

        txt_nama_barang = Entry(self.root, textvariable=self.var_nama_barang, font=("goudy old style", 12), bg='light yellow').place(x=150, y=160, width=180)
        txt_ciri_barang = Entry(self.root, textvariable=self.var_ciri_barang, font=("goudy old style", 12), bg='light yellow').place(x=450, y=160, width=180)

        separator = ttk.Separator(root, orient='horizontal')
        separator.place(x=0, y=200, relwidth=1)

        # BUTTONS
        btn_add = Button(self.root, text="Simpan", font=("goudy old style", 15), bg='blue', fg='white', cursor='hand2', command=self.add).place(x=200, y=230, width=150, height=30)
        btn_view_details = Button(self.root, text="Lihat Detail", font=("goudy old style", 15), bg='green', fg='white', cursor='hand2', command=self.view_details).place(x=370, y=230, width=150, height=30)
        btn_update_status = Button(self.root, text="Update Status", font=("goudy old style", 15), bg='orange', fg='white', cursor='hand2', command=self.update_status).place(x=200, y=270, width=320, height=30)

        # EMPLOYEE DETAILS / RESULT
        park_frame = Frame(self.root, bd=0, relief=RIDGE)
        park_frame.place(x=-1, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(park_frame, orient=VERTICAL)
        scrollx = Scrollbar(park_frame, orient=HORIZONTAL)

        self.KehilanganTable = ttk.Treeview(park_frame, columns=("id_hilang", "nama", "kontak", 'waktu', "nama_barang", "ciri_barang", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.KehilanganTable.xview)
        scrolly.config(command=self.KehilanganTable.yview)

        self.KehilanganTable.heading("id_hilang", text="ID hilang")
        self.KehilanganTable.heading("nama", text="Nama")
        self.KehilanganTable.heading("kontak", text="Kontak")
        self.KehilanganTable.heading("waktu", text="Waktu Kehilangan")
        self.KehilanganTable.heading("nama_barang", text="Nama Barang")
        self.KehilanganTable.heading("ciri_barang", text="Ciri-ciri Barang")
        self.KehilanganTable.heading("status", text="Status")

        self.KehilanganTable["show"] = "headings"

        self.KehilanganTable.column("id_hilang", width=90)
        self.KehilanganTable.column("nama", width=100)
        self.KehilanganTable.column("kontak", width=100)
        self.KehilanganTable.column("waktu", width=120)
        self.KehilanganTable.column("nama_barang", width=120)
        self.KehilanganTable.column("ciri_barang", width=120)
        self.KehilanganTable.column("status", width=90)

        self.KehilanganTable.pack(fill=BOTH, expand=1)
        self.show()

    def add(self):
        con = sqlite3.connect(database="parking.db")
        cur = con.cursor()

        now = datetime.now()
        formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S')

        try:
            if not self.var_nama_barang.get():
                messagebox.showerror("Error", "Nama Barang must be required!", parent=self.root)
            else:
                cur.execute("INSERT INTO kehilangan (nama, kontak, waktu, nama_barang, ciri_barang, status) VALUES (?,?,?,?,?,?)", (
                    self.var_nama.get(),
                    self.var_kontak.get(),
                    formatted_datetime,
                    self.var_nama_barang.get(),
                    self.var_ciri_barang.get(),
                    "Hilang",  # Default status is set to "Hilang" when adding a new item
                ))
                con.commit()
                messagebox.showinfo("Success", "Barang Hilang Added Successfully", parent=self.root)
                self.show()
                self.clear_fields()  # Call the method to clear fields after successful addition
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")
        finally:
            con.close()

    def clear_fields(self):
        # Clear all entry fields
        self.var_nama.set("")
        self.var_kontak.set("")
        self.var_nama_barang.set("")
        self.var_ciri_barang.set("")

    def show(self):
        con = sqlite3.connect(database="parking.db")
        cur = con.cursor()
        try:
            cur.execute('SELECT id_hilang, nama, kontak, waktu, nama_barang, ciri_barang, status FROM kehilangan')
            rows = cur.fetchall()

            # Clear previous data in the Treeview
            for item in self.KehilanganTable.get_children():
                self.KehilanganTable.delete(item)

            # Insert new data into the Treeview
            for row in rows:
                self.KehilanganTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def view_details(self):
        selected_item = self.KehilanganTable.selection()
        if not selected_item:
            messagebox.showinfo("Information", "Please select a row to view details.")
            return

        selected_id = self.KehilanganTable.item(selected_item, 'values')[0]  # Assuming the ID is the first column
        con = sqlite3.connect(database="parking.db")
        cur = con.cursor()

        try:
            cur.execute('SELECT * FROM kehilangan WHERE id_hilang = ?', (selected_id,))
            details = cur.fetchone()
            if details:
                details_window = Toplevel(self.root)
                details_window.title("Details of Barang Hilang")

                # Display details in the new window
                Label(details_window, text=f"ID: {details[0]}").pack()
                Label(details_window, text=f"Nama: {details[1]}").pack()
                Label(details_window, text=f"Kontak: {details[2]}").pack()
                Label(details_window, text=f"Waktu Kehilangan: {details[3]}").pack()
                Label(details_window, text=f"Nama Barang: {details[4]}").pack()
                Label(details_window, text=f"Ciri Barang: {details[5]}").pack()
                Label(details_window, text=f"Status: {details[6]}").pack()

            else:
                messagebox.showerror("Error", "Details not found.")
        except Exception as ex:
            messagebox.showerror("Error", f"Error retrieving details due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def update_status(self):
        selected_item = self.KehilanganTable.selection()
        if not selected_item:
            messagebox.showinfo("Information", "Please select a row to update status.")
            return

        selected_id = self.KehilanganTable.item(selected_item, 'values')[0]  # Assuming the ID is the first column
        new_status = messagebox.askquestion("Update Status", "Have you found the lost item?")

        if new_status == "yes":
            new_status = "Ditemukan"
        else:
            new_status = "Hilang"

        con = sqlite3.connect(database="parking.db")
        cur = con.cursor()

        try:
            cur.execute('UPDATE kehilangan SET status=? WHERE id_hilang=?', (new_status, selected_id))
            con.commit()
            messagebox.showinfo("Success", "Status Updated Successfully", parent=self.root)
            self.show()  # Refresh the displayed data after updating the status
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating status due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = KehilanganClass(root)
    root.mainloop()
