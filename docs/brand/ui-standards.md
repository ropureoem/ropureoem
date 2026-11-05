# ROPureOEM UI standards — v6

Status: implementation standard. This document translates the approved VI into reusable website rules. It does not replace the VI or authorize changes to the logo or product data.

## 1. Design direction and page framework

ROPureOEM is a B2B OEM / ODM catalogue for brand owners and distributors. Prioritize finding a model, understanding its confirmed specification, and starting a model-specific enquiry. Use a spacious catalogue layout with clear hierarchy, restrained surfaces and consistent components.

The legacy site is a structural reference only. Do not import its wording, identity, colours, pictures or product records. Use ROPureOEM's own approved assets, existing copy and verified catalogue data. Do not invent MOQ quantities, factory capabilities, certificates or product details.

Homepage sequence:
1. Petrol masthead: final logo, wide product search, language chips and quote CTA.
2. White navigation strip: Home; Products dropdown; OEM-ODM; Certification; About. Contact remains available in the footer and navigation utility link.
3. Two petrol hero cards: left introduction and one project CTA; right product-range title, verified product image and View Product Range CTA.
4. Compact supply facts: 62 confirmed models, five underlying ranges, sample-first process.
5. Six browse cards: Under-Sink RO; Countertop; Hot / Cold / Ice; Water Softening; Shower Filters; Faucet Filters.
6. Featured product cards, then existing OEM / ODM process, certification support and buyer guidance.
7. Shared footer and a fixed Need help? inquiry link.

Hot / Cold / Ice is a curated view of existing models with verified heating, cooling or ice capabilities. It is not a sixth underlying catalogue category or an addition to the 62-model inventory. Do not imply every model in the view has all three functions. Product pages retain their full existing content and specification tables.

Do not create a factory section without verified ROPureOEM factory content and images. Existing OEM / ODM process information supplies that part of the page instead.

## 2. Typography

Font stack: `system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`. No external font dependency. Logo artwork is an exception: preserve its approved file bytes and original typography.

| Role | Desktop (>= 1100px) | Tablet (700–1099px) | Mobile (< 700px) | Line height | Weight |
| --- | --- | --- | --- | --- | --- |
| Homepage hero H1 | 56px | 44px | 36px | 1.08 | 700 |
| Interior-page H1 | 40px | 36px | 30px | 1.18 | 700 |
| H2 / section heading | 32px | 28px | 26px | 1.22 | 700 |
| H3 / category heading | 22px | 22px | 20px | 1.30 | 700 |
| H4 / product name | 18px | 18px | 18px | 1.35 | 700 |
| Lead paragraph | 18px | 18px | 17px | 1.60 | 400 |
| Body, inputs | 16px | 16px | 16px | 1.65 | 400 |
| Navigation, buttons | 14px | 14px | 14px | 1.40 | 600 / 700 |
| Small text, SKU, captions | 14px | 14px | 14px | 1.50 | 400 / 500 |
| Eyebrow, compact count | 12px | 12px | 12px | 1.50 | 700 |

Use one H1 per page. Do not skip heading levels to obtain a visual size; apply a component class instead. Use -0.03em tracking on H1, -0.02em on H2, normal tracking on body text and 0.10em on uppercase eyebrows. Body reading measure is at most 70 characters where practical. Maintain at least 16px between paragraphs and 24px between a section heading block and its content.

## 3. Colour roles

Import `styles/brand-tokens.css` before component styles. The approved VI remains the colour source of truth. Do not repeat literal colour values throughout components.

| Colour | Permitted roles | Avoid |
| --- | --- | --- |
| Deep teal / Petrol `#00343D` | Masthead, footer and hero surfaces; headings/body text on white; secondary button fill; focus outline on light surfaces | Large dark surfaces behind dense specification tables |
| Ice cyan `#8CE2E4` | Primary CTA fill with petrol lettering; selected EN chip; links and small highlights on petrol; focus outline on dark surfaces | Ordinary text on white, white lettering on cyan |
| Coral `#FF786C` | Existing logo dot, small decorative indicator, restrained notice accent | Main CTA fill, large surface fills, ordinary text on white, implying live chat availability |
| White `#FFFFFF` | Main page and product-image backgrounds; card surfaces; body text on petrol; secondary button lettering | White text on cyan or coral |

Petrol and white dominate. Cyan directs action; coral is a small accent. Do not add green/amber branding, promotional gradients, or colour treatments to product photos.

Use only the VI's existing supporting UI colours: muted text `#49636A`, dividers `#D4E5E7`, cyan-tinted surfaces `#E9F8F8` / `#F1F8F9`, coral notice surface/border `#FFF0EE` / `#FFD0CA`, hover petrol `#00515E`, footer secondary text `#B8D4D8`. Artwork-specific light-version colours are confined to the approved logo assets.

Contrast reference: white/petrol 13.47:1; cyan/petrol 9.06:1; coral/petrol 5.23:1. Cyan/white (1.49:1) and coral/white (2.58:1) are unsuitable for ordinary text. Use at least 4.5:1 for normal text and 3:1 for essential control boundaries and large text. Error/status messages require words, not colour alone.

## 4. Spacing, grids and shape

Use a 4px base grid. Spacing tokens: 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64, 80 and 96px. Prefer these values; do not add arbitrary margins to individual pages.

- Page container: max-width 1280px including its horizontal padding; centred; 24px gutters on desktop/tablet and 16px below 700px.
- Main top padding: 32px desktop, 24px mobile. Main bottom padding: 80px desktop, 56px mobile.
- Homepage section separation: 80px desktop, 56px tablet, 40px mobile. Within interior pages use 32px before a new section heading and 16px below it.
- Grids: 24px gaps desktop; 16px below 1100px. Category browse: 3 columns desktop, 2 tablet, 1 mobile. Featured models: 3 / 2 / 1. Catalogue cards: 4 columns at >= 1100px, 3 at 900–1099px, 2 at 600–899px, 1 below 600px.
- Hero: two columns (approximately 55/45) at >= 900px; stacked below 900px. Gap 24px desktop / 16px mobile. Both cards stretch to the same row height.
- Component radii: controls 8px; product/category cards 12px; hero/large panels 16px. Pills are reserved for language chips, tags and counts.
- Borders: 1px divider colour. Default shadow: none; hover shadow `0 8px 24px rgba(0,52,61,0.08)`. Do not stack multiple shadows.

## 5. Buttons, links, inputs and interaction

Use real links for navigation and buttons for actions. Minimum hit target: 44×44px, including language chips and navigation toggles. Button font: 14px/1.4, weight 700. Default padding 12px 20px; small card actions 10px 16px with a 44px minimum height. Radius 8px. Icon-to-label gap 8px. Do not use transform/lift effects.

| Variant | Normal | Hover | Use |
| --- | --- | --- | --- |
| Primary | Cyan fill, petrol text, 1px cyan border | White fill with petrol text on a dark surface; petrol fill with white text on a light surface | Get a Quote, primary project action, Search |
| Secondary | Petrol fill, white text, 1px petrol border | Hover-petrol fill, white text | Secondary navigation action on white |
| Ghost / outline | Transparent fill, petrol text/border on white; white text and cyan border on petrol | Cyan-tinted fill/petrol text on white; cyan fill/petrol text on petrol | View Product Range, quieter alternatives |
| Text link | Petrol on white; cyan on petrol | Underline with 3px underline offset | View Category, View Details, Ask Service |

Disabled controls: visibly muted, `disabled` attribute, no hover reaction, explanatory title when useful. Language chips are EN active; ZH/RU/KK are clearly unavailable placeholders. Do not simulate translation.

Inputs: 16px body text; minimum height 48px; 12px 16px padding; 8px radius; white background, petrol text and 1px muted-ink border. Labels stay visible or use a proper screen-reader-only label. Placeholder text is muted, not a substitute for a label. Focus: 3px petrol outline on light or 3px cyan outline on dark, offset 3px. Keep focus visible throughout keyboard navigation.

Product search is a native GET form to the relative `products.html` path with parameter `q`. The catalogue reads the query, fills its local filter input and filters all 62 existing records, including SKU, text and category terms. The thermal collection uses `range=hot-cold-ice`. Show result counts, an empty state and a Clear filters link. Preserve model-specific quote links and `info@ropureoem.com` recipient handling.

Respect `prefers-reduced-motion`; otherwise limit colour/shadow transitions to 150ms. Never remove outlines without a replacement. Include Skip to content. Product dropdown uses native details/summary with keyboard support and closes on Escape/outside click. Mobile navigation exposes its expanded state.

## 6. Card standards

### Product cards

White surface; 1px divider border; 12px radius; no default shadow; 16px padding. Image well is white, 4:3, centred with object-fit contain. Keep the same image well across listings and related products. Never use cover/crop to cut off the product. Content order: category tag; model/title (18px); existing description (14px); SKU; optional MOQ only if confirmed, otherwise “MOQ: Confirm on enquiry”; View Details and Ask Service links. Do not invent MOQ numbers. Keep actions aligned at the bottom through flex layout. Hover changes border/shadow; no movement.

### Category cards

White surface; 1px divider border; 12px radius; 24px padding desktop / 20px mobile. Small number/count above H3, short ROPureOEM description, and a View Category link at the bottom. Coral may accent the small number but must not carry essential information. Every card links to an existing category or verified filtered collection.

### Hero cards

Petrol surface; 16px radius; 40px padding desktop / 24px mobile; no shadow. Left: eyebrow, one H1, short existing/verified ROPureOEM copy and one primary CTA. Right: H2 “RO Water Purifiers & Core Filter Components”, approved product photograph in a white image well, verified model caption and ghost View Product Range CTA. Use white body copy and cyan highlights. Keep each card's visual order clear without decorative imagery.

### Supporting content panels

OEM process, certification guidance, quote forms and specification tables use white or the approved cyan-tinted surface; 1px divider border; 12px radius; 24px panel padding. Retain all model-specific certificate caveats. Tables use 14–16px text, 12px 16px cell padding, tinted row-header cells and horizontal overflow containment on small screens. Do not hide specifications.

## 7. Header, navigation, footer and help

### Masthead

Petrol full-width background. Inner container is the standard 1280px. Three areas: original dark-background logo on the left (220px desktop, 190px mobile, original 1600:480 ratio and built-in whitespace); a search area that grows into the middle; language chips and Get a Quote on the right. Use 16px vertical padding, 24px desktop column gaps and 12px within action groups. Preserve the full logo; do not crop, redraw or recolour it.

At < 1100px allow the action row to wrap deliberately. Below 700px: logo and quote first row, full-width search second row, language chips third row. No horizontal overflow. All 75 pages use the same component with correct relative links.

### Navigation

White full-width strip directly below the masthead; 1px divider bottom border. Minimum row height 56px. Navigation text is petrol, 14px/1.4, weight 600. Active link gets an underline/visible selected treatment, not colour alone. Products dropdown contains all existing five categories, the thermal collection and All 62 models. Dropdown is white, 12px radius, 1px divider border, 12px padding and one restrained shadow. Keep Home, OEM-ODM, Certification, About, contact and quote destinations working.

At < 900px use an accessible Menu toggle and a stacked navigation panel. Navigation remains reachable without JavaScript. Desktop masthead/navigation may stick to the top; on smaller screens use normal document flow so the header does not consume the viewport.

### Footer

Petrol surface, white headings/body, cyan links. Use the standard container. Top inquiry row: existing-model/market prompt and primary quote CTA. Below: four columns for brand summary, ranges, OEM / ODM links and contact; two columns tablet and one mobile; 32px gaps. Include the final logo, info@ropureoem.com, existing WhatsApp link, contact page and all existing informational links. Separate copyright/back-to-top row with a muted divider. Reserve enough bottom space for the fixed inquiry control.

### Help

Fixed bottom-right link, 24px from desktop edges and 16px mobile; petrol background, white text and cyan outline; 12px radius; 12px 16px padding. Label “Need help?” and “Online inquiry”. Target the relative `get-quote.html`. It is a static inquiry shortcut, not live chat. Do not claim an agent is online or connect a chat backend. It must not obscure footer links or form submission controls. Provide an ordinary Back to top link.

## 8. Product-image standard and source acceptance

Use only verified ROPureOEM repo/source/catalogue images. Check model identity before editing; best-source priority is a clean full product cutout, then a clear catalogue photo, then a recoverable source photo. Never replace a model with a visually similar different model. RP-F02 is the silver standard-housing faucet confirmed on catalogue page 12; never use the gold/blue-light photo.

Retouch must preserve product geometry, controls, connectors, material colour and included components. Use background isolation and conservative non-generative tonal cleanup. Do not synthesize product parts or relight in a way that changes finish/colour. No arbitrary colour presets, AI-generated replacement products, upscaling presented as recovered detail, or fake reflections.

- Background: pure white #FFFFFF, no room/tabletop/lifestyle background.
- Export frame: 1200×900 (4:3) where source quality supports it; smaller source-limited exports may retain a 4:3 canvas without pretending to add detail. Consistent framing is more important than a misleading resolution claim.
- Product bounding box: centred; normally 72–84% of available width or height, with at least 8% clear space on all sides. Keep the complete product and all intentional included components. Do not crop away connectors or accessories.
- Lighting: neutral, consistent exposure with visible detail in black housings, controlled white highlights and natural metal colour. Do not bleach white housings or crush black ones. No decorative drop shadow baked into the image.
- No Chinese text, other brand names or watermarks in accepted display assets. Prefer a clean original. If such content cannot be removed safely without inventing/reconstructing the product, mark the model as missing an acceptable image instead of publishing that photo.
- Exclude unresolved watermarks, severe blur, clipped products and unrecoverable mixed/lifestyle compositions. Do not show low-quality original photos as a fallback after rejection.
- Preserve originals for provenance; use a dedicated polished asset path and track model, source path/hash, edit operations, output path/hash, dimensions and pass/fail reason in `docs/brand/product-image-audit.json` and a readable report.
- When no acceptable source/output exists, keep the model and all specifications, show a restrained text-only “Product image pending” well with its SKU, and list it in the missing-image report. Do not use a generic product illustration, a fake photograph or another model's photo.

Inspect every final display image for white background, clean edges, correct model, centring, natural lighting and forbidden branding/text. Missing-image counts must distinguish unavailable/unsuitable sources from processing failures; never call an unedited or failed image “retouched”. Replace hero/category/related image uses too; no hidden low-quality fallback on mobile or product details.

## 9. Implementation and release acceptance

Keep the approved VI tokens in `styles/brand-tokens.css`. Add shared UI roles/sizing tokens once in `styles/ui-tokens.css`, then one component stylesheet for all 75 pages. Do not append page-specific override piles, duplicate desktop/mobile component rules, inline colour declarations or one-off spacing patches. Page differences should be layout variants of the same component.

Before release verify:
- 75 HTML pages and exactly the existing 62 product-detail models; all specifications and non-homepage main content retained, apart from deliberate image-status presentation and catalogue filtering UI.
- One consistent header/nav/footer and accessible search on every page; no broken relative href/src/action links in root or nested pages.
- Homepage split hero, six range cards, catalogue search/query and thermal collection, language placeholders, inquiry shortcut and quote-model prefill work.
- Original approved logo bytes, petrol/cyan/coral identity, info@ropureoem.com and correct silver RP-F02 identity retained.
- Every displayed product image has a passing audit entry, or a clear missing-image state and report. No bad-photo fallback.
- JSON-LD remains valid and references accepted images only; omit an unavailable product image rather than reference a placeholder as a product photograph.
- Preview is self-contained in `preview/v6/`; the full ZIP is `releases/ropureoem-v6-preview.zip`. Preserve the v5 preview/release as a prior version.
- Record tests and any unavailable browser verification honestly; do not call source inspection a rendered browser test.
