import requests
from PIL import Image, ImageDraw

USERNAME = "Samm-05"

url = f"https://github-contributions-api.jogruber.de/v4/{USERNAME}"
data = requests.get(url).json()

weeks = data["contributions"]

frames = []

for step in range(20):
    img = Image.new("RGB", (800, 200), "black")
    draw = ImageDraw.Draw(img)

    for i, week in enumerate(weeks):
        for j, day in enumerate(week):
            if day["count"] > 0:
                x = i * 12
                y = j * 12 + (step * 2)

                draw.rectangle([x, y % 200, x+10, (y % 200)+10], fill="green")

    draw.rectangle([380, 170, 420, 190], fill="blue")

    frames.append(img)

frames[0].save(
    "animation.gif",
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=0
)
