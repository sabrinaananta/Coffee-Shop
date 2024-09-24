import mysql.connector # mengimport mysql.connector agar masuk ke database
import re #mengimport re agar dapat menggunakan regular expression


def connect_to_database():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="coffee"
    )

# Function to create a new coffee in the database
def create_coffee(nama, harga, cursor, conn):
    try:
        # Validation and SQL query execution
        if not nama or not harga:
            raise ValueError("Coffee name and price are required.")

        cursor.execute(
            """
            INSERT INTO coffees (nama, harga)
            VALUES (%s, %s)
            """,
            (nama, harga)
        )

        conn.commit()
        print(f"Coffee {nama} with price Rp.{harga} added to the database.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def read_coffees(cursor):
    try:
        cursor.execute("SELECT * FROM coffees")
        coffees = cursor.fetchall()

        print("====================================================")
        print("|                   DAFTAR MENU                    |")
        print("====================================================")

        for coffee in coffees:
            print(f"|ID: {coffee[0]}, | Nama: {coffee[1]}, | Harga: Rp.{coffee[2]} |")

        print("====================================================")

    except mysql.connector.Error as err:
        print(f"Error: {err}")


def update_coffee(coffee_id, new_nama, new_harga, cursor, conn):
    #mengeksekusikan pernyatan sql untuk memperbaharui data coffee berdasarkan IDnya
    cursor.execute(
        """
        UPDATE coffees SET nama = %s, harga = %s WHERE id = %s
    """,
        (new_nama, new_harga, coffee_id),
    )
    #commit perubahannya ke database
    conn.commit()
    
def update_coffee_menu(cursor, conn):
    print("==============================")
    print("|      UPDATE COFFEE MENU     |")
    print("==============================")

    # untuk menampilkan menu coffee
    read_coffees(cursor)

    # meminta admin memilih id coffee yang akan di update
    coffee_id = int(input("Enter the ID of the coffee to update: "))
    
    # meminta input nama dan harga baru 
    new_nama = input("Enter new name: ")
    new_harga = int(input("Enter new price: "))

    # meminta fungsi update coffee agar bisa mengupdate yang baru
    update_coffee(coffee_id, new_nama, new_harga, cursor, conn)

    print("Coffee updated successfully.")



def delete_coffee(coffee_id, cursor, conn):
    #mengeksekusikan pernyataan sql untuk menghapus data coffee berdasarkan IDnya
    cursor.execute("DELETE FROM coffees WHERE id = %s", (coffee_id,))
    #commit perubahannya ke database
    conn.commit()
    
def delete_coffee_menu(cursor, conn):
    print("==============================")
    print("|      DELETE COFFEE MENU     |")
    print("==============================")

    # untuk menampilkan menu coffee
    read_coffees(cursor)

    # meminta admin untuk memilih id yang akan dihapus
    coffee_id = int(input("Enter the ID of the coffee to delete: "))

    # memanggil fungsi delete_coffee untuk menghapusnya
    delete_coffee(coffee_id, cursor, conn)

    print("Coffee deleted successfully.")



def get_menu():
    #membuka koneksi ke database menggunakan informasi koneksi yang sudah diberikan
    conn = mysql.connector.connect(
        host="localhost", user="root", password="", database="coffee"
    )
    
    #membuat object cursor untuk berinteraksi dengan databasenya
    cursor = conn.cursor()

    #mengeksekusi pernyataan sql untuk menagmbil seluruh data dari coffees
    cursor.execute("SELECT * FROM coffees")
    #mengambil hasil data semuanya dari hasil eksekusi sql
    menu = cursor.fetchall()
    #menutup koneksi ke database setelah mendapatkan datanya
    conn.close()
    #mengembalikan menu sebagai hasil fungsi
    return menu

#variabel global di luar function
keranjang = [] #inisialisasi keranjang sebagai list kosong 

def manage_cart(menu, keranjang):
    while True: #berjalan terus menerus hingga ketika memilih opsi 5 untuk keluar dari loop
        print("==============================")
        print("|          KERANJANG         |")
        print("==============================")
        print("|1. Tambah Pesanan           |")
        print("|2. Hapus Pesanan            |")
        print("|3. Update Jumlah Pesanan    |")
        print("|4. Lihat Keranjang          |")
        print("|5. Selesai                  |")
        print("==============================")

        choice = input("Pilih opsi keranjang (1-5): ")

        if choice == "1":
            add_to_cart(menu, keranjang)# memanggil fungsi untuk menambah pesanan ke keranjang
        elif choice == "2":
            remove_from_cart(keranjang) #memanggil fungsi untuk menghapus pesanan dari keranjang
        elif choice == "3":
            update_quantity(keranjang) # memanggil fungsi untuk mengupdate jumlah pesanan di keranjang
        elif choice == "4":
            view_cart(keranjang)# memanggil fungsi untuk melihat isi keranjang
        elif choice == "5":
            break #keluar dari loopnya dan mengakhiri management keranjang
        else:
            print("Opsi tidak valid. Silakan coba lagi.")


def add_to_cart(menu, keranjang):
    #menampilkan menu ke pengguna
    print("===========================================")
    print("===================MENU====================")
    for item in menu:
        print(f"|{item[0]}.| {item[1]} \t Rp.{item[2]}")
    print("===========================================")

    #meminta pengguna untuk memasukan nomor menu yang ingin dipesan
    menu_pesanan = int(input("Masukan Menu Pesanan (Nomor Menu): "))
    #mencari item menu yang sesuai dnegan nomor yang dimasukan oleh pengguna
    found_item = next((item for item in menu if item[0] == menu_pesanan), None)

    if found_item:
        #jika item ditemukan maka akan meminta pengguna untuk emmasukan jumlah pembeliannya
        jumlah_pembelian = int(input("Masukan Jumlah Pembelian: "))
        total_harga = found_item[2] * jumlah_pembelian
        #manmbahkan informasi pesanan ke keranjang
        keranjang.append(
            {
                "nama": found_item[1],
                "harga": found_item[2],
                "jumlah": jumlah_pembelian,
                "total": total_harga,
            }
        )
        print(f"{found_item[1]} ditambahkan ke dalam keranjang.")
    else:
        #jika nomor menu tidak valid maka menampilkan pesan kesalahan 
        print("===========================================")
        print("|Menu tidak valid. Silahkan pilih kembali.|")
        print("===========================================")


def remove_from_cart(keranjang):
    if keranjang:
        print("===============================================================")
        print("|                HAPUS MENU DARI KERANJANG                    |")
        print("===============================================================")
        #membuat fungsi print_details untuk mencetak detail setiap item pesananya dengan lambda
        print_details = lambda i, order: print(
            f"{i + 1}. {order['nama']} \t Jumlah: {order['jumlah']} \t Total: Rp.{order['total']}"
        )

        #menampilkan detail setiap item pesanannya kedalam keranjang
        for i, order in enumerate(keranjang):
            print_details(i, order)
        #meminta pengguna memasukan nomor menu yang ingin dihapus
        index_hapus = int(
            input("Masukkan nomor menu yang ingin dihapus dari keranjang: ")
        )
        
        #memeriksa apakah nomor yang dimasukkan valid
        if 1 <= index_hapus <= len(keranjang):
            #menghapus item dari keranjang bedasarkan nomor yang dimasukann
            del_item = keranjang.pop(index_hapus - 1)
            print(f"{del_item['nama']} dihapus dari keranjang.")
        else:
            print("Nomor menu tidak valid.")
    else:
        print("Keranjang kosong.")


def update_quantity(keranjang):
    if keranjang:
        print("======================================================================")
        print("|                  UPDATE JUMLAH PESANAN DI KERANJANG                |")
        print("======================================================================")
        #membuat fungsi print_details untuk mencetak detail item pesanannya
        print_details = lambda i, order: print(
            f"{i + 1}. {order['nama']} \t Jumlah: {order['jumlah']} \t Total: Rp.{order['total']}"
        )
        
        #menampilkan detail setiap item pesanan dalam keranjang
        for i, order in enumerate(keranjang):
            print_details(i, order)

        #meminta inputan untuk mengupdate jumlah pesanan
        index_update = int(
            input("Masukkan nomor menu yang ingin diupdate jumlahnya: ")
        )
        #memeriksa apakah nomor menu yang dimasukan valid
        if 1 <= index_update <= len(keranjang):
            order = keranjang[index_update - 1]
            new_quantity = int(input("Masukkan jumlah baru: "))
            new_total = order['harga'] * new_quantity
            #mengupdate jumlah dan total pesanna
            keranjang[index_update - 1]['jumlah'] = new_quantity
            keranjang[index_update - 1]['total'] = new_total
            print(f"Jumlah pesanan {order['nama']} diupdate menjadi {new_quantity}.")
        else:
            print("Nomor menu tidak valid.")
    else:
        print("Keranjang kosong.")
        
def view_cart(keranjang):
    if keranjang:
        #menampilkan header untuk detail pesanannya
        print("=====================================================================")
        print("|                            DETAIL PESANAN                         |")
        print("=====================================================================")
        
        #menampilkan detail pesnanannya kedalam keranjang
        for order in keranjang:
            print(
                f"{order['nama']} \t Rp.{order['harga']} \t Jumlah: {order['jumlah']} \t Total: Rp.{order['total']}"
            )

        #menghitung total pembayaran dari semua pesanan dalam keranjang
        total_payment = sum(order['total'] for order in keranjang)
        #menampilkan total pembayaran
        print("======================================================================")
        print(f"Total Pembayaran: Rp.{total_payment}")
        print("======================================================================")
    else:
        #menampilkan jika pesanna keranjang kosong
        print("Keranjang kosong.")



def user_order():
    menu = get_menu() #mendpaatkan menu dari database
    #menampilkan header untuk aplikasi pemesanan coffee
    print("==============================")
    print("|        Like A Latte        |")
    print("==============================")

    #meminta nama pelanggan dan tanggal pembeliannya
    nama_pelanggan = input("Nama Pelanggan : ")
    tanggal_pembelian = input("Tanggal Pembelian : ")

    #menampilkan menu kepada pengguna 
    print("======================================")
    print("=================MENU=================")
    for item in menu:
        print(f"|{item[0]}.| {item[1]} \t Rp.{item[2]}")
    print("======================================")
    keranjang = []  # List untuk menyimpan pesanan

    #memulai manajemen keranjang
    print("======================================")
    manage_cart(menu, keranjang)

    #mememriksa apakah ada item yang ditambahkan kekeranjang sebelum melanjutkannya
    if not keranjang:
        print("Keranjang kosong. Pembelian dibatalkan.")
        return

    # Menampilkan isi keranjang
    print("=====================================================================")
    print("|                            DETAIL PESANAN                         |")
    print("=====================================================================")
    view_cart(keranjang)

    total_payment = sum(order['total'] for order in keranjang)

    if total_payment is not None:
        #menampilkan total pembayaran
        print("=================================================================")
        print(f"Total Pembayaran: Rp.{total_payment}")
        print("=================================================================")
        # Pilihan pembayaran
        print("================================")
        print("|Pilih metode pembayaran:      |")
        print("|1. Cash                       |")
        print("|2. Transfer                   |")
        print("================================")

        #meminta pengguna memilih metode pembayaran
        payment_method = input("Pilih nomor metode pembayaran (1-2): ")

        if payment_method == "1":
            #pembayaran tunai
            cash_payment(total_payment)
            save_order_to_database(nama_pelanggan, tanggal_pembelian, total_payment, "Cash")
        elif payment_method == "2":
            #pembayaran transfer
            bank_transfer(total_payment)
            save_order_to_database(
                nama_pelanggan, tanggal_pembelian, total_payment, "Transfer"
            )
        else:
            #menampilkan pesanan jika metode pembayaran tidak valid
            print("================================")
            print("|Metode pembayaran tidak valid.|")
            print("================================")
        #menampilkan pesan terimaksih 
        print("===================================")
        print("|Terima kasih atas pembelian Anda!|")
        print("===================================")
        
    else:
        #menampilkan pesan jika total pembayaran tidak valid
        print("Error: Total pembayaran tidak valid.")
        
        


def save_order_to_database(
    nama_pelanggan, tanggal_pembelian, total_pembayaran, metode_pembayaran
):
    #menghubungkan ke database
    conn = mysql.connector.connect(
        host="localhost", user="root", password="", database="coffee"
    )
    cursor = conn.cursor()
    #menyimpan pesanan kedalam tabel orders di database
    cursor.execute(
        """
        INSERT INTO orders (nama_pelanggan, tanggal_pembelian, total_pembayaran, metode_pembayaran)
        VALUES (%s, %s, %s, %s)
    """,
        (nama_pelanggan, tanggal_pembelian, total_pembayaran, metode_pembayaran),
    )

    #melakukan commit untuk menyimpan perubahan ke database
    conn.commit()
    #menutup koneksi ke database
    conn.close()


def cash_payment(total_amount):
    #menampilkan informasi pembayaran dengan tunai
    print("Pembayaran dengan uang tunai.")
    #meminta pengguna untuk memasukan jumlah uang yang akan diberikan
    cash_given = float(input("Jumlah uang yang diberikan: "))
    #memeriksa apakah jumlah uang yang diberikan cukup
    if cash_given < total_amount:
        print("Uang yang diberikan kurang. Transaksi dibatalkan.")
    else:
        #menghitung dan menampilkan uang kembaliannya
        change = cash_given - total_amount
        print(f"Uang kembalian: Rp.{change}")


def bank_transfer(total_amount):
    #menampilkan jika transfer bank maka transfer kesini
    print("=========================================")
    print("---=Pembayaran melalui transfer bank-----")
    print(" |Silakan transfer ke rekening berikut: |")
    print(" |Nama Bank: Bank BRI                   |")
    print(" |Nomor Rekening: 0987654321            |")
    print(" |Atas Nama: Like A Latte               |")
    print(f"|Jumlah Transfer: Rp.{total_amount}    |")
    print(" |Terima kasih!                         |")
    print("=========================================")
    
def view_transactions(cursor):
    #menampilkan data transaksi dari tabel orders
    cursor.execute("SELECT * FROM orders")
    transactions = cursor.fetchall()
    #menampilkan header untuk riwayat transaksinya
    print("===============================================================================================================================================")
    print("|                                                               TRANSACTIONS HISTORY                                                          |")
    print("===============================================================================================================================================")
    #menampilkan setiap transaksi dalam format yang sudah ditentukan
    for transaction in transactions:
        print(f"|ID: {transaction[0]}, | Nama Pelanggan: {transaction[1]}, | Tanggal Pembelian: {transaction[2]}, | Total Pembayaran: Rp.{transaction[3]}, | Metode Pembayaran: {transaction[4]} |")
    #menampikan pemisah untuk mengakhirinya
    print("===============================================================================================================================================")



def main(cursor, conn):
    while True: #loop utama program
        #menampikan menu utamanya
        print("=====================================")
        print("|      WELCOME TO Like A Latte      |")
        print("=====================================")
        print("|1. Login                           |")
        print("|2. Register                        |")
        print("|3. Exit                            |")
        print("=====================================")
        
        #meminta pengguna memilih opsi
        choice = int(input("Choose option (1-3): "))
        #memproses pilihan pengguna
        if choice == 1:
            #meminta informasi login dari pengguna
            name = input("Enter Username: ")
            password = input("Enter Password: ")
            #memanggil fungsi lofin untuk mendapatkan peran role
            role = login(name, password, cursor)
            #memproses peran pengguna setelah login
            if role == "ADMIN":
                #jika peran admin maka panggil menu admin
                admin_menu(cursor, conn)
            elif role == "USER":
                #jika peran user maka panggil menu user
                user_menu(cursor)
        elif choice == 2:
            #meminta informasi registrasi dari pengguna
            name = input("Enter Username: ")
            password = input("Enter Password: ")
            role = input("Enter Role (user/admin): ")
            #memanggil fungsi register untuk mendaftarkan pengguna
            register(name, password, role, cursor, conn)
            print("Registration successful. Please log in.")
        elif choice == 3:
            #mengakhiri program jika pengguna memilih keluar
            print("Program terminated.")
            break
        else:
            #menampilkan pesan jika pilihan tidak valid
            print("Invalid option. Please try again.")

#menutup kursor dan koneksi setelah loop selesai
    cursor.close()
    conn.close()



def user_menu(cursor):
    while True:#loop utama untuk menu pengguna
        #menampilkan menu pengguna
        print("==============================")
        print("|     MENU Like A Latte      |")
        print("==============================")
        print("|1. View Menu                |")
        print("|2. Place Order              |")
        print("|3. Exit                     |")
        print("==============================")
        #meminta pengguna untuk memilih opsi
        choice = int(input("Choose option (1-3): "))
        #memproses pilihan pengguna
        if choice == 1:
            #menampilkan menu cofee saat ini
            read_coffees(cursor)
        elif choice == 2:
            #memanggil fungsi untuk melakukan pemesanan
            user_order()
        elif choice == 3:
            #keluar dari menu pengguna jika pengguna memilih keluar
            print("================================")
            print("|         Exiting  menu.       |")
            print("================================")
            break
        else:
            #menampilkan pesan jika pilihan tidak valid
            print("===================================")
            print("|Invalid option. Please try again.|")
            print("===================================")



def admin_menu(cursor, conn):
    while True:
        print("==============================")
        print("|        ADMIN MENU          |")
        print("==============================")
        print("|1. Add Coffee               |")
        print("|2. View Menu                |")
        print("|3. Update Coffee            |")
        print("|4. Delete Coffee            |")
        print("|5. Transaksi History        |")
        print("|6. Exit                     |")
        print("==============================")
        choice = input("Choose option (1-6): ")

        if choice == "1":
            # Meminta input dari admin untuk menambahkan coffee baru
            nama = input("Enter coffee name: ")
            harga = float(input("Enter coffee price: "))
            
            # Memanggil fungsi create_coffee untuk menambahkan coffee ke database
            create_coffee(nama, harga, cursor, conn)
            
        elif choice == "2":
            # Menampilkan menu coffee kepada admin
            read_coffees(cursor)
        elif choice == "3":
            # Update Coffee
            update_coffee_menu(cursor, conn)
        elif choice == "4":
            # Delete Coffee
            delete_coffee_menu(cursor, conn)
        elif choice == "5":
            # Lihat transaksi
            view_transactions(cursor)
        elif choice == "6":
            print("===================================")
            print("|       Exiting admin menu.       |")
            print("===================================")
            break
        else:
            print("===================================")
            print("|Invalid option. Please try again.|")
            print("===================================")



def login(name, password, cursor):
    # Variable to mark the success of login and the user's role
    success = False
    role = ""
    try:
        # SQL query to check user credentials
        query = "SELECT * FROM user WHERE username = %s AND password = %s"
        
        # Execute the query with parameters
        cursor.execute(query, (name, password))

        # Fetch the result
        result = cursor.fetchone()

        # If the result is found, login is successful
        if result:
            success = True
            role = result[3]
        
    except mysql.connector.Error as err:
        # Handle the database error and print the details
        print(f"MySQL Error: {err}")
    
    # Print login status
    if success:
        print("-" * 50)
        print(f" | Login as {role} successful, welcome {name}! | ")
        print("-" * 50)
        return role
    else:
        print("-" * 50)
        print("| Username or password is incorrect. Please try again. |")
        print("-" * 50)
        return None



    
def is_valid_username(username):
    # Validasi nama pengguna: hanya huruf panjang minimal 4 karakter
    return re.match("^[a-zA]{4,}$", username) is not None

def is_valid_password(password):
    # Validasi kata sandi: minimal 8 karakter, setidaknya satu huruf besar, satu huruf kecil, dan satu angka
    return re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password) is not None


def register(name, password, role, cursor, conn):
    #query sql untuk menambahkan pengguna baru ke dalam tabel users
    query = "INSERT INTO user (username, password, role) VALUES (%s, %s, %s)"
    #menjalankan query dengan parameter username,password dan role
    cursor.execute(query, (name, password, role))
    #commit perubahannya ke database
    conn.commit()

if __name__ == "__main__": #blok yang akan dieksekusi hanya jika skrip dijalankan sebagai program utama
    #membuat koneksi kedatabase mysql dan membuat objek kursor yang akan digunakan untuk megeksekusi pernyatan sql
    conn = mysql.connector.connect(
        host="localhost", user="root", password="", database="coffee"
    )
    cursor = conn.cursor()
#memanggil fungsi main dengan melewatkan objek kursor dan koneksi sebagai argumen
    main(cursor, conn)