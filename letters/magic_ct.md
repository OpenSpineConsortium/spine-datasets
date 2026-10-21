# magic_ct: the request text

Not sent.

To: Maxim Popov and colleagues (Nazarbayev University), the contact named on Zenodo record 18389015.
Route: email with the owner's CITI certificate attached, from the owner's mailbox, the owner's hand only, since it is the application under the record's data use agreement.

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, derived from SchwingNet's docs/research/xray-dataset-requests.md (the request texts, copied verbatim), docs/research/data-access-requirements.md (who may act) and data/sources/<id>.json (the record). The text below is that file's, verbatim, headings included; the numbered section is the one it holds there. The rules every text follows and the sender block are in letters/TEMPLATE.md; the shared blocks it names (the project title, the lay summary, the data security, IRB, analysis plan and credit paragraphs) are there too.

## 11. MAGIC-CT (Zenodo 18389015, DUA application)

Page to open: https://zenodo.org/records/18389015 (version 2, 2026; 562 patients with abdominal
or thoracic tumours, NRRD, 39.1 GB, 492 with reports; Nazarbayev University, Kazakhstan). The
files download without a gate, but the record's data use agreement asks for an application with
proof of a completed human-subjects or HIPAA course, and binds the applicant to no
re-identification, no onward sharing, security, reporting any identifying information found to
the corresponding author, research use only, release of the code behind any disseminated result,
and either side ending the agreement. The contact the record names is maxim.popov@nu.edu.kz.

Route: email to that address with the owner's CITI certificate attached (the one PhysioNet's
credentialing holds; the owner downloads it from CITI, never a session). Subject:

```text
[XR/CT Imaging Research] MAGIC-CT data use application (Zenodo 18389015)
```

Body:

```text
Dear Dr Popov and colleagues,

I study the application of computer science to improving spinal health, and my current work needs trunk CT from scanners and populations outside North America and Western Europe, in which the vertebral column is in field end to end. MAGIC-CT's 562 patients, with the spine incidental to the tumour imaging, add a Central Asian population and scanner protocols no other collection I hold covers.

My work measures how reliably automated image-analysis methods recognise which vertebra is which, including the transitional variants at the thoracolumbar and lumbosacral junctions that cause wrong-level errors in spine care, and reports per-image agreement with expert labels and confidence intervals, by scanner and by variant. I use the images only for that; no tumour or clinical question is studied and no finding about any individual is produced.

This is my application under the data use agreement on the record. I accept its terms: no re-identification, no onward sharing, secure storage, reporting to you any identifying information I find, research use only, release of the code behind any result I disseminate, and either side's right to end the agreement. My proof of a completed human-subjects research course is attached (CITI Program, Wayne State University). I am at the Department of General Surgery, Wayne State University School of Medicine and the Detroit Medical Center; the work is on de-identified imaging under Wayne State IRB determination HPR 2026-269. The data will be held on Wayne State's research computing storage, read by me alone, and deleted if you ask. I will cite the record and quote the agreement in any publication.

With thanks,
```

followed by the sender block. Binding, the owner's hand only: the application and its attached
certificate, which the owner sends from the owner's own mailbox. Fee: none. What to expect back:
an acknowledgement; then the 39.1 GB is fetched to Ceph as a Slurm job on the owner's word and
checked against the record's checksums. The "release of the code" clause is read against the
patent position before the application goes, a lawyer question.
