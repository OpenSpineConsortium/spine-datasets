# The request letter: a template every collaborator fills in

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, derived from SchwingNet's
docs/research/xray-dataset-requests.md, whose sections "Rules every text follows" and "Shared text
blocks" are copied below verbatim, and from docs/research/data-access-requirements.md (who may act).

A collaborator sends a letter from their own institutional mailbox, with go2432@wayne.edu in copy,
under the rules below; the sender block then carries the collaborator's own name, department and
institution, with the owner's block as the example of its shape. Everything binding stays the
owner's: the letter asks for the terms and never accepts them (CONTRIBUTING.md). Before sending,
read the text once more for the words the confidentiality rule bans.

## The letter, to fill in

Subject:

```text
[XR/CT Imaging Research] Request for <the dataset's name as its page or paper gives it>
```

Body:

```text
Dear <the corresponding author's or the data custodian's name and title, as the page gives it>,

I study the application of computer science to improving spinal health, and my current work needs <what the set holds that the held sets do not: the modality, the region, the devices, the population, the labels>. <The set's name and reference> provides <the count and what comes with it, as the page or paper states>.

My work measures how reliably automated image-analysis methods recognise which vertebra is which on <radiographs, fluoroscopy or CT, as fits>, including the transitional variants that cause wrong-level errors in spine care, across modalities, devices and exposures, reported as per-image agreement with expert labels and confidence intervals<, by device, by level or by variant, as fits>.

I am writing to ask whether <the images, the labels, the metadata, named as files> could be shared for non-commercial research, and what terms you require. I work with Dr Gregory Schwing at the Department of General Surgery, Wayne State University School of Medicine and the Detroit Medical Center, where the images would be held on Wayne State's research computing storage, read only by the study team, never redistributed, and deleted at the end of the project if you ask; the work is on de-identified imaging under Wayne State IRB determination HPR 2026-269. Dr Schwing will sign a data use agreement through Wayne State on your terms, and we will cite <the paper or record>, quote the agreement in any publication, and share our results on your images with you before publication.

With thanks,

<Your name and degrees>
<Your department>
<Your institution>
<Your city and country>
<Your institutional email>
cc: Gregory J. Schwing, MD, PhD, go2432@wayne.edu
```

The sender block's shape, with the owner's own block as the example, is in the rules below; a
collaborator's letter ends with the collaborator's block in that shape and the cc line.

## Rules every text follows

- Short and direct. The opening line is "I study the application of computer science to improving
  spinal health, and my current work needs ...", finished for each set.
- The affiliation is the Department of General Surgery, Wayne State University School of Medicine
  and the Detroit Medical Center, Detroit, Michigan, USA; never Neurosurgery.
- No text says or implies that a neural network, a model, machine learning, deep learning, AI or
  training is built or used (patent confidentiality). The work is described only as measuring and
  improving how reliably automated image-analysis methods recognise spinal anatomy (which vertebra
  is which, transitional variants included, the variants behind wrong-level errors) across
  modalities, devices and exposures, with results reported as per-image agreement with expert
  labels and confidence intervals. Before pasting, read each text once more for the banned words;
  the 2026-09-26 letters said "neural network" and "train", and nothing of theirs is reused here.
- De-identified imaging only, under Wayne State University's IRB determination HPR 2026-269, with
  HPR 2026-330 the supplement that covers PhysioNet's VinDr-SpineXR.
- The images stay on Wayne State's research computing storage, read only by the owner, never
  redistributed, deleted at the end of the project if the source asks.
- The owner signs any DUA, credits the source and quotes its agreement ID in any publication.
- The subject tag of any email is "[XR/CT Imaging Research]".
- Anything binding (a DUA signature, a fee, a credentialing attestation, a licence checkbox) is the
  owner's hand only; a session drafts text and nothing more.

The sender block used in every email:

```text
Gregory J. Schwing, MD, PhD
Department of General Surgery
Wayne State University School of Medicine / Detroit Medical Center
Detroit, Michigan, USA
go2432@wayne.edu
+1 504-994-0403
```

## Shared text blocks

The portals ask the same things under different labels, so the blocks are written once and each
section says which to paste where.

Project title (one line):

```text
Reliability of automated recognition of vertebral levels on spine radiographs across devices, exposures and anatomical variants
```

Lay summary or aims (the general form; MrOS and SOF have their own below):

```text
Wrong-level spine surgery happens when an image is read and the wrong vertebra is named, most often where the anatomy is transitional (a sixth lumbar vertebra, a sacralised L5, an eleventh or thirteenth rib pair) or the image is degraded. My current work measures, and sets out to improve, how reliably automated image-analysis methods recognise which vertebra is which on radiographs and fluoroscopy, and whether that reliability holds across modalities, imaging devices, exposure settings and anatomical variants. Each image is scored against expert labels and the results are reported as per-image agreement with confidence intervals, by device and by variant. The requested images add devices, exposure recipes and patient populations that the sets already held do not cover.
```

Data security and handling (every form that asks):

```text
The images will be stored on Wayne State University's research computing storage, which is access-controlled and backed up, in a directory readable by me alone. They will not be copied to a laptop, a cloud service or any third party, will not be redistributed, re-identified or linked to any other data about the same people, and will be deleted at the end of the project if the data provider asks. Only de-identified data are requested.
```

IRB status (every form that asks):

```text
Wayne State University's IRB has determined that this work on de-identified imaging is not human-subjects research (HPR 2026-269; supplement HPR 2026-330 for data obtained under PhysioNet agreements). The determination letters can be supplied.
```

Analysis plan (every form that asks; one paragraph):

```text
For each image the vertebrae in field are identified by an automated method and compared with expert labels at the level of each vertebra. The outputs are per-image agreement rates with 95 percent confidence intervals, stratified by imaging device, exposure, projection, patient age group and anatomical variant, and a table of the disagreements by cause. No clinical outcome is studied and no finding about any individual is produced.
```

Credit and publication (where a form asks how the source will be acknowledged):

```text
Any publication will credit the data source by name, cite its paper and quote the agreement or licence identifier under which the images were obtained, and will follow the source's publication rules.
```
