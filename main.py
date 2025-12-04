import tkinter as tk
from tkinter import messagebox
import pyautogui
import threading
import time
import keyboard

# CẤU HÌNH
pyautogui.FAILSAFE = True

class AutoClickerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker Pro v3")
        self.root.geometry("350x340")
        
        # Biến trạng thái
        self.is_running = False
        self.click_thread = None
        self.current_hotkey = 'q'
        self.start_delay = 3

        # GIAO DIỆN
        # 1. Nhập Delay
        frame_delay = tk.Frame(root)
        frame_delay.pack(pady=15)
        
        tk.Label(frame_delay, text="Tốc độ click (giây):", font=("Arial", 11)).pack(side=tk.LEFT)
        
        self.entry_delay = tk.Entry(frame_delay, font=("Arial", 12), justify='center', width=8)
        self.entry_delay.insert(0, "0.1")
        self.entry_delay.pack(side=tk.LEFT, padx=10)

        # 2. Cài đặt Phím tắt
        frame_hotkey = tk.Frame(root)
        frame_hotkey.pack(pady=5)
        
        self.btn_change_key = tk.Button(frame_hotkey, text=f"Phím tắt: [{self.current_hotkey.upper()}]", 
                                        command=self.change_hotkey_listener,
                                        width=20, bg="#f0f0f0")
        self.btn_change_key.pack()
        tk.Label(frame_hotkey, text="(Bấm vào để đổi)", font=("Arial", 8), fg="gray").pack()

        # 3. Nút Start/Stop
        self.btn_toggle = tk.Button(root, text="BẮT ĐẦU (START)", 
                                    bg="green", fg="white", font=("Arial", 14, "bold"),
                                    width=20, height=2,
                                    command=self.toggle_clicking)
        self.btn_toggle.pack(pady=20)

        # 4. Trạng thái
        self.lbl_status = tk.Label(root, text="Trạng thái: Đang nghỉ", fg="red", font=("Arial", 10, "bold"))
        self.lbl_status.pack(pady=5)
        self.lbl_countdown = tk.Label(root, text="", fg="orange", font=("Arial", 12, "bold"))
        self.lbl_countdown.pack()

        # Bắt sự kiện click chuột trái bất kỳ đâu trên cửa sổ
        self.root.bind_all("<Button-1>", self.global_click_handler)

        # --- KHỞI TẠO HOTKEY ---
        self.update_hotkey_binding()

    def global_click_handler(self, event):
        """Hàm xử lý khi click bất kỳ đâu"""
        # Nếu cái widget vừa click vào KHÔNG PHẢI là ô nhập delay và KHÔNG PHẢI nút đổi phím
        if event.widget != self.entry_delay and event.widget != self.btn_change_key:
            # Thì trả focus về cửa sổ chính (làm mất con trỏ ở ô nhập)
            self.root.focus()

    def update_hotkey_binding(self):
        try:
            keyboard.unhook_all_hotkeys()
        except:
            pass
        keyboard.add_hotkey(self.current_hotkey, self.toggle_clicking)

    def change_hotkey_listener(self):
        self.btn_change_key.config(text="Đang chờ phím...", bg="yellow")
        self.root.update()
        
        keyboard.unhook_all_hotkeys()
        
        # Đợi phím nhấn xuống
        key_event = keyboard.read_event(suppress=True) 
        while key_event.event_type != 'down':
             key_event = keyboard.read_event(suppress=True)
        
        self.current_hotkey = key_event.name
        self.btn_change_key.config(text=f"Phím tắt: [{self.current_hotkey.upper()}]", bg="#f0f0f0")
        self.update_hotkey_binding()
        self.root.focus() # Trả focus để tránh lỗi gõ phím
        messagebox.showinfo("Thành công", f"Đã đổi phím tắt sang: {self.current_hotkey.upper()}")

    def run_clicker(self):
        """Logic click chuột"""
        
        # --- ĐẾM NGƯỢC ---
        for i in range(self.start_delay, 0, -1):
            if not self.is_running: 
                self.lbl_countdown.config(text="")
                return
            self.lbl_countdown.config(text=f"Click sau: {i}s")
            time.sleep(1)
        
        self.lbl_countdown.config(text="")
        self.lbl_status.config(text=">>> ĐANG CLICK <<<", fg="green")
        
        # BẮT ĐẦU CLICK 
        
        while self.is_running:
            try:
                delay_val = float(self.entry_delay.get())
                
                # Thực hiện click
                pyautogui.click()
                
                # Nghỉ
                time.sleep(delay_val)
            except ValueError:
                self.stop_clicker()
                break
            except Exception as e:
                print(f"Lỗi: {e}")
                break

    def start_clicker(self):
        self.root.focus() # Bỏ focus ô nhập ngay khi bắt đầu
        
        self.is_running = True
        self.btn_toggle.config(text=f"DỪNG ({self.current_hotkey.upper()})", bg="red")
        self.lbl_status.config(text="Chuẩn bị chạy...", fg="orange")
        
        self.click_thread = threading.Thread(target=self.run_clicker)
        self.click_thread.daemon = True
        self.click_thread.start()

    def stop_clicker(self):
        self.is_running = False
        self.btn_toggle.config(text="BẮT ĐẦU (START)", bg="green")
        self.lbl_status.config(text="Trạng thái: Đang nghỉ", fg="red")
        self.lbl_countdown.config(text="")

    def toggle_clicking(self):
        if self.is_running:
            self.stop_clicker()
        else:
            self.start_clicker()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerUI(root)
    root.attributes('-topmost', True) 
    root.mainloop()
