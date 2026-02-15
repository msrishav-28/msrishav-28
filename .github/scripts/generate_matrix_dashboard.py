import os
import requests
import datetime
import math

# Configuration
USERNAME = os.getenv('USERNAME', 'msrishav-28')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
DASHBOARD_FILE = 'assets/matrix-dashboard.svg'
LANG_FILE = 'assets/matrix-languages.svg'

# Matrix Colors
COLORS = {
    'bg': '#0d1117',
    'panel_bg': '#161b22',
    'border': '#003300',
    'text_primary': '#00ff41',
    'text_secondary': '#008f11',
    'text_dim': '#005500',
    'alert': '#ff0000',
    'bar_fill': '#00ff41',
    'bar_empty': '#003300'
}

IGNORED_LANGUAGES = {'Shell', 'HTML', 'CSS', 'Makefile', 'Jupyter Notebook', 'Dockerfile', 'Smarty', 'TeX'}

def run_graphql_query(query):
    """Executes a GraphQL query against GitHub API."""
    headers = {}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'Bearer {GITHUB_TOKEN}'
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        payload = request.json()
        if payload.get('errors'):
            raise Exception(f"GraphQL errors: {payload['errors']}")
        return payload
    else:
        raise Exception(f"Query failed with {request.status_code}: {request.text}")

def fetch_data():
    """Fetches all necessary data using GraphQL."""
    print(f"🔌 Connecting to Matrix (GitHub GraphQL)...")

    repos = []
    cursor = None
    user_data = None

    while True:
        after = f', after: "{cursor}"' if cursor else ''
        query = f"""
        {{
          user(login: "{USERNAME}") {{
            name
            createdAt
            followers {{ totalCount }}
            repositories(first: 100{after}, ownerAffiliations: OWNER, isFork: false, orderBy: {{field: STARGAZERS, direction: DESC}}) {{
              pageInfo {{
                hasNextPage
                endCursor
              }}
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
        response = run_graphql_query(query)
        user = response['data']['user']
        if user is None:
            raise Exception(f"User '{USERNAME}' not found or inaccessible")
        if user_data is None:
            user_data = user
        repos.extend(user['repositories']['nodes'])
        page_info = user['repositories']['pageInfo']
        if not page_info['hasNextPage']:
            break
        cursor = page_info['endCursor']

    merged_user_data = {
        **user_data,
        'repositories': {
            'nodes': repos,
            'pageInfo': {'hasNextPage': False, 'endCursor': page_info['endCursor']}
        }
    }
    return {'data': {'user': merged_user_data}}

def calculate_streak(calendar):
    """Calculates current and longest streak."""
    days = []
    for week in calendar['weeks']:
        for day in week['contributionDays']:
            date_obj = datetime.datetime.strptime(day['date'], '%Y-%m-%d').date()
            count = day['contributionCount']
            days.append({'date': date_obj, 'count': count})
    
    days.sort(key=lambda x: x['date'])
    
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    today = datetime.date.today()
    
    for day in days:
        if day['count'] > 0:
            temp_streak += 1
        else:
            longest_streak = max(longest_streak, temp_streak)
            temp_streak = 0
    longest_streak = max(longest_streak, temp_streak)

    active_streak = 0
    # Check current streak
    for day in reversed(days):
        if day['date'] > today: continue
        if day['count'] > 0:
            active_streak += 1
        elif day['date'] == today:
             continue # Today empty, but streak might be alive from yesterday
        else:
            break
            
    return active_streak, longest_streak

def process_languages(repos):
    """Aggregates language bytes and filters noise."""
    lang_stats = {}
    total_bytes = 0
    
    for repo in repos:
        if not repo['languages']['edges']: continue
        for edge in repo['languages']['edges']:
            lang_name = edge['node']['name']
            size = edge['size']
            if lang_name in IGNORED_LANGUAGES: continue
            lang_stats[lang_name] = lang_stats.get(lang_name, 0) + size
            total_bytes += size
            
    sorted_langs = sorted(lang_stats.items(), key=lambda item: item[1], reverse=True)
    final_stats = []
    for lang, size in sorted_langs[:6]: # Top 6
        pct = (size / total_bytes) * 100 if total_bytes > 0 else 0
        final_stats.append({'name': lang, 'pct': pct})
        
    return final_stats

def generate_dashboard_svg(data, streaks):
    """Renders Core Metrics + System Log (Without Languages)."""
    w, h = 800, 320 # Reduced height since languages are gone
    
    user = data['data']['user']
    repos = user['repositories']['nodes']
    
    total_stars = sum(r['stargazerCount'] for r in repos)
    total_forks = sum(r['forkCount'] for r in repos)
    repo_count = len(repos)
    followers = user['followers']['totalCount']
    total_contribs = user['contributionsCollection']['contributionCalendar']['totalContributions']
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
    
    <!-- Core Metrics Panel (Full Width) -->
    <rect x="20" y="60" width="760" height="130" class="panel" rx="4"/>
    <text x="35" y="85" class="text header">&gt; CORE_METRICS</text>
    
    <!-- Layout: 3 Columns -->
    <!-- Col 1 -->
    <text x="50" y="115" class="label">TOTAL STARS</text>
    <rect x="150" y="105" width="150" height="12" fill="{COLORS['bar_empty']}"/>
    <rect x="150" y="105" width="{min(total_stars*5, 150)}" height="12" fill="{COLORS['bar_fill']}"/>
    <text x="310" y="115" class="text value">{total_stars}</text>
    
    <text x="50" y="145" class="label">PUBLIC REPOS</text>
    <rect x="150" y="135" width="150" height="12" fill="{COLORS['bar_empty']}"/>
    <rect x="150" y="135" width="{min(repo_count*5, 150)}" height="12" fill="{COLORS['bar_fill']}"/>
    <text x="310" y="145" class="text value">{repo_count}</text>

    <!-- Col 2 -->
    <text x="350" y="115" class="label">FORKS</text>
    <rect x="420" y="105" width="100" height="12" fill="{COLORS['bar_empty']}"/>
    <rect x="420" y="105" width="{min(total_forks*10, 100)}" height="12" fill="{COLORS['bar_fill']}"/>
    <text x="530" y="115" class="text value">{total_forks}</text>
    
    <text x="350" y="145" class="label">FOLLOWERS</text>
    <rect x="420" y="135" width="100" height="12" fill="{COLORS['bar_empty']}"/>
    <rect x="420" y="135" width="{min(followers*2, 100)}" height="12" fill="{COLORS['bar_fill']}"/>
    <text x="530" y="145" class="text value">{followers}</text>

     <!-- Col 3: Stats Text -->
    <text x="600" y="115" class="label">CONTRIBUTIONS</text>
    <text x="600" y="135" class="text value" font-size="20">{total_contribs}</text>
    
    
    <!-- System Log (Bottom) -->
    <rect x="20" y="210" width="760" height="90" class="panel" rx="4"/>
    <text x="35" y="235" class="text header">&gt; SYSTEM_LOG</text>
    
    <text x="35" y="260" class="text value">User: {USERNAME} | Init: {join_year} | Time: {current_time}</text>
    <text x="35" y="280" class="text value">Current Streak: {streaks[0]} Days | Longest Streak: {streaks[1]} Days</text>
    
    <text x="650" y="270" class="text header glitch" font-size="20">THE ONE</text>
    
    </svg>"""
    return svg

def generate_languages_svg(languages):
    """Renders specific Language Distribution SVG (Wide)."""
    w, h = 800, 250
    
    svg = f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
    <style>
        .text {{ font-family: 'Courier New', Courier, monospace; fill: {COLORS['text_primary']}; }}
        .header {{ font-weight: bold; font-size: 16px; }}
        .label {{ font-size: 12px; fill: {COLORS['text_secondary']}; }}
        .value {{ font-size: 14px; font-weight: bold; }}
        .panel {{ fill: {COLORS['panel_bg']}; stroke: {COLORS['border']}; stroke-width: 1; }}
    </style>
    
    <rect width="{w}" height="{h}" fill="{COLORS['bg']}" rx="8" />
    
    <rect x="20" y="20" width="760" height="210" class="panel" rx="4"/>
    <text x="35" y="45" class="text header">&gt; SKILL_SPECTRUM_ANALYSIS</text>
    
    """
    
    # Render bars in 2 columns
    col1_x = 50
    col2_x = 420
    y_start = 80
    row_height = 40
    
    for i, lang in enumerate(languages):
        name = lang['name'].upper()
        pct = lang['pct']
        bar_w = (pct / 100) * 250 # Wider bars
        
        x_pos = col1_x if i < 3 else col2_x
        y_pos = y_start + ((i % 3) * row_height)
        
        svg += f"""
        <text x="{x_pos}" y="{y_pos}" class="label">{name}</text>
        <rect x="{x_pos+100}" y="{y_pos-10}" width="200" height="14" fill="{COLORS['bar_empty']}"/>
        <rect x="{x_pos+100}" y="{y_pos-10}" width="{bar_w}" height="14" fill="{COLORS['bar_fill']}"/>
        <text x="{x_pos+310}" y="{y_pos}" class="text value">{pct:.1f}%</text>
        """
        
    svg += "</svg>"
    return svg

def generate_fallback_svg(filename, error_msg):
    w, h = 800, 200
    svg = f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
        <style>.text {{ font-family: 'Courier New', monospace; fill: #00ff41; }}</style>
        <rect width="{w}" height="{h}" fill="#0d1117" rx="8" />
        <text x="50%" y="50%" class="text" text-anchor="middle" font-size="20">SYSTEM OFFLINE: {error_msg}</text>
    </svg>"""
    with open(filename, 'w') as f: f.write(svg)

def main():
    try:
        data = fetch_data()
        streaks = calculate_streak(data['data']['user']['contributionsCollection']['contributionCalendar'])
        lang_stats = process_languages(data['data']['user']['repositories']['nodes'])
        
        # 1. Generate Main Dashboard
        dash_svg = generate_dashboard_svg(data, streaks)
        with open(DASHBOARD_FILE, 'w', encoding="utf-8") as f: f.write(dash_svg)
        print(f"✅ Dashboard generated at {DASHBOARD_FILE}")
        
        # 2. Generate Language Matrix
        lang_svg = generate_languages_svg(lang_stats)
        with open(LANG_FILE, 'w', encoding="utf-8") as f: f.write(lang_svg)
        print(f"✅ Languages generated at {LANG_FILE}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        generate_fallback_svg(DASHBOARD_FILE, "API Error")
        generate_fallback_svg(LANG_FILE, "API Error")

if __name__ == "__main__":
    main()
