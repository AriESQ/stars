# KiCad PCB skills for Claude Code

Skills and command-line tools for developing, reviewing and sourcing KiCad (9/10) printed circuit boards with Claude
Code, aimed at hobby and small-batch boards made at JLCPCB/LCSC. They cover the path from an idea to an order: planning
the board, making scripted edits that are verified with KiCad's own tools, reviewing the design with measured evidence,
designing power supplies, and choosing and sourcing parts.

| Skill | Use it for |
|---|---|
| [`kicad-new-board`](skills/kicad-new-board/SKILL.md) | Starting a new hobby board: a short interview from purpose to parts (environment, blocks and interfaces, power budget, physical limits, JLCPCB manufacturing, 2 vs 4 layer stackup) that produces a requirements/architecture document the other skills build on |
| [`kicad-pcb-workflow`](skills/kicad-pcb-workflow/SKILL.md) | Creating and changing designs safely: a new schematic and board generated from scratch, scripted edits to `.kicad_sch` / `.kicad_pcb` in a scratch copy, staged layout from written briefs checked against datasheet layouts, routing as data, verification with KiCad's own DRC/ERC/parity plus the checks they miss, rendering and looking, diffing against the last commit, copying back |
| [`kicad-board-review`](skills/kicad-board-review/SKILL.md) | Engineering review: power and protection, copper capacity and heat, ground and return paths, regulators, SI/EMC, ESD, datasheet compliance, sourcing, mechanical - backed by a measured analysis pack and an adversarial reviewer |
| [`pcb-power-supply`](skills/pcb-power-supply/SKILL.md) | Designing a rail: LDO vs buck/boost/buck-boost, choosing the IC (optionally with TI WEBENCH in the browser), sizing the inductor, capacitors and dividers, input protection, layout and verification |
| [`pcb-battery-power`](skills/pcb-battery-power/SKILL.md) | Battery-powered boards: choosing the chemistry and cell, charger ICs and USB-C charging, NTC/JEITA, cell protection, power path, regulation from a cell, fuel gauges, sleep-current and battery-life estimates, layout, safety, shipping and bench tests |
| [`pcb-part-selection`](skills/pcb-part-selection/SKILL.md) | Choosing parts, reading datasheets, deriving values, importing from LCSC, and sweeping the BOM for stock before an order |

## Install

As a Claude Code plugin:

```
/plugin marketplace add jvanderberg/kicad-skills
/plugin install kicad-skills@kicad-skills
```

Or copy any folder under `skills/` into `~/.claude/skills/` (each skill is self-contained).

## Tools

All tools also work without Claude.

| Tool | What it does |
|---|---|
| `kicad-pcb-workflow/scripts/preflight.py` | Every tool the scripts need (KiCad and its python, the analysis venv, poppler, rsvg, jlcimport), with install hints; with `--project`, the pinned kicad-skills revision |
| `kicad-pcb-workflow/scripts/skills_rev.py` | Pin the kicad-skills commit (or, for a plugin install, its version and a hash of its files) and KiCad version a project builds with (`kicad-skills.lock`) and check it on every build; `assets/kskills.py` is the project-side template |
| `kicad-pcb-workflow/scripts/projfiles.py` | One convention for finding a project's own inputs (pin decisions, DRC and field exemptions, review config, reference parts, lock), used by every wrapper |
| `kicad-pcb-workflow/scripts/check.sh` | DRC (zone refill x2, schematic parity) + ERC on a copy of the project, summarised and diffed against a baseline, known items exempted only by name (`--accept`); runs `board_lint.py`, `nc_audit.py` and `partfields.py`, with the project's own notes and exemptions |
| `kicad-pcb-workflow/scripts/netspec.py` | Intended netlist vs KiCad's netlist: SPLIT / SHORT / MISSING / UNEXPECTED |
| `kicad-pcb-workflow/scripts/schgen.py`, `symgen.py` | Generate a readable wire-drawn KiCad 10 schematic and redrawn symbols from python (stacked pins written as KiCad's libraries do: copies hidden and passive, never a hidden power input); collision check; locate shorts |
| `kicad-pcb-workflow/scripts/new_board.py` | New board from the schematic netlist (footprints, symbol links, pad nets, fields, DNP / not-in-BOM / not-in-position-file attributes, outline, placement, labels per part or per pad with size and side, free silk texts) - KiCad has no CLI for this |
| `kicad-pcb-workflow/scripts/board_setup.py` | JLC stackup block, design rules and net classes (pcbnew cannot set a stackup); net-class assignments and patterns replaced by a run that gives `--assign` / `--pattern` (`--keep-assignments` adds), untouched by one that gives neither, and checked against the board's nets |
| `kicad-pcb-workflow/scripts/router.py` | Routing as data: tracks, vias, zones, keepouts by pad name, checked for clearance (exact: never looser than DRC), hole-to-hole (any net), vias on same-net pads and board edge before writing |
| `kicad-pcb-workflow/scripts/board_lint.py` | What DRC misses: silk outlines of footprints without courtyards overlapping (the outline is the placement boundary), missing 3D model files, silk text on part bodies, vias on pads of their own net, paste apertures over drilled holes (with exposed-pad paste coverage), other-net copper under mounting hardware on either side |
| `kicad-pcb-workflow/scripts/nc_audit.py` | Every unused pin, every pin the symbol types no_connect, and every input strapped to a rail, as a decision table with datasheet notes and the pin-table row |
| `kicad-pcb-workflow/scripts/partfields.py` | Every BOM part has a datasheet link and an LCSC/MPN in schematic and board, and every field matches between them (fails the build otherwise); `--online` checks the links |
| `kicad-pcb-workflow/scripts/refparts.py` | Each IC's datasheet typical application (parts, values, distance from the pin) against the design: names the part that satisfies each entry, or MISSING / WRONG VALUE / FAR |
| `kicad-pcb-workflow/scripts/fpcheck.py`, `add_courtyard.py`, `paste_clear.py` | Footprint vs package string and symbol (pad count, body size, numbering; `--pads` gives a custom pad's real copper size); add missing courtyards; derive a thermal-via footprint whose paste windows clear every drill (optionally with 0.3 mm drills, JLC's free size on 2 layers) |
| `kicad-pcb-workflow/scripts/strip_outline.py` | Same-named footprint copy without its silk outline, pin-1 and polarity marks kept, for a part placed tighter than its outline on purpose |
| `kicad-pcb-workflow/scripts/board_diff.py` | Everything that changed between two board (or schematic) versions or vs a git revision, every attribute (fields, pad nets, DNP, models, settings) as well as geometry, with anything outside the expected areas flagged |
| `kicad-pcb-workflow/scripts/kicad_sexpr/` | The file-format layer: lossless read/write of every KiCad s-expression file in KiCad's own formatting, plus builders for schematics (symbols, wires, labels, sheets), boards (footprints, tracks, vias, zones, keepouts, stackup) and project net classes, with stable uuids (regeneration is byte-identical). Generators and edits use it instead of formatting text; the writers above are built on it |
| `kicad-pcb-workflow/scripts/sexp.py` | Check s-expression files (balance, raw newlines in strings, duplicate uuids); list/get footprints and symbols |
| `kicad-pcb-workflow/scripts/render.py` | Render a window of chosen layers by KiCad coordinates to PNG (or a 3D render); also boards without an outline (imported reference layouts) |
| `kicad-pcb-workflow/scripts/kicad_open.sh`, `kicad_locks.py` | Is KiCad holding the project open? A running editor holding the folder, not a lock file (kicad-cli leaves stale ones; `--clean` removes them); every kicad-cli caller removes the locks it caused |
| `kicad-pcb-workflow/scripts/interp.py` | Which python has pcbnew and which has the analysis packages; scripts started with the wrong one re-run themselves under the right one; `interp.py run` gives an ad hoc script both |
| `kicad-board-review/scripts/make_pack.sh` | Build the analysis pack: netlist digest, board overview, DC power runs, planes, EMC, heat, DRC; each report starts with its coverage and warnings |
| `kicad-board-review/scripts/topology.py` | Ground nets, switch nodes, switching ICs and hot-loop candidates derived from the netlist's structure (not net names); writes a starter review config for the board |
| `kicad-board-review/scripts/power.py` | Resistive-grid DC solver: drop per load, copper loss, current density hotspots, current per via; a run whose net or pads are gone is reported NOT RUN with the reason |
| `kicad-board-review/scripts/planes.py`, `emc.py` | Ground plane pieces, slots (each with its own size; other nets' pours reported as pours) and stitching; reference continuity ranked by severity, crosstalk, layer changes, hot loops with a DC solve of each return path, Z0, differential pairs (Zdiff estimate, gap to the nearest pour) |
| `kicad-board-review/scripts/thermal.py`, `heat.py`, `thermal_model.py` | Heat-source table per part per corner (every candidate listed, unknown losses as UNKNOWN); steady-state layered thermal solve on the board's copper at a low / nominal / high film coefficient, next to the board-average check; junction estimates; thermal vias per exposed pad; pours under hot parts; ground stitching for heat, with a stitching what-if |
| `kicad-board-review/scripts/islands.py` | Same-net isolation on the filled copper: each declared island (single-point or quiet ground, local pour) one piece, no other pad of its net, joins as allowed |
| `kicad-board-review/scripts/decoupling.py` | Per IC supply pin, the nearest capacitor by copper path (tracks, vias, planes, joined as KiCad's own connectivity joins them) with a microstrip-based inductance estimate |
| `kicad-board-review/scripts/pour_check.py` | The quick check after a zone or placement edit: every pour piece has 2 vias to its plane, no track over a void (whole board or a window), on a refilled copy |
| `kicad-board-review/scripts/region.py`, `view.py` | List or render the copper inside a box |
| `pcb-part-selection/scripts/sourcing.py` | The project's sourcing context (assembler, LCSC warehouse region, quantity, stock policy) in one `sourcing.json`, and searches / stock checks that always name the region (exact part number ranked first, cross-references and JLCPCB placeholder parts called out); no default region |
| `pcb-part-selection/scripts/bom_check.py` | Stock (in the assembler's region), stock policy, package size, assembly class, datasheet links, ICs with no datasheet saved in the project, stale derived values, and one LCSC number split over several BOM lines, for the whole BOM via JLCImport |
| `pcb-part-selection/scripts/part_gate.py` | Lifecycle (TI product pages, order codes resolved to the device page including fixed-voltage codes and SN74/SN65/TXS/TXB/OPA families) and LCSC stock in the project's region per exact orderable variant or C-number, for candidate parts or for part numbers found in pasted text (e.g. WEBENCH's table view) |
| `pcb-part-selection/scripts/derived_check.py` | Each derived value (trip current, divider, snubber, thermal estimate) with the part parameters it came from: what depends on a part before a swap, and which values went stale after one |
| `pcb-part-selection/scripts/datasheet.py` | Fetch a datasheet only if it is really a PDF (a distributor viewer page is followed to its PDF; a bot-protection refusal says so, with the next step); find the pages holding a section or figure; render a page and record what it shows in the folder's INDEX.md |
| `pcb-power-supply/scripts/path_budget.py` | Operating point of a power path with the source's and the path's resistance at every corner, plus transients, against every element's limit (latching trips first); the path's own loss next to the converters', and --json for the review's heat table |

## Requirements

- KiCad 9 or 10 (`kicad-cli`, and KiCad's bundled python with `pcbnew` for `boarddump.py`). Paths are auto-detected on
  macOS, Linux and Windows; override with `KICAD_CLI` and `KICAD_PYTHON`.
- Python 3 with numpy, scipy, shapely >= 2 and matplotlib for the analysis scripts. `kicad_env.sh` creates a venv in
  `~/.cache/kicad-skills/venv` on first use (override with `PY`).
- `rsvg-convert` (librsvg) for `render.py`; poppler (`pdftotext`, `pdftoppm`, `pdfinfo`) for `datasheet.py`.
- [JLCImport](https://github.com/jvanderberg/kicad_jlcimport) (`jlcimport-cli`) for part search, import and stock checks:
  `pipx install git+https://github.com/jvanderberg/kicad_jlcimport` (checked October 2026). The scripts use
  `search --region`, which needs v1.6.0 or later; `jlcimport-cli search --help` shows whether you have it. They always
  pass the region from the project's `sourcing.json`: without `--region`, jlcimport-cli uses the region its KiCad
  plugin last saved, which may not be the warehouse your assembler buys from. The order files and placement check use
  `jlcimport-cli production`, in JLCImport v1.7.0 and later (`preflight.py` reports an older build, including a
  pre-v1.7.0 build of main that has `production` but splits one part over BOM lines); its stock check reads JLCPCB's international library only.

Run `skills/kicad-pcb-workflow/scripts/preflight.py` to check all of these at once.

## Limits

The analysis is DC and geometric: no field solving, no thermal model, components are not in the copper model. The
skills say so in their reports, and they keep design checks separate from hardware qualification.

## License

MIT - see [LICENSE](LICENSE).
