import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkbs
from ttkbootstrap.constants import *
# from bare import connector, on_name_arr_updated
from linkmaker import multi_search


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

def on_data_button_click(name, selected_option):
    # Create a link and open it in the web browser
    link_creator = multi_search([name])
    if selected_option == 'OP.GG':
        link_creator.open_link(link_creator.opgg)
    elif selected_option == 'U.GG':
        link_creator.open_link(link_creator.ugg)
    # Add more conditions for other options if needed

def update_ui_with_name_arr(names):
    # Update your UI components with the new data
    print("Updating UI with nameArr:", names)

    for name in names:
        # Create a button for each name
        button = ttk.Button(data_frame, text=name, command=lambda name=name: on_data_button_click(name, data_combox.get()))
        button.pack(pady=5)


root = ttkbs.Window(themename='darkly')
root.title("Emperor Eye")
root.geometry('600x500')
root.resizable(True, True)
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



# Initially show the waiting state
show_waiting_state()
update_ui_with_name_arr(["KaiserV#GOW", "Mikado#Khan", "Aim and Miss#BOBO", "AustinReaves15#AR15", "Daryl#LIGO"])
root.mainloop()