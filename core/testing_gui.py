import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkbs
from ttkbootstrap.constants import *


def show_waiting_state():
    waiting_frame.pack()
    loading_frame.pack_forget()
    data_frame.pack_forget()


def show_loading_state():
    waiting_frame.pack_forget()
    loading_frame.pack()
    data_frame.pack_forget()


def show_data_state():
    waiting_frame.pack_forget()
    loading_frame.pack_forget()
    data_frame.pack()


def start_search():
    # Simulating a search or loading process
    # Replace this with your actual code to gather data
    show_loading_state()
    # Simulated delay (replace with actual data loading process)
    root.after(3000, show_data_state)  # After 3 seconds, show data


root = ttkbs.Window(themename='darkly')
root.title("Emperor Eye")
root.geometry('600x500')
root.resizable(False, False)
root.iconbitmap('core\dd.ico')

# Frames for different states
waiting_frame = tk.Frame(root)
loading_frame = tk.Frame(root)
data_frame = tk.Frame(root)

# Widgets for waiting state
waiting_title = ttkbs.Label(
    waiting_frame,  text="Emperor Eye", font='Arial 24 bold')
waiting_title.pack(pady=10)
waiting_label1 = ttkbs.Label(
    waiting_frame, text='Unveils the hidden names of teammates', font='Arial 10')
waiting_label1.pack(pady=0)
waiting_label2 = ttkbs.Label(
    waiting_frame, text='and lessens the chances of playing with elo terrorist', font='Arial 10')
waiting_label2.pack(pady=0)

waiting_label = ttk.Label(
    waiting_frame, text='Not in champ select. Waiting for game...', font='Helvetica 12')
waiting_label.pack(pady=100)
start_button = ttk.Button(
    waiting_frame, text='Start Search', command=start_search)
start_button.pack(pady=10)

# Widgets for loading state
loading_title = ttkbs.Label(
    loading_frame,  text="Emperor Eye", font='Arial 24 bold')
loading_title.pack(pady=10)
loading_lable1 = ttkbs.Label(
    loading_frame, text='Unveils the hidden names of teammates', font='Arial 10')
loading_lable1.pack(pady=0)
loading_lable2 = ttkbs.Label(
    loading_frame, text='and lessens the chances of playing with elo terrorist', font='Arial 10')
loading_lable2.pack(pady=0)

loading_lable3 = ttk.Label(
    loading_frame, text='Found Lobby, Gathering Data.', font='Helvetica 12')
loading_lable3.pack(pady=100)


my_progress = ttkbs.Progressbar(
    loading_frame, bootstyle='default', maximum=100, mode='indeterminate', length=200, value=0)
my_progress.pack(pady=10)
my_progress.start()


# Widgets for data state (display the gathered data)
data_title = ttkbs.Label(
    data_frame,  text="Emperor Eye", font='Arial 24 bold')
data_title.pack(pady=10)

data_label = ttk.Label(
    data_frame, text='Lobby Found!', font='Helvetica 12')
data_label.pack(pady=0)

# Combobox
data_combox = ttkbs.Combobox(data_frame, values=[
                             'OP.GG', 'U.GG', 'TRACKER.GG', 'LEAGUE OF GRAPHS', 'LOLALYTICS', 'PORO.GG'], state='readonly')
data_combox.pack(pady=10)
data_combox.current(0)

# Make 5 Buttons
data1 = ttk.Button(data_frame, text="Kaiser",
                   command=lambda: on_data_button_click(1))
data1.pack(pady=5)

data2 = ttk.Button(data_frame, text="Player 2",
                   command=lambda: on_data_button_click(2))
data2.pack(pady=5)

data3 = ttk.Button(data_frame, text="Player 3",
                   command=lambda: on_data_button_click(3))
data3.pack(pady=5)

data4 = ttk.Button(data_frame, text="Player 4",
                   command=lambda: on_data_button_click(4))
data4.pack(pady=5)

data5 = ttk.Button(data_frame, text="Player 5",
                   command=lambda: on_data_button_click(5))
data5.pack(pady=5)

# Initially show the waiting state
show_waiting_state()

root.mainloop()
