from flask import Flask

app = Flask(__name__, static_url_path="/static")

app.secret_key="You are so close."

agent_images = {
    "Brimstone": "Brimstone_icon.jpg",
    "Viper": "Viper_icon.png",
    "Omen": "Omen_icon.png",
    "Killjoy": "Killjoy_icon.webp",
    "Cypher": "Cypher_icon.webp",
    "Sova": "Sova_icon.jpg",
    "Sage": "Sage_icon.jpg",
    "Phoenix": "Phoenix_icon.webp",
    "Jett": "Jett_icon.webp",
    "Reyna": "Reyna_icon.webp",
    "Raze": "Raze_icon.webp",
    "Breach": "Breach_icon.webp",
    "Skye": "Skye_icon.png",
    "Yoru": "Yoru_icon.webp",
    "Astra": "Astra_icon.webp",
    "Kay/O": "KAYO_icon.webp",
    "Chamber": "Chamber_icon.jpg",
    "Neon": "Neon_icon.webp",
    "Fade": "Fade_icon.png",
    "Harbor": "Harbor_icon.webp",
    "Gekko": "Gekko_icon.png"
}

rank_icons = {
    "Unranked": "default.png",
    "Iron 1": "Iron_1_Rank.png",
    "Iron 2": "Iron_2_Rank.png",
    "Iron 3": "Iron_3_Rank.png",
    "Bronze 1": "Bronze_1_Rank.png",
    "Bronze 2": "Bronze_2_Rank.png",
    "Bronze 3": "Bronze_3_Rank.png",
    "Silver 1": "Silver_1_Rank.png",
    "Silver 2": "Silver_2_Rank.png",
    "Silver 3": "Silver_3_Rank.png",
    "Gold 1": "Gold_1_Rank.png",
    "Gold 2": "Gold_2_Rank.png",
    "Gold 3": "Gold_3_Rank.png",
    "Platinum 1": "Platinum_1_Rank.png",
    "Platinum 2": "Platinum_2_Rank.png",
    "Platinum 3": "Platinum_3_Rank.png",
    "Diamond 1": "Diamond_1_Rank.png",
    "Diamond 2": "Diamond_2_Rank.png",
    "Diamond 3": "Diamond_3_Rank.png",
    "Ascendant 1": "Ascendant_1_Rank.png",
    "Ascendant 2": "Ascendant_2_Rank.png",
    "Ascendant 3": "Ascendant_3_Rank.png",
    "Immortal 1": "Immortal_1_Rank.png",
    "Immortal 2": "Immortal_2_Rank.png",
    "Immortal 3": "Immortal_3_Rank.png",
    "Radiant": "Radiant_Rank.png"
}

map_loads = {
    "Ascent": "Loading_Screen_Ascent.webp",
    "Bind": "Loading_Screen_Bind.webp",
    "Breeze": "Loading_Screen_Breeze.webp",
    "Fracture": "Loading_Screen_Fracture.webp",
    "Haven": "Loading_Screen_Haven.webp",
    "Icebox": "Loading_Screen_Icebox.webp",
    "Split": "Loading_Screen_Split.webp",
    "Lotus": "Loading_Screen_Lotus.webp",
    "Pearl": "Loading_Screen_Pearl.webp"
}