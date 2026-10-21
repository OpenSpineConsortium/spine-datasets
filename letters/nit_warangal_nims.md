# nit_warangal_nims: the request text

Sent 2026-10-21 by the owner; waiting for the answer.

To: the authors named on the 2D-3D-sci-registration repository and its manuscript (NIT Warangal; NIMS Hyderabad).
Route: email, with the subject "[XR/CT Imaging Research] Request for the 2D-3D-sci-registration raw frames and CTs", the closing paragraph of section 15 and the sender block.

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

### 15e. NIT Warangal and NIMS Hyderabad (2D-3D-sci-registration)

Nine living patients and 51 AP and lateral C-arm sets in the repository's README (at most 49
unique frames), a Ziehm C-arm, preoperative CT with level-named L1 to L5 centroids; the 60
centroid files and 54 overlay PNGs (the real frame at 8 bits beside a DRR) are public on the
repository, the CT and raw X-rays "available upon reasonable request". Write to the authors named
on the repository and the manuscript (National Institute of Technology Warangal; Nizam's
Institute of Medical Sciences, Hyderabad), to confirm.

```text
Dear colleagues,

I study the application of computer science to improving spinal health, and my current work needs real intraoperative C-arm images of the lumbar spine with the level of each vertebra established from the same patient's CT. Your 2D-3D-sci-registration repository publishes level-named L1 to L5 centroid files and overlay images for nine patients on a Ziehm C-arm, and says the CT and the raw X-rays are available on reasonable request.

My work measures how reliably automated image-analysis methods recognise which vertebra is which on intraoperative images across devices, reported as per-image agreement with CT-derived labels and confidence intervals. I am writing to ask for the raw anteroposterior and lateral frames at their original bit depth and size, the preoperative CTs and the projection geometry behind the overlays, for the nine patients and the two of the manuscript, under whatever agreement you require.
```
