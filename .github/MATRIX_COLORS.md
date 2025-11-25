# Matrix Green Color Palette

This document defines the consistent Matrix green color scheme used across all visualizations in the profile README, supporting both **GitHub Light Mode** and **GitHub Dark Mode**.

## Theme Support

All visualizations automatically adapt to the user's GitHub theme preference using the `<picture>` element with `prefers-color-scheme` media queries.

## Dark Mode Colors

### Primary Matrix Green
- **Main Green**: `#00ff41` - The iconic Matrix green color used for primary elements

### Green Shades (Dark to Light)
- **Level 0 (Background)**: `#0d1117` - Dark background matching GitHub dark theme
- **Level 1 (Darkest Green)**: `#00661a` - Dark green for lowest contribution levels
- **Level 2 (Medium Dark Green)**: `#009929` - Medium dark green
- **Level 3 (Medium Green)**: `#00cc33` - Medium bright green
- **Level 4 (Brightest Green)**: `#00ff41` - Bright Matrix green for highest activity

### Accent Shades (for variety in charts)
- **Accent 1**: `#33ff66` - Light green
- **Accent 2**: `#66ff8c` - Lighter green
- **Accent 3**: `#99ffb3` - Very light green

## Light Mode Colors

### Primary Green
- **Main Green**: `#008000` - Dark green for readability on white background

### Green Shades (Light to Dark)
- **Level 0 (Background)**: `#ffffff` or `#ebedf0` - White/light gray background
- **Level 1 (Lightest Green)**: `#99ffb3` - Very light green for lowest contribution
- **Level 2 (Light Green)**: `#33ff66` - Light green
- **Level 3 (Medium Green)**: `#00cc33` - Medium green
- **Level 4 (Darkest Green)**: `#008000` - Dark green for highest activity

### Accent Shades
- Text/Icons: `#008000` - Dark green for contrast
- Highlights: `#00cc33` - Medium bright green

## Usage Across Components

### 3D Contribution Graph

**Dark Mode:**
```yaml
backgroundColor: #0d1117
foregroundColor: #00ff41
strongColor: #00ff41
weakColor: #00661a
radarColor: #00ff41
contribColors: [#0d1117, #00661a, #009929, #00cc33, #00ff41]
```

**Light Mode:**
```yaml
backgroundColor: #ffffff
foregroundColor: #008000
strongColor: #00cc33
weakColor: #99ffb3
radarColor: #00cc33
contribColors: [#ebedf0, #99ffb3, #33ff66, #00cc33, #008000]
```

### Snake Animation

**Dark Mode:**
- Background: `#0d1117`
- Snake Color: `#00ff41`
- Contribution Levels: `#0d1117`, `#00661a`, `#009929`, `#00cc33`, `#00ff41`

**Light Mode:**
- Background: `#ebedf0`
- Snake Color: `#008000`
- Contribution Levels: `#ebedf0`, `#99ffb3`, `#33ff66`, `#00cc33`, `#008000`

### GitHub Stats & Language Charts

**Dark Mode:**
- Background: `#0d1117`
- Title: `#00ff41`
- Text: `#00ff41`
- Icons: `#00ff41`

**Light Mode:**
- Background: `#ffffff`
- Title: `#008000`
- Text: `#008000`
- Icons: `#00cc33`

### Activity Graphs

**Dark Mode:**
- Background: `#0d1117`
- Line/Color: `#00ff41`
- Points: `#00ff41`
- Area: `#00ff41` (with transparency)

**Light Mode:**
- Background: `#ffffff`
- Line/Color: `#00cc33`
- Points: `#00cc33`
- Area: `#99ffb3` (with transparency)

### Profile Summary Cards

**Dark Mode:** `theme=github_dark`
**Light Mode:** `theme=github`

### Trophies

**Dark Mode:** `theme=matrix`
**Light Mode:** `theme=flat`

## Workflow Configuration

### Profile 3D Contribution
- **Workflow**: `.github/workflows/profile-3d.yml`
- **Schedule**: Daily at midnight UTC
- **Outputs**:
  - Dark Mode: `profile-3d-contrib/profile-night-green.svg`
  - Light Mode: `profile-3d-contrib/profile-green-animate.svg`

### Snake Animation
- **Workflow**: `.github/workflows/snake.yml`
- **Schedule**: Every 12 hours
- **Outputs**:
  - Dark Mode: `github-contribution-grid-snake-dark.svg`
  - Light Mode: `github-contribution-grid-snake.svg`

## Testing Workflows

To manually trigger workflows:
1. Go to GitHub repository → Actions tab
2. Select the workflow (e.g., "Generate Snake" or "GitHub-Profile-3D-Contrib")
3. Click "Run workflow" → "Run workflow"

## Notes

### Accessibility
- All color combinations maintain **WCAG AA contrast ratio** for accessibility
- Dark mode colors optimized for GitHub's dark theme (`#0d1117` background)
- Light mode colors optimized for white/light backgrounds (`#ffffff` or `#ebedf0`)

### Theme Switching
- Uses native HTML `<picture>` element with `media="(prefers-color-scheme: dark|light)"`
- Automatically adapts to user's GitHub theme preference
- No JavaScript required - works with GitHub's built-in theme system

### Consistency
- Matrix green (`#00ff41`) remains the iconic color in dark mode
- Dark green (`#008000`) provides readability in light mode
- Green gradient maintains consistent visual hierarchy across both themes
- All visualizations use coordinated color palettes for cohesive appearance

### Browser Support
- Works in all modern browsers (Chrome, Firefox, Safari, Edge)
- Falls back to dark mode version if `prefers-color-scheme` is not supported
- GitHub automatically handles caching and CDN delivery of SVG assets
