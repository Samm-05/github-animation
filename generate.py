import requests
from PIL import Image, ImageDraw
import random

USERNAME = "Samm-05"

# -------- FETCH DATA --------
def get_data():
    try:
        url = f"https://github-contributions-api.jogruber.de/v4/{USERNAME}"
        res = requests.get(url, timeout=10)
        data = res.json()
        return data["contributions"]
    except:
        return [[[{"count": 1} for _ in range(7)] for _ in range(20)]][0]

weeks = get_data()

# -------- SETTINGS --------
WIDTH = 900
HEIGHT = 300
CELL = 12

frames = []

# Player position
player_x = WIDTH // 2
player_y = HEIGHT - 30

# Bullets
bullets = []

# -------- ANIMATION --------
for step in range(40):
    img = Image.new("RGB", (WIDTH, HEIGHT), (5, 10, 20))
    draw = ImageDraw.Draw(img)

    # Draw stars background
    for _ in range(80):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        draw.point((x, y), fill="white")

    # Draw contributions as enemies
    enemies = []
    for i, week in enumerate(weeks):
        for j, day in enumerate(week):
            if day["count"] > 0:
                x = i * CELL + 100
                y = j * CELL + (step * 2)

                y = y % HEIGHT

                draw.rectangle([x, y, x+10, y+10], fill=(0, 255, 100))
                enemies.append((x, y))

    # Fire bullet every few frames
    if step % 3 == 0:
        bullets.append([player_x, player_y])

    # Draw bullets
    new_bullets = []
    for b in bullets:
        b[1] -= 8
        draw.rectangle([b[0], b[1], b[0]+3, b[1]+8], fill="yellow")

        # collision
        hit = False
        for ex, ey in enemies:
            if abs(b[0] - ex) < 10 and abs(b[1] - ey) < 10:
                hit = True
                draw.rectangle([ex, ey, ex+10, ey+10], fill="red")
                break

        if not hit and b[1] > 0:
            new_bullets.append(b)

    bullets = new_bullets

    # Draw player (spaceship)
    draw.polygon([
        (player_x, player_y),
        (player_x - 10, player_y + 15),
        (player_x + 10, player_y + 15)
    ], fill=(0, 200, 255))

    frames.append(img)

# -------- SAVE GIF --------
frames[0].save(
    "animation.gif",
    save_all=True,
    append_images=frames[1:],
    duration=80,
    loop=0
)
