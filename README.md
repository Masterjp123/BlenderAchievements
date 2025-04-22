# Currently the Extendsion DOESN'T work because it is actively being worked on! All Contributions are welcome! :)

# 🏆 Blender Achievements Add-on

Currently there is no addon avalible but I'm working on it!
A fun, extensible achievement system for Blender that rewards your creative milestones!  
Track everything from your first render to modeling madness—all while keeping it fully open-source and user-powered.
Also Keep in mind this was purely made as a lol haha funni idea, please don't roast me in the issues about how this is an impractical idea, TRUST ME I KNOW IT IS.

---

![example-achievement](icons/default/example.png)

## ✨ Features

- ✅ **Unlock achievements** as you:
  - Reach high vertex counts
  - Render, save, and build complex scenes
  - Create objects, materials, animations, and more
- 🔁 **Automatically checks progress** every few seconds—no need to click or refresh anything
- 📂 **JSON-powered system** for defining achievements (no coding needed!)
- 🖼️ **512x512 PNG icons** make your unlocked trophies visually shine
- 🌐 **Community achievements**: opt-in support for fan-made milestones via GitHub
- 🔧 **Customizable preferences** to control achievement behavior and filtering
- 💬 **Pop-up notifications** when you unlock new achievements

---

## 📦 Installation

1. Download or clone this repo:

2. In Blender:
- Go to **Edit → Preferences → Add-ons**
- Click **Install…**
- Select the `blender_achievements.py` file
- Enable the add-on from the list

3. Press **N** in the 3D View → open the **Achievements** tab → Click **"Sync Achievements"**

🎉 You're now ready to start earning Blender achievements!

---

## 🎯 How It Works

- Achievements are defined entirely in `.json` files inside the `achievements/` folder
- Each entry includes:
```json
{
 "id": "unique_id",
 "name": "Super Modeler",
 "description": "Reach 1 million vertices",
 "trigger": "vertex_count",
 "threshold": 1000000,
 "icon": "super_modeler.png"
}
