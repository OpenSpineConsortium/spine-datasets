# aariz_cephalograms: the request text

Not sent; not needed while the download works.

To: Muhammad Moazam Fraz and colleagues (NUST), the authors of Aariz.
Route: email, kept in reserve: on 2026-10-21 the 1,000-film set was found to be an open figshare download (article 27986417, CC BY 4.0), so the set needs a grid job and no letter; send this only if the download route fails.

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, derived from SchwingNet's docs/research/xray-dataset-requests.md (the request texts, copied verbatim), docs/research/data-access-requirements.md (who may act) and data/sources/<id>.json (the record). The text below is that file's, verbatim, headings included; the numbered section is the one it holds there. The rules every text follows and the sender block are in letters/TEMPLATE.md; the shared blocks it names (the project title, the lay summary, the data security, IRB, analysis plan and credit paragraphs) are there too.

## 3. Aariz cephalometric benchmark (by request to the authors)

Page to open: https://arxiv.org/abs/2302.07797 (Khalid, Fraz et al., "Aariz: a benchmark dataset
for automatic cephalometric landmark detection and CVM stage classification"); the paper's data
availability line names the request route, likely a Google form or an email to the corresponding
author at NUST (Muhammad Moazam Fraz) or Riphah International University. To confirm in the paper's
PDF, which this container cannot open; the CEPHA29 challenge page (ISBI 2023) may carry a form of
its own.

Route: email, unless the paper gives a form. Subject:

```text
[XR/CT Imaging Research] Request for the Aariz cephalogram dataset (1,000 films, 7 devices)
```

Body:

```text
Dear Professor Fraz and colleagues,

I study the application of computer science to improving spinal health, and my current work needs lateral films of the upper cervical spine from several devices and from children and adolescents, which no spine-specific public set provides. Your Aariz benchmark (arXiv:2302.07797; the CEPHA29 challenge) gives 1,000 lateral cephalograms from seven devices with a cervical vertebral maturation stage per film, and C2 to C4 lie in every image.

My work measures how reliably automated image-analysis methods recognise which vertebra is which, across modalities, devices and exposures, including the transitional variants that cause wrong-level errors in spine care. On your films the question is the top of the cervical count: whether C2, C3 and C4 are identified consistently across seven devices and across the maturation stages, reported as per-image agreement with expert labels and confidence intervals, by device and by stage.

I am writing to ask for the 1,000 cephalograms with the landmark and CVM annotations and the per-image device labels, under whatever research agreement you use. I am at the Department of General Surgery, Wayne State University School of Medicine and the Detroit Medical Center. The images would be held on Wayne State's research computing storage, read by me alone, never redistributed, and deleted at the end of the project if you ask. The work is on de-identified imaging under a Wayne State IRB determination (HPR 2026-269). I will sign your agreement, cite the paper and the challenge, and quote the agreement in any publication.

With thanks,
```

followed by the sender block. Binding, the owner's hand only: the authors' agreement or a form's
checkbox, if any. Fee: none expected. What to expect back: an agreement to sign or a link; the
ISBI 2015 set (400 films, 19 landmarks) can be fetched openly meanwhile.
