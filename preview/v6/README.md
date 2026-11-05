# ROPureOEM v6 — OEM Product Studio

An incremental upgrade of v5: all 75 HTML pages, 62 catalogue models, specification tables, model-specific quote links and approved brand originals are retained. No framework or build dependency is required to serve the website.

Open `preview/v6/index.html` after extracting the full package, or serve the repo with `python -m http.server 8766 --bind 127.0.0.1`. Release: `releases/ropureoem-v6-preview.zip`. The public v5 preview and release receive contact-copy cleanup only; all image assets remain unchanged.

- Single petrol masthead; white product-led hero; six real range filters; featured model specifications; three-step OEM process; model-specific certification guidance; petrol enquiry panel; structured footer.
- Shared `styles/brand-tokens.css`, `styles/ui-tokens.css`, `styles/components.css`, header/search/navigation/footer across all 75 pages. Legacy `styles.css` is retained but no longer loaded.
- Mobile two-column categories and featured models, stacked process/certification, fixed Home / Products / Get Quote / Videos / Contact navigation.
- `products.html?q=WT-T13` searches SKU, card text and category terms. `?range=hot-cold-ice` selects 14 existing models; options and functions vary by model. The five base ranges still contain 62 models.
- Quote form opens the buyer's email app addressed to info@ropureoem.com. Floating help goes directly to WhatsApp; small footer help goes to get-quote.html. No chat backend.
- 45 restored product photos and 17 pending models remain as approved on main. Source originals, output images, references and specifications are unchanged by the SEO/contact update. See `docs/brand/product-image-audit.json` and `.md`.
- No verified factory video exists in the repo. The mobile portrait poster explicitly states that footage is pending, with no video or playback control. No existing Tawk.to ID was found.

Verification (Python packages: beautifulsoup4, pillow, playwright; system Chromium):

```sh
python scripts/verify_v6.py
# With a local HTTP server listening on 8766:
python scripts/verify_v6.py --browser
```

See STATUS.md for evidence and remaining source limitations. GitHub Pages workflow, CNAME and robots remain unchanged. Run `python scripts/generate_sitemap.py` to build the full 75-document sitemap; packaging runs it automatically. The inventory is 62 product pages, five category documents, seven top-level business pages and one standalone 404 document. Hot/Cold/Ice is a query filter, not a sixth category document.
