import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from bot.bot import text_to_voice, get_weather

import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from bot.bot import text_to_voice, get_weather
from tkinter import simpledialog

# Ensure the script is executed from the project root
base_dir = os.path.abspath(os.path.dirname(__file__))
image_folder = os.path.normpath(os.path.join(base_dir, "../gui_images"))

# Image paths
wave_image_path = os.path.normpath(os.path.join(image_folder, "wave.png"))
cloud_image_path = os.path.normpath(os.path.join(image_folder, "cloud.png"))
gmail_logo_path = os.path.normpath(os.path.join(image_folder, "gmail_logo.png"))

# Create the main window
root = tk.Tk()
root.title("Chatbot Interface")
root.geometry("600x500")
root.minsize(600, 500)
root.configure(bg="#2c3e50")

# Load images
try:
    wave_image = Image.open(wave_image_path).resize((60, 60), Image.Resampling.LANCZOS)
    wave_photo = ImageTk.PhotoImage(wave_image)

    cloud_image = Image.open(cloud_image_path).resize((60, 60), Image.Resampling.LANCZOS)
    cloud_photo = ImageTk.PhotoImage(cloud_image)

    gmail_logo = Image.open(gmail_logo_path).resize((30, 30), Image.Resampling.LANCZOS)
    gmail_photo = ImageTk.PhotoImage(gmail_logo)
except FileNotFoundError as e:
    print(f"[DEBUG] Error loading image: {e}")
    exit(1)

# Function to open Text-to-Voice window
def open_text_to_voice():
    window = tk.Toplevel(root)
    window.title("Text-to-Voice")
    window.geometry("400x200")
    window.configure(bg="#34495e")
    ttk.Label(window, text="Enter Text:", background="#34495e", foreground="white", font=("Arial", 12)).pack(pady=10)
    text_input = ttk.Entry(window, width=40)
    text_input.pack(pady=10)
    def convert_text():
        text = text_input.get()
        if text.strip():
            text_to_voice(text)
        else:
            messagebox.showwarning("Input Error", "Please enter some text.")
    ttk.Button(window, text="Convert to Voice", command=convert_text).pack(pady=10)

# Function to open Weather Info window
def open_weather_info():
    city = tk.simpledialog.askstring("Weather Info", "Enter City:")
    if not city:
        return

    weather_info = get_weather(city)
    if "City not found" in weather_info or not isinstance(weather_info, str):
        messagebox.showerror("Error", weather_info)
        return

    weather_window = tk.Toplevel(root)
    weather_window.title("Weather Information")
    weather_window.geometry("600x800")
    
    weather_data = []
    for line in weather_info.split('\n'):
        if line.strip() and ":" in line:
            key, value = line.split(':', 1)
            weather_data.append((key.strip(), value.strip()))

    description = next((value for key, value in weather_data if key == "Description"), "").lower()
    
    weather_colors = {
        "clear sky": "lightblue",
        "few clouds": "lightgrey",
        "scattered clouds": "grey",
        "broken clouds": "darkgrey",
        "shower rain": "lightcoral",
        "rain": "blue",
        "thunderstorm": "darkblue",
        "snow": "white",
        "mist": "lightyellow"
    }
    
    bg_color = weather_colors.get(description, "lightblue")
    
    weather_frame = ttk.Frame(weather_window, padding=20)
    weather_frame.pack(fill='both', expand=True)
    
    style = ttk.Style()
    style.configure("Weather.TFrame", background=bg_color)
    weather_frame.configure(style="Weather.TFrame")
    
    for i, (key, value) in enumerate(weather_data):
        ttk.Label(weather_frame, text=key, font=("Arial", 12), anchor="w", background=bg_color).grid(row=i, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(weather_frame, text=value, font=("Arial", 12), anchor="w", background=bg_color).grid(row=i, column=1, sticky="w", padx=10, pady=5)
    
    ttk.Button(weather_window, text="OK", command=weather_window.destroy).pack(pady=10)

# Main Frame
main_frame = ttk.Frame(root, padding=(20, 20, 20, 20))
main_frame.pack(expand=True)
main_frame.configure(style="Custom.TFrame")

# Define custom styles
style = ttk.Style()
style.configure("Custom.TFrame", background="#2c3e50")
style.configure("Custom.TButton", font=("Arial", 12), padding=10)

# Buttons with images to open new windows
btn1 = ttk.Button(main_frame, text=" Text-to-Voice", image=wave_photo, compound="left", style="Custom.TButton", command=open_text_to_voice)
btn1.pack(pady=10)

btn2 = ttk.Button(main_frame, text=" Weather Info", image=cloud_photo, compound="left", style="Custom.TButton", command=open_weather_info)
btn2.pack(pady=10)

# Bottom frame for owner details
bottom_frame = ttk.Frame(root, padding=(10, 5))
bottom_frame.pack(fill="x")
bottom_frame.configure(style="Custom.TFrame")

details_label = ttk.Label(bottom_frame, text="Owner: Shariar Ahamed", font=("Arial", 10), background="#2c3e50", foreground="white")
details_label.pack(side="left", padx=5)

gmail_label = ttk.Label(bottom_frame, image=gmail_photo, background="#2c3e50")
gmail_label.pack(side="left", padx=(5, 0))

email_label = ttk.Label(bottom_frame, text="www.saaulfy@gmail.com", font=("Arial", 10), foreground="lightblue", cursor="hand2", background="#2c3e50")
email_label.pack(side="left", padx=(5, 10))

def open_email(event):
    import webbrowser
    webbrowser.open("mailto:www.saaulfy@gmail.com")

email_label.bind("<Button-1>", open_email)

# Start the GUI loop
root.mainloop()
