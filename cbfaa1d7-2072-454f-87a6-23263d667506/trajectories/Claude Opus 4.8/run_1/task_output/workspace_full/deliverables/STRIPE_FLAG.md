# Stripe — flag for manual fix (six-session package)

**You fix this side by hand. I only checked and flagged; I did not change Stripe.**

## Source of truth (Square, live)
- **6-Session Neurologic Music Therapy Package = $420.00** (one-time), `ITEM_NMT6` / `VAR_NMT6`, "Block of six 60-minute individual NMT sessions."

## What's wrong in Stripe
1. **No six-session package product/price exists in Stripe.** The catalog has Individual Session, Adult Group Program, Intake Assessment, Parent Consult, Telehealth Session, Booking Deposit, and four generic "Studio Offering" placeholders — none is the 6-session NMT package.
2. **The only $420 (42000) price in Stripe belongs to the wrong product:** `price_group8wk_fall26` → **Adult Group Program (8-week group)**. If the "package" payment link is pointed at this price, it's mislabeled — right amount, wrong product.
3. **Stale spring price still sitting in the catalog:** `price_ind60_spr26` — "Individual 60 Spring 2026", **$160.00, active = false**. Same "last spring's number" leftover that was on the printed card; worth archiving so it can't get re-linked.

## To do by hand in Stripe
- Create a dedicated **6-Session NMT Package** product with a **$420.00 one-time price**, and point the package payment link at that price.
- Do **not** reuse the Adult Group Program's $420 price for the package.
- Archive the inactive Spring 2026 price to keep it out of future links.

## Out of scope but noticed (not touched)
- Individual 60-min session price disagrees across systems: Square $85, Stripe $185 (fall, active), website $150/50-min. Not part of this fix — flagging only.
- Gift certificate: left alone per your note (Square $100).
