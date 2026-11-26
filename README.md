# taumatix.github.io

Source of [taumatix.dev](https://taumatix.dev): the project index (libraries and tools), upstream pins and engineering notes.
Plain HTML and CSS served by GitHub Pages from `main`, with no build step.

- `index.html`, `notes/`: pages. Each carries its own header and footer.
- `assets/`: stylesheet, theme and version-badge script, favicon, `og.png`.
- `tools/og.html`: source of `assets/og.png`. Regenerate it with headless Chrome at 1200x630.
- `tools/check_site.py`: the CI check. Local links resolve and no private repository is named.

Preview: `python3 -m http.server --directory .`, then open `http://127.0.0.1:8000/`. Add `?theme=dark` to
check dark mode.

The project list is written by hand, so adding or releasing a library or tool means editing `index.html`. The
version badges refresh from the GitHub API in the browser and fall back to the baked-in value.

Licensed under Apache-2.0.
