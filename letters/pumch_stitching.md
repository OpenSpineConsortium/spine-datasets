# pumch_stitching: the request text

Sent 2026-10-21 by the owner; waiting for the answer.

To: Jinqian Liang and colleagues (Peking Union Medical College Hospital, Department of Orthopaedics).
Route: email, with the subject "[XR/CT Imaging Research] Request for the PUMCH stitching series", the closing paragraph of section 15 and the sender block; one letter can carry this and the SX-Stitch ask.

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, derived from SchwingNet's docs/research/xray-dataset-requests.md (the request texts, copied verbatim), docs/research/data-access-requirements.md (who may act) and data/sources/<id>.json (the record). The text below is that file's, verbatim, headings included; the numbered section is the one it holds there. The rules every text follows and the sender block are in letters/TEMPLATE.md; the shared blocks it names (the project title, the lay summary, the data security, IRB, analysis plan and credit paragraphs) are there too.

## 15. The intraoperative sets the literature names, drafted nowhere, never sent

LITERATURE_STATE.md section 2 lists every labelled intraoperative set as request-only or
unreleased. One short letter each, all by email, each with the subject
"[XR/CT Imaging Research] Request for <set>" and the sender block, each ending with the same
closing paragraph:

```text
I am at the Department of General Surgery, Wayne State University School of Medicine and the Detroit Medical Center. The images would be held on Wayne State's research computing storage, read by me alone, never redistributed, and deleted at the end of the project if you ask; the work is on de-identified imaging under Wayne State IRB determination HPR 2026-269. I will sign a data use agreement on your terms, cite your work and quote the agreement in any publication, and share my results on your images with you before publication.
```

Every one of these measures the same thing, said once here and once in each letter: how reliably
automated image-analysis methods recognise which vertebra is which on real intraoperative images,
reported as per-image agreement with expert or CT-derived labels and confidence intervals.

### 15d. PUMCH stitching series (Liu et al., Eur Spine J 2026)

43 scoliosis patients, four to six overlapping prone AP exposures each on a Philips Zenition 70;
the shift between shots estimated, not recorded; no labels stated; "No datasets were generated or
analysed", so the inventory judged asking unlikely to succeed. Write to the corresponding author
at Peking Union Medical College Hospital (Department of Orthopaedics), to confirm; if the
SX-Stitch letter (section 13) goes to Dr Liang at PUMCH, one letter can carry both asks.

```text
Dear Dr Liang and colleagues,

I study the application of computer science to improving spinal health, and my current work needs intraoperative C-arm exposures of one patient taken in overlapping sequence along the spine, since naming a level on an exposure that holds no landmark depends on carrying the count from the exposures before it. Your stitching series (Eur Spine J 2026: 43 scoliosis patients, four to six overlapping prone exposures each on a Philips Zenition 70) is one of two such collections described anywhere; the other is SX-Stitch from your group and SUSTech, which I am asking for in the same way.

My work measures how reliably automated image-analysis methods carry a vertebra's identity from one exposure to the next and name each vertebra, reported as per-image agreement with expert labels and confidence intervals. I am writing to ask whether the de-identified series, grouped by patient in acquisition order, could be shared under a data use agreement, and what terms you require.
```
