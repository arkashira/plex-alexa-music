# partner-targets.md

> Partner integration roadmap for **plex-alexa-music**. Ordered by ship priority. Effort: S = <1 wk, M = 1–3 wks, L = 1 mo+. Revenue tier flagged with 💰.

## Priority matrix (TL;DR)

| # | Partner | Effort | Rev-share | User job solved | Ship phase |
|---|---------|--------|-----------|-----------------|------------|
| 1 | Alexa Skills Kit + Login with Amazon | M | — (required) | "Talk to my library" | P0 (MVP) |
| 2 | Plex API (incl. Plex Pass) | M | 💰 referral | Connect the library | P0 (MVP) |
| 3 | Tailscale | S | 💰 partner | Reach my server safely | P0 (MVP) |
| 4 | Emby + Jellyfin API | M | — | Serve non-Plex self-hosters | P1 |
| 5 | Last.fm API | S | — | Scrobble + "play more like this" | P1 |
| 6 | Cloudflare Tunnel | S | — | Free remote-access fallback | P1 |
| 7 | Stripe / Lemon Squeezy | S | 💰 (own MRR) | Pay for the skill | P1 |
| 8 | Sonos Control API | L | — | Multi-room whole-home audio | P2 |

---

## P0 — Must ship with MVP

### 1. Amazon Alexa Skills Kit (ASK) + Login with Amazon
- **Why:** Non-negotiable. ASK is the runtime; Login with Amazon (LWA) does OAuth account-linking between the Alexa user and their self-hosted server.
- **Free-tier limits:** Free to publish. AWS Lambda free tier covers the backend: 1M requests + 400K GB-sec/mo — comfortably enough for ~50K skill invocations/day at zero infra cost.
- **Effort: M.** Intent schema (PlayArtist, PlayAlbum, PlayPlaylist, QueueControl), AudioPlayer interface for streaming, account-linking flow. AudioPlayer directives + buffering edge cases are the real time sink.
- **Value-add:** The entire product. "Alexa, play [artist] from my library."
- **Rev-share:** None directly, but Alexa device sales qualify for **Amazon Associates** (1–3% on Echo hardware) — embed a "works best on Echo" link in the skill listing + onboarding.

### 2. Plex API (+ Plex Pass referral)
- **Why:** Plex is the larger half of the target market. Use the official Plex API (`/library/sections`, `/playlists`, transcode/`/music/...` endpoints) + Plex.tv OAuth PIN flow for auth.
- **Free-tier limits:** Plex API is free. **Plex Pass** ($6.99/mo, $119.99 lifetime) unlocks better transcoding/sonic analysis — relevant for on-the-fly audio transcode to Alexa-compatible formats (MP3/AAC).
- **Effort: M.** OAuth PIN flow, library enumeration, fuzzy title/artist matching, transcode session management, direct-play vs transcode decisioning.
- **Value-add:** Connect-the-library — the core job for ~60% of TAM.
- **Rev-share: 💰** No formal affiliate program, but lifetime-Plex-Pass referral and a "recommended setup" guide can be monetized via content/affiliate adjacencies. Track as soft revenue.

### 3. Tailscale
- **Why:** The #1 hidden blocker — Alexa's cloud backend must reach a server sitting behind the user's home NAT/firewall. Tailscale gives a zero-config WireGuard mesh so the Lambda/backend can hit `http://plex.tailnet:32400` without port-forwarding or exposing the server publicly. This is your differentiator vs. half-baked competitors that demand sketchy port-forwarding.
- **Free-tier limits:** Free plan = 100 devices / 3 users — covers essentially every self-hoster. No cost to the user.
- **Effort: S.** Document the funnel/auth-key flow; optionally script an ephemeral auth-key onboarding.
- **Value-add:** "Reach my server safely" — removes the scariest setup step, biggest activation lever.
- **Rev-share: 💰** Tailscale runs a **partner/referral program**; pursue co-marketing + referral once volume is proven. Strong narrative fit ("self-hosted, secure-by-default").

---

## P1 — Fast follow (weeks 2–6)

### 4. Emby + Jellyfin API
- **Why:** Capture the non-Plex self-hosters explicitly named in the hypothesis. Emby and Jellyfin share a near-identical REST API (Jellyfin forked Emby), so one adapter ≈ covers both.
- **Free-tier limits:** Jellyfin fully free/OSS. Emby Premiere $4.99/mo (some features gated, but base API is free).
- **Effort: M.** New backend adapter behind a `MediaServer` interface; API key/user auth, item search, audio stream URLs. ~60% code reuse from Plex adapter if abstracted well.
- **Value-add:** Expands SAM by ~30–40% (the Emby/Jellyfin self-host segment) with marginal effort.
- **Rev-share:** None.

### 5. Last.fm API
- **Why:** Two jobs at once — scrobbling (table-stakes for music nerds) and similarity data ("play more like this", radio/discovery) that your local library metadata lacks.
- **Free-tier limits:** Free, non-commercial. ~5 req/sec courtesy limit; commercial use technically needs a paid license — budget for a commercial agreement at scale.
- **Effort: S.** `track.scrobble`, `track.updateNowPlaying`, `track.getSimilar`. OAuth web-auth flow per user.
- **Value-add:** Retention + discovery — turns a remote-control skill into a music *experience*.
- **Rev-share:** None.

### 6. Cloudflare Tunnel
- **Why:** Free alternative to Tailscale for users who prefer a public hostname or already run Cloudflare. Offer both so connectivity is never the reason a trial fails.
- **Free-tier limits:** Free tunnels, unlimited (subject to Cloudflare TOS on media streaming — flag this; heavy transcode streaming may bump policy limits).
- **Effort: S.** Documentation + config template; backend already speaks HTTP to a hostname.
- **Value-add:** Connectivity fallback — widens activation funnel.
- **Rev-share:** None.

### 7. Stripe / Lemon Squeezy
- **Why:** Monetize. Skill itself is free to list, so charge via external account-linking unlock (freemium: 1 server / basic playback free; multi-server, voice playlists, scrobbling = paid).
- **Free-tier limits:** Stripe — no monthly fee, 2.9% + 30¢/txn. **Lemon Squeezy** acts as merchant-of-record (handles global VAT/sales tax) at ~5% + 50¢ — worth it for a solo/indie founder avoiding tax compliance overhead.
- **Effort: S.** Checkout link + webhook → entitlement flag on the linked account.
- **Value-add:** "Pay for the thing" — and Lemon Squeezy removes tax-compliance burden.
- **Rev-share: 💰** This *is* the MRR engine. Target $4–5/mo or $39 lifetime; at 2K paying users that's ~$8–10K MRR.

---

## P2 — Later / opportunistic

### 8. Sonos Control API
- **Why:** Multi-room whole-home audio is the most-requested power-user upgrade. Let "Alexa" trigger playback from the Plex/Emby library onto Sonos groups.
- **Free-tier limits:** Free API; requires Sonos developer registration + integration review/cert.
- **Effort: L.** Separate control plane, group management, OAuth, and Sonos's certification process. Real lift.
- **Value-add:** Whole-home audio — premium tier justification, expands willingness-to-pay ceiling.
- **Rev-share:** None directly; gate behind the paid tier.

---

## Strategic notes
- **Connectivity is the moat, not voice.** Items #3 and #6 (Tailscale/Cloudflare) solve the activation killer competitors ignore. Lead onboarding with them.
- **Revenue path:** real MRR comes from #7 (Stripe/Lemon Squeezy). Affiliate dollars (#1 Associates, #3 Tailscale partner) are bonus, not the model — pursue once you clear ~1K MAU to have leverage in partner conversations.
- **Build order rationale:** one `MediaServer` abstraction (#2 Plex → #4 Emby/Jellyfin) lets you triple addressable market with ~one extra adapter. Prioritize that interface design in week 1.