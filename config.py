import tkinter as tk
from tkinter import ttk
import sqlite3

def getParkirTerisi():
    con = sqlite3.connect(database = "parking-system/parking.db")
    cur = con.cursor()
    cur.execute("Select * from parking where biaya = 0")
    rows = cur.fetchall()
    con.close()
    return len(rows)

def getPegawai():
    con = sqlite3.connect(database = "parking-system/parking.db")
    cur = con.cursor()
    cur.execute("Select * from pegawai")
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