# add-meter-watch-contract — atom-mw-01-scrape-floor

- Prefer the dashboard **Spending** scrape as the source.
- Treat `settings/usage` HTTP 404 as non-authoritative; do not invent figures.
- Enforce a scrape floor of **at least 5 minutes**.
- Stamp every report with **America/Chicago (CT)**.
