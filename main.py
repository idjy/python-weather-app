import tkinter as tk
import requests
from datetime import datetime
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = "your_openweathermap_api_key" 
DEFAULT_CITY = "Karbala"
DEFAULT_COUNTRY = "IQ"

def get_weather(city, country):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def get_uv_index(lat, lon):
    onecall_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily,alerts&appid={API_KEY}&units=metric"
    response = requests.get(onecall_url)
    data = response.json()
    return data["current"].get("uvi", "N/A")

def load_icon(path):
    img = Image.open(path)
    img = img.resize((20, 20), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

def create_icon_label(parent, icon, text):
    frame = tk.Frame(parent, bg="#cce7ff")
    label_icon = tk.Label(frame, image=icon, bg="#cce7ff")
    label_icon.pack(side="left", padx=(0,5))
    label_text = tk.Label(frame, text=text, bg="#cce7ff", font=("Arial", 12))
    label_text.pack(side="left")
    frame.pack(pady=2, anchor="w")
    return label_text

def update_weather():
    city = DEFAULT_CITY
    country = DEFAULT_COUNTRY
    weather = get_weather(city, country)

    if weather.get("cod") != 200:
        temp_label.config(text="Error loading weather.")
        desc_label.config(text="")
        icon_label.config(image="")
        humidity_label.config(text="")
        wind_label.config(text="")
        uv_label.config(text="")
        return

    temp = weather["main"]["temp"]
    desc = weather["weather"][0]["description"].capitalize()
    icon_id = weather["weather"][0]["icon"]
    city_name = weather["name"]

    humidity = weather["main"]["humidity"]
    wind_speed = weather["wind"]["speed"]

    lat = weather["coord"]["lat"]
    lon = weather["coord"]["lon"]
    uv_index = get_uv_index(lat, lon)

    temp_label.config(text=f"{city_name} | {temp}°C", font=("Arial", 20, "bold"))
    desc_label.config(text=desc, font=("Arial", 14))

    # Download main weather icon
    icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    icon_response = requests.get(icon_url)
    img_data = icon_response.content
    img = Image.open(BytesIO(img_data))
    img = img.resize((100, 100))
    photo = ImageTk.PhotoImage(img)

    icon_label.config(image=photo)
    icon_label.image = photo

    # Update new info labels
    humidity_label.config(text=f"Humidity: {humidity}%")
    wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
    uv_label.config(text=f"UV Index: {uv_index}")

# UI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("320x460")
root.resizable(False, False)

frame = tk.Frame(root, bg="#cce7ff")
frame.pack(fill="both", expand=True)

temp_label = tk.Label(frame, text="Loading...", bg="#cce7ff")
temp_label.pack(pady=(40, 10))

icon_label = tk.Label(frame, bg="#cce7ff")
icon_label.pack(pady=5)

desc_label = tk.Label(frame, text="", bg="#cce7ff")
desc_label.pack(pady=(5, 20))

# Load icons for new info
humidity_icon = load_icon("icons/humidity.png")
wind_icon = load_icon("icons/wind.png")
uv_icon = load_icon("icons/uv.png")

# Create labels with icons for humidity, wind, uv
humidity_label = create_icon_label(frame, humidity_icon, "")
wind_label = create_icon_label(frame, wind_icon, "")
uv_label = create_icon_label(frame, uv_icon, "")

last_update = tk.Label(frame, text="", font=("Arial", 8), bg="#cce7ff", fg="#444")
last_update.pack(side="bottom", pady=5)

def refresh():
    update_weather()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last_update.config(text=f"Last update: {now}")

refresh()

refresh_btn = tk.Button(frame, text="🔄 Refresh", command=refresh)
refresh_btn.pack(pady=10)

root.mainloop()
