import os

def generate_footer_svg():
    width = 800
    height = 150
    bg_color = "#00000000" # Transparent
    text_color = "#00ff41" # Matrix Green
    dim_color = "#008f11"
    font = "'Courier Prime', monospace"
    
    # Lines to type
    lines = [
        "> SYSTEM_DIAGNOSTIC: COMPLETE",
        "> TRACE_PROGRAM: ERASED",
        "> CARRIER_SIGNAL: LOST",
        "> ",
        "> \"I can only show you the door.",
        ">  You're the one that has to walk through it.\""
    ]
    
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&amp;display=swap');
        
        .term-text {{
            font-family: {font};
            font-size: 14px;
            fill: {text_color};
            font-weight: bold;
            opacity: 0;
            white-space: pre;
        }}
        
        .cursor {{
            fill: {text_color};
            animation: blink 1s step-end infinite;
        }}
        
        @keyframes blink {{ 50% {{ opacity: 0; }} }}
        
        /* Simple Opacity Reveal Animation */
        @keyframes reveal {{
            to {{ opacity: 1; }}
        }}
    </style>
'''
    
    y_start = 25
    line_height = 20
    current_delay = 0.5
    line_delay = 0.8 # Seconds between lines
    
    for i, line in enumerate(lines):
        y_pos = y_start + (i * line_height)
        
        # Staggered reveal
        delay = current_delay + (i * line_delay)
        
        svg += f'''
    <text x="20" y="{y_pos}" class="term-text" style="animation: reveal 0.1s forwards; animation-delay: {delay}s;">{line}</text>
'''

    # Blinking cursor at the end
    last_y = y_start + (len(lines) * line_height)
    cursor_appeartime = current_delay + (len(lines) * line_delay)
    
    svg += f'''
    <rect x="20" y="{last_y-10}" width="10" height="15" class="cursor" opacity="0" style="animation: reveal 0.1s forwards {cursor_appeartime}s, blink 1s step-end infinite {cursor_appeartime}s;">
    </rect>
    
</svg>'''

    output_path = os.path.join(os.path.dirname(__file__), '../../assets/matrix-footer.svg')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Matrix Footer SVG at: {output_path}")

if __name__ == "__main__":
    generate_footer_svg()
