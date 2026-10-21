# Fetching a plain-download set onto the grid

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21; derived from SchwingNet's
grid/README.md (the X-ray data chain), grid/fetch-xray.json and tools/fetch_sources.py, which is
the owner's chain and is not copied here, and from spine-program's grid rules (its CLAUDE.md, rule
7). This page is the shape of a collaborator's own job; nothing here is a script to run.

## What the owner's chain does, in one paragraph

SchwingNet's grid/ holds the owner's fetch chain: a list of entries (grid/fetch-xray.json), one
per open set, with the route (zenodo, figshare, mendeley, http, kaggle, physionet), the landing
folder, the size and the checksum the page states; a Slurm stage that runs one helper per entry
and writes FETCH.json beside each landing (what ran, the exit codes, every file's bytes and
sha256); a stage that turns a copy into a bank; and a stage that rebuilds the catalog with its
split check. It lands under the owner's own data root, which only the owner writes. A collaborator
with a grid account does the first stage alone, by hand, for one set, onto the shared volume, in
the same shape: a job, a checksum, a record.

## Where it lands

Every set a collaborator fetches lands at /rs/rs_grp_oschome/shared/datasets/<id>/raw, with <id>
the record's id in datasets/. Nothing is unpacked, renamed or converted there; a zip stays a zip
until the owner's chain reads it. Beside raw/ the job writes FETCH.json and the job's own log
folder.

## The shape of the job

A CPU job on the reqp partition with --qos=requeue, a wall time, and --output under the job's own
folder, submitted with -D so a relative --output resolves against that folder:

```
#!/bin/bash
#SBATCH --job-name=fetch-<id>
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --time=2-00:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --output=logs/%x-%j.out
set -euo pipefail
ID=<id>
DEST=/rs/rs_grp_oschome/shared/datasets/$ID/raw
mkdir -p "$DEST" "$(dirname "$DEST")/logs"
# a token, where the route needs one, is read from a file only you can read and never printed
TOKEN_FILE=$HOME/.spine-datasets/<route>.env   # mode 0600; one line NAME=value
if [ -f "$TOKEN_FILE" ]; then
  [ "$(stat -c %a "$TOKEN_FILE")" = "600" ] || { echo "token file must be mode 0600"; exit 2; }
  set -a; . "$TOKEN_FILE"; set +a
fi
cd "$DEST"
<the download command, resumable: wget -c, curl -C -, zenodo_get, or the route's own client>
<verify every file against the checksum the page states: sha256sum -c or md5sum -c>
<write FETCH.json, below>
```

Submit it from inside the set's own folder, `cd /rs/rs_grp_oschome/shared/datasets/<id> &&
sbatch -D "$PWD" fetch.sbatch`, and write the job id on the task at once. Estimate the wall time
from the size (an hour per 20 GB is the owner's guess until a log says otherwise) and give the job
more than that, since a requeued job starts over what it cannot resume.

Tokens and links that are credentials (a Kaggle token, a Hugging Face token, a PhysioNet
password, a presigned link) live in a mode-0600 file under your own $HOME and reach the job only
by being read from that file inside it. Never on the command line, never in --export, never in the
job script, never in a log, never in this repository. A download that needs the owner's own
account (PhysioNet, AIMI, Hugging Face gates) is not a collaborator's job: the task says
"needs the owner".

## FETCH.json

One file beside raw/, written by the job after the checksums pass, in this shape:

```
{
  "id": "<id>",
  "date": "<YYYY-MM-DD, UTC>",
  "job_id": <the Slurm job id>,
  "who": "<your GitHub login>",
  "source": "<the link the record gives>",
  "licence": "<the licence line as the page states it>",
  "files": [
    {"path": "raw/<file>", "bytes": <n>, "sha256": "<hex>", "md5": "<hex or null>", "verified_against": "<the page, the API or the record>"}
  ],
  "bytes_total": <n>,
  "command": "<the download command, with no token in it>"
}
```

The task's result line quotes the path, the job id and the byte total from it; the record's
`grid_path` takes the path and `status` becomes `fetched`.

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
