import os

def generate_morpheus_svg():
    # Configuration
    width = 800
    height = 100
    bg_color = "#00000000" # Transparent
    text_color = "#00FF41"
    font_family = "'Courier Prime', 'Courier New', monospace"
    font_size = 16
    line_height = 24
    
    # Dramatic Lines
    lines = [
        "> INCOMING TRANSMISSION...",
        "> SENDER: MORPHEUS",
        '> "This is your last chance. After this, there is no turning back."'
    ]
    
    # Timings
    typing_speed = 0.04
    line_delay = 0.8
    
    svg_content = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&amp;display=swap');
        
        .term-text {{
            font-family: {font_family};
            font-size: {font_size}px;
            fill: {text_color};
            font-weight: bold;
            white-space: pre;
            filter: drop-shadow(0 0 2px {text_color});
        }}
        
        /* Cursor Blinking */
        .cursor {{
            fill: {text_color};
            animation: blink 1s step-end infinite;
        }}
        @keyframes blink {{ 0%, 100% {{ opacity: 0; }} 50% {{ opacity: 1; }} }}
'''

    current_time = 0
    tspan_elements = []
    
    for i, line in enumerate(lines):
        char_count = len(line)
        duration = char_count * typing_speed
        start = current_time
        
        # Keyframe for typing
        svg_content += f'''
        @keyframes type-{i} {{
            0% {{ width: 0; }}
            100% {{ width: 100%; }}
        }}
        #mask-rect-{i} {{
            animation: type-{i} {duration}s steps({char_count}, end) forwards;
            animation-delay: {start}s;
            width: 0;
        }}
'''
        # SVG Element with Mask
        y_pos = 25 + (i * line_height)
        tspan_elements.append(f'''
    <defs>
        <mask id="mask-{i}">
            <rect id="mask-rect-{i}" x="0" y="{y_pos-15}" height="20" fill="white"/>
        </mask>
    </defs>
    <text x="10" y="{y_pos}" class="term-text" mask="url(#mask-{i})">{line}</text>
''')
        current_time += duration + line_delay

    svg_content += f'''    </style>
    <rect width="100%" height="100%" fill="{bg_color}"/>
    {''.join(tspan_elements)}
</svg>'''

    output_path = os.path.join(os.path.dirname(__file__), '../../assets/morpheus-quote.svg')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated Morpheus SVG at: {output_path}")

if __name__ == "__main__":
    generate_morpheus_svg()
