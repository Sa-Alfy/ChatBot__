import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from ChatBot.bot.bot import text_to_voice, get_weather, download_youtube_video
import requests
import webbrowser 
from datetime import datetime

# Ensure the script is executed from the project root
base_dir = os.path.abspath(os.path.dirname(__file__))
image_folder = os.path.normpath(os.path.join(base_dir, "../gui_images"))

# Image paths
wave_image_path = os.path.normpath(os.path.join(image_folder, "wave.png"))
cloud_image_path = os.path.normpath(os.path.join(image_folder, "cloud.png"))
gmail_logo_path = os.path.normpath(os.path.join(image_folder, "gmail_logo.png"))
youtube_logo_path = os.path.normpath(os.path.join(image_folder, "youtube_logo.png"))

# Add weather icons paths
weather_icons_folder = os.path.normpath(os.path.join(base_dir, "../gui_images/weather_icons"))
weather_icons = {
    "clear sky": "sun.png",
    "few clouds": "cloudy.png",
    "scattered clouds": "cloudy.png",
    "broken clouds": "cloudy.png",
    "shower rain": "rainy.png",
    "rain": "rainy.png",
    "thunderstorm": "storm.png",
    "snow": "snow.png",
    "mist": "mist.png"
}

# Create the main window
root = tk.Tk()
root.title("Assistant Interface")
root.geometry("800x600")
root.minsize(800, 600)
root.configure(bg="#1a1a2e")

# Load images
try:
    wave_image = Image.open(wave_image_path).resize((60, 60), Image.Resampling.LANCZOS)
    wave_photo = ImageTk.PhotoImage(wave_image)

    cloud_image = Image.open(cloud_image_path).resize((60, 60), Image.Resampling.LANCZOS)
    cloud_photo = ImageTk.PhotoImage(cloud_image)

    gmail_logo = Image.open(gmail_logo_path).resize((30, 30), Image.Resampling.LANCZOS)
    gmail_photo = ImageTk.PhotoImage(gmail_logo)

    youtube_logo = Image.open(youtube_logo_path).resize((60, 60), Image.Resampling.LANCZOS)
    youtube_photo = ImageTk.PhotoImage(youtube_logo)

    # Load weather icons
    weather_icon_images = {}
    for condition, icon_file in weather_icons.items():
        icon_path = os.path.join(weather_icons_folder, icon_file)
        if os.path.exists(icon_path):
            icon = Image.open(icon_path).resize((100, 100), Image.Resampling.LANCZOS)
            weather_icon_images[condition] = ImageTk.PhotoImage(icon)
except FileNotFoundError as e:
    print(f"[DEBUG] Error loading image: {e}")
    exit(1)

# Define custom styles
style = ttk.Style()
style.theme_use('clam')  # Use clam theme as base
style.configure("Custom.TFrame", background="#1a1a2e")
style.configure("Custom.TButton",
    font=("Helvetica", 12),
    padding=15,
    background="#0f3460",
    foreground="white"
)
style.configure("Custom.TLabel",
    font=("Helvetica", 12),
    background="#1a1a2e",
    foreground="white"
)
style.map("Custom.TButton",
    background=[("active", "#16213e")],
    relief=[("pressed", "groove"), ("!pressed", "ridge")]
)

# Function to create gradient frame
def create_gradient_frame(parent, color1, color2):
    gradient_frame = tk.Canvas(parent, highlightthickness=0)
    gradient_frame.pack(fill="both", expand=True)
    
    def redraw_gradient(event=None):
        width = event.width if event else parent.winfo_width()
        height = event.height if event else parent.winfo_height()
        gradient_frame.delete("gradient")
        
        for i in range(height):
            r1, g1, b1 = parent.winfo_rgb(color1)
            r2, g2, b2 = parent.winfo_rgb(color2)
            r = (r1 + int((r2-r1)*i/height))/256
            g = (g1 + int((g2-g1)*i/height))/256
            b = (b1 + int((b2-b1)*i/height))/256
            color = f'#{int(r):02x}{int(g):02x}{int(b):02x}'
            gradient_frame.create_line(0, i, width, i, fill=color, tags="gradient")
    
    gradient_frame.bind("<Configure>", redraw_gradient)
    return gradient_frame

# Create main gradient background
main_bg = create_gradient_frame(root, "#1a1a2e", "#16213e")

# Main Frame with modern styling
main_frame = ttk.Frame(main_bg, style="Custom.TFrame")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Function to open Text-to-Voice window
def create_modern_window(title, size="400x300"):
    window = tk.Toplevel(root)
    window.title(title)
    window.geometry(size)
    window.minsize(400, 300)  # Set minimum size
    window.configure(bg="#1a1a2e")  # Add background color to window
    
    bg = create_gradient_frame(window, "#1a1a2e", "#16213e")
    
    content_frame = ttk.Frame(bg, style="Custom.TFrame")
    content_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    # Make content frame responsive
    def update_frame_size(event=None):
        width = min(event.width - 20 if event else window.winfo_width() - 20, 1200)
        height = event.height - 20 if event else window.winfo_height() - 20
        content_frame.configure(width=width, height=height)
    
    bg.bind("<Configure>", update_frame_size)
    
    return window, content_frame

def open_text_to_voice():
    window, frame = create_modern_window("Text-to-Voice", "500x300")
    window.minsize(400, 250)
    
    # Configure frame to expand
    frame.pack(fill="both", expand=True, padx=0, pady=0)
    
    # Container for content
    content = ttk.Frame(frame, style="Custom.TFrame")
    content.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Title
    ttk.Label(content, 
              text="Text to Voice Converter", 
              style="Custom.TLabel",
              font=("Helvetica", 18, "bold")).pack(pady=(0, 20))
    
    # Input section
    ttk.Label(content, 
              text="Enter Text:", 
              style="Custom.TLabel",
              font=("Helvetica", 12)).pack(pady=(0, 5))
    
    text_input = ttk.Entry(content, 
                          width=40, 
                          font=("Helvetica", 12))
    text_input.pack(pady=(0, 20))
    text_input.focus()
    
    def convert_text():
        text = text_input.get()
        if text.strip():
            text_to_voice(text)
        else:
            messagebox.showwarning("Input Error", "Please enter some text.")
    
    # Convert button
    convert_btn = ttk.Button(content, 
                            text="Convert to Voice",
                            style="Custom.TButton", 
                            command=convert_text)
    convert_btn.pack(pady=10)

def open_youtube_downloader():
    window, frame = create_modern_window("YouTube Downloader", "500x450")
    window.minsize(400, 350)
    
    # Configure frame to expand
    frame.pack(fill="both", expand=True, padx=0, pady=0)
    
    # Container for content
    content = ttk.Frame(frame, style="Custom.TFrame")
    content.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Title
    ttk.Label(content, 
              text="YouTube Downloader", 
              style="Custom.TLabel",
              font=("Helvetica", 18, "bold")).pack(pady=(0, 20))
    
    # URL input section
    ttk.Label(content, 
              text="Enter YouTube URL:", 
              style="Custom.TLabel",
              font=("Helvetica", 12)).pack(pady=(0, 5))
    
    url_input = ttk.Entry(content, 
                         width=40, 
                         font=("Helvetica", 12))
    url_input.pack(pady=(0, 20))
    url_input.focus()
    
    # Download type selection
    download_type = tk.StringVar(value="video")
    
    type_frame = ttk.Frame(content, style="Custom.TFrame")
    type_frame.pack(pady=(0, 20))
    
    # Progress bar and status
    progress_var = tk.DoubleVar(value=0)
    progress_bar = ttk.Progressbar(content, 
                                 variable=progress_var,
                                 maximum=100,
                                 style="Custom.Horizontal.TProgressbar",
                                 length=300)
    
    status_label = ttk.Label(content,
                            text="Ready to download",
                            style="Custom.TLabel",
                            font=("Helvetica", 10))
    
    def update_progress(progress, speed=0):
        progress_var.set(progress)
        speed_mb = speed / 1024 / 1024 if speed else 0
        status_label.config(text=f"Downloading: {progress:.1f}% ({speed_mb:.1f} MB/s)")
        window.update()
    
    def start_download():
        url = url_input.get()
        if not url.strip():
            messagebox.showwarning("Input Error", "Please enter a YouTube URL.")
            return
        
        # Show progress bar and status
        progress_bar.pack(pady=(0, 5))
        status_label.pack(pady=(0, 10))
        
        # Disable input while downloading
        url_input.configure(state="disabled")
        download_btn.configure(state="disabled")
        
        try:
            result = download_youtube_video(url, download_type.get(), update_progress)
            progress_var.set(100)
            status_label.config(text="Download completed!")
            messagebox.showinfo("Success", result)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            # Re-enable input
            url_input.configure(state="normal")
            download_btn.configure(state="normal")
    
    # Style for progress bar
    style.configure("Custom.Horizontal.TProgressbar",
                   troughcolor="#1a1a2e",
                   background="#0f3460",
                   thickness=20)
    
    # Radio buttons
    ttk.Radiobutton(type_frame, 
                    text="Video", 
                    variable=download_type, 
                    value="video", 
                    style="Custom.TRadiobutton").pack(side="left", padx=10)
    
    ttk.Radiobutton(type_frame, 
                    text="Audio", 
                    variable=download_type, 
                    value="audio", 
                    style="Custom.TRadiobutton").pack(side="left", padx=10)
    
    # Download button
    download_btn = ttk.Button(content, 
                             text="Download",
                             style="Custom.TButton", 
                             command=start_download)
    download_btn.pack(pady=10)

# Function to open Weather Info window
def create_city_input_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("Enter City")
    dialog.geometry("400x200")
    dialog.configure(bg="#1a1a2e")
    
    bg = create_gradient_frame(dialog, "#1a1a2e", "#16213e")
    frame = ttk.Frame(bg, style="Custom.TFrame")
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    city_var = tk.StringVar()
    
    ttk.Label(frame, text="Enter City Name", style="Custom.TLabel", 
              font=("Helvetica", 14, "bold")).pack(pady=10)
    
    entry = ttk.Entry(frame, textvariable=city_var, width=30, 
                      font=("Helvetica", 12))
    entry.pack(pady=15)
    entry.focus()
    
    result = [None]
    
    def on_submit():
        result[0] = city_var.get()
        dialog.destroy()
        
    def on_cancel():
        dialog.destroy()
    
    btn_frame = ttk.Frame(frame, style="Custom.TFrame")
    btn_frame.pack(pady=15)
    
    ttk.Button(btn_frame, text="Search", style="Custom.TButton", 
               command=on_submit).pack(side="left", padx=10)
    ttk.Button(btn_frame, text="Cancel", style="Custom.TButton", 
               command=on_cancel).pack(side="left")
    
    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)
    
    return result[0]

def create_weather_card(parent, title, value, icon=None):
    card = ttk.Frame(parent, style="Weather.TFrame")
    card.pack(pady=10, padx=5, fill="x")
    
    if icon:
        ttk.Label(card, image=icon, style="Weather.TLabel").pack(side="left", padx=10)
    
    ttk.Label(card, text=title, style="WeatherTitle.TLabel", 
              font=("Helvetica", 12)).pack(side="left", padx=5)
    ttk.Label(card, text=value, style="WeatherValue.TLabel", 
              font=("Helvetica", 12, "bold")).pack(side="right", padx=10)
    
    return card

def open_weather_info():
    city = create_city_input_dialog()
    if not city:
        return

    weather_info = get_weather(city)
    if "City not found" in weather_info or not isinstance(weather_info, str):
        messagebox.showerror("Error", weather_info)
        return

    window, frame = create_modern_window("Weather Information", "800x600")
    window.minsize(600, 400)
    
    # Configure frame to expand
    frame.pack(fill="both", expand=True)
    
    # Parse weather data more reliably
    weather_data = {}
    for line in weather_info.split('\n'):
        if line.strip() and ":" in line:
            key, value = line.split(':', 1)
            weather_data[key.strip()] = value.strip()

    description = weather_data.get("Description", "").lower()
    
    # Configure styles with adjusted padding
    style.configure("Weather.TFrame", 
                   background="#1f2937", 
                   padding=5)  # Reduced padding
    style.configure("WeatherTitle.TLabel", 
                   background="#1f2937", 
                   foreground="#9ca3af",
                   font=("Helvetica", 12))
    style.configure("WeatherValue.TLabel", 
                   background="#1f2937", 
                   foreground="#ffffff",
                   font=("Helvetica", 12, "bold"))
    
    # Main container
    main_container = ttk.Frame(frame, style="Custom.TFrame")
    main_container.pack(fill="both", expand=True, padx=0, pady=0)  # Remove padding
    
    # Header frame
    header_frame = ttk.Frame(main_container, style="Custom.TFrame")
    header_frame.pack(fill="x", pady=(10, 5))  # Adjusted padding
    
    if description in weather_icon_images:
        icon_label = ttk.Label(header_frame, 
                             image=weather_icon_images[description],
                             background="#1a1a2e")
        icon_label.pack(pady=(5, 0))  # Adjusted padding
    
    ttk.Label(header_frame, 
             text=f"{city.title()}", 
             style="Custom.TLabel",
             font=("Helvetica", 24, "bold")).pack(pady=2)
    
    ttk.Label(header_frame,
             text=f"{weather_data.get('Temperature', '0')}",
             style="Custom.TLabel",
             font=("Helvetica", 36, "bold")).pack(pady=2)
    
    # Weather details section
    details_frame = ttk.Frame(main_container, style="Custom.TFrame")
    details_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    # Create columns with proper spacing
    left_frame = ttk.Frame(details_frame, style="Custom.TFrame")
    left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
    
    right_frame = ttk.Frame(details_frame, style="Custom.TFrame")
    right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
    
    # Add weather cards
    for frame, items in [(left_frame, [
        ("Feels Like", weather_data.get("Feels like", "N/A")),
        ("Humidity", weather_data.get("Humidity", "N/A")),
        ("Wind Speed", weather_data.get("Wind Speed", "N/A"))
    ]), (right_frame, [
        ("Pressure", weather_data.get("Pressure", "N/A")),
        ("Visibility", weather_data.get("Visibility", "N/A")),
        ("Description", description.title())
    ])]:
        for title, value in items:
            create_weather_card(frame, title, value)
    
    # Footer
    footer_frame = ttk.Frame(main_container, style="Custom.TFrame")
    footer_frame.pack(fill="x", pady=(5, 10))
    
    sunrise = weather_data.get('Sunrise', 'N/A')
    sunset = weather_data.get('Sunset', 'N/A')
    
    ttk.Label(footer_frame,
              text=f"Sunrise: {sunrise}  |  Sunset: {sunset}",
              style="Custom.TLabel",
              font=("Helvetica", 10)).pack()

# Update main buttons with modern styling
btn1 = ttk.Button(main_frame, text=" Text-to-Voice", 
                  image=wave_photo, compound="left", 
                  style="Custom.TButton", command=open_text_to_voice)
btn1.pack(pady=20)

btn2 = ttk.Button(main_frame, text=" Weather Info", 
                  image=cloud_photo, compound="left", 
                  style="Custom.TButton", command=open_weather_info)
btn2.pack(pady=20)

# Add a new button for YouTube Downloader
btn3 = ttk.Button(main_frame, text=" YouTube Downloader", 
                  image=youtube_photo, compound="left", 
                  style="Custom.TButton", command=open_youtube_downloader)
btn3.pack(pady=20)

# Modern styling for bottom frame
bottom_frame = ttk.Frame(root, style="Custom.TFrame")
bottom_frame.pack(side="bottom", fill="x", pady=20)
bottom_frame.lift()  # Ensure it stays on top of the gradient

details_label = ttk.Label(bottom_frame, 
                         text="Owner: Shariar Ahamed", 
                         style="Custom.TLabel")
details_label.pack(side="left", padx=20)

gmail_label = ttk.Label(bottom_frame, image=gmail_photo, background="#1a1a2e")
gmail_label.pack(side="left", padx=(5, 0))

email_label = ttk.Label(bottom_frame, text="www.saaulfy@gmail.com", font=("Arial", 10), foreground="lightblue", cursor="hand2", background="#1a1a2e")
email_label.pack(side="left", padx=(5, 10))

def open_email(event):
    import webbrowser
    webbrowser.open("mailto:www.saaulfy@gmail.com")

email_label.bind("<Button-1>", open_email)

# Start the GUI loop
root.mainloop()
