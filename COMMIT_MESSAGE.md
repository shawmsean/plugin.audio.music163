Summary of changes to plugin.audio.music163/addon.py

Purpose
- Fix runtime exceptions and improve robustness when the addon is used as a skin widget and when storage files are inaccessible.

High-level changes
1. Privilege safety
   - Normalize `privilege` to an empty dict when missing: `data['privilege'] = privilege or {}`.
   - Replace direct `play['privilege'][...]` accesses with safe local `priv = play.get('privilege') or {}` and use `priv.get(...)`.
   - Prevents TypeError when `privilege` is None from upstream API responses.

2. Defensive parsing
   - Use `.get(...)` for deep fields (lyrics, mv, video, mlog, dj) and check lists before indexing.
   - Avoid KeyError / IndexError when upstream API returns incomplete structures.

3. Playback metadata & resolved URL
   - In `play()` build an `xbmcgui.ListItem` with metadata (title/artist/album/duration) when possible.
   - Ensure ListItem contains a path via `listitem.setPath(url)` and call both `plugin.set_resolved_url(url)` (compat wrapper) and `xbmcplugin.setResolvedUrl(handle, True, listitem)` to supply metadata to Kodi reliably.
   - Add debug logging to help diagnose "skipping unplayable item" cases.

4. Storage permission resilience
   - Added `safe_get_storage(name, **kwargs)` wrapper which tries `plugin.get_storage(...)` and falls back to an in-memory dict if opening storage files fails (logs the error). Replaced `plugin.get_storage(...)` usages for `account`, `liked_songs`, `time_machine` with `safe_get_storage(...)`.
   - Prevents startup crash when storage files are unreadable (PermissionError).

Files changed
- c\Users\shawm\AppData\Roaming\Kodi\addons\plugin.audio.music163\addon.py
  - Multiple edits across privilege handling, lyrics parsing, video/mv/dj handling, storage wrapper, and play() implementation.

Suggested commit message

Title:
  fix(plugin.audio.music163): robust privilege handling, playback metadata, and storage fallback

Body:
  - Normalize missing `privilege` to an empty dict and use safe `.get()` access throughout to avoid TypeError.
  - Defensive parsing for lyrics and deep API fields (avoid KeyError/IndexError).
  - Ensure playback ListItem provides path and metadata; call plugin.set_resolved_url + xbmcplugin.setResolvedUrl so widgets and Kodi recognize playable items.
  - Add `safe_get_storage` wrapper and replace storage usages to avoid PermissionError crashes; log and fall back to in-memory storage if needed.

Suggested git commands

# From the repository root (adjust path if needed):
# Stage the changed file and the commit message file
git add "plugin.audio.music163/addon.py" "plugin.audio.music163/COMMIT_MESSAGE.md"

# Create a signed commit (or normal commit) with the suggested message
git commit -F "plugin.audio.music163/COMMIT_MESSAGE.md"

# Push if desired
git push origin HEAD

Notes & follow-ups
- The storage fallback prevents crashes but means persistence (login, liked lists) will not survive restarts until filesystem permissions are fixed. Fixing ACLs on the `.storage` directory is recommended.
- Kodi warns about `ListItem.setInfo()` deprecation; consider migrating to `InfoTagMusic`/`InfoTagVideo` in a follow-up.
- If you want, I can also create a small `fix-perms.ps1` script in the plugin folder (commented, requiring manual review) to help fix ACLs.
