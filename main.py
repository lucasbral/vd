import tkinter
from PIL import Image
from tkinter import filedialog
import customtkinter
from pytube import YouTube
import os
import requests

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("YouTube Video Downloader")
        self.geometry(f"{800}x{300}")
        self.minsize(800,300)
        self.maxsize(1000,800)
        self.iconbitmap(resource_path("icon.ico"))
        

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3, 4), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=0)

        
        self.folder_selected = customtkinter.StringVar()
        self.titulo = customtkinter.StringVar()
        self.folder_selected.set(self.get_download_path())
        self.pasta = self.get_download_path()

        self.img = customtkinter.CTkImage(light_image=Image.open(resource_path("default.png")),
                                  dark_image=Image.open(resource_path("default.png")),
                                  size=(150, 150))

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Configurações", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=5, pady=(0, 0))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Pasta de Download:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=10, pady=(30, 0))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, textvariable=self.folder_selected, anchor="w")
        self.appearance_mode_label.grid(row=2, column=0, padx=10, pady=(0, 0))
        self.buttom_1 = customtkinter.CTkButton(self.sidebar_frame,text="Mudar Diretório",command=self.diretorio)
        self.buttom_1.grid(row=3, column=0, padx=5, pady=(0, 0))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Tema:", anchor="w")
        self.appearance_mode_label.grid(row=4, column=0, padx=10, pady=(0, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System", "Dark", "Light"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=5, column=0, padx=5, pady=(0, 0))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Fonte:", anchor="w")
        self.scaling_label.grid(row=6, column=0, padx=10, pady=(0, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=7, column=0, padx=5, pady=(0, 10))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Link do Vídeo")
        self.entry.grid(row=0, column=1, padx=(5, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),text="Download",command=self.button_callback)
        self.main_button_1.grid(row=0, column=3, padx=(5, 20), pady=(20, 20), sticky="nsew")

        self.titulo_frame = customtkinter.CTkLabel(master=self, textvariable=self.titulo, text="Video Title")
        self.titulo_frame.grid(row=1, column=1, padx=5, pady=(0, 0))

        self.img_display = customtkinter.CTkLabel(master=self, image=self.img, text="Video Thumb")
        self.img_display.grid(row=2, column=1, padx=5, pady=(0, 0))

                
    #Discovering Download Path
    def get_download_path(self):
        """Returns the default downloads path for linux or windows"""
        if os.name == 'nt':
            import winreg
            self.sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            self.downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.sub_key) as key:
                location = winreg.QueryValueEx(key, self.downloads_guid)[0]
            return location
        return os.path.join(os.path.expanduser('~'), 'downloads')


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def button_callback(self):
        self.link = self.entry.get()
        yt = YouTube(self.link)
        self.titulo.set(yt.title)
        self.thumb = yt.thumbnail_url
        self.im = Image.open(requests.get(self.thumb, stream=True).raw)
        self.img2 = customtkinter.CTkImage(light_image=self.im,
                                  dark_image=self.im,
                                  size=(150, 150))
        self.img2_display = customtkinter.CTkLabel(master=self, image=self.img2)
        self.img2_display.grid(row=2, column=1, padx=5, pady=(0, 0))

        self.download_video(self.link,self.pasta)
        self.entry.delete(first_index=0,last_index=len(self.entry.get()))

        self.baixou = customtkinter.CTkLabel(master=self, text= 'Foi Baixado no Diretório Selecionado !')
        self.baixou.grid(row=3, column=1, padx=5, pady=(0, 0))
    


    def diretorio(self):
        self.pasta = filedialog.askdirectory()
        self.folder_selected.set(self.pasta)
        print(self.pasta)
        
    def download_video(self,video_link:str,diretorio:str):
        yt = YouTube(video_link)
        yd = yt.streams.get_highest_resolution()
        yd.download(self.pasta.replace('/','//'))

        

if __name__ == "__main__":
    app = App()
    app.mainloop()