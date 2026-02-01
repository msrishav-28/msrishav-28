import os
import requests
import datetime
import math

# Configuration
USERNAME = os.getenv('USERNAME', 'msrishav-28')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OUTPUT_FILE = 'assets/matrix-dashboard.svg'

# Matrix Colors
COLORS = {
    'bg': '#0d1117',
    'panel_bg': '#161b22',
    'border': '#003300',
    'text_primary': '#00ff41',
    'text_secondary': '#008f11',
    'text_dim': '#005500',
    'alert': '#ff0000', # For errors only (Matrix style usually avoids red, but useful for 'Critical')
    'bar_fill': '#00ff41',
    'bar_empty': '#003300'
}

IGNORED_LANGUAGES = {'Shell', 'HTML', 'CSS', 'Makefile', 'Jupyter Notebook', 'Dockerfile', 'Smarty', 'TeX'}

def run_graphql_query(query):
    """Executes a GraphQL query against GitHub API."""
    headers = {'Authorization': f'Bearer {GITHUB_TOKEN}'}
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(f"Query failed to run by returning code of {request.status_code}. {query}")

def fetch_data():
    """Fetches all necessary data using GraphQL."""
    print(f"🔌 Connecting to Matrix (GitHub GraphQL)...")
    
    query = f"""
    {{
      user(login: "{USERNAME}") {{
        name
        createdAt
        followers {{ totalCount }}
        repositories(first: 100, ownerAffiliations: OWNER, isFork: false, orderBy: {{field: STARGAZERS, direction: DESC}}) {{
          nodes {{
            name
            stargazerCount
            forkCount
            languages(first: 10, orderBy: {{field: SIZE, direction: DESC}}) {{
              edges {{
                size
                node {{
                  name
                  color
                }}
              }}
            }}
          }}
        }}
        contributionsCollection {{
          contributionCalendar {{
            totalContributions
            weeks {{
              contributionDays {{
                date
                contributionCount
              }}
            }}
          }}
        }}
      }}
    }}
    """
    return run_graphql_query(query)

def calculate_streak(calendar):
    """Calculates current and longest streak from contribution calendar."""
    days = []
    for week in calendar['weeks']:
        for day in week['contributionDays']:
            # GraphQL returns YYYY-MM-DD
            date_obj = datetime.datetime.strptime(day['date'], '%Y-%m-%d').date()
            count = day['contributionCount']
            days.append({'date': date_obj, 'count': count})
    
    # Sort days just in case
    days.sort(key=lambda x: x['date'])
    
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    today = datetime.date.today()
    
    # Iterate through all days to find longest streak
    for day in days:
        if day['count'] > 0:
            temp_streak += 1
        else:
            longest_streak = max(longest_streak, temp_streak)
            temp_streak = 0
    longest_streak = max(longest_streak, temp_streak) # Final check

    # Current Streak (Working backwards from today)
    # Note: GitHub calendar might not include 'today' immediately if timezone diff, 
    # but we check the last few entries.
    
    # Reverse iterate
    active_streak = 0
    # Find the index of today or yesterday (latest data)
    
    # Simple algorithm: Iterate backwards. 
    # If today has 0, check yesterday. If yesterday has 0, streak is 0.
    
    # We'll just trace backwards from the last available day
    is_streak_alive = True
    for day in reversed(days):
        if day['date'] > today:
            continue # Future?
        
        if day['count'] > 0:
            active_streak += 1
            is_streak_alive = True
        else:
            # If it's today and count is 0, streak might still be alive (haven't committed YET)
            if day['date'] == today:
                continue 
            else:
                break
    
    current_streak = active_streak
    
    return current_streak, longest_streak

def process_languages(repos):
    """Aggregates language bytes and filters noise."""
    lang_stats = {}
    total_bytes = 0
    
    for repo in repos:
        if not repo['languages']['edges']:
            continue
        
        for edge in repo['languages']['edges']:
            lang_name = edge['node']['name']
            size = edge['size']
            
            if lang_name in IGNORED_LANGUAGES:
                continue
                
            lang_stats[lang_name] = lang_stats.get(lang_name, 0) + size
            total_bytes += size
            
    # Convert to list and sort
    sorted_langs = sorted(lang_stats.items(), key=lambda item: item[1], reverse=True)
    
    # Calculate percentages
    final_stats = []
    for lang, size in sorted_langs[:6]: # Top 6
        pct = (size / total_bytes) * 100 if total_bytes > 0 else 0
        final_stats.append({'name': lang, 'pct': pct})
        
    return final_stats

def generate_svg(data, streaks, languages):
    """Renders the component as an SVG."""
    w = 800
    h = 420
    
    user = data['data']['user']
    repos = user['repositories']['nodes']
    
    # Aggregate Metrics
    total_stars = sum(r['stargazerCount'] for r in repos)
    total_forks = sum(r['forkCount'] for r in repos)
    repo_count = len(repos)
    followers = user['followers']['totalCount']
    
    # Access/Contribution Data
    contrib_calendar = user['contributionsCollection']['contributionCalendar']
    total_contribs = contrib_calendar['totalContributions']
    join_year = user['createdAt'][:4]
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    svg = f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
    <style>
        .text {{ font-family: 'Courier New', Courier, monospace; fill: {COLORS['text_primary']}; }}
        .text-dim {{ font-family: 'Courier New', Courier, monospace; fill: {COLORS['text_dim']}; }}
        .header {{ font-weight: bold; font-size: 16px; }}
        .label {{ font-size: 12px; fill: {COLORS['text_secondary']}; }}
        .value {{ font-size: 14px; font-weight: bold; }}
        .panel {{ fill: {COLORS['panel_bg']}; stroke: {COLORS['border']}; stroke-width: 1; }}
        
        /* Glitch Effect on Name */
        @keyframes glitch {{
            0% {{ transform: translate(0) }}
            20% {{ transform: translate(-2px, 2px) }}
            40% {{ transform: translate(-2px, -2px) }}
            60% {{ transform: translate(2px, 2px) }}
            80% {{ transform: translate(2px, -2px) }}
            100% {{ transform: translate(0) }}
        }}
        .glitch {{ animation: glitch 3s infinite; }}
    </style>
    
    <rect width="{w}" height="{h}" fill="{COLORS['bg']}" rx="8" />
    
    <!-- Top Bar -->
    <rect x="10" y="10" width="{w-20}" height="30" fill="{COLORS['border']}" opacity="0.3" rx="4"/>
    <text x="20" y="30" class="text header">[ SYSTEM MONITOR: {USERNAME.upper()} ]</text>
    <text x="{w-20}" y="30" class="text header" text-anchor="end">[ STATUS: CONNECTED ]</text>
    
    <!-- Panel 1: Core Metrics (Left) -->
    <rect x="20" y="60" width="370" height="200" class="panel" rx="4"/>
    <text x="35" y="85" class="text header">&gt; CORE_METRICS</text>
    
    <!-- Stars -->
    <text x="35" y="115" class="label">TOTAL STARS</text>
    <rect x="160" y="105" width="200" height="12" fill="{COLORS['bar_empty']}"/>
    <rect x="160" y="105" width="{min(total_stars*5, 200)}" height="12" fill="{COLORS['bar_fill']}"/>
    <text x="375" y="115" class="text value" text-anchor="end">{total_stars}</text>
    
    <!-- Repos -->
    <text x="35" y="145" class="label">PUBLIC REPOS</text>
    <rect x="160" y="135" width="200" height="12" fill="{COLORS['bar_empty']}"/>
    <rect x="160" y="135" width="{min(repo_count*5, 200)}" height="12" fill="{COLORS['bar_fill']}"/>
    <text x="375" y="145" class="text value" text-anchor="end">{repo_count}</text>
    
    <!-- Forks -->
    <text x="35" y="175" class="label">FORKS</text>
    <rect x="160" y="165" width="200" height="12" fill="{COLORS['bar_empty']}"/>
    <rect x="160" y="165" width="{min(total_forks*10, 200)}" height="12" fill="{COLORS['bar_fill']}"/>
    <text x="375" y="175" class="text value" text-anchor="end">{total_forks}</text>
    
    <!-- Followers -->
    <text x="35" y="205" class="label">FOLLOWERS</text>
    <rect x="160" y="195" width="200" height="12" fill="{COLORS['bar_empty']}"/>
    <rect x="160" y="195" width="{min(followers*2, 200)}" height="12" fill="{COLORS['bar_fill']}"/>
    <text x="375" y="205" class="text value" text-anchor="end">{followers}</text>
    
    <!-- Total Contribs -->
    <text x="35" y="235" class="label">PACKET_SEND</text>
    <text x="160" y="235" class="text value">{total_contribs} (Total Contribs)</text>
    
    <!-- Panel 2: Tech Stack (Right) -->
    <rect x="410" y="60" width="370" height="200" class="panel" rx="4"/>
    <text x="425" y="85" class="text header">&gt; SKILL_SPECTRUM</text>
    
    """
    
    # Language Bars
    y_offset = 115
    for lang in languages:
        name = lang['name'].upper()
        pct = lang['pct']
        bar_w = (pct / 100) * 180
        
        svg += f"""
        <text x="425" y="{y_offset}" class="label">{name}</text>
        <rect x="520" y="{y_offset-10}" width="180" height="12" fill="{COLORS['bar_empty']}"/>
        <rect x="520" y="{y_offset-10}" width="{bar_w}" height="12" fill="{COLORS['bar_fill']}"/>
        <text x="710" y="{y_offset}" class="text value">{pct:.1f}%</text>
        """
        y_offset += 30
        
    svg += f"""
    
    <!-- Panel 3: System Log (Bottom) -->
    <rect x="20" y="280" width="760" height="120" class="panel" rx="4"/>
    <text x="35" y="305" class="text header">&gt; SYSTEM_LOG</text>
    
    <text x="35" y="335" class="text value">User: {USERNAME}</text>
    <text x="35" y="355" class="text value">Init: {join_year}</text>
    <text x="35" y="375" class="text value">Time: {current_time}</text>
    
    <text x="300" y="335" class="text value">Current Streak: {streaks[0]} Days</text>
    <text x="300" y="355" class="text value">Longest Streak: {streaks[1]} Days</text>
    
    <text x="600" y="350" class="text header glitch" font-size="20">THE ONE</text>
    
    </svg>
    """
    return svg

def main():
    try:
        data = fetch_data()
        
        # Process Data
        streaks = calculate_streak(data['data']['user']['contributionsCollection']['contributionCalendar'])
        lang_stats = process_languages(data['data']['user']['repositories']['nodes'])
        
        # Generate SVG
        svg_content = generate_svg(data, streaks, lang_stats)
        
        # Save
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding="utf-8") as f:
            f.write(svg_content)
            
        print(f"✅ Dashboard generated at {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        # Optional: Generate a 'System Offline' SVG here fallback
        
if __name__ == "__main__":
    main()
