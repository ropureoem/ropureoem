# ROPureOEM v6 — OEM Product Studio

An incremental upgrade of v5: all 75 English HTML pages plus 75 Chinese counterparts, 62 catalogue models, specification tables, model-specific quote links and approved brand originals are retained. No framework or build dependency is required to serve the website.

Open `preview/v6/index.html` after extracting the full package, or serve the repo with `python -m http.server 8766 --bind 127.0.0.1`. Release: `releases/ropureoem-v6-preview.zip`. The public v5 preview and release receive contact-copy cleanup and EN/ZH links to the maintained production pages; all image assets remain unchanged.

- Single petrol masthead; white product-led hero; six real range filters; featured model specifications; three-step OEM process; model-specific certification guidance; petrol enquiry panel; structured footer.
- Shared `styles/brand-tokens.css`, `styles/ui-tokens.css`, `styles/components.css`, header/search/navigation/footer across all 150 production pages. Legacy `styles.css` is retained but no longer loaded.
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

See STATUS.md for evidence and remaining source limitations. GitHub Pages workflow, CNAME and robots remain unchanged. Run `python scripts/generate_sitemap.py` to build the 75-document English-only sitemap; packaging runs it automatically. Each language has 62 product pages, five category documents, seven top-level business pages and one standalone 404 document (150 HTML pages; sitemap: 75 EN URLs, 0 ZH). Hot/Cold/Ice is a query filter, not a sixth category document.


Bilingual publishing: English lives at `/`; Chinese review pages live under `/zh/` with `noindex, nofollow`, with matching filenames and product SKUs. `scripts/build_bilingual.py` generates all 75 Chinese pages from English sources using the reviewed `scripts/i18n/zh.tsv` translations. It adds EN/ZH links in both header and footer, reciprocal en/zh hreflang, language-specific canonicals and shared asset references. Product titles, descriptions, navigation and specification labels are translated; specification values/units are copied directly except “Confirmed per order” becomes “按订单确认（Confirmed per order）”. No image files are generated or altered. RU/KK are absent.

`package_v6.py` runs bilingual generation and sitemap generation, copies both languages into preview/v6, then creates `releases/ropureoem-v6-preview.zip` with 150 HTML files. To verify all language pairs and numerical specifications, run `python scripts/verify_bilingual.py`; add `--browser` with a local server on 8766 to check actual EN↔ZH navigation, Chinese search and query/quote-model preservation. Use `--preview` for the portable tree.

Homepage assembly/logistics gallery: three original AI-generated illustrations are stored in `images/homepage-factory/`, immediately below the hero and above the catalogue search on EN/ZH homepages. Each full-frame WebP is 1536×1024; no old-site photos are reused. A visible bilingual AI disclosure accompanies the gallery. Provenance/hashes are recorded in `docs/brand/homepage-factory-image-audit.json`; run `python scripts/verify_homepage_factory.py` with the local server on 8766 for desktop EN/ZH and portable-preview checks. Packaging includes the new `images/` directory.
