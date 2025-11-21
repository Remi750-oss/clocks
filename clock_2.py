import math
import tkinter as tk
from datetime import datetime


class AnalogClock(tk.Canvas):
    def __init__(self, master=None, size=400, **kwargs):
        self.size = size
        self.center = size // 2
        self.radius = int(size * 0.45)
        super().__init__(master, width=size, height=size, bg="white", highlightthickness=0, **kwargs)
        self.pack()

        # Outer circle (thicker stroke)
        self.create_oval(self.center - self.radius, self.center - self.radius,
                         self.center + self.radius, self.center + self.radius,
                         fill="#f8f8f8", outline="#222", width=8)

        self.create_marks()
        # Draw hour numbers
        self.create_numbers()

        # Hands
        self.hour_hand = None
        self.minute_hand = None
        self.second_hand = None
        # Create a single center dot item to reuse
        self.center_dot = self.create_oval(self.center - 6, self.center - 6,
                                           self.center + 6, self.center + 6,
                                           fill="#222")
        self.update_clock()

    def create_marks(self):
        for h in range(12):
            angle = math.radians(h * 30)  # 360/12
            x_outer = self.center + int(self.radius * math.sin(angle))
            y_outer = self.center - int(self.radius * math.cos(angle))
            length = 18 if h % 3 == 0 else 10
            x_inner = self.center + int((self.radius - length) * math.sin(angle))
            y_inner = self.center - int((self.radius - length) * math.cos(angle))
            width = 3 if h % 3 == 0 else 2
            self.create_line(x_inner, y_inner, x_outer, y_outer, width=width, fill="#000")

    def create_numbers(self):
        # Place numbers 1..12 around the dial
        for n in range(1, 13):
            angle = math.radians(n * 30)
            # position slightly inside the outer edge
            num_radius = int(self.radius * 0.72)
            x = self.center + int(num_radius * math.sin(angle))
            y = self.center - int(num_radius * math.cos(angle))
            # center the text; adjust vertical offset for better centering
            self.create_text(x, y, text=str(n), font=("Helvetica", int(self.size * 0.06), "bold"), fill="#000")

    def _hand_coords(self, angle_deg, length_fraction):
        angle = math.radians(angle_deg)
        x = self.center + int(self.radius * length_fraction * math.sin(angle))
        y = self.center - int(self.radius * length_fraction * math.cos(angle))
        return (self.center, self.center, x, y)

    def update_clock(self):
        now = datetime.now()
        hour = now.hour % 12
        minute = now.minute
        second = now.second
        micro = now.microsecond

        # Hour hand: include minute fraction
        hour_angle = (hour + minute / 60.0) * 30
        minute_angle = (minute + second / 60.0) * 6

        # Remove old hands
        if self.hour_hand:
            self.delete(self.hour_hand)
        if self.minute_hand:
            self.delete(self.minute_hand)
        if self.second_hand:
            self.delete(self.second_hand)

        # Draw hour and minute hands
        self.hour_hand = self.create_line(*self._hand_coords(hour_angle, 0.5), width=6, fill="#222", capstyle=tk.ROUND)
        self.minute_hand = self.create_line(*self._hand_coords(minute_angle, 0.8), width=4, fill="#444", capstyle=tk.ROUND)

        # Second hand (trotteuse) - smooth using microseconds
        second_fraction = second + micro / 1_000_000.0
        second_angle = second_fraction * 6
        # Draw a slightly thicker, smooth second hand
        self.second_hand = self.create_line(*self._hand_coords(second_angle, 0.9), width=4, fill="#d00", capstyle=tk.ROUND)

        # Keep center dot item on top
        self.tag_raise(self.center_dot)

        # Schedule next update frequently for smooth movement
        self.after(50, self.update_clock)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Horloge analogique")
    clock = AnalogClock(root, size=420)

    # Speak time function (try pyttsx3, otherwise fallback to PowerShell TTS)
    def speak_time():
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        # human-readable
        text = f"Il est {hour} heure"
        if minute != 0:
            text += f" {minute}"

        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception:
            # Fallback: use PowerShell System.Speech (Windows)
            import subprocess
            ps = f"Add-Type –AssemblyName System.speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak('{text}');"
            subprocess.run(["powershell", "-Command", ps], check=False)

    # Button to speak the time
    speak_btn = tk.Button(root, text="Dire l'heure", command=speak_time)
    speak_btn.pack(pady=8)

    root.mainloop()
