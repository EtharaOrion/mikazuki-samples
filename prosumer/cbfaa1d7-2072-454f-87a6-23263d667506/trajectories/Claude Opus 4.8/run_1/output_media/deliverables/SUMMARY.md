# Package card fix — summary

**Live price from Square (source of truth):** 6-Session NMT Package = **$420.00**, six 60-minute individual sessions (`ITEM_NMT6`). Kept distinct from the 4-Session Starter ($300, `ITEM_NMT4`). Gift certificate left alone ($100).

## Done
- **Package card** — corrected to **6 sessions / $420** (was showing last spring's number). File: `package_card_corrected.png`.
- **Website product tile** — added/aligned the six-session package tile to **$420, 6 × 60 min** in the practice site. Files: `website_product_tile_corrected.html` (full page, edited in place at `home/Public/entry_a4.html`) and `website_product_tile_snippet.html` (tile only).
- **Stripe** — checked, did not change. Stale/mismatched details flagged for your manual fix in `STRIPE_FLAG.md`.

## What changed vs. what was on file
| | Old / stale | Corrected (Square) |
|---|---|---|
| Printed card | 8 sessions, $380 | 6 sessions, $420 |
| Draft card | 6 sessions, $400 (unfinalized) | 6 sessions, $420 |
| Website tile | none / stale | 6 sessions, $420 |
| Stripe | no $420 package price (see flag) | fix by hand |

## Deliverables in this folder
- `package_card_corrected.png` — the card to send/print
- `website_product_tile_corrected.html`, `website_product_tile_snippet.html`
- `STRIPE_FLAG.md`
- `make_card.py` — card source
