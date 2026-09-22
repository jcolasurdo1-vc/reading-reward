# Read. Earn. Build.

Reading reward tracker for a 7-year-old: every finished book earns points, points unlock PC parts.
Installable phone app (PWA), no app store needed.

- `index.html` — the whole app (logic in the `<script>` block: `computeAward`, `weekStart`, `norm`, `render`, `renderTrack`)
- `manifest.webmanifest`, `sw.js`, `icons/` — what makes it installable and work offline
- `icons/make_icons.py` — regenerates the icons (needs Pillow)
- `SPEC.md` — rules, data model, screens

## Install on a phone
1. Open the GitHub Pages URL in Safari (iPhone) or Chrome (Android).
2. iPhone: Share → **Add to Home Screen**. Android: menu → **Install app** / **Add to Home screen**.
3. Tap **Parent** and set a 4-digit PIN. Kids see the totals and log; parents add and remove books.

Data is stored on the device. Use **Parent → Backup → Save backup** now and then, and **Restore backup** to move the log to another phone.

## Ship an update
Edit, bump `VERSION` in `sw.js`, commit, push. Phones pick up the new version on the next open.
