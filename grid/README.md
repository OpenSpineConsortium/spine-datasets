# Fetching a plain-download set onto the grid

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21; derived from SchwingNet's
grid/README.md (the X-ray data chain), grid/fetch-xray.json and tools/fetch_sources.py, which is
the owner's chain and is not copied here, and from spine-program's grid rules (its CLAUDE.md, rule
7), and the thread "Automated dataset PR review", 2026-10-21 (issue #100), which made a pull
request with a manifest the one way a collaborator's set reaches the shared tree.

## What the owner's chain does, in one paragraph

SchwingNet's grid/ holds the owner's fetch chain: a list of entries (grid/fetch-xray.json), one
per open set, with the route (zenodo, figshare, mendeley, http, kaggle, physionet), the landing
folder, the size and the checksum the page states; a Slurm stage that runs one helper per entry
and writes FETCH.json beside each landing (what ran, the exit codes, every file's bytes and
sha256); a stage that turns a copy into a bank; and a stage that rebuilds the catalog with its
split check. It lands under the owner's own data root, which only the owner writes. A collaborator's
set reaches the shared volume in the same shape, a checksum and a record, through a pull request
and the promoter below.

## Where it lands, and who writes it

Every set lands at /rs/rs_grp_oschome/shared/datasets/<id>/raw, with <id> the record's id in
datasets/, and only one writer ever touches that tree: the promoter, which runs as the owner's own
grid account (tools/promote.py, kept queued by grid/promote.sh, issue #100). A collaborator's grid
account reads the tree and never writes it, so nobody needs, or asks for, an entry in its access
list. Nothing is unpacked, renamed or converted there; a zip stays a zip until the owner's chain
reads it. Every file is 0444 and every folder of raw/ 0555; beside raw/ the promoter writes
PROMOTED.json (the manifest's commit, the pull request and who merged it, the promoter's job id,
and every file's bytes and sha256 as measured after the copy).

## How a set gets there

1. The collaborator who holds the task writes manifests/<id>.json (manifests/README.md) from what
   the source publishes, and sets the record to `fetching`, in the task's pull request.
2. The required check reviews it (tools/dataset_review.py; CONTRIBUTING.md, "The automated
   review").
3. The owner, or a session on the owner's standing word, merges it.
4. Within about ten minutes the promoter's pass finds the manifest, confirms that an owner merged
   its last change (and not on the promoter's own promote/ branch), downloads every file from its link inside the Slurm job, checks the bytes and
   the checksum of what landed, renames the checked tree into place, makes it read-only, and opens
   the record's update to `fetched` as a pull request from promote/<id> with auto-merge on for
   that exact commit, so a push by anyone else to that branch is never merged by it.

X-ray sets are promoted before CT. A set over the space budget in grid/promote.json waits until
the owner names it there. A download that fails or does not check stays in
shared/<id>/.incoming-<job> and the next pass resumes it; a raw/ already there that does not match
is left alone and reported in the promoter's log.

## The promoter, for the owner

The chain is a Slurm job on reqp/requeue, eight hours of wall time, that first queues its own
successor (afterany), so it comes back after a preemption or a wall time with nobody at the
keyboard; successors are singleton jobs of one name and a lock keeps two passes apart. Each pass
takes the promoter's code, and reads the space budget, from the default branch only where the
last change came from a pull request the owner opened and merged with no commit in it tied to
anyone else's account; anything else keeps the copy on the grid, or the default budget of 100 GB.
It acts on a manifest only where the owner merged it, never from its own promote/ branches, and
leaves a terabyte free on the volume. It needs gh signed in as the owner and curl, both already
there for hpcworker. Its folder is /rs/rs_grp_oschome/go2432/spine-datasets-promoter (code/,
logs/ and the lock). Started once, in a grid shell, with COMMIT a commit of the default branch
the owner has read, whose copy of the code the chain starts from:

```
gh api -H "Accept: application/vnd.github.raw" "repos/OpenSpineConsortium/spine-datasets/contents/grid/promote.sh?ref=COMMIT" > ~/promote.sh
bash ~/promote.sh start COMMIT
```

`bash ~/promote.sh status` shows the chain and its latest log lines; `bash ~/promote.sh stop`
cancels it.

## What nobody does

- Nothing on the login node: no download, no checksum, no unzip, no python; every byte moves inside
  a Slurm job on a compute node, and temp goes on the node's local disk (not $TMPDIR, which is
  CephFS at Wayne State).
- Never fetch Radiopaedia by script: its terms bar automated access; the licence application is
  the owner's and the cases come by the route the countersigned agreement gives.
- Never a set whose licence or agreement is not yet granted, or whose licence line still reads "to
  confirm on the page": read the page, write the line into the record, then fetch.
- Never a set the record marks excluded or not to be fetched (the Roboflow relabels of
  VinDr-SpineXR; the Kaggle fracture set until its origin is shown redistributable; the Kaggle
  scoliosis set is fetched but used only after its hashes are checked against the AASCE copy).
- Never CT-RATE (21.3 TB) or the full NLST (2.3 TB) without the owner's word on the space.
- Never delete anything under the shared volume; a failed fetch is reported, not cleaned up.
- Never copy an image off the grid, into this repository, a laptop, a cloud service or a chat.
