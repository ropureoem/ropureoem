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

Baseline c8d5ab654ec030f2eb08113ec90245818d1cc4d4: 45 restored photographs, 17 pending. No source/output image bytes or image-audit documents changed. All English image nodes, placeholders, catalogue cards, SKU values and specification tables remain unchanged; Chinese pages resolve to the same image files and copy every specification value/unit without numeric conversion. The four previously protected outputs remain identical. WT-T13 uses the approved silver-housing source. CNAME, robots and Pages workflow remain unchanged.

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

The homepage retains WT-CT21 and replaces WT-T27 / WT-SH14 / WT-T25 with three existing, photo-approved mainline products. EN/ZH homepages show the same four models in this order:

1. WT-CT21 — countertop RO with freshly ground coffee; the original featured card remains unchanged.
2. WT-UR04 — high-capacity under-sink household RO; catalogue capacity 1000 / 1200 / 1600 GPD.
3. WT-CT19 — RO purifier with ice, hot and cold water; catalogue capacity 50 / 75 / 100 GPD.
4. WT-CT09 — countertop hydrogen-water RO dispenser; catalogue membrane/production 200 GPD / 30 L/h, SPE electrolysis listed in the existing specification table.

The three replacement cards are copied from products.html; their added specification excerpts are copied from the first row of the corresponding existing product specification tables, with matching Chinese translations. All product photographs are existing approved assets. No model is invented and no product file is edited. All faucet/shower SKUs are absent from homepage features, and WT-T27 / WT-T25 / WT-SH14 are absent from both homepage source files. The full catalogue and category/product pages remain byte-identical to image commit `2f9c2ca4c85f04d3923b8cb3457ff66156abed91`, including accessory SEO. Category navigation remains available.

Validation:

- `work/venv/bin/python scripts/verify_homepage_featured.py --browser`: PASS. EN/ZH production sources and portable preview at 320/390/768/1440px; four models, 2-column mobile and 4-column desktop layout, four decoded images, every product link and header language switch, no overflow/JS/resource failures. CT21 card, full homepage head/header/footer/hero/AI gallery and all catalogue/category/product files match the previous commit exactly. Mobile screenshots are saved under ignored work/.
- `work/venv/bin/python scripts/verify_v6.py --browser`: PASS. Original product files/images/specifications, English SEO and responsive catalogue/quote/navigation checks remain valid; sitemap remains 75 English URLs, 0 ZH.
- `work/venv/bin/python scripts/verify_bilingual.py --browser`: PASS. Matching EN/ZH features, paired links, unchanged numerical specifications and image reuse; compact search/EN-ZH controls across 10 viewport widths, 75/75 ZH noindex and 0/75 EN noindex.
- `work/venv/bin/python scripts/package_v6.py`: PASS. Rebuilt bilingual preview/ZIP with all 150 pages, gallery assets, mainline features, correct robots metadata and English-only sitemap.
- `git diff --check`: PASS. Product/catalogue/category source bytes, images, CNAME, robots.txt, Pages workflow and sitemap are unchanged by this selection update.

The preceding AI-gallery commit `2f9c2ca4c85f04d3923b8cb3457ff66156abed91` was pushed to main and GitHub Pages deployment succeeded: https://github.com/tileserachied/ropureoem/actions/runs/42065722955 . The user retains live-domain checks; the video remains pending their upload/path.
