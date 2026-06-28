```markdown
# tech-spec.md — plex-alexa-music (v1)

## Stack

| Layer | Choice | Why |
|---|---|---|
| Skill runtime | **Node.js 20.x** + `ask-sdk-core` v2.14 | Lowest-latency cold starts on Lambda vs. Python for the AudioPlayer request/response loop; first-class ASK SDK support. |
| Skill type | **Alexa Custom Skill** + `AudioPlayer` + `PlaybackController` interfaces | The native "Music Skill API" (CloudPlayer/MSP) is invite-gated by Amazon and requires a content-catalog ingest pipeline we don't have. Custom Skill + AudioPlayer ships in weeks, not quarters, and streams arbitrary HTTPS URLs. |
| Media abstraction | Thin adapter layer `PlexClient` / `EmbyClient` behind a `MediaServer` interface | Plex (`/library/sections`, `/search`, transcode/`/music/:/transcode/universal`) and Emby (`/Items`, `/Audio/{id}/universal`) diverge enough to warrant separate adapters with one contract. |
| Transcode | Request **MP3 128–192 kbps** via server-side transcode endpoint | Alexa AudioPlayer only reliably plays MP3/AAC over HTTPS; FLAC/ALAC must be transcoded by Plex/Emby, not us. |
| Lang/build | TypeScript 5.x → esbuild bundle | Type-safe adapter contracts; esbuild keeps the Lambda zip < 3 MB for sub-400 ms warm invokes. |
| IaC | **AWS SAM** (`template.yaml`) | Single-command deploy of Lambda + DynamoDB + IAM; matches free-tier story below. |

## Hosting (free-tier-first)

| Component | Platform | Free-tier headroom |
|---|---|---|
| Skill endpoint | **AWS Lambda** (us-east-1, required region for Alexa skills) | 1M req/mo + 400k GB-s free forever. At 128 MB / 300 ms avg, ~10M invokes/mo stay free. |
| Token/config store | **DynamoDB on-demand** | 25 GB + 25 WCU/RCU free. Our row count = #users; trivial. |
| Account-linking OAuth proxy | **Cloudflare Workers** (free: 100k req/day) | Hosts the Plex PIN-flow → OAuth2 shim that Alexa account-linking requires (Plex has no native OAuth2 `/authorize`). |
| Logs/metrics | **CloudWatch** free tier (5 GB logs, 10 custom metrics) | Sufficient at launch. |
| Stream transport | **User's own Plex/Emby remote access** (Plex Relay or user reverse-proxy) | $0 to us — the self-hoster already owns the egress. We never proxy audio bytes (cost + bandwidth killer). |

**Hard rule:** audio bytes never traverse our infra. We return the user-server stream URL to Alexa; Alexa pulls directly. This keeps us inside Lambda free tier indefinitely.

## Data model (DynamoDB, single-table)

**Table `pam_users`** (PK = `alexaUserId`)

| Field | Type | Notes |
|---|---|---|
| `alexaUserId` (PK) | S | From `context.System.user.userId` |
| `serverType` | S | `plex` \| `emby` |
| `serverBaseUrl` | S | User's publicly reachable HTTPS base (e.g. `https://x.plex.direct:32400`) |
| `authToken` | S | Plex `X-Plex-Token` / Emby `X-Emby-Token` — **encrypted** (see Security) |
| `musicSectionId` | S | Plex library section key / Emby parent folder id |
| `clientId` | S | Stable per-install UUID sent to Plex/Emby |
| `tokenEncDataKey` | B | KMS-wrapped data key for envelope encryption |
| `createdAt` / `updatedAt` | N | epoch ms |

**Table `pam_playback`** (PK = `alexaUserId`) — transient queue state

| Field | Type | Notes |
|---|---|---|
| `alexaUserId` (PK) | S | |
| `queue` | L | Ordered list of `{token, streamUrl, title, artist, ratingKey, offsetMs}` |
| `index` | N | Current track pointer for Next/Previous |
| `ttl` | N | DynamoDB TTL, 24h — auto-evict stale queues |

## API surface

The skill's *external* surface is the single Alexa-invoked Lambda; "endpoints" below are (a) intents Alexa routes to us and (b) HTTP routes on the Cloudflare account-linking shim.

| # | Method / Path (or Intent) | Purpose |
|---|---|---|
| 1 | `POST /alexa` (Lambda URL) | Single entry; dispatches all Alexa request envelopes (Launch, Intent, AudioPlayer, SessionEnded). |
| 2 | `Intent PlayArtist` (slot `{artist}`) | Resolve artist → enqueue tracks → return `AudioPlayer.Play`. |
| 3 | `Intent PlayAlbum` (slots `{album}`,`{artist?}`) | Resolve album → enqueue ordered tracks. |
| 4 | `Intent PlayPlaylist` (slot `{playlist}`) | Map spoken name to Plex/Emby playlist → enqueue. |
| 5 | `Intent PlaySong` (slots `{song}`,`{artist?}`) | Single-track search → play. |
| 6 | `AudioPlayer.PlaybackNearlyFinished` | Pre-fetch next stream URL for gapless continuation. |
| 7 | `AudioPlayer.PlaybackFailed` | Re-transcode at lower bitrate / surface spoken error. |
| 8 | `GET /link/start` (CF Worker) | Begin Plex PIN flow; redirect user to `plex.tv/link`. |
| 9 | `GET /link/callback` (CF Worker) | Poll PIN → exchange for token → mint OAuth2 `code` for Alexa account-linking. |
| 10 | `POST /token` (CF Worker) | Alexa OAuth2 token endpoint; returns access/refresh tied to `alexaUserId`. |

## Security model

- **Auth (account linking):** Alexa OAuth2 Authorization Code flow → Cloudflare Worker shim. Plex uses its PIN/`plex.tv` flow (no OAuth2), so the Worker bridges PIN → OAuth2 code. Emby uses username/password → token exchanged server-side. The resulting media-server token is the credential we persist.
- **Secrets at rest:** media-server tokens stored with **envelope encryption** — AWS KMS CMK generates a per-user data key; token encrypted with AES-256-GCM; only the KMS-wrapped key lives in DynamoDB. Lambda decrypts on demand; tokens never logged.
- **Secrets in transit:** All hops HTTPS/TLS 1.2+. Reject any user-supplied `serverBaseUrl` that is not `https://` or resolves to RFC-1918 (prevents SSRF into our VPC; the URL must be the user's *public* endpoint).
- **IAM:** Lambda execution role scoped to: `dynamodb:GetItem/PutItem/UpdateItem` on the two tables only, `kms:Decrypt/GenerateDataKey` on the single CMK, `logs:*` on its own log group. No `*` resources.
- **Request verification:** Validate Alexa `signaturecertchainurl` + timestamp skew (< 150 s) on every invoke; reject replays. Validate `applicationId` matches our skill.
- **Tenant isolation:** Every DynamoDB access keyed by `alexaUserId` from the verified request — no cross-user reads possible.

## Observability

- **Logs:** Structured JSON (`pino`) to CloudWatch. Fields: `requestId`, `alexaUserId` (hashed SHA-256, never raw), `intent`, `serverType`, `latencyMs`, `resolveHits`. **Never** log tokens, stream URLs, or search terms at INFO.
- **Metrics (CloudWatch custom, 10 within free tier):** `IntentLatencyMs` (p50/p95), `SearchResolveFailures`, `PlaybackFailedCount`, `TranscodeFallbacks`, `AccountLinkSuccess/Failure`, `ColdStartCount`.
- **Traces:** AWS X-Ray on Lambda + downstream HTTP calls to Plex/Emby (segment per `MediaServer` adapter call) to localize whether latency is ours vs. the user's home server. Sampling 10%.
- **Alarms:** `PlaybackFailedCount` > 5% of plays (5-min window) and p95 `IntentLatencyMs` > 1500 ms → SNS to founder email.

## Build / CI

- **CI:** GitHub Actions. Pipeline: `npm ci` → `tsc --noEmit` → `eslint` → `vitest` (adapter unit tests against recorded Plex/Emby fixture responses) → `esbuild` bundle → `sam validate`.
- **Skill model:** Interaction model (`en-US.json`) linted via `ask-cli`; `ask deploy --target skill-metadata` on merge to `main`.
- **Deploy:** `sam build && sam deploy` (Lambda + tables + IAM) gated behind a manual `production` environment approval. CF Worker deploys via `wrangler deploy`.
- **Secrets in CI:** AWS creds + `ASK_*` tokens from GitHub OIDC → short-lived role assumption (no long-lived keys in repo).
- **Quality gates (block merge):** coverage ≥ 70% on adapter layer; zero `eslint` errors; `sam validate` pass.
```