import json
import requests
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import os.path



class Program:

    def __init__(self, window):

        main_frame = tk.Frame(window)
        main_frame.pack()
        
        

        self.file_name = tk.StringVar()
        self.file_name.set('')

        self.info_text = tk.StringVar()
        self.info_text.set('')

        self.lb_oracle_cards_filename = tk.Label(window, text = 'oracle-cards.json: ')
        self.lb_oracle_cards_filename.place(x=20, y=50)

        self.entry_filename = tk.Entry(window, state= tk.DISABLED, textvariable= self.file_name, bd = 2, width= 32, background = 'white')
        self.entry_filename.place(x=130, y=50)

        self.bt_browse = tk.Button(window, text= 'browse', command=self.load_json)
        self.bt_browse.place(x=370, y=45)

        self.data = tk.StringVar()

        self.bt_update = tk.Button(window, text = 'Download DB', command=self.popup_window)
        self.bt_update.place(x=450, y=45)

        self.entry_input_setname = tk.Entry(window, text = "Setname", bd = 2, width = 5)
        self.entry_input_setname.place(x=130,y=100)

        self.lb_input_setname = tk.Label(window, text = 'Set Code = ')
        self.lb_input_setname.place(x=20, y=100)

        self.bt_get_set = tk.Button(window, text = 'Get Set', command=self.get_set)
        self.bt_get_set.place(x=370, y=95)

        self.lb_info = tk.Label(window, text = 'Info: ')
        self.lb_info.place(x=20, y=150)

        self.entry_info = tk.Entry(window, state= tk.DISABLED, textvariable= self.info_text, bd = 2, width= 32, background = 'white')
        self.entry_info.place(x=130, y=150)

        self.bt_clear_info = tk.Button(window, text='clear', command=self.clear_info)
        self.bt_clear_info.place(x=370, y=145)

        window.geometry('640x260+20+20')
        window.title('mtg set extractor')
        window.mainloop()

    def clear_info(self):
        self.info_text.set('')

    def get_set(self):

        set_name = str(self.entry_input_setname.get()).lower()

        try:

            filtered_data = set_filter(self.data, set_name)

            output_cards(filtered_data, set_name)

            if len(filtered_data) > 0:

                info_string = "Success! Got " + set_name
        
            else:

                info_string = "Error: " + set_name + " does not exist"
        except:

            info_string = "Error: No DB loaded"

        self.info_text.set(info_string)

    def load_json(self):

        file = tk.filedialog.askopenfile(mode='r', filetypes=[('JSON Files', '*.json')])
   
        if file:
            self.file_name.set(str(file).split('\'')[1])
            self.data = json.load(file)
            file.close()

            self.info_text.set('JSON loaded successfully')
            
        else:
            self.data = None

        


    def popup_window(self):
        new_popup = Popup(tk.Tk())


class Popup:

    def __init__(self, window):

        main_frame = tk.Frame(window)
        main_frame.pack()

        self.lb_info = tk.Label(window, text = 'About to download oracle-cards.json (about 120mb)')
        self.lb_info_cont = tk.Label(window, text = '(App will appear frozen while downloading)')
        self.lb_info_2 = tk.Label(window, text = 'Are you sure?')

        self.lb_info.place(x=50, y=20)
        self.lb_info_cont.place(x=50, y=40)
        self.lb_info_2.place(x=50, y=70)

        self.bt_yes = tk.Button(window, text = 'Yes', command= lambda: [window.destroy(), self.download()])
        self.bt_yes.place(x=120, y=120)

        self.bt_no = tk.Button(window, text = 'No', command=window.destroy)
        self.bt_no.place(x=200, y=120)

        window.geometry('400x200+60+60')
        window.title('Download Oracle cards')
        window.mainloop()


    def download(self):

        r = download_oracle_cards()
        if r == 1:

            error_popup = Error(tk.Tk())

        else:
            complete_message = Complete(tk.Tk())

        

class Message:

    def __init__(self, window):

        main_frame = tk.Frame(window)
        main_frame.pack()
        

        self.bt_close = tk.Button(window, text = 'Close', command= window.destroy)
        self.bt_close.place(x=75, y=100)


        window.geometry('200x150+60+60')
        window.title('Alert')
        

class Complete(Message):

    def __init__(self, window):

        super().__init__(window)

        self.lb_message = tk.Label(window, text = 'Download Complete')
        self.lb_message.place(x=50, y=50)

        window.mainloop()

class Download(Message):

    def __init__(self, window):

        super().__init__(window)

        self.lb_message = tk.Label(window, text = 'Downloading...')
        self.lb_message.place(x=50, y=50)

        self.bt_close.destroy()

        window.mainloop()

class Error(Message):

    def __init__(self, window):

        super().__init__(window)

        self.lb_message = tk.Label(window, text = 'An Error Occured...')
        self.lb_message.place(x=50, y=50)

        window.mainloop()

def open_file():

    file = tk.filedialog.askopenfile(mode='r', filetypes=[('JSON Files', '*.json')])
   
    if file:

        data = json.load(file)
        file.close()
        return(data)
    else:
        return(1)


def download_oracle_cards():

    headers = {'Accept': 'application/json'}
    
    try:
        r = requests.get('https://api.scryfall.com/bulk-data', headers=headers)

        if str(r) == '<Response [200]>':

            #print(str(r))

            data = r.json()['data']

            url = ''

            for item in data:
                if item['type'] == 'oracle_cards':
                    url = item['download_uri']
    
            r2 = requests.get(url, headers = headers)
            if str(r2) == '<Response [200]>':

                oracle_cards = r2.json()

   

                with open("oracle-cards.json", "w") as outfile:
                   json.dump(oracle_cards, outfile)
                outfile.close()

                return(r)
            else:
                return(1)
        else:
            return(1)

    except:
        return(1)

    

def open_data(dataname):

    with open(dataname, encoding='utf-8') as f:
        data = json.load(f)

    f.close()

    return(data)


def set_filter(data, setname):

    filtered_list = []

    for card in data:

        if card['set'] == setname:

            filtered_list.append(card)

    return(filtered_list)

def output_cards(data, filename='output'):
    
    filename += '.txt'
    directory = './output/'
    if not os.path.isdir(directory):
        os.mkdir(directory)
    file_path = os.path.join(directory, filename)

    output_file = open(file_path, 'w')

    try:

        for card in data:

            string = card["name"] + '\n'
            output_file.write(string)

    except:
        print('there was an error')
        pass

    output_file.close()

#================================================================================

app = Program(tk.Tk())


