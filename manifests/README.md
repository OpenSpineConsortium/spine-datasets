# Manifests: what the promoter fetches into the shared tree

Source: the thread "Automated dataset PR review", 2026-10-21 (issue #100).

A collaborator never writes /rs/rs_grp_oschome/shared/datasets. They open a pull request with the
record and one file here, manifests/<id>.json, the exact list of what the set is; the required
check reviews it (tools/dataset_review.py); the owner, or a session on the owner's standing word,
merges it; and the promoter, running as the owner's own grid account (tools/promote.py, kept
queued by grid/promote.sh), downloads every file from its link, checks the bytes and the checksum
of what landed, installs it read-only at /rs/rs_grp_oschome/shared/datasets/<id>/raw with
PROMOTED.json beside it, and opens the record's update to fetched as a pull request of its own.
X-ray sets are promoted before CT.

## The file

```
{
 "id": "<the record's id, which is also this file's name>",
 "source": "<the record's link, exactly>",
 "licence": "<the record's licence, exactly>",
 "date": "<YYYY-MM-DD, UTC, when the list was read>",
 "files": [
  {
   "path": "raw/<the file's name>",
   "url": "https://<a public link on the source's own site>",
   "bytes": <n>,
   "sha256": "<64 hex digits, as the source publishes it>",
   "verified_against": "<where the checksum came from: the source's API, its page, a checksum file>"
  }
 ],
 "bytes_total": <the sum of the files' bytes>
}
```

Where the source publishes an md5 and no sha256 (Zenodo, figshare), a file carries `"md5"` in
place of `"sha256"`; PROMOTED.json then records the sha256 the promoter computed.

## Writing one

For Mendeley Data and Zenodo the source's own API gives every file's size and checksum, so the
manifest is written from it, on any machine with the network (not in the check):

```
python3 tools/dataset_review.py manifest <id> --mendeley <dataset id> --version <n>
python3 tools/dataset_review.py manifest <id> --zenodo <record number>
```

On a Mac with the python.org Python, the call fails certificate verification until Python is
given the system's certificates: run it as `SSL_CERT_FILE=/etc/ssl/cert.pem python3 tools/...`, or
run once the `Install Certificates.command` that python.org's installer puts in the Python folder
under Applications.

For any other source, write it by hand from what the page states. In the same pull request set
the record's `status` to `fetching`, add a `fetching` entry to its `history` ("manifest ready; the
promoter fetches after merge"), and set `next` to "the promoter installs it after merge". Leave
`grid_path` null: the promoter's own pull request fills it.

## The rules the check holds a manifest to

The record exists and its licence allows the fetch (an open licence such as CC BY or CC0 with no
non-commercial or no-derivatives term, or a `granted` step in its history; never "to confirm"); the source and licence are copied exactly;
every path is raw/<name> with no ".."; every link is https on the source's own host (or one the
source is known to serve files from, such as ndownloader.figshare.com) with no token, key or
signature in it; every size is positive and they add up; every checksum has its
shape. No set is held to a size of its own: it is promoted whenever the shared volume has room.
The promoter acts only on a manifest whose last change an owner merged, never one from its own
promote/ branches, and leaves a terabyte free on the shared volume.
