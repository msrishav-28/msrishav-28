#!/usr/bin/env python3
"""
Custom Matrix Green Statistics Generator
Generates fully customizable SVG cards with Matrix green theme
Includes custom Matrix green Octocat integration
"""

import os
import requests
from datetime import datetime

USERNAME = os.getenv('USERNAME', 'msrishav-28')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Matrix Green Color Palette
COLORS = {
    'bg_dark': '#0d1117',
    'bg_light': '#161b22',
    'green_0': '#00661a',
    'green_1': '#009929',
    'green_2': '#00cc33',
    'green_3': '#00ff41',  # Primary Matrix green
    'green_4': '#33ff66',
    'text': '#00ff41',
    'text_dim': '#009929',
}

def create_green_octocat_svg():
    """Create a Matrix green Octocat SVG"""
    octocat = f'''<g id="green-octocat">
    <!-- Octocat Head -->
    <circle cx="0" cy="0" r="28" fill="{COLORS['green_3']}" opacity="0.9"/>
    
    <!-- Ears -->
    <ellipse cx="-18" cy="-15" rx="8" ry="10" fill="{COLORS['green_3']}" opacity="0.9"/>
    <ellipse cx="18" cy="-15" rx="8" ry="10" fill="{COLORS['green_3']}" opacity="0.9"/>
    
    <!-- Eyes -->
    <ellipse cx="-10" cy="-3" rx="5" ry="8" fill="{COLORS['bg_dark']}"/>
    <ellipse cx="10" cy="-3" rx="5" ry="8" fill="{COLORS['bg_dark']}"/>
    
    <!-- Pupils with glow -->
    <circle cx="-10" cy="-2" r="3" fill="{COLORS['green_3']}">
        <animate attributeName="opacity" values="1;0.5;1" dur="3s" repeatCount="indefinite"/>
    </circle>
    <circle cx="10" cy="-2" r="3" fill="{COLORS['green_3']}">
        <animate attributeName="opacity" values="1;0.5;1" dur="3s" repeatCount="indefinite"/>
    </circle>
    
    <!-- Nose -->
    <ellipse cx="0" cy="5" rx="3" ry="2" fill="{COLORS['green_2']}"/>
    
    <!-- Smile -->
    <path d="M -8 10 Q 0 15 8 10" stroke="{COLORS['bg_dark']}" stroke-width="2" fill="none" stroke-linecap="round"/>
    
    <!-- Whiskers -->
    <line x1="-28" y1="2" x2="-15" y2="3" stroke="{COLORS['green_2']}" stroke-width="1.5"/>
    <line x1="-28" y1="8" x2="-15" y2="7" stroke="{COLORS['green_2']}" stroke-width="1.5"/>
    <line x1="28" y1="2" x2="15" y2="3" stroke="{COLORS['green_2']}" stroke-width="1.5"/>
    <line x1="28" y1="8" x2="15" y2="7" stroke="{COLORS['green_2']}" stroke-width="1.5"/>
    
    <!-- Glow effect -->
    <circle cx="0" cy="0" r="30" fill="none" stroke="{COLORS['green_3']}" stroke-width="1" opacity="0.3">
        <animate attributeName="r" values="30;32;30" dur="2s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.3;0.1;0.3" dur="2s" repeatCount="indefinite"/>
    </circle>
</g>'''
    return octocat

def get_github_stats():
    """Fetch GitHub statistics using GitHub API"""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    
    # Get user info
    user_url = f'https://api.github.com/users/{USERNAME}'
    user_data = requests.get(user_url, headers=headers).json()
    
    # Get repos
    repos_url = f'https://api.github.com/users/{USERNAME}/repos?per_page=100'
    repos_data = requests.get(repos_url, headers=headers).json()
    
    # Calculate stats
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
    total_forks = sum(repo.get('forks_count', 0) for repo in repos_data)
    total_repos = user_data.get('public_repos', 0)
    
    # Get languages
    languages = {}
    for repo in repos_data:
        if repo.get('language'):
            lang = repo['language']
            languages[lang] = languages.get(lang, 0) + 1
    
    return {
        'repos': total_repos,
        'stars': total_stars,
        'forks': total_forks,
        'followers': user_data.get('followers', 0),
        'languages': languages,
    }

def generate_language_pie_svg(languages_data):
    """Generate a custom Matrix green pie chart for languages"""
    
    # Sort and get top 6 languages
    sorted_langs = sorted(languages_data.items(), key=lambda x: x[1], reverse=True)[:6]
    total = sum(count for _, count in sorted_langs)
    
    if total == 0:
        return ""
    
    # Calculate percentages and angles
    lang_percentages = []
    current_angle = 0
    
    for lang, count in sorted_langs:
        percentage = (count / total) * 100
        angle = (count / total) * 360
        lang_percentages.append({
            'name': lang,
            'percentage': percentage,
            'start_angle': current_angle,
            'end_angle': current_angle + angle,
            'count': count
        })
        current_angle += angle
    
    # Generate SVG
    width, height = 450, 300
    center_x, center_y = 150, 150
    radius = 100
    
    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <rect width="{width}" height="{height}" fill="{COLORS['bg_dark']}" rx="10"/>
    
    <!-- Title -->
    <text x="225" y="30" font-family="'Courier New', monospace" font-size="18" fill="{COLORS['text']}" text-anchor="middle" font-weight="bold">
        MATRIX LANGUAGES
    </text>
    
    <!-- Mini Octocat in corner -->
    <g transform="translate(410, 270) scale(0.5)">
        {create_green_octocat_svg()}
    </g>
    
    <!-- Pie Chart -->
'''
    
    # Draw pie slices
    green_shades = [COLORS['green_3'], COLORS['green_2'], COLORS['green_1'], COLORS['green_4'], COLORS['green_0'], '#66ff8c']
    
    for i, lang_data in enumerate(lang_percentages):
        start = lang_data['start_angle']
        end = lang_data['end_angle']
        
        # Calculate coordinates
        start_rad = (start - 90) * 3.14159 / 180
        end_rad = (end - 90) * 3.14159 / 180
        
        x1 = center_x + radius * __import__('math').cos(start_rad)
        y1 = center_y + radius * __import__('math').sin(start_rad)
        x2 = center_x + radius * __import__('math').cos(end_rad)
        y2 = center_y + radius * __import__('math').sin(end_rad)
        
        large_arc = 1 if (end - start) > 180 else 0
        
        color = green_shades[i % len(green_shades)]
        
        svg += f'''    <path d="M {center_x} {center_y} L {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z" 
              fill="{color}" opacity="0.9"/>
'''
    
    # Draw legend
    legend_x = 310
    legend_y = 60
    
    for i, lang_data in enumerate(lang_percentages):
        y_pos = legend_y + (i * 35)
        color = green_shades[i % len(green_shades)]
        
        svg += f'''    <rect x="{legend_x}" y="{y_pos}" width="15" height="15" fill="{color}" rx="2"/>
    <text x="{legend_x + 22}" y="{y_pos + 12}" font-family="'Courier New', monospace" font-size="12" fill="{COLORS['text']}">
        {lang_data['name']}
    </text>
    <text x="{legend_x + 100}" y="{y_pos + 12}" font-family="'Courier New', monospace" font-size="11" fill="{COLORS['text_dim']}" text-anchor="end">
        {lang_data['percentage']:.1f}%
    </text>
'''
    
    svg += '''</svg>'''
    
    return svg

def generate_stats_card_svg(stats):
    """Generate custom Matrix green stats card"""
    
    svg = f'''<svg width="495" height="195" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="matrixGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{COLORS['green_1']};stop-opacity:0.1" />
            <stop offset="100%" style="stop-color:{COLORS['green_3']};stop-opacity:0.1" />
        </linearGradient>
    </defs>
    
    <rect width="495" height="195" fill="{COLORS['bg_dark']}" rx="10"/>
    <rect width="495" height="195" fill="url(#matrixGradient)" rx="10"/>
    
    <!-- Title -->
    <text x="247" y="30" font-family="'Courier New', monospace" font-size="18" fill="{COLORS['text']}" text-anchor="middle" font-weight="bold">
        &gt; MATRIX STATISTICS
    </text>
    
    <!-- Stats Grid -->
    <!-- Total Repos -->
    <text x="30" y="70" font-family="'Courier New', monospace" font-size="14" fill="{COLORS['text_dim']}">
        Public Repos
    </text>
    <text x="30" y="95" font-family="'Courier New', monospace" font-size="32" fill="{COLORS['text']}" font-weight="bold">
        {stats['repos']}
    </text>
    
    <!-- Total Stars -->
    <text x="160" y="70" font-family="'Courier New', monospace" font-size="14" fill="{COLORS['text_dim']}">
        Total Stars
    </text>
    <text x="160" y="95" font-family="'Courier New', monospace" font-size="32" fill="{COLORS['text']}" font-weight="bold">
        {stats['stars']}
    </text>
    
    <!-- Total Forks -->
    <text x="290" y="70" font-family="'Courier New', monospace" font-size="14" fill="{COLORS['text_dim']}">
        Total Forks
    </text>
    <text x="290" y="95" font-family="'Courier New', monospace" font-size="32" fill="{COLORS['text']}" font-weight="bold">
        {stats['forks']}
    </text>
    
    <!-- Followers -->
    <text x="30" y="130" font-family="'Courier New', monospace" font-size="14" fill="{COLORS['text_dim']}">
        Followers
    </text>
    <text x="30" y="155" font-family="'Courier New', monospace" font-size="32" fill="{COLORS['text']}" font-weight="bold">
        {stats['followers']}
    </text>
    
    <!-- Matrix Green Octocat with Animation -->
    <g transform="translate(420, 110)">
        {create_green_octocat_svg()}
    </g>
    
    <!-- Matrix Code Background -->
    <text x="420" y="40" font-family="'Courier New', monospace" font-size="8" fill="{COLORS['green_0']}" opacity="0.3">
        010101
    </text>
    <text x="440" y="60" font-family="'Courier New', monospace" font-size="8" fill="{COLORS['green_1']}" opacity="0.3">
        110011
    </text>
    <text x="430" y="80" font-family="'Courier New', monospace" font-size="8" fill="{COLORS['green_0']}" opacity="0.3">
        101010
    </text>
    
    <!-- Footer -->
    <text x="247" y="185" font-family="'Courier New', monospace" font-size="10" fill="{COLORS['text_dim']}" text-anchor="middle">
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
    </text>
</svg>'''
    
    return svg

def generate_profile_summary_svg():
    """Generate custom Matrix green profile summary card"""
    
    svg = f'''<svg width="900" height="250" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="profileGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:{COLORS['green_1']};stop-opacity:0.2" />
            <stop offset="50%" style="stop-color:{COLORS['green_3']};stop-opacity:0.1" />
            <stop offset="100%" style="stop-color:{COLORS['green_1']};stop-opacity:0.2" />
        </linearGradient>
    </defs>
    
    <rect width="900" height="250" fill="{COLORS['bg_dark']}" rx="10"/>
    <rect width="900" height="250" fill="url(#profileGradient)" rx="10"/>
    
    <!-- Title -->
    <text x="450" y="35" font-family="'Courier New', monospace" font-size="20" fill="{COLORS['text']}" text-anchor="middle" font-weight="bold">
        &gt; MATRIX PROFILE SUMMARY
    </text>
    
    <!-- Contribution Graph Bars (decorative) -->
'''
    
    # Add decorative contribution bars
    import random
    random.seed(42)  # For consistent output
    bar_x = 50
    for week in range(52):
        for day in range(7):
            height = random.randint(2, 12)
            opacity = random.choice([0.2, 0.4, 0.6, 0.8, 1.0])
            color = random.choice([COLORS['green_0'], COLORS['green_1'], COLORS['green_2'], COLORS['green_3']])
            svg += f'''    <rect x="{bar_x + week * 15}" y="{60 + day * 15}" width="12" height="12" fill="{color}" opacity="{opacity}" rx="2"/>
'''
    
    svg += f'''    
    <!-- Summary Text -->
    <text x="450" y="200" font-family="'Courier New', monospace" font-size="14" fill="{COLORS['text']}" text-anchor="middle">
        Matrix operations active • All systems green • Contributions flowing
    </text>
    
    <text x="450" y="230" font-family="'Courier New', monospace" font-size="11" fill="{COLORS['text_dim']}" text-anchor="middle">
        The Matrix has you, Neo. Follow the white rabbit.
    </text>
</svg>'''
    
    return svg

def generate_standalone_octocat():
    """Generate standalone Matrix green Octocat SVG"""
    svg = f'''<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg" viewBox="-50 -50 100 100">
    <defs>
        <radialGradient id="octocatGlow">
            <stop offset="0%" style="stop-color:{COLORS['green_3']};stop-opacity:0.8" />
            <stop offset="100%" style="stop-color:{COLORS['green_3']};stop-opacity:0" />
        </radialGradient>
    </defs>
    
    <!-- Glow background -->
    <circle cx="0" cy="0" r="45" fill="url(#octocatGlow)"/>
    
    <!-- Main Octocat -->
    <g transform="translate(0, 0)">
        {create_green_octocat_svg()}
    </g>
    
    <!-- Signature -->
    <text x="0" y="45" font-family="'Courier New', monospace" font-size="8" fill="{COLORS['text']}" text-anchor="middle" opacity="0.7">
        MATRIX OCTOCAT
    </text>
</svg>'''
    return svg

def main():
    """Main function to generate all custom cards"""
    print("🟢 Generating Matrix Green Statistics...")
    print("🐱 Creating Matrix Green Octocat...")
    
    # Create output directory
    os.makedirs('assets', exist_ok=True)
    
    # Generate standalone Octocat first
    octocat_svg = generate_standalone_octocat()
    with open('assets/green-octocat.svg', 'w') as f:
        f.write(octocat_svg)
    print("✅ Generated green-octocat.svg (standalone)")
    
    # Fetch stats
    stats = get_github_stats()
    print(f"✅ Fetched stats: {stats['repos']} repos, {stats['stars']} stars")
    
    # Generate stats card with Octocat
    stats_svg = generate_stats_card_svg(stats)
    with open('assets/matrix-stats.svg', 'w') as f:
        f.write(stats_svg)
    print("✅ Generated matrix-stats.svg (with animated Octocat)")
    
    # Generate language pie chart with Octocat
    if stats['languages']:
        lang_svg = generate_language_pie_svg(stats['languages'])
        with open('assets/matrix-languages.svg', 'w') as f:
            f.write(lang_svg)
        print("✅ Generated matrix-languages.svg (with Octocat corner)")
    
    # Generate profile summary
    profile_svg = generate_profile_summary_svg()
    with open('assets/matrix-profile-summary.svg', 'w') as f:
        f.write(profile_svg)
    print("✅ Generated matrix-profile-summary.svg")
    
    print("🎉 All Matrix green visualizations generated!")
    print("🟢 Green Octocat successfully integrated into all cards!")

if __name__ == '__main__':
    main()
