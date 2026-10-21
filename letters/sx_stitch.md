# sx_stitch: the request text

Sent 2026-10-21 by the owner; waiting for the answer.

To: Wei Liu (SUSTech) and Jinqian Liang (PUMCH), the corresponding authors of SX-Stitch.
Route: email, with the sender block.

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, derived from SchwingNet's docs/research/xray-dataset-requests.md (the request texts, copied verbatim), docs/research/data-access-requirements.md (who may act) and data/sources/<id>.json (the record). The text below is that file's, verbatim, headings included; the numbered section is the one it holds there. The rules every text follows and the sender block are in letters/TEMPLATE.md; the shared blocks it names (the project title, the lay summary, the data security, IRB, analysis plan and credit paragraphs) are there too.

## 13. SX-Stitch intraoperative C-arm series (Li et al., arXiv:2409.05681)

The set: 1,032 intraoperative C-arm spinal images at 512, 1024 and 1920 pixels, in consecutive
overlapping series from one patient at 20 to 90 percent overlap, with vertebra masks; the only
published collection of overlapping intraoperative C-arm frames of the spine. Corresponding
authors: Jinqian Liang (Peking Union Medical College Hospital) and Wei Liu (Department of
Mechanical and Energy Engineering, Southern University of Science and Technology). No email is
printed in the arXiv version, so the addresses come from the SUSTech and PUMCH directories, to
confirm; the paper's data statement says no datasets were generated, so the inventory judges
success unlikely. Route: email. Subject:

```text
[XR/CT Imaging Research] Request for the SX-Stitch intraoperative C-arm image series
```

Body:

```text
Dear Professor Liu and Dr Liang,

I study the application of computer science to improving spinal health, and my current work needs real intraoperative C-arm images of the spine taken as consecutive overlapping exposures of one patient, which no public set provides. Your SX-Stitch paper (arXiv:2409.05681) describes 1,032 such images in overlapping series at 20 to 90 percent overlap, with vertebra masks.

My work measures how reliably automated image-analysis methods recognise which vertebra is which on intraoperative images, where a limited field often holds no landmark and the level must be carried from one exposure to the next; wrong-level errors arise exactly there. Every number I have so far comes from single radiographs and from simulated series, and your set would let the same measurement be reported on real intraoperative series, as per-image agreement with your masks and confidence intervals.

I am writing to ask whether the series could be shared for non-commercial research: the images grouped by patient in acquisition order, any vertebra masks or level labels that exist, and the terms you require. I am at the Department of General Surgery, Wayne State University School of Medicine and the Detroit Medical Center. The images would be held on Wayne State's research computing storage, read by me alone, never redistributed, and deleted at the end of the project if you ask; the work is on de-identified imaging under Wayne State IRB determination HPR 2026-269. I will sign a data use agreement through Wayne State on your terms, cite SX-Stitch in any publication, and share my results on your series with you before publication.

With thanks,
```

followed by the sender block. Binding, the owner's hand only: the DUA, if one is offered. Fee:
none expected. What to expect back: most likely a refusal or silence; a yes brings a Chinese
institutional agreement and a transfer by link.
