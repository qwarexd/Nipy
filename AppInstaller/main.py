import customtkinter as ctk
import threading
import subprocess
import os
import paramiko
from scp import SCPClient # качаешь целые папки с анапой 2006?? -  pip install scp
import logging # пока хз нахуя

# ~ ~ ~ C O N F I G U R A T I O N ~ ~ ~
#              100 % S E X
SERVER_IP = "Enter Your SFTP/FTPS/FTP IP" # <== тут указываешь айпи своей тачки где собственно сам sftp
SSH_USER = "user" # <= здесь указываешь логин от системы на которой стоит сфтп
SSH_PASSWORD = "user" # <= здесь пороль, позже можно будет воткнуть ssh ключ ок да
REMOTE_DISTRIB_PATH = "/path/to/your/distributives" # путь до пакетов
LOCAL_TEMP_PATH = r"C:\Setup_Temp" # временная папка куда все будет качатся
# она еще и не удаляется после установки :skull:


# пиздец
APPS = [
    {"name": "7-Zip", "file": "7z.exe", "args": "/S"},
    {"name": "Equalizer APO", "file": "EqualizerAPO-x64-1.4.2.exe", "args": "/S"},
    {"name": "VLC Player", "file": "vlc-3.0.23-win64.exe", "args": "/S"},
]

# пока что реализация конкретно списка приложений сделана именно так но вскоре будет 
# подтягивание файлов через json , а там уже будет шик


class NiniteClone(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Nipy Build v0.1")
        self.geometry("350x400")
        self.minsize(350, 300)
        
        
        self.grid_rowconfigure(1, weight=1) 
        self.grid_columnconfigure(0, weight=1)


        self.label = ctk.CTkLabel(self, text="Auto Install", font=("Arial", 22, "bold"))
        self.label.grid(row=0, column=0, pady=20, padx=10, sticky="nsew")


        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        self.app_rows = {}
        for app in APPS:
            name = app['name']
            lbl = ctk.CTkLabel(self.scroll_frame, text=f"• {name}", font=("Arial", 14))
            lbl.pack(anchor="w", padx=10, pady=5)
            
            status_lbl = ctk.CTkLabel(self.scroll_frame, text="Waiting...", text_color="gray")
            status_lbl.pack(anchor="w", padx=30, pady=(0, 10))
            
            self.app_rows[name] = status_lbl


        self.start_btn = ctk.CTkButton(self, text="Begin Install", command=self.start_thread, height=40)
        self.start_btn.grid(row=2, column=0, pady=20, padx=20, sticky="ew")

    def update_status(self, name, text, color="white"):
        self.app_rows[name].configure(text=text, text_color=color)

    def start_thread(self):
        self.start_btn.configure(state="disabled")
        threading.Thread(target=self.main_process, daemon=True).start()

    def download_files(self):
        """Downloading files via SFTP/FTP/FTPS"""
        if not os.path.exists(LOCAL_TEMP_PATH):
            os.makedirs(LOCAL_TEMP_PATH)
            
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(SERVER_IP, username=SSH_USER, password=SSH_PASSWORD)
            
            sftp = ssh.open_sftp()
            
            for app in APPS:
                remote_file = f"{REMOTE_DISTRIB_PATH}/{app['file']}"
                local_file = os.path.join(LOCAL_TEMP_PATH, app['file'])
                
                self.label.configure(text=f"Downloading: {app['name']}...")
                sftp.get(remote_file, local_file)
            
            sftp.close()
            ssh.close()
            return True
        except Exception as e:
            print(f"SFTP ERROR: {e}")
            return False

    def main_process(self):

        self.label.configure(text="Connecting to server...")
        if not self.download_files():
            self.label.configure(text="Connection Error!", text_color="red")
            self.start_btn.configure(state="normal")
            return


        self.label.configure(text="Installing...")
        for app in APPS:
            name = app['name']
            local_file = os.path.join(LOCAL_TEMP_PATH, app['file'])
            
            self.update_status(name, "Installing...", "yellow")
            
            try:

                process = subprocess.run(f'"{local_file}" {app["args"]}', shell=True, capture_output=True)
                
                if process.returncode == 0:
                    self.update_status(name, "Done ✅", "green")
                else:
                    self.update_status(name, f"Error code: {process.returncode} ❌", "red")
            except Exception as e:
                self.update_status(name, f"Error: {str(e)} ❌", "red")

        self.label.configure(text="All Done!", text_color="green")
        self.start_btn.configure(text="Exit", command=self.destroy, state="normal")

if __name__ == "__main__":
    app = NiniteClone()
    app.mainloop()