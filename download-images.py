#!/usr/bin/env python3
"""
Download images for Elle's birthday collage.
Run from the birthday-collage/web/ directory:
    python download-images.py

Images saved to ./images/{id}.jpg  (or .png if the URL ends in .png)
Safe to re-run — skips files that already exist.
Delete a file and re-run to refresh it.

Fallback order per item:
  1. 'url' key (direct link, if provided)
  2. backup-images/{id}.jpg / .jpeg / .png  (drop files here to override)
  3. loremflickr.com keyword search

─── DIRECT URL ─────────────────────────────────────────────────────────────────
Add a 'url' key to any item. It will be tried first:

    {
        'id':       'lucy',
        'keywords': 'campfire,fire,night',   # used as loremflickr fallback
        'w': 700, 'h': 900, 'lock': 140,
        'url': 'https://example.com/my-campfire-photo.jpg',
    },

─── BACKUP FOLDER ──────────────────────────────────────────────────────────────
Drop any image into backup-images/ named {id}.jpg / {id}.jpeg / {id}.png.
It will be copied into images/ automatically, before loremflickr is tried.
This is the easiest way to use a locally saved photo for a specific person.

────────────────────────────────────────────────────────────────────────────────
"""

import os
import shutil
import time
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, "images")
BACKUP_DIR = os.path.join(SCRIPT_DIR, "backup-images")

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

LOREMFLICKR = "https://loremflickr.com/{w}/{h}/{kw}?lock={lock}"

# ── Item definitions ─────────────────────────────────────────────────────────
# Required fields:  id, keywords, w, h, lock
# Optional field:   url  →  use this direct URL instead of loremflickr
#
# For the four Snorlax entries the 'url' field is pre-filled with PokeAPI
# sprites; edit them just like any other entry.

ITEMS = [
    {
        "id": "brother",
        "keywords": "baobab,tree,africa",
        "w": 800, "h": 1000, "lock": 11,
    },
    {
        "id": "rani",
        "keywords": "sunflower,yellow",
        "w": 700, "h": 900, "lock": 22,
    },
    {
        "id": "gina",
        "keywords": "fire,flames,red",
        "w": 600, "h": 900, "lock": 33,
        "url": "blob:https://gemini.google.com/7e99af7d-14ae-482c-a244-003f034c4907",
    },
    {
        "id": "saif",
        "keywords": "cycling,bicycle,sport",
        "w": 900, "h": 700, "lock": 44,
    },
    {
        "id": "tal-toy",
        "keywords": "toy,vintage,colorful",
        "w": 700, "h": 600, "lock": 55,
        "url": "https://treehousetoys.us/cdn/shop/files/ScreenShot2023-05-02at5.18.15PM.png?v=1683062327&width=1920",
    },
    {
        "id": "tal-globe",
        "keywords": "snow,globe,winter",
        "w": 700, "h": 700, "lock": 66,
        "url": "https://m.media-amazon.com/images/I/81Z5KHEspPL.jpg",
    },
    {
        "id": "tal-ball",
        "keywords": "rubber,bands,colorful",
        "w": 700, "h": 700, "lock": 77,
        "url": "https://d1jqecz1iy566e.cloudfront.net/large/pg009.jpg",
    },
    {
        "id": "tal-glitter",
        "keywords": "glitter,sparkle,gold",
        "w": 700, "h": 600, "lock": 88,
        "url":"https://festivalglitter.co.uk/cdn/shop/products/rose-gold-2_1080x.jpg?v=1523394788"
    },
    {
        "id": "tal-chopstick",
        "keywords": "chopsticks,noodles,asian",
        "w": 400, "h": 900, "lock": 99,
        "url": "https://www.wikihow.com/images/thumb/2/2d/Put-Your-Hair-up-With-Chopsticks-Step-24.jpg/v4-460px-Put-Your-Hair-up-With-Chopsticks-Step-24.jpg",
    },
    {
        "id": "sangeeta",
        "keywords": "pillow,cozy,bedroom",
        "w": 800, "h": 600, "lock": 110,
        "url": "https://cdn.shopify.com/s/files/1/0650/7560/9847/files/MYH-1037271_8244830a-f989-4628-81c3-56a23ae8f550.jpg?v=1695279972",
    },
    {
        "id": "claireyun",
        "keywords": "cappuccino,coffee,latte",
        "w": 700, "h": 700, "lock": 120,
    },
    {
        "id": "alkamasi1",
        "keywords": "beach,ocean,waves",
        "w": 1000, "h": 600, "lock": 130,
    },
    {
        "id": "lucy",
        "keywords": "campfire,fire,night",
        "w": 700, "h": 900, "lock": 140,
    },
    {
        "id": "elaine",
        "keywords": "fashion,clothes,shopping",
        "w": 700, "h": 900, "lock": 150,
        "url": "https://preview.redd.it/mall-nostalgia-info-on-forever21-90s-2005-v0-q9qlkslzu9gg1.jpg?width=640&crop=smart&auto=webp&s=a20491bcb01dd63d6405dd9441ef203bb5620967",
    },
    {
        "id": "cengiz",
        "keywords": "lightning,energy,electric",
        "w": 600, "h": 900, "lock": 160,
        "url": "blob:https://i.imgur.com/uVOJWHp.png"
    },
    {
        "id": "adil",
        "keywords": "snorlax,pokemon",
        "w": 800, "h": 800, "lock": 1,
        "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/143.png",
    },
    {
        "id": "danny",
        "keywords": "snorlax,pokemon",
        "w": 800, "h": 800, "lock": 1,
        "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/143.png",
    },
    {
        "id": "adrienne",
        "keywords": "snorlax,pokemon",
        "w": 800, "h": 800, "lock": 1,
        "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/143.png",
    },
    {
        "id": "david",
        "keywords": "snorlax,pokemon",
        "w": 800, "h": 800, "lock": 1,
        "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/shiny/143.png",
    },
    {
        "id": "michael",
        "keywords": "raven,crow,bird,black",
        "w": 900, "h": 600, "lock": 170,
        "url": "blob:https://wingsplain.com/wp-content/uploads/Chihuahuan-Raven-196x300.png",
    },
    {
        "id": "alkamasi2",
        "keywords": "fairy,sparkle,magic,dust",
        "w": 700, "h": 700, "lock": 180,
    },
    {
        "id": "kirbnoj",
        "keywords": "sunglasses,fashion,eyewear",
        "w": 1000, "h": 500, "lock": 190,
        "url": "https://johannwolff.com/cdn/shop/files/johann-wolff-alma-black-brown-sunglasses2.jpg",
    },
    {
        "id": "tim1",
        "keywords": "jujube,dates,red,fruit",
        "w": 700, "h": 600, "lock": 200,
        "url": "https://assets.clevelandclinic.org/transform/LargeFeatureImage/e339899b-9f3f-48cb-8b78-757048ab6a14/jujubes-1289657102",
    },
    {
        "id": "tim2",
        "keywords": "egg,yolk,fried",
        "w": 700, "h": 700, "lock": 210,
        "url": "blob:https://gemini.google.com/954428fc-6d49-457d-81bf-5ba29d67d532",
    },
    {
        "id": "pipe",
        "keywords": "space,nebula,stars,cosmos",
        "w": 700, "h": 900, "lock": 220,
        "url": "https://t4.ftcdn.net/jpg/11/70/51/51/360_F_1170515123_pbaFKKQBwDjVAgXLKxZ6eKJO1egMrr7k.jpg"
    },
    {
        "id": "claire",
        "keywords": "pasta,macaroni,cheese,food",
        "w": 700, "h": 600, "lock": 230,
    },
    {
        "id": "rhan",
        "keywords": "lotion,perfume,bottle,beauty",
        "w": 600, "h": 900, "lock": 240,
        "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgDAW6-jDYbgErvtkYiFu9Ip3328IkkSKDWQ&s",
    },
    {
        "id": "amanda",
        "keywords": "noodles,takeout,food,bowl",
        "w": 800, "h": 700, "lock": 250,
    },
    {
        "id": "joanus",
        "keywords": "panda,bear,cute",
        "w": 700, "h": 700, "lock": 260,
    },
    {
        "id": "sumin",
        "keywords": "dog,puppy,fluffy,cute",
        "w": 700, "h": 700, "lock": 270,
        "url": "https://mblogthumb-phinf.pstatic.net/20160622_196/dkdlel315_1466590781515r4hJf_JPEG/%C1%A6%B8%F1_%BE%F8%C0%BD.jpg?type=w420",
    },
    {
        "id": "jennifer",
        "keywords": "salmon,seared,food,plated",
        "w": 800, "h": 600, "lock": 280,
        "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTN5vPTNComVBDhRwwXQfB_81Y4W0aW1wF6YQ&s",
    },
    {
        "id": "shreya",
        "keywords": "sunset,golden,sky,horizon",
        "w": 1000, "h": 600, "lock": 290,
        "url": "https://images.ctfassets.net/0wjmk6wgfops/6JWSPm7M0PksPIZe4p1SFv/eef8eefbb9f2279f99d139d1f2b2c50e/_1d63e83a-f6a2-4135-b104-ecd309fe74d9.bc1b1f6022.jpg",
    },
    {
        "id": "ari",
        "keywords": "bedroom,cozy,mattress,sleep",
        "w": 900, "h": 500, "lock": 300,
        "url": "blob:https://gemini.google.com/9b53768d-d6cf-4416-91f9-1ced771b40ef"
    },
    {
        "id": "sherry",
        "keywords": "yellow,door,bright",
        "w": 600, "h": 900, "lock": 310,
    },
    {
        "id": "katie",
        "keywords": "sparklers,fire,night",
        "w": 900, "h": 600, "lock": 320,
    },
    {
        "id": "nupoor",
        "keywords": "crabs,seafood,claws",
        "w": 800, "h": 800, "lock": 330,
    },
]

# ── Helpers ───────────────────────────────────────────────────────────────────

SNORLAX_FALLBACK = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/143.png"

# ── Helpers ───────────────────────────────────────────────────────────────────

def ext_for(url):
    path = url.split("?")[0].lower()
    return ".png" if path.endswith(".png") else ".jpg"


def find_backup(item_id):
    """Return path of backup file if one exists for this id, else None."""
    for ext in (".jpg", ".jpeg", ".png"):
        p = os.path.join(BACKUP_DIR, item_id + ext)
        if os.path.exists(p):
            return p
    return None


def download_url(url, dest, label):
    print(f"  ↓ {label} ...", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        with open(dest, "wb") as f:
            f.write(data)
        print(f"{len(data) // 1024} KB")
        return True
    except Exception as e:
        print(f"FAILED ({e})")
        return False


def process(item):
    item_id = item["id"]
    direct  = item.get("url")
    kw      = item["keywords"]
    w, h    = item["w"], item["h"]
    lock    = item["lock"]

    # Skip if already downloaded (any extension)
    for ext in (".jpg", ".jpeg", ".png"):
        p = os.path.join(IMAGES_DIR, item_id + ext)
        if os.path.exists(p):
            size = os.path.getsize(p)
            print(f"  ✓ {item_id} already exists ({size // 1024} KB)")
            return True

    # 1. Direct URL
    if direct:
        dest = os.path.join(IMAGES_DIR, item_id + ext_for(direct))
        ok   = download_url(direct, dest, f"{item_id} (direct URL)")
        if ok:
            return True
        print(f"    → direct URL failed, trying backup folder...")

    # 2. Backup folder
    backup = find_backup(item_id)
    if backup:
        dest_ext = os.path.splitext(backup)[1]
        dest_p   = os.path.join(IMAGES_DIR, item_id + dest_ext)
        print(f"  ↑ {item_id} copying from backup-images/", end=" ", flush=True)
        shutil.copy2(backup, dest_p)
        print(f"{os.path.getsize(dest_p) // 1024} KB")
        return True

    if direct:
        print(f"    → no backup found, falling back to loremflickr...")

    # 3. loremflickr
    lf_url  = LOREMFLICKR.format(w=w, h=h, kw=kw, lock=lock)
    lf_dest = os.path.join(IMAGES_DIR, f"{item_id}.jpg")
    ok = download_url(lf_url, lf_dest, f"{item_id} (loremflickr)")

    if not ok and "snorlax" in kw:
        ok = download_url(SNORLAX_FALLBACK,
                          os.path.join(IMAGES_DIR, f"{item_id}.png"),
                          f"{item_id} (snorlax fallback)")
    return ok


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"\nSaving images to:  {IMAGES_DIR}")
    print(f"Backup folder:     {BACKUP_DIR}\n")
    errors = []

    for item in ITEMS:
        ok = process(item)
        if not ok:
            errors.append(item["id"])
        time.sleep(0.25)

    print()
    total = len(ITEMS)
    print(f"Done. {total - len(errors)}/{total} images downloaded.")
    if errors:
        print(f"Failed: {', '.join(errors)}")
        print("Tip: drop a file into backup-images/{id}.jpg, or change lock= for a different photo.")
    else:
        print("All good — open standalone.html in a browser!")


if __name__ == "__main__":
    main()
