# The dataset records

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21; the records are copied from
SchwingNet's data/sources/<id>.json (the registry rendered by tools/sources.py, whose field rules
are src/schwingnet/sources.py), and the routes from docs/research/data-access-requirements.md.

One JSON file per dataset not yet held on Wayne State's grid: 81 of SchwingNet's 111 records,
every one whose `reach` is `get` (public or by request, not yet fetched), `gated` (behind an
agreement, an application or a login) or `embargoed`; the 26 held sets, the one that exists
nowhere (cervical_thoracic_intraop) and the three set aside (spinesac, mendeley_5jdfdgp762,
roboflow_vindr_relabels) are not here. Five more records were written from
docs/research/xray-dataset-requests.md section 15 for intraoperative sets the literature names
that had no registry record (levelcheck_jhu, vanderbilt_tha_fluoro, huashan_fudan,
pumch_stitching, nit_warangal_nims), each saying so in its `record` field. 86 records in all.

The fields, as SchwingNet's record has them, copied exactly (licence and link above all):

- `id`, `name`, `group` (fluoro, video, projections, films, ct, future), `what`, `level_truth`,
  `reach`, `licence`, `link`, `how_to_get` (the steps, as the registry gives them, naming
  SchwingNet's and the data platform's tools), `grid_path` (null until fetched), `counts`,
  `measured` (empty until a grid job fills it), `record` (where the record came from).
- `source_status`: SchwingNet's own `status` text as of 2026-10-21, kept so nothing is lost.

The fields this repository adds:

- `route`: how the set comes in: `letter`, `form`, `account`, `agreement`, `download` or
  `owner-only`.
- `status`: where the task stands: `todo`, `requested`, `granted`, `fetched`, `refused` or
  `needs-owner`.
- `result`: free text, the dated result line README.md describes; empty until there is one.
- `history`: the steps taken so far, oldest first, each `{"date": "YYYY-MM-DD", "step": ...,
  "note": ...}` with the step one of `researched`, `asked`, `granted`, `fetching`, `fetched`,
  `refused`, `handed-back` or `note`, and the note one line saying what happened (the letter
  sent and to whom, the form submitted, the job id, the reason). A status other than `todo`
  needs at least one entry saying when.
- `obstacles`: a list of one-line strings, what stands in the way right now (a DUA to sign, a
  bounce, a licence line still to confirm, a token only the owner holds); empty when nothing.
- `next`: one line, what whoever holds the task does next; empty when nothing is planned.

The pipeline board (tools/pipeline.py; PIPELINE.md on the branch `pipeline`, and the interactive
pipeline.html on the docs site) is drawn from these fields and nothing else: the status and the
route put a record in its column, the history is the trail, the obstacles and the next step are
the card. `bash scripts/check.sh` runs `python3 tools/pipeline.py check`, which refuses a record
whose fields do not hold together. Inside every column the X-ray groups (fluoro, video,
projections, films) come before ct, and the fetch order follows the same rule: X-ray sets before
CT, the owner's order of 2026-10-21.

A collaborator changes `status`, `result` and, after a fetch, `grid_path` and `measured`, and
replaces a "to confirm on the page" with what the page says; `licence` and `link` change only when
the page shows the record wrong, and the pull request says so. The path convention for a fetch is
/rs/rs_grp_oschome/shared/datasets/<id>/raw (grid/README.md); the registry's own paths under
/rs/rs_grp_oschome/go2432/data/<id>/raw in `how_to_get` are the owner's landing and are not
writable by a collaborator.
