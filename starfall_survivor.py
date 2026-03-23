import random
import time
import tkinter as tk


WIDTH = 900
HEIGHT = 600
PLAYER_SPEED = 7
DASH_MULTIPLIER = 2.2
DASH_DURATION_MS = 140
STAR_SPAWN_MS = 260
STAR_BASE_SPEED = 3.2
ENEMY_SPAWN_MS = 950
ENEMY_BASE_SPEED = 2.8
POWERUP_SPAWN_MS = 9500
BACKGROUND_SCROLL_SPEED = 1


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Starfall Survivor")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="#070b16", highlightthickness=0)
        self.canvas.pack()

        self.keys = set()
        self.running = False
        self.game_over = False
        self.paused = False
        self.last_dash_time = 0
        self.dash_until = 0

        self.score = 0
        self.best_score = 0
        self.start_time = 0
        self.last_score_tick = 0
        self.enemy_speed_bonus = 0

        self.bg_stars = []
        self.pickups = []
        self.obstacles = []

        self.player_radius = 18
        self.player_x = WIDTH // 2
        self.player_y = HEIGHT - 80
        self.player = None
        self.player_glow = None

        self.hud_text = None
        self.status_text = None
        self.instructions_text = None

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)

        self.build_background()
        self.show_title_screen()

    def build_background(self):
        self.bg_stars.clear()
        for _ in range(100):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.choice((1, 1, 1, 2, 2, 3))
            speed = random.uniform(0.4, 1.8)
            star = self.canvas.create_oval(x, y, x + size, y + size, fill="#b8d9ff", outline="")
            self.bg_stars.append((star, speed, size))

    def animate_background(self):
        for i, (star, speed, size) in enumerate(self.bg_stars):
            self.canvas.move(star, 0, speed + BACKGROUND_SCROLL_SPEED * 0.15)
            coords = self.canvas.coords(star)
            if coords[1] > HEIGHT:
                x = random.randint(0, WIDTH)
                self.canvas.coords(star, x, -size, x + size, 0)

    def show_title_screen(self):
        self.canvas.delete("ui")
        self.canvas.create_text(
            WIDTH / 2,
            160,
            text="STARFALL SURVIVOR",
            fill="#e8f1ff",
            font=("Helvetica", 28, "bold"),
            tags="ui",
        )
        self.canvas.create_text(
            WIDTH / 2,
            230,
            text="Dodge the falling drones. Grab cyan cores for bonus points.",
            fill="#9cc6ff",
            font=("Helvetica", 14),
            tags="ui",
        )
        self.canvas.create_text(
            WIDTH / 2,
            290,
            text="Move: WASD / Arrows   Dash: Shift   Pause: P",
            fill="#cfe4ff",
            font=("Helvetica", 14),
            tags="ui",
        )
        self.canvas.create_text(
            WIDTH / 2,
            335,
            text="Press Enter to Start",
            fill="#71f1ff",
            font=("Helvetica", 18, "bold"),
            tags="ui",
        )
        self.canvas.create_text(
            WIDTH / 2,
            380,
            text="Press R any time after a round to restart",
            fill="#8aa3c2",
            font=("Helvetica", 12),
            tags="ui",
        )
        self.loop_title()

    def loop_title(self):
        if not self.running:
            self.animate_background()
            self.root.after(30, self.loop_title)

    def reset_game(self):
        self.canvas.delete("game")
        self.canvas.delete("ui")
        self.obstacles.clear()
        self.pickups.clear()
        self.keys.clear()
        self.running = True
        self.game_over = False
        self.paused = False
        self.score = 0
        self.enemy_speed_bonus = 0
        self.start_time = time.time()
        self.last_score_tick = time.time()
        self.player_x = WIDTH // 2
        self.player_y = HEIGHT - 80
        self.dash_until = 0

        self.player_glow = self.canvas.create_oval(0, 0, 0, 0, fill="#1c7cff", outline="", tags="game")
        self.player = self.canvas.create_polygon(0, 0, 0, 0, 0, 0, fill="#ffffff", outline="#71f1ff", width=2, tags="game")
        self.hud_text = self.canvas.create_text(
            18, 18, anchor="nw", text="", fill="#eaf4ff", font=("Helvetica", 14, "bold"), tags="ui"
        )
        self.status_text = self.canvas.create_text(
            WIDTH - 18, 18, anchor="ne", text="", fill="#9cc6ff", font=("Helvetica", 12), tags="ui"
        )
        self.instructions_text = self.canvas.create_text(
            WIDTH / 2, HEIGHT - 22, text="Survive. Dash through gaps. Avoid red drones.", fill="#89a2c7", font=("Helvetica", 11), tags="ui"
        )

        self.update_player_graphics()
        self.schedule_star_spawn()
        self.schedule_enemy_spawn()
        self.schedule_powerup_spawn()
        self.game_loop()

    def on_key_press(self, event):
        key = event.keysym.lower()
        self.keys.add(key)

        if key == "return" and not self.running:
            self.reset_game()
        elif key == "p" and self.running and not self.game_over:
            self.paused = not self.paused
            if not self.paused:
                self.game_loop()
        elif key == "r":
            self.reset_game()
        elif key in ("shift_l", "shift_r") and self.running and not self.paused and not self.game_over:
            now = time.time()
            if now - self.last_dash_time > 1.15:
                self.last_dash_time = now
                self.dash_until = now + DASH_DURATION_MS / 1000

    def on_key_release(self, event):
        key = event.keysym.lower()
        self.keys.discard(key)

    def update_player_graphics(self):
        x = self.player_x
        y = self.player_y
        r = self.player_radius
        glow_r = r + 12
        self.canvas.coords(self.player_glow, x - glow_r, y - glow_r, x + glow_r, y + glow_r)
        self.canvas.coords(
            self.player,
            x, y - r - 6,
            x - r, y + r,
            x, y + r - 6,
            x + r, y + r,
        )

    def schedule_star_spawn(self):
        if self.running and not self.game_over:
            self.spawn_trail_star()
            self.root.after(STAR_SPAWN_MS, self.schedule_star_spawn)

    def schedule_enemy_spawn(self):
        if self.running and not self.game_over:
            self.spawn_enemy()
            interval = max(290, int(ENEMY_SPAWN_MS - self.score * 3.2))
            self.root.after(interval, self.schedule_enemy_spawn)

    def schedule_powerup_spawn(self):
        if self.running and not self.game_over:
            self.spawn_pickup()
            self.root.after(POWERUP_SPAWN_MS, self.schedule_powerup_spawn)

    def spawn_trail_star(self):
        size = random.randint(4, 10)
        x = random.randint(0, WIDTH - size)
        speed = random.uniform(STAR_BASE_SPEED, STAR_BASE_SPEED + 3.3 + self.score * 0.01)
        color = random.choice(["#ffe97a", "#ffca6a", "#ffd3f7", "#9ed0ff"])
        shape = self.canvas.create_oval(x, -size, x + size, 0, fill=color, outline="", tags="game")
        self.obstacles.append({"id": shape, "type": "star", "speed": speed, "size": size})

    def spawn_enemy(self):
        size = random.randint(22, 38)
        x = random.randint(size, WIDTH - size)
        speed = random.uniform(ENEMY_BASE_SPEED, ENEMY_BASE_SPEED + 2 + self.enemy_speed_bonus)
        core = self.canvas.create_oval(x - size, -size * 2, x + size, 0, fill="#ff4365", outline="#ffc1cc", width=2, tags="game")
        self.obstacles.append({"id": core, "type": "enemy", "speed": speed, "size": size})

    def spawn_pickup(self):
        size = 14
        x = random.randint(size, WIDTH - size)
        speed = random.uniform(2.6, 3.5)
        pickup = self.canvas.create_rectangle(
            x - size,
            -size,
            x + size,
            size,
            fill="#4ef5ff",
            outline="#d6fdff",
            width=2,
            tags="game",
        )
        self.pickups.append({"id": pickup, "speed": speed, "size": size})

    def get_player_speed(self):
        speed = PLAYER_SPEED
        if time.time() < self.dash_until:
            speed *= DASH_MULTIPLIER
            self.canvas.itemconfig(self.player_glow, fill="#71f1ff")
        else:
            self.canvas.itemconfig(self.player_glow, fill="#1c7cff")
        return speed

    def move_player(self):
        speed = self.get_player_speed()
        dx = 0
        dy = 0

        if "left" in self.keys or "a" in self.keys:
            dx -= speed
        if "right" in self.keys or "d" in self.keys:
            dx += speed
        if "up" in self.keys or "w" in self.keys:
            dy -= speed
        if "down" in self.keys or "s" in self.keys:
            dy += speed

        self.player_x = min(WIDTH - self.player_radius, max(self.player_radius, self.player_x + dx))
        self.player_y = min(HEIGHT - self.player_radius, max(self.player_radius, self.player_y + dy))
        self.update_player_graphics()

    def collides(self, item_coords, size):
        x1, y1, x2, y2 = item_coords
        px1 = self.player_x - self.player_radius
        py1 = self.player_y - self.player_radius
        px2 = self.player_x + self.player_radius
        py2 = self.player_y + self.player_radius
        return not (x2 < px1 or x1 > px2 or y2 < py1 or y1 > py2)

    def update_objects(self):
        remaining = []
        for obj in self.obstacles:
            self.canvas.move(obj["id"], 0, obj["speed"])
            coords = self.canvas.coords(obj["id"])
            if self.collides(coords, obj["size"]):
                self.end_game()
                return
            if coords[1] <= HEIGHT + 50:
                remaining.append(obj)
            else:
                self.canvas.delete(obj["id"])
        self.obstacles = remaining

        pickup_remaining = []
        for obj in self.pickups:
            self.canvas.move(obj["id"], 0, obj["speed"])
            coords = self.canvas.coords(obj["id"])
            if self.collides(coords, obj["size"]):
                self.score += 15
                self.canvas.delete(obj["id"])
                self.flash_message("+15 core")
                continue
            if coords[1] <= HEIGHT + 50:
                pickup_remaining.append(obj)
            else:
                self.canvas.delete(obj["id"])
        self.pickups = pickup_remaining

    def flash_message(self, text):
        temp = self.canvas.create_text(
            self.player_x,
            self.player_y - 40,
            text=text,
            fill="#71f1ff",
            font=("Helvetica", 12, "bold"),
            tags="ui",
        )

        def fade(step=0):
            if step >= 12:
                self.canvas.delete(temp)
                return
            self.canvas.move(temp, 0, -2)
            self.root.after(35, lambda: fade(step + 1))

        fade()

    def update_score(self):
        now = time.time()
        if now - self.last_score_tick >= 0.12:
            gained = int((now - self.last_score_tick) * 14)
            self.score += max(1, gained)
            self.last_score_tick = now
            self.enemy_speed_bonus = min(6, self.score * 0.008)

    def update_hud(self):
        dash_ready = max(0, 1.15 - (time.time() - self.last_dash_time))
        dash_text = "READY" if dash_ready == 0 else f"{dash_ready:.1f}s"
        self.canvas.itemconfig(self.hud_text, text=f"Score: {self.score}   Best: {max(self.best_score, self.score)}")
        self.canvas.itemconfig(self.status_text, text=f"Dash: {dash_text}")

    def end_game(self):
        self.running = False
        self.game_over = True
        self.best_score = max(self.best_score, self.score)
        self.canvas.create_text(
            WIDTH / 2,
            HEIGHT / 2 - 20,
            text="GAME OVER",
            fill="#ffffff",
            font=("Helvetica", 30, "bold"),
            tags="ui",
        )
        self.canvas.create_text(
            WIDTH / 2,
            HEIGHT / 2 + 20,
            text=f"Final Score: {self.score}",
            fill="#9cc6ff",
            font=("Helvetica", 16),
            tags="ui",
        )
        self.canvas.create_text(
            WIDTH / 2,
            HEIGHT / 2 + 56,
            text="Press R to Restart",
            fill="#71f1ff",
            font=("Helvetica", 14, "bold"),
            tags="ui",
        )

    def game_loop(self):
        if not self.running or self.game_over:
            return

        self.animate_background()

        if self.paused:
            self.canvas.itemconfig(self.instructions_text, text="Paused - Press P to Resume")
            self.root.after(30, self.game_loop)
            return

        self.canvas.itemconfig(self.instructions_text, text="Survive. Dash through gaps. Avoid red drones.")
        self.move_player()
        self.update_objects()
        if not self.running:
            return
        self.update_score()
        self.update_hud()
        self.root.after(16, self.game_loop)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Game().run()
