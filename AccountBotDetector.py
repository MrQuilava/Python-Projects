import tkinter as tk
from tkinter import messagebox
import re

def detect_bot():
    email = email_entry.get().strip()
    
    if not email:
        messagebox.showwarning("Input Error", "Please enter an email address!")
        return

    # --- PATTERNS ---
    bsu_pattern = r'^2[1-5]-\d{5}@g\.batstate-u\.edu\.ph$'
    general_format = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    excessive_numbers = r'\d{5,}' 
    gibberish_pattern = r'[^aeiouy0-9]{5,}'

    # --- LOGIC ---
    bsu_match = re.match(bsu_pattern, email, re.IGNORECASE)
    general_match = re.match(general_format, email, re.IGNORECASE)
    status, category, color = "", "", ""


    if bsu_match:
        status, category, color = "Verified Student ✅", "BSU Student", "#388E3C"
    elif not general_match:
        status, category, color = "Unacceptable Domain", "Unknown", "#FF8C00"
    else:
        username = email.split('@')[0].lower()
        domain_type = email.split('@')[1].lower()
        
        categories_dict = {"gmail.com": "Personal", "edu.ph": "PH Edu", "edu": "Intl Edu", "gov": "Gov", "org": "Org"}
        base_cat = categories_dict.get(domain_type, "Entity")

        if not general_match:
            status, category, color = "Bot Detected 🤖", f"Suspicious {base_cat}", "#D32F2F"
        elif re.search(excessive_numbers, username) or re.search(gibberish_pattern, username):
            status, category, color = "Bot Detected 🤖", f"Suspicious {base_cat}", "#D32F2F"
        else:
            status, category, color = "Verified Real ✅", f"{base_cat} Account", "#388E3C"

    # Update UI Labels
    result_label.config(text=f"Status: {status}", fg=color)
    type_label.config(text=f"Category: {category}")

    # --- NEW FEATURE: DYNAMIC LOGGING ---
    # This inserts the result into our "Table" at the bottom
    log_display.config(state="normal") # Enable editing to add text
    log_display.insert("end", f"{email:<35} | {category:<20} | {status}\n")
    log_display.config(state="disabled") # Disable editing so user can't type in it
    log_display.see("end") # Auto-scroll to the latest entry

# --- GUI SETUP ---
gui = tk.Tk()
gui.title("The Account Bot Detector - Official Version")
gui.geometry("900x750") # Increased height for the table
gui.configure(bg="#F0F0F0")

main_frame = tk.Frame(gui, bg="#F0F0F0")
main_frame.pack(pady=20)

# Title Label: Large header text
tk.Label(main_frame, text="The Account Bot Detector", 
         font=("Helvetica", 24, "bold"), bg="#F0F0F0").pack(pady=10)
sss
# Subtitle: Small instruction text
tk.Label(main_frame, text="Recognizes SR-Codes and Official Domains", 
         font=("Helvetica", 12), fg="#666", bg="#F0F0F0").pack()

email_entry = tk.Entry(main_frame, width=35, font=("Helvetica", 18), bd=2, relief="groove", justify="center")
email_entry.pack(pady=20, ipady=8)

detect_button = tk.Button(main_frame, text="Click to Analyze and Record", command=detect_bot, 
                          bg="#D32F2F", fg="white", font=("Helvetica", 12, "bold"), padx=30, pady=10)
detect_button.pack()

result_label = tk.Label(main_frame, text="Waiting for input...", font=("Helvetica", 16, "bold"), bg="#F0F0F0")
result_label.pack(pady=(15, 0))

type_label = tk.Label(main_frame, text="Category: None", font=("Helvetica", 14), fg="#555", bg="#F0F0F0")
type_label.pack()

# --- THE RECORDING TABLE (LOG SECTION) ---
tk.Label(gui, text="--- SESSION ACTIVITY LOG ---", font=("Courier", 12, "bold"), bg="#F0F0F0", fg="#333").pack(pady=(20, 0))

# Header for our fake table
header = f"{'EMAIL ADDRESS':<35} | {'CATEGORY':<20} | {'STATUS'}"
tk.Label(gui, text=header, font=("Courier", 10, "bold"), bg="#E0E0E0", anchor="w", width=90).pack()

log_display = tk.Text(gui, height=12, width=90, font=("Courier", 10), state="disabled", bg="white", relief="sunken")
log_display.pack(pady=10)

gui.mainloop()
