import os

OUTPUT_FILE = 'assets/matrix-quote.svg'
Link = "https://github.com/msrishav-28"

def generate_svg():
    # Matrix Colors
    COLOR = '#00ff41'
    BG_COLOR = '#0d1117' # Matching GitHub Dark mode for seamless look
    
    # Text
    TEXT = "I know you're out there. I can feel you now."
    
    # SVG Content
    # We use a masking rectangle that expands to reveal the text
    svg = f"""<svg width="600" height="60" viewBox="0 0 600 60" xmlns="http://www.w3.org/2000/svg">
    <style>
        .text {{ 
            font-family: 'Courier New', Courier, monospace; 
            fill: {COLOR}; 
            font-size: 20px; 
            font-weight: bold;
        }}
        .cursor {{
            fill: {COLOR};
            animation: blink 1s step-end infinite;
        }}
        .mask-rect {{
            animation: type 3.5s steps(40, end) forwards;
        }}
        
        @keyframes type {{
            from {{ width: 0; }}
            to {{ width: 550px; }}
        }}
        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0; }}
        }}
    </style>
    
    <rect width="600" height="60" fill="{BG_COLOR}" rx="4" opacity="0"/>
    
    <defs>
        <mask id="textMask">
            <rect class="mask-rect" x="0" y="0" width="0" height="60" fill="white" />
        </mask>
    </defs>
    
    <!-- Text revealed by mask -->
    <text x="20" y="38" class="text" mask="url(#textMask)">{TEXT}</text>
    
    <!-- Cursor following the text (Approximate for visual effect) -->
    <!-- Ideally cursor moves with mask, but simple blink at end is safer for SVG -->
    <!-- Using a rect attached to the mask end is hard in pure CSS SVG without JS -->
    <!-- We'll just put a blinking cursor at the end line to simulate 'waiting for input' after type -->
    
    <g transform="translate(560, 20)">
        <rect class="cursor" width="10" height="25" y="0" opacity="0">
             <animate attributeName="opacity" values="0;1;0" dur="1s" repeatCount="indefinite" begin="3.5s"/>
        </rect>
    </g>
    
</svg>"""
    
    return svg

def main():
    try:
        svg_content = generate_svg()
        
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding="utf-8") as f:
            f.write(svg_content)
            
        print(f"✅ Matrix Quote generated at {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
