Langkah-Langkah Menjalankan Program:

1. Pastikan Python telah diinstal di komputer Anda. Anda bisa mendownloadnya dari python.org.

2. Salin kode Python yang telah Anda tulis ke dalam sebuah file Python dengan ekstensi .py. Misalnya, simpan sebagai multi_cipher_gui.py.

3. Menjalankan Program:
- Buka terminal atau command prompt, dan arahkan ke direktori di mana Anda menyimpan file Python tersebut.
- Jalankan program dengan perintah berikut di terminal:
python multi_cipher_gui.py

4. Penggunaan Antarmuka Aplikasi:
Saat program dijalankan, sebuah jendela GUI akan terbuka dengan judul Multi-Cipher Application.
Bagian Input:
- Cipher Method: Pilih metode cipher yang ingin Anda gunakan, yaitu Vigenere, Playfair, atau Hill.
- Input Source: Pilih apakah Anda ingin memasukkan teks secara langsung atau memuat teks dari sebuah file.
    Jika memilih "Text", Anda bisa mengetik teks di area yang disediakan.
    Jika memilih "File", Anda harus memilih file teks (.txt) dari komputer Anda.

- Bagian Kunci (Key):
Masukkan kunci yang diperlukan untuk enkripsi atau dekripsi. Kunci harus minimal 12 karakter untuk metode cipher Vigenere dan Playfair. Untuk Hill cipher, kunci harus dapat diterjemahkan menjadi matriks 3x3.

- Bagian Operasi:
Pilih apakah Anda ingin melakukan Encrypt (enkripsi) atau Decrypt (dekripsi) pada teks yang telah dimasukkan.

5. Proses Cipher:
- Setelah memasukkan teks, memilih metode cipher, memasukkan kunci, dan memilih operasi enkripsi atau dekripsi, klik tombol Process.
- Hasil enkripsi atau dekripsi akan ditampilkan di bagian Output di bagian bawah aplikasi.

Contoh Penggunaan:
Jika Anda memilih Vigenere cipher, memasukkan teks "HELLO" dan kunci "KEYKEYKEYKEY", serta memilih operasi "Encrypt", hasil enkripsinya akan muncul di bagian output.

7. Error Handling:
Jika Anda tidak memasukkan kunci dengan panjang minimal 12 karakter, atau tidak memasukkan teks, akan muncul pesan kesalahan menggunakan messagebox.
