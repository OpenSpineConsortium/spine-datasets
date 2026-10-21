# stanford_aimi_merlin: the request text

Not sent.

To: the Stanford AIMI portal, the Merlin entry.
Route: a research use agreement click-through on the owner's AIMI account, the owner's hand only.

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, derived from SchwingNet's docs/research/xray-dataset-requests.md (the request texts, copied verbatim), docs/research/data-access-requirements.md (who may act) and data/sources/<id>.json (the record). The text below is that file's, verbatim, headings included; the numbered section is the one it holds there. The rules every text follows and the sender block are in letters/TEMPLATE.md; the shared blocks it names (the project title, the lay summary, the data security, IRB, analysis plan and credit paragraphs) are there too.

## 10. Stanford AIMI Merlin and INSPECT (research-use agreement)

Pages to open, signed in to the owner's AIMI account:
https://stanfordaimi.azurewebsites.net/datasets/60b9c7ff-877b-48ce-96c3-0194c8205c40 (Merlin; the
same data are listed at https://stanford.redivis.com/datasets/exfv-e8h3kvfhs) and the INSPECT
entry on the same portal (its address to confirm on the page). Merlin is 25,494 abdominal CTs of
18,317 patients (Stanford ED 2012 to 2018); INSPECT about 19,400 CT pulmonary angiography
patients; the data platform ranks Merlin alone above the whole of its tier 1 for new transitional
spines (expected 1,260 people; ACQUISITION_PLAN.md section 7). These are CT, not X-ray, and go in
this file because the owner's ask covers every gated set.

Fields likely asked (to confirm on the page): the account's name, institution and email, a
per-dataset research use agreement with checkboxes (non-commercial, no redistribution, no
re-identification, Stanford's acknowledgement), sometimes an intended-use line. Text for the line:

```text
Measuring how reliably automated image-analysis methods recognise which vertebra is which in CT of the trunk, including the transitional lumbosacral and thoracolumbar variants behind wrong-level errors, across scanners and protocols; non-commercial research, Department of General Surgery, Wayne State University School of Medicine and the Detroit Medical Center; de-identified images under IRB determination HPR 2026-269.
```

Binding, the owner's hand only: the two agreement click-throughs (one per dataset), each binding
the person who accepts; read the clauses on derivative works and on what may be built from the images first, a lawyer question. Fee:
none. What to expect back: approval and a time-limited Azure Blob URL per dataset. That URL is a
credential: it goes into a mode-0600 file on the grid (under the owner's HOME or the Ceph data
root, never a job script, argv or `sbatch --export`), and an AzCopy Slurm job on the owner's word
reads it from the file, verifies against the portal's file list and records the fetch; a URL that
expires before the job runs is re-issued from the portal by the owner.
