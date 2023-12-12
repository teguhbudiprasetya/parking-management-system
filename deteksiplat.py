import easyocr

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