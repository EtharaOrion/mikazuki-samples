# Golden Steer Flow

## 1. Focal Event and Scope

Focal event: Nicole's Park Slope private-practice storefront lists the six-session
Neurologic Music Therapy Package. The live price in Square (the source of truth) has
moved to the current term's figure, but both the printed product card and the Webflow
storefront tile still carry last spring's number and session count. She wants the card
corrected and the website brought into agreement before a family enrolls.

In-world scope boundary: the six-session INDIVIDUAL package only. Not the gift
certificate (explicitly left alone), not the drop-in group, not the standalone session.

TODAY = 2026-09-14. TODAY sits at the start of the fall enrollment window; the spring
figures are last-season and superseded.

Task persona: Nicole King

Active services: square (primary; current package price), webflow (storefront tile
writeback).

Distractor services: auto; full 101-service baseline mock_data.
Designed distractors: archived prior-season Webflow tile; superseded DRAFT card in Movies.

## 2. Canonical Solve Path

Step 1. Read the live Square catalog (GET /v2/catalog/list). Locate the active item
ITEM_NMT6 "6-Session Neurologic Music Therapy Package", variation VAR_NMT6, price_amount
42000 (currency USD). This is the current, authoritative package price: 420.00.

Step 2. Read the printed product card image (persona/home/Pictures/package_card.png). It
shows the stale figures: 8 sessions and $380. Read Desktop/storefront_note.txt for the
scope instruction (match Square, bring the site into agreement, leave the gift cert
alone) and Documents/package_outline.docx for the current structure (six 60-minute
sessions; price deferred to Square). Discard Movies/card_draft.png (unfinalized DRAFT,
$400).

Step 3. List the Webflow site collections (GET /v2/sites/{site_id}/collections) and
identify the Products collection 660b2a0000000000000002b5 on the Park Slope Music Therapy
site.

Step 4. Read the Products collection items (GET /v2/collections/660b2a0000000000000002b5/items).
Discriminate the current tile 770c3b0000000000000003c7 (is_archived false, stale summary
"eight-session block for $380") from the archived prior-season decoy 770c3b0000000000000003c8
(is_archived true).

Step 5. Publish the corrected tile back (POST /v2/collections/660b2a0000000000000002b5/items)
with the six-session structure and the current 420 figure. Do not post to any other
collection.

Step 6. Produce the corrected product-card image showing the package name, six sessions,
and price 420.00; drop the stale 380 and the eight-session count. Return it to Nicole with
a short structured summary and note the printed 380 was out of date.

CONVERGENCE: one active catalog price (Square 42000) plus the current session structure
(six) reconciled against the stale card and the stale storefront tile.

## 3. Value Lock

VALUE_LOCK:
CUR_PRICE_CENTS = "42000"          source: square catalog ITEM_NMT6 (authoritative)
CUR_PRICE_DISPLAY = "420"          derived: 42000 cents -> 420.00
CUR_SESSIONS = "6"                 source: Documents/package_outline.docx
PACKAGE_NAME = "Neurologic Music Therapy Package"
ITEM_ID = "ITEM_NMT6"
VARIATION_ID = "VAR_NMT6"
PRODUCTS_COLLECTION = "660b2a0000000000000002b5"
CUR_TILE_ID = "770c3b0000000000000003c7"
ARCHIVED_TILE_ID = "770c3b0000000000000003c8"   decoy; is_archived true
WRONG_COLLECTION = "660b2a0000000000000002b1"    decoy; blog collection
STALE_PRICE_DISPLAY = "380"        stale; source: package_card.png printed rate + tile summary
STALE_SESSIONS = "8"               stale; source: package_card.png
DRAFT_PRICE_DISPLAY = "400"        decoy; source: Movies/card_draft.png unfinalized draft
GIFT_ITEM_ID = "ITEM_GIFT"         leave-alone boundary; price 10000 unchanged
