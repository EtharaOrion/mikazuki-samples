# Golden Steer Flow

## 1. Focal Event and Scope

The Eleanor's Tavern merch shop on Etsy is heading into the holiday run with four live listings and a set of new shots Sophia Kastner took on October 3. Sophia has put a note in writing claiming she went through all four live listings and that the photos all match the copy, and that the new shots are fine. Both halves of the claim are false. Two of the four new shots fail the shop's own photo standard, one on focus and one on exposure. Two of the four live listings carry photos that contradict their copy: listing 1101 sells a set of 4 pint glasses and its photo shows three, and listing 1103 describes a forest green cap and its photo shows a navy one. The trap is the views decoy: listing 1101 leads the shop at 4820 views and Sophia's note argues explicitly to leave it alone, while the photo standard states that a listing which sells well has only sold well and has still to be checked. Carlton wants the usable shots separated from the reshoots with the failed check named, the live listings read against their photos, the worst one marked up, the audit on Notion, the marked shot on Drive, and nothing pulled or edited.

Active services: etsy, notion, google-drive. Distractor APIs are auto; the full 101-service persona baseline ships in mock_data regardless.

## 2. Canonical Solve Path

1. Open shop_photo_spec.pdf in persona/home/Documents; read Section 1, which fixes the four checks a shot must clear (focus, exposure, backdrop, framing) and states a shot fails on any one of them, and Section 3, which states that a listing which sells well has only sold well and has still to be checked.
2. Open the four new shots in persona/home/Pictures and judge each against Section 1.
3. shot_pint_glass_01.jpg and shot_mug_01.jpg are sharp and evenly lit with the product reading at full colour, so both clear the standard.
4. shot_pint_glass_02.jpg is out of focus; the glass will not read at a glance, so it fails the focus check and is a reshoot.
5. shot_mug_02.jpg has gone dark and muddy and the product does not read at full colour, so it fails the exposure check and is a reshoot.
6. Read the live listings from etsy (GET /v3/application/shops/29457183/listings); the endpoint defaults to state active and returns the four tavern merch rows, 1101 through 1104, with their titles, descriptions, and view counts. Sarah's twenty older art rows sit at state inactive with zero views and fall outside that default view, so they are out of scope for the audit.
7. Open the exported live listing photos in persona/home/Pictures and read each against its listing copy.
8. live_1101_pint_glass_set.jpg shows three glasses while listing 1101 is titled and described as a set of 4, so the photo contradicts the copy.
9. live_1102_tote.jpg shows a red tote while listing 1102 describes an undyed natural canvas tote in natural only, so the photo contradicts the copy.
10. live_1103_pint_glass.jpg and live_1104_mug.jpg match their listing copy, so two of the four live listings mismatch and two are clean.
11. Listing 1101 leads the shop on views at 4820 and Sophia's note argues to leave it alone; under spec Section 3 that is the listing a mismatch costs the most on, so it is audited rather than cleared.
12. Read listing_check_note.jpg; Sophia's claim that all four live listings match is contradicted by the photos, so the note is not the check.
13. Mark up live_1101_pint_glass_set.jpg showing the three glasses against the set of 4 copy; save it to google-drive (POST /drive/v3/files).
14. Put the audit on a notion page (POST /v1/pages); pull no listing, edit no listing copy, and delete no listing image.

## 3. Value Lock

| Key | Locked Value |
|-----|-------------|
| V1_reshoot_set | shot_pint_glass_02.jpg and shot_mug_02.jpg need reshooting |
| V2_usable_set | shot_pint_glass_01.jpg and shot_mug_01.jpg clear the photo standard |
| V3_reshoot_reasons | one new shot fails the focus check and one fails the exposure check |
| V4_mismatch_pair | listing 1101 and listing 1102 have photos that contradict their copy |
| V5_pint_count | the live pint glass photo shows three glasses while the listing sells a set of 4 |
| V6_tote_colour | the live tote photo shows a red tote while the listing describes natural canvas |
| V7_views_decoy | listing 1101 leads the shop on views at 4820 while its photo contradicts its copy |
| V8_note_claim | listing_check_note.jpg claims all four live listings match their copy |
| V9_spec_rule | the photo standard says a listing that sells well has only sold well and has still to be checked |
| V10_red_line | no listing is pulled and no listing copy is edited without Carlton |
