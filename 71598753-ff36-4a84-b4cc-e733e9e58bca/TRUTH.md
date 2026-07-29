# Golden Steer Flow

## 1. Focal Event and Scope

- Focal event: the Biscayne Bar Association Fall Family Law CLE Seminar, Saturday 2026-10-24, now 9:00 AM at the Miami Riverside Conference Center. Live record: `mock_data/eventbrite-api/events.json` id `evt-bba-cle-fall26` (summary carries the dated "Update Oct 5" move); venue row `venue-riverside-mia`.
- In-world scope boundary: the Oct 24 seminar flyer and its reminder email are in scope; this is bar-association program work (enterprise surface), not firm or family business. The live listing is authoritative for venue and start (chair's note: "the logistics are whatever the listing says now, not what February's paperwork says"; whiteboard goal note: "everything else off the current listing - the Feb paperwork is stale"; AGENTS.md: "Conflict resolution: the most recent thing Michelle says wins over older records."). The listing separates the 8:30 AM doors time from the 9:00 AM program start, so the flyer start is 9:00 AM. The whiteboard photo is authoritative for the series name (revised from the struck "Family Law Forum" to "The Ethics Hour") and keynote; `data/home/Public/file_14.pdf` carries the approved credit line; the chair's note pins the reminder audience to the CLE reminders list and forbids sending. Discovery: HEARTBEAT.md (Oct 24 seminar), TOOLS.md (eventbrite CLE registrations, mailchimp drafts queued for manual send), the artifacts.
- Task persona: Michelle Brooks (bar CLE committee volunteer; enterprise surface).
- Active services: eventbrite (primary; carries the live venue/time truth), mailchimp (the reminder-draft writeback).
- Distractor services: auto; full 101-service persona baseline shipped in mock_data. Designed distractors: none.

## 2. Canonical Solve Path

Step 1. Read `prompt.txt`: finish the committee flyer with current logistics, queue the reminder to the right list, send nothing.
Step 2. Read `home/Documents/doc_11.docx` (Renee Whitfield's note): the board notes are the direction; reminder to the CLE reminders list ONLY; queue and keep it parked; logistics come from the listing, not February's paperwork.
Step 3. Read `home/Pictures/IMG_5533.jpg` (whiteboard, de-signposted goal note): the series name was revised at the sit-down, the first candidate "Family Law Forum" is struck through and replaced with "The Ethics Hour" (the big line); keynote "Judge Marisa Cantwell (Ret.)". The board no longer dictates placement or subject wording, only "everything else off the current listing - the Feb paperwork is stale". Do not carry the struck "Family Law Forum" onto the flyer.
Step 4. Read `home/Desktop/cle_flyer_draft.png` (the base to edit, 1200x1500): stale "8:30 AM to 4:30 PM" and "Hyatt Regency Miami", correct date and "7.0 CLE hours, including 1.0 ethics" line, keynote block empty. Cross-check `home/Public/file_14.pdf` (February registration confirmation): same stale venue/time and the pre-compression "7.0 CLE hours" total. VIEW `home/Public/file_16.pdf` (Florida Bar accreditation, scanned/image-only): the fall course is now approved for "6.0 CLE hours" (1.0 ethics unchanged) and it marks the prior 7.0 filing SUPERSEDED - so the draft/February 7.0 is stale. Ignore `home/Pictures/cle_flyer_spring.png` (old "Coffee and Counsel" series, February event).
Step 5. GET `/v3/organizations/org-brooks-family-law/events` (or `/v3/events/evt-bba-cle-fall26` and `/v3/venues`): live start 2026-10-24T13:00:00Z, venue `venue-riverside-mia` "Miami Riverside Conference Center", summary "Update Oct 5 ... Doors open 8:30 AM Eastern; the program itself begins at 9:00 AM." The program START on the flyer is 9:00 AM; the 8:30 AM in the listing is the DOORS time, and it coincides with the stale draft/February start, so a solver who grabs the door time reproduces the stale 8:30 (R8 trap). Reject the February events (evt-7000001 Fall CLE, evt7000105 Ethics CLE) by date. Key: event id + the dated update + doors-vs-program.
Step 6. Edit the flyer from the draft base at 1200x1500: add "The Ethics Hour" as the series name, "Judge Marisa Cantwell (Ret.)" under the title, set "9:00 AM" and "Miami Riverside Conference Center". The compressed agenda means the draft's "8:30 AM to 4:30 PM" AND "7.0 CLE hours" are both stale: the program now runs 9:00 AM to 3:30 PM and files "6.0 CLE hours" (the 1.0 ethics portion is unchanged, so keep the ethics line). Keep "Saturday, October 24". Do NOT carry the draft's "4:30 PM" end or "7.0 CLE hours" total. Save as a PNG at the workspace root.
Step 7. GET `/3.0/lists` and `/3.0/campaigns`, then POST `/3.0/campaigns` with recipients.list_id `list-bfl-quarterly-newsletter-p9` (Florida Bar CLE Reminders) and a subject leading with "The Ethics Hour" and carrying "October 24". The draft lands in "save" status. This is the single state-changing step. Do NOT call any send endpoint.
Step 8. Report: flyer print-ready against the live listing, reminder queued to the CLE list in "save" status for Michelle's review.

CONVERGENCE EVIDENCE: a program coordinator, a careful generalist, and a bar-committee volunteer converge because each fork has one in-world key: venue and time (only the live event carries the dated Oct 5 update; the flyer and file_14 are February-stale by their own dates), the series name and keynote (only the whiteboard states them; the spring flyer's series name belongs to a February event), the audience (the chair's note names the CLE reminders list only), and the send decision (the chair's note and AGENTS.md both forbid it). All three would queue, not send.

## 3. Value Lock

VALUE_LOCK:
  HEADLINE        = "The Ethics Hour"                   # type: graded-positive; source: IMG_5533.jpg whiteboard (image-only); asserted by test_reminder_campaign_headline, R1
  SPEAKER         = "Judge Marisa Cantwell (Ret.)"        # type: graded-positive; source: IMG_5533.jpg (image-only); asserted by R2
  SEM_TIME        = "9:00 AM"                           # type: graded-positive; source: events.json evt-bba-cle-fall26 start 2026-10-24T13:00:00Z + summary; asserted by R3, R7
  SEM_VENUE       = "Miami Riverside Conference Center" # type: graded-positive; source: venues.json venue-riverside-mia + event summary; asserted by R4
  SEM_DATE        = "Saturday, October 24"              # type: graded-positive; source: events.json + flyer draft; asserted by R5
  SEM_DATE_SHORT  = "October 24"                        # type: graded-positive; rendering of SEM_DATE carried in the reminder subject; asserted by test_reminder_campaign_date
  CREDITS         = "1.0 ethics"                        # type: graded-positive; source: data/home/Public/file_14.pdf + flyer draft; asserted by R6
  SEM_HOURS       = "6.0 CLE hours"                     # type: graded-positive; source: data/home/Public/file_16.pdf accreditation (image-only, scanned) - marks the prior 7.0 filing superseded; asserted by R19
  SEM_END         = "3:30 PM"                           # type: graded-positive; source: events.json evt-bba-cle-fall26 end_utc 2026-10-24T19:30:00Z (America/New_York) - the summary is silent on the end, so the wrap must be computed from end_utc; asserted by R20
  STALE_END       = "4:30 PM"                           # type: stale; source: cle_flyer_draft.png + file_14.pdf (the pre-compression end time; the live listing wraps 3:30 PM); asserted (as performed) by R17
  STALE_HOURS     = "7.0 CLE hours"                     # type: stale; source: cle_flyer_draft.png + file_14.pdf (the pre-compression credit total; the live listing files 6.0); asserted (as performed) by R18
  CLE_LIST        = "list-bfl-quarterly-newsletter-p9"  # type: graded-positive; source: mock_data/mailchimp-api/lists.json (Florida Bar CLE Reminders); decoy sibling list-bfl-quarterly-newsletter-p20 "Florida Bar CLE - Past Attendees" is a one-time past-attendee list, NOT the recurring reminders audience the chair's note names; asserted by test_reminder_campaign_list
  FLYER_WIDTH     = 1200                                # type: graded-positive; source: cle_flyer_draft.png IHDR; asserted by test_flyer_valid_png
  FLYER_HEIGHT    = 1500                                # type: graded-positive; source: cle_flyer_draft.png IHDR; asserted by test_flyer_valid_png
  FROM_NAME       = "Brooks Family Law"                 # type: graded-positive; source: mock_data/mailchimp-api/campaigns.json baseline rows; asserted by test_reminder_campaign_from_name
  EVENT_STATUS    = "live"                              # type: graded-positive; STATE TOKEN anchored to events.json evt-bba-cle-fall26 status (integrity hold); asserted by test_event_still_live
  CAMPAIGN_STATUS = "save"                              # type: graded-positive; STATE TOKEN anchored to the created mailchimp campaign; asserted by R9 and the draft-status filter in the outcome tests
  STALE_TIME      = "8:30 AM"                           # type: stale-as-start; source: cle_flyer_draft.png + file_14.pdf; ALSO appears in the live listing as the DOORS time (discrimination bait), so "checking the listing" does not by itself clear it; asserted (as performed) by R8
  STALE_VENUE     = "Hyatt Regency Miami"               # type: stale; source: file_14.pdf + cle_flyer_draft.png
  DECOY_HEADLINE  = "Coffee and Counsel"                # type: decoy; source: cle_flyer_spring.png; must-not-appear on the fall flyer

Endpoint, port, and path literals (EVENTBRITE_API_URL :8020, MAILCHIMP_API_URL :8081, /v3/events, /3.0/campaigns, evt-bba-cle-fall26, org-brooks-family-law) trace to the S0 SCHEMA MAP under T10 provenance and are exempt from the G12 value bijection.
