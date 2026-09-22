# Read. Earn. Build. — Reading Reward App Spec

A reading-reward tracker for a 7-year-old. Every finished book earns points; points unlock real PC parts for a gaming computer he and Dad are building together. This document is the full spec — rules, data model, screens, and logic — for building it as a phone app. A working web version exists as `reading-reward-tracker.html` (single-file HTML/JS) and can be used as a reference implementation.

---

## 1. Goal

- Total goal: **1,600 points**.
- Target pace: **100–250 points per week** (roughly 10–12 weeks to finish).
- Points are earned per finished book, scaled by difficulty tier, with rules for re-reads, a stretch bonus, and a weekly cap.

## 2. Book tiers

Tier is chosen by the parent when logging a book. Value is the base points for a first read.

| Points | Name | Description | Examples |
|---|---|---|---|
| 1 | Tiny | Board books or a few words per page, read out loud on his own | — |
| 2 | Short | Short picture books he reads himself | Biscuit, Bob Books, Hop on Pop |
| 5 | Picture | Longer picture books or level 1–2 readers | Little Bear, Henry and Mudge, Splat the Cat |
| 10 | Easy | Easy readers he reads all by himself | Elephant & Piggie, Pete the Cat, Frog and Toad, Fly Guy |
| 20 | Early chapter | ~60–100 pages, a few pictures | Magic Tree House, Dog Man, Owl Diaries, Mercy Watson |
| 40 | Chapter | ~100–180 pages | Captain Underpants, Diary of a Wimpy Kid, The Bad Guys, Zoey and Sassafras |
| 70 | Big | ~180–250 pages, mostly words | The Wild Robot, Charlotte's Web, Because of Winn-Dixie |
| 100 | Giant | 250+ pages, a real challenge | Harry Potter 1, Percy Jackson, How to Train Your Dragon, Narnia |

Tier colors (used for buttons, log dots, and the track):

```
1:  #7a8aa0    2:  #4f9aa8    5:  #5aa864    10: #2e8b57
20: #2f6fb3    40: #6a3fa0    70: #e07b1a    100: #c8402c
```

## 3. Rules

1. **Book report required.** A book only counts after a 2-minute book report to Dad: favorite part, what happened, one thing he'd change. The app enforces this with a required "Book report given to Dad" checkbox before points can be added.
2. **Re-reads pay less.** Re-reads are detected by matching the title (case-insensitive, punctuation stripped) against previously logged books.
   - 1st read: 100% of tier value
   - 2nd read: 50%
   - 3rd read and beyond: 25%
   - Round to the nearest whole point.
3. **Stretch bonus: +20.** The first time he finishes a book from a harder tier than he's read before. Parent toggles this manually when logging (a checkbox).
4. **Read-aloud counts, audiobooks don't.** Reading out loud to Dad earns full value. Audiobooks alone earn nothing. (Not enforced by the app — a house rule shown on the Rules screen.)
5. **Weekly cap: 250 points.** The week runs Monday 00:00 → Sunday 23:59 local time. If an award would push the week over 250, trim it to whatever room is left. If there's no room left, the award is 0 and the Add button stays disabled with a "weekly cap reached" note.

### Award formula

```
base   = round(tier × multiplier)        // multiplier = 1 / 0.5 / 0.25 by read number
bonus  = stretchBonus ? 20 : 0
raw    = base + bonus
room   = max(0, 250 − pointsEarnedThisWeek)
award  = min(raw, room)
```

## 4. Milestones

Cumulative point thresholds. A milestone is **unlocked** when total points ≥ threshold. Unlocking means the part gets added to the Amazon cart.

| Cumulative points | Part | Note |
|---|---|---|
| 100 | PC case | The box that holds it all |
| 200 | Power supply | Gives the parts electricity |
| 250 | CPU cooler | Thermalright Peerless Assassin 120 Vision MAX (with screen) |
| 700 | CPU + motherboard | Ryzen 7 5800XT + ASUS ROG Strix B550-F Gaming WiFi II |
| 850 | SSD 1 TB | Where the games live |
| 1,100 | RAM | Corsair Vengeance LPX 32 GB DDR4-3200 |
| 1,600 | Graphics card | Radeon RX 9060 XT 16 GB — runs BeamNG, Farming Sim, Roblox |

Milestone order and thresholds should be editable by the parent (see §7, nice-to-haves) but ship with these defaults.

## 5. Data model

One record per logged book.

```json
{
  "id": "string, unique (e.g. timestamp + random)",
  "title": "string, as entered",
  "tier": 1 | 2 | 5 | 10 | 20 | 40 | 70 | 100,
  "pts": "integer, points actually awarded after re-read scaling, bonus, and cap",
  "readNum": "integer, 1 for first read, 2 for second, ...",
  "bonus": 0 | 20,
  "ts": "integer, Unix ms when logged"
}
```

Derived values (never stored, always computed from the records):

- `total` = sum of `pts` across all records
- `weekPts` = sum of `pts` where `ts` ≥ start of the current week (Monday 00:00 local)
- `nextMilestone` = first milestone with `threshold > total`
- `readNum` for a new entry = count of existing records with matching normalized title + 1

Storage: local on-device is fine for v1 (SQLite / Core Data / AsyncStorage). If two devices should share one log (Dad's phone + kid's tablet), sync through a small cloud store (Firebase, Supabase, iCloud/CloudKit). The web version uses a shared document store with the same record shape.

## 6. Screens

### 6.1 Home (single scrolling screen in the web version; can be split into tabs on mobile)

**Hero**
- App title: "Read. Earn. Build."
- Big total: current points (large, gold), "of 1,600 points"
- Next-up line: "**N** more points to unlock the **[part]**" — or "You did it! Every part is unlocked." when total ≥ 1,600

**Progress track**
- A horizontal race-track graphic: green verge, dark road with dashed center line, checkered flag at the end.
- A small cartoon car sits at `total / 1600` along the track; the road behind it is highlighted gold.
- Each milestone is a flag post on the track, labeled with the part name and its point threshold; alternate labels above/below the road. Unlocked milestones turn green and show ✓.

**Add a book** (form)
- Book title (text input)
- Tier picker: 8 large colored buttons (1 / 2 / 5 / 10 / 20 / 40 / 70 / 100), two rows of four; selected one is highlighted with a gold outline. Tapping shows a one-line help text describing the tier with examples.
- Checkbox: "Stretch bonus — first book from a harder tier (+20)"
- Checkbox: "Book report given to Dad" (required)
- Live preview: "This book earns **+N**" with a reason string, e.g. "2nd read · half points · +20 bonus · trimmed to weekly cap"
- Big gold "Add points" button, disabled until title, tier, and report checkbox are set and the award > 0
- Success message: `+N points for "Title"!`

**Milestones list**
- One row per milestone: checkbox (green ✓ when unlocked), part name, one-line description, and either the threshold or "unlocked". The next-up milestone is highlighted.

**This week**
- "**N** of 250 points (resets Monday)" with a progress bar.

**Book log**
- Newest first. Each row: tier color dot, title, date · tier · read # · bonus flag, `+N`, and a remove (×) button with a confirm dialog. Removing a book recalculates totals.

**Rules**
- The five house rules, in kid-readable language.

### 6.2 Optional: kid mode vs. parent mode
- Kid mode: read-only home screen (total, track, milestones, log). Big, fun, no form.
- Parent mode (PIN or Face ID): the Add-a-book form and remove buttons.

## 7. Nice-to-haves (not in the web version)

- Confetti / sound on milestone unlock; the car "revs" when points are added.
- Push a notification on Monday: "New week! 250 points available."
- Parent-editable settings: goal total, weekly cap, tier values, milestone list and thresholds.
- Photo of the book cover on each log entry (camera or barcode/ISBN lookup to autofill the title).
- Export the log as CSV.
- Two-device sync (see §5).

## 8. Visual style

- Typeface: **Fredoka** (Google Fonts), rounded and friendly; fall back to Nunito / system rounded sans.
- Palette: navy hero `#1b2f57`, sky blue `#2f6fb3`, gold accent `#ffcc33` (points, buttons, car), light blue page background `#eaf2fb`, white panels with a flat 6 px bottom shadow. Dark mode: navy backgrounds `#0f1a2e` / `#182642`.
- Big touch targets (min 44 pt), one screen of content per section, large numbers. It's for a 7-year-old and a parent using it one-handed.

## 9. Reference implementation

`reading-reward-tracker.html` — self-contained HTML/CSS/JS, no build step. All of the logic in §3–§5 lives in the `<script>` block: `computeAward()`, `weekStart()`, `norm()` (title normalization), `render()`, `renderTrack()`. Port these functions directly; they are framework-agnostic.
