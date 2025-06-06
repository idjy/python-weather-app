
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

def update_weather():
    city = DEFAULT_CITY
    country = DEFAULT_COUNTRY
    weather = get_weather(city, country)

    if weather.get("cod") != 200:
        temp_label.config(text="Error loading weather.")
        return

    temp = weather["main"]["temp"]
    desc = weather["weather"][0]["description"].capitalize()
    icon_id = weather["weather"][0]["icon"]
    city_name = weather["name"]

    temp_label.config(text=f"{city_name} | {temp}°C", font=("Arial", 20, "bold"))
    desc_label.config(text=desc, font=("Arial", 14))

    # Download icon
    icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    icon_response = requests.get(icon_url)
    img_data = icon_response.content
    img = Image.open(BytesIO(img_data))
    img = img.resize((100, 100))
    photo = ImageTk.PhotoImage(img)

    icon_label.config(image=photo)
    icon_label.image = photo

# UI
root = tk.Tk()
root.title("Weather App")
root.geometry("300x400")
root.resizable(False, False)

frame = tk.Frame(root, bg="#cce7ff")
frame.pack(fill="both", expand=True)

temp_label = tk.Label(frame, text="Loading...", bg="#cce7ff")
temp_label.pack(pady=(40, 10))

icon_label = tk.Label(frame, bg="#cce7ff")
icon_label.pack(pady=5)

desc_label = tk.Label(frame, text="", bg="#cce7ff")
desc_label.pack(pady=(5, 20))

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