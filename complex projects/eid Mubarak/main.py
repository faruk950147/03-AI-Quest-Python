import tkinter as tk
from PIL import Image, ImageTk
import random
import math

# Window setup
root = tk.Tk()
root.title("Eid Mubarak Animation")

canvas_width = 800
canvas_height = 600

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Load and resize background image
bg_img = Image.open(r"background.png")
bg_img = bg_img.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_img)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Star class
class Star:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = random.randint(0, canvas_width)
        self.y = random.randint(0, canvas_height)
        self.base_size = random.randint(2, 5)
        self.size = self.base_size
        self.dot_id = canvas.create_oval(
            self.x, self.y, self.x+self.size, self.y+self.size,
            fill=random.choice(["white", "yellow", "#aeefff"]), outline=""
        )
        self.speed = random.uniform(0.5, 2)
        self.grow = True

    def move(self):
        self.y += self.speed
        if self.y > canvas_height:
            self.y = 0
            self.x = random.randint(0, canvas_width)
            self.speed = random.uniform(0.5, 2)
            canvas.itemconfig(self.dot_id, fill=random.choice(["white", "yellow", "#aeefff"]))

        if self.grow:
            self.size += 0.1
            if self.size >= self.base_size + 1:
                self.grow = False
        else:
            self.size -= 0.1
            if self.size <= self.base_size - 0.5:
                self.grow = True

        self.canvas.coords(self.dot_id, self.x, self.y, self.x+self.size, self.y+self.size)

# Generate stars
num_stars = 100
stars = [Star(canvas) for _ in range(num_stars)]

# Text setup
text_message = "EID MUBARAK"
text_id = canvas.create_text(canvas_width//2, canvas_height+50,
                             text=text_message,
                             font=("Helvetica", 50, "bold"),
                             fill="gold")

text_speed = 2
wave_amplitude = 50
wave_frequency = 0.02
angle = 0

# Sparkle particles around text
class Sparkle:
    def __init__(self, canvas, text_id):
        self.canvas = canvas
        self.text_id = text_id
        self.offset_x = random.randint(-150, 150)
        self.offset_y = random.randint(-20, 20)
        self.size = random.randint(2, 4)
        self.color = random.choice(["white", "yellow", "#ffe066", "#ffd700"])
        self.id = canvas.create_oval(0, 0, self.size, self.size, fill=self.color, outline="")

    def move(self):
        x, y = canvas.coords(self.text_id)
        # Sparkle follows text with offset
        new_x = x + self.offset_x
        new_y = y + self.offset_y + random.uniform(-1, 1)
        canvas.coords(self.id, new_x, new_y, new_x + self.size, new_y + self.size)
        # Randomly change color for sparkle effect
        colors = ["gold", "yellow", "#ffe066", "#ffd700", "white"]
        canvas.itemconfig(self.id, fill=random.choice(colors))

num_sparkles = 30
sparkles = [Sparkle(canvas, text_id) for _ in range(num_sparkles)]

# Animation function
def animate():
    global angle
    # Move stars
    for star in stars:
        star.move()

    # Move text vertically
    x, y = canvas.coords(text_id)
    y -= text_speed
    if y < -50:
        y = canvas_height + 50

    # Apply horizontal wave
    wave_x = canvas_width//2 + wave_amplitude * math.sin(angle)
    canvas.coords(text_id, wave_x, y)
    angle += wave_frequency * 360

    # Move sparkles around text
    for sparkle in sparkles:
        sparkle.move()

    # Optional: text color sparkle
    colors = ["gold", "yellow", "#ffe066", "#ffd700"]
    canvas.itemconfig(text_id, fill=random.choice(colors))

    root.after(50, animate)

animate()
root.mainloop()