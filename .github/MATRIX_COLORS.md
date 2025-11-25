# Matrix Green Color Palette

This document defines the consistent Matrix green color scheme used across all visualizations in the profile README.

## Primary Matrix Green
- **Main Green**: `#00ff41` - The iconic Matrix green color used for primary elements

## Green Shades (Dark to Light)

### Darker Shades
- **Level 0 (Background)**: `#0d1117` - Dark background matching GitHub dark theme
- **Level 1 (Darkest Green)**: `#00661a` - Dark green for lowest contribution levels
- **Level 2 (Medium Dark Green)**: `#009929` - Medium dark green

### Lighter Shades
- **Level 3 (Medium Green)**: `#00cc33` - Medium bright green
- **Level 4 (Brightest Green)**: `#00ff41` - Bright Matrix green for highest activity

### Accent Shades (for variety in charts)
- **Accent 1**: `#33ff66` - Light green
- **Accent 2**: `#66ff8c` - Lighter green
- **Accent 3**: `#99ffb3` - Very light green

## Usage Across Components

### 3D Contribution Graph
```yaml
backgroundColor: #0d1117
foregroundColor: #00ff41
strongColor: #00ff41
weakColor: #00661a
radarColor: #00ff41
contribColors: [#0d1117, #00661a, #009929, #00cc33, #00ff41]
```

### Snake Animation
- Background: `#0d1117`
- Snake Color: `#00ff41`
- Contribution Levels: `#0d1117`, `#00661a`, `#009929`, `#00cc33`, `#00ff41`

### Pie Charts & Language Stats
- Uses 6 shades: `#00ff41`, `#00cc33`, `#009929`, `#33ff66`, `#66ff8c`, `#99ffb3`

### Activity Graphs
- Background: `#0d1117`
- Line/Color: `#00ff41`
- Points: `#00ff41`
- Area: `#00ff41`

### Profile Cards
- Theme: `github_dark` (maintains consistency with Matrix green elements)

## Workflow Configuration

### Profile 3D Contribution
- **Workflow**: `.github/workflows/profile-3d.yml`
- **Schedule**: Daily at midnight UTC
- **Output**: `profile-3d-contrib/profile-night-green.svg`

### Snake Animation
- **Workflow**: `.github/workflows/snake.yml`
- **Schedule**: Every 12 hours
- **Output**: `github-contribution-grid-snake-dark.svg`

## Testing Workflows

To manually trigger workflows:
1. Go to GitHub repository → Actions tab
2. Select the workflow (e.g., "Generate Snake" or "GitHub-Profile-3D-Contrib")
3. Click "Run workflow" → "Run workflow"

## Notes
- All colors maintain WCAG AA contrast ratio for accessibility
- Colors are optimized for GitHub's dark theme (`#0d1117` background)
- Consistent green palette creates cohesive Matrix-themed profile
