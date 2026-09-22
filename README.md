# Read. Earn. Build.

Reading reward tracker for kids: every finished book earns points, points unlock rewards the parent picks.
Installable phone app (PWA), no app store needed. Live at https://jcolasurdo1-vc.github.io/reading-reward/

- `index.html` — the whole app (logic in the `<script>` block: `computeAward`, `weekStart`, `norm`, `render`, `renderTrack`)
- `manifest.webmanifest`, `sw.js`, `icons/` — what makes it installable and work offline
- `icons/make_icons.py` — regenerates the icons (needs Pillow)
- `SPEC.md` — rules, data model, screens

## Install on a phone
1. Open the GitHub Pages URL in Safari (iPhone) or Chrome (Android).
2. iPhone: Share → **Add to Home Screen**. Android: menu → **Install app** / **Add to Home screen**.
3. Tap **Parent** and set a 4-digit PIN. Kids see the totals and log; parents add and remove books.
4. In **Settings**, set your own rewards (name, description, points needed), the point value of each book level, the weekly cap, the stretch bonus, and the grown-up's name. The goal total is the biggest reward's threshold. The defaults are one family's PC-build list as an example.

Anyone can use it: share the link (there's a **Share this app** button in Settings). Each phone keeps its own log and settings.

Data and settings are stored on the device. Use **Parent → Backup → Save backup** now and then, and **Restore backup** to move the log to another phone.

## Ship an update
Edit, bump `VERSION` in `sw.js`, commit, push. Phones pick up the new version on the next open.
