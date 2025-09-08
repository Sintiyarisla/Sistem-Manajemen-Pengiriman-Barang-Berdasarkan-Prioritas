from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
import tkinter as tk
from tkinter import Entry, Button
from PIL import Image, ImageTk
import csv
from collections import deque
from tkinter import ttk, filedialog, Tk
import datetime
import customtkinter

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

class PackageSorter:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = []

    def read_csv(self):
        try:
            with open(self.file_name, 'r') as file:
                reader = csv.reader(file)
                self.data = list(reader)
        except FileNotFoundError:
            print("File not found:", self.file_name)
        except Exception as e:
            print("Error occurred while reading the file:", str(e))

    def shell_sort(self):
        n = len(self.data)
        gap = n // 2

        while gap > 0:
            for i in range(gap, n):
                temp = self.data[i]
                j = i
                while j >= gap and self.compare_priority(self.data[j - gap], temp):
                    self.data[j] = self.data[j - gap]
                    j -= gap
                self.data[j] = temp
            gap //= 2

    @staticmethod
    def compare_priority(p1, p2):
        priority_order = {"Prioritas": 1, "Reguler": 2, "Retur": 3}
        type1 = p1[5]
        type2 = p2[5]
        
        # Compare based on priority first
        if priority_order[type1] != priority_order[type2]:
            return priority_order[type1] > priority_order[type2]
        
        # If both have the same priority, compare by type
        if p1[4] == p2[4]:
            # Convert receipt numbers to integers for proper comparison
            resi1 = int(p1[3])
            resi2 = int(p2[3])
            return resi1 > resi2
        
        # Compare by type
        return p1[4] > p2[4]

    def sort_and_write(self):
        self.read_csv()
        if not self.data:
            print("No data to sort.")
            return
        header = self.data[0]
        self.data = self.data[1:]
        self.shell_sort()
        self.data = [header] + self.data
        return self.data




class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self, tujuan= None):
        self.head = None
        self.filename = ""
        self.tujuan= tujuan


    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def __contains__(self, value):
        current = self.head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False
    
    def generate_nomor_resi(self, filename):
        last_number = 0
        data = LinkedList()

        # Membaca file CSV dan mencari angka terakhir yang belum di-generate
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Mengabaikan baris header
            for row in reader:
                number = int(row[4][2:])  # Mengambil angka dari nomor resi
                data.append(number)
                if number > last_number:
                    last_number = number

        # Meng-generate nomor resi baru
        new_number = last_number + 1
        while new_number in data:
            new_number += 1
        if self.tujuan.lower()=='jakarta':
            nomor_resi = 'jp{:04d}'.format(new_number)  # Format nomor resi dengan 4 digit angka
        elif self.tujuan.lower()=='surabaya':
            nomor_resi= 'sp{:04d}'.format(new_number)

        return nomor_resi

 #------------------------------------------------------------------------------------------------------------------------------------------------     

class PackageSearch:
    def __init__(self, file_path):
        self.data = self.read_csv(file_path)

    def read_csv(self, file_path):
        data = {}
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Lewati header
            for row in reader:
                if len(row) >= 7:
                    nomor_paket = row[4]
                    data[nomor_paket] = row
        return data

    def bfs_search(self, search_term):
        queue = deque()
        visited = set()

        for nomor_paket, row in self.data.items():
            # print('Ini contoh',nomor_paket,row)
            if search_term in nomor_paket:
                queue.append(row)
                visited.add(nomor_paket)
                break

        while queue:
            row = queue.popleft()
            nomor_paket = row[4]

            if nomor_paket == search_term:
                return row

            for neighbor in self.get_neighbors(nomor_paket):
                if neighbor not in visited:
                    queue.append(self.data[neighbor])
                    visited.add(neighbor)

        return None

    def get_neighbors(self, nomor_paket):
        neighbors = []
        for row in self.data.values():
            if row[4] != nomor_paket:
                neighbors.append(row[4])
        return neighbors

class Barang:
    def __init__(self, jenis, berat, retur=False):
        self.jenis = jenis
        self.berat = berat
        self.retur = retur
        self.harga_prioritas_per_kg = 26000
        self.harga_reguler_per_kg = 17000

    def hitung_harga(self):
        if self.retur:
            return 0

        if self.jenis.lower() == 'prioritas':
            return self.harga_prioritas_per_kg * self.berat
        elif self.jenis.lower() == 'reguler':
            return self.harga_reguler_per_kg * self.berat
        else:
            return "Jenis barang tidak valid. Pilih antara 'prioritas' atau 'reguler'."


class InformasiBarangApp(tk.Tk):
    def __init__(self, file_path):
        super().__init__()
        self.configure()
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{width}x{height}")
        self.title('Informasi Barang')
        self.search_text = tk.StringVar()
        self.resi_label = None
        self.penerima_label = None
        self.pengirim_label = None
        self.dari_label = None
        self.tujuan_label = None
        self.jenis_paket_label = None
        self.data = []  # Initialize data attribute
        # self.linked_list = LinkedList()
        self.package_search = PackageSearch(file_path)
        
        self.Tracking()


 #------------------------------------------------------------------------------------------------------------------------------------------------       
    def Tracking(self):
        self.img_lacak_barang = Image.open('images/1.png')
        self.img_hal = self.img_lacak_barang.resize((1280,800))
        self.photo_lacak_barang = ImageTk.PhotoImage(self.img_hal)
        
        self.titik_img = Image.open("images/titik.png")
        self.titik_img = self.titik_img.resize((75, 75))
        self.photo_titik = ImageTk.PhotoImage(self.titik_img)
        
        self.label_lacak_barang = tk.Label(self, image=self.photo_lacak_barang, bg='white', bd=0)
        self.label_lacak_barang.place(x=0, y=0)
        
        self.resi = Entry(self, width=25, fg='black', border=0, bg='#D79F38', font=('Poppins',16))
        self.resi.place(x=300, y=460)
        self.resi.insert(0,'Masukkan No. Resi')
        self.resi.bind('<FocusIn>', self.on_enter)
        self.resi.bind('<FocusOut>', self.on_leave)
        
        self.tombol_cari = Button(self, text="Cari", command=self.search_resi, font=("Poppins", 16), bg='#D13123', border=0, activebackground='#D13123',activeforeground="white", cursor="hand2")
        self.tombol_cari.place(x=370, y=540)
        
        self.titik_login_button = Button(self, image=self.photo_titik, command=self.hamburger_menu, bd=0, bg='#FEF7E4', activebackground='#FEF7E4',cursor="hand2")
        self.titik_login_button.place(x=1170, y=50)
        
    def on_enter(self, e):
        self.resi.delete(0,'end')

    def on_leave(self, e):
        name = self.resi.get()
        if name == '':
            self.resi.insert(0,'Masukkan No. Resi')

    def search_resi(self):
        self.img_Informasi_barang = Image.open('images/2.png')
        self.img_hal = self.img_Informasi_barang.resize((1280,800))
        self.photo_Informasi_barang = ImageTk.PhotoImage(self.img_hal)
        
        self.kembali_merah_img = Image.open("images/red arrow.png")
        self.kembali_merah_img = self.kembali_merah_img.resize((60, 60))
        self.photo_kembali_merah = ImageTk.PhotoImage(self.kembali_merah_img)
        
        self.label_Informasi_barang = tk.Label(self, image=self.photo_Informasi_barang, bg='white', bd=0)
        self.label_Informasi_barang.place(x=0, y=0)
        
        self.kembali_merah_button = Button(self, image=self.photo_kembali_merah, bd=0, bg='#FFFFFF', activebackground='#FFFFFF', cursor="hand2", command=self.Tracking)
        self.kembali_merah_button.place(x=1170, y=50)

        self.resi_label = tk.Label(self, text="",font=('poppins',18),bg='#D79F38')
        self.resi_label.place(x= 280,y=335)
        
        self.pengirim_label = tk.Label(self, text="",font=('poppins',18),bg='#D79F38')
        self.pengirim_label.place(x= 280,y=374)
        
        self.penerima_label = tk.Label(self, text="",font=('poppins',18),bg='#D79F38')
        self.penerima_label.place(x= 280,y=412)
        
        self.tujuan_label = tk.Label(self, text="",font=('poppins',18),bg='#D79F38')
        self.tujuan_label.place(x= 280,y=449)
        
        self.jenis_pengiriman_label = tk.Label(self, text="",font=('poppins',18),bg='#D79F38')
        self.jenis_pengiriman_label.place(x= 280,y=485)
        
        self.PathFile = tk.Label(self, text="",font=('poppins',28,'bold'),bg='#FEF7E4')
        self.PathFile.place(x= 350,y=570)
        
        self.Cari_Label()


        # self.dari_label = tk.Label(self, text="",font=('poppins',12),bg='#D79F38')
        # self.dari_label.place(x= 280,y=400)
         
        
        # self.berat_label = tk.Label(self, text="",font=('poppins',12),bg='#D79F38')
        # self.berat_label.place(x= 280,y=475)
#------------------------------------------------------------------------------------------------------------------------------------------------
    def Cari_Label(self):
        search_term = self.resi.get()
        result = None
        file_path = None

        # Search the CSV files and find the result
        file_paths = ["database\\Jakarta\\package_in.csv", "database\\Jakarta\\package_out.csv",
                    "database\\Surabaya\\package_in.csv", "database\\Surabaya\\package_out.csv"]
        for file in file_paths:
            package_search = PackageSearch(file)
            result = package_search.bfs_search(search_term)
            if result:
                file_path = file
                break

        if result:
            nama_kota = file_path.split("\\")[1]
            nama_pengirim, nama_penerima, alamat_pengirim, alamat_penerima, nomor_paket, jenis_pengiriman, berat_barang, Tanggal, Cabang_Tujuan = result
            self.pengirim_label.config(text=f"{nama_pengirim}")
            self.penerima_label.config(text=f"{nama_penerima}")
            self.tujuan_label.config(text=f"{alamat_penerima}")
            self.resi_label.config(text=f"{nomor_paket}")
            self.jenis_pengiriman_label.config(text=f"{jenis_pengiriman}")
            # self.dari_label.config(text=f"{alamat_pengirim}")
            # self.berat_label.config(text=f"{berat_barang}")
            self.PathFile.config(text=f"{nama_kota}")
        else:
            showerror("Error", "Tidak ditemukan data")
 #-----------------------------------------------------------------------------------------------------------------------------------------------------

    def hamburger_menu(self):
        self.img_3 = Image.open('images/3.png')
        self.img_hal = self.img_3.resize((1280,800))
        self.photo_3 = ImageTk.PhotoImage(self.img_hal)
        
        self.kembali_hitam_img = Image.open("images/back.png")
        self.kembali_hitam_img = self.kembali_hitam_img.resize((50, 50))
        self.photo_kembali_hitam = ImageTk.PhotoImage(self.kembali_hitam_img)
        
        self.label_3 = tk.Label(self, image=self.photo_3, bg='white', bd=0)
        self.label_3.place(x=0, y=0)
        
        self.user = tk.Label(self, width=25, fg='black', border=0, bg='#D79F38', font=('Poppins',16), text='Masukkan No. Resi')
        self.user.place(x=241, y=460)
        # self.user.insert(0,'Masukkan No. Resi')
        # self.user.bind('<FocusIn>', self.on_enter)
        # self.user.bind('<FocusOut>', self.on_leave)
        
        self.tombol_cari = Button(self, text="Cari", command=self.tombol_cari, font=("Poppins", 16), bg='#D13123', border=0, activebackground='#D13123', cursor="hand2")
        self.tombol_cari.place(x=370, y=540)
        
        self.kembali_hitam_button = Button(self, image=self.photo_kembali_hitam, bd=0, bg='#D79F38', activebackground='#D79F38', cursor="hand2", command=self.Tracking)
        self.kembali_hitam_button.place(x=941, y=41)
        
        self.tombol_login = Button(self, text="Login", font=("Poppins", 18), bd=0, bg='#D79F38', activebackground='#D79F38', cursor="hand2",activeforeground="white",command=self.LogIn)
        self.tombol_login.place(x= 1060, y=160)
        
        self.tombol_about = Button(self, text="About", font=("Poppins", 18), bd=0, bg='#D79F38', activebackground='#D79F38', cursor="hand2", activeforeground="white",command=self.aboutUs)
        self.tombol_about.place(x= 1060, y=245)

#------------------------------------------------------------------------------------------------------------------------------------------------
    def aboutUs(self):
        self.img_about = Image.open('images/4.png')
        self.img_hal = self.img_about.resize((1280,800))
        self.photo_about = ImageTk.PhotoImage(self.img_hal)
        
        self.kembali_merah_4_img = Image.open("images/red arrow.png")
        self.kembali_merah_4_img = self.kembali_merah_4_img.resize((60, 60))
        self.photo_kembali_merah_4 = ImageTk.PhotoImage(self.kembali_merah_4_img)
        
        self.label_about = tk.Label(self, image=self.photo_about, bg='white', bd=0)
        self.label_about.place(x=0, y=0)
        
        self.kembali_merah_button = Button(self, image=self.photo_kembali_merah_4, command=self.Tracking, bd=0, bg='#FEF7E4', activebackground='#FEF7E4',cursor="hand2")
        self.kembali_merah_button.place(x=1170, y=50)


#------------------------------------------------------------------------------------------------------------------------------------------------
    def LogIn(self):
        self.img_login = Image.open('images/5.png')
        self.img_hal = self.img_login.resize((1280,800))
        self.photo_login = ImageTk.PhotoImage(self.img_hal)
        self.hide_image = ImageTk.PhotoImage(file='images\\show.png')
        self.show_image = ImageTk.PhotoImage(file='images\\hide.png')
        
        self.titik_img = Image.open("images/red arrow.png")
        self.titik_img = self.titik_img.resize((60, 60))
        self.photo_titik = ImageTk.PhotoImage(self.titik_img)
        
        self.label_login = tk.Label(self, image=self.photo_login, bg='white', bd=0)
        self.label_login.place(x=0, y=0)
        
        self.user = Entry(self, width=22, fg='black', border=0, bg='#D13123', font=('Poppins',16))
        self.user.place(x=755, y=275)
        self.user.insert(0,'Masukkan Username')
        self.user.bind('<FocusIn>', self.on_enterUser)
        self.user.bind('<FocusOut>', self.on_leaveUser)
        
        self.password = Entry(self, width=22, fg='black', border=0, bg='#D13123', font=('Poppins',16))
        self.password.place(x=700, y=350)
        self.password.insert(0,'Masukkan password')
        self.password.bind('<FocusIn>', self.on_enterPassword)
        self.password.bind('<FocusOut>', self.on_leavePassword)
        
        self.tombol_login = Button(self, text="Login", command=self.userName, font=("Poppins", 16), bg='#D13123', border=0, activebackground='#D13123', cursor="hand2")
        self.tombol_login.place(x=825, y=430)
        
        self.titik_login_button = Button(self, image=self.photo_titik, command=self.Tracking, bd=0, bg='#FFFFFF', activebackground='#FFFFFF',cursor="hand2")
        self.titik_login_button.place(x=1170, y=50)

        self.show_button = Button(self, image=self.show_image, command=self.show, relief=FLAT,activebackground="#D13123", borderwidth=0, background="#D13123", cursor="hand2")
        self.show_button.place(x=930, y=355)

    def show(self):
        self.hide_button = Button(self, image=self.show_image, command=self.hide, relief=FLAT,activebackground="#D13123", borderwidth=0, background="#D13123", cursor="hand2")
        self.hide_button.place(x=930, y=355)
        self.password.config(show='*')
 
    def hide(self):
        self.show_button1 = Button(self, image=self.hide_image, command=self.show, relief=FLAT,
                                  activebackground="#D13123"
                                  , borderwidth=0, background="#D13123", cursor="hand2")
        self.show_button1.place(x=930, y=355)
        self.password.config(show='') 

    def on_enterUser(self, e):
        widget = e.widget
        widget.delete(0, 'end')
    
    def on_leaveUser(self, e):
        widget = e.widget
        if widget.get() == '':
            widget.insert(0, 'Masukkan email')

    def on_enterPassword(self, e):
        if self.password.get() == 'Masukkan password':
            self.password.delete(0, 'end')
            self.password.config(show='*')
    
    def on_leavePassword(self, e):
        if self.password.get() == '':
            self.password.insert(0, 'Masukkan password')
            self.password.config(show='')


    def userName(self):
        with open('database/User_Auth.csv', mode='r') as file:
            reader = csv.reader(file,delimiter=",")
            if self.user.get() == 0 or self.user.get() == 'Username':
                showerror('Error','Username belum diisi')
            else:
                for i in reader:
                    if i == [self.user.get(), self.password.get()]:
                        showinfo(title="Login Success", message="You Successfully Login")
                        self.Main_Menu()
                        return
                showinfo(title="Error", message="Invalid Password")

#------------------------------------------------------------------------------------------------------------------------------------------------

    def Main_Menu(self):
        self.img_cabang = Image.open('images/6.png')
        self.img_hal = self.img_cabang.resize((1280,800))
        self.photo_cabang = ImageTk.PhotoImage(self.img_hal)
        
        self.kembali_merah_img = Image.open("images/red arrow.png")
        self.kembali_merah_img = self.kembali_merah_img.resize((60, 60))
        self.photo_kembali_merah = ImageTk.PhotoImage(self.kembali_merah_img)
        
        self.label_cabang = tk.Label(self, image=self.photo_cabang, bg='white', bd=0)
        self.label_cabang.place(x=0, y=0)
        
        self.kembali_merah_button = Button(self, image=self.photo_kembali_merah, command=self.kembali_merah, bd=0, bg='#FEF7E4', activebackground='#FEF7E4', cursor="hand2")
        self.kembali_merah_button.place(x=1170, y=50)
        
        self.tombol_pengiriman = Button(self, text="Click", command=self.pengiriman, font=("Poppins", 17, 'bold'), bg='#D13123', border=0, activebackground='#D13123', cursor="hand2")
        self.tombol_pengiriman.place(x=239, y=670)
        
        self.tombol_pemantauan = Button(self, text="Click", command=self.tombol_click_pemantauan, font=("Poppins", 17, 'bold'), bg='#D13123', border=0, activebackground='#D13123', cursor="hand2")
        self.tombol_pemantauan.place(x=660, y=670)

        self.label_waktu = tk.Label(self, font=('calibri', 82, 'bold'), background='#D79F38', foreground='#3B435F')
        self.label_waktu.place(x=950, y=620)  

        self.cabang_text = tk.Label(self, font= ("Poppins", 27 ,'bold'), text="Cabang {}".format(self.user.get()), bg='#FEF7E4', fg='#3B435F')
        self.cabang_text.place(x=50, y=48)
        
        self.waktu()
        
    def waktu(self):
        self.sekarang = datetime.datetime.now()
        string_waktu = self.sekarang.strftime('%H:%M')
        self.label_waktu.config(text=string_waktu)
        self.label_waktu.after(1000, self.waktu) 
        
    def kembali_merah(self):  
        sure = askyesno("Logout", "Are you sure you want to logout?")
        if sure == True:
            self.Tracking()

#------------------------------------------------------------------------------------------------------------------------------------------------

    def pengiriman(self):
        self.img_pendataan_barang = Image.open('images/7.png')
        self.img_hal = self.img_pendataan_barang.resize((1280,800))
        self.photo_pendataan_barang = ImageTk.PhotoImage(self.img_hal)
        
        self.kembali_merah_7_img = Image.open("images/red arrow.png")
        self.kembali_merah_7_img = self.kembali_merah_7_img.resize((60, 60))
        self.photo_kembali_merah_7 = ImageTk.PhotoImage(self.kembali_merah_7_img)
        
        self.label_pendataan_barang = tk.Label(self, image=self.photo_pendataan_barang, bg='white', bd=0)
        self.label_pendataan_barang.place(x=0, y=0)
        
        self.kembali_merah_7_button = Button(self, image=self.photo_kembali_merah_7, command=self.Main_Menu, bd=0, bg='#FEF7E4', activebackground='#FEF7E4', cursor='hand2')
        self.kembali_merah_7_button.place(x=1170, y=50)
        
        self.tombol_proses_7 = Button(self, text="Proses", command=self.Proses_barang, font=("Poppins", 18), bg='#D13123', border=0, activebackground='#D13123',cursor='hand2')
        self.tombol_proses_7.place(x=845, y=618)
        
        cabang_tujuan = ["Jakarta", "Surabaya"]
        jenis_pengiriman = ["Reguler", "Prioritas", "Retur"]
        
        self.input_pengirim = Entry(self, width=26, fg='black', border=0, bg='#CD8746', font=('Poppins',16))
        self.input_pengirim.place(x=140,y=226)

        self.input_penerima = Entry(self, width=26, fg='black', border=0, bg='#CD8746', font=('Poppins',16))
        self.input_penerima.place(x=140,y=321)

        self.input_alamat_pengirim = Entry(self, width=26, fg='black', border=0, bg='#CD8746', font=('Poppins',16))
        self.input_alamat_pengirim.place(x=140,y=423)

        self.input_alamat_tujuan = Entry(self, width=26, fg='black', border=0, bg='#CD8746', font=('Poppins',16))
        self.input_alamat_tujuan.place(x=140,y=525)

        self.input_berat = Entry(self, width=10, fg='black', border=0, bg='#CD8746', font=('Poppins',18))
        self.input_berat.place(x=610,y=421)

        self.style= customtkinter.CTkComboBox
        self.input_cabangTujuan = customtkinter.CTkComboBox(self, values=cabang_tujuan, height= 38,width= 200, bg_color='#FCE8BC',fg_color='#CD8746',font=('Poppins', 20),dropdown_font=('Poppins', 17),corner_radius=50,border_color= '#CD8746',button_color='#AC2B22',
                                                            dropdown_hover_color='#FEF7E4',dropdown_fg_color='#CD8746',dropdown_text_color='black',text_color='black')
        self.input_cabangTujuan.place(x=130,y=630)

        self.input_jenisPengiriman = customtkinter.CTkComboBox(self, values=jenis_pengiriman, height= 38,width= 200, bg_color='#FCE8BC',fg_color='#CD8746',font=('Poppins', 20),dropdown_font=('Poppins', 17),corner_radius=50,border_color= '#CD8746',button_color='#AC2B22',
                                                            dropdown_hover_color='#FEF7E4',dropdown_fg_color='#CD8746',dropdown_text_color='black',text_color='black')
        self.input_jenisPengiriman.place(x=600,y=318)

        
    def Proses_barang(self):
        self.filename = f"database/{self.user.get()}/package_out.csv"
        
        tujuan= self.user.get()
        self.linked_list= LinkedList(tujuan)
        
        # self.linked_list = LinkedList()
        # kode= LinkedList(tujuan)
        self.nomor_resi = self.linked_list.generate_nomor_resi(self.filename)
        self.sekarang = datetime.datetime.now()
        self.tanggal = self.sekarang.strftime("%d/%m/%Y %H:%M:%S")

        jenis_pengiriman = self.input_jenisPengiriman.get()
        berat = float(self.input_berat.get())
        retur = jenis_pengiriman.lower() == 'retur'
        
        barang = Barang(jenis_pengiriman, berat, retur)
        self.harga = barang.hitung_harga()

        if isinstance(self.harga, str):
            showinfo("Error", self.harga)
            return

        with open(self.filename, 'a+', newline='') as f:
            data_baru = [self.input_pengirim.get(), self.input_penerima.get(), self.input_alamat_pengirim.get(), self.input_alamat_tujuan.get(), self.nomor_resi, self.input_jenisPengiriman.get(), self.input_berat.get(),self.tanggal,self.input_cabangTujuan.get()]
            write = csv.writer(f, data_baru)
            write.writerow(data_baru)
            showinfo("success", "Data sudah berhasil diinput")
            showinfo("Info",f"nomor resi anda adalah : {self.nomor_resi}")
            showinfo("Info", f"Harga barang Anda adalah: Rp.{self.harga}")       

#------------------------------------------------------------------------------------------------------------------------------------------------
    def tombol_click_pemantauan(self):
        self.img_Pemantauan = Image.open('images/8.png')
        self.img_hal = self.img_Pemantauan.resize((1280,800))
        self.photo_Pemantauan = ImageTk.PhotoImage(self.img_hal)

        self.kembali_merah_8 = Image.open('images/red arrow.png')
        self.kembali_merah_8 = self.kembali_merah_8.resize((60, 60))
        self.photo_kembali_merah_8 = ImageTk.PhotoImage(self.kembali_merah_8)
        
        self.label_Pemantauan = tk.Label(self, image=self.photo_Pemantauan, bg='white', bd=0)
        self.label_Pemantauan.place(x=0, y=0)

        self.kembali_merah_8_button = Button(self, image=self.photo_kembali_merah_8, command=self.Main_Menu, bd=0, bg='#FEF7E4', activebackground='#FEF7E4',cursor='hand2')
        self.kembali_merah_8_button.place(x=1170, y=50)
        
        self.tombol_kedatangan = Button(self, text="Click", command=self.tombol_click_kedatangan, font=("Poppins", 18), bg='#D13123', border=0, activebackground='#D13123',cursor='hand2')
        self.tombol_kedatangan.place(x=385, y=567)
        
        self.tombol_keberangkatan = Button(self, text="Click", command=self.tombol_click_keberangkatan, font=("Poppins", 18), bg='#D13123', border=0, activebackground='#D13123',cursor='hand2')
        self.tombol_keberangkatan.place(x=835, y=567)
#-------------------------------------------------------------------------------------------------------------------------
    def tombol_click_keberangkatan(self):
        self.img = PhotoImage(file="images/11.png")
            
        self.img_label = Label(self, image=self.img,bg='white', bd=0)
        self.img_label.place(x=0, y=0)

        self.load_treeview_img= Image.open('images/refresh.png')
        self.load_treeview_img= self.load_treeview_img.resize((35,35))
        self.photo_load_treeview= ImageTk.PhotoImage(self.load_treeview_img)

        self.sort_treeview_img= Image.open('images/sort.png')
        self.sort_treeview_img= self.sort_treeview_img.resize((40,40))
        self.photo_sort_treeview= ImageTk.PhotoImage(self.sort_treeview_img)

        self.style= ttk.Style()
        self.style.theme_use('default')

        self.style.configure('Treeview',
            background='#CD8746',
            foreground='white',
            rowheight=25,
            fieldbackground='#CD8746',
            font=('calibri', 9)
            )
        self.style.configure('Treeview.Heading',
            background='#C24914',
            foreground='white',
            rowheight=25,
            font=('calibri', 9)
            )
        
        self.style.map('Treeview',
                background=[('selected','#F7D08A')],
                foreground=[('selected','#000000')])
        
        self.tree = ttk.Treeview(self)
        self.open_button1 = Button(self,image=self.photo_load_treeview, command=self.openFile_keberangkatan, bg='#FEF7E4', bd=0, activebackground='#FEF7E4',cursor='hand2')
        self.move_button = Button(self, text="Kirim", command=self.move_selected_row,font=("Poppins", 16, 'bold'), bg='#D13123', border=0, activebackground='#D13123',cursor='hand2')
        self.kembali_merah_9_button = Button(self, image=self.photo_kembali_merah_8, command=self.tombol_click_pemantauan, bd=0, bg='#FEF7E4', activebackground='#FEF7E4',cursor='hand2')
        self.Sort_button = Button(self,image=self.photo_sort_treeview,command=self.sorting2, bg='#FEF7E4', bd=0, activebackground='#FEF7E4',cursor='hand2')
            
        self.tree.place(x=310, y=92, width=866, height=537)
        self.open_button1.place(x=136, y=118)
        self.move_button.place(x=160, y=172)
        self.kembali_merah_9_button.place(x=1195, y=30)
        self.Sort_button.place(x=196, y=116)

        self.cabang_text1 = tk.Label(self, font= ("Poppins", 30 ,'bold'), text="Cabang {}".format(self.user.get()), bg='#FEF7E4', fg='#3B435F')
        self.cabang_text1.place(x=50, y=15)

    def clear_treeview(self):
        self.tree.delete(*self.tree.get_children()) 

    def openFile_keberangkatan(self):
        self.current_file_path2 = f'database/{self.user.get()}/package_out.csv'
        if self.current_file_path2:
            with open(self.current_file_path2, 'r') as file:
                csvreader = csv.reader(file)
                headers = next(csvreader)

                self.clear_treeview()

                self.tree["columns"] = headers
                self.tree["show"] = "headings"

                for col in headers:
                    self.tree.heading(col, text=col)

                for row in csvreader:
                    self.tree.insert("", "end", values=row)

    def move_selected_row(self):
        move = askyesno('Move', 'Apakah Anda ingin memindah data ini?')
        if move == True:
            selected_item = self.tree.selection()
            if not selected_item:
                showwarning("No selection", "Please select a row to move.")
                return

            row_values = self.tree.item(selected_item, "values")

            last_column_value = self.cabang_tujuan(row_values)
            target_file_path = f'database/{last_column_value}/package_in.csv'

        with open(target_file_path, 'a', newline='') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(row_values)

        self.tree.delete(selected_item)
        self.remove_row_from_csv(self.current_file_path2, row_values)

    def cabang_tujuan(self, row_values):
        if row_values:
            return row_values[-1]  
        return None

    def remove_row_from_csv(self, file_path, row_values):
        file_path = f'database/{self.user.get()}/Package_out.csv'
        with open(file_path, 'r') as file:
            rows = list(csv.reader(file))

        with open(file_path, 'w', newline='') as file:
            csvwriter = csv.writer(file)
            for row in rows:
                if row != list(row_values):
                    csvwriter.writerow(row)

    def sorting2(self):
        file_name = f'database/{self.user.get()}/package_out.csv'
        package_sorter = PackageSorter(file_name)
        sorted_data = package_sorter.sort_and_write()

        if sorted_data:
            self.data = sorted_data[1:]  # Exclude the header

            # Clear existing data in treeview
            self.clear_treeview()

            # Populate treeview with sorted data
            for row in self.data:
                self.tree.insert("", "end", values=row)
#------------------------------------------------------------------------------------------------------------------------------------------------------

    def tombol_click_kedatangan(self):
        self.img = PhotoImage(file="images/11.png")
            
        self.img_label = Label(self, image=self.img,bg='white', bd=0)
        self.img_label.place(x=0, y=0)

        self.load_treeview_img= Image.open('images/refresh.png')
        self.load_treeview_img= self.load_treeview_img.resize((35,35))
        self.photo_load_treeview= ImageTk.PhotoImage(self.load_treeview_img)

        self.sort_treeview_img= Image.open('images/sort.png')
        self.sort_treeview_img= self.sort_treeview_img.resize((40,40))
        self.photo_sort_treeview= ImageTk.PhotoImage(self.sort_treeview_img)

        self.style= ttk.Style()
        self.style.theme_use('default')

        self.style.configure('Treeview',
            background='#CD8746',
            foreground='white',
            rowheight=25,
            fieldbackground='#CD8746',
            font=('calibri', 9)
            )
        self.style.configure('Treeview.Heading',
            background='#C24914',
            foreground='white',
            rowheight=25,
            font=('calibri', 9)
            )
        
        self.style.map('Treeview',
                background=[('selected','#F7D08A')],
                foreground=[('selected','#000000')])
        
        self.tree = ttk.Treeview(self)
        self.open_button1 = Button(self,image=self.photo_load_treeview, command=self.openFile_kedatangan, bg='#FEF7E4', bd=0, activebackground='#FEF7E4',cursor='hand2')
        self.move_button = Button(self, text="Proses", command=self.move_selected_row1,font=("Poppins", 16, 'bold'), bg='#D13123', border=0, activebackground='#D13123',cursor='hand2')
        self.kembali_merah_9_button = Button(self, image=self.photo_kembali_merah_8, command=self.tombol_click_pemantauan, bd=0, bg='#FEF7E4', activebackground='#FEF7E4',cursor='hand2')
        self.Sort_button = Button(self,image=self.photo_sort_treeview,command=self.sorting1, bg='#FEF7E4', bd=0, activebackground='#FEF7E4',cursor='hand2')
            
        self.tree.place(x=310, y=92, width=866, height=537)
        self.open_button1.place(x=136, y=118)
        self.move_button.place(x=155, y=172)
        self.kembali_merah_9_button.place(x=1195, y=30)
        self.Sort_button.place(x=196, y=116)

        self.cabang_text1 = tk.Label(self, font= ("Poppins", 30 ,'bold'), text="Cabang {}".format(self.user.get()), bg='#FEF7E4', fg='#3B435F')
        self.cabang_text1.place(x=50, y=15)

    def clear_treeview1(self):
        self.tree.delete(*self.tree.get_children())  # Clear treeview

    def openFile_kedatangan(self):
        self.current_file_path3 = f'database/{self.user.get()}/package_in.csv'
        if self.current_file_path3:
            with open(self.current_file_path3, 'r') as file:
                csvreader = csv.reader(file)
                headers = next(csvreader)

                self.clear_treeview1()

                self.tree["columns"] = headers
                self.tree["show"] = "headings"

                for col in headers:
                    self.tree.heading(col, text=col)

                for row in csvreader:
                    self.tree.insert("", "end", values=row)

    def move_selected_row1(self):
        move = askyesno('Move', 'Apakah pelanggan meminta retur?')
        selected_item = self.tree.selection()
        if not selected_item:
            showwarning("No selection", "Please select a row to move.")
            return

        row_values = self.tree.item(selected_item, "values")

        if move:
            showinfo("retur", "Silahkan masukkan kembali data barang di pengiriman.")

        self.tree.delete(selected_item)
        self.remove_row_from_csv1(self.current_file_path3, row_values)

        if not move:
            showinfo("Shipment Complete", "Pengiriman paket untuk barang ini telah selesai.")

    def remove_row_from_csv1(self, file_path, row_values):
        file_path = f'database/{self.user.get()}/Package_in.csv'
        with open(file_path, 'r') as file:
            rows = list(csv.reader(file))

        with open(file_path, 'w', newline='') as file:
            csvwriter = csv.writer(file)
            for row in rows:
                if row != list(row_values):
                    csvwriter.writerow(row)

    def sorting1(self):
        file_name = f'database/{self.user.get()}/package_in.csv'
        package_sorter = PackageSorter(file_name)
        sorted_data = package_sorter.sort_and_write()

        if sorted_data:
            self.data = sorted_data[1:]  # Exclude the header

            # Clear existing data in treeview
            self.clear_treeview1()

            # Populate treeview with sorted data
            for row in self.data:
                self.tree.insert("", "end", values=row)

#------------------------------------------------------------------------------------------------------------------------------------------------



file_path = "database/Jakarta/package_in.csv"

if __name__ == "__main__":
    app = InformasiBarangApp(file_path)
    app.mainloop()
