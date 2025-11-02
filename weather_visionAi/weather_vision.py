#!/usr/bin/env python3
"""
Weather Vision - Single file app with dynamic UI based on weather
Features:
- Minimal tkinter GUI
- Fetch weather via Open-Meteo (no API key) based on city name (geo via Nominatim)
- Dynamic UI colors/icons/layout depending on weather code and temperature
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
import json
import urllib.parse
import urllib.request

# Mapping of WMO weather codes to conditions
WMO_MAP = {
    0: ("Clear sky", "sunny"),
    1: ("Mainly clear", "sunny"),
    2: ("Partly cloudy", "cloudy"),
    3: ("Overcast", "cloudy"),
    45: ("Fog", "fog"), 48: ("Depositing rime fog", "fog"),
    51: ("Light drizzle", "rain"), 53: ("Moderate drizzle", "rain"), 55: ("Dense drizzle", "rain"),
    56: ("Light freezing drizzle", "rain"), 57: ("Dense freezing drizzle", "rain"),
    61: ("Slight rain", "rain"), 63: ("Moderate rain", "rain"), 65: ("Heavy rain", "rain"),
    66: ("Light freezing rain", "rain"), 67: ("Heavy freezing rain", "rain"),
    71: ("Slight snow fall", "snow"), 73: ("Moderate snow fall", "snow"), 75: ("Heavy snow fall", "snow"),
    77: ("Snow grains", "snow"),
    80: ("Slight rain showers", "rain"), 81: ("Moderate rain showers", "rain"), 82: ("Violent rain showers", "rain"),
    85: ("Slight snow showers", "snow"), 86: ("Heavy snow showers", "snow"),
    95: ("Thunderstorm", "storm"), 96: ("Thunderstorm with slight hail", "storm"), 99: ("Thunderstorm with heavy hail", "storm"),
}

THEMES = {
    "sunny": {"bg": "#FFF8DC", "fg": "#C97F00", "accent": "#FFD54F", "icon": "☀️"},
    "cloudy": {"bg": "#ECEFF1", "fg": "#455A64", "accent": "#B0BEC5", "icon": "☁️"},
    "rain": {"bg": "#E3F2FD", "fg": "#1565C0", "accent": "#90CAF9", "icon": "🌧️"},
    "snow": {"bg": "#F0F4FF", "fg": "#1E3A8A", "accent": "#93C5FD", "icon": "❄️"},
    "storm": {"bg": "#ECE7F6", "fg": "#4A148C", "accent": "#B39DDB", "icon": "⛈️"},
    "fog":   {"bg": "#F5F5F5", "fg": "#616161", "accent": "#BDBDBD", "icon": "🌫️"},
    "default": {"bg": "#FFFFFF", "fg": "#333333", "accent": "#E0E0E0", "icon": "🌡️"},
}

class WeatherClient:
    def geocode(self, city):
        url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
            "q": city, "format": "json", "limit": 1
        })
        req = urllib.request.Request(url, headers={"User-Agent": "WeatherVision/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8"))
        if not data:
            raise ValueError("City not found")
        return float(data[0]["lat"]), float(data[0]["lon"]), data[0].get("display_name", city)

    def get_weather(self, lat, lon):
        url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode({
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "weather_code", "relative_humidity_2m", "wind_speed_10m"],
            "timezone": "auto"
        }, doseq=True)
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8"))
        current = data.get("current", {})
        return {
            "temp": current.get("temperature_2m"),
            "code": current.get("weather_code"),
            "humidity": current.get("relative_humidity_2m"),
            "wind": current.get("wind_speed_10m"),
        }

class WeatherVisionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Vision AI")
        self.root.geometry("720x520")
        self.client = WeatherClient()
        self.style = ttk.Style()

        self.build_ui()
        self.apply_theme("default")

    def build_ui(self):
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill=tk.X)

        self.city_var = tk.StringVar()
        ttk.Label(top, text="City:").pack(side=tk.LEFT)
        self.city_entry = ttk.Entry(top, textvariable=self.city_var, width=30)
        self.city_entry.pack(side=tk.LEFT, padx=6)
        ttk.Button(top, text="Get Weather", command=self.fetch).pack(side=tk.LEFT)

        self.icon_label = ttk.Label(top, text="🌡️", font=("Segoe UI Emoji", 28))
        self.icon_label.pack(side=tk.RIGHT)

        self.summary = ttk.Label(self.root, text="Enter a city to get started", font=("Arial", 14))
        self.summary.pack(pady=6)

        cards = ttk.Frame(self.root, padding=10)
        cards.pack(fill=tk.BOTH, expand=True)

        self.temp_lbl = ttk.Label(cards, text="Temp: -", font=("Arial", 18, "bold"))
        self.temp_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.cond_lbl = ttk.Label(cards, text="Condition: -")
        self.cond_lbl.grid(row=1, column=0, padx=10, pady=4, sticky="w")

        self.hum_lbl = ttk.Label(cards, text="Humidity: -")
        self.hum_lbl.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.wind_lbl = ttk.Label(cards, text="Wind: -")
        self.wind_lbl.grid(row=1, column=1, padx=10, pady=4, sticky="w")

        self.status = ttk.Label(self.root, text="Ready", anchor="w")
        self.status.pack(fill=tk.X, side=tk.BOTTOM, padx=6, pady=4)

    def apply_theme(self, key):
        theme = THEMES.get(key, THEMES["default"])
        bg = theme["bg"]; fg = theme["fg"]; accent = theme["accent"]
        self.root.configure(bg=bg)
        for w in self.root.winfo_children():
            try:
                w.configure(style="TFrame")
            except tk.TclError:
                pass
            try:
                w.configure(background=bg)
            except tk.TclError:
                pass
        self.summary.configure(background=bg, foreground=fg)
        self.status.configure(background=bg, foreground=fg)
        self.temp_lbl.configure(background=bg, foreground=fg)
        self.cond_lbl.configure(background=bg, foreground=fg)
        self.hum_lbl.configure(background=bg, foreground=fg)
        self.wind_lbl.configure(background=bg, foreground=fg)
        self.icon_label.configure(background=bg)
        self.icon_label.configure(text=theme["icon"])        

        # window accent (title hint using emoji already), could add border colors in frames if using custom ttk themes

    def pick_theme_key(self, code, temp_c):
        kind = WMO_MAP.get(code, ("Unknown", "default"))[1]
        # Adjust sunny vs hot (add heat theme via layout tweak)
        if kind == "sunny" and temp_c is not None and temp_c >= 32:
            return "sunny"  # keep sunny palette; we will add heat badge in summary
        return kind

    def fetch(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Input required", "Please enter a city name")
            return
        self.status.config(text="Fetching...")
        self.root.update_idletasks()
        try:
            lat, lon, display = self.client.geocode(city)
            data = self.client.get_weather(lat, lon)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch weather: {e}")
            self.status.config(text="Error")
            return

        code = data.get("code")
        temp = data.get("temp")
        humidity = data.get("humidity")
        wind = data.get("wind")

        condition, kind = WMO_MAP.get(code, ("Unknown", "default"))
        theme_key = self.pick_theme_key(code, temp)
        self.apply_theme(theme_key)

        heat_badge = " 🔥" if temp is not None and temp >= 32 else ""
        cold_badge = " 🧊" if temp is not None and temp <= 0 else ""

        self.summary.config(text=f"{display}\n{condition}")
        self.temp_lbl.config(text=f"Temp: {temp:.1f}°C{heat_badge}{cold_badge}" if temp is not None else "Temp: -")
        self.cond_lbl.config(text=f"Condition: {condition} (code {code})")
        self.hum_lbl.config(text=f"Humidity: {humidity}%" if humidity is not None else "Humidity: -")
        self.wind_lbl.config(text=f"Wind: {wind} km/h" if wind is not None else "Wind: -")

        # Layout adaptation: if rain/snow, stack labels to emphasize alerts
        if theme_key in ("rain", "snow", "storm"):
            # grid to stacked layout
            self.temp_lbl.grid_configure(row=0, column=0, sticky="w")
            self.cond_lbl.grid_configure(row=1, column=0, sticky="w")
            self.hum_lbl.grid_configure(row=2, column=0, sticky="w")
            self.wind_lbl.grid_configure(row=3, column=0, sticky="w")
        else:
            # two-column layout
            self.temp_lbl.grid_configure(row=0, column=0, sticky="w")
            self.cond_lbl.grid_configure(row=1, column=0, sticky="w")
            self.hum_lbl.grid_configure(row=0, column=1, sticky="w")
            self.wind_lbl.grid_configure(row=1, column=1, sticky="w")

        self.status.config(text="Updated")


def main():
    root = tk.Tk()
    app = WeatherVisionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
