import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from bot.bot import text_to_voice, get_weather

# Ensure the script is executed from the project root
base_dir = os.path.abspath(os.path.dirname(__file__))
image_folder = os.path.normpath(os.path.join(base_dir, "../gui_images"))

# Debugging output for paths
wave_image_path = os.path.normpath(os.path.join(image_folder, "wave.png"))
cloud_image_path = os.path.normpath(os.path.join(image_folder, "cloud.png"))
gmail_logo_path = os.path.normpath(os.path.join(image_folder, "gmail_logo.png"))

print(f"[DEBUG] Wave image path: {wave_image_path}")
print(f"[DEBUG] Cloud image path: {cloud_image_path}")
print(f"[DEBUG] Gmail logo path: {gmail_logo_path}")

# Create the main window
root = tk.Tk()
root.title("Chatbot Interface")
root.geometry("600x500")
root.minsize(600, 500)

# Load images after the Tkinter root window is created
try:
    wave_image = Image.open(wave_image_path).resize((40, 40), Image.Resampling.LANCZOS)
    wave_photo = ImageTk.PhotoImage(wave_image)

    cloud_image = Image.open(cloud_image_path).resize((40, 40), Image.Resampling.LANCZOS)
    cloud_photo = ImageTk.PhotoImage(cloud_image)

    gmail_logo = Image.open(gmail_logo_path).resize((20, 20), Image.Resampling.LANCZOS)
    gmail_photo = ImageTk.PhotoImage(gmail_logo)
    print("[DEBUG] Images loaded successfully")
except FileNotFoundError as e:
    print(f"[DEBUG] Error loading image: {e}")
    exit(1)

# Functions for handling actions
def handle_text_to_voice():
    text = text_input.get()
    if not text.strip():
        messagebox.showwarning("Input Error", "Please enter some text.")
    else:
        text_to_voice(text)
        #messagebox.showinfo("Bot", "Text has been converted to voice.")

def handle_weather():
    city = city_input.get()
    weather_info = get_weather(city)

    # Check if weather information was retrieved successfully
    if "City not found" in weather_info or not isinstance(weather_info, str):
        messagebox.showerror("Error", weather_info)
        return

    weather_window = tk.Toplevel()
    weather_window.title("Weather Information")
    weather_window.geometry("600x800")  # Set size of the new window

    # Parse weather information into a list of tuples
    weather_data = []
    for line in weather_info.split('\n'):
        if line.strip() and ":" in line:  # Ensure line has a colon to split
            key, value = line.split(':', 1)
            weather_data.append((key.strip(), value.strip()))

    # Extract weather description to determine background color
    description = next((value for key, value in weather_data if key == "Description"), "").lower()

    # Define a dictionary mapping weather descriptions to colors
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

    # Get the background color based on the description
    bg_color = weather_colors.get(description, "lightblue")  # Default to lightblue

    # Create a frame to hold the weather details with dynamic background color
    weather_frame = ttk.Frame(weather_window, padding=20)
    weather_frame.pack(fill='both', expand=True)
    weather_frame.configure(style="Custom.TFrame")

    # Define a custom style for the frame with the selected background color
    style = ttk.Style()
    style.configure("Custom.TFrame", background=bg_color)

    # Create a grid table with labels
    for i, (key, value) in enumerate(weather_data):
        parameter_label = ttk.Label(weather_frame, text=key, font=("Arial", 12), anchor="w", background=bg_color)
        parameter_label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
        value_label = ttk.Label(weather_frame, text=value, font=("Arial", 12), anchor="w", background=bg_color)
        value_label.grid(row=i, column=1, sticky="w", padx=10, pady=5)

    # Create an OK button to close the window
    ok_button = ttk.Button(weather_window, text="OK", command=weather_window.destroy)
    ok_button.pack(pady=10)

    
# Configure grid for the main window
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)

# Create the main frame for the chatbot interface
main_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.columnconfigure(0, weight=0)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=0)

# Add widgets for Text-to-Voice
ttk.Label(main_frame, text="Enter Text for Text-to-Voice:").grid(column=0, row=0, sticky=tk.W, pady=10, padx=10)
wav_label = ttk.Label(main_frame, image=wave_photo)
wav_label.grid(column=0, row=1, sticky=tk.W, padx=10)
text_input = ttk.Entry(main_frame, width=40)
text_input.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=10)
text_to_voice_button = ttk.Button(main_frame, text="Convert to Voice", command=handle_text_to_voice)
text_to_voice_button.grid(column=2, row=1, pady=10, padx=10)


#Widget
ttk.Label(main_frame, text="Enter City Name for Weather Info:").grid(column=0, row=2, sticky=tk.W, pady=10, padx=10)
cloud_label = ttk.Label(main_frame, image=cloud_photo)
cloud_label.grid(column=0, row=3, sticky=tk.W, padx=10)
city_input = ttk.Entry(main_frame, width=50)
city_input.grid(column=1, row=3, sticky=(tk.W, tk.E), pady=10)
weather_button = ttk.Button(main_frame, text="Get Weather", command=handle_weather)
weather_button.grid(column=2, row=3, pady=10, padx=10)


# Add a bottom frame for the details
bottom_frame = ttk.Frame(root, padding=(10, 5))
bottom_frame.grid(row=1, column=0, sticky="ew")
bottom_frame.columnconfigure(1, weight=1)

# Add owner details to the bottom frame
details_label = ttk.Label(bottom_frame, text="Owner: Shariar Ahamed", font=("Arial", 10))
details_label.grid(column=0, row=0, sticky=tk.W, padx=5)

# Add Gmail logo and email address
gmail_label = ttk.Label(bottom_frame, image=gmail_photo)
gmail_label.grid(column=1, row=0, sticky=tk.W, padx=(5, 0))

email_label = ttk.Label(bottom_frame, text="www.saaulfy@gmail.com", font=("Arial", 10), foreground="blue", cursor="hand2")
email_label.grid(column=2, row=0, sticky=tk.W, padx=(5, 10))

def open_email(event):
    import webbrowser
    webbrowser.open("mailto:www.saaulfy@gmail.com")

email_label.bind("<Button-1>", open_email)

# Start the main event loop
root.mainloop()
