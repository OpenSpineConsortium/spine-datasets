# totalsegmentator_tasks: the request text

Sent 2026-10-21 by the owner; waiting for the answer.

To: Jakob Wasserthal (University Hospital Basel, Department of Radiology), the corresponding author of the TotalSegmentator papers; one letter covers the records zenodo_ts_task_hip_implant, zenodo_ts_task_liver_lesions and zenodo_ts_task_pleural_effusion.
Route: email, with the sender block; nothing binding, the sets are CC BY 4.0.

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, derived from SchwingNet's docs/research/xray-dataset-requests.md (the request texts, copied verbatim), docs/research/data-access-requirements.md (who may act) and data/sources/<id>.json (the record). The text below is that file's, verbatim, headings included; the numbered section is the one it holds there. The rules every text follows and the sender block are in letters/TEMPLATE.md; the shared blocks it names (the project title, the lay summary, the data security, IRB, analysis plan and credit paragraphs) are there too.

## 16. TotalSegmentator task sets: an overlap question to the authors (Basel)

The three Zenodo task sets (liver_lesions, record 20272572, 842 CT; pleural_pericard_effusion,
600 CT; hip_implant, record 20272031, 71 CT; CC BY 4.0, published 2026-05-18) are open and need
no request to fetch; what is not known is whether their subjects are among the public v2 and v3
releases already held (doi:10.5281/zenodo.10047292), which decides whether they add people or
only repeat them, since the platform counts a person once. One email to Jakob Wasserthal
(University Hospital Basel, Department of Radiology), the corresponding author of the
TotalSegmentator papers, address from the paper's correspondence line, to confirm. Subject:

```text
[XR/CT Imaging Research] TotalSegmentator task data: overlap with the v2 and v3 releases?
```

Body:

```text
Dear Dr Wasserthal,

I study the application of computer science to improving spinal health, and my current work counts every CT subject once across the collections it reads, so that an agreement measured on one person is never counted twice. I hold the public TotalSegmentator v2 and v3 releases and am about to add the three task datasets you published on Zenodo in May 2026 (liver_lesions, 842 CT; pleural_pericard_effusion, 600 CT; hip_implant, 71 CT). Could you tell me whether the subjects of those three sets overlap the v2 and v3 subjects, and, if they do, whether a subject map or a shared identifier exists, or whether the file names can be matched? If no map exists, a yes or no on overlap is enough for me to treat them conservatively. Thank you for the datasets; they are credited in everything built on them.

With thanks,
```

followed by the sender block. Binding: nothing; the sets are CC BY 4.0 and the fetch is a grid
job on the owner's word. What to expect back: a one-line answer, or none, in which case the
platform treats the three sets as overlapping (no new people) until shown otherwise.
