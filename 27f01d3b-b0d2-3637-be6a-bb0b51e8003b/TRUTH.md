# Golden Steer Flow

## 1. Focal Event and Scope

Focal event: the Crossroads Conservatory 5th Anniversary Showcase, Saturday 10 October 2026 at
The Phoenix, 302 W 8th St, Kansas City. TODAY is 2026-10-07 (Wednesday), so the show is three days out.

In-world scope boundary: the ONE published, public, in-window showcase listing, which is the live
Eventbrite event `evt-cc-001` plus its two paid public ticket tiers, and the ONE live run-of-show item
on the Showcase board, `item-1001`. The prompt never states this. A careful solver derives it from:
- `persona/HEARTBEAT.md`, "October 10, 2026: Crossroads Conservatory 5th Anniversary Showcase at The Phoenix, 6:00 PM" (fixes the date and the venue, and carries the now-stale time);
- `persona/MEMORY.md`, "5th anniversary showcase planned for October 2026" under Crossroads Conservatory;
- `data/home/Desktop/b4.docx`, Claire's note, which fixes WHICH asset is still in play (digital only, print already shipped), WHERE the run sheet lives (the board, not the Music-folder copy, not the flyer kanban), that the venue's change touches the music and NOT the doors, and the house convention that the DOOR price is printed, never the all-in;
- `data/home/Music/file_8.docx`, the May run of show, which fixes the venue address and the ensemble order.

The boundary excludes, by their own in-world keys: the closed dress rehearsal (`evt-cc-001-dr`,
capacity 40, not ticketed to the public), the abandoned draft (`evt-cc-001-hold`, `status` "draft"),
last year's show (`evt-cc-000-2025`, `start_utc` in 2025), the comp tier (`tc-cc-001-comp`, `free`
true, not a public price), and on the board the archived 2025 run sheet (`item-1000`), the dress
rehearsal call sheet (`item-1007`) and the December recital run sheet (`item-1008`).

Task persona: Jessica Webb (assistant: OpenClaw).

Active services (2): `eventbrite` (PRIMARY, carries the graded ground truth), `monday` (the writeback).

Distractor services: auto; full 101-service persona baseline shipped in mock_data.
Designed distractors: `trello` (Claire's marketing and flyer kanban, same Project-Management cluster as monday).

WHY monday AND NOT wordpress: the reference solve at build time proved that `wordpress`, `trello`,
`etsy`, `eventbrite` and `notion` all mutate a DEEP COPY in this environment. `_mutable_store.rows()`
returns `[copy.deepcopy(...)]` and those data modules never call the store write API, so a `PUT` there
returns the updated object and persists nothing. Only nine of the 101 services write through
(`youtube`, `quickbooks`, `monday`, `intercom`, `instagram`, `mailchimp`, `salesforce`, `algolia`,
`airbnb`). `monday_data.update_item` genuinely patches the store, and TOOLS.md already has Jessica
tracking "the 5th anniversary showcase plan from booking to run-of-show" there, so the writeback is
both durable and in-world.

## 2. Canonical Solve Path

Step 1. Read `prompt.txt`. The ask is goal-only: a corrected poster at "the size we use for the
digital one", plus the run sheet "saying the right thing". No file, service, date, price or scope pin.

Step 2. Read `persona/HEARTBEAT.md` and `persona/MEMORY.md`. Establish the focal event: the 5th
Anniversary Showcase, 10 October 2026, The Phoenix. HEARTBEAT records the start as 6:00 PM. Per
`persona/AGENTS.md` ("Re-read the calendar, inbox, and any sheets tied to prior work, treating
yesterday's snapshot as unverified") and `persona/IDENTITY.md` ("You never quote a number, a date, or
a booking without checking the latest version of its source first"), that remembered time is NOT
ground truth.

Step 3. Locate the poster in `data/home/`. It is `data/home/Pictures/p3.png`, findable by content, not
by filename. READ IT VISUALLY. It prints: SATURDAY . OCTOBER 10 . 2026; THE PHOENIX . 302 W 8TH ST;
DOORS 5:30 PM . MUSIC 6:00 PM; GENERAL ADMISSION $25; PREMIUM SEATING + RECEPTION $60; the four
ensemble lines (BEGINNING STRINGS, YOUTH JAZZ COMBO, ADVANCED JAZZ ENSEMBLE, ADULT THEORY PLAYERS);
the quartet closing set; and the stamp PROOF v2 . 21 AUG 2026 . NOT FOR PRINT. The $25 and the
6:00 PM exist ONLY on this image.

Step 4. Read `data/home/Documents/m9.pdf` (Marta Quintero, 21 August 2026). She states she
cross-checked the door time and the two prices against the ticket page "the same afternoon" and that
"if a time or a price changes after today this proof is just a picture of what was true in August".
Her claim dates the proof; it is not current truth.

Step 5. Read `data/home/Desktop/b4.docx` (Claire Reynolds, updated 10/05/26). Establishes: the 18x24
print run shipped 09/18 and cannot be recalled; the DIGITAL poster is the only asset still in play;
the run sheet lives on the board, under the Showcase run-of-show item, and the Music-folder copy is
the May version nobody has touched; the flyer kanban is for marketing tasks and is NOT where timings
go; the venue's change is a changeover issue that "only touches the music, not the doors"; and the
house convention is that the DOOR price is printed, never the all-in.

Step 6. Read `data/home/Desktop/k2.xlsx` (Claire's promo asset specs). Row "Digital poster" is the
only row with status "NEEDS NEW EXPORT"; width 1080, height 1350 (4:5). Every other row is shipped,
done, or n/a. This fixes the export size.

Step 7. Read the live event. `GET {EVENTBRITE_API_URL}/v3/organizations/org-crossroads/events` or
`GET /v3/events/evt-cc-001`. Select `evt-cc-001` on the single in-world key: it is the only listing
that is `status` "live", public, and starts on 10 October 2026. Its `start_utc` is
`2026-10-10T23:30:00Z` and its `timezone` is `America/Chicago`. Its `summary` carries the freshness
signal: "Downbeat revised 5 October at the venue's request ... Doors hold where they were."

Step 8. CONVERT. 2026-10-10T23:30:00Z in America/Chicago (CDT, UTC-5 on that date) is
Saturday 10 October 2026, 6:30 PM. The string "6:30 PM" appears verbatim nowhere in the bundle; it is
computed from the live UTC stamp plus the record's own timezone field.

Step 9. Read the live prices. `GET {EVENTBRITE_API_URL}/v3/events/evt-cc-001/ticket_classes`.
Envelope is `{"ticket_classes": [...]}`. Take the two PAID PUBLIC tiers: `tc-cc-001`
"General Admission" `cost` 2750, and `tc-cc-002` "Premium Seating plus Reception" `cost` 6450. Skip
`tc-cc-001-comp` (`free` true). CONVERT cents to dollars: 2750 -> $27.50 and 6450 -> $64.50. Per
Claire's house convention the printed price is `cost` (the door price), NOT `cost` plus `fee`.

Step 10. Produce the corrected poster. Rebuild the proof's layout and lineup at 1080 x 1350 with
exactly three corrections: music 6:00 PM -> 6:30 PM, general admission $25 -> $27.50, premium seating
with reception $60 -> $64.50. DOORS STAY AT 5:30 PM: the event summary and Claire's note both say the
change touches the music only. Write the export to the workspace root as `poster.png`.

Step 11. Straighten the run sheet. `GET {MONDAY_API_URL}/v2/boards` and
`GET /v2/boards/board-101/items` to find the Showcase Run-of-Show board. Select `item-1001`,
"Run of show for Showcase night", the only live run sheet for this night. Two things on it are
stale and both must move: the `downbeat` column reads "6:00 PM" and the `notes` prose reads
"doors 5:30, downbeat 6:00". `ItemUpdateBody` carries one `column_id` per call, so this is two
calls. `PUT {MONDAY_API_URL}/v2/items/item-1001` with `{"column_id": "downbeat", "text": "6:30 PM"}`,
then again with `{"column_id": "notes", "text": "... doors 5:30, downbeat 6:30 ..."}`. The
structured `downbeat` column is the Channel A surface and the `notes` prose is the Channel B
surface, so writing only one of the two forfeits the other channel. Do NOT touch the trello flyer
kanban and do NOT edit the Music-folder docx.

Step 12. Report briefly, in Jessica's register: what moved and what did not, what the proof said, what
the live record says, that the printed 18x24 run already shipped and cannot be corrected, and that the
run sheet is updated.

CONVERGENCE EVIDENCE. Three simulated experts (a design producer, a venue box-office manager, and a
careful generalist assistant) converge on the same answer and the same restraint for single-key
reasons. On the DOWNBEAT all three take `evt-cc-001` because it is the only `status` "live" public
listing on 10 October 2026, and all three convert its own `start_utc` with its own `timezone` field
rather than trusting HEARTBEAT or the August proof, because AGENTS.md tells them live state outranks a
snapshot. On the DOORS all three leave 5:30 PM alone, because the event `summary` and `b4.docx` both
say the change touches the music only. On the PRICES all three take `tc-cc-001` and `tc-cc-002`
because they are the only rows on `evt-cc-001` with `free` false, and all three print `cost` rather
than `cost` plus `fee` because Claire's note states the house convention verbatim. On the EXPORT SIZE
all three take 1080 x 1350 because it is the single row on the promo sheet marked "NEEDS NEW EXPORT".
On the RUN SHEET all three take `item-1001` because Claire's note says the run sheet lives on the
board, and `item-1000` is archived 2025, `item-1007` is the closed rehearsal and `item-1008` is
December. No expert prints the $25 or the 6:00 PM, because both are stamped PROOF v2 . 21 AUG 2026 and
the live record is dated later. The mechanical proof of the single in-scope instance is the G20 grep.

## 3. Value Lock

```
VALUE_LOCK:
  SHOW_TIME_LIVE        = "6:30 PM"       # type: graded-positive; computed from mock_data/eventbrite-api/events.json evt-cc-001 start_utc 2026-10-10T23:30:00Z in timezone America/Chicago
  DOWNBEAT_TOKEN        = "6:30"          # type: graded-positive; the computed value R10 judges on the monday item-1001 downbeat column and notes
  GA_PRICE_DISPLAY      = "$27.50"        # type: graded-positive; computed from mock_data/eventbrite-api/ticket_classes.json tc-cc-001 cost 2750 cents, as printed on the poster deliverable
  PREMIUM_PRICE_DISPLAY = "$64.50"        # type: graded-positive; computed from mock_data/eventbrite-api/ticket_classes.json tc-cc-002 cost 6450 cents, as printed on the poster deliverable
  DOORS_TIME            = "5:30 PM"       # type: graded-positive; IMAGE-ONLY; source: data/home/Pictures/p3.png "DOORS 5:30 PM". Unchanged by the venue: the anti-overcorrection value.
  POSTER_WIDTH          = "1080"          # type: graded-positive; source: data/home/Desktop/k2.xlsx sheet "assets" cell C7 (row "Digital poster")
  POSTER_HEIGHT         = "1350"          # type: graded-positive; source: data/home/Desktop/k2.xlsx sheet "assets" cell D7 (row "Digital poster")
  EVENT_ID              = "evt-cc-001"    # type: graded-positive; STATE TOKEN anchored to mock_data/eventbrite-api/events.json id evt-cc-001
  RUNSHEET_ITEM_ID      = "item-1001"     # type: graded-positive; STATE TOKEN anchored to mock_data/monday-api/items.json item_id item-1001
  LINEUP_ENSEMBLE       = "Advanced Jazz Ensemble"  # type: graded-positive; IMAGE-ONLY; source: data/home/Pictures/p3.png lineup block
  PRINT_RUN_SPEC        = "18x24"         # type: graded-positive; source: data/home/Desktop/b4.docx and data/home/Desktop/k2.xlsx row "Print poster 18x24"
  STALE_SHOW_TIME       = "6:00 PM"       # type: stale; IMAGE-ONLY on the proof; source: data/home/Pictures/p3.png "MUSIC 6:00 PM" (also echoed in persona/HEARTBEAT.md and the item-1001 notes column)
  STALE_PREMIUM_PRICE   = "$60"           # type: stale; IMAGE-ONLY on the proof; source: data/home/Pictures/p3.png "PREMIUM SEATING + RECEPTION $60"
  STALE_GA_PRICE        = "$25"           # type: stale; IMAGE-ONLY on the proof; source: data/home/Pictures/p3.png "GENERAL ADMISSION $25"
  DECOY_HOLD_EVENT_DATE = "2026-10-17"    # type: decoy; must-not-appear; source: mock_data/eventbrite-api/events.json evt-cc-001-hold start_utc (status draft)
  DECOY_DRESS_REHEARSAL = "evt-cc-001-dr" # type: decoy; must-not-appear; source: mock_data/eventbrite-api/events.json (capacity 40, closed)
  DECOY_ARCHIVE_RUNSHEET = "item-1000"    # type: decoy; must-not-appear; source: mock_data/monday-api/items.json (the archived 2025 run sheet)
  DECOY_LASTYEAR_GA     = "2000"          # type: decoy; must-not-appear; source: mock_data/eventbrite-api/ticket_classes.json tc-cc-000-2025-ga cost
```
