# rexgradient_160k: the request text

Not sent, and no longer needed: the owner passed the gate on the Hugging Face page under the owner's own account, and the owner's chain fetched the whole set on 2026-10-23 (datasets/rexgradient_160k.json, held). A separate note to the corresponding author, drafted 2026-10-22 in the owner's mailbox and asking leave to download all ten image parts under the agreement's section A.5, waits for the owner's word: deleted, or reworded as an after-the-fact note.

To: the gate form on the dataset's Hugging Face page.
Route: form (a gate with an agreement checkbox), the owner's hand only, on the owner's Hugging Face account.

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, derived from SchwingNet's docs/research/xray-dataset-requests.md (the request texts, copied verbatim), docs/research/data-access-requirements.md (who may act) and data/sources/<id>.json (the record). The text below is that file's, verbatim, headings included; the numbered section is the one it holds there. The rules every text follows and the sender block are in letters/TEMPLATE.md; the shared blocks it names (the project title, the lay summary, the data security, IRB, analysis plan and credit paragraphs) are there too.

## 4. ReXGradient-160K (Hugging Face, gated)

Page to open: https://huggingface.co/datasets/rajpurkarlab/ReXGradient-160K, signed in to the
owner's Hugging Face account; the gate form sits above the file list.

Fields the gate is likely to ask (to confirm on the page): full name, affiliation and institutional
email, intended use (a text box), and a checkbox accepting the non-commercial data access and use
agreement; some gates add country and a "I agree not to redistribute" line. Text for the use box:

```text
I study the application of computer science to improving spinal health, and my current work needs chest radiographs from many sites, since a lateral chest film is a lateral thoracic spine from T1 to about L1 and a frontal film shows the thoracic spine behind the mediastinum. The work measures how reliably automated image-analysis methods recognise which vertebra is which across devices and exposure settings, reported as per-image agreement with expert labels and confidence intervals, by site. The 79 sites of ReXGradient-160K are the widest exposure coverage of any chest set. Non-commercial academic research at the Department of General Surgery, Wayne State University School of Medicine, on de-identified images under IRB determination HPR 2026-269; the images stay on Wayne State's research computing storage, read by me alone, and are not redistributed. The source and its agreement will be credited in any publication.
```

Binding, the owner's hand only: the agreement checkbox, which binds the person who ticks it. Read
the agreement's clauses on models, derivatives and outputs before ticking anything, as the
Radiopaedia record (data/sources/radiopaedia.json) records that same question for its licence;
whether such a clause touches this project is a question for the owner's lawyer, not for a session.
Fee: none. What to expect back: an instant or a reviewed approval (the Rajpurkar lab gates have
been reviewed by hand, days); then `huggingface-cli download` with the owner's token in a file on
the grid, as a job on the owner's word. Whether the studies include lateral views is read from the
metadata once approved.
