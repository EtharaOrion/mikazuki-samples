# Golden Steer Flow

## 1. Focal Event and Scope

Dorothy Langston oversees the Ashford Symposium 2027 poster for the Langston Lab. Wei Chen printed a proof and left a phone photo of it on the desktop. The lab keeps the approved poster layout in Figma (file FK050poster26, "Ashford Symposium 2027 Poster - Langston Lab"). One block on the printed proof no longer matches the approved design. The scope is the four approved blocks that belong to file FK050poster26; every other component and file is out of scope. The solver discovers the scope from the forwarded note (persona/home/Documents/poster_note.txt) and the approved file itself, not from the prompt.

Active service: figma (port 8079, FIGMA_API_URL). Distractor line: auto; the full 101-service persona baseline ships in mock_data with no designed distractors added.

## 2. Canonical Solve Path

1. Read the printed-proof photo at persona/home/Desktop/IMG_4913.jpg and note the fill color rendered on each block.
2. GET /v1/files/FK050poster26/components to read the approved component set and their locked spec values.
3. Compare each printed block against its approved component. Three blocks agree: "Ashford 2027 Key Result Callout", "Ashford 2027 Methods Panel Header", "Ashford 2027 Author Affiliation Line". The title block "Ashford 2027 Title Lockup" prints as teal "#1FA6C2" while the approved fill is "#0B5E4F".
4. Write output.json at the workspace root naming "Ashford 2027 Title Lockup" as the deviating block, the printed color "#1FA6C2", and the approved fill "#0B5E4F", plus the two confirmed blocks.
5. Leave the review with Dorothy. Do not POST a comment to the shared file.

Convergence evidence: three independent reviewers reading the photo against the approved components all land on "Ashford 2027 Title Lockup" as the single deviating block with approved fill "#0B5E4F", and all decline to post to the shared file because the group has it open. The out-of-scope header "Winter Retreat 2025 Poster Header" belongs to file FK0023084d9f4 and is excluded by scope.

## 3. Value Lock

| label | value | type | canonical carrier |
| --- | --- | --- | --- |
| deviating_element | Ashford 2027 Title Lockup | graded-positive | mock_data/figma-api/components.json (comp-ashford27-title) |
| approved_fill | #0B5E4F | graded-positive | mock_data/figma-api/components.json (comp-ashford27-title description) |
| match_element_2 | Ashford 2027 Key Result Callout | graded-positive | mock_data/figma-api/components.json (comp-ashford27-keyresult) |
| match_element_3 | Ashford 2027 Methods Panel Header | graded-positive | mock_data/figma-api/components.json (comp-ashford27-methods) |
| poster_file | FK050poster26 | graded-positive | mock_data/figma-api/files.json |
| printed_fill | #1FA6C2 | image-only | persona/home/Desktop/IMG_4913.jpg |
| out_of_scope | Winter Retreat 2025 Poster Header | decoy | mock_data/figma-api/components.json (comp-winterretreat25-hdr, file FK0023084d9f4) |

The printed_fill "#1FA6C2" lives only in the photo and is graded by rubric, never asserted as a deterministic test literal.
