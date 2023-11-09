import tkinter as tk
from tkinter import ttk, filedialog
import sqlite3
import easyocr
from datetime import datetime

def getParkirTerisi():
    con = sqlite3.connect(database = "parking-system/parking.db")
    cur = con.cursor()
    cur.execute("Select * from parking where biaya = 0")
    rows = cur.fetchall()
    con.close()
    return len(rows)
def getParkirKeluar():
    con = sqlite3.connect(database = "parking-system/parking.db")
    cur = con.cursor()
    now = datetime.now().strftime('%Y-%m-%d')
    cur.execute("SELECT * FROM parking WHERE waktu_OUT LIKE '%"+now+"%'")
    rows = cur.fetchall()
    con.close()
    return len(rows)

def getPegawai():
    con = sqlite3.connect(database = "parking-system/parking.db")
    cur = con.cursor()
    cur.execute("Select * from pegawai where pegawai_id != 0")
    rows = cur.fetchall()
    # result = [row[1] for row in rows]
    con.close()
    ids, names, passwords = [], [], []
    for item in rows:
        id, name, password = item
        ids.append(id)
        names.append(name)
        passwords.append(password)
    return ids, names, passwords

def getNamaPegawai():
    _,nama,_ = getPegawai()
    return nama
def getPasswordPegawai():
    _,_,password = getPegawai()
    return password

def getPasswordByName(namaParam):
    con = sqlite3.connect(database = "parking-system/parking.db")
    cur = con.cursor()
    cur.execute("Select password from pegawai where nama_pegawai=?",(namaParam,))
    rows = cur.fetchone()
    password = rows[0]
    con.close()
    return password

def getIdByName(namaParam):
    con = sqlite3.connect(database = "parking-system/parking.db")
    cur = con.cursor()
    cur.execute("Select pegawai_id from pegawai where nama_pegawai=?",(namaParam,))
    rows = cur.fetchone()
    id = rows[0]
    con.close()
    return id

def getHighestIdParking():
    con = sqlite3.connect(database = "parking-system/parking.db")
    cur = con.cursor()
    cur.execute("Select parking_id from parking order by parking_id desc")
    rows = cur.fetchone()
    id = rows[0]
    con.close()
    return id

def deteksi_plat(img):
    # Buat objek EasyOCR
    reader = easyocr.Reader(['en'])  # Menggunakan bahasa Inggris (ganti 'en' dengan kode bahasa yang sesuai)

    # Baca teks dari gambar
    results = reader.readtext(img, detail=0)

    # Tampilkan hasil teks yang dikenali

    result_list = [char for item in results for char in item.replace(" ", "")]

    # print(result_list)
    plat = []
    for i in range(len(result_list)):
        if i < 2: #PLAT 1/2 HURUF AWAL
            plat.append(result_list[i])
        else: 
            if result_list[i] in [str(n) for n in range(10)]: #PLAT ANGKA
                plat.append(result_list[i])
            else:
                plat.append(result_list[i])
                if result_list[i+1] in [str(n) for n in range(10)]: #PLAT HURUF AKHIR, JIKA HURUF BERIKUTNYA ANGKA MAKA STOP
                    break

    result_string = ''.join(plat)

    return result_string

def getKalkulasiBiaya(idParam, keluar):
    con = sqlite3.connect(database = "parking-system/parking.db")
    cur = con.cursor()
    cur.execute("Select waktu from parking where parking_id=?",(idParam,))
    rows = cur.fetchone()
    masuk = rows[0]    
    print(masuk)
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

# now = datetime.now()
# keluar = now.strftime('%Y-%m-%d %H:%M:%S')
# biaya = getKalkulasiBiaya(14, keluar)
# print(biaya)