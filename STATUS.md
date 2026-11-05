# ROPureOEM v6 verification

## Final bilingual revision

The user's updated language requirement supersedes the initial English-only plan. English remains at `/`; all 75 pages now have real Chinese counterparts under `/zh/`: 62 product-detail pages, five category documents, seven top-level business pages (home, products, OEM/ODM, certification, about, quote and contact), plus 404. Total: 75 EN + 75 ZH = 150 URLs.

`scripts/build_bilingual.py` uses reviewed local translations in `scripts/i18n/zh.tsv`. It translates product titles, descriptions, navigation, UI copy and specification labels. All specification values/units are copied verbatim, apart from the explicit unresolved-value phrase translated as “按订单确认（Confirmed per order）”. It adds matching EN/ZH links to header and footer and reciprocal en/zh hreflang/canonicals for every production pair. Query parameters and fragments are preserved when switching. Historical v5 preview/download contact copy is sanitized and language links point to the maintained production pair; v5 source images remain identical.

No RU/KK buttons, personal contact name, new WhatsApp number, DNS change or new certification claims. Contact page retains ROPureOEM, info@ropureoem.com and WhatsApp +86 189 2882 3858 (https://wa.me/8618928823858).

## SEO placement (English)

- index.html title/H1/meta: oem water purifier manufacturer. Homepage meta also includes oem water filter manufacturer. Existing water purifier OEM wording remains in organization metadata and other pages.
- oem-odm.html title/FAQ: oem water filter manufacturer. FAQ also includes ultra high purity purifier, water purifier parts, water purification parts, water filter components and industrial reverse osmosis hot water. Special-purpose feasibility and unverified specifications remain Confirmed per order.
- products/countertop.html title/H1/meta/FAQ: hot and cold water purifier.
- products.html FAQ: portable water purifier market, without a market-size or portability claim.

## Sitemap cause and fix

The old sitemap.xml was a manually enumerated checked-in file with 74 URLs and no generator. The omitted HTML document was 404.html. Actual original inventory: 62 product pages + 5 category documents + 7 business pages + 1 error page = 75. Hot/Cold/Ice is a products.html query filter, not a sixth category document. The requested full inventory includes 404.html, which remains an error document, not a new product/category landing page.

`scripts/generate_sitemap.py` discovers English root/products HTML and Chinese zh/**/*.html. English index.html maps to `/`, Chinese index.html to `/zh/`. Historical previews are excluded. Packaging regenerates translations and sitemap before building the ZIP. Validation checks exact URL set equality and uniqueness: 75 English + 75 Chinese = 150.

## Image and specification protection

Baseline c8d5ab654ec030f2eb08113ec90245818d1cc4d4: 45 restored photographs, 17 pending. No source/output image bytes or image-audit documents changed. All English image nodes, placeholders, catalogue cards, SKU values and specification tables remain unchanged; Chinese pages resolve to the same image files and copy every specification value/unit without numeric conversion. The four previously protected outputs remain identical. WT-T13 uses the approved silver-housing source. CNAME, robots and Pages workflow remain unchanged.

The image audit retains original v5 page hashes as historical provenance. Verification checks those hashes against the immutable commit and separately proves that public v5 HTML/ZIP changes consist only of contact cleanup and language links; all source images and references are preserved.

## Verification

- 75 English and 75 Chinese documents, every language pair, header/footer switches, canonical/hreflang, Chinese titles/headings/labels, model values and all local links/fragments.
- All original model specification rows and 45/17 image status; SHA-256/output dimensions and source provenance; protected brand originals/CNAME/Pages configuration.
- Portable preview and ZIP integrity; 150 HTML documents, 62 English + 62 Chinese model pages, every archive entry equals its preview file.
- Chromium on local HTTP: desktop/mobile 320/390/768/1024/1440px, six filters, SKU/category search, empty state, quote model prefill, native menu/Escape, mobile navigation, actual EN↔ZH home/product/contact navigation, Chinese range/search/count and query/quote-model preservation. No JavaScript exceptions or failed assets.
- Live domain verification is blocked by the environment network proxy: HTTPS CONNECT to ropureoem.com returns 403 before reaching the website. Local checks do not establish live deployment success; GitHub push/deployment evidence is reported separately.
