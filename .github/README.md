# GitHub Profile Configuration & Automation

This folder contains all configuration files, workflows, and documentation for the Matrix-themed GitHub profile README.

## 📁 Directory Structure

```
.github/
├── workflows/              # GitHub Actions workflows
│   ├── profile-3d.yml      # 3D contribution graph generation
│   ├── snake.yml           # Snake animation generation
│   └── update-readme.yml   # Recent activity updates
├── MATRIX_COLORS.md        # Color palette reference (dark & light modes)
├── DUAL_MODE_IMPLEMENTATION.md  # Theme switching implementation guide
├── AUTOMATION_STATUS.md    # Component update schedules & status
└── README.md              # This file
```

## 🎯 Quick Start

### Initial Setup (One-time)

1. **Repository Settings**
   - Enable GitHub Actions: `Settings` → `Actions` → `General` → Allow all actions
   - Enable workflow permissions: `Settings` → `Actions` → `General` → Read and write permissions

2. **Manual First Run**
   ```bash
   # Go to Actions tab and manually run:
   - GitHub-Profile-3D-Contrib
   - Generate Snake
   ```

3. **Verify**
   - Check that files are generated in `profile-3d-contrib/` and `output/` branch
   - View your profile in both light and dark modes
   - Confirm all visualizations display correctly

### That's It! 🎉

Everything now updates automatically:
- **Real-time components**: Update on every page view (no action needed)
- **3D Graph**: Updates daily at midnight UTC
- **Snake Animation**: Updates every 12 hours

## 🔄 Workflows

### profile-3d.yml - 3D Contribution Graph

**Purpose**: Generate a 3D isometric view of GitHub contributions

**Schedule**: Daily at 00:00 UTC

**Outputs**:
- `profile-3d-contrib/profile-night-green.svg` (Dark mode - Matrix green)
- `profile-3d-contrib/profile-green-animate.svg` (Light mode - Green animated)

**Colors**:
- Dark: `#00661a` → `#009929` → `#00cc33` → `#00ff41`
- Light: `#ebedf0` → `#99ffb3` → `#33ff66` → `#00cc33` → `#008000`

**Manual Trigger**: Actions tab → GitHub-Profile-3D-Contrib → Run workflow

---

### snake.yml - Contribution Snake Animation

**Purpose**: Generate animated snake eating GitHub contributions

**Schedule**: Every 12 hours (00:00 and 12:00 UTC)

**Outputs**:
- `github-contribution-grid-snake-dark.svg` (Dark mode)
- `github-contribution-grid-snake.svg` (Light mode)
- Deployed to `output` branch

**Colors**:
- Dark: Snake `#00ff41`, dots from `#0d1117` to `#00ff41`
- Light: Snake `#008000`, dots from `#ebedf0` to `#008000`

**Manual Trigger**: Actions tab → Generate Snake → Run workflow

---

### update-readme.yml - Recent Activity

**Purpose**: Update recent activity section in README

**Schedule**: As configured (check workflow file)

**Output**: Updates `<!--START_SECTION:activity-->` section

**Manual Trigger**: Actions tab → Update README → Run workflow

## 🎨 Color System

The profile uses a consistent Matrix green color scheme across all components.

### Dark Mode Palette
```
#0d1117 (background) → #00661a → #009929 → #00cc33 → #00ff41 (bright)
```

### Light Mode Palette
```
#ffffff (background) → #99ffb3 → #33ff66 → #00cc33 → #008000 (dark)
```

**Full Details**: See [MATRIX_COLORS.md](./MATRIX_COLORS.md)

## 🔧 Customization Guide

### Change Colors

Edit the workflow files:

**For 3D Graph** (`profile-3d.yml`):
```yaml
contribColors: [
  "#0d1117",  # No contributions
  "#00661a",  # Low
  "#009929",  # Medium-low
  "#00cc33",  # Medium-high
  "#00ff41"   # High
]
```

**For Snake** (`snake.yml`):
```yaml
color_dots=0d1117,00661a,009929,00cc33,00ff41
```

### Change Update Schedule

**3D Graph** (`profile-3d.yml`):
```yaml
on:
  schedule:
    - cron: "0 0 * * *"  # Minute Hour Day Month DayOfWeek
```

**Snake** (`snake.yml`):
```yaml
on:
  schedule:
    - cron: "0 */12 * * *"  # Every 12 hours
```

**Cron Examples**:
- `0 0 * * *` - Daily at midnight
- `0 */6 * * *` - Every 6 hours
- `0 0 * * 1` - Every Monday
- `0 0 1 * *` - First day of month

### Add New Visualizations

1. Choose appropriate dual-mode implementation method:
   - **SVG files in repo**: Use `#gh-dark-mode-only` / `#gh-light-mode-only`
   - **External APIs**: Use `<picture>` element

2. Follow color guidelines from [MATRIX_COLORS.md](./MATRIX_COLORS.md)

3. Test in both light and dark modes

4. Update documentation

## 📊 Component Matrix

| Component | Type | Updates | Dual Mode | Method |
|-----------|------|---------|-----------|--------|
| GitHub Stats | API | Real-time | ✅ | Picture |
| Streak Stats | API | Real-time | ✅ | Picture |
| Languages | API | Real-time | ✅ | Picture |
| Activity Graph | API | Real-time | ✅ | Picture |
| 3D Graph | Workflow | Daily | ✅ | Fragment |
| Snake | Workflow | 12hrs | ✅ | Fragment |
| Trophies | API | Real-time | ✅ | Picture |
| Profile Cards | API | Real-time | ✅ | Picture |

## 🐛 Troubleshooting

### Workflow Fails

**Check**:
1. Actions tab for error details
2. Repository permissions (Settings → Actions)
3. Token permissions (`contents: write` required)

**Fix**:
- Re-run failed workflow
- Check for rate limits
- Verify GITHUB_TOKEN is valid

### Images Not Displaying

**Check**:
1. Files exist in repository (`profile-3d-contrib/`, `output` branch)
2. URLs in README match actual file names
3. Browser cache (try hard refresh: Ctrl+Shift+R)

**Fix**:
- Manually trigger workflows
- Wait for CDN cache to clear (up to 24 hours)
- Check raw file URLs in browser

### Theme Not Switching

**Check**:
1. GitHub theme setting (not OS theme)
2. Browser supports `prefers-color-scheme`
3. URLs are correct for both modes

**Fix**:
- Switch GitHub theme in Settings
- Try different browser
- Clear cache

### Colors Don't Match

**Check**:
1. Workflow configuration matches [MATRIX_COLORS.md](./MATRIX_COLORS.md)
2. Recent workflow runs completed successfully
3. Using latest file versions

**Fix**:
- Re-run workflows after color changes
- Wait for cache to clear
- Manually verify color codes

## 📚 Documentation

- **[MATRIX_COLORS.md](./MATRIX_COLORS.md)**: Complete color palette reference
- **[DUAL_MODE_IMPLEMENTATION.md](./DUAL_MODE_IMPLEMENTATION.md)**: Theme switching technical guide
- **[AUTOMATION_STATUS.md](./AUTOMATION_STATUS.md)**: Update schedules and automation details

## 🚀 Performance Tips

1. **Don't over-trigger workflows**: Let automatic schedules work
2. **API rate limits**: External APIs have rate limiting
3. **Cache awareness**: Some components cache for up to 1 hour
4. **Workflow limits**: GitHub has monthly action minutes limit

## ✨ Zero Maintenance Required

Once set up, the profile is **100% automated**:

- ✅ Real-time API components refresh automatically
- ✅ Workflows run on schedule automatically
- ✅ Theme switching works automatically
- ✅ No manual updates needed

Just push code and let GitHub Actions do the work! 🎉

## 📞 Support

If you encounter issues:

1. Check [AUTOMATION_STATUS.md](./AUTOMATION_STATUS.md)
2. Review workflow logs in Actions tab
3. Verify files in [MATRIX_COLORS.md](./MATRIX_COLORS.md)
4. Clear browser cache and retry

---

**Profile Status**: ✅ Fully Automated  
**Theme Support**: ✅ Light & Dark  
**Maintenance**: ✅ Zero Required  
**Matrix Aesthetic**: ✅ Consistent

*"Welcome to the real world, Neo."* - Morpheus
