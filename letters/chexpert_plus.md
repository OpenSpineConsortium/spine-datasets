# chexpert_plus: the request text

Not sent.

To: the Stanford AIMI portal, the CheXpert Plus entry.
Route: a research use agreement click-through on the owner's AIMI account, the owner's hand only.

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, derived from SchwingNet's docs/research/xray-dataset-requests.md (the request texts, copied verbatim), docs/research/data-access-requirements.md (who may act) and data/sources/<id>.json (the record). The text below is that file's, verbatim, headings included; the numbered section is the one it holds there. The rules every text follows and the sender block are in letters/TEMPLATE.md; the shared blocks it names (the project title, the lay summary, the data security, IRB, analysis plan and credit paragraphs) are there too.

## 6. CheXpert Plus (Stanford AIMI)

Page to open: https://stanfordaimi.azurewebsites.net/ , the CheXpert Plus entry (the entry's own
address is to confirm on the page); the owner's existing AIMI account, the one INSPECT and Merlin
need, covers it.

Fields likely asked (to confirm): the account's name and institution, a per-dataset research use
agreement with checkboxes (non-commercial, no redistribution, no re-identification, Stanford's
publication acknowledgement), and sometimes a one-line intended use. Text for the use line:

```text
Measuring how reliably automated image-analysis methods recognise which vertebra is which on frontal and lateral chest radiographs across the many devices of one centre; non-commercial research, Department of General Surgery, Wayne State University, de-identified images under IRB determination HPR 2026-269.
```

Binding, the owner's hand only: the research use agreement click-through, one per dataset. Read
its clauses on derivative works and on what may be built from the images before accepting, a lawyer question. Fee: none. What to expect
back: a time-limited Azure Blob URL, fetched with AzCopy as a grid job on the owner's word; the
DICOM release is several terabytes, so the JPG-plus-DICOM choice is made before the fetch.
