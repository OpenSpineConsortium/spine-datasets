# vanderbilt_tha_fluoro: the request text

Sent 2026-10-21 12:30 UTC by the owner to its senior authors; waiting for the answer.

To: the corresponding and senior authors of Chan et al., J Arthroplasty 2025 (Vanderbilt).
Route: email, with the subject "[XR/CT Imaging Research] Request for the Vanderbilt intraoperative THA fluoroscopy set", the closing paragraph of section 15 and the sender block.

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

### 15b. Vanderbilt intraoperative THA fluoroscopy (Chan et al., J Arthroplasty 2025)

146 living patients, 161 anterior-approach hips, 336 AP frames with eight bony landmarks
including midline L5/S1 and both sacroiliac joints, plus 84 cup frames; AP only; the C-arm is
not reported; no data statement, code only at github.com/vine-lab-vu/Label-Augmentation
(doi:10.1016/j.arth.2025.01.032). Write to the corresponding author named on the paper
(Vanderbilt Orthopaedic Surgery and Computer Science), to confirm.

```text
Dear Dr Chan and colleagues,

I study the application of computer science to improving spinal health, and my current work needs real intraoperative frames of the pelvis on which the lumbosacral junction has been marked by an expert, since the sacrum and L5 are the anchors from which lumbar levels are counted and the lumbosacral transitional variants are the commonest cause of a wrong count. Your fluoroscopy set (J Arthroplasty 2025;40:2092) marks midline L5/S1 and both sacroiliac joints on 336 intraoperative frames from 146 patients.

My work measures how reliably automated image-analysis methods find those anchors and name the vertebrae above them on real intraoperative images, reported as per-image agreement with your landmarks and confidence intervals. I am writing to ask whether the de-identified frames with the bony landmarks could be shared under a data use agreement with Vanderbilt, and what terms you require; the cup landmarks are not needed.
```
