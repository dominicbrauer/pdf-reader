import customtkinter as ctk
from tkinter import filedialog, messagebox

from config_parse import parseConfig
from confirm_request import confirmRequest

import main

# Set appearance and theme
ctk.set_appearance_mode("Dark")  # "Light", "Dark", or "System"
ctk.set_default_color_theme('dark-blue')  # "blue", "green", "dark-blue"

# Create the app window
app = ctk.CTk()
app.geometry("600x500")
app.title("PDF_2_CSV")

config = parseConfig()

# Globals
text_font = ctk.CTkFont(family="Arial", size=16, weight="normal")
heading_font = ctk.CTkFont(family="Arial", size=20, weight="bold")


##### PDF Frame #####
pdf_frame = ctk.CTkFrame(app)
pdf_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

def browse_file():
  file_path = filedialog.askopenfilename()
  if file_path:
    pdf_entry_var.set(file_path)

pdf_entry_label = ctk.CTkLabel(pdf_frame, text="PDF:", font=heading_font)
pdf_entry_label.grid(row=0, column=0, padx=5, pady=5)

pdf_entry_var = ctk.StringVar()
pdf_entry = ctk.CTkEntry(pdf_frame, textvariable=pdf_entry_var, width=250, font=text_font)
pdf_entry.grid(row=0, column=1, padx=5, pady=5)

browse_button = ctk.CTkButton(pdf_frame, text="Browse File", command=browse_file, width=100, height=30, font=text_font)
browse_button.grid(row=0, column=2, padx=5, pady=5)
##### PDF Frame #####


##### Contra Account Frame #####
contra_account_frame = ctk.CTkFrame(app)
contra_account_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

contra_account_entry_label = ctk.CTkLabel(contra_account_frame, text="Gegenkonto", font=heading_font)
contra_account_entry_label.grid(row=0, column=0, padx=5, pady=5)

contra_account_entry = ctk.CTkEntry(contra_account_frame, placeholder_text=f"Leer für '{config["contra_account"]}'", font=text_font)
contra_account_entry.grid(row=0, column=1, padx=5, pady=5)

contra_account_error_check_var = ctk.StringVar(value="on")
contra_account_error_checkbox = ctk.CTkCheckBox(
  contra_account_frame,
  checkbox_width=20,
  checkbox_height=20,
  text="Fehler einfügen ('!')",
  variable=contra_account_error_check_var,
  onvalue="on",
  offvalue="off",
  font=("Arial", 16)
)
contra_account_error_checkbox.grid(row=0, column=2, padx=5, pady=5)
##### Contra Account Frame #####


##### Account Frame #####
account_frame = ctk.CTkFrame(app)
account_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

account_entry_label = ctk.CTkLabel(account_frame, text="Konto", font=heading_font)
account_entry_label.grid(row=0, column=0, padx=5, pady=5)

account_entry = ctk.CTkEntry(account_frame, placeholder_text=f"Leer für '{config["account"]}'", font=text_font)
account_entry.grid(row=0, column=1, padx=5, pady=5)
##### Account Frame #####


##### CSV Frame #####
csv_frame = ctk.CTkFrame(app)
csv_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")

def choose_save_path():
  file_path = filedialog.asksaveasfilename(
    defaultextension=".csv",
    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
    title="Choose save location"
  )
  if file_path:
    csv_entry_var.set(file_path)

csv_entry_label = ctk.CTkLabel(csv_frame, text="CSV:", font=heading_font)
csv_entry_label.grid(row=0, column=0, padx=5, pady=5)

csv_entry_var = ctk.StringVar()
csv_entry = ctk.CTkEntry(csv_frame, textvariable=csv_entry_var, width=250, font=text_font)
csv_entry.grid(row=0, column=1, padx=5, pady=5)

csv_location_button = ctk.CTkButton(csv_frame, text="Choose Save Location", command=choose_save_path, font=text_font)
csv_location_button.grid(row=0, column=2, padx=5, pady=5)
##### CSV Frame #####


##### Commit Frame #####
commit_frame = ctk.CTkFrame(app)
commit_frame.grid(row=4, column=0, padx=10, pady=10, sticky="w")

def commit():
  userConfig = {
    "pdf_location": pdf_entry.get(),
    "contra_account": contra_account_entry.get(),
    "wanted_error": contra_account_error_checkbox.get(),
    "account": account_entry.get(),
    "csv_location": csv_entry.get()
  }
  if confirmRequest(userConfig) == False:
    messagebox.showerror("Fail", "Check your inputs")
  else:
    main.main(userConfig)

commit_button = ctk.CTkButton(commit_frame, text="Generate", command=commit, font=heading_font, height=40)
commit_button.grid(row=0, column=0, padx=5, pady=5)
##### Commit Frame #####


# Run the app
app.mainloop()