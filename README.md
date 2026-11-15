# buenaobra.net

Personal resume and portfolio site for Lester Buenaobra. Plain static HTML, CSS and JS with no build step.

- `PROFILE.md`: source of truth for all site content
- `site/`: what gets deployed (Cloudflare Pages output directory)
- `site/_headers`: security headers for Cloudflare Pages
- `tools/serve.ps1`: local preview server, `pwsh tools/serve.ps1` then open http://localhost:8787
- `tools/build-icons.ps1`: regenerates `site/assets/icons/*.svg` for the skills section. Download the Iconify sets it names (`@iconify-json/<set>` `icons.json` from npm/jsDelivr) into a folder, then `pwsh tools/build-icons.ps1 -SetsDir <folder>`. Edit the `$map` at the top to add or swap icons. `mono` on an `<img class="ti">` darkens single-colour icons in plain mode and print.
- `site/assets/icons/vendor/`: logos taken from each vendor's own website (favicon or touch icon), for tools the open icon sets don't cover. `ink` lightens an all-black logo in neon mode.
