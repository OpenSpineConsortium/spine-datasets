# Lineage and retirement: one patient once, every sample traced, any set rebuilt

Source: the thread "Check frozen manifest job", 2026-10-24, the owner's ask of that day: be able
to remove datasets to make room for more pertinent, useful or complete ones under the oschome
cap; build a custom dataset drawn from others with no duplicate patients (CTSpine1K and
CTPelvic1K, for example, as parts of CTSpinoPelvic1K); know where every single sample came from;
and be able to regenerate any dataset that was removed. This note is the design and the plan. It
has no numbers about overlap yet, because none has been measured: what the records already say
is in "What the records say now", and the first measurement is step 2 of the plan.

## What exists already

- The freeze (tools/freeze.py, docs/memory/frozen-datasets.md). Every frozen set has, beside its
  data on the grid, FROZEN.files.tsv.gz with the sha256, size and path of every file, and the
  record's measured block carries its bytes, files and tree_sha256. 97 of the 99 planned sets are
  frozen as of 2026-10-24 (the missing two are rsna_rspect and ctpelvic1k). This gives three
  things for free. A refetched copy can be proved identical to what was deleted by its
  tree_sha256. Two sets that hold the same file can be found by joining their lists on sha256
  without reading any data again. And the list is the per-file inventory a removed set leaves
  behind.
- The records (datasets/<id>.json). Each record says where the set came from (link, how_to_get,
  route, record) and what it holds (counts, segmentations, regions). No record yet says that it
  is made from another set or that it overlaps one.
- The reproduce map in SchwingNet (data/reproduce, docs/research/datasets-reproduce.md there),
  which gives every registry record its fetch command, checks and grid path. That is the rebuild
  recipe for a set fetched from a public source.
- The sample index in SchwingNet (grid/run-samples.sh, samples.sqlite on the grid), which already
  reads the DICOM header of every held file. That is where a patient key is read from. This note
  uses only the fact that the index exists, and copies nothing out of it.

## What is missing

1. A set-level lineage. Nothing records that a set was built from others, or which of its cases
   come from where.
2. A sample-level ledger that says, for every image or volume on the grid, which set holds it,
   its path and sha256, and its origin: the collection it first came from, the patient there, and
   the study and series. That origin is what makes "one patient once" decidable across sets that
   renamed, re-encoded or re-anonymised the same scan.
3. A retirement step. Today a set is either on the grid or not; nothing keeps what is needed to
   rebuild a set while deleting its bulk, and nothing refuses a deletion that would lose
   something no other source has.
4. Derived datasets as recipes. A custom set should be a list of sample keys over the kept sets,
   rebuilt the same way every time, not a copy.

## The design

### The origin key

Every sample gets one origin key: `collection / patient / study / series`, taken in this order of
trust:

1. the set's own mapping file, where a derived set ships one (CTSpine1K's metadata, the
   CTSpinoPelvic1K manifest.json, AbdomenAtlas's case table, CTPelvic1K's per-dataset lists);
2. the DICOM header (PatientID, StudyInstanceUID, SeriesInstanceUID) with the TCIA or IDC
   collection, which survives into most NIfTI conversions only through the set's own naming;
3. the file's sha256, which only matches byte-identical copies.

A sample with no key from 1 or 2 is marked origin unknown. It is kept apart, never assumed to be a
new patient, and the person-keyed split guards it as it guards everything else.

### The ledger

lineage.sqlite, built on the grid by one read-only job, one row per sample: set, path, sha256,
bytes, origin key and how the key was found. A view groups rows by patient, so a query answers
which sets hold this person and which copy is the most complete (most labels, original
resolution, licence that allows the use). Only aggregates leave the grid, as with the sample
index: OVERLAP.json, saying for each pair of sets how many patients and bytes they share, goes
into the repository and the census.

### Lineage in the records

Each record gains an optional `lineage` block:

```
"lineage": {
  "built_from": [{"id": "ctspine1k", "patients": 0, "how": "...", "evidence": "..."}],
  "covered_by": [{"id": "...", "patients": 0, "bytes": 0}]
}
```

`built_from` is what the set's authors say. `covered_by` is filled from OVERLAP.json: the share of
this set's patients that kept sets also hold. `python3 tools/census.py check` holds the two
blocks to OVERLAP.json, as it already holds measured to the freeze.

### Retiring a set

A record gets `"reach": "retired"` and a `retired` block only when all of the following hold,
which the census check enforces:

- the set is frozen, so its file list and tree_sha256 stand for exactly what was deleted;
- every sample is either covered by a kept set (same origin key, same or better labels), or
  rebuildable from a public source by a recipe the reproduce map or the record's how_to_get names;
- whatever only this set has, its own labels and metadata above all, is kept: the label folders
  are small next to the images and stay on the grid under the record's id;
- the owner gave the word for that set, by name.

What stays after retirement is the record, FROZEN.json, the file list, the kept extras and the
recipe. The images are deleted by one job on the owner's word, which writes the deletion into the
record's history.

### Repairing a retired set

`repair <id>` rebuilds a retired set in one of two ways. It refetches from the source by the
recipe, or it reassembles the set from the kept sets through the ledger (a symlink or hard-link
tree for samples whose bytes are identical, a conversion step where the set had re-encoded them).
Either way it ends with `freeze.py verify` against the kept file list, so a repair is only called
done when the tree_sha256 matches. Where reassembly cannot reach byte identity, the repair says
which files differ and why.

### A custom dataset

A custom set is a recipe under datasets/derived/<name>.json: the sets it draws from, the
preference order when a patient appears in several (for example the copy with expert level labels
first, then the one with automatic labels), filters (region, modality, licence class), and the
rule one patient once. Building it writes a symlink tree on the grid, freezes it like any other
set, and records every sample's origin, so it can be dropped and rebuilt at no cost. It takes no
space beyond its links and its own labels.

## What the records say now (not measured)

These are leads to measure in step 2, not conclusions.

- CTSpinoPelvic1K (202.7 GB, 802 volumes) is the consortium's release built on TCIA sources with
  CTSpine1K's vertebra labels. CTSpine1K (162.4 GB) holds 1,005 volumes from four sources, so on
  the counts alone about 200 of its volumes are not in CTSpinoPelvic1K; which 200, and whether
  they matter, is what the mapping files will say.
- The ctpelvic1k record holds the 172 volumes of CTPelvic1K's datasets 6 and 7 (the clinical
  sets) plus the pelvic masks of datasets 1 to 5 mapped back to their sources. By the records, it
  is the clinical part that is unique to it, and nothing says those volumes are inside
  CTSpinoPelvic1K. So CTPelvic1K is a candidate for having its images checked against other sets,
  not yet for removal.
- abdomenatlas3_mini (570.6 GB) is assembled from public abdominal CT collections; amos22
  (102.6 GB) may be among them. The case table will say.
- idc_ldct_and_projection_data measured 862.7 GB against a stated 16.5 GB, because the folder
  holds the raw projection data as well as the CT images. Keeping only the reconstructed CT, or
  retiring it with its IDC recipe, is the single largest saving in view.
- The IDC collections held as idc_* are each a refetch from IDC with a known tree hash, so any of
  them can be retired and repaired once the ledger shows nothing unique would be lost.

## The first measurement (2026-10-24, grid job 40775283)

The first pass of tools/lineage.py read 98 frozen sets (lineage/OVERLAP.json, built
2026-10-24T17:59:50Z; rsna_rspect froze after it ran and ctpelvic1k is not frozen yet). It found
no pair of sets that shares anything it can see: no file over 64 KB with the same sha256, no DICOM
series or study UID, no PatientID that looks like an identifier, no identifier-like file name.

That is a true reading of what this pass measures and no answer to the owner's question. The sets
the question is about (CTSpine1K, CTSpinoPelvic1K, CTPelvic1K, AbdomenAtlas, AMOS) are NIfTI
volumes: each release re-encoded and renamed its scans, so no two copies share a byte, and NIfTI
carries no UID. The 52 sets where the pass did read DICOM headers are mostly separate IDC and TCIA
collections, which are not expected to share patients, and none shares a UID with another. So "0 pairs" says that
nothing is held twice byte for byte, and says nothing about the same patient held twice in two
encodings.

What the next pass needs, to see a scan across re-encodings:

1. The sets' own mapping files, which say where each case came from (CTSpine1K's source lists,
   the CTSpinoPelvic1K manifest, AbdomenAtlas's case table, CTPelvic1K's per-dataset lists). Their
   formats have to be read on the grid first.
2. A content fingerprint of each NIfTI volume that survives re-encoding: the shape, the voxel
   spacing and a hash of the voxel values after decompression, read from each volume once. This
   reads image data, unlike the first pass, so it is a heavier job and needs the owner's word and
   count.

What the first pass does give now: the per-set sizes, file counts and DICOM series, study and
patient counts for the 52 DICOM sets (6.5 TB across all 98), which feed the removal list's sizes.

## The plan

1. This note and the record schema for `lineage` and `retired`, with the census check that
   refuses a retirement which breaks the rules above (no grid job).
2. One read-only grid job, on the owner's word (given 2026-10-24): build lineage.sqlite from the
   frozen file lists and the DICOM headers, and write OVERLAP.json. It reads lists and headers, not
   image bytes, and writes nothing into any dataset folder. Built as tools/lineage.py, queued by
   the gate word freeze overlap (grid/freeze.sh overlap), its table carried back by freeze report
   as lineage/OVERLAP.json. The sets' own mapping files and the sample index are not read in this
   first pass: the UIDs, the hashes and identifier-like names come first, and the mapping files
   join once their formats are read from the grid.
3. A removal list from OVERLAP.json: for each candidate, the bytes it frees, the patients it
   shares and with which set, what it alone holds, and its recipe. The owner picks by name.
4. Retirement jobs for the sets the owner picks, one deletion job each, each written into its
   record's history; the census then shows the room gained against the cap.
5. `repair` and the derived-dataset builder, proved by retiring one small set, repairing it and
   matching its tree_sha256.
