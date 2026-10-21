# huashan_fudan: the request text

Sent 2026-10-21 by the owner; waiting for the answer.

To: Jiang Jianyuan and colleagues (Huashan Hospital, Fudan University, Department of Orthopaedics).
Route: email, with the subject "[XR/CT Imaging Research] Request for the Huashan intraoperative lumbar films and CTs", the closing paragraph of section 15 and the sender block.

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

### 15c. Huashan Hospital, Fudan University (Shao et al. 2024)

140 living lumbar patients (January 2020 to December 2023) with preoperative CT and
intraoperative AP and lateral films of L1 to L5; the device is unnamed; two co-authors are from
Shanghai Maestro Surgical Robotics; no data statement. Write to the corresponding author (Jiang
Jianyuan, Huashan Hospital, Department of Orthopaedics), address from the paper's correspondence
line, to confirm.

```text
Dear Professor Jiang and colleagues,

I study the application of computer science to improving spinal health, and my current work needs real intraoperative lumbar images of living patients paired with the same patient's preoperative CT, so that the correct level of each vertebra on the intraoperative image can be established from the CT. Your series of 140 patients with preoperative CT and intraoperative anteroposterior and lateral films (Shao et al. 2024) is the largest of that kind I have found.

My work measures how reliably automated image-analysis methods recognise which vertebra is which on intraoperative images, including the transitional variants that cause wrong-level errors, reported as per-image agreement with CT-derived labels and confidence intervals, by device and by variant. I am writing to ask whether the de-identified films and CTs could be shared under a data use agreement, and, to judge fit, the make and type of the C-arm, whether the films exist as DICOM with headers, and how many frames each patient has.
```
