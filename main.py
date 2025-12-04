import pyautogui
import keyboard
import time

# Cấu hình
pyautogui.FAILSAFE = True
delay = 0.005  # Tốc độ click (0.05 giây/click)
clicking = False # Ban đầu là đang tắt

print("=== TOOL AUTO CLICK SIÊU CẤP ===")
print("  [Q]   : Bật / Tắt Auto Click")
print("  [ESC] : Thoát chương trình")
print("================================")

def toggle_event():
    global clicking
    clicking = not clicking # Đảo ngược trạng thái (Đang bật -> Tắt, Đang tắt -> Bật)
    
    if clicking:
        print(">>> ĐANG CLICK (Nhấn Q để dừng)")
    else:
        print(">>> ĐÃ TẠM DỪNG (Nhấn Q để tiếp tục)")

# Đăng ký phím tắt: Khi nhấn 'q' thì chạy hàm toggle_event
keyboard.add_hotkey('q', toggle_event)

try:
    while True:
        # Nếu trạng thái đang là Bật -> thì Click
        if clicking:
            pyautogui.click()
            time.sleep(delay)
        else:
            # Nếu đang tắt -> Cho máy nghỉ tí đỡ ngốn CPU
            time.sleep(0.1)
            
        # Kiểm tra nếu nhấn ESC thì thoát
        if keyboard.is_pressed('esc'):
            print("\nĐã thoát chương trình.")
            break

except KeyboardInterrupt:
    print("\nĐã dừng.")