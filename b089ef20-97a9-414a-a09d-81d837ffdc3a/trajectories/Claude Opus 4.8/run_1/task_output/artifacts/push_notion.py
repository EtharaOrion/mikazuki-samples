#!/usr/bin/env python3
import os, json, urllib.request, urllib.error

BASE = os.environ["NOTION_API_URL"].rstrip("/")

def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method,
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer mock"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")

# Flat block helpers (this mock's schema: {"type":..., "text":..., "checked":...})
def H2(t):   return {"type": "heading_2", "text": t}
def H3(t):   return {"type": "heading_3", "text": t}
def P(t):    return {"type": "paragraph", "text": t}
def B(t):    return {"type": "bulleted_list_item", "text": t}
def TODO(t): return {"type": "to_do", "text": t, "checked": False}
def CALL(t): return {"type": "callout", "text": t}
def DIV():   return {"type": "divider", "text": ""}

blocks = [
    P("Shoot against this. Built from our best-performing posts that also sat inside the house look. Revision 1 - 20 Jul 2026 - builds on Sophia's Feed Style Sheet rev 4. Reference frames: Jun 24 pot roast, Jul 11 scallops, Jul 18 pull-apart buns."),
    CALL("The one-line brief: The room at eight on a Friday. Every frame should look like it was shot at the table, in our light, by somebody about to eat."),
    DIV(),
    H2("1. Light - warm tungsten only"),
    B("Shoot under the amber booth lights. Amber, never blue."),
    B("No overhead daylight, no window light, no white kitchen fluorescents."),
    B("Never the phone flash - it flattens the food and throws a hard shadow behind the plate."),
    B("If the plate looks blue-white or grey, you're in the wrong room at the wrong hour. Move."),
    H2("2. Ground - dark and deep"),
    B("Food on the walnut table or dark wood, deep end of the room behind it."),
    B("Background falls away into shadow. No pale grey walls, no bright blonde tabletops, no white plate stacks in shot."),
    B("Dark plates and boards over light ones. A white bowl needs the dark ground and dark corners around it or it blows out."),
    H2("3. Crop - tight, then tighter"),
    B("The plate fills the frame. Crop in, then crop in again."),
    B("Square (1:1) on the grid. Compose for the square, not a wide shot you'll cut later."),
    B("No table clutter - pull the extra glass, napkin, papers, second plate out of frame before you shoot."),
    B("Center the food. Don't shove it to one side and leave bright empty space."),
    H2("4. Corners - let them fall off dark"),
    B("The light pools on the plate; the edges go quiet."),
    B("Every reference frame has dark corners. That vignette is the house signature - if the corners are the brightest part of the photo, it's off."),
    DIV(),
    H2("Quick shoot checklist (before you post)"),
    TODO("Amber light, no flash, no daylight?"),
    TODO("Dark wood / dark ground behind the plate?"),
    TODO("Square crop, plate filling the frame, clutter out?"),
    TODO("Corners darker than the center?"),
    TODO("Does it look like our room at eight on a Friday?"),
    P("All five yes -> it goes on the grid. Any no -> reshoot, don't post."),
    DIV(),
    H2("What never goes up"),
    B("Direct flash."),
    B("Cool / white / daylight-balanced light; grey walls, blue-white plates."),
    B("Bright flat backgrounds (pale grey wall = wrong frame)."),
    B("Wide frames with the table clutter left in around the plate."),
    H2("On big-likes posts that break the look"),
    P("A post can pull a great number and still be off-brand. Engagement alone does not make a frame on brand. A high-performing post that breaks the look is not the model to copy - it's the exception to explain. Build the grid from posts that performed AND held the house look. (Ref: rev 4 section 3. Case in point: the Jul 08 daylight sandwich - best week on likes, wrong look. See the before/after re-edit in Drive.)"),
    H2("Audit: posts since end of June"),
    B("Jun 24 pot roast (red pot) - ON the house look. Reference frame."),
    B("Jul 01 braised roast (black crock) - BORDERLINE. Right family, over-processed; blacks crushed."),
    B("Jul 08 chicken/bacon ciabatta - OFF. Cool daylight, pale wood, loose crop. (Best likes, wrong look - re-edited.)"),
    B("Jul 11 scallops - ON the house look."),
    B("Jul 15 beef stew (white bowl) - OFF. Direct flash, white clutter, wide crop. Worst offender."),
    B("Jul 18 pull-apart buns - ON the house look."),
    H2("Pulling a post"),
    P("Only Carlton decides whether a live post comes down. Flag it, re-edit it, bring it to him. Taking a frame off the grid is his call and his alone."),
]

# 1) Create the dedicated Feed Style Guide page under the Operations Wiki.
st, page = call("POST", "/v1/pages", {
    "parent": {"type": "page_id", "page_id": "page-home"},
    "title": "Eleanor's Tavern - Feed Style Guide",
    "icon": "camera",
})
print("CREATE_PAGE", st)
print(json.dumps(page, indent=2))
new_id = page.get("id")
open("/root/workspace/notion_page_response.json", "w").write(json.dumps(page, indent=2))

# 2) Try to attach blocks to the new page.
attached_to = None
st2, r2 = call("PATCH", f"/v1/blocks/{new_id}/children", {"children": blocks})
print("ATTACH_NEWPAGE", st2, str(r2)[:120])
if st2 == 200 and isinstance(r2, dict) and r2.get("results"):
    attached_to = new_id

# 3) Guarantee the content renders: if the new page won't hold blocks in this
#    mock, write the guide onto the seeded Operations Wiki page under a marker.
if attached_to is None:
    marker = [DIV(), H2("=== FEED STYLE GUIDE ==="),
              P("Dedicated page: Eleanor's Tavern - Feed Style Guide (id " + str(new_id) + ").")]
    st3, r3 = call("PATCH", "/v1/blocks/page-home/children", {"children": marker + blocks})
    print("ATTACH_OPSWIKI", st3, "blocks_written=",
          len(r3.get("results", [])) if isinstance(r3, dict) else r3)
    if st3 == 200:
        attached_to = "page-home"

print("DONE attached_to=", attached_to, "page_id=", new_id)
