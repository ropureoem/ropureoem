# ROPureOEM v6 verification

## Final bilingual revision

The user's updated language requirement supersedes the initial English-only plan. English remains at `/`; all 75 pages now have real Chinese counterparts under `/zh/`: 62 product-detail pages, five category documents, seven top-level business pages (home, products, OEM/ODM, certification, about, quote and contact), plus 404. Total: 75 EN + 75 ZH = 150 HTML pages; only 75 English URLs are in the sitemap.

`scripts/build_bilingual.py` uses reviewed local translations in `scripts/i18n/zh.tsv`. It translates product titles, descriptions, navigation, UI copy and specification labels. All specification values/units are copied verbatim, apart from the explicit unresolved-value phrase translated as “按订单确认（Confirmed per order）”. It adds matching EN/ZH links to header and footer and reciprocal en/zh hreflang/canonicals for every production pair. Query parameters and fragments are preserved when switching. Historical v5 preview/download contact copy is sanitized and language links point to the maintained production pair; v5 source images remain identical.

No RU/KK buttons, personal contact name, new WhatsApp number, DNS change or new certification claims. Contact page retains ROPureOEM, info@ropureoem.com and WhatsApp +86 189 2882 3858 (https://wa.me/8618928823858).

## SEO placement (English)

- index.html title/H1/meta: oem water purifier manufacturer. Homepage meta also includes oem water filter manufacturer. Existing water purifier OEM wording remains in organization metadata and other pages.
- oem-odm.html title/FAQ: oem water filter manufacturer. FAQ also includes ultra high purity purifier, water purifier parts, water purification parts, water filter components and industrial reverse osmosis hot water. Special-purpose feasibility and unverified specifications remain Confirmed per order.
- products/countertop.html title/H1/meta/FAQ: hot and cold water purifier.
- products.html FAQ: portable water purifier market, without a market-size or portability claim.

## Sitemap cause and fix

The old sitemap.xml was a manually enumerated checked-in file with 74 URLs and no generator. The omitted HTML document was 404.html. Actual original inventory: 62 product pages + 5 category documents + 7 business pages + 1 error page = 75. Hot/Cold/Ice is a products.html query filter, not a sixth category document. The requested full inventory includes 404.html, which remains an error document, not a new product/category landing page.

`scripts/generate_sitemap.py` discovers only English root/products HTML. English index.html maps to `/`. Chinese review pages and historical previews are excluded. Packaging regenerates translations and sitemap before building the ZIP. Validation checks exact URL set equality and uniqueness: 75 English URLs, 0 Chinese URLs. All 75 Chinese pages have one head robots tag with `noindex, nofollow`, generated automatically. English pages have no noindex tag. Header language links are compact inline text immediately after the shortened search form, in the same search row (below the logo/menu/quote row on mobile); footer switches remain available.

## Image and specification protection

Baseline c8d5ab654ec030f2eb08113ec90245818d1cc4d4: 45 restored photographs, 17 pending. No source/output image bytes or image-audit documents changed. All English image nodes, placeholders, catalogue cards, SKU values and specification tables remain unchanged; Chinese pages resolve to the same image files and copy every specification value/unit without numeric conversion. The four previously protected outputs remain identical. RP-F02 uses the approved silver-housing source. CNAME, robots and Pages workflow remain unchanged.

The image audit retains original v5 page hashes as historical provenance. Verification checks those hashes against the immutable commit and separately proves that public v5 HTML/ZIP changes consist only of contact cleanup and language links; all source images and references are preserved.

## Verification

- 75 English and 75 Chinese documents, every language pair, header/footer switches, canonical/hreflang, Chinese titles/headings/labels, model values and all local links/fragments.
- All original model specification rows and 45/17 image status; SHA-256/output dimensions and source provenance; protected brand originals/CNAME/Pages configuration.
- Portable preview and ZIP integrity; 150 HTML documents, 62 English + 62 Chinese model pages, every archive entry equals its preview file.
- Chromium on local HTTP: desktop/mobile 320/390/768/1024/1440px, six filters, SKU/category search, empty state, quote model prefill, native menu/Escape, mobile navigation, actual EN↔ZH home/product/contact navigation, Chinese range/search/count and query/quote-model preservation. No JavaScript exceptions or failed assets.
- Live domain verification is blocked by the environment network proxy: HTTPS CONNECT to ropureoem.com returns 403 before reaching the website. Local checks do not establish live deployment success; GitHub push/deployment evidence is reported separately.

## Review-only Chinese SEO and compact search-row verification (2026-11-06)

- `python scripts/package_v6.py`: PASS, 150 HTML files (75 EN + 75 ZH), ZIP CRC and every preview byte match; embedded sitemap has 75 unique English URLs, 0 `/zh/` URLs; all 75 archived Chinese pages have exactly one `noindex, nofollow` head tag and all 75 archived English pages have no robots tag.
- `python scripts/verify_v6.py --browser`: PASS, source provenance/images/specifications/links, English SEO and responsive catalogue/quote/navigation checks. All 75 English titles, H1s, descriptions, keywords, hreflang and canonicals match pre-change main `2571a9905dd34c9389ce238d52c2f3269cf4ef01`.
- `python scripts/verify_bilingual.py --browser`: PASS, 75/75 ZH noindex, 0/75 EN noindex; sitemap 75 total / 0 ZH; reciprocal header/footer language links and queries; compact search + EN/ZH in one row at widths 320, 390, 699, 700, 768, 1024, 1100, 1199, 1200 and 1440. No JS/resource errors.
- At 390px, both EN/ZH headers are 114.8px tall: logo/menu/quote occupy the first row; the 190px search form starts at x=16, with compact 42.2×32px EN/ZH links at x=218, on the same vertical centre. No separate language row or filled language buttons.
- Local sample `/zh/about.html`: title `关于 ROPureOEM — 净水器 OEM / ODM 制造商`, H1 `关于 ROPureOEM`, robots `noindex, nofollow`. Local sample `/about.html`: title `About ROPureOEM — Water Purifier OEM / ODM Manufacturer`, H1 `About ROPureOEM`, no robots tag; English title/H1 unchanged.
- `git diff --check`: PASS. Image files, image audits, historical v5 files, robots.txt, CNAME and Pages workflow have no changes.
- Live checks require network access to ropureoem.com: current proxy rejects HTTPS CONNECT with 403 before reaching the origin. Local results above do not claim live verification. The user explicitly took over live sitemap/noindex/title/H1/mobile-header verification; only GitHub Pages deployment status is checked after the single main commit.


## New homepage illustrations (2026-11-06)

Three original images were generated independently with OpenAI image_gen from text prompts, without old-site/reference photos. Each was visually reviewed for unwanted text/signs/brands/watermarks/domains. The generated 1536×1024 frame is retained in full; only WebP encoding (quality 86) is applied. The gallery includes a visible AI-generated illustration disclosure in English and Chinese, without claiming to show an actual company facility.

The section `#factory-gallery` is immediately below `.studio-hero` and before the model-search/category section on both homepages. Desktop: three columns; mobile: one column. Files and site URLs:

- `images/homepage-factory/container-loading.webp` — https://ropureoem.com/images/homepage-factory/container-loading.webp
- `images/homepage-factory/purifier-assembly.webp` — https://ropureoem.com/images/homepage-factory/purifier-assembly.webp
- `images/homepage-factory/warehouse-dispatch.webp` — https://ropureoem.com/images/homepage-factory/warehouse-dispatch.webp

`docs/brand/homepage-factory-image-audit.json` records generation method, scene prompts, dimensions, sizes, SHA-256 hashes and visual review. Product image sources/outputs/audits remain unchanged. No video or video placeholder was changed.

Validation:

- `work/venv/bin/python scripts/verify_v6.py --browser`: PASS, existing product images/specifications, all 75 English titles/H1/descriptions/keywords/hreflang/canonicals, responsive homepage/gallery/catalogue/quote/navigation at 320/390/768/1024/1440px; no JS/HTTP failures.
- `work/venv/bin/python scripts/verify_bilingual.py --browser`: PASS, EN/ZH pairing, image reuse, compact search-row language controls across 10 widths from 320 to 1440px, 75/75 ZH noindex and 0/75 EN noindex, English-only sitemap 75 URLs / 0 ZH.
- `work/venv/bin/python scripts/verify_homepage_factory.py`: PASS, 1280/1440px desktop on EN/ZH source and portable preview (8 combinations); all three images decode at original dimensions, full 3:2 frame, three-column alignment, no horizontal overflow, visible AI disclosure, working header language switches, no JS/resource errors. Screenshots/results are saved under ignored `work/`.
- `work/venv/bin/python scripts/package_v6.py`: PASS, rebuilt `releases/ropureoem-v6-preview.zip`; 150 bilingual HTML files with new images, byte-matched preview tree and correct sitemap/robots metadata.
- `git diff --check`: PASS. No CNAME, robots.txt, Pages workflow, old-site assets, product images, product image audits or sitemap changes in this image update.

Live-domain checks remain assigned to the user as previously requested; Pages deployment is checked separately after pushing this image commit to main.


## Mainline-only homepage features (2026-11-06)

The homepage retains RP-C11 and replaces RP-F11 / RP-S06 / RP-F10 with three existing, photo-approved mainline products. EN/ZH homepages show the same four models in this order:

1. RP-C11 — countertop RO with freshly ground coffee; the original featured card remains unchanged.
2. RP-U03 — high-capacity under-sink household RO; catalogue capacity 1000 / 1200 / 1600 GPD.
3. RP-C09 — RO purifier with ice, hot and cold water; catalogue capacity 50 / 75 / 100 GPD.
4. RP-C04 — countertop hydrogen-water RO dispenser; catalogue membrane/production 200 GPD / 30 L/h, SPE electrolysis listed in the existing specification table.

The three replacement cards are copied from products.html; their added specification excerpts are copied from the first row of the corresponding existing product specification tables, with matching Chinese translations. All product photographs are existing approved assets. No model is invented and no product file is edited. All faucet/shower SKUs are absent from homepage features, and RP-F11 / RP-F10 / RP-S06 are absent from both homepage source files. The full catalogue and category/product pages remain byte-identical to image commit `2f9c2ca4c85f04d3923b8cb3457ff66156abed91`, including accessory SEO. Category navigation remains available.

Validation:

- `work/venv/bin/python scripts/verify_homepage_featured.py --browser`: PASS. EN/ZH production sources and portable preview at 320/390/768/1440px; four models, 2-column mobile and 4-column desktop layout, four decoded images, every product link and header language switch, no overflow/JS/resource failures. RP-C11 card, full homepage head/header/footer/hero/AI gallery and all catalogue/category/product files match the previous commit exactly. Mobile screenshots are saved under ignored work/.
- `work/venv/bin/python scripts/verify_v6.py --browser`: PASS. Original product files/images/specifications, English SEO and responsive catalogue/quote/navigation checks remain valid; sitemap remains 75 English URLs, 0 ZH.
- `work/venv/bin/python scripts/verify_bilingual.py --browser`: PASS. Matching EN/ZH features, paired links, unchanged numerical specifications and image reuse; compact search/EN-ZH controls across 10 viewport widths, 75/75 ZH noindex and 0/75 EN noindex.
- `work/venv/bin/python scripts/package_v6.py`: PASS. Rebuilt bilingual preview/ZIP with all 150 pages, gallery assets, mainline features, correct robots metadata and English-only sitemap.
- `git diff --check`: PASS. Product/catalogue/category source bytes, images, CNAME, robots.txt, Pages workflow and sitemap are unchanged by this selection update.

The preceding AI-gallery commit `2f9c2ca4c85f04d3923b8cb3457ff66156abed91` was pushed to main and GitHub Pages deployment succeeded: https://github.com/tileserachied/ropureoem/actions/runs/42065722955 . The user retains live-domain checks; the video remains pending their upload/path.


## Final public model numbering (2026-11-06)

All 62 models now use category letters and two-digit ordinals: RP-C01–C14, RP-U01–U18, RP-F01–F13, RP-S01–S14 and RP-W01–W03. The final user-provided numbering is the sole active scheme. No correspondence table/CSV is published or committed; private delivery is in the conversation only.

The migration updates English/Chinese product filenames and URLs, titles/H1s/SKUs, image filenames/alt text, JSON-LD, catalogue cards, homepage features, search inputs/results, quote option values/prefill, translation data, generated metadata, root/preview sitemaps, public documents/scripts, historical v5 preview and both downloadable ZIPs. Old product files are removed rather than redirected. Unlisted housing-variant identifiers are removed from caveats; configuration-by-order wording is preserved without inventing additional models. Existing image bytes and numerical specification values remain unchanged.

Homepage features remain four mainline products: RP-C11, RP-U03, RP-C09, RP-C04; no Faucet/Shower features. All 75 English SEO titles/H1s/descriptions/keywords/canonicals/hreflang compare against immutable Git evidence after identifier-only normalisation. Chinese pages retain noindex/nofollow and header/footer switching. The compact search-row EN/ZH layout is unchanged. CNAME, DNS, robots.txt and Pages workflow are unchanged. The pending P90 plan and assets/video/p90-1-product.mp4 path, plus the #videos area, are untouched.

Validation:

- `python scripts/verify_model_namespace.py --browser`: PASS. Exactly 62 identifiers across the five final ranges; 462 parameter rows unchanged; no obsolete identifiers or filenames in public UTF-8 files or extracted archive entries; no CSV published; 62 catalogue/search records and quote options per language; sitemap 75 English URLs, 0 Chinese, with all 62 product URLs using current identifiers. Five-category local product samples return 200; corresponding former routes return 404 without retired identifiers, and all former product files are absent.
- `python scripts/verify_v6.py --browser`: PASS. Historical image provenance/SHA-256, specifications, JSON-LD, original SEO keywords, all local links/fragments, responsive catalogue/search/quote/navigation, no JS/resource failures. Immutable revision checks normalise identifiers transiently without writing correspondence data.
- `python scripts/verify_bilingual.py --browser`: PASS. 75 EN + 75 ZH; robots 0/75 EN and 75/75 ZH; paired header/footer switches and canonical/hreflang; Chinese labels, identical numerical values and image sources; compact controls at 10 widths from 320 to 1440px.
- `python scripts/verify_homepage_featured.py --browser`: PASS. Four final mainline models, all product/quote destinations; 2-column mobile and 4-column desktop, EN/ZH source and portable preview, no overflow/JS/resource failures.
- `python scripts/verify_homepage_factory.py`: PASS. EN/ZH gallery and portable preview at 1280/1440px, three full-frame decoded images, correct language switches.
- `python scripts/package_v6.py`: PASS. Clean portable rebuild; 150 bilingual HTML files and 62 models per language; correct sitemap and robots metadata; archive CRC and every preview byte match. Already compressed media are stored without redundant deflation.
- Public text scans exclude immutable .git history and ignored work scratch; downloadable archives are also inspected after extraction. Namespace/content/path residual counts are zero. `git diff --check`: PASS.

Live-domain requests are still blocked by the environment proxy with HTTP 403; local HTTP results do not establish live responses. Pages deployment status is checked separately after pushing main. Rollback is a revert of this namespace commit; the pre-change Git evidence remains immutable.


## Mobile menu, full-width search row and two-choice contact control (2026-11-06)

Root cause reproduced at 390px with JavaScript disabled: the source main-menu details element had an open attribute, exposing a 333.5px dropdown from y=72 over the hero at y=138.8. The fix removes the initial open attribute from all 150 production EN/ZH pages. `scripts/build_bilingual.py` enforces this on every regeneration. Shared `script.js` retains native Menu toggling and closes the mobile menu on outside clicks, direct/nested navigation links, Escape, mobile breakpoint entry and restored history pages. Desktop navigation stays visible.

The mobile `.header-tools` row spans the full padded header width. Its search form flexes to consume remaining space; EN/ZH stay compact text links at the right content edge. At 390px in both languages: row x=16 / width=358px; input width=235.8px; language links end at x=374 (16px right padding). The first header row and five bottom-navigation destinations are unchanged.

The shared generator replaces the direct floating contact link with `details.help-widget` / `summary.help`, followed by a small two-choice panel. WhatsApp points to https://wa.me/8618928823858 in a new tab; Email us / its Chinese translation opens the matching-language get-quote.html and shows info@ropureoem.com. No other contact channels or personal identifiers were introduced. The trigger keeps its prior position, dimensions, fonts, border, radius and colours, confirmed against pre-change 390/1440px measurements in both languages. Native details allows opening/closing and accessing contact links without JavaScript; JavaScript additionally handles outside/Escape/selection closure and focus return.

Validation completed:

- `python scripts/verify_mobile_menu.py`: PASS. All 150 production pages, 150 preview pages and 150 archived pages default closed. EN/ZH home/product source and preview at 320/390/768/1024px; menu toggling, outside click, direct/nested links, Escape/history, desktop-to-mobile resize, visible hero, full-width search row, five bottom-navigation destinations and language switches; no JS/resource failures. Default closure also verified without JavaScript.
- `python scripts/verify_contact_options.py`: PASS. Every production/preview/archive page has exactly two contact choices and the correct quote destination. Browser checks at 320/390/768/1440px cover initial closure, both visible options, native no-JS fallback, keyboard/Escape/outside/toggle behavior and actual navigation to the EN/ZH quote form. Trigger geometry/style matches the pre-change measurements. No external chat service was opened by the tests.
- `python scripts/verify_bilingual.py --browser`: PASS. Full-width mobile search and right-aligned small EN/ZH links across the responsive cases, language/query preservation, 75/75 ZH noindex and 0/75 EN noindex, correct sitemap and links.
- `python scripts/verify_v6.py`, `python scripts/verify_homepage_featured.py`, `python scripts/verify_model_namespace.py`: PASS. Product parameters and image bytes, all English SEO values, four mainline featured models, final model namespace and root/archived sitemap remain valid. Historical UI comparisons permit only the intentional initial-menu/help-control differences.
- Public text and both extracted ZIPs were checked for cancelled private-contact labels/identifiers: zero residuals. No correspondence CSV is published.
- `python scripts/package_v6.py`: PASS. The bilingual portable preview and releases/ropureoem-v6-preview.zip were rebuilt with these shared controls; 150 HTML files, correct robots/sitemap, CRC and byte equality.
- `git diff --check`: PASS. CNAME, robots.txt, Pages workflow, product parameters/images, mainline features and the pending P90 video plan/path are unchanged.

Local 390px screenshots are saved under ignored work/: mobile-ui-en-closed.png, mobile-ui-zh-closed.png, mobile-ui-en-help-open.png and mobile-ui-zh-help-open.png. Live-domain HTTPS CONNECT is still rejected by the environment proxy with 403, so these screenshots/results are explicitly local; Pages deployment is checked separately after pushing main.


## Compact mobile homepage and redistributed factory scenes (2026-11-06)

The same pending mobile-controls commit also simplifies the homepage at widths below 700px. The hero, four mainline feature cards, OEM process and quote panel remain primary. Duplicate model discovery/search/category panels and certification guidance are visually suppressed only on phones; duplicated SKU/MOQ/specification excerpts and per-card quote actions are suppressed there while model descriptions and product-detail links remain. OEM steps use three plain numbered rows. The mobile homepage footer keeps branding/copyright/language controls without repeated navigation/contact columns. Desktop discovery/search, categories, certification, full feature-card specifications/actions, process cards and footer remain available.

The existing video target remains in the same DOM location and is revealed on phones when #videos is selected; default video placeholders no longer lengthen the initial mobile reading path. All five bottom-navigation destinations remain functional. No video file, old footage or additional model identifier has been introduced; the pending P90 path remains unchanged.

The homepage factory strip now contains exactly two distinct existing scenes: purifier assembly followed by container loading. Both remain full-frame, with no pixel edits or cropping. On phones the strip has no large heading and uses two small columns. At 390px in both languages the images are 171×114px and the complete strip is 174.8px high. The warehouse-carton photo is removed from the homepage and placed in the existing About page at #factory-dispatch, with its own bilingual AI disclosure. No new HTML page or sitemap URL is added. All three image hashes are unchanged; the image audit records their current placement. Desktop shows the two pictures compactly beside the introduction and keeps its other rich content.

Latest validation supersedes the older three-photo/single-column gallery expectations:

- `python scripts/verify_homepage_factory.py`: PASS for EN/ZH source and portable preview at 320/390/768/1280/1440px. Exactly two different homepage scenes in one row, full-frame decode, compact mobile dimensions, warehouse photo on About only, visible mobile core content, hidden secondary phone blocks, desktop rich content retained, working language switches and Videos target, no horizontal overflow/JS/resource errors.
- `python scripts/verify_mobile_menu.py` and `python scripts/verify_contact_options.py`: PASS again with the simplified homepage; all generated menus/help panels default closed, every menu close path and contact choice works, bottom navigation and header layout remain valid, floating trigger appearance/position still match the original measurements.
- `python scripts/verify_v6.py --browser`, `python scripts/verify_bilingual.py --browser`, `python scripts/verify_homepage_featured.py --browser`, `python scripts/verify_model_namespace.py`: PASS. All 75 English SEO records, numerical parameters, final 62-model namespace, four mainline features, EN/ZH switching, noindex rules and sitemap counts remain valid. The mobile category/video expectations now match the requested simplified default view and explicit Videos activation.
- Cancelled private-contact labels/identifiers, obsolete model identifiers and previous-site branding were checked in public text plus both extracted ZIPs: zero residuals. No private correspondence file is published.
- `python scripts/package_v6.py`: PASS; preview and releases/ropureoem-v6-preview.zip rebuilt with the full batch, 150 bilingual pages, matching assets/bytes, CRC and correct sitemap/robots metadata.
- `git diff --check`: PASS. CNAME, robots.txt, Pages workflow, product image bytes and numerical specification values are unchanged.

Local evidence is under ignored work/: factory-mobile-en.png / factory-mobile-zh.png, full-page home-simple-mobile-en.png / home-simple-mobile-zh.png, and the mobile controls/contact screenshots above. Full-page reading screenshots temporarily omit fixed overlays during capture only; actual viewport screenshots retain them. Both the live domain and requested external style reference are blocked by the environment proxy (HTTPS CONNECT 403); no source content or assets from the reference were fetched/copied, and no live screenshot is claimed. Pages status is verified separately after pushing main.
