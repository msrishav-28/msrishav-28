#!/usr/bin/env python3
"""
Custom Matrix Green Statistics Generator
Generates fully customizable SVG cards with Matrix green theme
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
    'green_3': '#00ff41',
    'green_4': '#33ff66',
    'text': '#00ff41',
    'text_dim': '#009929',
}

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
    
    <!-- Green Octocat -->
    <g transform="translate(380, 110)">
        <path d="M0-30c-8.3 0-15 6.7-15 15 0 6.6 4.3 12.2 10.3 14.2.8.1 1-.3 1-.7v-2.6c-4.2.9-5.1-2-5.1-2-.7-1.7-1.7-2.2-1.7-2.2-1.4-.9.1-.9.1-.9 1.5.1 2.3 1.5 2.3 1.5 1.3 2.3 3.5 1.6 4.4 1.2.1-1 .5-1.6 1-2-3.3-.4-6.8-1.7-6.8-7.4 0-1.6.6-3 1.5-4-.2-.4-.7-1.9.1-4 0 0 1.3-.4 4.1 1.5 1.2-.3 2.5-.5 3.8-.5s2.6.2 3.8.5c2.9-1.9 4.1-1.5 4.1-1.5.8 2.1.3 3.6.1 4 1 1 1.5 2.4 1.5 4 0 5.8-3.5 7-6.8 7.4.5.5 1 1.4 1 2.8v4.1c0 .4.3.9 1 .7 6-2 10.2-7.6 10.2-14.2C15-23.3 8.3-30 0-30z" 
              fill="{COLORS['green_3']}"/>
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

def main():
    """Main function to generate all custom cards"""
    print("🟢 Generating Matrix Green Statistics...")
    
    # Create output directory
    os.makedirs('assets', exist_ok=True)
    
    # Fetch stats
    stats = get_github_stats()
    print(f"✅ Fetched stats: {stats['repos']} repos, {stats['stars']} stars")
    
    # Generate stats card
    stats_svg = generate_stats_card_svg(stats)
    with open('assets/matrix-stats.svg', 'w') as f:
        f.write(stats_svg)
    print("✅ Generated matrix-stats.svg")
    
    # Generate language pie chart
    if stats['languages']:
        lang_svg = generate_language_pie_svg(stats['languages'])
        with open('assets/matrix-languages.svg', 'w') as f:
            f.write(lang_svg)
        print("✅ Generated matrix-languages.svg")
    
    # Generate profile summary
    profile_svg = generate_profile_summary_svg()
    with open('assets/matrix-profile-summary.svg', 'w') as f:
        f.write(profile_svg)
    print("✅ Generated matrix-profile-summary.svg")
    
    print("🎉 All Matrix green visualizations generated!")

if __name__ == '__main__':
    main()
