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
        self.create_oval(self.center - self.radius, self.center - self.radius,
                         self.center + self.radius, self.center + self.radius,
                         fill="#f8f8f8", outline="#222")
        self.create_marks()
        # Hands
        self.hour_hand = None
        self.minute_hand = None
        self.update_clock()

    def create_marks(self):
        for h in range(12):
            angle = math.radians(h * 30)  # 360/12
            x_outer = self.center + int(self.radius * math.sin(angle))
            y_outer = self.center - int(self.radius * math.cos(angle))
            length = 15 if h % 3 == 0 else 8
            x_inner = self.center + int((self.radius - length) * math.sin(angle))
            y_inner = self.center - int((self.radius - length) * math.cos(angle))
            self.create_line(x_inner, y_inner, x_outer, y_outer, width=2, fill="#000")

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
        # Hour hand: include minute fraction
        hour_angle = (hour + minute / 60.0) * 30
        minute_angle = (minute + second / 60.0) * 6

        # Remove old hands
        if self.hour_hand:
            self.delete(self.hour_hand)
        if self.minute_hand:
            self.delete(self.minute_hand)

        # Draw hour and minute hands
        self.hour_hand = self.create_line(*self._hand_coords(hour_angle, 0.5), width=6, fill="#222", capstyle=tk.ROUND)
        self.minute_hand = self.create_line(*self._hand_coords(minute_angle, 0.8), width=4, fill="#444", capstyle=tk.ROUND)

        # Center dot
        self.create_oval(self.center - 6, self.center - 6, self.center + 6, self.center + 6, fill="#222")

        # Schedule next update roughly on the next second
        self.after(200, self.update_clock)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Horloge analogique")
    clock = AnalogClock(root, size=420)
    root.mainloop()
