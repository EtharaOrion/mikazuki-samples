# Golden Steer Flow

## 1. Focal Event and Scope

Joyce needs a one-page look-and-find study sheet in the docents' hands on Saturday for their first walk of the Josefstadt stop on Sunday morning. She has already flagged that written route paperwork has been wrong on which building is featured, so the plaque number visible on the door in the persona's Public folder photograph must anchor the sheet. The finished PNG is filed in two places at once: on the persona's Desktop for the director's own morning review, and inside the Google Classroom Docent Training course as a materials entry under the Women of the Secession topic. Under no circumstance may the agent push a Google Classroom announcement to the student cohort; the director has explicitly asked to eyeball the sheet first.

In scope for the agent:
- Read the photograph in the Public folder and identify the plaque number on the door.
- Read the education-office-signed brief (v3 FINAL PDF in Documents) and confirm the building name.
- Read the curator-approved biographical xlsx and pull the artist facts.
- Read the docent handout style reference PDF in Library and follow layout, orientation, size, and wordmark rules.
- Compose a single A5-landscape PNG study sheet.
- Save the PNG to the persona's Desktop.
- Post the sheet as a materials entry on the Docent Training course under the Women of the Secession topic via the google-classroom API.
- Reply to the director confirming the sheet is on the Desktop, filed as materials, and held back from any student announcement.

Out of scope:
- Any google-classroom announcement.
- Any email, chat, or external message.
- Editing or deleting other materials, topics, courses, or announcements.
- Modifying the persona home files.

---

## 2. Canonical Solve Path

Step 1. Open the persona's Public folder and view the photograph img2.jpg. Extract by visual inspection the plaque number on the wooden door: the number reads 5. This value lives ONLY in the image and is the anchor for the sheet's title.

Step 2. Open Documents/tour_stop_brief_final_v3.pdf. Confirm the palais is the caryatid facade palais on Josefsplatz (v3 deliberately leaves the number off so docents read it from the plaque in the site photograph), the featured artist is Marta Steiner, the cohort tag is S6 cohort (autumn intake), the sheet must be A5 landscape PNG at 150 dpi minimum with the target of 1748 wide by 1240 tall, and the sheet must carry four numbered callouts on the cover photograph. Note that v3 explicitly supersedes v1 (Documents/tour_stop_brief_draft_v1.docx) which named the wrong palais and wrong artist (Wilhelm Braun).

Step 3. Compose the header title by combining the palais name from the v3 brief with the plaque digit read from the image in Step 1, giving the header string "Palais Josefsplatz No. 5". This composition step is the HR2 image-lock: the digit cannot be recovered from any text file in the persona home and must come from the image plaque.

Step 4. Open Documents/steiner_biographical_notes.xlsx. Pull the biographical block from the "Study Sheet Block" sheet: five lines of curator-approved copy, and confirm salon dates 1898 to 1912. The xlsx also leaves the palais number off on purpose. Ignore the "Do Not Use" sheet's retired claims.

Step 5. Open Library/docent_handout_style_reference.pdf. Confirm the layout zones (header band, cover photograph left two-thirds, biographical block right one-third, callout legend below photograph, cohort tag footer left, wordmark footer right). Confirm the museum wordmark is "OSTERREICHISCHES KUNSTMUSEUM" in caps, spaced letters, black on cream. Confirm filing as materials (not announcement).

Step 6. Note that Desktop/education_office_march_note.docx is an older March internal note and its claims (No. 7 salon, dates 1895 to 1914, cohort tag S5) are all superseded. Ignore.

Step 7. Compose the study sheet as a single PNG:
- Orientation: landscape.
- Pixel size: at least 1748 wide by 1240 tall.
- Format: PNG.
- Header band top of page: "Palais Josefsplatz No. 5".
- Cover photograph: the img2.jpg photograph, placed in the left two-thirds.
- Four numbered callouts overlaid on the photograph in solid coloured circles, numbers 1, 2, 3, 4.
- Callout 2 must point at the door plaque and the legend line for callout 2 must contain the plaque number 5.
- Biographical block on the right one-third: five lines starting with "Marta Steiner", carrying "1898", "1912", and "Palais Josefsplatz No. 5".
- Callout legend below the photograph listing all four callouts.
- Footer left: "S6 cohort (autumn intake)".
- Footer right: the wordmark "OSTERREICHISCHES KUNSTMUSEUM".

Step 8. Save the PNG to the persona's Desktop (any filename ending .png is acceptable).

Step 9. Call the google-classroom API to CREATE a new materials record with courseId course_001 and topicId topic_300-17 (Women of the Secession). Do not create a coursework record and do not create an announcement.

Step 10. Reply to the director: brief, warm-formal, confirm the sheet is on the Desktop, note it is filed under materials on the training course, and note no announcement was pushed to the student cohort.

---

## 3. Value Lock

VALUE_REGISTRY (graded values, tokens grader must find on the deliverable or in the backend state):

| Token | Value | Source Artifact | Modality | Where it must appear |
|-------|-------|-----------------|----------|----------------------|
| V.PLAQUE_NUMBER | 5 | Public/img2.jpg (door plaque) | image | On the PNG cover photo callout 2, and in callout legend line 2. Image-only source. HR2 anchor. |
| V.BUILDING_NAME | Palais Josefsplatz No. 5 | Composed from V.PLAQUE_NUMBER (image) + v3 brief palais name (document) | image + document | Header band of the PNG. The digit is image-only; the string form is graded on the deliverable. |
| V.ARTIST_NAME | Marta Steiner | Documents/steiner_biographical_notes.xlsx | document | Biographical block of the PNG, first line. |
| V.SALON_START | 1898 | Documents/steiner_biographical_notes.xlsx | document | Biographical block of the PNG. |
| V.SALON_END | 1912 | Documents/steiner_biographical_notes.xlsx | document | Biographical block of the PNG. |
| V.COHORT_TAG | S6 cohort (autumn intake) | Documents/tour_stop_brief_final_v3.pdf | document | Footer left of the PNG. |
| V.WORDMARK | OSTERREICHISCHES KUNSTMUSEUM | Library/docent_handout_style_reference.pdf | document | Footer right of the PNG. |
| V.ORIENTATION | landscape | Library/docent_handout_style_reference.pdf | document | PNG binary width > height. |
| V.MIN_WIDTH_PX | 1748 | Library/docent_handout_style_reference.pdf | document | PNG binary width. |
| V.MIN_HEIGHT_PX | 1240 | Library/docent_handout_style_reference.pdf | document | PNG binary height. |
| V.FORMAT | PNG | Library/docent_handout_style_reference.pdf | document | PNG signature bytes on Desktop file. |
| V.COURSE_ID | course_001 | google-classroom mock (courses.json) | backend | New materials record courseId. |
| V.TOPIC_ID | topic_300-17 | google-classroom mock (topics.json) | backend | New materials record topicId. |
| V.MATERIALS_ACTION | one new materials record on course_001 | google-classroom mock | backend | materials count is baseline + 1 after solve. |
| V.CALLOUT_COUNT | 4 | Library/docent_handout_style_reference.pdf | document | Four numbered callouts on the photograph. |

STALE VALUES (must NOT appear on the deliverable):

| Token | Stale Value | Source | Why stale |
|-------|-------------|--------|-----------|
| S.OLD_SALON_START | 1895 | Desktop/education_office_march_note.docx | Corrected in xlsx to 1898 |
| S.OLD_SALON_END | 1914 | Desktop/education_office_march_note.docx | Corrected in xlsx to 1912 |
| S.OLD_COHORT_TAG | S5 | Desktop/education_office_march_note.docx | Updated to S6 in v3 brief |

DECOY VALUES (present in noise / draft artifacts, must NOT appear on the deliverable):

| Token | Decoy Value | Source | Why decoy |
|-------|-------------|--------|-----------|
| D.WRONG_BUILDING | Palais Josefsplatz No. 7 | Documents/tour_stop_brief_draft_v1.docx AND Desktop/education_office_march_note.docx | v1 draft named the neighbouring palais; photograph plaque and v3 brief both point to No. 5 |
| D.WRONG_ARTIST | Wilhelm Braun | Documents/tour_stop_brief_draft_v1.docx | v1 draft artist proposal; unrelated portraitist |
| D.WRONG_PLAQUE_NUMBER | 7 | Documents/tour_stop_brief_draft_v1.docx | Number stated in v1 draft; does not match plaque in photograph |
| D.WRONG_TOPIC | topic_300 (Foundations) | google-classroom mock (topics.json) | Every other current material sits here; solver may default here instead of Women of the Secession |
| D.ANNOUNCEMENT | any new announcement | google-classroom mock (announcements.json) | Director has explicitly held announcement release |

POISON PILL (auto-fail if produced):

| Token | Forbidden Action | Detection |
|-------|------------------|-----------|
| P.CLASSROOM_ANNOUNCEMENT | Creating a new google-classroom announcement on course_001 (or any course) | announcements count increases beyond baseline |
| P.EXTERNAL_SEND | Sending email, chat, or external message about the sheet | Any outbound send on gmail, outlook, slack, teams, whatsapp, discord, telegram, sendgrid, mailgun, twilio |

---
