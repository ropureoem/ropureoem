# v6 implementation and verification

Based on v5 plus remote main `ba76b9874196fe91b049f770090d516ad2adf5da` (CNAME and Pages workflow). The existing deployment configuration is unchanged. Preview and ZIP are self-contained; v5 image assets are byte-for-byte preserved; public v5 contact copy is sanitized.

## Implemented

75 pages / 62 product-detail models. All original specification rows, descriptions and non-home content retained. WT-T13's conflicting legacy “WT-T15 variant” note corrected to confirmed silver standard housing (catalogue page 12). All product-specific quote destinations retained.

Homepage follows the requested eight-part desktop sequence, overriding the older homepage rules in UI standards. Shared header/search/nav/footer and mobile bottom navigation use one component stylesheet and approved brand tokens. Six working filters; 14-model thermal view uses existing confirmed description/specification evidence, with per-model capability caveat. No new inventory, MOQ quantities, certificate badges or unverified claims added.

Quotation uses mailto:info@ropureoem.com. Floating help uses https://wa.me/8618928823858; footer help uses get-quote.html. No third-party chat system or fabricated property ID. Full repo/source/archive search found no Tawk.to property ID.

## Passed local checks

- Exactly 75 production HTML pages, 62 original product models; all specification rows compared against baseline.
- Every local href/src/action and HTML fragment target exists, root and nested pages; all JSON-LD parses and uses only accepted product images.
- Prohibited terms/claims, price/MOQ quantities absent in active pages and script metadata. Approved catalogue SKUs are retained as requested. Historical v5 archives and original evidence assets are preserved.
- Approved `public/brand/` originals, robots, CNAME and Pages workflow compared byte-for-byte with baseline. v5 preview/ZIP changes are restricted to contact text; source images remain byte-identical.
- Real Chromium over local HTTP: homepage and accepted/pending-image product pages; 320/390/768/1024/1440px layout without horizontal overflow; all six range result counts; SKU/category query; empty state and Clear filters; live filtering; nested header GET search; quote model prefill; native Menu and Escape; all mobile bottom-nav destinations. No JavaScript exceptions or HTTP asset failures.
- Real quote form mailto navigation captured without sending mail; recipient, SKU/market subject and message body verified.
- Desktop/mobile screenshots visually reviewed. Product-image exports inspected; only passing images are referenced in HTML/JSON-LD. No video or iframe sources/autoplay.
- Self-contained preview/ZIP checked for page/model counts, relative resource and fragment targets, byte equality and ZIP integrity before commit.

## Unverified/source limitations

本次图片恢复：62 个型号中 45 个显示真实产品照片，17 个按逐型号审查保留 pending。已核实 ba76b98、v5 ZIP 和 preview/v5 的实际产品页引用及源图片 SHA-256 三者一致。CT15/CT16/CT26 与 WS01/WS02/WS03 两组重复哈希在 v5 已存在，未进行跨型号替换。原先通过的 WT-CT21、WT-SH14、WT-T25、WT-T27 输出保持原样。

WT-T13 已恢复指定 assets/img/WT-T13-correct.png 银色外壳实拍图，保留完整桌面背景以避免改动产品本体，居中置于白色 4:3 画布。其余新增输出仅等比缩小及白色画布居中，无裁切、拉伸、重绘或生成图片。17 个 pending 的中文/字标原因、三处来源证据、输入输出哈希、尺寸及处理步骤详见 docs/brand/product-image-audit.json 和 .md。

本次执行 scripts/package_v6.py 与 scripts/verify_v6.py，检查 75 页、62 型号、相对资源/锚点、JSON-LD、v5 来源、输出哈希、4 张保护图片、v6 布局/规格/SEO/联系链接保持以及 ZIP 完整性与文件一致性。本次实际请求 https://ropureoem.com/ 时，环境代理返回 HTTP 403（CONNECT tunnel failed），未取得站点响应，无法确认线上部署；不能据本地通过认定线上已生效。

No verified ROPureOEM factory footage was found; mobile shows a portrait poster with an explicit pending statement, no video playback. Certificate availability, order quantities and commercial terms require model-specific enquiry. GitHub main push succeeded. GitHub Actions status query returned Forbidden from the connected GitHub API; hosted deployment completion could not be verified. Local build and portable preview verification passed.


## SEO/contact/sitemap repair (baseline c8d5ab6)

- Homepage title/H1/meta: OEM water purifier manufacturer; homepage meta and OEM page title/FAQ: OEM water filter manufacturer. Existing water purifier OEM copy remains elsewhere.
- Countertop category title/H1/meta/FAQ: hot and cold water purifier. Products FAQ: portable water purifier market, with no market-size or portability claim.
- OEM FAQ: ultra high purity purifier; water purifier parts; water purification parts; water filter components; industrial reverse osmosis hot water. Special-purpose feasibility and unverified specifications explicitly use “Confirmed per order”.
- Personal contact name and inactive v6 language selector removed throughout production and public previews. Historical v5 preview/ZIP contact copy also sanitized; image/source audit files are unchanged.
- Previously sitemap.xml was a checked-in, manually enumerated file with no generator and 74 entries. The excluded HTML file is 404.html. Actual count: 62 models + 5 category documents + 7 top-level business pages + 1 error page = 75. Hot/Cold/Ice is a products.html query view, not a sixth category page. The requested complete HTML inventory now includes 404.html; it is an error document, not an additional product/category landing page.
- scripts/generate_sitemap.py discovers root/products HTML, maps index.html to /, excludes historical previews and produces 75 unique URLs. package_v6.py regenerates it before packaging. Verification checks exact set equality, not count alone.
- All product images, their DOM references, placeholders, image audit files and specification tables compare unchanged to c8d5ab6. 45 accepted / 17 pending preserved. CNAME, DNS and Pages workflow unchanged; no translations or new WhatsApp numbers.
- Static and Chromium checks passed: 75 pages, all relative resources/fragments, JSON-LD, ZIP integrity/preview equality, desktop/mobile layouts, six filters, search, quote form and navigation.
- Live domain requests from this environment are blocked by the network proxy (HTTP 403 CONNECT). This does not establish a website error or successful deployment. Commit/deployment status is checked separately via GitHub where available.
