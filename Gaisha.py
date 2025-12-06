import tkinter as tk
import math
import random

# --- Konfiguration ---
WIDTH, HEIGHT = 600, 600
BG_COLOR = "#2c1e31"   
SKIN_COLOR = "#fff0e6" 
HAIR_COLOR = "#1a1a1a"
KIMONO_MAIN = "#d93f59" 
KIMONO_SEC = "#ff9eb5"  
OBI_COLOR = "#d4af37"   
FAN_COLOR = "#f5e6a2"   
FAN_RIM = "#cf961d"     

class GeishaFigure:
    def __init__(self, canvas, x, y):
        self.c = canvas
        self.x = x
        self.y = y
        self.t = 0
        
        # Der Fächer muss zuerst initialisiert werden, damit die ID existiert
        # Wir erstellen ihn leer und updaten ihn gleich
        self.fan_id = self.c.create_polygon(0,0,0,0, fill=FAN_COLOR, outline=FAN_RIM, width=2)

        self.draw_body()
        self.draw_head()
        
    def draw_body(self):
        # Kimono
        coords = [
            self.x - 40, self.y + 120, 
            self.x + 40, self.y + 120, 
            self.x + 25, self.y + 40,  
            self.x - 25, self.y + 40   
        ]
        # WICHTIG: Das Sternchen *coords entpackt die Liste!
        self.c.create_polygon(*coords, fill=KIMONO_MAIN, outline="", smooth=True)
        
        # Obi
        self.c.create_rectangle(self.x - 28, self.y + 70, self.x + 28, self.y + 90, fill=OBI_COLOR, outline="")

        # Linker Ärmel
        sleeve_coords = [
            self.x - 25, self.y + 45, 
            self.x - 65, self.y + 80, 
            self.x - 45, self.y + 100
        ]
        self.c.create_polygon(*sleeve_coords, fill=KIMONO_SEC, smooth=True)

    def draw_head(self):
        # Haare (Hinterkopf)
        self.c.create_oval(self.x - 35, self.y - 45, self.x + 35, self.y + 25, fill=HAIR_COLOR)
        
        # Gesicht
        self.c.create_oval(self.x - 25, self.y - 30, self.x + 25, self.y + 20, fill=SKIN_COLOR, outline="")
        
        # Haare (Dutt)
        self.c.create_oval(self.x - 20, self.y - 55, self.x + 20, self.y - 25, fill=HAIR_COLOR)
        
        # Haarschmuck
        self.c.create_line(self.x + 10, self.y - 40, self.x + 40, self.y - 30, fill="#ff3333", width=3)
        self.c.create_oval(self.x + 38, self.y - 32, self.x + 44, self.y - 26, fill="#ff3333", outline="")

        # Augen
        self.c.create_arc(self.x - 18, self.y - 10, self.x - 8, self.y, start=0, extent=-180, style=tk.ARC, width=1.5, outline="black")
        self.c.create_arc(self.x + 8, self.y - 10, self.x + 18, self.y, start=0, extent=-180, style=tk.ARC, width=1.5, outline="black")
        
        # Mund
        self.c.create_oval(self.x - 3, self.y + 8, self.x + 3, self.y + 11, fill="#cc0000", outline="")

    def update(self):
        self.t += 0.05
        
        # Fächer bewegen
        hand_x = self.x + 30
        hand_y = self.y + 60
        
        angle_base = math.sin(self.t) * 0.5
        
        fan_points = [hand_x, hand_y] 
        
        radius = 50
        start_angle = -1.5 + angle_base
        end_angle = 0.5 + angle_base
        steps = 10
        
        for i in range(steps + 1):
            curr_a = start_angle + (end_angle - start_angle) * (i / steps)
            px = hand_x + math.cos(curr_a) * radius
            py = hand_y + math.sin(curr_a) * radius
            fan_points.extend([px, py])
            
        # Hier ist das Update der Koordinaten
        self.c.coords(self.fan_id, *fan_points)
        # Damit der Fächer VOR dem Körper bleibt, heben wir ihn an
        self.c.tag_raise(self.fan_id)

class SimplePetal:
    def __init__(self, canvas):
        self.c = canvas
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.speed = random.uniform(1, 3)
        self.size = random.randint(3, 6)
        self.id = self.c.create_oval(0,0,0,0, fill="#ffccdd", outline="")
    
    def move(self):
        self.y += self.speed
        self.x += math.sin(self.y * 0.05) * 0.5 
        if self.y > HEIGHT:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, WIDTH)
        
        self.c.coords(self.id, self.x, self.y, self.x+self.size, self.y+self.size)

def run_animation():
    root = tk.Tk()
    root.title("Geisha Fan Dance")
    
    cv = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0)
    cv.pack()
    
    petals = [SimplePetal(cv) for _ in range(30)]
    geisha = GeishaFigure(cv, WIDTH//2, HEIGHT//2 + 50)
    
    def loop():
        geisha.update()
        for p in petals:
            p.move()
        root.after(30, loop) 
        
    loop()
    root.mainloop()

if __name__ == "__main__":
    run_animation()