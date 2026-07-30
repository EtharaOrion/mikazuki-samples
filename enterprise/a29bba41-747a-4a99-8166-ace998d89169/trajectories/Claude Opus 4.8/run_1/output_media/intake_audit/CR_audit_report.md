# Mentorship Program Intake Portal — Fall Build UAT Review

**Prepared for:** Bar Association mentorship pilot committee
**Subject:** Vendor ClearLine Digital, fall build `2.4.1` (Oct 2026) on `pilot.biscaynebar.org/intake`
**Checked against:** September committee change requests **CR-4 through CR-7**
**Reviewed:** July 20, 2026
**Disposition:** ⛔ **REVIEW NOT PASSED — do not go live Friday. Return to vendor with the punch list below.**

---

## 1. Why this review exists

Tomas Herrera (ClearLine) emailed on Oct 7, 2026 that the fall build is live and that
*"All the committee change requests from September are in this build, so … you can mark the
review passed and we can push the pilot live Friday."*

That claim does not hold up. Checking **what we asked for** (the September CR register) against
**what the system shows** (the vendor's own screenshots of build 2.4.1), one request was not
done at all and three cannot be accepted on a screenshot alone. Details below.

## 2. Scorecard

| CR | What we asked for | Verdict | One-line reason |
|----|-------------------|---------|-----------------|
| **CR-7** | Rename "Mentee" label to "Participant" throughout | 🔴 **NOT MET** | Section still reads "Mentee information" in build 2.4.1 |
| **CR-4** | Source dropdown mirrors the CRM lead sources | 🟠 **NOT VERIFIED** | "Bar Referral" swapped for "Friend or colleague"; not shown to match the CRM picklist |
| **CR-5** | Response-time promise updated per the intake SLA | 🟠 **NOT VERIFIED** | Promise moved "five" → "ten business days"; SLA target not confirmed |
| **CR-6** | Pairing widget reads live from the CRM | 🟠 **NOT VERIFIED** | Count moved 9 → 11 but card is still "UAT preview"; live read not demonstrated |

**Bottom line:** 0 of 4 CRs can be signed off. 1 hard fail, 3 unverified.

## 3. Findings in detail

### CR-7 — Rename "Mentee" → "Participant" (🔴 NOT MET)
- **Evidence:** The intake screen still displays the heading **"Mentee information"** in build 2.4.1,
  identical to the prior build 2.3. See `markup_current_build_v2.4.1.png` (flag 7) and
  `compare_before_after.png` (flag 1 — unchanged in *both* builds).
- This is the clearest, at-a-glance contradiction of the vendor's "all CRs are in" claim.
- **Required to close:** rename every "Mentee" instance to "Participant" (heading, and any label,
  helper text, confirmation copy, and admin views). Re-screenshot.

### CR-4 — Source dropdown mirrors CRM lead sources (🟠 NOT VERIFIED)
- **Evidence:** "How did you hear about the program?" options changed from
  `Website / Conference / Bar Referral / Other` → `Website / Conference / Friend or colleague / Other`.
- The requirement is to **mirror the CRM lead-source picklist**, not to relabel by guess. Replacing a
  Bar-specific source ("Bar Referral") with a generic one ("Friend or colleague") is a red flag for a
  *Bar Association* program.
- **Required to close:** provide the CRM lead-source list and show the dropdown matches it 1:1.

### CR-5 — Response-time promise per intake SLA (🟠 NOT VERIFIED)
- **Evidence:** Footer promise changed from "We respond to every intake within **five** business days"
  → "**ten** business days."
- The promise got **looser**, and the target number is unconfirmed. A public-facing "ten business days"
  may be the wrong direction and the wrong number.
- **Required to close:** confirm the number against the actual intake SLA document.

### CR-6 — Pairing widget reads live from the CRM (🟠 NOT VERIFIED)
- **Evidence:** "Pairings in Qualification" moved 9 → 11 between builds, captioned "reads from the
  program CRM" — but the card is still headed **"UAT preview: program stats."**
- A number changing between two static screenshots does not prove a live CRM connection.
- **Required to close:** live demo (or logged API call) showing the widget pulling current CRM data,
  and remove the "UAT preview" framing before go-live.

## 4. Acceptance reference note
The exact wording and ground rules for these CRs sit in the **September committee minutes**; those,
plus the **CRM lead-source picklist** and the **intake SLA**, are the acceptance yardstick for CR-4/5/7.
> ⚠️ A 31-minute recording (`Pictures/audio_2.mp3`) and a 15-minute recording (`Movies/audio_1.mp3`)
> are staged but **could not be transcribed** — the transcription sidecar has no `whisper` model
> available (only chat/embedding models). If either is the September committee recording, confirm the
> exact target values (CRM sources, SLA number, label wording) against it before final acceptance.

## 5. Recommendation (needs Michelle's approval before anything goes to the vendor)
1. **Do not mark the review "passed"** and **do not go live Friday.**
2. Send ClearLine the punch list: **fix CR-7 now**; supply **evidence for CR-4, CR-5, CR-6**.
3. Re-review after the corrected build + evidence land. The January cohort timeline is ClearLine's
   pressure, not a reason to accept an unverified build.

## 6. Deliverables in this folder
- `markup_current_build_v2.4.1.png` — the current screen marked up, problems flagged at a glance.
- `compare_before_after.png` — build 2.3 vs 2.4.1, showing what changed and what didn't.
- `CR_register_updated.csv` — the CR record brought up to date with evidence-based review status.
- `CR_audit_report.md` — this report.
