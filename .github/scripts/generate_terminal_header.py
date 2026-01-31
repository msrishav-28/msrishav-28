import os

def generate_svg():
    # Configuration
    width = 800
    height = 120
    bg_color = "#00000000" # Transparent background
    text_color = "#00FF41"
    font_family = "'Courier Prime', 'Courier New', monospace"
    font_size = 14
    line_height = 20
    
    # Lines to type
    lines = [
        "> INITIALIZING...",
        "> BYPASSING FIREWALL... [DONE]",
        "> ESTABLISHING SECURE CONNECTION... [DONE]",
        "> LOADING PROFILE: M_S_RISHAV_SUBHIN..."
    ]
    
    # Animation timings
    typing_speed_per_char = 0.05  # Seconds per character
    line_delay = 0.5             # Delay between lines
    
    # Generate SVG Content
    svg_content = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&amp;display=swap');
        
        .terminal-text {{
            font-family: {font_family};
            font-size: {font_size}px;
            fill: {text_color};
            font-weight: bold;
            white-space: pre; 
        }}
        
        /* Cursor Animation */
        .cursor {{
            animation: blink 1s step-end infinite;
            fill: {text_color};
            opacity: 0;
        }}
        
        @keyframes blink {{
            0%, 100% {{ opacity: 0; }}
            50% {{ opacity: 1; }}
        }}
'''

    # Generate CSS animations for each line
    current_time = 0
    tspan_elements = []
    
    for i, line in enumerate(lines):
        char_count = len(line)
        duration = char_count * typing_speed_per_char
        start_time = current_time
        end_time = start_time + duration
        
        # Unique ID for this line's mask
        mask_id = f"mask-{i}"
        
        # CSS for the typing effect (using a mask)
        svg_content += f'''
        @keyframes type-{i} {{
            0% {{ width: 0; }}
            100% {{ width: 100%; }}
        }}
        
        #path-{i} {{
            animation: type-{i} {duration}s steps({char_count}, end) forwards;
            animation-delay: {start_time}s;
            width: 0; /* Hidden initially */
        }}
        
        /* Cursor visibility control */
        #cursor-{i} {{
            animation: blink 1s step-end infinite, cursor-vis-{i} {duration + 0.5}s forwards;
            animation-delay: 0s, {start_time}s;
            opacity: 0;
        }}
        
        @keyframes cursor-vis-{i} {{
            0% {{ opacity: 0; }} /* Wait */
            1% {{ opacity: 1; }} /* Start typing */
            99% {{ opacity: 1; }} /* Typing done */
            100% {{ opacity: 0; }} /* Hide after done */
        }}
'''
        
        # SVG Element Construction
        y_pos = 20 + (i * line_height)
        
        # We simulate typing by revealing the text with a clip-path or mask
        # Since SVG masks on text can be tricky with 'steps', let's use a simpler approach:
        # A rectangular mask that grows.
        
        tspan_elements.append(f'''
    <!-- Line {i+1} -->
    <defs>
        <mask id="{mask_id}">
            <rect id="path-{i}" x="0" y="{y_pos - 10}" height="15" fill="white"/>
        </mask>
    </defs>
    <text x="10" y="{y_pos}" class="terminal-text" mask="url(#{mask_id})">{line}</text>
    ''')
        
        # Update time for next line
        current_time = end_time + line_delay

    svg_content += f'''    </style>

    <rect width="100%" height="100%" fill="{bg_color}"/>
    
    { "".join(tspan_elements) }
    
</svg>'''

    # Writing file
    output_path = os.path.join(os.path.dirname(__file__), '../../assets/terminal-header.svg')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    print(f"Generated SVG at: {output_path}")

if __name__ == "__main__":
    generate_svg()
