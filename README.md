# Sistem-Manajemen-Pengiriman-Barang-Berdasarkan-Prioritas
Sistem Manajemen Pengiriman Barang Berdasarkan Prioritas sangat penting dalam industri logistik. Kepuasan pelanggan merupakan faktor utama yang mendorong pengembangan sistem ini, karena pelanggan sering kali memiliki kebutuhan mendesak yang memerlukan pengiriman barang tepat waktu. Keterlambatan pengiriman dapat berdampak negatif pada operasional pelanggan sehingga sistem manajemen pengiriman barang berdasarkan prioritas diperlukan untuk memastikan pengiriman tepat waktu sesuai dengan tingkat kepentingan dan urgensi pelanggan. Selain itu, persaingan di industri logistik juga mendorong perusahaan untuk menawarkan layanan pengiriman barang prioritas sebagai cara untuk memenangkan kepercayaan pelanggan dan mempertahankan keunggulan kompetitif. Dalam kesimpulannya, sistem ini memungkinkan perusahaan memberikan layanan yang lebih baik, meningkatkan kepuasan pelanggan, dan memperoleh keuntungan dalam pasar yang kompetitif.

## Tujuan
1. Mengatur prioritas barang yang akan dikirim terlebih dahulu.
2. Mengurutkan barang yang akan dikirim berdasarkan tanggal input barang yang lebih dahulu dibuat atau berdasarkan prioritas barang.
3. Mengetahui Status Barang dan mengatur proses barang yang akan dikirim.
4. Mengetahui alamat tujuan serta nama pengirim barang.

## Metode 
1. Shell Sort: Shell sort digunakan ketika pengurutan di list barang berdasarkan jenis paket, ketika ada jenis paket yg sama maka akan diurutkan dari no.resi terkecil
2. Breadth-First Search: BFS digunakan untuk mencari data pengirim berdasarkan nomor resi nya.
3. Queue dan Priority Queue: Dipakai pada Breath First Search. Selain itu untuk melihat jenis pengiriman barang apakah prioritas atau reguler.
4. Linked List: Dipakai untuk men-generate nomor resi baru, akan mengecek node nomor resi sampai ke node terakhir, ketika node terakhir ditemukan, generate nomor resi baru dengan menambahkan +1 dari nomor resi node sebelumnya.

## Alur Program
**1. Tampilan Awal**
Terdapat pilihan layanan 
-Login (Untuk masuk ke akses karyawan)
- Pemantauan Pengiriman (yang dapat dilakukan oleh customer)

**2. Login**
Login diberlakukan untuk mendeteksi cabang pengiriman. Tiap tiap cabang akan memiliki akses data yang berbeda.

**3. Pemantauan Pengiriman Admin**
Admin bisa mengecek daftar barang yang akan dikirim serta memilih barang mana saja yang akan diproses. Pada tampilan ini daftar barang bisa di urutkan berdasarkan tanggal input, nama barang, maupun jenis pengiriman (prioritas atau bukan)

**4. Pendaftaran Pengiriman**
Pengisian form(mampu menentukan tingkat prioritas barang yang akan dikirim) -> mendapatkan no.resi dan bukti pengiriman -> masuk ke list penjadwalan pengiriman

