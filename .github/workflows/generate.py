import requests
from PIL import Image, ImageDraw

USERNAME = "YOUR_USERNAME"

def get_data():
    try:
        url = f"https://github-contributions-api.jogruber.de/v4/{USERNAME}"
        res = requests.get(url, timeout=10)

        if res.status_code != 200:
            print("API failed, using dummy data")
            return [[[{"count": 1} for _ in range(7)] for _ in range(20)]][0]

        data = res.json()

        if "contributions" not in data:
            print("Invalid API data")
            return [[[{"count": 1} for _ in range(7)] for _ in range(20)]][0]

        return data["contributions"]

    except Exception as e:
        print("Error:", e)
        return [[[{"count": 1} for _ in range(7)] for _ in range(20)]][0]


weeks = get_data()

frames = []

for step in range(20):
    img = Image.new("RGB", (800, 200), "black")
    draw = ImageDraw.Draw(img)

    for i, week in enumerate(weeks):
        for j, day in enumerate(week):
            try:
                if day["count"] > 0:
                    x = i * 12
                    y = (j * 12 + step * 2) % 200

                    draw.rectangle([x, y, x+10, y+10], fill="green")
            except:
                pass

    # spaceship
    draw.rectangle([380, 170, 420, 190], fill="blue")

    frames.append(img)

# Save GIF safely
if frames:
    frames[0].save(
        "animation.gif",
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0
    )

print("GIF created successfully")
