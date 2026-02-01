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
        
        @keyframes type {{
            0% {{ width: 0; opacity: 1; }}
            100% {{ width: 100%; opacity: 1; }}
        }}
        
        /* Sequential Typing Animation */
    </style>
    
    <!-- Background (Optional, keep transparent for footer integration) -->
    <!-- <rect width="100%" height="100%" fill="#0d1117" /> -->
'''
    
    y_start = 25
    line_height = 20
    current_delay = 0
    type_speed_per_char = 0.04
    
    for i, line in enumerate(lines):
        duration = len(line) * type_speed_per_char
        y_pos = y_start + (i * line_height)
        
        # Unique animation for each line
        anim_name = f"typeline{i}"
        
        # CSS for this line
        svg += f'''
    <style>
        .line-{i} {{
            overflow: hidden; /* Ensures typing reveal */
            border-right: 2px solid {text_color}; /* The Cursor */
            white-space: pre;
            width: 0;
            animation: 
                typing-{i} {duration}s steps({len(line)}, end) forwards,
                cursor-blink-{i} 0.75s step-end infinite;
            animation-delay: {current_delay}s;
        }}
        
        @keyframes typing-{i} {{
            from {{ width: 0; opacity: 1; }}
            to {{ width: 100%; opacity: 1; }}
        }}
        
        /* Cursor logic: Blink during typing, hide after */
        @keyframes cursor-blink-{i} {{
            from, to {{ border-color: transparent; }}
            50% {{ border-color: {text_color}; }}
        }}
        
        /* Hide cursor after typing is done (except maybe the last one) */
        .line-{i} {{
             border-right-color: transparent; /* Default hidden */
        }}
        
        /* We need a specific keyframe to show the cursor ONLY during the duration + delay */
        /* Actually, simpler approach: Just animate the width/opacity of the text element */
    </style>
'''
        # Simplified Approach: Opacity reveal is easier for pure SVG without complex HTML/CSS mix
        # But we want the "Typing" effect.
        # Let's use the Mask trick again, it was reliable.
        
        mask_id = f"mask-{i}"
        svg += f'''
        <defs>
            <mask id="{mask_id}">
                <rect x="0" y="{y_pos-15}" height="20" fill="white">
                    <animate attributeName="width" from="0" to="600" begin="{current_delay}s" duration="{duration}s" fill="freeze" />
                </rect>
            </mask>
        </defs>
        <text x="20" y="{y_pos}" class="term-text" mask="url(#{mask_id})" opacity="1">{line}</text>
'''
        current_delay += duration + 0.3

    # Blinking cursor at the end
    last_y = y_start + (len(lines) * line_height)
    svg += f'''
    <rect x="20" y="{last_y-10}" width="10" height="15" class="cursor">
        <animate attributeName="opacity" values="0;1;0" dur="1s" begin="{current_delay}s" repeatCount="indefinite" />
    </rect>
    
</svg>'''

    output_path = os.path.join(os.path.dirname(__file__), '../../assets/matrix-footer.svg')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Matrix Footer SVG at: {output_path}")

if __name__ == "__main__":
    generate_footer_svg()
