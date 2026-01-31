import os
import random

def generate_rain_svg():
    width = 850
    height = 300
    bg_color = "#0d1117"
    text_color = "#00ff41" # Matrix Green
    font_size = 14
    
    # Standard Matrix-like characters (Katakana + Numbers)
    chars = "ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ1234567890"
    
    # Number of rain drops (columns)
    columns = 40
    
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&amp;display=swap');
        
        .matrix-bg {{ fill: {bg_color}; }}
        
        .rain-drop {{
            font-family: 'Courier Prime', monospace;
            font-size: {font_size}px;
            fill: {text_color};
            font-weight: bold;
            opacity: 0;
            writing-mode: vertical-rl;
            text-orientation: upright;
            white-space: pre;
            filter: drop-shadow(0 0 2px {text_color});
        }}
        
        @keyframes fall {{
            0% {{ transform: translateY(-100%); opacity: 0; }}
            10% {{ opacity: 1; }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateY(100%); opacity: 0; }}
        }}
        
        @keyframes flicker {{
            0% {{ opacity: 0.8; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0.8; }}
        }}
    </style>
    
    <rect width="100%" height="100%" class="matrix-bg"/>
'''

    # Generate columns of rain
    for i in range(columns):
        # Random properties for natural feel
        x_pos = i * (width / columns) + 5
        duration = random.uniform(3, 8)      # Fall speed
        delay = random.uniform(0, 5)         # Start delay
        length = random.randint(10, 25)      # Length of the string
        
        # Generate random character string for this drop
        drop_text = "".join(random.choice(chars) for _ in range(length))
        
        # We use a unique ID for animation variation if needed, 
        # but here we inline the style for randomness
        
        svg += f'''
    <text x="{x_pos}" y="0" class="rain-drop" style="animation: fall {duration}s linear infinite; animation-delay: -{delay}s;">
        {drop_text}
    </text>
'''

    # Add a "System Status" overlay line
    svg += f'''
    <text x="10" y="{height - 10}" font-family="Courier Prime" font-size="10" fill="#009929" opacity="0.8">
        > SYSTEM ACTIVITY: DECRYPTING...
    </text>
</svg>'''

    output_path = os.path.join(os.path.dirname(__file__), '../../assets/matrix-rain.svg')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Matrix Rain SVG at: {output_path}")

if __name__ == "__main__":
    generate_rain_svg()
