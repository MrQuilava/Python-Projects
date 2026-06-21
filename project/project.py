import os
import re
import sys
import tkinter as tk
from tkinter import messagebox


def main():
    # Wrap your UI setup loop completely inside main() to satisfy CS50P requirements
    global date, email_entry, result_label, type_label, result_box

    gui = tk.Tk()
    gui.title("Account Bot Detector: Email Analysis & Logging")
    gui.geometry("900x850")
    gui.configure(bg="#F0F0F0")

    main_frame = tk.Frame(gui, bg="#F0F0F0")
    main_frame.pack(pady=20)

    tk.Label(main_frame, text="Account Bot Detector", font=("Helvetica", 24, "bold"), bg="#F0F0F0").pack()
    tk.Label(main_frame, text="Enter email addresses and enter logs by date", font=("Helvetica", 12), fg="#666", bg="#F0F0F0").pack()

    # The Date Input
    tk.Label(main_frame, text="Enter Date Today (e.g., April172026):", font=("Helvetica", 12, "bold"), bg="#F0F0F0").pack(pady=(15,0))
    date = tk.Entry(main_frame, font=("Helvetica", 14), width=30, justify="center", bd=2, relief="sunken")
    date.pack(pady=5)

    # The Email Input
    tk.Label(main_frame, text="Analyze Email Address:", font=("Helvetica", 12, "bold"), bg="#F0F0F0").pack(pady=(10,0))
    email_entry = tk.Entry(main_frame, width=35, font=("Helvetica", 18), bd=2, relief="groove", justify="center")
    email_entry.pack(pady=10, ipady=5)

    # Control Buttons
    btn_frame = tk.Frame(main_frame, bg="#F0F0F0")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Analyze & Save", bg="#FF0000", fg="white", width=18, font=("Helvetica", 10, "bold"), command=detect_bot).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Load Current Logs", bg="#2196F3", fg="white", width=18, font=("Helvetica", 10, "bold"), command=load_file).pack(side=tk.LEFT, padx=5)

    # Display Results
    result_label = tk.Label(main_frame, text="Waiting for input...", font=("Helvetica", 16, "bold"), bg="#F0F0F0")
    result_label.pack(pady=(10, 0))

    type_label = tk.Label(main_frame, text="Category: None", font=("Helvetica", 14), fg="#555", bg="#F0F0F0")
    type_label.pack()

    # Layout Header
    header = f"{'EMAIL ADDRESS':<35} | {'CATEGORY':<20} | {'STATUS'}"
    tk.Label(gui, text=header, font=("Courier", 10, "bold"), bg="#E0E0E0", width=100, anchor="w").pack(pady=(20,0))

    # Text Frame Box
    result_box = tk.Text(gui, font=("Courier", 10), bg="white", height=15, width=100, relief="solid", bd=1)
    result_box.pack(padx=20, pady=10)

    gui.mainloop()


# --- REQUIRED CUSTOM FUNCTION 1 (Tested via Pytest) ---
def validate_email_format(email):
    """Checks if email format matches general standards or BatStateU formatting."""
    bsu_pattern = r'^2[1-5]-\d{5}@g\.batstate-u\.edu\.ph$'
    general_format = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"

    if re.match(bsu_pattern, email, re.IGNORECASE):
        return "BSU"
    elif re.match(general_format, email, re.IGNORECASE):
        return "GENERAL"
    return "INVALID"


# --- REQUIRED CUSTOM FUNCTION 2 (Tested via Pytest) ---
def classify_domain(domain):
    """Maps domain extension type strings to their structural entities."""
    categories_dict = {
        "gmail.com": "Personal Account",
        "edu.ph": "PH Education",
        "edu": "International Education",
        "gov": "Government Account",
        "org": "Organization/Company Account"
    }
    return categories_dict.get(domain.lower(), "Entity")


# --- REQUIRED CUSTOM FUNCTION 3 (Tested via Pytest) ---
def check_suspicious_patterns(username):
    """Scans the username segment for dense structural anomalies."""
    excessive_numbers = r'\d{5,}'
    gibberish_pattern = r'[^aeiouy0-9]{5,}'

    if re.search(excessive_numbers, username) or re.search(gibberish_pattern, username):
        return True
    return False


def detect_bot():
    date_input = date.get().strip()
    if not date_input:
        messagebox.showwarning("File Error", "Besto Frendo! Please enter the Date/Session name!")
        return

    filename = f"recordlogs_{date_input}.txt"
    email = email_entry.get().strip()
    if not email:
        messagebox.showwarning("Input Error", "Please enter an email address!")
        return

    # Utilize our cleanly abstracted standalone functions
    email_type = validate_email_format(email)
    status, category, color = "", "", ""

    if email_type == "BSU":
        status, category, color = "Verified Student", "BSU Student", "#388E3C"
    elif email_type == "INVALID":
        status, category, color = "Unacceptable Domain", "Unknown", "#FF8C00"
    else:
        try:
            username, domain_type = email.split('@', 1)
            base_cat = classify_domain(domain_type)

            if check_suspicious_patterns(username):
                status, category, color = "Bot Detected", f"Suspicious {base_cat}", "#D32F2F"
            else:
                status, category, color = "Verified Real", f"{base_cat} Account", "#388E3C"
        except ValueError:
            status, category, color = "Unacceptable Domain", "Unknown", "#FF8C00"

    # Append to file
    with open(filename, "a") as file:
        file.write(f"{email:<35} | {category:<20} | {status}\n")

    # Update UI Elements
    result_label.config(text=f"Status: {status}", fg=color)
    type_label.config(text=f"Category: {category}")
    result_box.delete("1.0", tk.END)
    result_box.insert("1.0", f"SUCCESS: Record saved to {filename}!")


def load_file():
    date_input = date.get().strip()
    if not date_input:
        messagebox.showwarning("Selection Error", "File does not exist!")
        return

    filename = f"recordlogs_{date_input}.txt"

    if os.path.exists(filename):
        with open(filename, "r") as file:
            content = file.read()
            result_box.delete("1.0", tk.END)
            result_box.insert("1.0", content)
    else:
        result_box.delete("1.0", tk.END)
        result_box.insert("1.0", f"Error: {filename} not found.")


if __name__ == "__main__":
    main()
