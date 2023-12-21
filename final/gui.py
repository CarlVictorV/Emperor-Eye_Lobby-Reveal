import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkbs
from ttkbootstrap.constants import *

# from bare import connector, on_name_arr_updated

from linkmaker import multi_search, single_search
from data import data_container

def run_gui(nameArrz):

    def show_data_state():
        data_frame.pack()

    def on_data_single_click(name, selected_option):
        # Create a link and open it in the web browser
        link_creator = single_search(name)
        if selected_option == 'OP.GG':
            link_creator.open_link(link_creator.opgg)
        elif selected_option == 'U.GG':
            link_creator.open_link(link_creator.ugg)
        elif selected_option == 'TRACKER.GG':
            link_creator.open_link(link_creator.tracker)
        elif selected_option == 'LEAGUE OF GRAPHS':
            link_creator.open_link(link_creator.leagueofgraphs)
        elif selected_option == 'LOLALYTICS':
            link_creator.open_link(link_creator.lolalytics)
        elif selected_option == 'PORO.GG':
            link_creator.open_link(link_creator.porogg)
        # Add more conditions for other options if needed

    def update_ui_with_name_arr(names):
        # Update your UI components with the new data
        print("Updating UI with nameArr:", names)
        
        for name in names:
            # Create a button for each name
            button = ttk.Button(data_frame, text=name, command=lambda name=name: on_data_single_click(name, data_combox.get()))
            button.pack(pady=5)

    def update_ui_multi(names):
        multi_search_button = ttk.Button(data_frame, text='Multi-Search', command=lambda: on_data_multi_click(names, data_combox1.get()))
        multi_search_button.pack(pady=10)

    def on_data_multi_click(names, selected_option):
        selected_option = data_combox1.get()
        link_creator = multi_search(names)
        
        if selected_option == 'OP.GG':
            link_creator.open_link(link_creator.opgg)
        elif selected_option == 'U.GG':
            link_creator.open_link(link_creator.ugg)

    root = ttkbs.Window(themename='darkly')
    root.title("Emperor Eye")
    root.geometry('600x800')
    root.resizable(True, True)
    root.iconbitmap('final\dd.ico')

    # Frames for different states
    data_frame = tk.Frame(root)


    # Widgets for data state (display the gathered data)
    data_title = ttkbs.Label(
        data_frame,  text="Emperor Eye", font='Arial 24 bold')
    data_title.pack(pady=10)

    data_label = ttk.Label(
        data_frame, text='Lobby Found!', font='Helvetica 12')
    data_label.pack(pady=0)

    space_label = ttk.Label(data_frame, text='', font='Helvetica 12')
    space_label.pack(pady=10)

    data_label1 = ttk.Label(
        data_frame, text='Multi Search', font='Helvetica 12')
    data_label1.pack(pady=5)

    data_combox1 = ttkbs.Combobox(data_frame, values=[
                                'OP.GG', 'U.GG'], state='readonly')
    data_combox1.pack(pady=10)
    data_combox1.current(0)
    # Combobox
    
    update_ui_multi(data_container.updated_test())

    space_label1 = ttk.Label(data_frame, text='', font='Helvetica 12')
    space_label1.pack(pady=5)

    data_label2 = ttk.Label(
        data_frame, text='Single Search', font='Helvetica 12')
    data_label2.pack(pady=5)

    data_combox = ttkbs.Combobox(data_frame, values=[
                                'OP.GG', 'U.GG', 'TRACKER.GG', 'LEAGUE OF GRAPHS', 'LOLALYTICS', 'PORO.GG'], state='readonly')
    data_combox.pack(pady=10)
    data_combox.current(0)


    # Initially show the waiting state
    show_data_state()

    update_ui_with_name_arr(data_container.updated_test())
    data_container.clear()
    root.mainloop()
    
if __name__ == "__main__":
    run_gui()