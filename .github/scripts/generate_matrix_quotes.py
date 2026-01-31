import os
import html

def generate_quotes_svg():
    # Configuration
    width = 600
    height = 50
    bg_color = "#00000000" # Transparent
    text_color = "#00FF41"
    font_family = "'Courier Prime', 'Courier New', monospace"
    font_size = 20
    
    # Quotes to cycle through
    quotes = [
        "Wake up, Rishav...",
        "The Matrix has you...",
        "Follow the white rabbit.",
        "Ignorance is bliss.",
        "I know Kung Fu.",
        "Choice is an illusion.",
        "Never send a human to do a machine's job."
    ]
    
    # Timing configuration
    typing_speed = 0.1   # Time to type one char
    hold_time = 2.0      # Time to hold the full quote
    delete_speed = 0.05  # Time to delete one char
    pause_between = 0.5  # Time before next quote starts
    
    # Calculate total duration
    total_duration = 0
    quote_timings = []
    
    current_start = 0
    for quote in quotes:
        length = len(quote)
        type_duration = length * typing_speed
        delete_duration = length * delete_speed
        
        # Cycle: Type -> Hold -> Delete -> Pause
        # Actually for CSS simplicity, we often just do: Show -> Wait -> Hide
        # But to simulate "typing" with widths, we need precise timings.
        
        # Start time for this quote in the master loop
        start = current_start
        
        # End of typing
        typed = start + type_duration
        
        # Start of deleting
        start_delete = typed + hold_time
        
        # End of deleting (fully gone)
        end = start_delete + delete_duration
        
        quote_timings.append({
            "quote": quote,
            "start": start,
            "typed": typed,
            "start_delete": start_delete,
            "end": end,
            "duration": end - start
        })
        
        current_start = end + pause_between
        
    total_duration = current_start
    
    # SVG Config
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="2" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
    </defs>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&amp;display=swap');
        
        .matrix-text {{
            font-family: {font_family};
            font-size: {font_size}px;
            fill: {text_color};
            font-weight: bold;
            filter: url(#glow);
            white-space: pre;
            opacity: 0; /* Hidden by default */
        }}
        
        .cursor {{
            fill: {text_color};
            animation: blink 1s step-end infinite;
        }}
        
        @keyframes blink {{
            0%, 100% {{ opacity: 0; }}
            50% {{ opacity: 1; }}
        }}
'''

    # Generate CSS for each quote
    for i, q in enumerate(quote_timings):
        # We need keyframes that set visibility/width based on the global percentage
        # Percentage = (time / total_duration) * 100
        
        start_pct = (q['start'] / total_duration) * 100
        typed_pct = (q['typed'] / total_duration) * 100
        delete_start_pct = (q['start_delete'] / total_duration) * 100
        end_pct = (q['end'] / total_duration) * 100
        
        # Text ID
        tid = f"q{i}"
        
        # Mask ID for typing effect
        mid = f"m{i}"
        
        # Keyframe name
        kname = f"anim-{i}"
        
        # We animate the Width of the Mask to simulate typing
        # And we animate the Opacity of the Text to show/hide it entirely when not active
        
        svg += f'''
        /* Animation for Quote {i}: "{q['quote']}" */
        #{mid}-rect {{
            animation: {kname} {total_duration}s linear infinite;
        }}
        
        #{tid} {{
            animation: {kname}-os {total_duration}s step-end infinite;
        }}
        
        /* Mask Width Animation (Typing) */
        @keyframes {kname} {{
            0%, {start_pct}% {{ width: 0; }}
            {typed_pct}%, {delete_start_pct}% {{ width: 100%; }}
            {end_pct}%, 100% {{ width: 0; }}
        }}
        
        /* Opacity/Visibility Animation (Only show during active window) */
        @keyframes {kname}-os {{
            0%, {start_pct}% {{ opacity: 0; }}
            {start_pct}%, {end_pct}% {{ opacity: 1; }}
            {end_pct}%, 100% {{ opacity: 0; }}
        }}
'''

    svg += f'''    </style>
    
    <!-- Background (Transparent) -->
    <rect width="100%" height="100%" fill="{bg_color}"/>
    
    <!-- Centered Container -->
    <g transform="translate({width/2}, {height/2 + 5})">
'''

    # Create Elements
    for i, q in enumerate(quote_timings):
        tid = f"q{i}"
        mid = f"m{i}"
        
        # Centered text requires text-anchor="middle"
        # BUT mask-based typing from the center is hard (it reveals from left to right).
        # Better to have it Left-Aligned but centered in the block if possible, 
        # OR just plain Left-Aligned. The external one was centered.
        # To center typing text: We can center the text element, but the mask needs to grow from the center? 
        # No, typing usually moves left-to-right. 
        # Let's group ("<g>") it and shift it left by half its approximate width? 
        # Or simpler: Just text-anchor="middle" and grow mask from left? No, that reveals middle out.
        # Let's stick to text-anchor="middle" because that's what the user had.
        # Implication: "Typing" reveal from Left-to-Right on Centered Text is tricky.
        # Alternative: Don't use mask. Use "content" replacement? No CSS support.
        # Alternative: We use a Monospace font. We can calculate exact width.
        # Let's try text-anchor="middle" and a mask that covers the whole width, 
        # but the mask rect moves? 
        # Actually, "Typing" usually implies left alignment. Centers typing looks weird.
        # Let's switch to text-anchor="middle" and ignore true "left-to-right" typing visuals 
        # and instead do a "glitch reveal" or just keep the mask simple (Left to Right reveal on Centered text).
        # Yes, Left-to-Right reveal on Centered Text works: it reveals the left part of the sentence first.
        
        # We need to know the text width roughly. 20px monospace ~ 12px width per char?
        char_w = 12.5 # Approx for Courier Prime 20px
        text_w = len(q['quote']) * char_w
        half_w = text_w / 2
        
        svg += f'''
        <defs>
            <mask id="{mid}">
                <!-- The mask needs to cover the centered text. 
                     Text is at x=0 (centered).
                     So text spans from -half_w to +half_w.
                     Mask rect should start at -half_w and grow width.
                -->
                <rect id="{mid}-rect" x="{-half_w}" y="-20" height="40" fill="white" width="0"/>
            </mask>
        </defs>
        
        <text id="{tid}" class="matrix-text" text-anchor="middle" mask="url(#{mid})">{html.escape(q['quote'])}</text>
'''

    svg += '''
    </g>
</svg>'''

    # Output
    output_path = os.path.join(os.path.dirname(__file__), '../../assets/matrix-quotes.svg')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
        
    print(f"Generated SVG at: {output_path}")

if __name__ == "__main__":
    generate_quotes_svg()
