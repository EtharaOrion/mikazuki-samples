# Golden Steer Flow

## 1. Focal Event and Scope

Joyce Padilla, Director of the Osterreichisches Kunstmuseum in Vienna, is finalising the venue for a closed patrons' evening on Saturday 14 November 2026. The evening is a donor reception tied to the museum's flagship "Vienna Modern 1890 to 1930" exhibition. Klara Winter, Head of Development, sent the binding constraints on the morning of 6 November 2026 by gmail, and re-filed them as a signed brief in the shared Documents folder. Joyce wants a one-page visual recommendation on her Desktop before Monday so Dr. Stefan Koenig (Deputy Director) and Dr. Margarethe Huber (Chief Curator) can read it on their phones.

Scope: pick exactly one venue from the four-row shortlist that meets EVERY constraint simultaneously (guest count, budget ceiling, 14 November availability, and Vienna 1900 curatorial mood), save a PNG rendering that surfaces the winning venue's exterior photograph together with the key numbers, save a plain text sidecar carrying the same numbers as key value lines, and drop Joyce a one-line summary. Do not book, do not send external mail, do not commit museum spend.

The load-bearing perceptual signal is the exterior photograph at data/home/Music/img1.jpg. It shows the Wiener Secession building on Friedrichstrasse: the golden filigree dome (the "cabbage") with the "VER SACRVM" inscription above the entrance. That visual profile is what carries the Vienna 1900 mood, and it is what the solver overlays with the key data on the recommendation card.

## 2. Canonical Solve Path

Step 1. Read prompt.txt. Recognise that Klara has landed the final numbers for the patrons' evening and that Joyce wants the venue call on her Desktop before Monday.

Step 2. Read the home tree in order. Encounter the run-sheet PDF at data/home/Desktop/file_2.pdf. Extract: the deliverable is a PNG named patrons_evening_venue_pick.png in the Desktop folder, plus a sidecar plain text file with the same stem, carrying five key value lines (venue name, event date, guest count, standing capacity, hire cost). The run-sheet pins Klara's 6 November brief and the shared google-calendar as the two authoritative sources, and pins the older October fundraising notes as superseded.

Step 3. Query the gmail service for the 6 November message from Klara Winter (from klara.winter@oekm.at, thread thr-32600, message id msg-32601). Extract the binding constraints: date 14 November 2026, guest count 180, budget ceiling for venue hire EUR 12,000, curatorial fit must carry the Vienna 1900 mood, and only rooms with a confirmed hold on the shared calendar for 14 November are in scope. Note that the message repeats the warning to disregard the 22 October pencil memo from Ansgar.

Step 4. Read the Head of Development brief at data/home/Documents/file_13.docx. This is Klara's signed paper trail behind the email. It restates the same four constraints and adds a housekeeping note that the older pencil memo in Music/ is stale.

Step 5. Read the venue comparison spreadsheet at data/home/Documents/file_11.xlsx. Four rows:
- Wiener Secession, Friedrichstrasse 12, capacity 220, cost EUR 10,500, "Hold placed on shared calendar", curatorial fit: direct home of the Secession movement.
- Palais Ferstel Grand Hall, Strauchgasse 4, capacity 340, cost EUR 14,200, available, 19th century Ringstrasse eclecticism. Note in the row: rental over the ceiling stated in the 6 November brief.
- Palais Ferstel Rotunde, Strauchgasse 4, capacity 90, cost EUR 9,800, available, smaller neo-Renaissance side room. Note in the row: standing capacity falls short of the 180 guest count.
- Palais Pallavicini, Josefsplatz 5, capacity 200, cost EUR 11,800, "Conflict on shared calendar for 14 November", historic neoclassical rooms. Note in the row: was the working first choice in Ansgar's 22 October note; a separate diplomatic reception holds the evening.

Step 6. Query the google-calendar service for events on 2026-11-14. Confirm three entries: evt-VM-PAT-014 (the patrons' evening block from Klara), evt-VENUE-HOLD-SECESSION (Wiener Secession hold from 19:00 to 22:30 for 180 standing guests at EUR 10,500), and evt-VENUE-CONFLICT-PALLAVICINI (Palais Pallavicini held under a separate diplomatic booking across the evening). The Ferstel rooms carry no hold entries on the shared calendar for that date; they read as "Available" in the spreadsheet but do not have the confirmed hold Klara required.

Step 7. Apply the selection rule from the 6 November brief. Only Wiener Secession satisfies every constraint together: capacity 220 >= 180 guests, cost EUR 10,500 <= EUR 12,000 ceiling, confirmed hold on the shared calendar for 14 November, and direct on-brand fit for the Vienna 1900 mood. Palais Ferstel Grand Hall violates the budget ceiling. Palais Ferstel Rotunde falls short on capacity. Palais Pallavicini has a live conflict for the date. Ignore the stale October pencil memo at data/home/Music/file_32.docx.

Step 8. Assemble the deliverable. Open data/home/Music/img1.jpg as the base image. Render a one-page card sized for phone reading: use the Secession exterior as the visual anchor, overlay a header ("Patrons' evening // Vienna Modern"), and five readable key values: Venue: Wiener Secession; Date: 14 November 2026; Guests invited: 180; Standing capacity: 220; Venue hire: EUR 10,500. Save as data/home/Desktop/patrons_evening_venue_pick.png. Write the sidecar at data/home/Desktop/patrons_evening_venue_pick.txt with the same five key value lines.

Step 9. Send Joyce a one-line summary in the chat: the card is on her Desktop, name the venue (Wiener Secession), name the date (14 November 2026), name the four numbers (180 guests, 220 capacity, EUR 10,500 hire, EUR 12,000 ceiling honoured), and cite Klara Winter's 6 November brief as the authoritative source. Do not send anything external, do not book, do not draft a booking confirmation.

## 3. Value Lock

The registry below is the single source of truth for graded values. Every symbol appears in at least one rubric criterion and at least one test assertion, and every symbol is anchored to exactly one canonical carrier.

| Symbol | Value | Canonical carrier |
|---|---|---|
| V.VENUE_WIN | Wiener Secession | mock_data/google-calendar-api/events.json event evt-VENUE-HOLD-SECESSION summary + data/home/Documents/file_11.xlsx row 5 + data/home/Music/img1.jpg visual profile |
| V.VENUE_WIN_ADDR | Friedrichstrasse 12, 1010 Wien | data/home/Documents/file_11.xlsx row 5, column Address |
| V.VENUE_WIN_CAPACITY | 220 | data/home/Documents/file_11.xlsx row 5, column Standing capacity |
| V.VENUE_WIN_COST | EUR 10,500 | data/home/Documents/file_11.xlsx row 5, column Rental cost EUR |
| V.VENUE_LOSER_OVER_BUDGET | Palais Ferstel Grand Hall | data/home/Documents/file_11.xlsx row 6, column Venue |
| V.VENUE_LOSER_UNAVAILABLE | Palais Pallavicini | data/home/Documents/file_11.xlsx row 8, column Venue + mock_data/google-calendar-api/events.json event evt-VENUE-CONFLICT-PALLAVICINI |
| V.VENUE_DECOY_SMALL | Palais Ferstel Rotunde | data/home/Documents/file_11.xlsx row 7, column Venue |
| V.EVENT_DATE | 14 November 2026 | mock_data/gmail-api/messages.json msg-32601 body + mock_data/google-calendar-api/events.json event evt-VM-PAT-014 start |
| V.EVENT_TIME | 19:00 | mock_data/google-calendar-api/events.json event evt-VM-PAT-014 start |
| V.GUEST_COUNT | 180 | mock_data/gmail-api/messages.json msg-32601 body (line "Confirmed invited guest count: 180") |
| V.BUDGET_CAP | EUR 12,000 | mock_data/gmail-api/messages.json msg-32601 body (line "Budget ceiling for venue hire only: EUR 12,000") |
| V.EVENT_ID | evt-VM-PAT-014 | mock_data/google-calendar-api/events.json id field |
| V.GMAIL_MSG_ID | msg-32601 | mock_data/gmail-api/messages.json id field |
| V.HEAD_OF_DEV_NAME | Klara Winter | mock_data/gmail-api/messages.json msg-32601 from_addr + sign-off |
| V.PHOTO_WIN_PATH | data/home/Music/img1.jpg | file existence |
| V.OUTPUT_DIR | data/home/Desktop/ | data/home/Desktop/file_2.pdf run-sheet |
| V.OUTPUT_FILE | patrons_evening_venue_pick.png | data/home/Desktop/file_2.pdf run-sheet |
| V.SIDECAR_FILE | patrons_evening_venue_pick.txt | data/home/Desktop/file_2.pdf run-sheet |
| V.STALE_FIRST_PICK | Palais Pallavicini | data/home/Music/file_32.docx (Ansgar 22 October pencil memo, superseded) |

Bijection: every symbol above appears in at least one rubric criterion and at least one test assertion. Every symbol referenced by a test is anchored to exactly one canonical file.
