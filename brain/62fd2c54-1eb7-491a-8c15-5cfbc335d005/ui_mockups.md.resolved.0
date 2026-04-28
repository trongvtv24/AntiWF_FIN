# 🎨 YT-Intel — UI Mockups & Design Specs

## 📱 Màn hình 1: Dashboard

![Dashboard](C:\Users\Trong\.gemini\antigravity\brain\62fd2c54-1eb7-491a-8c15-5cfbc335d005\ytintel_dashboard_1777069850473.png)

**Key elements:**
- 4 stat cards: Channels / Videos / New Today / Alerts
- Trending Videos panel (48h hottest by view/hr)
- Recent Alerts feed + API Quota progress bars
- Scheduler status bar at bottom

---

## 📺 Màn hình 2: Channel Detail

![Channel Detail](C:\Users\Trong\.gemini\antigravity\brain\62fd2c54-1eb7-491a-8c15-5cfbc335d005\ytintel_channel_detail_1777069869360.png)

**Key elements:**
- Channel header với avatar, subs count, VIP badge, group badge
- Subscriber Growth line chart (30 ngày)
- Video list với metrics inline + Transcript/Comment quick actions

---

## 📝 Màn hình 3: Video Detail + Transcript

![Video Detail](C:\Users\Trong\.gemini\antigravity\brain\62fd2c54-1eb7-491a-8c15-5cfbc335d005\ytintel_video_detail_1777069883404.png)

**Key elements:**
- Video header: thumbnail + title + meta
- Metrics row: Views / Likes / Comments / Engagement %
- View Velocity chart (1h → 30d growth curve)
- Transcript viewer với timestamps + Export dropdown (MD/TXT)
- Tab system: Transcript | Comments | Notes

---

## 🎨 Design System

### Color Palette
| Token | Hex | Dùng cho |
|-------|-----|---------|
| `--bg-primary` | `#0F0F13` | Background toàn app |
| `--bg-surface` | `#1A1A24` | Cards, sidebar |
| `--bg-elevated` | `#22223A` | Hover, elevated cards |
| `--accent-red` | `#FF2D55` | Active nav, CTA buttons, Export |
| `--accent-blue` | `#4F8EF7` | Views metric, charts, links |
| `--accent-green` | `#34D399` | Growth indicators, positive |
| `--accent-yellow` | `#FBBF24` | Warnings, neutral metrics |
| `--text-primary` | `#F0F0F8` | Nội dung chính |
| `--text-secondary` | `#9999B8` | Labels, muted text |
| `--border` | `#2A2A40` | Subtle borders |

### Typography
| Element | Font | Size | Weight |
|---------|------|------|--------|
| App Logo | Inter | 18px | 700 |
| Page Title | Inter | 24px | 600 |
| Card Metric | Inter | 28px | 700 |
| Body | Inter | 14px | 400 |
| Label/Muted | Inter | 12px | 400 |
| Timestamp | JetBrains Mono | 12px | 400 |

### Spacing
| Token | Value |
|-------|-------|
| `--space-xs` | 4px |
| `--space-sm` | 8px |
| `--space-md` | 16px |
| `--space-lg` | 24px |
| `--space-xl` | 32px |

### Border Radius
| Element | Radius |
|---------|--------|
| Cards | 12px |
| Buttons | 8px |
| Badges/Pills | 999px |
| Charts | 8px |

### Shadows
```css
--shadow-card: 0 2px 8px rgba(0, 0, 0, 0.4);
--shadow-elevated: 0 8px 24px rgba(0, 0, 0, 0.5);
--glow-red: 0 0 12px rgba(255, 45, 85, 0.25);
--glow-blue: 0 0 12px rgba(79, 142, 247, 0.25);
--glow-green: 0 0 12px rgba(52, 211, 153, 0.2);
```

### Animations
| Name | Duration | Easing | Dùng cho |
|------|----------|--------|---------|
| hover-lift | 150ms | ease-out | Card hover |
| fade-in | 200ms | ease-in | Page transitions |
| skeleton-pulse | 1.5s | ease-in-out | Loading states |

---

## 🧩 Component Specs

### MetricCard
```
Width: flex (4 equal columns)
Height: 88px
Padding: 16px
Border: 1px solid #2A2A40
Border-radius: 12px
Hover: background → #22223A, subtle glow

Structure:
  [Icon 20px] [Label 12px muted]
  [Big Number 28px bold]
  [Trend indicator: ↑ +12% in accent-green]
```

### VideoRow
```
Height: 72px
Padding: 12px 16px
Thumbnail: 112×63px (16:9), border-radius: 6px
Hover: background → #22223A

Right side stats (inline):
  👁 [views] | 👍 [likes] | 💬 [comments]
  [Engagement badge: pill, green if >3%]
  [Views/hr: bold if trending 🔥]
  [📝 Transcript button] [💬 button]
```

### SentimentBadge
```
question: background #2A2A60, text #818CF8, icon ❓
positive: background #052E16, text #34D399, icon 😊
negative: background #2D0A0A, text #F87171, icon 😞
neutral:  background #1A1A24, text #9999B8, icon 😐
```

### QuotaBar
```
Height: 6px
Border-radius: 999px
Track: #2A2A40
Fill: 
  >50%: #34D399 (green)
  20-50%: #FBBF24 (yellow)
  <20%: #FF2D55 (red urgent)
```
