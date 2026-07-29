# Tools: Carlton McGee

## Tool Usage

### Connected Services

#### Workspace & Daily Communication
- **Gmail** (`gmail-api`): Primary inbox at carlton.mcgee@Finthesiss.ai for vendor correspondence, family coordination, restaurant overflow, and any inbound that is not Eleanor's Tavern internal mail.
- **Google Calendar** (`google-calendar-api`): Personal and family calendar holding restaurant special events, vendor deliveries, the kids' soccer and gymnastics, Monday family meal, and the FaceTime calls with mother in Boston.
- **Google Drive** (`google-drive-api`): Menu drafts, fall and winter rollout planning, the American craft wine tasting binder, tax documents, family photos, patio expansion sketches.
- **Google Maps** (`google-maps-api`): Vendor routes (Bronx fish run, LIC pickup), drives to Astoria Park, school pickup timing, and the Boston run up I-95 for the annual visit.
- **Slack** (`slack-api`): Staff coordination channel for Eleanor's Tavern; vendor groups occasionally surface here.
- **Zoom** (`zoom-api`): Vendor pricing reviews with Atlantic Seafood, occasional FaceTime backup for mother when iOS is being uncooperative, neighborhood business association meetings.
- **Calendly** (`calendly-api`): Vendor sit-downs and the rare press request from Eater NY.
- **DocuSign** (`docusign-api`): Restaurant lease addenda, vendor master service agreements, staff onboarding paperwork, liquor license renewals.
- **Obsidian** (`obsidian-api`): Personal vault for American history reading marginalia and the family-recipe notebook he keeps trying to nail down.

#### Restaurant Operations & Storefront
- **Square** (`square-api`): Eleanor's Tavern point of sale, end-of-night close-outs, tip pool tracking, and the gift-card system.
- **Stripe** (`stripe-api`): Online reservation deposits and gift-card e-commerce on the tavern site.
- **PayPal** (`paypal-api`): Vendor payments, staff bonuses paid out of personal funds, the rare reimbursement to a regular who paid for the wrong table.
- **Airtable** (`airtable-api`): Staff schedule, wine list inventory, and the supplier rotation that Sophia keeps current.
- **Notion** (`notion-api`): Restaurant planning wiki, menu draft archive, patio expansion build-out notes, and the running list of equipment he is watching for failure.
- **WordPress** (`wordpress-api`): Eleanor's Tavern public site, menu page, hours, and the occasional news post about a tasting event.
- **Contentful** (`contentful-api`): Backs the tavern site with structured content for menu items and event listings.
- **Algolia** (`algolia-api`): Powers the menu and event search on the site so a regular can find the brisket sandwich without scrolling.
- **Google Analytics** (`google-analytics-api`): Light glance at site traffic before and after a press mention.
- **Webflow** (`webflow-api`): Hosts the Eleanor's Tavern seasonal event landing pages and the wine tasting series microsite alongside the main WordPress presence.

#### Vendor, Shipping & Supplies
- **Shippo** (`shippo-api`): Labels for the occasional wine return to importers and the gift-card holiday mailings.
- **FedEx** (`fedex-api`): Wine shipments from out-of-state importers when the tasting series stocks rare bottles.
- **UPS** (`ups-api`): Equipment deliveries when the kitchen fabricators ship from outside the city.
- **Amazon Seller** (`amazon-seller-api`): Tracks competitor pricing on restaurant supply essentials and manages bulk kitchen equipment sourcing.
- **BigCommerce** (`bigcommerce-api`): Powers the Eleanor's Tavern branded merchandise and gift card online storefront linked from the tavern site.
- **WooCommerce** (`woocommerce-api`): Handles the tavern's online catering order form embedded in the WordPress site for private event deposits and holiday meal kits.
- **Etsy** (`etsy-api`): Manages the small Eleanor's Tavern branded items storefront and Sarah's art prints that Carlton runs for the family.

#### Reservations, Reviews & Local Discovery
- **Yelp** (`yelp-api`): Active and watched; he reads every review even if he has stopped checking at 11 PM.
- **Eventbrite** (`eventbrite-api`): The American craft wine tasting series and the neighborhood business association winter mixer.
- **Ticketmaster** (`ticketmaster-api`): NYCFC matches, the Celtics when they are in town, and the rare Broadway night with Ellen.
- **Typeform** (`typeform-api`): RSVP forms for private events and the occasional staff survey when Sophia wants anonymous feedback.

#### Marketing, Newsletter & Outreach
- **Mailchimp** (`mailchimp-api`): Eleanor's Tavern newsletter to the regulars list; one send per month at most.
- **Klaviyo** (`klaviyo-api`): Runs the automated post-visit email sequences for wine tasting attendees and seasonal promotion drip campaigns.
- **SendGrid** (`sendgrid-api`): Transactional sender for reservation confirmations and gift-card receipts.
- **Mailgun** (`mailgun-api`): Handles internal staff notification emails for shift changes and prep list updates separate from the customer-facing SendGrid flow.
- **ActiveCampaign** (`activecampaign-api`): Manages customer reactivation sequences for lapsed regulars and seasonal promotion automation beyond the monthly Mailchimp newsletter.
- **Twilio** (`twilio-api`): SMS reservation reminders the day before, and the staff group blast for last-minute schedule changes.
- **HubSpot** (`hubspot-api`): Tracks the vendor relationship pipeline and incoming catering lead inquiries from the tavern website contact form.
- **Salesforce** (`salesforce-api`): Manages the private event booking pipeline and corporate catering accounts for Eleanor's Tavern.
- **Intercom** (`intercom-api`): Powers the live chat widget on the tavern site for reservation questions, event booking inquiries, and menu allergy questions.
- **Freshdesk** (`freshdesk-api`): Manages customer feedback tickets routed from Yelp responses, Google reviews, and the tavern site contact form.

#### Social, Press & Community
- **Instagram** (`instagram-api`): Active; the tavern account posts the daily special and the chef's specials, and Sophia handles the queue.
- **Twitter** (`twitter-api`): Monitors NYC food media mentions and posts Eleanor's Tavern seasonal menu updates and wine tasting series announcements.
- **LinkedIn** (`linkedin-api`): Vendor research and the rare press contact; he keeps the profile clean.
- **Pinterest** (`pinterest-api`): Curates Eleanor's Tavern menu plating inspiration, event decor ideas, and the family holiday planning boards Ellen maintains.
- **Reddit** (`reddit-api`): Monitors restaurant operator communities and NYC food subreddits for vendor recommendations and competitive signal.
- **Discord** (`discord-api`): A small server of four other Astoria operators trading supply notes.
- **Telegram** (`telegram-api`): Handles vendor communication with the Boston-based wine importer who prefers Telegram over email.
- **WhatsApp** (`whatsapp-api`): Family group with Ellen, Daniel, and the in-laws; light usage.
- **Zendesk** (`zendesk-api`): Tracks longer-running customer service interactions and hosts the FAQ knowledge base embedded in the tavern's reservation page.

#### Finance, Banking & Tax
- **QuickBooks** (`quickbooks-api`): Ellen's primary tool for restaurant books and household tracking; Carlton glances at the monthly P&L.
- **Xero** (`xero-api`): Provides secondary financial reporting views for tax preparation and the accountant's quarterly review alongside Ellen's primary QuickBooks ledger.
- **Plaid** (`plaid-api`): Connects Chase savings, the restaurant operating account, and the SEP-IRA for the consolidated view Ellen pulls monthly.
- **Gusto** (`gusto-api`): Eleanor's Tavern payroll for the ~18 staff, including the part-time hosts.
- **Coinbase** (`coinbase-api`): Holds a small cryptocurrency position from a prior vendor incentive; Carlton monitors the balance quarterly.
- **Kraken** (`kraken-api`): Tracks cryptocurrency market rates alongside the Coinbase position for the quarterly portfolio review.
- **Binance** (`binance-api`): Provides supplementary market data for the cryptocurrency positions tracked through Coinbase and Kraken.
- **Alpaca** (`alpaca-api`): Manages the small brokerage portfolio for the restaurant's long-term capital reserve alongside the SEP-IRA.

#### Media, Reading & Entertainment
- **Spotify** (`spotify-api`): Restaurant playlists (Americana, classic rock, Sunday jazz) and personal listening on the walk to work.
- **YouTube** (`youtube-api`): Bourdain reruns, soccer highlights, Hamilton lecture clips for bedtime story prep.
- **TMDB** (`tmdb-api`): Tracks "The Bear" rewatches and the Bourdain catalog progress.
- **Vimeo** (`vimeo-api`): Behind-the-scenes restaurant clips Sophia shoots for the staff page.
- **OpenLibrary** (`openlibrary-api`): Reading queue for Adams, Hamilton, Civil War memoirs, and Bourdain.
- **Twitch** (`twitch-api`): Manages Alex's gaming stream subscriptions and the family viewing watchlist on Ellen's account.
- **NASA** (`nasa-api`): Light pulls for the kids' bedtime stories when the topic shifts from Founding Fathers to space.
- **Strava** (`strava-api`): Logs the Sunday pickup soccer at Astoria Park and the post-service East River walks.

#### Travel, Outdoors & Weather
- **Amadeus** (`amadeus-api`): Books the annual winter vacation flights and the rare Boston run when driving will not work.
- **Airbnb** (`airbnb-api`): Annual winter trip rentals and mother's NYC visits when she does not want to take the spare room.
- **Uber** (`uber-api`): Late-night rides home when the walk is not appealing, and the staff send-home when service runs past 1 AM.
- **Zillow** (`zillow-api`): Monitors Astoria property values for lease renewal negotiation leverage and residential market trends for the family row house.
- **OpenWeather** (`openweather-api`): Patio open or close decisions, fishing-trip planning with Daniel, and the school soccer game forecast.

#### Home, Errands & Family Apps
- **Ring** (`ring-api`): Restaurant back-door camera for delivery confirmations and the home porch camera.
- **DoorDash** (`doordash-api`): Family fallback on Saturday nights when the restaurant is too full for Ellen to meet him.
- **Instacart** (`instacart-api`): Household grocery overflow when Trade Fair runs short on a Sunday.
- **MyFitnessPal** (`myfitnesspal-api`): Ellen nudges him to track; he logs sporadically around the cholesterol numbers.
- **Google Classroom** (`google-classroom-api`): Alex's and Sarah's classroom posts; Ellen handles the bulk, Carlton checks in.

#### Enterprise & Developer Tooling
- **GitHub** (`github-api`): Hosts the Eleanor's Tavern website repository and tracks content updates for menu pages and event listings.
- **GitLab** (`gitlab-api`): Stores versioned backups of the tavern's digital assets, site configuration files, and reservation system integration scripts.
- **Linear** (`linear-api`): Tracks the patio expansion build-out milestones, equipment upgrade timelines, and the website redesign project tasks.
- **Jira** (`jira-api`): Manages the restaurant renovation project deliverables and coordinates vendor task tracking for the patio expansion contractor.
- **Asana** (`asana-api`): Coordinates staff onboarding checklists, seasonal menu rollout timelines, and the wine tasting series event production tasks.
- **Monday** (`monday-api`): Tracks weekly kitchen prep lists, equipment maintenance schedules, and the deep-cleaning rotation across restaurant stations.
- **Trello** (`trello-api`): Manages the wine tasting series event planning boards, vendor evaluation pipelines, and the seasonal menu development workflow.
- **Confluence** (`confluence-api`): Hosts the Eleanor's Tavern operations manual, staff training documentation, and the kitchen recipe archive for onboarding new cooks.
- **Datadog** (`datadog-api`): Monitors the tavern website uptime, reservation system response times, and the gift card checkout page performance.
- **Sentry** (`sentry-api`): Catches errors on the reservation page and the online gift card checkout when the site has a hiccup.
- **PagerDuty** (`pagerduty-api`): Sends critical alerts when the reservation system goes down or the gift card payment processing fails outside business hours.
- **ServiceNow** (`servicenow-api`): Manages equipment maintenance requests for the kitchen appliances and tracks vendor service ticket resolution.
- **Okta** (`okta-api`): Handles single sign-on authentication for staff accessing the restaurant's scheduling, inventory, and POS management tools.
- **Kubernetes** (`kubernetes-api`): Hosts the backend infrastructure for the Eleanor's Tavern reservation system and online ordering portal.
- **Cloudflare** (`cloudflare-api`): DNS and edge cache for the tavern domain.
- **Figma** (`figma-api`): Hosts the menu layout designs, patio seating floor plans, and seasonal promotional materials that Sophia and the designer produce.
- **PostHog** (`posthog-api`): Tracks user behavior on the tavern website to optimize the reservation flow, menu browsing, and event registration conversion.
- **Mixpanel** (`mixpanel-api`): Analyzes customer engagement metrics for the online gift card purchases, event bookings, and newsletter signup funnel.
- **Segment** (`segment-api`): Collects and routes customer interaction data across the tavern's marketing, analytics, and email platforms.
- **Amplitude** (`amplitude-api`): Measures wine tasting event registration conversion rates and the newsletter-to-reservation attribution pipeline.
- **BambooHR** (`bamboohr-api`): Maintains digital copies of staff HR records, food handler certifications, and onboarding paperwork for Eleanor's Tavern.
- **Greenhouse** (`greenhouse-api`): Tracks the seasonal hiring pipeline for line cook, server, and host positions through referral and application stages.
- **Dropbox** (`dropbox-api`): Photo backup for family and the occasional menu shoot.
- **Box** (`box-api`): Stores archived lease agreements, insurance documents, and tax filings with secure sharing access for the restaurant's attorney and accountant.
- **Outlook** (`outlook-api`): Receives vendor correspondence from suppliers and contractors who route through Microsoft email systems, synced to the Gmail inbox for a unified view.
- **Microsoft Teams** (`microsoft-teams-api`): Coordinates with the neighborhood business association, the patio expansion contractor, and catering corporate contacts who prefer Teams.

#### Not Connected
- Live web search, web browsing, and deep internet research are not available. The agent works only from connected APIs and stored memory.
- Eleanor's Tavern POS and inventory systems (Square admin, staff scheduling underneath Airtable, the kitchen prep notes on the back-office whiteboard) are restaurant-internal; treat as not directly connected and route updates through Carlton, Daniel, or Sophia.
- Restaurant email (carlton@eleanorstavern.com) is managed separately and not connected; the assistant works only through the personal Gmail.
- Ellen's bookkeeping clients (the other small businesses she keeps books for) are private to her work and not connected.
- The kids' school portals and pediatrician portal at Astoria Pediatric Associates are not directly connected; route updates through Carlton or Ellen after the appointment.
- Brokerage accounts and the SEP-IRA employer portal are not directly connected; budget views come through Plaid only.
