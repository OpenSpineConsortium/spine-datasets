# The dataset records

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21; the records are copied from
SchwingNet's data/sources/<id>.json (the registry rendered by tools/sources.py, whose field rules
are src/schwingnet/sources.py), and the routes from docs/research/data-access-requirements.md. The
held sets, the status `held`, the standard counts, the pairing block and the census come from the
thread "Dataset census and roadmap", 2026-10-23 (issue #178).

One JSON file per dataset, the one place its facts are written, so that every count of the data is
made from these files and nobody passes over a dataset twice. They are, first, 81 of SchwingNet's
111 records, every one whose `reach` is `get` (public or by request, not yet fetched), `gated`
(behind an agreement, an application or a login) or `embargoed`; second, five records written from
docs/research/xray-dataset-requests.md section 15 for intraoperative sets the literature names
that had no registry record (levelcheck_jhu, vanderbilt_tha_fluoro, huashan_fudan,
pumch_stitching, nit_warangal_nims), each saying so in its `record` field; third, the sets the
owner already held on Wayne State's grid when the census began, written from the registry's
dataset facts with `reach` `held` and the status `held` (one record per release: the registry's
three COBRA2026 entries are cobra2026, its C-ArmLSpine sweeps are inside carmlspine, and its
CTSpine1K, CTPelvic1K and RibFrac entry is three records); and every record added since. Not here:
the one set that exists nowhere (cervical_thoracic_intraop), the three set aside (spinesac,
mendeley_5jdfdgp762, roboflow_vindr_relabels), and the synthetic films and renders already held,
for which no patient was imaged: the project's own renders, derived rather than obtained, and
Spinal-AI2024's synthetic films. Two collections the owner holds wait for his call before they get
records: the public fluoroscopy clips gathered from articles and sites, and the FluoroCap
literature panels. The anomaly harvest is a list of CT sources: its planned and gated members have
records of their own, and the releases of it already on the grid get theirs by issue #181. The
census (below) gives the count.

The fields, as SchwingNet's record has them, copied exactly (licence and link above all):

- `id`, `name`, `group` (fluoro, video, projections, films, ct, future), `what`, `level_truth`,
  `reach`, `licence`, `link`, `how_to_get` (the steps, as the registry gives them, naming
  SchwingNet's and the data platform's tools), `grid_path` (null until fetched), `counts`,
  `measured` (empty until a grid job fills it), `record` (where the record came from).
- `source_status`: SchwingNet's own `status` text as of 2026-10-21, kept so nothing is lost.

The fields this repository adds:

- `route`: how the set comes in: `letter`, `form`, `account`, `agreement`, `download` or
  `owner-only`.
- `status`: where the task stands: `todo`, `requested`, `granted`, `fetching` (a manifest is in,
  manifests/README.md, and the promoter fetches it after merge), `fetched` (the promoter's word
  alone: in the shared tree with its manifest), `held` (on the grid by the owner's own chain,
  not the promoter, so no manifest covers it: under the owner's data root, or copied into the
  shared tree by hand; `grid_path` says where), `refused` or `needs-owner`.
- `result`: free text, the dated result line README.md describes; empty until there is one.
- `history`: the steps taken so far, oldest first, each `{"date": "YYYY-MM-DD", "step": ...,
  "note": ...}` with the step one of `researched`, `asked`, `granted`, `fetching`, `fetched`,
  `held`, `refused`, `handed-back` or `note`, and the note one line saying what happened (the
  letter sent and to whom, the form submitted, the job id, the reason). A status other than
  `todo` needs at least one entry saying when, and `held` a `grid_path` too.
- `obstacles`: a list of one-line strings, what stands in the way right now (a DUA to sign, a
  bounce, a licence line still to confirm, a token only the owner holds); empty when nothing.
- `next`: one line, what whoever holds the task does next; empty when nothing is planned.
- `pairing`, only on a real X-ray set with the same subject's CT or CBCT, placed after `group`:
  `spine` (true, or false for a pair of something else, a femur, a phantom, a pig limb),
  `region`, `xray`, `ct`, `subjects`, `pose` (stored, shipped, or how it would be found), `masks`
  (what segmentation ships), `annotate` (what a reader would add), each one line of text, and
  `pair_key` (how each X-ray is matched to its CT: the case number, the patient, one specimen)
  and `priority` (a whole number, the order in which annotation takes the sets), both optional.

The counts the census adds up are read from `counts` under the standard keys `subjects`,
`xray_images` (a still image counted once), `videos` (a run, clip, recording or sweep counted
once), `run_frames` (the frames inside those videos and sweeps, counted apart from still images:
COBRA2026's 375,618 projections are 692 sweeps), `ct_volumes` and `bytes`, and, where a record has
none of these, under the names the records already use (`patients`, `films`, `frames`, `clips`,
`cts`, `size_gb` and the rest, read by the kind of set: in a video or projection set `frames`,
`projections` and `images` are frames inside runs, and in a CT set only the standard keys name
X-rays, tools/census.py); the size on the grid is `measured.bytes`, else the bytes of the
promoter's result line, else the record's own size. A record that gives a count under a standard
key gives a number there; anything the census cannot read is listed on the census page under what
the records still lack, to be written once, here.

The pipeline board (tools/pipeline.py; PIPELINE.md on the branch `pipeline`, and the interactive
pipeline.html on the docs site) is drawn from these fields and nothing else: the status and the
route put a record in its column, the history is the trail, the obstacles and the next step are
the card. `bash scripts/check.sh` runs `python3 tools/pipeline.py check`, which refuses a record
whose fields do not hold together. Inside every column the X-ray groups (fluoro, video,
projections, films) come before ct, and the fetch order follows the same rule: X-ray sets before
CT, the owner's order of 2026-10-21.

The census (tools/census.py; census.json, CENSUS.md and census.html on the branch `census`, and
census.html on the docs site) is folded from the same files: each run of the Census workflow
(.github/workflows/census.yml) reads the last census.json and derives a row again only for a
record that is new or whose content changed since, by the record's sha256, carrying every other
row as it was, and logs what moved with the date: a record added or removed, a status, a stage, a
count or a tier changed. A change to tools/census.py or tools/pipeline.py, the rules a row is
derived by, derives every row afresh on the next run, with one line in the log; each record keeps
the date the census first saw it, even if it is removed and written again, and the date its
content last changed. It shows the totals, the paired CT and X-ray breakout in tiers (A on the
grid, B open or granted, C asked or still to ask, D refused or embargoed, E pairs of something
other than the spine), every dataset with filters, what the records still lack and the log. A pair
moves from tier to tier by itself as its record's status moves. `bash scripts/check.sh` runs
`python3 tools/census.py check`, which refuses a pairing block, a standard count, a text field or
a `measured` that does not hold together, two records with one id, and a record whose id is not
its file's name.

A collaborator changes `status`, `result` and, after a fetch, `grid_path` and `measured`, and
replaces a "to confirm on the page" with what the page says; `licence` and `link` change only when
the page shows the record wrong, and the pull request says so. The path convention for a fetch is
/rs/rs_grp_oschome/shared/datasets/<id>/raw, written only by the promoter after a manifest's pull
request merges (grid/README.md, manifests/README.md); the registry's own paths under
/rs/rs_grp_oschome/go2432/data/<id>/raw in `how_to_get` are the owner's landing and are not
writable by a collaborator. A new dataset is a new record, in the pull request of the task that
found it; the census takes it in on the merge.
