import os
import requests

USERNAME = os.getenv('USERNAME', 'msrishav-28')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def generate_fallback_svg(width, height, bg_color, text_color):
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <style>.text {{ font-family: 'Courier New', monospace; fill: {text_color}; }}</style>
    <rect width="100%" height="100%" fill="{bg_color}" rx="5"/>
    <text x="50%" y="45%" class="text" text-anchor="middle" font-size="14">&gt; ACHIEVEMENTS DATA OFFLINE</text>
    <text x="50%" y="62%" class="text" text-anchor="middle" font-size="12">Could not verify live GitHub metrics.</text>
</svg>'''

def generate_achievements_svg():
    width = 800
    height = 160
    bg_color = "#0d1117"
    text_color = "#00ff41" # Matrix Green
    dim_color = "#00661a"
    
    # Define Achievements logic
    # (Simplified for demo: In a real scenario, we'd fetch specific data)
    # Fetch real GitHub data
    user_data = None
    try:
        headers = {}
        if GITHUB_TOKEN:
            headers['Authorization'] = f'token {GITHUB_TOKEN}'
        
        resp = requests.get(f'https://api.github.com/users/{USERNAME}', headers=headers)
        if resp.status_code == 200:
            user_data = resp.json()
        else:
            print(f"Error fetching user data: {resp.status_code}")
    except Exception as e:
        print(f"Exception fetching user data: {e}")

    if user_data is None:
        svg = generate_fallback_svg(width, height, bg_color, text_color)
        output_path = os.path.join(os.path.dirname(__file__), '../../assets/matrix-achievements.svg')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print("Generated fallback achievements SVG due to unavailable live data.")
        return

    # Default Logic using Real Data
    repo_count = user_data.get('public_repos', 0)
    followers = user_data.get('followers', 0)
    following = user_data.get('following', 0)
    created_at = user_data.get('created_at', '2025')[:4] # Year

    achievements = [
        {"name": "THE ONE", "desc": "Profile Owner", "unlocked": True, "icon": "救"}, 
        {"name": "OPERATOR", "desc": "10+ Repos", "unlocked": repo_count >= 10, "icon": "操"},
        {"name": "ARCHITECT", "desc": "20+ Repos", "unlocked": repo_count >= 20, "icon": "築"},
        {"name": "TRINITY", "desc": "10+ Followers", "unlocked": followers >= 10, "icon": "参"},
        {"name": "AGENT", "desc": "Networker", "unlocked": following > 5, "icon": "敵"},
        {"name": "ORACLE", "desc": "Early Adopter", "unlocked": int(created_at) < 2024, "icon": "預"}
    ]
    
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&amp;display=swap');
        
        .box {{
            fill: {bg_color};
            stroke: {dim_color};
            stroke-width: 1;
        }}
        .box.unlocked {{
            stroke: {text_color};
            filter: drop-shadow(0 0 2px {text_color});
        }}
        
        .title {{
            font-family: 'Courier Prime', monospace;
            font-size: 10px;
            fill: {text_color};
            text-anchor: middle;
            font-weight: bold;
        }}
        .desc {{
            font-family: 'Courier Prime', monospace;
            font-size: 8px;
            fill: {dim_color};
            text-anchor: middle;
        }}
        .icon {{
            font-family: 'Courier Prime', monospace;
            font-size: 20px;
            fill: {text_color};
            text-anchor: middle;
        }}
        
        /* Glitch Animation */
        @keyframes glitch {{
            0% {{ opacity: 1; }}
            95% {{ opacity: 1; }}
            96% {{ opacity: 0.8; transform: translateX(1px); }}
            97% {{ opacity: 1; transform: translateX(0); }}
            100% {{ opacity: 1; }}
        }}
        .glitch {{ animation: glitch 4s infinite alternate; }}
    </style>
    
    <rect width="100%" height="100%" fill="{bg_color}" rx="5"/>
    
    <text x="{width/2}" y="20" font-family="'Courier Prime', monospace" font-size="14" fill="{text_color}" text-anchor="middle" letter-spacing="2">
        > SYSTEM UPGRADES UNLOCKED
    </text>
'''

    # Layout Grid
    cols = 6
    box_w = 110
    box_h = 90
    start_x = (width - (cols * box_w)) / 2 + 5
    start_y = 50
    
    for i, ach in enumerate(achievements):
        x = start_x + (i * (box_w + 10))
        y = start_y
        
        # Style based on unlocked status
        box_class = "box unlocked" if ach['unlocked'] else "box"
        icon_fill = text_color if ach['unlocked'] else dim_color
        
        svg += f'''
    <g transform="translate({x}, {y})" class="glitch" style="animation-delay: {i*0.5}s">
        <rect width="{box_w}" height="{box_h}" class="{box_class}" rx="5"/>
        <text x="{box_w/2}" y="35" class="icon" fill="{icon_fill}">{ach['icon']}</text>
        <text x="{box_w/2}" y="60" class="title">{ach['name']}</text>
        <text x="{box_w/2}" y="75" class="desc">{ach['desc']}</text>
    </g>
'''

    svg += '</svg>'

    output_path = os.path.join(os.path.dirname(__file__), '../../assets/matrix-achievements.svg')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Matrix Achievements SVG at: {output_path}")

if __name__ == "__main__":
    generate_achievements_svg()
