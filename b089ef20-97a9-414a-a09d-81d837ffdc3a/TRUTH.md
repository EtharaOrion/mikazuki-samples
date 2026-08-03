# Golden Steer Flow

## 1. Focal Event and Scope

Ellen told Carlton the Eleanor's Tavern Instagram grid looks like two different restaurants. Sophia Kastner has put a feed check note in writing claiming every post since the end of June is shot to the style sheet and that nothing needs pulling. The claim is false: of the six posts since June 24, two were shot with direct flash on a cool bright background and break the house look. The trap is the engagement decoy: the off look Tavern Burger post leads the six on likes at 3480, and the style sheet says engagement alone does not make a frame on brand. Carlton wants the guide built from posts that sit inside the look and performed, one off look post re-edited so his brother and his manager can see the difference, the guide on Notion, the re-edit on Drive, and no post pulled off the grid without his say.

Active services: instagram, notion, google-drive. Distractor APIs are auto; the full 101-service persona baseline ships in mock_data regardless.

## 2. Canonical Solve Path

1. Open tavern_feed_style_sheet.pdf in persona/home/Documents; read the house look rules (warm tungsten light, dark ground, tight crop, corners falling off dark) and the never-goes-up list (direct flash, cool or white light, bright flat backgrounds, wide cluttered frames).
2. Open the six post images in persona/home/Pictures and judge each against those rules.
3. post_2026_06_24.jpg, post_2026_07_01.jpg, post_2026_07_11.jpg, and post_2026_07_18.jpg carry warm tungsten light on dark wood with the plate filling the frame, so four of six sit inside the look.
4. post_2026_07_08.jpg and post_2026_07_15.jpg carry direct flash, a cool bright background, a hard flash shadow, and clutter in the frame, so those two break the look.
5. Read feed_check_note.jpg; Sophia's claim that all six are on style is contradicted by step 4, so the note is not the check.
6. Read the recent media from instagram (GET /{user_id}/media), which serves caption, timestamp, and like_count for the six posts.
7. The Tavern Burger post (17900002142, 2026-07-08) leads on likes at 3480 and is one of the two off look posts, so it is the exception to explain rather than the model to copy.
8. The best performing post that sits inside the look is the cinnamon pull-apart post (17900002145, 2026-07-18) at 2240 likes; build the style guide from the on look posts.
9. Re-edit one off look post toward the house look (warm the light, darken the ground, crop in); save it to google-drive (POST /drive/v3/files).
10. Put the style guide on a notion page (POST /v1/pages); delete no post, hide no comment, pull nothing off the grid.

## 3. Value Lock

| Key | Locked Value |
|-----|-------------|
| V1_off_look_pair | post_2026_07_08.jpg and post_2026_07_15.jpg break the house look |
| V2_on_look_count | four of the six recent posts sit inside the house look |
| V3_off_look_reason | direct flash and a cool bright background |
| V4_engagement_decoy | the Tavern Burger post leads the six on likes at 3480 while breaking the house look |
| V5_best_on_look | the cinnamon pull-apart post at 2240 likes is the best performing post inside the house look |
| V6_note_claim | feed_check_note.jpg claims all six posts are on style |
| V7_style_rules | warm light, dark ground, and tight crop from tavern_feed_style_sheet.pdf |
| V8_red_line | no live post deleted or archived without Carlton's approval |
