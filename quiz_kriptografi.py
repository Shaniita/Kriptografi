import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from tkinter.font import Font

def get_input():
    if input_choice.get() == 'File':
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                return file.read().strip()
        else:
            messagebox.showwarning("Warning", "No file selected.")
            return None
    else:
        return input_text.get("1.0", tk.END).strip()

def get_key(min_length=12):
    key = key_entry.get().strip().upper()
    if len(key) < min_length:
        messagebox.showerror("Error", f"Key must be at least {min_length} characters.")
        return None
    return key

# Vigenere Cipher
def vigenere_cipher(text, key, encrypt=True):
    result = ""
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % key_length]) - ord('A')
            if not encrypt:  # untuk decrypt
                shift = -shift
            if char.isupper():
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += char
    return result

# Playfair Cipher
def generate_playfair_matrix(key):
    key = ''.join(dict.fromkeys(key.upper().replace("J", "I") + "ABCDEFGHIKLMNOPQRSTUVWXYZ"))
    return [list(key[i:i+5]) for i in range(0, 25, 5)]

def find_in_matrix(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return -1, -1

def playfair_cipher(text, key, encrypt=True):
    matrix = generate_playfair_matrix(key)
    text = text.upper().replace("J", "I")
    if len(text) % 2 != 0:
        text += 'X'
    
    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        row1, col1 = find_in_matrix(matrix, a)
        row2, col2 = find_in_matrix(matrix, b)
        
        if row1 == row2:
            col1, col2 = (col1 + (1 if encrypt else -1)) % 5, (col2 + (1 if encrypt else -1)) % 5 
        elif col1 == col2:
            row1, row2 = (row1 + (1 if encrypt else -1)) % 5, (row2 + (1 if encrypt else -1)) % 5
        else:
            col1, col2 = col2, col1
        
        result += matrix[row1][col1] + matrix[row2][col2]
    
    return result

# Hill Cipher
def matrix_multiply(matrix1, matrix2, mod):
    result = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]
            result[i][j] %= mod
    return result

def matrix_determinant(matrix):
    return (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
            - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
            + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))

def matrix_inverse(matrix, mod):
    det = matrix_determinant(matrix) % mod
    det_inv = pow(det, -1, mod)
    
    adjugate = [
        [(matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) % mod,
         (matrix[0][2] * matrix[2][1] - matrix[0][1] * matrix[2][2]) % mod,
         (matrix[0][1] * matrix[1][2] - matrix[0][2] * matrix[1][1]) % mod],
        [(matrix[1][2] * matrix[2][0] - matrix[1][0] * matrix[2][2]) % mod,
         (matrix[0][0] * matrix[2][2] - matrix[0][2] * matrix[2][0]) % mod,
         (matrix[0][2] * matrix[1][0] - matrix[0][0] * matrix[1][2]) % mod],
        [(matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]) % mod,
         (matrix[0][1] * matrix[2][0] - matrix[0][0] * matrix[2][1]) % mod,
         (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % mod]
    ]
    
    return [[((adjugate[i][j] * det_inv) % mod) for j in range(3)] for i in range(3)]

def hill_cipher(text, key, encrypt=True):
    key_matrix = [[ord(key[i*3+j]) - ord('A') for j in range(3)] for i in range(3)]
    if not encrypt:
        key_matrix = matrix_inverse(key_matrix, 26)  # untuk decrypt
    
    text = text.upper()
    if len(text) % 3 != 0:
        text += 'X' * (3 - len(text) % 3)
    
    result = ""
    for i in range(0, len(text), 3):
        block = [[ord(text[i+j]) - ord('A')] for j in range(3)]
        encrypted_block = matrix_multiply(key_matrix, block, 26)  # untuk encrypt
        result += ''.join([chr(int(c[0]) + ord('A')) for c in encrypted_block])
    
    return result

def process_cipher():
    method = cipher_choice.get()
    operation = operation_choice.get()
    
    text = get_input()
    if text is None:
        return
    
    key = get_key()
    if not text or not key:
        return
    
    try:
        if method == 'Vigenere':
            result = vigenere_cipher(text, key, operation == 'Encrypt')
        elif method == 'Playfair':
            result = playfair_cipher(text, key, operation == 'Encrypt')
        elif method == 'Hill':
            result = hill_cipher(text, key, operation == 'Encrypt')
        else:
            messagebox.showerror("Error", "Unrecognized method.")
            return
        
        output_text.config(state='normal')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
        output_text.config(state='disabled')
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_input_state(*args):
    if input_choice.get() == 'File':
        input_text.config(state='disabled')
        select_file_button.config(state='normal')
    else:
        input_text.config(state='normal')
        select_file_button.config(state='disabled')

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            input_text.config(state='normal')
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, file.read().strip())
            input_text.config(state='disabled')

# GUI setup
root = tk.Tk()
root.title("Multi-Cipher Application")
root.geometry("800x600")
root.configure(bg='#f0f0f0')

style = ttk.Style()
style.theme_use('clam')

title_font = Font(family="Helvetica", size=16, weight="bold")
header_font = Font(family="Helvetica", size=12, weight="bold")
normal_font = Font(family="Helvetica", size=10)

main_frame = ttk.Frame(root, padding="20 20 20 20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Title
title_label = ttk.Label(main_frame, text="Multi-Cipher Application", font=title_font)
title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

# Left frame for input and cipher selection
left_frame = ttk.Frame(main_frame, padding="10 10 10 10")
left_frame.grid(row=1, column=0, sticky="nsew")

ttk.Label(left_frame, text="Cipher Method:", font=header_font).grid(row=0, column=0, sticky="w", pady=(0, 10))
cipher_choice = tk.StringVar(value='Vigenere')
ttk.Radiobutton(left_frame, text="Vigenere", variable=cipher_choice, value='Vigenere', style='TRadiobutton').grid(row=1, column=0, sticky="w")
ttk.Radiobutton(left_frame, text="Playfair", variable=cipher_choice, value='Playfair', style='TRadiobutton').grid(row=2, column=0, sticky="w")
ttk.Radiobutton(left_frame, text="Hill", variable=cipher_choice, value='Hill', style='TRadiobutton').grid(row=3, column=0, sticky="w")

ttk.Label(left_frame, text="Input Source:", font=header_font).grid(row=4, column=0, sticky="w", pady=(20, 10))
input_choice = tk.StringVar(value='Text')
input_choice.trace('w', update_input_state)
ttk.Radiobutton(left_frame, text="Text", variable=input_choice, value='Text', style='TRadiobutton').grid(row=5, column=0, sticky="w")
ttk.Radiobutton(left_frame, text="File", variable=input_choice, value='File', style='TRadiobutton').grid(row=6, column=0, sticky="w")

ttk.Label(left_frame, text="Input:", font=header_font).grid(row=7, column=0, sticky="w", pady=(20, 10))
input_text = scrolledtext.ScrolledText(left_frame, height=8, width=40, font=normal_font)
input_text.grid(row=8, column=0, sticky="nsew")

select_file_button = ttk.Button(left_frame, text="Select File", command=select_file)
select_file_button.grid(row=9, column=0, sticky="w", pady=(10, 0))
select_file_button.config(state='disabled')

# Right frame for key input, operation selection, and output
right_frame = ttk.Frame(main_frame, padding="10 10 10 10")
right_frame.grid(row=1, column=1, sticky="nsew", padx=(20, 0))

ttk.Label(right_frame, text="Key (min 12 characters):", font=header_font).grid(row=0, column=0, sticky="w", pady=(0, 10))
key_entry = ttk.Entry(right_frame, width=40, font=normal_font)
key_entry.grid(row=1, column=0, sticky="ew")

ttk.Label(right_frame, text="Operation:", font=header_font).grid(row=2, column=0, sticky="w", pady=(20, 10))
operation_choice = tk.StringVar(value='Encrypt')
ttk.Radiobutton(right_frame, text="Encrypt", variable=operation_choice, value='Encrypt', style='TRadiobutton').grid(row=3, column=0, sticky="w")
ttk.Radiobutton(right_frame, text="Decrypt", variable=operation_choice, value='Decrypt', style='TRadiobutton').grid(row=4, column=0, sticky="w")

process_button = ttk.Button(right_frame, text="Process", command=process_cipher)
process_button.grid(row=5, column=0, sticky="w", pady=(20, 0))

ttk.Label(right_frame, text="Output:", font=header_font).grid(row=6, column=0, sticky="w", pady=(20, 10))
output_text = scrolledtext.ScrolledText(right_frame, height=8, width=40, font=normal_font, state='disabled')
output_text.grid(row=7, column=0, sticky="nsew")

# Configure grid weights
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(1, weight=1)
left_frame.columnconfigure(0, weight=1)
left_frame.rowconfigure(8, weight=1)
right_frame.columnconfigure(0, weight=1)
right_frame.rowconfigure(7, weight=1)

root.mainloop()