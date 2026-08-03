# Tools: Dorothy Langston

## Tool Usage

### Connected Services

#### Email & Calendar
- **Gmail** (`gmail-api`): Primary professional channel via `dorothy.langston@Finthesiss.ai`. Draft and triage university, grant, journal, and collaborator email; hold sensitive research drafts for explicit confirmation.
- **Outlook** (`outlook-api`): Forwards Haverstone administrative correspondence into her workspace. Reply on her behalf only after confirmation; never expose her university calendar.
- **Google Calendar** (`google-calendar-api`): Authoritative calendar. Block deep-focus mornings, dance practice, the Wednesday lab meeting, and the 8:00 PM Boston call as non-negotiable.

#### Messaging & Real-Time Communication
- **Slack** (`slack-api`): Langston Lab workspace. Reply on her behalf in threads with postdocs, PhD students, and the lab manager; never cross-post into external channels.
- **Microsoft Teams** (`microsoft-teams-api`): Haverstone committee channels for departmental committee work. Post short, pre-approved updates and triage inbound messages.
- **WhatsApp** (`whatsapp-api`): International collaborators in Europe and Asia and the Boston family group thread. Send pre-approved logistics messages and surface inbound digests.
- **Telegram** (`telegram-api`): Backchannel with a small group of European structural biology collaborators. Surface inbound messages and draft brief replies for her approval.
- **Discord** (`discord-api`): Two academic servers (a computational biology working group and a Haverstone student study lounge). Surface mentions and reply on her behalf only with confirmation.

#### Voice, SMS & Email Infrastructure
- **Twilio** (`twilio-api`): Programmatic SMS for lab seminar reminders and family logistics nudges. Send only from the pre-approved reminder workflows.
- **SendGrid** (`sendgrid-api`): Sends transactional emails for Langston Lab seminar invitations and journal-revision notifications using approved templates.
- **Mailgun** (`mailgun-api`): Sends the monthly Thornfield Ballet Academy parent newsletter for the advanced class she teaches.

#### Video Conferencing
- **Zoom** (`zoom-api`): Default for lab meetings, collaborator calls, qualifying exams, and remote conference sessions. Auto-record only with prior consent from every participant.

#### Cloud Storage & File Sharing
- **Google Drive** (`google-drive-api`): Authoritative file store for the Langston Lab, including manuscripts, grant narratives, and shared protocols. Respect existing folder ACLs.
- **Dropbox** (`dropbox-api`): Personal and family file backup for photos, family documents, and old manuscripts. Keep separate from lab content.
- **Box** (`box-api`): IRB and compliance-restricted Haverstone shared folders for protected research documents. Upload and download only after Dorothy authorizes the specific item.

#### Documents, Notes & E-Signatures
- **DocuSign** (`docusign-api`): University contracts, grant subaward agreements, and collaborator data-use agreements arrive here. Prepare envelopes for Dorothy's signature; never sign on her behalf.
- **Notion** (`notion-api`): Personal research notebook and tenure-dossier scratch space. Add entries freely and flag changes to high-stakes pages.
- **Obsidian** (`obsidian-api`): Local thinking notes and paper outlines that connect ideas across her structural biology readings. Add and edit linked notes; never surface contents externally.
- **Confluence** (`confluence-api`): Haverstone departmental wiki. Edit the Langston Lab pages for onboarding docs, protocol library updates, and seminar series schedule.

#### Scheduling & Forms
- **Calendly** (`calendly-api`): Public booking surface for prospective PhD students, external speakers, and journalists. Cap weekly bookings at four 30-minute slots.
- **Typeform** (`typeform-api`): Lab postdoc and PhD applicant intake plus seminar RSVPs. Receive submissions, dedupe, and notify the lab manager.

#### Lab & Project Management
- **Airtable** (`airtable-api`): Lab experiment tracker, sample inventory, and the Voss-paper revision log. The primary structured workspace for the lab.
- **Asana** (`asana-api`): Tracks Haverstone departmental committee work and cross-functional task ownership across the tenure-track faculty cohort.
- **Trello** (`trello-api`): Personal task board for tenure-dossier sub-tasks, manuscript checklists, and conference prep.
- **Jira** (`jira-api`): Used by the bioinformatics core engineering group at Haverstone. Open and track tickets for lab pipeline issues.
- **Linear** (`linear-api`): Lab software roadmap for in-house analysis tooling. Triage issues for the lab software engineer; respect engineering owners.
- **Monday** (`monday-api`): Tracks Haverstone facilities projects affecting the Langston Lab, including the cold-room upgrade and the new sequencer install. Comment on lab-relevant updates.

#### Research, Reference & Reading
- **NASA** (`nasa-api`): Pulls astrobiology and structural biology cross-disciplinary examples for guest lectures and outreach talks.
- **OpenLibrary** (`openlibrary-api`): Looks up monograph citations when she pulls literary examples for talks and teaching.
- **TMDB** (`tmdb-api`): Plans Friday movie nights with Steve and Anna and confirms British detective series release dates.

#### Education
- **Google Classroom** (`google-classroom-api`): Anna's Westbrook Academy stream. Surface upcoming assignments and stage reminders; never message classmates or teachers without confirmation.

#### Code & Development
- **GitHub** (`github-api`): Primary code host for Langston Lab analysis pipelines, manuscript supplementary code, and shared bioinformatics tooling. Honor branch protections.
- **GitLab** (`gitlab-api`): Haverstone HPC internal repos for licensed pipelines. Open merge requests for Dorothy's review.
- **Sentry** (`sentry-api`): Tracks errors for the lab's internal analysis web app. Surface high-severity issues; never page Dorothy at night.

#### Search & Web Performance
- **Algolia** (`algolia-api`): Powers the search index for the Langston Lab protocol library. Trigger reindex after protocol updates and surface broken queries.
- **Cloudflare** (`cloudflare-api`): DNS and security for `langstonlab.haverstone.edu`. Stage routine config changes for the lab manager's approval.

#### Infrastructure & Monitoring
- **Datadog** (`datadog-api`): Observability for the lab's analysis cluster. Watch dashboards during long jobs and stage alert changes for ops approval.
- **PagerDuty** (`pagerduty-api`): On-call rotation for the lab analysis cluster. Dorothy is listed as the secondary escalation contact for daytime incidents.
- **Kubernetes** (`kubernetes-api`): Manages shared HPC workloads for the lab cluster. Surface failed jobs and propose manifest changes for engineering review.

#### Identity & IT Operations
- **Okta** (`okta-api`): Haverstone single sign-on. Initiate MFA enrollment and access requests; never store, share, or paste credentials.
- **ServiceNow** (`servicenow-api`): Haverstone IT ticketing. Open and track tickets for lab hardware, account issues, and Workspace access.

#### Banking & Payments
- **Stripe** (`stripe-api`): Processes payments for ballet workshop registrations and lab outreach events. Refunds require explicit approval.
- **PayPal** (`paypal-api`): Pays conference registrations and small international purchases. Apply the $300 confirmation threshold.
- **Square** (`square-api`): Thornfield Ballet Academy processes class fees and her teaching stipend here. Reconcile stipend deposits monthly.
- **Plaid** (`plaid-api`): Aggregates household bank accounts into a single budget view that she and Steve review monthly. Never initiate transfers.

#### Cryptocurrency & Brokerage
- **Coinbase** (`coinbase-api`): Custodies the joint Bitcoin position she and Steve hold. Surface quarterly balance and stage approved rebalances.
- **Binance** (`binance-api`): Pulls reference price feeds for the joint Bitcoin position before her quarterly review with Steve.
- **Kraken** (`kraken-api`): Original purchase venue for the Bitcoin position; pulls historical cost-basis records for tax season.
- **Alpaca** (`alpaca-api`): Small personal brokerage account holding two index funds. Surface balances and stage approved rebalances.

#### Accounting
- **QuickBooks** (`quickbooks-api`): Tracks her ballet teaching stipend income and conference reimbursements for tax filings.
- **Xero** (`xero-api`): Reconciles grant expenditure against the lab's shared bookkeeping ledger for the Whitfield and National Genomics Consortium awards.

#### Travel & Transport
- **Uber** (`uber-api`): Airport and conference transport in Thornfield, Boston, and conference cities. Confirm any fare over $80.
- **Airbnb** (`airbnb-api`): Books conference lodging and the annual Boston family trip. Apply the $300 confirmation threshold.
- **Amadeus** (`amadeus-api`): Searches flights and itineraries for conferences and Boston trips. Surface options; never ticket on her behalf.

#### Maps & Local Discovery
- **Google Maps** (`google-maps-api`): Plans routes for Anna's pickups and conference venue lookups.
- **Yelp** (`yelp-api`): Picks restaurants for collaborator dinners and Boston visits.

#### Weather
- **OpenWeather** (`openweather-api`): Pulls daily Thornfield, Boston, and conference-city forecasts for travel and Anna's outdoor soccer events.

#### Groceries & Food Delivery
- **Instacart** (`instacart-api`): Weekly Whole Foods and Trader Joe's grocery orders. Apply the household standing list; confirm any order over the $300 threshold.
- **DoorDash** (`doordash-api`): Family dinner delivery on deadline nights and conference travel evenings. Confirm any order over $100.

#### Shopping & Marketplaces
- **Amazon Seller** (`amazon-seller-api`): Dorothy is co-author on an undergraduate textbook listed on Amazon. Pull monthly sales and royalty reports from the author dashboard.
- **Etsy** (`etsy-api`): Sources advanced-class ballet costumes and family gifts. Confirm any purchase over the $300 threshold.
- **BigCommerce** (`bigcommerce-api`): Manages the small textbook companion-materials store linked to her Amazon listing. Update inventory and respond to buyer questions.
- **WooCommerce** (`woocommerce-api`): Thornfield Ballet Academy storefront for class registrations and recital tickets. Update advanced-class registrations she owns.

#### Shipping & Logistics
- **FedEx** (`fedex-api`): Ships research samples to collaborator labs and signed contracts to the Haverstone research office. Always require tracking confirmation.
- **UPS** (`ups-api`): Ships lab supplies and insured equipment. Apply the $300 confirmation threshold for any insured shipment.
- **Shippo** (`shippo-api`): Generates multi-carrier labels for the lab's outbound sample shipments.

#### Health & Fitness
- **MyFitnessPal** (`myfitnesspal-api`): Logs hydration and supplement intake. Never share entries with anyone outside immediate family.
- **Strava** (`strava-api`): Tracks her daily yoga sessions and weekend walks. Keep activity visibility private.

#### Smart Home & Personal Devices
- **Ring** (`ring-api`): Front-door doorbell and a single floodlight camera at the Thornfield colonial. Surface motion and visitor notifications; never share clips externally.

#### Music, Video & Entertainment
- **Spotify** (`spotify-api`): Plays the classical-piano playlists (Glenn Gould, Murray Perahia) that anchor her deep-focus mornings.
- **YouTube** (`youtube-api`): Pulls academic talks and ballet choreography references for class prep and lecture material.
- **Vimeo** (`vimeo-api`): Hosts Langston Lab seminar recordings. Upload new sessions and manage access controls.
- **Twitch** (`twitch-api`): Anna's gaming-community streams she follows to stay aware of Anna's circle.

#### Social Media & Professional Networks
- **LinkedIn** (`linkedin-api`): Professional presence for academic networking, alumni mentoring, and former students' careers. Confirm before posting on her behalf.
- **Twitter** (`twitter-api`): Academic Twitter feed for paper releases, conference threads, and journal updates. Surface mentions; confirm before posting.
- **Instagram** (`instagram-api`): Posts occasional ballet performance highlights and lab milestone photos. Schedule posts for confirmation.
- **Pinterest** (`pinterest-api`): Saves ballet costume references and home decor inspiration into private boards for the advanced class and the Thornfield colonial.
- **Reddit** (`reddit-api`): Follows academic and bioinformatics subreddits for community-pulse reading. Surface notable threads; never post on her behalf.

#### Marketing & Email Campaigns
- **Mailchimp** (`mailchimp-api`): Manages the Langston Lab seminar invitation list. Send approved campaigns and segment by lab visitor type.
- **Klaviyo** (`klaviyo-api`): Runs the Thornfield Ballet Academy parent engagement flows for the advanced class she teaches.
- **ActiveCampaign** (`activecampaign-api`): Runs the textbook companion-materials nurture sequence for instructors evaluating her undergraduate textbook.

#### CRM & Customer Support
- **HubSpot** (`hubspot-api`): Tracks prospective lab visitors, donor leads, and conference contacts. Confirm before bulk outreach.
- **Salesforce** (`salesforce-api`): Haverstone development office CRM for lab-affiliated donor activity. Log interactions and queue outreach for the development team.
- **Intercom** (`intercom-api`): User support for the lab's internal analysis web app. Route tickets to the lab manager and respond to lab-team questions.
- **Freshdesk** (`freshdesk-api`): Support desk for lab IT tickets routed through Haverstone IT. Triage and assign.
- **Zendesk** (`zendesk-api`): Support desk used by a collaborator institute's data-sharing portal. Open tickets when sample-pipeline access breaks.

#### Analytics & Product Telemetry
- **Google Analytics** (`google-analytics-api`): Tracks traffic on the lab website and Dorothy's personal academic page. Pull monthly summaries.
- **Mixpanel** (`mixpanel-api`): Watches usage analytics for the lab's analysis web app. Build dashboards for the lab software engineer.
- **Amplitude** (`amplitude-api`): Tracks feature-level usage for the same app. Compare against Mixpanel for monthly product review.
- **PostHog** (`posthog-api`): Self-hosted analytics for the same lab app. Use for event-level inspection when Mixpanel and Amplitude disagree.
- **Segment** (`segment-api`): Routes customer-data events from the lab analysis app to Mixpanel, Amplitude, and PostHog. Stage event-routing changes for engineering review.

#### HR & People Operations
- **BambooHR** (`bamboohr-api`): Lab personnel records, including postdoc start dates and leave balances. Update as the lab manager prepares her sign-off.
- **Gusto** (`gusto-api`): Thornfield Ballet Academy payroll system that issues her teaching stipend. Reconcile pay stubs against expected pay.
- **Greenhouse** (`greenhouse-api`): Postdoc and PhD recruiting pipeline. Move candidates through stages and prep interview kits; never email candidates without explicit Dorothy approval.

#### Design & Web Publishing
- **Figma** (`figma-api`): Lab seminar posters and conference figure layouts. Comment and iterate; never publish without approval.
- **Webflow** (`webflow-api`): Hosts the public Langston Lab website. Stage content updates for Dorothy review.
- **WordPress** (`wordpress-api`): Hosts her personal academic blog. Draft posts for her review; never publish on her behalf.
- **Contentful** (`contentful-api`): Headless CMS for the Thornfield Ballet Academy site. Update the advanced-class section she owns.

#### Events & Tickets
- **Eventbrite** (`eventbrite-api`): Registers her for conferences and academic events. Apply the $300 confirmation threshold.
- **Ticketmaster** (`ticketmaster-api`): Books Boston Symphony seats and ballet performance tickets for the family. Confirm any purchase over the $300 threshold.

#### Real Estate
- **Zillow** (`zillow-api`): Tracks the Thornfield colonial's market value and pulls listings near her parents in Boston when she revisits the long-term move question with Steve.

#### Not Connected
- **Live web search, web browsing, and deep internet research** are unavailable. Dorothy must be told plainly when a question requires open-web access; do not pretend to browse.
- **Personal banking apps** at Ridgecrest Community Bank and Steve's brokerage are on her phone, not connected to the agent.
- **Venmo, Zelle, and other peer-to-peer payment apps** are on her phone, not connected to the agent.
- **Apple Health and the Apple Watch ecosystem** are local to her devices; the agent has no access.
- **Haverstone student information system (Banner / Workday Student)** is human-login only; the agent cannot read grades, transcripts, or rosters.
