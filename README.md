# DC TV with Lee Heggan — Spotify feed

Spotify show `0Lyo1KUzIUjQp4vs8CofDj` reads this repository's public
`https://leeheggan-droid.github.io/dctv-podcast/feed.xml`.

`build_feed.py` mirrors only the already-approved feed at
`https://media.leeheggan.tech/dc-tv/assets/podcast/feed.xml`.
It refuses to lose published episodes or change their GUIDs, enclosure URLs,
byte lengths or dates. The workflow checks for updates every 30 minutes and
requests an actual Pages build; a workflow commit alone does not trigger Pages.

5 November 2026: repaired the 15-episode frozen feed and restored Lee Heggan
branding with episodes 16–17. Historical audio files remain at their original
URLs. Do not run the retired metadata-based feed reconstruction or create a
second Spotify show. An RSS update is not proof of Spotify ingestion: verify
the public title, episodes and search results independently.
