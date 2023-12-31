import tkinter as tk
from tkinter import ttk, filedialog
import sqlite3
from datetime import datetime

class ConfigClass:
    def getParkirTerisi(self):
        con = sqlite3.connect(database = "parking.db")
        cur = con.cursor()
        cur.execute("Select * from parking where biaya = 0")
        rows = cur.fetchall()
        con.close()
        return len(rows)
    
    def getParkirTerisiNow(self):
        con = sqlite3.connect(database = "parking.db")
        cur = con.cursor()
        now = datetime.now().strftime('%Y-%m-%d')
        cur.execute("Select * from parking where biaya = 0 and waktu LIKE '%"+now+"%'")
        rows = cur.fetchall()
        con.close()
        # print(rows)
        return len(rows)
    
    def getParkirKeluar(self):
        con = sqlite3.connect(database = "parking.db")
        cur = con.cursor()
        now = datetime.now().strftime('%Y-%m-%d')
        cur.execute("SELECT * FROM parking WHERE waktu_OUT LIKE '%"+now+"%'")
        rows = cur.fetchall()
        con.close()
        return len(rows)
    
    def getBarangHilang(self):
        con = sqlite3.connect(database = "parking.db")
        cur = con.cursor()
        now = datetime.now().strftime('%Y-%m-%d')
        cur.execute("SELECT * FROM kehilangan WHERE status='Hilang'")
        rows = cur.fetchall()
        con.close()
        return len(rows)

    def getPegawai(self):
        con = sqlite3.connect(database = "parking.db")
        cur = con.cursor()
        cur.execute("Select * from pegawai where pegawai_id != 0")
        rows = cur.fetchall()
        # result = [row[1] for row in rows]
        con.close()
        ids, names, passwords, aktif = [], [], [], []
        for item in rows:
            id, name, password, _ = item
            ids.append(id)
            names.append(name)
            passwords.append(password)
        return ids, names, passwords

    def getNamaPegawai(self):
        _,nama,_ = self.getPegawai()
        return nama
    def getPasswordPegawai(self):
        _,_,password = self.getPegawai()
        return password

    def getPasswordByName(self, namaParam):
        con = sqlite3.connect(database = "parking.db")
        cur = con.cursor()
        cur.execute("Select password from pegawai where nama_pegawai=?",(namaParam,))
        rows = cur.fetchone()
        password = rows[0]
        con.close()
        return password

    def getPasswordByID(self, idParam):
        con = sqlite3.connect(database = "parking.db")
        cur = con.cursor()
        cur.execute("Select password from pegawai where pegawai_id=?",(idParam,))
        rows = cur.fetchone()
        password = rows[0]
        con.close()
        return password

    def getAdminPassword(self):
        con = sqlite3.connect(database = "parking.db")
        cur = con.cursor()
        cur.execute("Select password from pegawai where pegawai_id=0")
        rows = cur.fetchone()
        password = rows[0]
        con.close()
        return password

    def getIdByName(self, namaParam):
        con = sqlite3.connect(database = "parking.db")
        cur = con.cursor()
        cur.execute("Select pegawai_id from pegawai where nama_pegawai=?",(namaParam,))
        rows = cur.fetchone()
        id = rows[0]
        con.close()
        return id

    def getHighestIdParking(self):
        con = sqlite3.connect(database = "parking.db")
        cur = con.cursor()
        cur.execute("Select parking_id from parking order by parking_id desc")
        rows = cur.fetchone()
        id = rows[0]
        con.close()
        return id


    def getKalkulasiBiaya(self, idParam, keluar):
        con = sqlite3.connect(database = "parking.db")
        cur = con.cursor()
        cur.execute("Select waktu from parking where parking_id=?",(idParam,))
        rows = cur.fetchone()
        masuk = rows[0]    
        # print(masuk)
        start_time = datetime.strptime(masuk, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(keluar, '%Y-%m-%d %H:%M:%S')

        time_difference = end_time - start_time

        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        print(f'Selisih waktu: {days} hari, {hours} jam, {minutes} menit, {seconds} detik')

        satujam = 2000
        perjam = 1000
        perhari = 25000
        if days > 0:
            biaya = perhari * days
        elif hours > 1:
            biaya = satujam + (perjam * (hours - 1))
        else:
            biaya = perjam
        
        return biaya
