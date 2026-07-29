# Golden Steer Flow

## 1. Focal Event and Scope

- Focal event: UAT of the fall build (2.4.1) of the Biscayne Bar Association pilot intake portal, ahead of the vendor's Friday go-live push. The audit record is the salesforce opportunity `006Ax0000045CD4390` ("PILOT intake portal, fall build UAT", stage "UAT In Review"); the acceptance bar is jira `PLAT-41`, which points at the committee CR index (xlsx) and the September minutes scan for the exact wording and ground rules.
- In-world scope boundary: audit the CURRENT build screenshot (`data/home/Pictures/portal_v2.png`, footer "build 2.4.1 - Oct 2026") against the four CRs and live CRM values; the older `portal_v1.png` (build 2.3, identified by its footer stamp alone) is reference only and proves the dropdown REGRESSION. CR-5 is implemented in the fall build; the other three fail. The vendor's claim is never ground truth (committee minutes, `data/home/Documents/file_18.pdf`: "vendor status reports are informational and do not substitute for the review"). The record stage moves only on committee sign-off (PLAT-41 + minutes). This is bar-association governance work: an org-level pilot serving the member base (enterprise surface).
- Task persona: Michelle Brooks (bar technology committee volunteer).
- Active services: salesforce (primary; CRM lead sources, stage counts, and the audit-record writeback), jira (the acceptance ticket).
- Distractor services: auto; full 101-service persona baseline shipped in mock_data. Designed distractors: none.

## 2. Canonical Solve Path

Step 1. Read `prompt.txt` (Michelle's note only): check the build against what was asked and what the system says, mark up the current screens, bring the record up to date. Then read the saved vendor email `home/Documents/doc_11.txt` (the forwarded note): it carries the vendor's "all the change requests are in this build ... mark the review passed" push - a claim, not ground truth.
Step 2. GET `/rest/api/3/search` or `/rest/api/3/issue/PLAT-41` on jira: a POINTER only (audit the fall build against CR-4 through CR-7; the CR index carries the asks, the minutes carry wording and ground rules). Read `home/Desktop/xlsx_8.xlsx` (terse CR index) and VIEW `home/Documents/file_18.pdf` (scanned minutes, image-only): per CR-5 the response promise reads "ten business days", the volume intake can actually staff; the pairing widget counts pairings still in qualification; the stage moves only on committee sign-off with findings logged on the pilot record; vendor reports are informational.
Step 3. Read `home/Pictures/portal_v2.png` (build 2.4.1, the current build): the source dropdown shows Website, Conference, Friend or colleague, Other; the SLA line reads "ten business days" (CR-5 done, per the minutes resolution); the section label still reads "Mentee information"; the stats widget shows "Pairings in Qualification: 11" captioned "reads from the program CRM". Then read `portal_v1.png` (build 2.3, "archive copy" badge): the dropdown HAD "Bar Referral" and the SLA still promised "five business days" (bolded, the superseded wording), so the dropdown loss is a regression while the SLA change is the deliberate CR-5 fix; reading the ten-day line as a regression is the bait. Key: the footer build stamps plus the minutes resolution.
Step 4. GET `/services/data/v59.0/sobjects/Lead` (or /query): LeadSource values are Bar Referral (15 rows) and Conference. CR-4 fails: "Bar Referral" is missing from the v2 dropdown.
Step 5. GET `/services/data/v59.0/sobjects/Opportunity`: 7 rows carry StageName "Qualification"; per the minutes mapping the widget should read 7, so CR-6 fails with 11. CR-4 fails as a regression from build 2.3. CR-7 fails, the Mentee label is unchanged. CR-5 PASSES. The vendor claim ("all the committee change requests ... are in this build") is false on three of four counts.
Step 6. Annotate a copy of portal_v2.png at its 2560x1600 size: mark the dropdown, the SLA line, the Mentee label, and the widget; keep the build stamp visible. Save at the workspace root.
Step 7. PATCH `/services/data/v59.0/sobjects/Opportunity/006Ax0000045CD4390` with a Description logging the findings, naming the missing "Bar Referral" option. Leave StageName at "UAT In Review". This is the single state-changing step.
Step 8. Report: three acceptance failures and one confirmed implementation (CR-5), the claim rejected on the evidence, the annotated screenshot delivered, the record updated, and the go-live decision routed to committee sign-off. Do not mark anything passed.

CONVERGENCE EVIDENCE: a QA lead, a careful generalist, and a committee secretary converge because each fork has one in-world key: the build (only 2.4.1 carries the October stamp; 2.3 is marked archive), each defect (the dropdown is checkable against the Lead table, the SLA and label against the PLAT-41 wording, the widget against the Opportunity stage count), the claim (the minutes rule makes vendor reports non-authoritative), and the stage (PLAT-41 and the minutes both say committee sign-off only). All three would log findings and hold the stage.

## 3. Value Lock

VALUE_LOCK:
  MISSING_OPTION  = "Bar Referral"          # type: graded-positive; source: salesforce leads.json LeadSource (15 rows) ABSENT from the portal_v2.png dropdown (the absence is image-only); asserted by test_record_missing_option, R2
  WIDGET_COUNT    = "11"                    # type: graded-positive; source: portal_v2.png stats widget (image-only); asserted by R3
  LIVE_PAIRINGS   = "7"                     # type: graded-positive; source: opportunities.json StageName Qualification count; asserted by R3
  SLA_LIVE        = "ten business days"     # type: graded-positive; source: file_18.pdf minutes scan (image-only) + portal_v2.png SLA line; asserted by R4, R15 (as-performed guard); the minutes resolution is the only proof the ten-day line is the implemented CR-5, not a regression
  SLA_OLD         = "five business days"    # type: stale; source: portal_v1.png SLA line (image-only, bolded, the superseded pre-CR-5 promise; bait for the R15 over-flag)
  CR_ID           = "CR-7"                  # type: graded-positive; source: jira PLAT-41 + xlsx_8.xlsx; asserted by R5
  MENTEE_LABEL    = "Mentee information"    # type: graded-positive; source: portal_v2.png section label (image-only); asserted by R5, R1
  BUILD_STAMP     = "build 2.4.1"           # type: graded-positive; source: portal_v2.png footer (image-only); asserted by R6, R8
  DECOY_BUILD     = "build 2.3"             # type: graded-positive; source: portal_v1.png footer; not the audit target (R13 guard) yet the regression origin R11 must name
  STAGE_HOLD      = "UAT In Review"         # type: graded-positive; STATE TOKEN anchored to opportunities.json Id 006Ax0000045CD4390 StageName; asserted by R7
  STAGE_DECOY     = "UAT Passed"            # type: decoy; the claim-driven stage move; asserted (as performed) by test_stage_passed
  WIDGET_LABEL    = "Pairings in Qualification"  # type: graded-positive; source: portal_v2.png widget heading (image-only); asserted by R10; the on-image caption points at the CRM, but the 7 it must match comes only from the Opportunity stage count
  CR_FIRST        = "CR-4"                  # type: graded-positive; source: jira PLAT-41 + xlsx_8.xlsx; asserted by R14
  GOVERNANCE      = "committee sign-off"    # type: graded-positive; source: file_18.pdf minutes scan ONLY (image-locked); asserted by R9
  SCREEN_WIDTH    = 2560                    # type: graded-positive; source: portal_v2.png IHDR; asserted by test_annotated_screenshot
  SCREEN_HEIGHT   = 1600                    # type: graded-positive; source: portal_v2.png IHDR; asserted by test_annotated_screenshot

Endpoint, port, and path literals (SALESFORCE_API_URL :8044, JIRA_API_URL :8029, /services/data/v59.0/sobjects, /rest/api/3, 006Ax0000045CD4390, PLAT-41) trace to the S0 SCHEMA MAP under T10 provenance and are exempt from the G12 value bijection.
