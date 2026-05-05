# CardForensics

Client-side smart card APDU trace forensic analyzer. Drop a macOS CryptoTokenKit log file and get a full security audit with zero data leaving your machine.

<p>
<img src="docs/assets/screenshot-landing.png" width="49%" alt="Landing page with Matrix APDU rain" />
<img src="docs/assets/screenshot-analysis.png" width="49%" alt="Analyzing a YubiKey PIV trace" />
</p>

## Features

- **Card identification** via ATR database (~5,100 cards including ~200 wildcard patterns), AID database (44 known applications), CLA/tag heuristics, and ATR regex pattern matching
- **Token identity extraction** aggregates serial number, firmware version, vendor, and CHUID fields (FASC-N, GUID, expiration) across all exchanges. Supports YubiKey and SafeNet eToken/Fusion hardware
- **ATR structural parsing** per ISO 7816-3: convention, protocols, historical bytes, TCK validation
- **Application identification** for EMV (Visa, Mastercard, Amex, JCB, Discover), OpenPGP, FIDO U2F/FIDO2, European eIDs (Belgian, German, Estonian, Spanish, Italian), GlobalPlatform, and health cards
- **Protocol reconstruction** with session boundaries, auth state machine tracking, and 61xx chaining
- **PIV analysis** covering 35 named data objects, 25 key references, 12 algorithm IDs (including ML-DSA-65), and certificate slot provisioning checks
- **SafeNet vendor decoding** for CLA=0x82 hardware serial retrieval, DF30 applet version, FF F3 key container mapping, and FF90 key template inventory
- **EMV tag dictionary** with ~50 TLV tags and value interpreters (PAN masking, CVM rules, cryptogram types, transaction counters)
- **Certificate viewer** with X.509 parsing via [Peculiar Ventures certificate viewer](https://github.com/PeculiarVentures/x509)
- **Default key detection** via PIV GEN AUTH (AES-ECB, both witness and challenge tags) and GP SCP03 (session key derivation) brute-force against 10 known management keys
- **Threat analysis** covering credential exposure, nonce replay, timing side-channels, bulk erasure patterns, orphaned keys, and ACL bypass
- **Security scoring** with threat-aware deductions (default keys -40, credential exposure -30, per-warning -5), provisioning-aware confidence gating, and letter-grade output (A-F)
- **AI analysis** with optional per-exchange and session-level LLM analysis (requires your API key)
- **Forensic export** as deterministic JSON evidence package (schema v2.4) with token identity, ATR parse, AID resolution, and database coverage metadata

Everything runs in the browser. No data leaves your machine (unless AI is enabled with your API key).

## Live

[peculiarventures.github.io/cardforensics](https://peculiarventures.github.io/cardforensics/)

## Claude Skill

CardForensics includes a Claude skill for offline trace analysis. Upload a CryptoTokenKit log and Claude runs the full analysis pipeline, adds AI commentary, and renders an interactive React dashboard — no API key needed for the AI summaries.

### Install

Add the skill to your Claude project's user skills:

```bash
# Clone the repo (skill is at skill/)
git clone https://github.com/PeculiarVentures/cardforensics.git
cd cardforensics && npm install
```

For **Claude.ai Projects**, add the `skill/` directory as a user skill in your project settings. For **Claude Code**, reference the skill path in your CLAUDE.md or let Claude discover it in the repo.

The skill triggers automatically when you upload a `.log` file and mention APDU analysis, smart card forensics, PIV provisioning, CardForensics, or related terms.

### Usage

1. Upload a CryptoTokenKit `.log` file to Claude
2. Ask Claude to analyze it (e.g., "analyze this smart card trace", "what's wrong with this PIV provisioning?", "run CardForensics on this")
3. Claude produces an interactive React dashboard artifact with:
   - Letter grade (A–F) with score breakdown
   - Executive summary and per-session AI narratives
   - Threat findings with severity filters and spec reference badges
   - Collapsible session blocks with operation badges
   - Annotated hex with TLV-colored segments and hover tooltips
   - Embedded X.509 certificate viewer (vendored [@peculiar/certificates-viewer](https://github.com/PeculiarVentures/pv-certificates-viewer))
   - Keyboard navigation (arrow keys, j/k, space for play/pause)
   - Object ledger, compliance profile, and token identity panel

You can also do ATR-only lookups: "What card has ATR 3BFD1300008131FE158073C021C057597562694B657940?"

### How It Works

The skill runs a three-step pipeline:

```
skill/
  SKILL.md              # Skill definition, triggers, and presentation guidance
  scripts/
    analyze.js          # Full pipeline: parse → annotate → threats → score → export JSON
    render.js           # JSON → React JSX dashboard renderer
  vendor/
    pv-cert-viewer.*    # Vendored certificate viewer (base64 + minified JS)
```

```bash
# Step 1: Analyze (produces JSON)
npx vite-node skill/scripts/analyze.js trace.log --verbose > analysis.json

# Step 2: Claude enriches JSON with AI summaries and per-exchange explanations

# Step 3: Render dashboard
cat enriched.json | npx vite-node skill/scripts/render.js --output dashboard.jsx
```


## Supported Card Families

| Vendor | Card identification | Token identity | Vendor APDU decoding |
|--------|-------------------|----------------|---------------------|
| Yubico (YubiKey 5) | ATR + AID + version probe | Version, GUID | Standard PIV |
| Thales SafeNet eToken 5110 | CLA heuristics + FF F3 containers | Serial, version, CHUID | CLA=0x82 serial, DF30 version, FF F3/FF90 containers |
| Thales SafeNet Fusion | CLA heuristics + FF F3 containers | Serial, version, CHUID | CLA=0x82 serial, DF30 version, FF F3/FF90 containers |
| Generic PIV | AID selection | CHUID if populated | Standard PIV |
| EMV (Visa/MC/Amex) | AID + ATR | N/A | EMV TLV decoding |
| OpenPGP | AID | N/A | Standard |
| FIDO U2F/FIDO2 | AID | N/A | Standard |

## Development

```bash
npm install
npm run dev
```

## Test

```bash
npm test                 # regression suite (3 traces, 803 exchanges)
npm run test:update      # regenerate snapshots after intentional changes
```

The test suite covers SafeNet eToken, SafeNet Fusion, and YubiKey PIV traces with snapshot diffing for card ID, token metadata, threats, annotations, and export schema.

## Build

```bash
npm run build
# Output: dist/index.html (single-file, ~1,370KB)
# Copy to docs/ for GitHub Pages:
cp dist/index.html docs/index.html
```

## License

MIT © [Peculiar Ventures](https://peculiarventures.com)
