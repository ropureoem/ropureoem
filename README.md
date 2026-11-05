# ROPureOEM v6 — OEM Product Studio

An incremental upgrade of v5: all 75 English HTML pages plus 75 Chinese counterparts, 62 catalogue models, specification tables, model-specific quote links and approved brand originals are retained. No framework or build dependency is required to serve the website.

Open `preview/v6/index.html` after extracting the full package, or serve the repo with `python -m http.server 8766 --bind 127.0.0.1`. Release: `releases/ropureoem-v6-preview.zip`. The public v5 preview and release receive contact-copy cleanup and EN/ZH links to the maintained production pages; all image assets remain unchanged.

- Single petrol masthead; white product-led hero; six real range filters; featured model specifications; three-step OEM process; model-specific certification guidance; petrol enquiry panel; structured footer.
- Shared `styles/brand-tokens.css`, `styles/ui-tokens.css`, `styles/components.css`, header/search/navigation/footer across all 150 production pages. Legacy `styles.css` is retained but no longer loaded.
- Mobile two-column categories and featured models, stacked process/certification, fixed Home / Products / Get Quote / Videos / Contact navigation.
- `products.html?q=RP-F02` searches SKU, card text and category terms. `?range=hot-cold-ice` selects 14 existing models; options and functions vary by model. The five base ranges still contain 62 models.
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

Homepage assembly/logistics gallery: two original AI-generated illustrations (purifier assembly and container loading) appear in a compact two-column strip. The warehouse-dispatch illustration is on About (`about.html#factory-dispatch`), so the homepage has no repeated logistics scene. All three full-frame 1536×1024 WebP assets remain in `images/homepage-factory/`, with bilingual AI disclosures and generation/hash/placement records in `docs/brand/homepage-factory-image-audit.json`. Run `python scripts/verify_homepage_factory.py` on local port 8766 to check mobile and desktop source/preview layouts.

Homepage featured models: RP-C11 (countertop coffee RO), RP-U03 (under-sink RO), RP-C09 (ice/hot/cold RO) and RP-C04 (countertop hydrogen-water RO). Four cards use existing reviewed product photos and catalogue/specification copy. Faucet/shower models remain in the full catalogue and category/product pages, and are excluded from homepage features. Run `python scripts/verify_homepage_featured.py --browser` on local port 8766 to verify mobile layout, paired homepage links and unchanged catalogue bytes.

Final product namespace: 62 models, numbered RP-C01–C14 (Countertop), RP-U01–U18 (Under-Sink), RP-F01–F13 (Faucet), RP-S01–S14 (Shower) and RP-W01–W03 (Softener). Every public page, asset filename/reference, search card, quote option, data file, preview and downloadable archive uses these identifiers. The four homepage features are RP-C11, RP-U03, RP-C09 and RP-C04. No correspondence CSV is included in the site or repository. `python scripts/verify_model_namespace.py --browser` checks the namespace, metadata, unchanged parameter rows, search/quote interactions and former-route removal on local port 8766. Packaging rebuilds the preview directory from scratch to avoid stale files.

Mobile header/contact controls: all EN/ZH pages ship with the main menu closed in HTML. Menu toggles, outside clicks, navigation links, Escape and history restoration close it appropriately. On phones the search input grows to fill the second header row while the small EN/ZH links align to its right content edge. The floating help control retains its original appearance and opens a native two-choice disclosure: WhatsApp or Email us (the matching-language quote form, with the email address shown). Both native disclosures remain usable without JavaScript. Run `python scripts/verify_mobile_menu.py` and `python scripts/verify_contact_options.py` with the local server on 8766.

The homepage is simpler only below 700px: hero, four featured mainline products, compact OEM steps and the quote panel are primary. Duplicate discovery/search/category/certification blocks and repeated card details/actions are visually suppressed on phones; desktop keeps them. The short two-image strip is secondary, and homepage mobile footer navigation is reduced while its language switch remains. The existing #videos target is revealed when selected through the unchanged bottom Videos link; no video has been added and the pending P90 path is unchanged.
