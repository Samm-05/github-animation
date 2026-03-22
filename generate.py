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
        return data.get("contributions", [])
    except:
        return [[{"count": 1} for _ in range(7)] for _ in range(30)]

weeks = get_data()

# -------- SETTINGS --------
WIDTH = 900
HEIGHT = 300
CELL = 12

frames = []

player_x = WIDTH // 2
player_y = HEIGHT - 40

bullets = []

# -------- ANIMATION --------
for step in range(50):
    img = Image.new("RGB", (WIDTH, HEIGHT), (5, 10, 20))
    draw = ImageDraw.Draw(img)

    # 🌌 Stars background
    for _ in range(100):
        draw.point((random.randint(0, WIDTH), random.randint(0, HEIGHT)), fill="white")

    enemies = []

    # 🟩 Contributions (with fill boost)
    for i, week in enumerate(weeks):
        for j, day in enumerate(week):
            count = 0

            if isinstance(day, dict):
                count = day.get("count", day.get("contributionCount", 0))

            if count > 0 or random.random() < 0.3:
                x = i * CELL + 100
                y = (j * CELL + step * 2) % HEIGHT

                draw.rectangle([x, y, x + 10, y + 10], fill=(0, 255, 100))
                enemies.append((x, y))

    # 🔫 Fire bullets
    if step % 2 == 0:
        bullets.append([player_x, player_y])

    new_bullets = []

    for b in bullets:
        b[1] -= 10

        # bullet glow
        draw.ellipse([b[0]-2, b[1], b[0]+4, b[1]+10], fill=(255, 255, 0))

        hit = False

        for ex, ey in enemies:
            if abs(b[0] - ex) < 10 and abs(b[1] - ey) < 10:
                hit = True

                # 💥 explosion rings
                for r in range(3, 12, 3):
                    draw.ellipse([ex-r, ey-r, ex+r, ey+r], outline="red")

                break

        if not hit and b[1] > 0:
            new_bullets.append(b)

    bullets = new_bullets

    # 🚀 ADVANCED SPACESHIP

    # glow
    for i in range(6, 0, -1):
        draw.ellipse([
            player_x - i*3,
            player_y - i*2,
            player_x + i*3,
            player_y + i*2
        ], outline=(0, 150, 255))

    # main body
    draw.polygon([
        (player_x, player_y - 12),
        (player_x - 15, player_y + 15),
        (player_x + 15, player_y + 15)
    ], fill=(0, 200, 255))

    # cockpit
    draw.ellipse([
        player_x - 5, player_y - 5,
        player_x + 5, player_y + 5
    ], fill="white")

    # wings
    draw.polygon([
        (player_x - 15, player_y + 15),
        (player_x - 25, player_y + 25),
        (player_x - 5, player_y + 20)
    ], fill=(0, 120, 255))

    draw.polygon([
        (player_x + 15, player_y + 15),
        (player_x + 25, player_y + 25),
        (player_x + 5, player_y + 20)
    ], fill=(0, 120, 255))

    # engine flame
    draw.ellipse([
        player_x - 5, player_y + 15,
        player_x + 5, player_y + 30
    ], fill=(255, 120, 0))

    frames.append(img)

# -------- SAVE GIF --------
frames[0].save(
    "animation.gif",
    save_all=True,
    append_images=frames[1:],
    duration=70,
    loop=0
)

print("🚀 Advanced Space Shooter GIF Created!")
