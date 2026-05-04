import tkinter as tk
from tkinter import ttk
import requests

MOISTURE_CHANNEL_ID = "KPY9Y27J2Q9O3CCK"
TURBIDITY_CHANNEL_ID = "7ZE9CBK4GJC7ANTQ"
TEMP_CHANNEL_ID = "GXY7HKM8Z9NVQMNR"
HUMIDITY_CHANNEL_ID = "4ELRIDMF0K7W4XCQ"

MOISTURE_READ_KEY = ""
TURBIDITY_READ_KEY = ""
TEMP_READ_KEY = ""
HUMIDITY_READ_KEY = ""


def get_channel_data(channel_id, read_key):
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?results=1"

    if read_key != "":
        url += "&api_key=" + read_key

    response = requests.get(url, timeout=5)
    data = response.json()
    return data["feeds"][-1]


def update_gui():
    try:
        moisture = get_channel_data(MOISTURE_CHANNEL_ID, MOISTURE_READ_KEY)
        turbidity = get_channel_data(TURBIDITY_CHANNEL_ID, TURBIDITY_READ_KEY)
        temp = get_channel_data(TEMP_CHANNEL_ID, TEMP_READ_KEY)
        humidity = get_channel_data(HUMIDITY_CHANNEL_ID, HUMIDITY_READ_KEY)

        channels = [moisture, turbidity, temp, humidity]
        label_groups = [moisture_labels, turbidity_labels, temp_labels, humidity_labels]

        for channel_data, labels in zip(channels, label_groups):
            for i in range(8):
                value = channel_data.get("field" + str(i + 1))
                if value is None:
                    value = "--"
                labels[i].config(text=value)

        status_label.config(text="System updated successfully", foreground="#2e7d32")

    except Exception:
        status_label.config(text="Error reading ThingSpeak data", foreground="#c62828")

    root.after(15000, update_gui)


def create_card(parent, title, unit):
    card = tk.Frame(parent, bg="white", padx=15, pady=15)
    card.pack(side="left", padx=12, pady=10, fill="both", expand=True)

    title_label = tk.Label(
        card,
        text=title,
        font=("Arial", 15, "bold"),
        bg="white",
        fg="#1f2937"
    )
    title_label.pack(pady=(0, 10))

    labels = []

    for i in range(8):
        row = tk.Frame(card, bg="white")
        row.pack(fill="x", pady=3)

        step_label = tk.Label(
            row,
            text=str((i + 1) * 100) + " readings",
            font=("Arial", 10),
            bg="white",
            fg="#6b7280",
            width=12,
            anchor="w"
        )
        step_label.pack(side="left")

        value_label = tk.Label(
            row,
            text="--",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#111827",
            width=8,
            anchor="e"
        )
        value_label.pack(side="right")

        unit_label = tk.Label(
            row,
            text=unit,
            font=("Arial", 10),
            bg="white",
            fg="#6b7280",
            width=4,
            anchor="w"
        )
        unit_label.pack(side="right")

        labels.append(value_label)

    return labels


root = tk.Tk()
root.title("Smart Water Monitoring Prediction Viewer")
root.geometry("1000x520")
root.configure(bg="#f3f4f6")

style = ttk.Style()
style.theme_use("clam")

header = tk.Frame(root, bg="#1e3a8a", pady=18)
header.pack(fill="x")

title = tk.Label(
    header,
    text="Smart Water Monitoring System",
    font=("Arial", 22, "bold"),
    bg="#1e3a8a",
    fg="white"
)
title.pack()

subtitle = tk.Label(
    header,
    text="Prediction Results from 100 to 800 Readings",
    font=("Arial", 12),
    bg="#1e3a8a",
    fg="#dbeafe"
)
subtitle.pack(pady=(5, 0))

main_frame = tk.Frame(root, bg="#f3f4f6")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

moisture_labels = create_card(main_frame, "Moisture", "%")
turbidity_labels = create_card(main_frame, "Turbidity", "%")
temp_labels = create_card(main_frame, "Temperature", "°C")
humidity_labels = create_card(main_frame, "Humidity", "%")

footer = tk.Frame(root, bg="#f3f4f6")
footer.pack(fill="x", pady=(0, 15))

status_label = tk.Label(
    footer,
    text="Updating every 15 seconds",
    font=("Arial", 11),
    bg="#f3f4f6",
    fg="#374151"
)
status_label.pack()

update_gui()
root.mainloop()