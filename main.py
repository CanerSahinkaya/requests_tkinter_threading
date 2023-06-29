import requests
import tkinter as tk
from tkinter import ttk
import webbrowser
from PIL import Image, ImageTk
import threading


def get_universities():
    response = requests.get("http://universities.hipolabs.com/search?country=United+States")
    if response.status_code == 200:
        return response.json()


def search_university():
    result_label.config(text="")
    thread = threading.Thread(target=find_universities)
    thread.start()


def find_universities():
    university_response = get_universities()
    user_input = entry_uni.get()
    found_universities = []
    for university in university_response:
        if university["name"] == user_input:
            if university["web_pages"]:
                found_universities.extend(university["web_pages"])
                break
    if found_universities:
        wn.after(0, update_result_label, found_universities[0])


def update_result_label(url):
    result_label.config(text=url)
    result_label.bind("<Button-1>", lambda event: open_url(url))
    result_label.config(foreground="blue", font=("Arial", 12))


def open_url(url):
    webbrowser.open(url)


wn = tk.Tk()
wn.title("University Search")
wn.minsize(width=300, height=200)
img = Image.open("USDE.png")
usde_img = ImageTk.PhotoImage(img)
label_img = ttk.Label(image=usde_img)
label_img.pack()
label_uni = ttk.Label(wn, text="Enter your university name", font=("Arial", 14, "normal"))
label_uni.pack()
entry_uni = ttk.Entry(wn, width=30)
entry_uni.pack()
button_uni = ttk.Button(wn, text="Search", command=search_university, width=25)
button_uni.pack()
result_label = ttk.Label(wn, text="")
result_label.pack()

wn.mainloop()