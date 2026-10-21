# levelcheck_jhu: the request text

Sent 2026-10-21 by the owner; waiting for the answer.

To: Jeffrey Siewerdsen (MD Anderson) and the JHU co-authors (Ali Uneri, Wojciech Zbijewski, J. Webster Stayman).
Route: email, with the subject "[XR/CT Imaging Research] Request for the LevelCheck clinical cohort", the closing paragraph of section 15 and the sender block.

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

### 15a. LevelCheck clinical cohort (Johns Hopkins, Siewerdsen group)

178 patients with preoperative CT and 398 intraoperative radiographs (De Silva et al., Spine
2016), plus Ketcha et al. 2017's 24 thoracolumbar patients with 61 Carestream DRX-1 radiographs,
and the 62-image reader set of Manbachi et al. 2018. Neither paper has a data statement; the
route is a DUA with the PI. Jeffrey Siewerdsen has been at MD Anderson (Surgical Data Science)
since 2022; copy the JHU co-authors still there (Ali Uneri, Wojciech Zbijewski, J. Webster
Stayman), addresses from the institutional directories, to confirm.

```text
Dear Professor Siewerdsen and colleagues,

I study the application of computer science to improving spinal health, and my current work needs real intraoperative radiographs of the spine for which the correct level of each vertebra is already known from the same patient's labelled preoperative CT. The LevelCheck clinical cohort (De Silva et al., Spine 2016: 178 CTs and 398 radiographs; Ketcha et al. 2017; the 62 reader images of Manbachi et al. 2018) is the only collection of that kind and size described in the literature, and the hard cases in it, transitional anatomy and degraded images, are exactly where wrong-level errors happen.

My work measures how reliably automated image-analysis methods recognise which vertebra is which on such images from image content alone, reported as per-image agreement with the levels your registration placed and confidence intervals, by level and by anatomical variant; the result would sit beside the surgeon error rates your group measured. I am writing to ask whether the de-identified radiographs with their level labels (and the CTs, if the agreement allows) could be shared under a data use agreement with Johns Hopkins or MD Anderson, and what terms you require.
```
