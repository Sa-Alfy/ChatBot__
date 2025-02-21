import tkinter as tk
from tkinter import ttk

class LoadingSpinner(tk.Canvas):
    def __init__(self, parent, size=30, width=4):
        super().__init__(parent, width=size, height=size, bg="#1a1a2e", highlightthickness=0)
        self.size = size
        self.angle = 0
        self.width = width
        self._draw_spinner()
        
    def _draw_spinner(self):
        self.delete("spinner")
        x = y = self.size // 2
        r = (self.size - self.width) // 2
        angle2 = self.angle + 90
        self.create_arc(self.width, self.width, self.size-self.width, self.size-self.width,
                       start=self.angle, extent=angle2,
                       width=self.width, style="arc",
                       outline="#e94560",
                       tags="spinner")
        self.angle = (self.angle + 10) % 360
        self.after(50, self._draw_spinner)

class ModernButton(ttk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style="Modern.TButton", **kwargs)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, e):
        self.configure(style="Modern.TButton.Hover")
    
    def _on_leave(self, e):
        self.configure(style="Modern.TButton")

class WeatherCard(ttk.Frame):
    def __init__(self, parent, title, value, icon=None, **kwargs):
        super().__init__(parent, style="Weather.TFrame", **kwargs)
        
        self.title = title
        self.value = value
        self.icon = icon
        
        self._create_widgets()
    
    def _create_widgets(self):
        if self.icon:
            ttk.Label(self, image=self.icon).pack(side="left", padx=5)
        
        ttk.Label(self, text=self.title,
                 style="WeatherTitle.TLabel").pack(side="left", padx=5)
        ttk.Label(self, text=self.value,
                 style="WeatherValue.TLabel").pack(side="right", padx=5)

class CitySearchBox(ttk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.placeholder = "Enter city name..."
        self._is_empty = True
        
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        
        self._show_placeholder()
    
    def _show_placeholder(self):
        if not self.get():
            self._is_empty = True
            self.insert(0, self.placeholder)
            self.configure(foreground="grey")
    
    def _on_focus_in(self, event):
        if self._is_empty:
            self.delete(0, "end")
            self.configure(foreground="white")
            self._is_empty = False
    
    def _on_focus_out(self, event):
        self._show_placeholder()
