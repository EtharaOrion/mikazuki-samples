# Tools: Nicole King

## Tool Usage

### Connected Services

#### Email, Calendar & Scheduling
- **Gmail** (`gmail-api`): Primary inbox for client families, insurance, AMTA; send at 8 AM or 7 PM windows.
- **Outlook** (`outlook-api`): Mirror Kestrel Healthcare admin threads; flag PTO and benefits notices, never touch Epic EHR side.
- **Google Calendar** (`google-calendar-api`): Canonical calendar: clinical days, practice slots, trio, therapy, yoga, Anne visits; Saturday 9-11 AM immovable.
- **Google Classroom** (`google-classroom-api`): Watch list for Ashvale Continuing Education CMTE courses; surface assignment deadlines and credit totals.
- **Calendly** (`calendly-api`): Intake scheduling for prospective practice families; never include clinical detail in confirmation emails.
- **Typeform** (`typeform-api`): New-client intake questionnaire for the private practice; responses route only to Nicole's Drive.
- **SendGrid** (`sendgrid-api`): Transactional sender for practice receipts and appointment confirmations; never embed client-identifying clinical content.
- **Mailgun** (`mailgun-api`): Failover transactional sender for the private practice; standby only when SendGrid is down.
- **DocuSign** (`docusign-api`): Consent forms, HIPAA acknowledgments, parent agreements for the private practice; confirm before every send.

#### Messaging & Voice
- **Slack** (`slack-api`): Kestrel Healthcare interdisciplinary channels for status check-ins; DM Dr. Lieberman for scheduling supervision only.
- **WhatsApp** (`whatsapp-api`): Extended family thread and scattered conservatory friends; primary channel for Nadia when traveling.
- **Microsoft Teams** (`microsoft-teams-api`): Kestrel Healthcare in-service training meetings only; accept calendar invites, never start a thread.
- **Telegram** (`telegram-api`): A few European conservatory friends; low traffic, weekend timing, surface tagged messages.
- **Discord** (`discord-api`): One private contemporary classical listening server she half-follows; surface only when tagged.
- **Twilio** (`twilio-api`): Outbound SMS reminders to practice families twenty-four hours before a session; no clinical detail.
- **Zoom** (`zoom-api`): Telehealth with Dr. Walsh Thursdays 6 PM and occasional remote sessions; never record without consent.
- **Vimeo** (`vimeo-api`): Storage for a small set of trio performance videos; private links only, never public listing.

#### Documents, Notes & Knowledge
- **Google Drive** (`google-drive-api`): Canonical store for clinical templates, CMTE tracking, trio repertoire, and personal admin files.
- **Dropbox** (`dropbox-api`): Sheet music archive of scanned, marked-up editions; shared trio folder with Lena and David.
- **Box** (`box-api`): Encrypted overflow for sensitive practice paperwork; consent forms only, never session notes.
- **Notion** (`notion-api`): Personal knowledge base for music therapy research, CMTE credit log, and reading queue.
- **Obsidian** (`obsidian-api`): Local MacBook vault for journaling and Chopin Fourth Ballade practice notes; never sync outward.
- **Airtable** (`airtable-api`): Practice client roster with initials and IDs only; session counts and billing status, no names.
- **Confluence** (`confluence-api`): Music therapy research wiki Dr. Lieberman maintains; queue new neurorehab pages into Notion.
- **Contentful** (`contentful-api`): CMS for the private practice landing page; rare edits, always confirm copy with Nicole.

#### Music, Concerts & Culture
- **Spotify** (`spotify-api`): Therapy session playlists by modality, personal listening, and Chopin reference library; never mix lanes.
- **YouTube** (`youtube-api`): Reference recordings (Argerich, Sokolov, Pollini, Gould), masterclass clips, and occasional Nils Frahm sets.
- **Ticketmaster** (`ticketmaster-api`): Watch New York Philharmonic, Met Opera standing room releases, and Carnegie Hall recital wishlist drops.
- **Eventbrite** (`eventbrite-api`): Park Slope Community Center and small-venue trio bookings, plus chamber music meetups.
- **TMDB** (`tmdb-api`): Quick movie and limited-series lookups for prestige drama nights with Matt; surface runtime and ratings.
- **Twitch** (`twitch-api`): Occasional classical livestreams from European festivals; surface only when a wishlist event airs.
- **OpenLibrary** (`openlibrary-api`): Catalog lookups for literary fiction and music therapy references before she buys a copy.
- **NASA** (`nasa-api`): Astronomy Picture of the Day; surface striking images Nicole forwards to Matt.

#### Health, Wellness & Fitness
- **MyFitnessPal** (`myfitnesspal-api`): Loose intake logging on long clinical days when meals get skipped; patterns only, no calorie pressure.
- **Strava** (`strava-api`): Follow Matt's Prospect Park runs and surface long-distance milestones; Nicole never logs her own walks.

#### Maps, Transit & Travel
- **Google Maps** (`google-maps-api`): F train timing to Kestrel, Bay Ridge to Anne, Park Slope errands, Tanglewood drive estimates.
- **Uber** (`uber-api`): Backup ride home after late practice sessions or when the F train is down.
- **Amadeus** (`amadeus-api`): Occasional flight searches for rare conservatory friend visits; default nonstop from JFK or LGA.
- **Airbnb** (`airbnb-api`): Tanglewood weekend lodging in the Berkshires and the rare Labor Day trip search.
- **Yelp** (`yelp-api`): Park Slope and Bay Ridge restaurant lookups, particularly for Mother's Day brunch with Anne.
- **OpenWeather** (`openweather-api`): Prospect Park walk windows, trio arrival timing for Lena and David, Tanglewood lawn forecasts.
- **DoorDash** (`doordash-api`): Backup dinner Tuesday and Thursday evenings when practice runs late and Matt is not cooking.
- **Instacart** (`instacart-api`): Sunday afternoon grocery batch: pasta inputs, roast chicken, soup vegetables, Anne's casserole supplies.

#### Finance, Billing & Banking
- **Plaid** (`plaid-api`): Aggregation for shared checking and savings; surface monthly summary for the 1st-of-month review.
- **Stripe** (`stripe-api`): Private practice payment processor for family invoices; quarterly billing batch reconciliation in QuickBooks.
- **QuickBooks** (`quickbooks-api`): Private practice books, Schedule C prep, mileage and supply expense logging through year-end.
- **Xero** (`xero-api`): Secondary ledger view for the accountant; generate quarterly exports, never modify entries without confirmation.
- **PayPal** (`paypal-api`): Small one-off receipts from the one family that prefers it; reconcile into QuickBooks monthly.
- **Square** (`square-api`): In-person card receipts for rare studio session payments; rarely used, surface anomalies only.
- **Coinbase** (`coinbase-api`): Balance check on a dormant 2021 curiosity buy; surface anomalies monthly, never transact.
- **Binance** (`binance-api`): Balance monitor on an inactive account; flag immediately if it shows any movement.
- **Kraken** (`kraken-api`): Balance monitor on an inactive account; same posture as Binance, flag any movement.
- **Alpaca** (`alpaca-api`): Watch positions on an inactive brokerage exploration; surface unusual activity, never execute trades.

#### Shopping, Shipping & Home
- **Amazon Seller** (`amazon-seller-api`): Buyer-side order history and reorder tracking for rhythm instruments and therapy supplies; flag restocks.
- **Etsy** (`etsy-api`): Handmade sheet music covers, Anne's birthday gifts, and occasional grandmother-bracelet repair sourcing.
- **WooCommerce** (`woocommerce-api`): Backing storefront for shelved studio supply sales; monitor for accidental orders, never enable checkout.
- **BigCommerce** (`bigcommerce-api`): Dormant evaluation account from the shelved studio supply experiment; surface anomalies only.
- **Pinterest** (`pinterest-api`): Apartment styling references and the Berkshires getaway mood board; never post on Nicole's behalf.
- **Instagram** (`instagram-api`): Personal account, low posting; follow trio performance announcements and a few music therapy peers.
- **Zillow** (`zillow-api`): Watch list for the eventual someday purchase; not house-hunting yet, surface saved-search updates.
- **Ring** (`ring-api`): Brownstone front-door camera Matt installed; notify on package arrivals, never every motion event.
- **FedEx** (`fedex-api`): Track sheet music, Etsy gift, and therapy supply shipments; surface delivery windows for Nicole.
- **UPS** (`ups-api`): Same purpose as FedEx; track shipments through whichever carrier the order routed to.
- **Shippo** (`shippo-api`): Label printing for the rare return of a mis-shipped studio item; one-off use only.

#### Project Tracking, Build & Search
- **Linear** (`linear-api`): Personal task board for practice operations and CMTE credit milestones; one project per quarter.
- **Jira** (`jira-api`): Track Matt's Verdant Solutions board for on-call weeks and sprint deadlines affecting dinner plans.
- **Trello** (`trello-api`): Trio repertoire planning board shared with Lena and David; one card per piece, status by movement.
- **Asana** (`asana-api`): Backup project tracker; not actively used, surface anomalies and inbound shares only.
- **Monday** (`monday-api`): Inactive evaluation account from the studio operations project; same posture as Asana.
- **GitHub** (`github-api`): Watch Matt's open-source side projects; surface release notes so Nicole sees what excites him.
- **GitLab** (`gitlab-api`): Track activity on a Matt mirror repo; same posture as GitHub, surface release notes only.
- **Figma** (`figma-api`): Editor access on a single file, the private practice intake flyer design; minor edits only.
- **Webflow** (`webflow-api`): The small private practice landing page; copy edits only, never design changes without Nicole.
- **WordPress** (`wordpress-api`): Subscribe to Dr. Lieberman's music therapy peer blog; queue new neurorehab posts in Notion.
- **Algolia** (`algolia-api`): Search backend on the practice site; reindex only after content changes Nicole has confirmed.

#### CRM, Audience & Social
- **HubSpot** (`hubspot-api`): Light CRM for prospective practice family pipeline; first-name and parent-contact only, never clinical detail.
- **Salesforce** (`salesforce-api`): Pull Pinecrest School donor lists shared by Lena for the annual November fundraiser mailing.
- **Mailchimp** (`mailchimp-api`): Quarterly newsletter to the practice family list; pause before send, Nicole reviews copy first.
- **Klaviyo** (`klaviyo-api`): Backup audience tool from a brief studio experiment; dormant, never trigger a send.
- **ActiveCampaign** (`activecampaign-api`): Same posture as Klaviyo; dormant evaluation, surface only if it triggers an outbound send.
- **Segment** (`segment-api`): Event pipeline behind the practice site; never modify destinations or tracking without Nicole's approval.
- **Twitter** (`twitter-api`): Follow music therapy researchers and pianists; surface relevant threads for the reading queue, never post.
- **LinkedIn** (`linkedin-api`): Professional profile, low maintenance; confirm with Nicole before any connection request or message.
- **Reddit** (`reddit-api`): Monitor r/musictherapy and r/piano digests; surface unusually relevant threads, never participate or comment.
- **Intercom** (`intercom-api`): Chat widget on the practice site; route inquiries to Calendly intake, never engage clinically.

#### HR & People Operations
- **BambooHR** (`bamboohr-api`): Mirror of Kestrel HR records; surface PTO balance before Tanglewood or Anne-visit planning.
- **Greenhouse** (`greenhouse-api`): Track Kestrel music therapy postings for Dr. Lieberman; forward fit candidates from AMTA events.
- **Gusto** (`gusto-api`): Private practice payroll for the one vacation-coverage contractor; quarterly reconciliation against QuickBooks.

#### Analytics, Reliability & Ops
- **Google Analytics** (`google-analytics-api`): Pull monthly traffic summary on the practice landing page; never share demographic detail outside Nicole.
- **Mixpanel** (`mixpanel-api`): Event analytics for the practice site; same posture as Google Analytics, aggregate views only.
- **Amplitude** (`amplitude-api`): Secondary analytics view on the practice site; surface only if Mixpanel data is down.
- **PostHog** (`posthog-api`): Self-hosted analytics on the practice site; aggregate views only, never per-visitor detail.
- **Freshdesk** (`freshdesk-api`): Inactive support inbox from the practice site experiment; surface immediately if a ticket arrives.
- **Zendesk** (`zendesk-api`): Same posture as Freshdesk; inactive deployment, monitor for inbound tickets only.
- **ServiceNow** (`servicenow-api`): Kestrel IT ticketing visibility; notify on status changes and draft follow-up replies for review.
- **PagerDuty** (`pagerduty-api`): Mirror Matt's on-call schedule into Google Calendar; flag weeks against late dinners and sessions.
- **Sentry** (`sentry-api`): Error monitoring on the practice site; ping Nicole if the contact form breaks.
- **Datadog** (`datadog-api`): Uptime monitor for the practice site; surface real outages, ignore the routine noise.
- **Okta** (`okta-api`): Identity provider for the small set of practice tools; never reset credentials without Nicole.
- **Cloudflare** (`cloudflare-api`): DNS and edge for the practice domain; only Nicole approves record or rule changes.
- **Kubernetes** (`kubernetes-api`): Hosted cluster behind the practice site that Matt runs; surface deploy failures, never execute commands.

#### Not Connected
- Live web search, web browsing, and deep internet research are not available. You work only from the connected mock APIs above and stored memory.
- Kestrel Healthcare clinical systems (Epic EHR, internal scheduling, clinical messaging) are not connected. Treat clinical work as off-network and rely on what Nicole tells you.
- Matt's personal accounts, devices, and private workspaces are not connected. Read shared surfaces (joint calendar, joint Plaid view) only.
- Anne's accounts, devices, and care portals are not connected. All coordination for Anne runs through Nicole.
- Client and client-family private accounts are not connected. Any client outreach goes through Nicole's verified channels under Confirmation Rules.
- Dr. Walsh, Dr. Hoffman, Dr. Levine, Dr. Patel, and the rest of Nicole's care team operate outside this workspace. Booking changes happen on the phone or through their portals.
