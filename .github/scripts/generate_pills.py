import os

def generate_pills_svg():
    width = 950
    height = 100
    bg_color = "#00000000"
    font_family = "'Courier Prime', 'Courier New', monospace"
    font_size = 16
    line_height = 30
    
    # Colors
    blue_color = "#0080FF" # Electric Blue
    red_color = "#FF0040"  # Matrix Red
    
    lines = [
        {"text": "> BLUE PILL: The story ends, you wake up in your bed...", "color": blue_color},
        {"text": "> RED PILL:  You stay in Wonderland, and I show you how deep the rabbit hole goes.", "color": red_color}
    ]
    
    typing_speed = 0.03
    
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&amp;display=swap');
        
        .pill-text {{
            font-family: {font_family};
            font-size: {font_size}px;
            font-weight: bold;
            white-space: pre;
            opacity: 0;
        }}
        
        .blue-glow {{ fill: {blue_color}; filter: drop-shadow(0 0 2px {blue_color}); }}
        .red-glow {{ fill: {red_color}; filter: drop-shadow(0 0 2px {red_color}); }}
        
        /* Cursor */
        .cursor {{
            fill: {red_color};
            animation: blink 1s step-end infinite;
            opacity: 0;
        }}
        @keyframes blink {{ 0%, 100% {{ opacity: 0; }} 50% {{ opacity: 1; }} }}
'''

    current_time = 0
    
    for i, line in enumerate(lines):
        char_count = len(line['text'])
        duration = char_count * typing_speed
        start = current_time
        
        css_class = "blue-glow" if i == 0 else "red-glow"
        y_pos = 35 + (i * line_height)
        
        # We need a Keyframe that:
        # 1. Sets Opacity to 1 (Show text)
        # 2. Scans a mask (Typewriter)
        
        svg += f'''
        @keyframes type-{i} {{
             0% {{ width: 0; opacity: 1; }}
             100% {{ width: 100%; opacity: 1; }}
        }}
        
        #mask-rect-{i} {{
            animation: type-{i} {duration}s steps({char_count}, end) forwards;
            animation-delay: {start}s;
            width: 0;
        }}
        
        #text-{i} {{
            animation: show-{i} 0.1s forwards;
            animation-delay: {start}s;
        }}
        @keyframes show-{i} {{ to {{ opacity: 1; }} }}
'''
        
        svg += f'''
    </style>
    <!-- Element {i} -->
    <defs>
        <mask id="mask-{i}">
            <rect id="mask-rect-{i}" x="0" y="{y_pos-20}" height="30" fill="white"/>
        </mask>
    </defs>
    <text id="text-{i}" x="10" y="{y_pos}" class="pill-text {css_class}" mask="url(#mask-{i})">{line['text']}</text>
'''
        current_time += duration + 0.5 # Pause between lines

    # Add cursor at the end acting like it chose red
    cursor_start = current_time
    svg += f'''
    <rect x="10" y="{35 + line_height + 5}" width="10" height="2" class="cursor" style="animation-delay: {cursor_start}s; fill: {red_color};"/>
</svg>'''

    # Fix the style tag closure which was split in the loop logic above for simplicity
    # Actually, simpler approach: Build all CSS string first, then HTML.
    
    # RE-DOING GENERATION LOGIC FOR CLEANER SVG STRUCTURE
    
    css_content = ""
    html_content = ""
    current_time = 0.5 # Initial delay
    
    for i, line in enumerate(lines):
        char_count = len(line['text'])
        duration = char_count * typing_speed
        start = current_time
        
        css_class = "blue-glow" if i == 0 else "red-glow"
        y_pos = 35 + (i * line_height)
        
        css_content += f'''
        /* Line {i} */
        #mask-rect-{i} {{
            animation: type-{i} {duration}s steps({char_count}, end) forwards;
            animation-delay: {start}s;
            width: 0;
        }}
        @keyframes type-{i} {{ 
            0% {{ width: 0; }} 
            100% {{ width: 100%; }} 
        }}
        
        #text-{i} {{
            animation: fade-in-{i} 0.1s forwards;
            animation-delay: {start}s;
            opacity: 0;
        }}
        @keyframes fade-in-{i} {{ to {{ opacity: 1; }} }}
'''
        html_content += f'''
    <defs>
        <mask id="mask-{i}">
            <rect id="mask-rect-{i}" x="0" y="{y_pos-20}" height="30" fill="white"/>
        </mask>
    </defs>
    <text id="text-{i}" x="20" y="{y_pos}" class="pill-text {css_class}" mask="url(#mask-{i})">{line['text']}</text>
'''
        current_time += duration + 0.5

    final_svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&amp;display=swap');
        
        .pill-text {{
            font-family: {font_family};
            font-size: {font_size}px;
            font-weight: bold;
            white-space: pre;
        }}
        .blue-glow {{ fill: {blue_color}; filter: drop-shadow(0 0 2px {blue_color}); }}
        .red-glow {{ fill: {red_color}; filter: drop-shadow(0 0 2px {red_color}); }}
        
        {css_content}
    </style>
    
    <rect width="100%" height="100%" fill="{bg_color}"/>
    {html_content}
</svg>'''

    output_path = os.path.join(os.path.dirname(__file__), '../../assets/matrix-pills.svg')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_svg)
    print(f"Generated Pills SVG at: {output_path}")

if __name__ == "__main__":
    generate_pills_svg()
