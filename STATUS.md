# v6 implementation and verification

Based on v5 plus remote main `ba76b9874196fe91b049f770090d516ad2adf5da` (CNAME and Pages workflow). The existing deployment configuration is unchanged. Preview and ZIP are self-contained; v5 archives are byte-for-byte preserved.

## Implemented

75 pages / 62 product-detail models. All original specification rows, descriptions and non-home content retained. WT-T13's conflicting legacy “WT-T15 variant” note corrected to confirmed silver standard housing (catalogue page 12). All product-specific quote destinations retained.

Homepage follows the requested eight-part desktop sequence, overriding the older homepage rules in UI standards. Shared header/search/nav/footer and mobile bottom navigation use one component stylesheet and approved brand tokens. Six working filters; 14-model thermal view uses existing confirmed description/specification evidence, with per-model capability caveat. No new inventory, MOQ quantities, certificate badges or unverified claims added.

Quotation uses mailto:info@ropureoem.com. Floating help uses https://wa.me/8618928823858; footer help uses get-quote.html. No third-party chat system or fabricated property ID. Full repo/source/archive search found no Tawk.to property ID.

## Passed local checks

- Exactly 75 production HTML pages, 62 original product models; all specification rows compared against baseline.
- Every local href/src/action and HTML fragment target exists, root and nested pages; all JSON-LD parses and uses only accepted product images.
- Prohibited terms/claims, price/MOQ quantities absent in active pages and script metadata. Approved catalogue SKUs are retained as requested. Historical v5 archives and original evidence assets are preserved.
- Approved `public/brand/` originals, sitemap, robots, CNAME, Pages workflow, v5 preview and v5 ZIP compared byte-for-byte with baseline.
- Real Chromium over local HTTP: homepage and accepted/pending-image product pages; 320/390/768/1024/1440px layout without horizontal overflow; all six range result counts; SKU/category query; empty state and Clear filters; live filtering; nested header GET search; quote model prefill; native Menu and Escape; all mobile bottom-nav destinations. No JavaScript exceptions or HTTP asset failures.
- Real quote form mailto navigation captured without sending mail; recipient, SKU/market subject and message body verified.
- Desktop/mobile screenshots visually reviewed. Product-image exports inspected; only passing images are referenced in HTML/JSON-LD. No video or iframe sources/autoplay.
- Self-contained preview/ZIP checked for page/model counts, relative resource and fragment targets, byte equality and ZIP integrity before commit.

## Unverified/source limitations

4 individually reviewed and normalized white-background images pass: WT-CT21, WT-SH14, WT-T25, WT-T27. 58 sources are pending or unsuitable; 0 processing failures. No failed/unedited image is labelled retouched. Detailed provenance, hashes, dimensions, operations and status are in the JSON audit and readable report. All source originals remain unchanged.

WT-T13 original is the correct silver standard housing from catalogue page 12 (original PNG preserved); its tabletop background fails display acceptance. It displays an explicit SKU placeholder pending a clean source or verified conservative isolation; no gold/blue-light replacement is used.

No verified ROPureOEM factory footage was found; mobile shows a portrait poster with an explicit pending statement, no video playback. Certificate availability, order quantities and commercial terms require model-specific enquiry. GitHub main push succeeded. GitHub Actions status query returned Forbidden from the connected GitHub API; hosted deployment completion could not be verified. Local build and portable preview verification passed.
