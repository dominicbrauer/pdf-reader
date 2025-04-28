import customtkinter as ctk

# Set appearance and theme
ctk.set_appearance_mode("Dark")  # "Light", "Dark", or "System"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

# Create the app window
app = ctk.CTk()
app.geometry("400x300")
app.title("CustomTkinter Example")

# Add a label
label = ctk.CTkLabel(app, text="Hello, CustomTkinter!", font=("Arial", 20))
label.pack(pady=20)

# Add an entry (input box)
entry = ctk.CTkEntry(app, placeholder_text="Type something...")
entry.pack(pady=10)

# Add a button
def button_callback():
    label.configure(text=f"You typed: {entry.get()}")

button = ctk.CTkButton(app, text="Submit", command=button_callback)
button.pack(pady=10)

# Run the app
app.mainloop()
