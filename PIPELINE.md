# Pipeline: where every dataset stands

Written by tools/pipeline.py on 2026-10-25 from the records under datasets/ and the tasks of
https://github.com/OpenSpineConsortium/spine-datasets; nobody edits it by hand. A dataset moves left to right: a record's
status and route put it in its column, its history is the steps taken so far, its obstacles are
what stands in the way, and its next step is what whoever holds it does next. The interactive
board is pipeline.html beside this file, served by the docs site. Inside each stage the X-ray
sets (fluoroscopy, video, projections, films) come before CT, the owner's order of 2026-10-21.

| Stage | Datasets |
|---|---|
| [Downloadable now](#downloadable) | 9 |
| [To ask](#to-ask) | 5 |
| [Asked, waiting](#asked) | 27 |
| [Granted, fetch pending](#granted) | 5 |
| [Fetching](#fetching) | 0 |
| [On the grid](#on-grid) | 7 |
| [Held by the owner](#held) | 97 |
| [Needs the owner](#needs-owner) | 13 |
| [Refused](#refused) | 2 |
| [Later](#later) | 1 |

<a id="downloadable"></a>

## Downloadable now (9)

Open on its page; a grid job fetches it.

<details><summary><b>Coronary angiography sets (CADICA, ARCADE, XCAD, AngioCAD)</b> (video, download)</summary>

- What: real fluoroscopy video with the thoracic spine in the background: CADICA 42 patients DICOM at 10 fps, ARCADE 3,000 images, XCAD 1,747 images, AngioCAD 413 patients; heavy contrast, LAO/RAO rotation
- Licence: varies by set
- Status: todo; task open
- Steps so far:
  - 2026-10-21 researched: the only large real thoracic fluoroscopy without a DUA; the thoracic test would be annotated by hand; CADICA (Universidad de Malaga, 42 patients, over 6,000 images), ARCADE (Scientific Data 2024, 3,000 images), XCAD (ICCV 2021, 1,747 images, the link), AngioCAD (413 patients); each set's own licence is read before fetching; CathAction (cathaction, about 500,000 frames, no DUA) is the larger real-fluoroscopy exposure pool found by the sweep of 2026-10-21, with Guide3D (guide3d) beside it
- Next: a grid job onto /rs/rs_grp_oschome/shared/datasets/coronary_angiography/raw by grid/README.md, from the holder's Beethoven session, once the licence on the page is confirmed
- Links: [task #38](https://github.com/OpenSpineConsortium/spine-datasets/issues/38), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/coronary_angiography.json), [source](https://github.com/AISIGSJTU/SSVS)

</details>

<details><summary><b>Neurosurgical Focus: Video (every article CC BY 4.0)</b> (video, download)</summary>

- What: a library of spine-surgery videos PMC serves as MP4; the one checked (PMC13418632, 200 MB, 8 min) shows saved C-arm stills under a tracking overlay, not cine; the rest unscreened
- Licence: CC BY 4.0
- Status: todo; task open
- Steps so far:
  - 2026-10-21 researched: download by browser (a proof-of-work gate stops scripts); screen for live fluoroscopy; AANS reserves TDM/AI-training rights in a footer
  - 2026-10-21 note: audit (#97): seven articles' MP4s already held under external/fluoro_video; the rest unscreened
- Next: screen the remaining articles in a browser for live fluoroscopy and list the ones worth a download in this record; the seven held need nothing
- Links: [task #43](https://github.com/OpenSpineConsortium/spine-datasets/issues/43), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/neurosurgical_focus_video.json), [source](https://thejns.org/page/72659)

</details>

<details><summary><b>VFSS2022 videofluoroscopic swallow frames (TIB)</b> (video, download, aschehr)</summary>

- What: 440 videofluoroscopic swallow frames with instance masks of the bolus and pharynx, the cervical spine in every frame (doi:10.57702/w1ye2nim; Video-TransUNet)
- Licence: to confirm on the page
- Status: todo; task closed
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; open per the listing, licence to confirm on the page; a small labelled cervical fluoroscopy set that the swallow requests (DysphagiaBank, Pittsburgh) do not yet deliver
  - 2026-10-22 note: read on https://service.tib.eu/ldmservice/dataset/vfss2022-dataset: no licence line and no file or resource listed, only the homepage https://github.com/SimonZeng7108/Video-TransUNet and doi:10.57702/w1ye2nim; that repository's Data section says the team's data ethics approval only grants usage and showing on paper, not yet support full release, and gives no download; so there is nothing to fetch and no manifest
- Obstacles:
  - the frames are not released: the authors' ethics approval does not yet allow a full release, and no page gives a licence or a download
- Next: a letter to the authors from letters/TEMPLATE.md, written as letters/vfss2022.md with the corresponding author's address verified on the paper, asking whether the 440 frames can be shared for research and on what terms; the route moves to letter with it
- Links: [task #42](https://github.com/OpenSpineConsortium/spine-datasets/issues/42), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/vfss2022.json), [source](https://service.tib.eu/ldmservice/dataset/vfss2022-dataset)

</details>

<details><summary><b>FracAtlas (Abedeen 2023, Scientific Data)</b> (films, download)</summary>

- What: 4,083 musculoskeletal radiographs from three Bangladeshi hospitals (hand, leg, hip, shoulder), 717 with 922 fracture instances, boxes and masks; the hip and pelvis films show the sacrum and L5
- Licence: CC BY 4.0
- Status: todo; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; a South Asian population and devices the project has not seen
- Next: a grid job onto /rs/rs_grp_oschome/shared/datasets/fracatlas/raw by grid/README.md, from the holder's Beethoven session, once the licence on the page is confirmed
- Links: [task #36](https://github.com/OpenSpineConsortium/spine-datasets/issues/36), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/fracatlas.json), [source](https://figshare.com/articles/dataset/The_dataset/22363012)

</details>

<details><summary><b>Mendeley DDH hip sets (jf3pv98m9g and 4gvcb6gmh2)</b> (films, download)</summary>

- What: infant and child AP pelvis radiographs with developmental dysplasia labels: jf3pv98m9g (Jordan, 354 subjects) and 4gvcb6gmh2 (AV-DDH, 2,417 infant hip films, updated 2026-03); the lumbosacral junction in field at low exposure
- Licence: CC BY 4.0 (to confirm on the page)
- Status: todo; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; the only sizeable pediatric pelvic film source found
- Obstacles:
  - the licence on the page is still to confirm before any fetch
- Next: a grid job onto /rs/rs_grp_oschome/shared/datasets/mendeley_ddh_hips/raw by grid/README.md, from the holder's Beethoven session, once the licence on the page is confirmed
- Links: [task #33](https://github.com/OpenSpineConsortium/spine-datasets/issues/33), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/mendeley_ddh_hips.json), [source](https://data.mendeley.com/datasets/jf3pv98m9g)

</details>

<details><summary><b>VertXNet extra labels for NHANES II (Mo, Papiez, Chen 2023)</b> (films, download)</summary>

- What: labels only, for films already held: 8 landmarks per vertebral body with vertebral identity on the NHANES II cervical and lumbar laterals, and the reference bodies C2 and S1 annotated by radiologists where visible; the Zenodo record 'NHANES II Spinal X-ray with Extra Labels For Reference Vertebral Bodies (C2, S1)', version 1, 2023, named in the Data availability statement of Scientific Reports 14:3341 (doi:10.1038/s41598-023-49923-3)
- Licence: Zenodo, open; licence to confirm on the page (the held record of the same authors is CC BY 4.0)
- Status: todo; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; the manifest's nhanes2_zenodo_landmarks already names Zenodo 10223910 (concept 10145564) by the same authors, whose osteophyte annotation zip is the held 543-film landmark set, so whether the C2 and S1 labels are another file of that record or a sibling record under the concept is to confirm on the page; closes the registry's NHANES gap (C3-C7 and L1-L5 only) at no imaging cost
- Obstacles:
  - the licence on the page is still to confirm before any fetch
- Next: a grid job onto /rs/rs_grp_oschome/shared/datasets/vertxnet_nhanes2_labels/raw by grid/README.md, from the holder's Beethoven session, once the licence on the page is confirmed
- Links: [task #28](https://github.com/OpenSpineConsortium/spine-datasets/issues/28), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/vertxnet_nhanes2_labels.json), [source](https://doi.org/10.1038/s41598-023-49923-3)

</details>

<details><summary><b>IDC `lidc_idri` (tier 2)</b> (ct, download)</summary>

- What: IDC v24 collection lidc_idri (TCIA doi:10.7937/k9/tcia.2015.lo9ql9sx), tier 2 of the anomaly harvest: 997 subjects, about 123.3 GB raw plus screen; chest, abdomen and pelvis
- Licence: CC BY 3.0
- Status: todo; task open
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain after idc_tier2.csv is regenerated; the ranking's refusals: not a regularly spaced 3-D volume 9, slice over 3.0 mm 4
- Next: a grid job onto /rs/rs_grp_oschome/shared/datasets/idc_lidc_idri/raw by grid/README.md, from the holder's Beethoven session, once the licence on the page is confirmed
- Links: [task #48](https://github.com/OpenSpineConsortium/spine-datasets/issues/48), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_lidc_idri.json), [source](https://doi.org/10.7937/k9/tcia.2015.lo9ql9sx)

</details>

<details><summary><b>IDC `prostate_anatomical_edge_cases` (tier 2)</b> (ct, download)</summary>

- What: IDC v24 collection prostate_anatomical_edge_cases (TCIA doi:10.7937/qstf-st65), tier 2 of the anomaly harvest: 131 subjects, about 16.6 GB raw plus screen; pelvis
- Licence: CC BY 4.0
- Status: todo; task open
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain after idc_tier2.csv is regenerated; the ranking's refusals: none
- Next: a grid job onto /rs/rs_grp_oschome/shared/datasets/idc_prostate_anatomical_edge_cases/raw by grid/README.md, from the holder's Beethoven session, once the licence on the page is confirmed
- Links: [task #52](https://github.com/OpenSpineConsortium/spine-datasets/issues/52), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_prostate_anatomical_edge_cases.json), [source](https://doi.org/10.7937/qstf-st65)

</details>

<details><summary><b>Veterinary: canine lateral thoracic radiographs for vertebral heart size (Mendeley ktx4cj55pn)</b> (future, download)</summary>

- What: 152 anonymised lateral thoracic radiographs of dogs; a lateral dog thorax shows T1 to L1 and the VHS method itself counts vertebrae from T4
- Licence: CC BY 4.0 (the Mendeley Data page's licence line, read 2026-10-22)
- Status: todo; task open
- Steps so far:
  - 2026-10-21 researched: the owner's veterinary direction of 2026-10-20; found by the sweep of 2026-10-21; not fetched; the only other public veterinary spine radiograph set found beside the pig CBCT (veterinary_pig_levelcheck)
  - 2026-10-22 note: read the Mendeley Data page ktx4cj55pn: version 1, published 2020-12-10, CC BY 4.0, by Cesar Augusto Flores Duenas, Soila Maribel Gaxiola Camacho and Martin Francisco Montano Gomez; the files are single PNG images with a sha256 each in Mendeley's public API (the first 86 read add up to about 282 MB; the list was cut there, so no total yet); the description counts 156 images in one place and 152 in another; the site footer reserves text and data mining rights for its own content and says the Creative Commons terms apply to open access sets
- Next: a collaborator writes the manifest with python3 tools/dataset_review.py manifest canine_thoracic_vhs --mendeley ktx4cj55pn --version 1 and opens the pull request at fetching
- Links: [task #32](https://github.com/OpenSpineConsortium/spine-datasets/issues/32), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/canine_thoracic_vhs.json), [source](https://data.mendeley.com/datasets/ktx4cj55pn)

</details>


<a id="to-ask"></a>

## To ask (5)

A letter, a form or an application not yet sent.

<details><summary><b>CheXpert and CheXpert Plus (Stanford AIMI)</b> (films, form)</summary>

- What: 224,316 chest radiographs of 65,240 patients, frontal and lateral (CheXpert); CheXpert Plus adds reports and DICOM
- Licence: Stanford AIMI research use agreement, non-commercial
- Status: todo; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; the Stanford AIMI research use agreement, the same portal as INSPECT and Merlin (stanford_aimi_inspect, stanford_aimi_merlin), so the owner's AIMI account would cover it
- Obstacles:
  - gated: Stanford AIMI research use agreement, non-commercial
- Next: fill the form named in letters/chexpert_plus.md with its paragraphs as the purpose, then record the date here
- Links: [task #13](https://github.com/OpenSpineConsortium/spine-datasets/issues/13), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/chexpert_plus.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/chexpert_plus.md), [source](https://stanfordaimi.azurewebsites.net/)

</details>

<details><summary><b>Kaggle bone fracture multi-region X-ray data (bmadushanirodrigo)</b> (films, account, the owner)</summary>

- What: 10,580 radiographs in fractured and non-fractured folders over lower limbs, upper limbs, lumbar spine, hips and knees; 481 MB
- Licence: ODC Public Domain Dedication and Licence (PDDL) in the Kaggle metadata field, while the description names ODC Attribution (ODC-By) 1.0 (both read from Kaggle's dataset API on 2026-10-22); the three source sets' own terms are not read yet
- Status: todo; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; warning: the licence and the images' origin are unstated in what was read (many Kaggle fracture sets are scraped from teaching sites), to confirm on the page; an exposure-diversity pool only, and not to be fetched until its origin is shown to be redistributable
  - 2026-10-22 note: read from Kaggle's dataset API: owner Madushani Rodrigo (bmadushanirodrigo), last updated 2024-04-23, 507,724,147 bytes, 10,580 images; the description says the images were merged from three other Kaggle uploads (Mohan Kumar's bone break upload, Abdelaziz Faramawy's bone_fracture, Harsha Arya's fracture dataset), so this is a copy of copies and its own open licence does not show the films may be passed on
- Obstacles:
  - the three source uploads' own licences and the films' first origin are not read yet; not fetched until they show the films may be passed on
  - the owner's hand afterwards: a Kaggle download needs a Kaggle login and its token
- Next: a collaborator reads the three source uploads' Kaggle pages for their licence and where their films came from, and writes it here; only then the owner's Kaggle fetch
- Links: [task #24](https://github.com/OpenSpineConsortium/spine-datasets/issues/24), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/kaggle_fracture_multiregion.json), [source](https://www.kaggle.com/datasets/bmadushanirodrigo/fracture-multi-region-x-ray-data)

</details>

<details><summary><b>PadChest (BIMCV, Alicante)</b> (films, form)</summary>

- What: 160,868 chest radiographs of 67,625 patients, 109 projections including lateral (about 30 percent) and some oblique; labels include 174 findings
- Licence: research use by request; a licence form on the page
- Status: todo; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; a licence form on the page (research use, by request); European devices and film-era digitised plates, the richest set of non-standard chest projections
- Obstacles:
  - gated: research use by request; a licence form on the page
- Next: fill the form named in letters/padchest.md with its paragraphs as the purpose, then record the date here
- Links: [task #12](https://github.com/OpenSpineConsortium/spine-datasets/issues/12), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/padchest.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/padchest.md), [source](https://bimcv.cipf.es/bimcv-projects/padchest/)

</details>

<details><summary><b>NLST, full (tier 2; 500-person pilot fetched)</b> (ct, owner-only, the owner)</summary>

- What: the National Lung Screening Trial in IDC v24 (TCIA doi:10.7937/tcia.hmq8-j677), full: 24,713 subjects, about 2,305 GB raw plus screen; the 500-person pilot is fetched (the manifest's nlst_pilot, in the harvest)
- Licence: CC BY 4.0
- Status: todo; task open
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f and refused as it stands by the stopping rule (2.3 TB for about 110 T13 people, its only yield, about 1.5 percent single-labeller calls that all need adjudication); no fetch job until the owner lifts that rule; the ranking's refusals: localizer 65,174, slice over 3.0 mm 21,188, under 60 slices 5,209, not a regularly spaced 3-D volume 3,652
- Obstacles:
  - the owner's hand: lifting the stopping rule; no fetch job until then
- Next: the owner's step as the task says; nothing for a collaborator yet
- Links: [task #91](https://github.com/OpenSpineConsortium/spine-datasets/issues/91), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_nlst.json), [source](https://doi.org/10.7937/tcia.hmq8-j677)

</details>

<details><summary><b>ENHANCE.PET 1.6k: whole-/total-body FDG-PET/CT, 1,683 studies (NIfTI)</b> (ct, owner-only, the owner)</summary>

- What: ENHANCE.PET 1.6k, whole- and total-body FDG-PET/CT, 1,683 studies as NIfTI (Science Data Bank doi:10.57760/sciencedb.34150), about 286 GB; multi-centre (Vienna, UC Davis, Careggi, Leipzig, Tuebingen), so Tuebingen may be autoPET and Vienna's healthy controls QUADRA_HC, both tier 1, which the landing dedupe would find; the slice thickness per study is in its CT-details.xlsx, not read
- Licence: CC BY 4.0
- Status: todo; task open
- Steps so far:
  - 2026-10-21 researched: the owner's hand: confirm whether Science Data Bank needs a login and read CT-details.xlsx for slice thickness; no fetch route exists in tools/acquisition_fetch.py for Science Data Bank (planned in the data platform at bf1432f)
- Obstacles:
  - the owner's hand: confirm whether Science Data Bank asks for a login and read CT-details.xlsx; no fetch route exists yet
- Next: the owner's step as the task says; nothing for a collaborator yet
- Links: [task #90](https://github.com/OpenSpineConsortium/spine-datasets/issues/90), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/scidb_enhance_pet_1_6k.json), [source](https://doi.org/10.57760/sciencedb.34150)

</details>


<a id="asked"></a>

## Asked, waiting (27)

Sent; the answer is pending.

<details><summary><b>CM Spine (Zeng et al., Electronics 2024): 208 intraoperative lumbar G-arm images</b> (fluoro, letter)</summary>

- What: 208 anteroposterior lumbar spine images at 1024 x 1024, taken during surgery with a mobile dual-mode G-arm (Geelin500-A), of patients with lumbar disc herniation or vertebral compression fractures, each lumbar vertebra in view annotated by its level, L1 to L5, 537 vertebrae, split 148 and 60 in the paper (Zeng et al., Electronics 2024;13(11):2137); the paper's data statement points to its repository, github.com/zengyuyuyu/Neighbor, whose README linked this Drive file as the set and whose code reads the set as COCO files (train2022, val2022, spine_train.json, spine_val.json); on 2026-10-23 the repository is no longer public and the Drive file does not open, so the set is held by its authors alone
- Licence: none stated: the paper's data statement and its repository's README name no licence, and the repository has no licence file (read 2026-10-23)
- Status: requested; task open
- Steps so far:
  - 2026-10-21 researched: empty in the data platform at bf1432f; the owner's hand: gdown into a scratch directory, inspect, then decide
  - 2026-10-23 note: the link opens the Drive file by the id the data platform gives, so the owner's look is one press; the file was not opened from the session
  - 2026-10-23 note: identified: CM Spine of Zeng et al., Electronics 2024;13(11):2137, whose data statement points to github.com/zengyuyuyu/Neighbor, whose README links this Drive file; 208 intraoperative AP lumbar G-arm images, L1 to L5 annotated; no licence in the paper or the repository; found by checking the owner's list of fluoroscopy sets of 2026-10-23
  - 2026-10-23 researched: the Drive file answers not found to the owner's Google account and the repository is no longer public (its files 404, no public repository on the profile); Software Heritage keeps the code (src only); no public copy, fork or re-upload found by search; the paper's corresponding authors are Erkang Cheng and Bo Song, Institute of Intelligent Machines, Hefei; the letter is rewritten for them and the route is letter
  - 2026-10-23 asked: the letter sent from the owner's mailbox to Cheng and Song, Zeng in copy, and the same day a note to the Electronics editorial office with the two corresponding authors in copy, citing the Data Availability Statement, since the owner's own emails of 2026-09-10 and 2026-09-20 to the three authors about the dead Drive link had no answer; waiting for either; the Drive link is still the owner's to open logged in
- Obstacles:
  - the set was only ever a Google Drive file linked from a repository README, and both are gone from public view; no licence is stated and the paper carries no ethics or consent statement, so the terms and the approval must come from the authors
- Next: waiting for the authors or the editorial office to answer the letter and the note of 2026-10-23; a yes moves the record to granted and the fetch is a Slurm job on the owner's word; the owner still opens the Drive link logged in (Request access if the page offers it)
- Links: [task #8](https://github.com/OpenSpineConsortium/spine-datasets/issues/8), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/cm_spine_drive_file.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/cm_spine_drive_file.md), [source](https://drive.google.com/file/d/1r9wX1802gkU4-EQHMMlyAlEiWXGWLhhJ/view)

</details>

<details><summary><b>Huashan Hospital, Fudan University, intraoperative lumbar films with preoperative CT (Shao et al. 2024)</b> (fluoro, letter)</summary>

- What: 140 living lumbar patients (January 2020 to December 2023) with preoperative CT and intraoperative AP and lateral films of L1 to L5; the device is unnamed; two co-authors are from Shanghai Maestro Surgical Robotics; no data statement
- Licence: not recorded; a data use agreement is the route
- Status: requested; task open
- Steps so far:
  - 2026-10-21 researched: a letter sent 2026-10-21; no record in SchwingNet's registry yet
  - 2026-10-21 asked: Letter sent 2026-10-21 09:40 UTC by the owner to the corresponding author; waiting for the answer.
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #61](https://github.com/OpenSpineConsortium/spine-datasets/issues/61), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/huashan_fudan.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/huashan_fudan.md)

</details>

<details><summary><b>NIT Warangal and NIMS Hyderabad intraoperative C-arm sets (2D-3D-sci-registration)</b> (fluoro, letter)</summary>

- What: nine living patients and 51 AP and lateral C-arm sets in the repository's README (at most 49 unique frames), a Ziehm C-arm, preoperative CT with level-named L1 to L5 centroids; the 60 centroid files and 54 overlay PNGs (the real frame at 8 bits beside a simulated projection) are public on the repository, the CT and raw X-rays available upon reasonable request
- Licence: not recorded; the raw frames and CTs are available upon reasonable request
- Status: requested; task open
- Steps so far:
  - 2026-10-21 researched: a letter sent 2026-10-21; no record in SchwingNet's registry yet
  - 2026-10-21 asked: Letter sent 2026-10-21 09:40 UTC by the owner; waiting for the answer.
  - 2026-10-23 note: the link is the 2D-3D-sci-registration repository the record names, found on 2026-10-23 by its name and description; its page could not be read from the session
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #64](https://github.com/OpenSpineConsortium/spine-datasets/issues/64), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/nit_warangal_nims.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/nit_warangal_nims.md), [source](https://github.com/RaghuGangoluNITW/2D-3D-sci-registration)

</details>

<details><summary><b>PUMCH stitching series (Liu et al., Eur Spine J 2026)</b> (fluoro, letter)</summary>

- What: 43 scoliosis patients, four to six overlapping prone AP exposures each on a Philips Zenition 70; the shift between shots estimated, not recorded; no labels stated; the paper says no datasets were generated or analysed
- Licence: not recorded; a data use agreement is the route
- Status: requested; task open
- Steps so far:
  - 2026-10-21 researched: a letter sent 2026-10-21; no record in SchwingNet's registry yet
  - 2026-10-21 asked: Letter sent 2026-10-21 09:40 UTC by the owner; waiting for the answer.
  - 2026-10-23 note: the link is Liu et al.'s paper (European Spine Journal 2026, PubMed 41910750), found on 2026-10-23 by its journal and subject; its page could not be read from the session
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #63](https://github.com/OpenSpineConsortium/spine-datasets/issues/63), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/pumch_stitching.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/pumch_stitching.md), [source](https://doi.org/10.1007/s00586-026-09872-7)

</details>

<details><summary><b>SX-Stitch intraoperative C-arm series (Li 2024, PUMCH)</b> (fluoro, letter)</summary>

- What: intraoperative C-arm series translated along the spine for stitching
- Licence: not recorded
- Status: requested; task open
- Steps so far:
  - 2026-10-20 asked: request 6 sent 2026-10-20 22:59 UTC by the owner to liuw2@sustech.edu.cn
  - 2026-10-21 researched: request drafted 2026-09-19, never sent; the paper's data statement says no datasets, so success is unlikely
  - 2026-10-21 asked: Letter sent 2026-10-21 09:40 UTC by the owner; waiting for the answer (the paper's data statement makes success unlikely).
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #62](https://github.com/OpenSpineConsortium/spine-datasets/issues/62), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/sx_stitch.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/sx_stitch.md), [source](https://arxiv.org/abs/2409.05681)

</details>

<details><summary><b>Vanderbilt intraoperative THA fluoroscopy (Chan et al., J Arthroplasty 2025)</b> (fluoro, letter)</summary>

- What: 146 living patients, 161 anterior-approach hips, 336 AP frames with eight bony landmarks including midline L5/S1 and both sacroiliac joints, plus 84 cup frames; AP only; the C-arm is not reported; no data statement, code only at github.com/vine-lab-vu/Label-Augmentation (doi:10.1016/j.arth.2025.01.032)
- Licence: not recorded; a data use agreement with Vanderbilt is the route
- Status: requested; task open
- Steps so far:
  - 2026-10-21 researched: a letter sent 2026-10-21; no record in SchwingNet's registry yet
  - 2026-10-21 asked: Letter sent 2026-10-21 12:25 UTC by the owner to the senior authors; waiting for the answer.
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #65](https://github.com/OpenSpineConsortium/spine-datasets/issues/65), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/vanderbilt_tha_fluoro.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/vanderbilt_tha_fluoro.md), [source](https://doi.org/10.1016/j.arth.2025.01.032)

</details>

<details><summary><b>Inselspital Bern dynamic myelography (Piechowiak 2021)</b> (video, letter)</summary>

- What: four pulsed fluoroscopy runs at 7.5 frames a second, the detector moved cranially along the spine during tilting: the only overlapping travelling frames found; the published MP4s are on the grid, the native DICOM is not
- Licence: CC BY 4.0 (the article's videos); native DICOM available on reasonable request under Swiss law
- Status: requested; task open
- Steps so far:
  - 2026-09-26 asked: Request 3 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer. The published videos are already held under CC BY; the request is for the native DICOM.
  - 2026-10-21 researched: the published videos held under CC BY; request 3 for the native DICOM drafted, never sent
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #73](https://github.com/OpenSpineConsortium/spine-datasets/issues/73), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/bern_myelography.json), [source](https://pmc.ncbi.nlm.nih.gov/articles/PMC8463391/)

</details>

<details><summary><b>Bournemouth cervical quantitative fluoroscopy (BORDaR 385)</b> (video, letter)</summary>

- What: 252 lateral flexion and extension sequences from 63 people at 15 fps, 1024 x 1024 16-bit DICOM; the deposit holds the per-frame vertebral corner tracks (.mat, 24 MB) and no pixels
- Licence: CC BY 4.0 (the tracks); README.rtf CC BY-ND
- Status: requested; task open
- Steps so far:
  - 2026-09-26 asked: Request 1 of the 2026-09-26 sheet sent 2026-10-20 by the owner and forwarded to ckaching.cheung@polyu.edu.hk on 2026-10-21 03:57 UTC; waiting for the answer. The letter text is spine-program's and is not in this repository.
  - 2026-10-21 researched: the tracks are on the grid; the DICOM cine is request 1, drafted, never sent; the letter (request 1) was forwarded to ckaching.cheung@polyu.edu.hk on 2026-10-21 03:57 UTC
  - 2026-10-22 note: Branney replied 10:56 UTC: happy to share; checking with Bournemouth's research department about the data-sharing arrangement; will get back
  - 2026-10-24 note: the owner's reply-all of 03:08 UTC in Branney's thread asked about the lumbar OSF deposit and said the request for the cine stands as written; nothing new asked for this set
- Next: wait for Branney's second answer with the arrangement; a Bournemouth data-sharing agreement would be the owner's to sign; then record granted here and go on to the fetch
- Links: [task #70](https://github.com/OpenSpineConsortium/spine-datasets/issues/70), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/bournemouth_cervical_qf.json), [source](https://bordar.bournemouth.ac.uk/385/)

</details>

<details><summary><b>Bournemouth lumbar quantitative fluoroscopy (Breen 2021)</b> (video, letter)</summary>

- What: weight-bearing and recumbent L2 to S1 flexion and extension cine of 127 subjects at 15 fps, 60 degrees at 6 degrees a second; only per-frame angles are public on OSF a27py, while the group's public OSF deposit z2jby holds preproc_224_wb_flex.zip, 1,492,963,815 bytes of weight-bearing flexion frames preprocessed to 224 by 224 pixels, as its name and the repository's sample frames (five vertebral boxes) show, with no licence stated (how_to_get); the full-resolution cine, recumbent and extension included, stays the letter's ask
- Licence: not recorded (OSF a27py holds derived tables only; the image deposit OSF z2jby states no licence)
- Status: requested; task open
- Steps so far:
  - 2026-10-20 asked: Asked for in request 1, sent 2026-10-20 by the owner and forwarded to ckaching.cheung@polyu.edu.hk on 2026-10-21 03:57 UTC; waiting for the answer.
  - 2026-10-21 researched: the only confirmed lumbar cine; asked for in request 1; the letter (request 1) was forwarded to ckaching.cheung@polyu.edu.hk on 2026-10-21 03:57 UTC
  - 2026-10-22 note: Branney replied 10:56 UTC: happy to share; checking with Bournemouth's research department about the data-sharing arrangement; will get back
  - 2026-10-23 researched: the group's public OSF deposit z2jby found: preproc_224_wb_flex.zip (1,492,963,815 bytes) and two .pth files (383,648,577 and 459,107,325 bytes), no licence stated, read through OSF's API from the owner's computer; the image set of dsibournemouth/project-maid (Samaratunga et al., Procedia Computer Science 2025, vol. 270, pp. 2291-2300); the owner read the OSF page and the grant page (UKRI: Budka, August 2022 to February 2023, on Breen's existing QF database, whose participants consented to future research use) the same day, and chose not to chase Branney, who is checking with his research department
  - 2026-10-24 asked: the owner's reply-all of 03:08 UTC in Branney's thread, the original copy list kept, asked whether the OSF deposit z2jby may be used in the meantime and on what terms, and whether it is drawn from the whole L2-S1 database or from a subset; the request for the full-resolution cine stands as written
- Obstacles:
  - the OSF deposit z2jby states no licence: the promoter fetches it only after Bournemouth's grant is recorded as a granted step (manifests/README.md)
- Next: wait for Branney's answer on the data-sharing arrangement and on the OSF deposit (asked 2026-10-24 03:08 UTC); a yes on the deposit is recorded as a granted step, then the manifest from OSF's API and fetching; a Bournemouth data-sharing agreement would be the owner's to sign
- Links: [task #71](https://github.com/OpenSpineConsortium/spine-datasets/issues/71), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/bournemouth_lumbar_qf.json), [source](https://osf.io/a27py/)

</details>

<details><summary><b>DARADIA vertebroplasty video (Kolkata)</b> (video, letter)</summary>

- What: a step-by-step percutaneous vertebroplasty under fluoroscopy on YouTube
- Licence: unknown
- Status: requested; task open
- Steps so far:
  - 2026-09-26 asked: Request 14 of the 2026-09-26 sheet sent 2026-10-20 by the owner to info@daradia.com; waiting for the answer.
  - 2026-10-21 researched: request 14 drafted, never sent
  - 2026-10-21 note: Daradia replied 16:17 UTC: reviewing availability, consent and permissions with Dr Das; will get back; the owner thanked them
- Next: wait for Daradia's answer after Dr Das's review; if none by 2026-11-04, the owner sends one follow-up
- Links: [task #83](https://github.com/OpenSpineConsortium/spine-datasets/issues/83), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/daradia_vertebroplasty.json), [source](https://daradia.com/)

</details>

<details><summary><b>DMX Imaging digital motion X-ray</b> (video, letter)</summary>

- What: lateral lumbar flexion-extension at 30 frames a second, a commercial practice's YouTube video
- Licence: unknown
- Status: requested; task open
- Steps so far:
  - 2026-09-26 asked: Request 7 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer.
  - 2026-10-21 researched: request 7 drafted, never sent
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #77](https://github.com/OpenSpineConsortium/spine-datasets/issues/77), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/dmx_imaging.json), [source](https://www.dmxworks.com/)

</details>

<details><summary><b>ThePainSource (Faubel) fluoroscopy clips</b> (video, letter)</summary>

- What: pain-procedure fluoroscopy clips on YouTube; fax or phone only
- Licence: unknown
- Status: requested; task open
- Steps so far:
  - 2026-10-21 researched: request 13 drafted, never sent; request 13 sent 2026-10-21 04:01 UTC to thepainsource@gmail.com (fax fallback 815-381-7498, to confirm)
  - 2026-10-21 asked: Request 13 sent 2026-10-21 04:01 UTC by the owner to thepainsource@gmail.com (fax fallback 815-381-7498, to confirm); waiting for the answer.
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #82](https://github.com/OpenSpineConsortium/spine-datasets/issues/82), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/faubel_painsource.json), [source](https://www.faubelmd.com/contact-us)

</details>

<details><summary><b>Jefferson Neurosurgery DRG stimulation video (Hines 2020)</b> (video, letter)</summary>

- What: a Neurosurgical Focus Video article with lumbosacral fluoroscopy; the YouTube copy carries a CC BY licence and is on the grid
- Licence: CC BY (YouTube copy); the article text says CC BY-NC-ND while linking CC BY 4.0
- Status: requested; task open
- Steps so far:
  - 2026-09-26 asked: Request 11 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer. The copy is usable now under CC BY.
  - 2026-10-21 researched: request 11 drafted, never sent; the copy is usable now under CC BY
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #80](https://github.com/OpenSpineConsortium/spine-datasets/issues/80), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/jefferson_drg.json), [source](https://doi.org/10.3171/2020.7.FOCVID2034)

</details>

<details><summary><b>Konica Minolta dynamic digital radiography sequences</b> (video, letter)</summary>

- What: flat-panel lumbar motion sequences shown in a marketing video; not fluoroscopy, a separate arm
- Licence: unknown
- Status: requested; task open
- Steps so far:
  - 2026-09-26 asked: Request 10 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer.
  - 2026-10-21 researched: request 10 drafted, never sent; expect an NDA or a pointer to a clinical site
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #79](https://github.com/OpenSpineConsortium/spine-datasets/issues/79), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/konica_ddr.json), [source](https://healthcare.konicaminolta.us/contact-us)

</details>

<details><summary><b>Maastricht UMC+ cervical flexion-extension cine (van Santbrink 2026)</b> (video, letter)</summary>

- What: 112 lateral cervical recordings at 1024 x 1024, 15 fps, uncompressed, with C0 to C7 contours on every frame carrying identity through the sequence
- Licence: available on request under privacy restrictions; a Dutch WMO/GDPR data transfer agreement is expected
- Status: requested; task open
- Steps so far:
  - 2026-09-26 asked: Request 2 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer. The SchwingNet record of 2026-10-21 still says drafted, so confirm the date in the owner's Sent folder.
  - 2026-10-21 researched: request 2 drafted, never sent; on request only
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #72](https://github.com/OpenSpineConsortium/spine-datasets/issues/72), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/maastricht_cervical.json), [source](https://pmc.ncbi.nlm.nih.gov/articles/PMC13024292/)

</details>

<details><summary><b>Mayfield Brain and Spine kyphoplasty alignment series</b> (video, letter)</summary>

- What: two native DICOM C-arm alignment series played in OsiriX on YouTube: AP 98 frames, lateral 65 frames; a birth date is burned in
- Licence: unknown
- Status: requested; task open
- Steps so far:
  - 2026-09-26 asked: Request 6 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer.
  - 2026-10-21 researched: request 6 drafted, never sent
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #76](https://github.com/OpenSpineConsortium/spine-datasets/issues/76), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/mayfield_kyphoplasty.json), [source](https://www.youtube.com/watch?v=fkRFgkESCgQ)

</details>

<details><summary><b>Manual Therapy Foundation of India lumbar coupling video</b> (video, letter)</summary>

- What: AP lumbar side-bending with rotation under video fluoroscopy, a view the project lacks
- Licence: unknown
- Status: requested; task open
- Steps so far:
  - 2026-09-26 asked: Request 12 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer.
  - 2026-10-21 researched: request 12 drafted (address on the site, not decoded), never sent
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #81](https://github.com/OpenSpineConsortium/spine-datasets/issues/81), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/mtfi_lumbar_coupling.json), [source](https://www.mtfi.net/)

</details>

<details><summary><b>IRI-VFI: pediatric interventional radiology image sequences (Chongqing)</b> (video, letter)</summary>

- What: 95,308 real fluoroscopy images in 1,357 sequences with the lumbar spine in field; pediatric, DSA subtraction frames to be excluded
- Licence: not recorded
- Status: requested; task open
- Steps so far:
  - 2026-10-21 researched: a grain calibration target and an unlabelled pool; 150 to 200 frames would be annotated as a test set; the record is IRI-VFI on IEEE DataPort (doi:10.21227/v4kg-zp42, 1,357 sequences, 95,308 images, angiography, fluoroscopy and subtraction, Children's Hospital of Chongqing Medical University, ChiCTR2200058971); its licence line was not readable from the cloud session
  - 2026-10-21 asked: Letter sent 2026-10-21 19:54 UTC by the owner to the paper's two corresponding authors, since the files were not reachable through IEEE DataPort; waiting for the answer.
- Obstacles:
  - the authors' answer and their terms; any data use agreement is the owner's hand
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #21](https://github.com/OpenSpineConsortium/spine-datasets/issues/21), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/pediatric_iri.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/pediatric_iri.md), [source](https://ieee-dataport.org/documents/iri-vfi-dataset)

</details>

<details><summary><b>Pittsburgh videofluoroscopic swallow corpus (Sejdic, Coyle)</b> (video, letter)</summary>

- What: about 1,500 lateral swallow clips at 30 fps captured by video card, 265 patients and 70 volunteers on two machines
- Licence: by request
- Status: requested; task open
- Steps so far:
  - 2026-09-26 asked: Request 4 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer.
  - 2026-10-21 researched: request 4 drafted, never sent; a Pitt data use agreement expected
  - 2026-10-21 note: Sejdic replied 18:57 UTC: no longer at Pitt, cannot share; Pitt's IRB never covered sharing; 'maybe Jim knows' (James Coyle, copied)
  - 2026-10-23 note: truth corrected from the paper's methods (PMC8560570): the points include C3's two corners, labelled on only the first three frames of each subject, which the old line left out
- Obstacles:
  - Pittsburgh's IRB for the swallow study never covered sharing the recordings (Sejdic, 2026-10-21); the corpus is Coyle's to answer for now
- Next: wait for James Coyle's answer; if none by 2026-10-28, the owner sends one short follow-up to him alone
- Links: [task #74](https://github.com/OpenSpineConsortium/spine-datasets/issues/74), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/pittsburgh_swallow.json), [source](https://doi.org/10.1016/j.media.2021.102218)

</details>

<details><summary><b>The Procedure Guide (Puranik) live fluoroscopy clips</b> (video, form)</summary>

- What: four YouTube clips of live fluoroscopy under a CC BY-NC-SA 4.0 site licence whose reach to the clips is unstated
- Licence: CC BY-NC-SA 4.0 (site)
- Status: requested; task open
- Steps so far:
  - 2026-10-21 researched: request 9 drafted (contact form, no e-mail), never sent
  - 2026-10-21 asked: Request 9 submitted 2026-10-21 01:25 UTC through the contact form at theprocedureguide.com/contact; waiting for the answer.
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #78](https://github.com/OpenSpineConsortium/spine-datasets/issues/78), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/procedure_guide.json), [source](https://theprocedureguide.com/contact)

</details>

<details><summary><b>Seattle Science Foundation spine videos</b> (video, letter)</summary>

- What: 12 YouTube surgical teaching videos with live C-arm feeds (spinal cord stimulator trials, kyphoplasty); re-encodes on the grid
- Licence: unknown; embedding disabled
- Status: requested; task open
- Steps so far:
  - 2026-09-26 asked: Request 5 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer.
  - 2026-10-21 researched: request 5 drafted, never sent; one request covers all 12
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #75](https://github.com/OpenSpineConsortium/spine-datasets/issues/75), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/seattle_science_foundation.json), [source](https://www.seattlesciencefoundation.org/)

</details>

<details><summary><b>Harms Study Group registries (adolescent idiopathic scoliosis and other pediatric spinal deformity)</b> (films, letter)</summary>

- What: the Harms Study Group's prospective multicentre registries of pediatric spinal deformity, run with the Setting Scoliosis Straight Foundation: the adolescent idiopathic scoliosis registry, which the group calls the largest AIS database, with cerebral palsy, Scheuermann's kyphosis and Marfan syndrome registries beside it and a quality improvement registry; about twenty years of surgical cases from 37 member surgeons; whether the standing radiographs themselves are shared, or only the measurements taken from them, is not stated on the site and is what the request asks
- Licence: not recorded; the Database User Program page lists a research tool at USD 5,000 a year (database user access and hosting) and custom research database building at USD 50,000 to 150,000; the terms of a data release are not on the site
- Status: requested; task open
- Steps so far:
  - 2026-10-23 researched: named by Ali Uneri (Johns Hopkins) in his answer on LevelCheck, with an offer to introduce the owner to the group's administrative team; the site read the same day gives the registries, 37 members, the Database User Program's fees and the contact addresses, and says nothing about sharing images
  - 2026-10-23 note: the owner sent the reply to Uneri at 16:56 UTC on 2026-10-23, thanking him, letting LevelCheck go and accepting the introduction to the Harms Study Group's administrative team, with the question whether the radiographs themselves can be shared with a research user; waiting for the introduction
  - 2026-10-23 note: Uneri introduced the owner to Michelle Marks, the group's Executive/Research Director, the same day, and her welcome at 20:10 UTC asked for details of the study and the imaging needs
  - 2026-10-23 asked: letters/hsg_ais_registry.md sent 20:24 UTC as the owner's reply-all to Michelle Marks (mmarks@ssshsg.org), Uneri in copy, the greeting adapted to her: whether the de-identified standing films with their instrumented levels and measurements can be shared with a research user, and on what terms; nothing accepted, the fee and any agreement left to the owner
- Obstacles:
  - whether the registry shares the radiographs, or only measurements, is unknown
  - the Database User Program's fee (USD 5,000 a year) and any agreement are the owner's decision and hand
- Next: wait for Michelle Marks' review (the request went 2026-10-23 20:24 UTC); record her answer here as granted or refused, with the terms, which are the owner's to decide and sign; if nothing has come by 2026-11-06, the owner follows up in the same thread
- Links: [task #273](https://github.com/OpenSpineConsortium/spine-datasets/issues/273), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/hsg_ais_registry.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/hsg_ais_registry.md), [source](https://hsg.settingscoliosisstraight.org/database-user-program/)

</details>

<details><summary><b>MIMIC-CXR and MIMIC-CXR-JPG (PhysioNet)</b> (films, agreement, the owner)</summary>

- What: 377,110 chest radiographs of 227,835 studies, 65,379 patients, Beth Israel Deaconess; frontal and lateral views, the lateral share roughly a third (to confirm from the metadata CSV)
- Licence: PhysioNet credentialed health data licence; to confirm on the page
- Status: requested; task open
- Steps so far:
  - 2026-10-09 note: the owner's PhysioNet credentialed access was approved 2026-10-09; only this dataset's agreement click remains
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; PhysioNet credentialed access (CITI training and the data use agreement, as VinDr-SpineXR needed); the largest source of lateral chest films, hence of thoracic spine laterals, free of charge once credentialed
  - 2026-10-21 asked: the owner's credentialed agreement is on file; PhysioNet reviews his CITI course record before the files open
- Obstacles:
  - PhysioNet's review of the owner's CITI course record
  - the IRB office is asked whether HPR 2026-330 covers it before any image is read
- Next: wait for PhysioNet to approve the CITI course record; then the owner submits the grid fetch (SchwingNet grid/run-xray-chain.sh --credentialed --only mimic_cxr_jpg)
- Links: [task #15](https://github.com/OpenSpineConsortium/spine-datasets/issues/15), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/mimic_cxr.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/mimic_cxr.md), [source](https://physionet.org/content/mimic-cxr/2.1.0/)

</details>

<details><summary><b>TVGH ankylosing spondylitis cervical and lumbar spine films</b> (films, letter)</summary>

- What: paired cervical and lumbar spine radiograph series in DICOM from Taipei Veterans General Hospital, in patients with ankylosing spondylitis; counts not shown to a visitor
- Licence: not recorded
- Status: requested; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21 on the Taiwan medical data portal (data.dmc.nycu.edu.tw, data set d08); the portal lists the set and shows no files to a visitor
  - 2026-10-21 asked: Letter sent 2026-10-21 19:56 UTC by the owner to the contacts the portal names at Taipei Veterans General Hospital; it also asks about TVGH-SpineXR; waiting for the answer.
- Obstacles:
  - the hospital's answer and its terms; any data use agreement is the owner's hand
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #108](https://github.com/OpenSpineConsortium/spine-datasets/issues/108), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/tvgh_as_spine_xray.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/tvgh_as_spine_xray.md), [source](https://data.dmc.nycu.edu.tw/dataset/d08-x-ray)

</details>

<details><summary><b>TVGH-SpineXR</b> (films, letter)</summary>

- What: a Taiwanese spine radiograph set behind a login
- Licence: not recorded
- Status: requested; task open
- Steps so far:
  - 2026-10-21 researched: 403 at a login; access never requested; the record is on IEEE DataPort (doi:10.21227/x6bb-7r75) with T1-L5 per-vertebra level labels, masks and end-plates per its description, never seen
  - 2026-10-21 asked: Letter sent 2026-10-21 19:54 UTC by the owner to the senior author at National Taiwan University; the letter of 19:56 UTC to Taipei Veterans General Hospital about its ankylosing spondylitis films asks about this set too; waiting for the answer.
- Obstacles:
  - the authors' answer and their terms; any data use agreement is the owner's hand
- Next: wait for the answer; when it comes, record it here as granted or refused and go on to the fetch
- Links: [task #14](https://github.com/OpenSpineConsortium/spine-datasets/issues/14), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/tvgh_spinexr.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/tvgh_spinexr.md), [source](https://ieee-dataport.org/documents/tvgh-spinexr)

</details>

<details><summary><b>VinDr-CXR (PhysioNet)</b> (films, agreement, the owner)</summary>

- What: 18,000 adult frontal chest radiographs from two Vietnamese hospitals with radiologist boxes; the same institutions and devices as VinDr-SpineXR
- Licence: PhysioNet credentialed health data licence; to confirm on the page
- Status: requested; task open
- Steps so far:
  - 2026-10-09 note: the owner's PhysioNet credentialed access was approved 2026-10-09; only this dataset's agreement click remains
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; PhysioNet credentialed access, the route VinDr-SpineXR already took
  - 2026-10-21 asked: the owner's credentialed agreement is on file; PhysioNet reviews his CITI course record before the files open
- Obstacles:
  - PhysioNet's review of the owner's CITI course record
  - the IRB question as for MIMIC-CXR
- Next: wait for PhysioNet to approve the CITI course record; then the owner submits the grid fetch (SchwingNet grid/run-xray-chain.sh --credentialed --only vindr_cxr)
- Links: [task #16](https://github.com/OpenSpineConsortium/spine-datasets/issues/16), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/vindr_cxr.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/vindr_cxr.md), [source](https://physionet.org/content/vindr-cxr/1.0.0/)

</details>

<details><summary><b>AbdomenAtlas 2.0 Mini (10,135 CT)</b> (ct, letter)</summary>

- What: AbdomenAtlas 2.0 Mini, 10,135 CT in 21 tars, about 620 GB on Hugging Face (tree read 2026-09-24); no card, no metadata; the AbdomenAtlas line aggregates public sets, 3.0 Mini (9,262) is already fetched and the other about 873 are unidentified
- Licence: CC BY-NC-SA 4.0
- Status: requested; task open
- Steps so far:
  - 2026-10-21 researched: the owner's hand: an id map against AbdomenAtlas 3.0 Mini first, since there is no card and no metadata (planned in the data platform at bf1432f)
  - 2026-10-22 note: letter drafted (letters/hf_abdomenatlas2_0_mini.md) to Zongwei Zhou at Johns Hopkins asking for the case list against 3.0 Mini; not sent, waiting for the owner's go
  - 2026-10-22 asked: letter sent by the owner at 16:14 UTC to Zongwei Zhou (zzhou82@jh.edu), go2432@wayne.edu in copy, asking for the case list against 3.0 Mini
- Obstacles:
  - waiting for the case list; then a grid job fetching only the cases not already held, on the owner's word
- Next: wait for Professor Zhou's answer; with the case list, a grid job fetches only the cases not already held, on the owner's word
- Links: [task #89](https://github.com/OpenSpineConsortium/spine-datasets/issues/89), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/hf_abdomenatlas2_0_mini.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/hf_abdomenatlas2_0_mini.md), [source](https://huggingface.co/datasets/AbdomenAtlas/AbdomenAtlas2.0Mini)

</details>


<a id="granted"></a>

## Granted, fetch pending (5)

The source said yes; the fetch is next.

<details><summary><b>Radiopaedia spine cases</b> (video, agreement, the owner)</summary>

- What: every case whose body system is Spine (and musculoskeletal cases whose images show the spine), in every modality, with the reference articles on vertebral numbering and transitional vertebrae; the seven fluoroscopy cases first identified (rID 24796, rID 90103, rID 21585 and four fluoroscopy-guided injection cases) are within it; the count is Radiopaedia's to state at approval
- Licence: CC BY-NC-SA 3.0 (the site); ML use by application
- Status: granted; task open
- Steps so far:
  - 2026-10-21 researched: applied for on 2026-10-21: the non-commercial machine-learning licence agreement (v1.3) signed and submitted through Radiopaedia's SignNow form at 03:36 UTC, fee USD 250 paid (receipt 1967-5247), checklist NO/NO/NO, pending Radiopaedia's countersignature; the form cut the Project Aims and Radiopaedia Content answers off, so the full text goes to license@radiopaedia.org in a follow-up; any model that reads these cases is a Model under the agreement (release only under CC BY-NC-SA, no commercial use), which is the lawyer's question before training on them
  - 2026-10-21 asked: Licence application signed and submitted 2026-10-21 03:36 UTC by the owner, fee paid (receipt 1967-5247); pending Radiopaedia's countersignature; the full text of two cut-off fields goes to license@radiopaedia.org.
  - 2026-10-21 note: the full text of the two cut-off fields went to license@radiopaedia.org at 04:00 UTC; Radiopaedia's Image License Manager acknowledged at 04:33 UTC and will add it to the application and write once it is reviewed
  - 2026-10-23 granted: Murphy approved the application as submitted for the first phase at 03:17 UTC; the copy with the approval ID follows from Juliette; no export or DICOM, the images are collected from the site at a gentle rate (clause 3)
- Obstacles:
  - the copy with the approval ID has not arrived yet
  - how the spine cases are collected within clause 3's rate is the owner's decision; what the agreement says about anything built from the cases is a lawyer's question before any use beyond the first phase
- Next: wait for Juliette's copy with the approval ID and record it here; then the owner decides how the spine cases are collected within clause 3's rate
- Links: [task #84](https://github.com/OpenSpineConsortium/spine-datasets/issues/84), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/radiopaedia.json), [source](https://radiopaedia.org/licence)

</details>

<details><summary><b>VinDr-PCXR (PhysioNet)</b> (films, agreement, the owner)</summary>

- What: 9,125 pediatric frontal chest radiographs from the VinDr hospitals with radiologist boxes; the only sizeable public pediatric spine-bearing radiograph source found
- Licence: PhysioNet Restricted Health Data License 1.5.0 (no CITI review needed)
- Status: granted; task open
- Steps so far:
  - 2026-10-09 note: the owner's PhysioNet credentialed access was approved 2026-10-09; only this dataset's agreement click remains
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; PhysioNet credentialed access, the route VinDr-SpineXR already took
  - 2026-10-21 granted: the owner's restricted data use agreement is on file; the Files section lists the image folders and the annotation CSVs
  - 2026-10-21 fetching: Slurm chain submitted 2026-10-21 21:35 UTC by the SchwingNet thread through Beethoven's gate word (schwingnet fetch vindr_pcxr, SchwingNet 5ecce95) with the owner's PhysioNet credentials from ~/.netrc: fetch 40697734, then bank and ingest 40697735, then catalog 40697736 (each afterany); about 30 GB, about two hours, landing at /rs/rs_grp_oschome/go2432/data/vindr_pcxr/raw
  - 2026-10-22 note: Fetch job 40697734 stopped after 8 seconds with no file: PhysioNet answered 401, then 403 to the login wget sent from the grid's netrc, so the login held and the account was refused this version's files. A second fetch through the same gate word, job 40702518 at 04:23 UTC on SchwingNet ff9c743, stopped before any request: the netrc check added in SchwingNet #83 says the file is not one it can read. The record goes back to granted until a fetch brings files.
  - 2026-10-22 note: Fetch job 40702657 at 05:45 UTC, with SchwingNet #102's netrc reader, read the grid's netrc and stopped after 5 seconds: PhysioNet answered 401, then 403, so the netrc obstacle is gone and the account's access to VinDr-PCXR 1.0.0 is the one left.
- Obstacles:
  - PhysioNet refused the files to the account the grid's netrc names (401 then 403, job 40697734): either that account's agreement for VinDr-PCXR 1.0.0 is not in effect yet, or the netrc names a different PhysioNet account from the one that holds it.
- Next: The owner confirms on https://physionet.org/content/vindr-pcxr/1.0.0/, signed in as the account the grid's netrc names, that the Files section lists the files (or completes the agreement it asks for); then send the gate word schwingnet-fetch-vindr_pcxr again and check the copy with sha256sum -c SHA256SUMS.txt before recording fetched.
- Links: [task #17](https://github.com/OpenSpineConsortium/spine-datasets/issues/17), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/vindr_pcxr.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/vindr_pcxr.md), [source](https://physionet.org/content/vindr-pcxr/1.0.0/)

</details>

<details><summary><b>CADS CT (unique cases)</b> (ct, agreement, the owner)</summary>

- What: 753 CTs; a gated anomaly-harvest collection (group B7)
- Licence: a data use agreement (non-commercial)
- Status: granted; task open
- Steps so far:
  - 2026-10-21 researched: access granted on the owner's Hugging Face account on 2026-10-21; not yet fetched
  - 2026-10-21 granted: Access granted on the owner's Hugging Face account 2026-10-21; not yet fetched.
- Obstacles:
  - the owner's hand: the word for the job; the token in ~/.hf/token.env on the owner's grid account
- Next: the fetch: a grid job by grid/README.md, with what the result line says the fetch needs
- Links: [task #86](https://github.com/OpenSpineConsortium/spine-datasets/issues/86), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/cads.json), [source](https://huggingface.co/datasets/mrmrx/CADS-dataset)

</details>

<details><summary><b>CT-RATE chest CT</b> (ct, agreement, the owner)</summary>

- What: 25,692 CT of 21,304 patients; a gated anomaly-harvest collection (group B7)
- Licence: a data use agreement (non-commercial)
- Status: granted; task open
- Steps so far:
  - 2026-10-21 researched: access granted on the owner's Hugging Face account on 2026-10-21 (the dataset page shows the gate accepted); not yet fetched: 21.3 TB, so the fetch waits for the owner's word on how much Ceph space it may take
  - 2026-10-21 granted: Access granted on the owner's Hugging Face account 2026-10-21; the fetch (21.3 TB) waits for the owner's word on how much Ceph space it may take.
  - 2026-10-21 note: the full 21.3 TB download is off, since it cannot fit on the shared volume, and X-ray sets come before CT in every queue (the owner, 2026-10-21); a subset, if ever, is a later decision of the owner's
- Obstacles:
  - 21.3 TB does not fit on the shared volume: the full set is not fetched (the owner, 2026-10-21)
  - the token in ~/.hf/token.env on the owner's grid account, for any subset the owner later names
- Next: no fetch for now; a subset only on the owner's word, naming the series and the size
- Links: [task #85](https://github.com/OpenSpineConsortium/spine-datasets/issues/85), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/ct_rate.json), [source](https://huggingface.co/datasets/ibrahimhamamci/CT-RATE)

</details>

<details><summary><b>RSNA abdominal trauma CT (RATIC)</b> (ct, agreement, the owner)</summary>

- What: 3,147 patients, 4,711 series; a gated anomaly-harvest collection (group B7)
- Licence: a data use agreement (non-commercial)
- Status: granted; task open
- Steps so far:
  - 2026-10-21 researched: an RSNA download link (a presigned zip, valid until 2026-10-28 02:38 UTC) received by the owner on 2026-10-21 after accepting RSNA's terms; the fetch command was given to the owner (curl -C - into DEST on reqp --qos=requeue); job id not yet recorded
  - 2026-10-21 granted: RSNA's terms accepted 2026-10-21; a presigned link valid until 2026-10-28 02:38 UTC is in the owner's ~/.rsna/ratic_link; job id not yet recorded.
- Obstacles:
  - the owner's hand: the sbatch from the owner's grid account before the link expires; the job id goes in the record
- Next: the fetch: a grid job by grid/README.md, with what the result line says the fetch needs
- Links: [task #87](https://github.com/OpenSpineConsortium/spine-datasets/issues/87), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/rsna_ratic.json), [source](https://mira.rsna.org/dataset/5)

</details>


<a id="fetching"></a>

## Fetching (0)

A grid job is submitted or running.


<a id="on-grid"></a>

## On the grid (7)

Under /rs/rs_grp_oschome/shared/datasets/<id>/raw with checksums.

<details><summary><b>CADICA invasive coronary angiography sequences (Mendeley p9bpx9ctcv)</b> (video, download)</summary>

- What: invasive coronary angiography videos of 42 patients as PNG frames (512 x 512 pixels, 10 frames per second, 1 to 151 frames a video) from a Siemens Artis Zee at Hospital Universitario Virgen de la Victoria, Malaga, Spain, with lesion boxes and selected clinical features (Jimenez-Partinen et al., Expert Systems 2024)
- Licence: CC BY 4.0 (Creative Commons Attribution 4.0 International, as Mendeley Data's public API gives it for version 5, 2026-10-21)
- Status: fetched; task closed
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; open on Mendeley Data under CC BY 4.0; real C-arm sequences from a Siemens Artis Zee with the dose stated (5 to 50 mGy a projection); version 5 holds one zip of 3,076,112,179 bytes with the sha256 Mendeley's public API gives
  - 2026-10-21 fetching: manifest ready; the promoter fetches after merge
  - 2026-10-21 fetched: on the grid at /rs/rs_grp_oschome/shared/datasets/cadica/raw, 1 files, 3076112179 bytes, sha256-checked, promoter job 40696334
- Next: not written yet
- Links: [task #109](https://github.com/OpenSpineConsortium/spine-datasets/issues/109), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/cadica.json), [source](https://data.mendeley.com/datasets/p9bpx9ctcv)

</details>

<details><summary><b>Fraiwan spine X-ray set (Mendeley xkt857dsxk)</b> (films, download, aschehr)</summary>

- What: 338 subjects' spine radiographs from King Abdullah University Hospital, Jordan, in three classes (scoliosis, spondylolisthesis, normal), original and resized (Fraiwan et al. 2022); views to confirm on the page
- Licence: CC BY 4.0 (Creative Commons Attribution 4.0 International, as the Mendeley page's licence line reads for version 1, 2026-10-21)
- Status: fetched; task closed
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; new people from a Middle-Eastern centre, with spondylolisthesis cases
  - 2026-10-21 note: licence read on the Mendeley page: CC BY 4.0; version 1 (DOI 10.17632/xkt857dsxk.1) holds six zip files, the original-size images and five resized copies, 85,596,630 bytes, each with the sha256 the page's API gives
  - 2026-10-21 fetching: Slurm job 40689730 submitted from the holder's Beethoven session, onto /rs/rs_grp_oschome/shared/datasets/fraiwan_spine_xray/raw (grid/README.md)
  - 2026-10-21 note: Slurm job 40689730 stopped at its first step: mkdir /rs/rs_grp_oschome/shared/datasets was refused (Permission denied); nothing was fetched or written
  - 2026-10-21 fetching: manifest ready; the promoter fetches it after merge
  - 2026-10-21 fetched: on the grid at /rs/rs_grp_oschome/shared/datasets/fraiwan_spine_xray/raw, 6 files, 85596630 bytes, sha256-checked, promoter job 40696334
- Next: not written yet
- Links: [task #31](https://github.com/OpenSpineConsortium/spine-datasets/issues/31), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/fraiwan_spine_xray.json), [source](https://data.mendeley.com/datasets/xkt857dsxk)

</details>

<details><summary><b>MTDDH paediatric pelvic X-rays with hip dysplasia key points (Qi et al., Science Data Bank 2025)</b> (films, download)</summary>

- What: 2,156 pelvic radiographs of children aged 5 to 40 months, one film per child, from the Children's Hospital of Zhejiang University School of Medicine and Hebei Children's Hospital, in two parts: 1,250 (781 girls, 469 boys, mean age 14.6 months) annotated with four regions for image quality (both obturator foramina and both ilia) and eight key points for developmental dysplasia of the hip, as JPG in three split folders with JSON annotations for the first two, and 906 (558 girls, 384 boys, mean age 14.3 months) with the eight key points alone, as PNG with COCO-format annotations; file names randomised by the authors; released with the hospital's ethics approval 2023-IRB-0287-P-01, consent waived, anonymised (Qi, Jiao, Li and others, Scientific Data 2025, doi:10.1038/s41597-025-05146-x; Science Data Bank doi:10.57760/sciencedb.24372, V1, issued 2025-04-29, 4,053,482,052 bytes in three files: JPG_DICOM.rar, MTDDH.zip and code.zip); the lumbosacral junction is in the field of a pelvic film, as in the Mendeley DDH hip sets
- Licence: CC BY 4.0 (DataCite's record of the DOI, read 2026-10-23)
- Status: fetched; task closed
- Steps so far:
  - 2026-10-23 researched: found by the search of the Chinese dataset hosts on 2026-10-23 (Science Data Bank, through its search page and then DataCite's record of the DOI); not fetched; CC BY 4.0, 4.05 GB in three files; the owner's hand: confirm whether Science Data Bank asks for a login, and a fetch route for Science Data Bank is written first
  - 2026-10-23 researched: the owner opened the page: downloads with no login; the three files, their sizes, md5s and download links read through the site's public API from the owner's computer; the paper read (Scientific Data 2025); the authors' older figshare copy found as a fallback; the fetch waits on the owner's word for the manifest
  - 2026-10-23 fetching: manifest ready; the promoter fetches after merge (the owner gave the word for one set of 4.05 GB at 19:54 UTC)
  - 2026-10-24 fetched: on the grid at /rs/rs_grp_oschome/shared/datasets/scidb_mtddh/raw, 3 files, 4053482052 bytes, sha256-checked, promoter job 40754479
- Next: not written yet
- Links: [task #324](https://github.com/OpenSpineConsortium/spine-datasets/issues/324), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/scidb_mtddh.json), [source](https://www.scidb.cn/en/detail?dataSetId=c088644bd0b2406eb49830ad447c17fb)

</details>

<details><summary><b>LumVBCanSeg lumbar CT (185, ShengJing Hospital)</b> (ct, download, Gregory-Schwing-MD-PhD)</summary>

- What: LumVBCanSeg lumbar CT, 185 subjects, ShengJing Hospital, Zenodo 8181250 published 2023-07-25, about 10.1 GB
- Licence: CC BY 4.0
- Status: fetched; task closed
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain
  - 2026-10-22 fetching: manifest ready from Zenodo's file list (1 files, 10.08 GB, md5 each); the licence on the page reads CC BY 4.0; the promoter fetches after merge
  - 2026-10-22 fetched: on the grid at /rs/rs_grp_oschome/shared/datasets/zenodo_lumvbcanseg/raw, 1 files, 10075438693 bytes, sha256-checked, promoter job 40702867
- Next: not written yet
- Links: [task #55](https://github.com/OpenSpineConsortium/spine-datasets/issues/55), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/zenodo_lumvbcanseg.json), [source](https://zenodo.org/records/8181250)

</details>

<details><summary><b>MedPelvis3D pelvic CT (99, PLA General Hospital)</b> (ct, download, Gregory-Schwing-MD-PhD)</summary>

- What: MedPelvis3D pelvic CT, 99 subjects, PLA General Hospital, Zenodo 21757686 published 2026-08-02, about 15.1 GB
- Licence: CC BY 4.0
- Status: fetched; task closed
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain
  - 2026-10-22 fetching: manifest ready from Zenodo's file list (100 files, 31.35 GB, md5 each); the licence on the page reads CC BY 4.0; the promoter fetches after merge
  - 2026-10-22 fetched: on the grid at /rs/rs_grp_oschome/shared/datasets/zenodo_medpelvis3d/raw, 100 files, 31351310903 bytes, sha256-checked, promoter job 40702867
- Next: not written yet
- Links: [task #56](https://github.com/OpenSpineConsortium/spine-datasets/issues/56), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/zenodo_medpelvis3d.json), [source](https://zenodo.org/records/21757686)

</details>

<details><summary><b>International TMTV Benchmark, lymphoma FDG PET/CT (60)</b> (ct, download, Gregory-Schwing-MD-PhD)</summary>

- What: International TMTV Benchmark, lymphoma FDG PET/CT, 60 subjects, Zenodo 13255214 published 2024-08-07, about 6.9 GB; the NIfTI CTs on the PET grid are over 3 mm, so the DICOM is wanted
- Licence: CC BY 4.0
- Status: fetched; task closed
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain once a zipped-DICOM convert route is written
  - 2026-10-22 fetching: manifest ready from Zenodo's file list (5 files, 6.85 GB, md5 each); the licence on the page reads CC BY 4.0; the promoter fetches after merge
  - 2026-10-22 fetched: on the grid at /rs/rs_grp_oschome/shared/datasets/zenodo_tmtv_benchmark/raw, 5 files, 6846084599 bytes, sha256-checked, promoter job 40702867
- Next: not written yet
- Links: [task #57](https://github.com/OpenSpineConsortium/spine-datasets/issues/57), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/zenodo_tmtv_benchmark.json), [source](https://zenodo.org/records/13255214)

</details>

<details><summary><b>UniToChest chest CT (623 patients; distributed as slices)</b> (ct, download, Gregory-Schwing-MD-PhD)</summary>

- What: UniToChest chest CT, 623 patients, distributed as slices, Zenodo 5797912 published 2021-12-22, about 84 GB
- Licence: CC BY 4.0
- Status: fetched; task closed
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain
  - 2026-10-22 fetching: manifest ready from Zenodo's file list (2 files, 84.07 GB, md5 each); the licence on the page reads CC BY 4.0; the promoter fetches after merge
  - 2026-10-22 fetched: on the grid at /rs/rs_grp_oschome/shared/datasets/zenodo_unitochest/raw, 2 files, 84067545368 bytes, sha256-checked, promoter job 40702868
- Next: not written yet
- Links: [task #58](https://github.com/OpenSpineConsortium/spine-datasets/issues/58), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/zenodo_unitochest.json), [source](https://zenodo.org/records/5797912)

</details>


<a id="held"></a>

## Held by the owner (97)

On the grid by the owner's own chain, not the promoter; grid_path says where.

<details><summary><b>C-ArmLSpine (Zhang et al., Medical Image Analysis 2024)</b> (fluoro, download)</summary>

- What: 149 lumbar intraoperative cases from one mobile C-arm: 299 AP and lateral spot frames, an intraoperative CBCT of every case from the same device, and the raw CBCT projection sweeps of two cases (case39 and case134, 301 frames each, rotational); 59,609 DICOM files in the release (Zenodo 22768651)
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/carmlspine, fetched from Zenodo with the zip's md5 checked on 2026-09-21, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
- Next: not written yet
- Links: [task #261](https://github.com/OpenSpineConsortium/spine-datasets/issues/261), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/carmlspine.json), [source](https://zenodo.org/records/22768651)

</details>

<details><summary><b>DeepFluoro (Grupp et al., IPCAI 2020): the H5 release and the vendor DICOMs</b> (fluoro, download)</summary>

- What: 6 cadaver specimens from pelvic osteotomy experiments: 366 fluoroscopy frames with registered poses and 3D and 2D labels in one H5 file (doi:10.7281/T1/IFSXNV), and the vendor DICOM deposit of the same experiments, 2,659 frames and 19 CT files (doi:10.7281/T1/C304HZ)
- Licence: CC BY-NC 4.0 by the H5 release's LICENSE, CC BY-NC-SA 4.0 by its datasheet: non-commercial either way
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/deepfluoro_h5; /rs/rs_grp_oschome/go2432/data/deepfluoro_vendor, fetched from the JHU Dataverse on 2026-09-20 and 2026-09-22, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
- Next: not written yet
- Links: [task #271](https://github.com/OpenSpineConsortium/spine-datasets/issues/271), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/deepfluoro.json), [source](https://github.com/rg2/DeepFluoroLabeling-IPCAI2020)

</details>

<details><summary><b>Geneva hip phantom (BV Pulsera; D&#x27;Isidoro et al., Medical Physics 2021)</b> (fluoro, download)</summary>

- What: 116 fluoroscopy frames of one hip phantom on a Philips BV Pulsera C-arm, with the phantom's CT, a gold-standard rigid transform for each frame and the projection matrix
- Licence: CC BY-SA 4.0, as the source's page gives it (read 2026-10-23), which also lists a 'Contract on the use of data' and shows none of its terms
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/geneva_hip_src, fetched by the owner, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
  - 2026-10-23 note: the source's page on Yareta (the link; doi 10.26037/yareta:2kw5s2jadbbv3ngtkzsovihtnu, the paper Medical Physics 48(10) 2021, doi 10.1002/mp.15124) read: CC BY-SA 4.0, public, with a 'Contract on the use of data' whose terms it does not show; it gives no frame count or C-arm, so what stays as the registry gives it; link and licence written
- Obstacles:
  - the owner's hand: the source's page lists a contract on the use of data with no terms shown; whether one binds the copy on the grid is his decision
- Next: the owner decides whether the contract the page lists binds the copy on the grid
- Links: [task #272](https://github.com/OpenSpineConsortium/spine-datasets/issues/272), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/geneva_hip.json), [source](https://yareta.unige.ch/archives/ed4bb43a-eaaa-4e62-8763-bd5803f5cd47)

</details>

<details><summary><b>Ljubljana 2D/3D registration gold standard (PIXIUM 4600)</b> (fluoro, download)</summary>

- What: 18 X-ray images of one cadaver lumbar spine with fiducial markers, L1 to L5, each with its sensor pose and source position in its header; five CT and five MR volumes, one per vertebra, each with a gold-standard rigid transform to the X-rays; the flat panel is a PIXIUM 4600 as SchwingNet's registry records it, which neither the source's page nor its user guide names
- Licence: CC BY-NC-ND, as the source's page gives it (read 2026-10-23); the user guide that comes with the set says the data are used only under an agreement form between the user and the Laboratory of Imaging Technologies, and never redistributed
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/ljubljana, fetched by the owner, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
  - 2026-10-23 note: the source's page (the link) and its user guide read: CC BY-NC-ND on the page, an agreement form with the Laboratory of Imaging Technologies in the guide; five CT and five MR volumes, one per vertebra, each with a gold-standard rigid transform, and 18 X-ray images whose headers give the sensor pose and source position, where the record had one CT and a pose per frame; neither names the X-ray device; link, licence, what, level truth, pairing and counts corrected
- Obstacles:
  - the owner's hand: the source's page gives CC BY-NC-ND (non-commercial, no derivatives) and its user guide an agreement form with the lab; which terms govern, and whether the project uses the copy on the grid under them, is his decision
- Next: the owner decides which terms govern the copy on the grid
- Links: [task #315](https://github.com/OpenSpineConsortium/spine-datasets/issues/315), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/ljubljana_2d3d_gs.json), [source](https://lit.fe.uni-lj.si/en/raziskave/viri/2D-3D-GS)

</details>

<details><summary><b>LUMOS (Zhejiang University)</b> (fluoro, download, aschehr)</summary>

- What: 803 living patients: 1,620 lumbar AP or lateral radiographs and 280 non-contrast lumbar CTs, anonymised DICOM and NPY; diagnostic radiography, not C-arm fluoroscopy; no pose given
- Licence: CC BY-NC 4.0 (Creative Commons Attribution Non Commercial 4.0 International, as the Zenodo page's licence line reads for v1, published 2025-10-27, read 2026-10-22)
- Status: held; task closed
- Steps so far:
  - 2026-10-21 researched: open on Zenodo; never fetched; still open on Zenodo at the sweep of 2026-10-21, never fetched; queued in the fetch chain of #38
  - 2026-10-22 note: licence read on the Zenodo page: Creative Commons Attribution Non Commercial 4.0 International; v1 (2025-10-27) lists 15 files with an md5 each, about 46.4 GB, and its README says lumos_x_741_670_dcm.zip should read lumos_x_741_770_dcm.zip; no manifest written, since the check takes no non-commercial licence
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/zenodo_lumos, 77 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), no fetch job in the listing's window; more than the record's 46.4 GB; what makes up the difference is for the landing pass to read; fetched by the owner's chain, not the promoter, so no manifest covers it
  - 2026-10-23 note: the owner's word at 09:25 UTC, in the project's thread on the paired CT and X-ray sets: the non-commercial licence is fine for LUMOS; the copy on the grid, 77 GB in zenodo_lumos in the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b), needed no fetch
- Next: the landing pass (#204) checks the files and their sizes; #207 shows whether film n and CT n are the same patient
- Links: [task #27](https://github.com/OpenSpineConsortium/spine-datasets/issues/27), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/lumos.json), [source](https://zenodo.org/records/18173664)

</details>

<details><summary><b>CathAction (Jianu et al. 2024, AIRVLab)</b> (video, download, aschehr)</summary>

- What: about 500,000 fluoroscopy frames (600,000 in the 2026 revision) of endovascular catheterisation, animal and phantom, with action labels, collision labels and 25,000 to 40,000 catheter and guidewire masks; two zips, 4.35 GB and 9.88 GB
- Licence: CC BY-NC-SA 4.0 (cc-by-nc-sa-4.0, as the Hugging Face page's licence line reads, read 2026-10-22), with a download form
- Status: held; task closed
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; the largest real fluoroscopy frame pool in the open with no DUA, from clinical C-arms with live instruments: an exposure, noise and device-domain source beside coronary_angiography and fluoro_video_clips, not anatomy
  - 2026-10-22 note: licence read on https://huggingface.co/datasets/airvlab/CathAction: cc-by-nc-sa-4.0, 56.2 GB in all; the card says 'Please fill out the download form and agree to our license prior to downloading the dataset', so a form and a licence acceptance come first; no manifest written
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/cathaction, 57 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), no fetch job in the listing's window; more than the two zips the record states (4.35 and 9.88 GB); the sample report shows 4 zips and 16 other files, 52.3 GB; fetched by the owner's chain, not the promoter, so no manifest covers it
- Obstacles:
  - the owner's hand: the authors' download form and their licence (non-commercial, share-alike) are to be filled in and accepted by him alone
- Next: the owner decides on the non-commercial term and, if he takes it, fills in the authors' download form; then a granted step lets a manifest go in; a copy on the grid grants no use: the licence decision above still waits on the owner
- Links: [task #39](https://github.com/OpenSpineConsortium/spine-datasets/issues/39), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/cathaction.json), [source](https://huggingface.co/datasets/airvlab/CathAction)

</details>

<details><summary><b>DysphagiaBank (TalkBank), UNM corpus</b> (video, account, the owner)</summary>

- What: lateral swallow videofluoroscopy of about 7 to 53 adults, cervical only, non-commercial, by registration
- Licence: non-commercial, by registration
- Status: held; task closed
- Steps so far:
  - 2026-09-27 fetched: the owner's TalkBank account was verified 2026-09-27 and the corpus downloaded to the grid
  - 2026-10-21 researched: a registration, not a letter; the count on the corpus page is to be checked when registering
  - 2026-10-21 note: audit (#97): held on Ceph, 87 files, 19 GB (MANIFEST_GRID.md, ls 2026-10-08); the record said todo because SchwingNet's registry had it as reach get
  - 2026-10-23 held: the corpus is in the owner's data root, not the shared tree, so the status is held; only the promoter marks a set fetched (the census, #178)
- Obstacles:
  - non-commercial TalkBank terms; whole swallow studies, cervical only (C2 to about C4/5), no level names
- Next: none to obtain; a collaborator may screen the clips for spine visibility once a grid job is approved for scoring
- Links: [task #20](https://github.com/OpenSpineConsortium/spine-datasets/issues/20), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/dysphagiabank.json), [source](https://dysphagia.talkbank.org/)

</details>

<details><summary><b>COBRA2026 public cases (Elekta and Varian)</b> (projections, download)</summary>

- What: the 692 public cases of the COBRA2026 challenge, 467 from Elekta and 225 from Varian linacs at six centres: raw kV CBCT projections of supine pelvic radiotherapy patients (375,618 in all), each case with its CBCT reconstruction and the planning CT deformably registered; the held-back cases are cobra_embargoed (Thummerer, Rit, Kamp, Maspero et al.)
- Licence: CC BY-NC 4.0
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/cobra2026, fetched from the challenge's Girder archive, every catalogued file at its catalogued size, 2026-09-21 to 2026-09-23, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
- Next: not written yet
- Links: [task #262](https://github.com/OpenSpineConsortium/spine-datasets/issues/262), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/cobra2026.json), [source](https://zenodo.org/records/21322350)

</details>

<details><summary><b>IPCAI 2025 paired X-ray and CT set of the distal femur (Flepp 2025, Zenodo 15753063)</b> (projections, download, aschehr)</summary>

- What: one zip, dataset_ipcai.zip, 6.7 GB (md5 cc8bf3e445495d2deb6d50dd058dc977): 50 real calibrated X-rays of 5 cadaveric distal femur specimens (ten views each, about 9 degrees apart, Siemens Fluorospot), their 5 CTs at 0.2 mm slices, the poses, the contour masks and bone surface meshes, from 'Automatic multi-view X-ray/CT registration using bone substructure contours' (Flepp and others, IPCAI 2025, arXiv 2506.13292); the femur, no spine
- Licence: Research-Only Dataset License (as the Zenodo page's licence line reads for version 1.0, published 2025-05-20, read 2026-10-22)
- Status: held; task closed
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; anatomy to confirm; if spine or pelvis, one more real C-arm set with a registered CT, the COBRA and DeepFluoro kind, from a fourth device
  - 2026-10-22 note: licence read on the Zenodo page: Research-Only Dataset License; version 1.0 (2025-05-20) holds one file, dataset_ipcai.zip, 6.7 GB, md5 cc8bf3e445495d2deb6d50dd058dc977; the page does not say which anatomy the X-ray images show; no manifest written, since the check takes only an open licence or a granted step
  - 2026-10-23 held: fetched to /rs/rs_grp_oschome/go2432/data/ipcai2025_xray_ct/raw by the owner's X-ray chain on 2026-10-21 and still zipped (the grid's sample index of 2026-10-22 lists the folder: 4 files, 6.2 GB, one zip); the Zenodo page and the paper show the distal femur of five cadaveric specimens, not the pelvis or spine, so the set names no level and serves as a 2D/3D registration benchmark only (the owner's registry record, 2026-10-23)
- Obstacles:
  - the owner's hand: the licence is a research-only licence, not an open one, so its terms are his to read and accept or decline
- Next: nothing to fetch: unzip as a grid job on the owner's word and read the layout before any use
- Links: [task #34](https://github.com/OpenSpineConsortium/spine-datasets/issues/34), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/ipcai2025_xray_ct.json), [source](https://zenodo.org/records/15753063)

</details>

<details><summary><b>Aariz cephalometric benchmark (Khalid, Fraz 2023) and the ISBI 2015 cephalograms</b> (films, download)</summary>

- What: 1,000 lateral cephalograms from 7 devices with 29 landmarks and a cervical vertebral maturation (CVM) stage per film, C2 to C4 in every image (arXiv:2302.07797; the CEPHA29 challenge at ISBI 2023); the ISBI 2015 set of 400 cephalograms with 19 landmarks and no CVM stage is openly downloadable
- Licence: CC BY 4.0 (the figshare record's licence field, read from the API on 2026-10-21)
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; the 1,000-film set is an open figshare download (27986417, one zip of 2,098,209,792 bytes), entered in grid/fetch-xray.json as aariz on 2026-10-21 (issue #40); the 400-film ISBI 2015 set's link is still to confirm; pediatric anchors for the top of the cervical counter from seven devices
  - 2026-10-23 held: the 1,000 films on the grid at /rs/rs_grp_oschome/go2432/data/aariz, fetched by the owner's chain (SchwingNet's registry, 2026-10-23); the ISBI 2015 cephalograms are not among them
- Next: fetch the ISBI 2015 set of 400 cephalograms once its link is confirmed
- Links: [task #25](https://github.com/OpenSpineConsortium/spine-datasets/issues/25), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/aariz_cephalograms.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/aariz_cephalograms.md), [source](https://doi.org/10.6084/m9.figshare.27986417)

</details>

<details><summary><b>AASCE 2019 / BoostNet AP whole-spine films</b> (films, form)</summary>

- What: 609 AP whole-spine films with 68 landmarks each, the corners of 17 vertebrae from T1 to L5 (481 and 128 in the BoostNet release's two parts), and 98 challenge films whose landmarks were never published; the GitHub mirror holds all 707, an older request-form copy 579 of them (Wu et al., MICCAI 2017; Wang et al., Medical Image Analysis 2021)
- Licence: by request form (SpineWeb dataset 16); the mirror repository is MIT, the images' reuse terms not recorded
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/aasce2019_boostnet; the mirror at /rs/rs_grp_oschome/go2432/data/thoracic_xr/mirror_zlinzju_ke30_u7_AASCE2019, the request-form copy from SpineWeb and the GitHub mirror (md5-checked, 2026-09-22), before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
- Next: not written yet
- Links: [task #254](https://github.com/OpenSpineConsortium/spine-datasets/issues/254), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/aasce.json), [source](https://aasce19.github.io/)

</details>

<details><summary><b>BUU-LSPINE (Klinwichit et al., Applied Sciences 2023)</b> (films, form)</summary>

- What: 3,603 lateral and 3,600 AP lumbar radiographs of 3,600 people with vertebral end-plate lines; the release's 2000 relabel and 400 sample are contained in it
- Licence: the release's end-user agreement by request form: acknowledgement required, no re-identification, never redistributed
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/buu_lspine_3600, received through the release's request form, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
- Next: not written yet
- Links: [task #259](https://github.com/OpenSpineConsortium/spine-datasets/issues/259), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/buu_lspine.json), [source](https://services.informatics.buu.ac.th/spine/)

</details>

<details><summary><b>CSXA, the Cervical Spine X-ray Atlas V3.0 (Ran et al., Scientific Data 2024)</b> (films, download)</summary>

- What: 4,963 lateral cervical radiographs with vertebral corner points in JSON
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/csxa_cervical_xray_atlas, downloaded from Science Data Bank and the release's GitHub repository, 2026-09-01 to 2026-09-09, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
- Next: not written yet
- Links: [task #264](https://github.com/OpenSpineConsortium/spine-datasets/issues/264), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/csxa.json), [source](https://doi.org/10.57760/sciencedb.15391)

</details>

<details><summary><b>KUB-StoneX (Daffodil International University HIRL)</b> (films, download)</summary>

- What: 2,570 AP kidney-ureter-bladder radiographs of 1,703 patients from two Bangladeshi hospitals, with pixel-level stone masks and radiomic features; a KUB film is a frontal lumbar spine and pelvis radiograph at abdominal exposure, with the iliac crests and the sacrum in field
- Licence: CC BY 4.0 (the figshare record's licence field, read from the API on 2026-10-21)
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; an open figshare download (32049369, one zip of 20,765,554,562 bytes), entered in grid/fetch-xray.json as kub_stonex on 2026-10-21 (issue #40); the frontal counterpart of what the registry lacks in volume
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/kub_stonex, 56 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), no fetch job in the listing's window; more than the 20.8 GB zip the record states, since the folder holds it unpacked; the sample report counts 9,630 PNG files; fetched by the owner's chain, not the promoter, so no manifest covers it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #26](https://github.com/OpenSpineConsortium/spine-datasets/issues/26), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/kub_stonex.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/kub_stonex.md), [source](https://doi.org/10.6084/m9.figshare.32049369)

</details>

<details><summary><b>NHANES II spinal films with landmarks (Mo, Papiez, Chen et al., Zenodo)</b> (films, download)</summary>

- What: 543 digitised cervical and lumbar films of 364 people from NHANES II with vertebral landmarks (Zenodo 10223910); the films are among the CDC's 17,073
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/nhanes2_zenodo_landmarks, downloaded from Zenodo on 2026-09-01, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
- Next: not written yet
- Links: [task #316](https://github.com/OpenSpineConsortium/spine-datasets/issues/316), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/nhanes2_annotated.json), [source](https://doi.org/10.5281/zenodo.10223910)

</details>

<details><summary><b>NHANES II cervical and lumbar spine films (NCHS, 1976 to 1980)</b> (films, download)</summary>

- What: 16,531 digitised cervical and lumbar spine films of the second National Health and Nutrition Examination Survey with no landmarks: the 17,073 films on disk (the CDC's index lists 17,075, two of them empty at the source, L00452 and L00456) less the 542 that nhanes2_annotated labels, whose 543rd, L00452, survives only in its landmarks file
- Licence: US government work, public domain (NCHS)
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/nhanes2_cdc_films, downloaded from the CDC's index by a resumable grid job, 2026-09-09 to 2026-09-23, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
- Next: not written yet
- Links: [task #317](https://github.com/OpenSpineConsortium/spine-datasets/issues/317), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/nhanes2_unannotated.json), [source](https://wwwn.cdc.gov/nchs/data/nhanes2/NH2_Xray.htm)

</details>

<details><summary><b>NIH ChestX-ray14 and the RSNA pneumonia subset</b> (films, download)</summary>

- What: 112,120 frontal chest films of 30,805 patients; the RSNA pneumonia detection challenge on Kaggle used 30,000 of them
- Licence: open (NIH); Kaggle competition rules for the RSNA subset
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; open (NIH) and Kaggle competition rules (RSNA); volume with no agreement, no laterals
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/nih_chestxray14, 46 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), no fetch job in the listing's window; the sample report counts the 12 gzip archives NIH publishes the films in, 42.0 GB; fetched by the owner's chain, not the promoter, so no manifest covers it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #37](https://github.com/OpenSpineConsortium/spine-datasets/issues/37), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/nih_chestxray14.json), [source](https://nihcc.app.box.com/v/ChestXray-NIHCC)

</details>

<details><summary><b>ReXGradient-160K (Rajpurkar lab and Gradient Health, 2025)</b> (films, form)</summary>

- What: 160,000 chest radiograph studies with reports from 109,487 patients at 79 US sites; several images per study, so laterals are likely included (to confirm on the page)
- Licence: a non-commercial data access and use agreement on the Hugging Face page
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; Hugging Face gated behind a non-commercial data access and use agreement signed on the page; 79 sites means 79 exposure recipes
  - 2026-10-22 note: owner's sitting prepared: the Hugging Face gate asks only for a signed-in account and agreement to share contact information, under a non-commercial, non-clinical agreement that forbids downloading the whole repository (only the part the project needs), redistribution and re-identification, and asks citation and credit to Gradient Health; 273,004 images in 160,000 studies, downsampled to 25 percent, as split deid_png.part files
  - 2026-10-22 granted: the owner accepted the data access and use agreement on Hugging Face
  - 2026-10-22 note: the owner chose to take the whole repository, about 156 GB, knowing that clause A.5 of the agreement limits a download to the part the project needs; it is a gated source of SchwingNet's platform fetch, read with his Hugging Face token
  - 2026-10-22 fetching: on the owner's choice to take the whole repository despite clause A.5, and with his Hugging Face token on the grid, SchwingNet's gate word fetch hf_rexgradient_160k submitted job 40712197 at SchwingNet 25159c0, about 156 GB
  - 2026-10-23 note: job 40712197 ended COMPLETED after 6 s with nothing fetched (the status word, 2026-10-23 09:29 UTC): the chain read its include filter as a glob that matched no file and still returned 0; the chain was changed the same day to fetch the whole repository with no filter and to fail such a run by name, and the resend went as the gate word fetch hf_rexgradient_160k on the owner's word and count (156 GB), job 40743347
  - 2026-10-24 held: on the grid at /rs/rs_grp_oschome/go2432/data/hf_rexgradient_160k, 156 GB in the status listing of 2026-10-24 02:17 UTC (symphony-template grid branch, 281cfcb), the stated size; fetched by the owner's chain on 2026-10-23 11:27 UTC (job 40743347, done in 59 minutes with the owner's Hugging Face token), not the promoter, so no manifest covers it; the record on the default branch said todo until 2026-10-24, the claim that had recorded the sitting and the first fetch having been released unmerged on 2026-10-23, and its history is carried here
  - 2026-10-24 asked: the owner sent Dr Xiaoman Zhang, the corresponding author, the note drafted 2026-10-22, at 03:24 UTC: it says the agreement is accepted under the owner's account, that section A.5 allows only the portion a project needs while the images come as one archive in ten parts that cannot be split by view before download, and asks leave to download all ten parts with the metadata, keeping only the studies the work uses and deleting the rest once identified from the view-position metadata; waiting for the answer
- Obstacles:
  - the agreement's section A.5 allows only the portion a project needs, and the whole archive is on the grid: the owner's note of 2026-10-24 asked the corresponding author's leave for all ten parts and promised to keep only the studies the work uses, so what is kept once the view-position metadata is read follows that promise, and the answer is awaited
- Next: wait for Dr Zhang's answer to the note of 2026-10-24 03:24 UTC and record it; read the view-position metadata and keep only the lateral studies, deleting the rest, as the note promised; the landing pass checks the files kept (the image parts and the metadata) and a freeze follows on the owner's word
- Links: [task #11](https://github.com/OpenSpineConsortium/spine-datasets/issues/11), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/rexgradient_160k.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/rexgradient_160k.md), [source](https://huggingface.co/datasets/rajpurkarlab/ReXGradient-160K)

</details>

<details><summary><b>VinDr-SpineXR (Nguyen et al., MICCAI 2021)</b> (films, agreement, the owner)</summary>

- What: 10,466 spine radiographs in DICOM from 5,000 studies with lesion boxes, in the release's two splits of 8,389 and 2,077
- Licence: PhysioNet Restricted Health Data License 1.5.0 (credentialed, named-person agreement)
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/vindr_spinexr, downloaded from PhysioNet under the owner's credentialed access, 2026-09-07 to 2026-09-10, checked against SHA256SUMS.txt, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
- Next: not written yet
- Links: [task #328](https://github.com/OpenSpineConsortium/spine-datasets/issues/328), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/vindr_spinexr.json), [source](https://physionet.org/content/vindr-spinexr/1.0.0/)

</details>

<details><summary><b>AbdomenAtlas 3.0 Mini (= AbdomenAtlas 1.1 images)</b> (ct, download)</summary>

- What: AbdomenAtlas 3.0 Mini, the Hugging Face dataset AbdomenAtlas/AbdomenAtlas3.0Mini, the images of AbdomenAtlas 1.1, gathered from public sets that arXiv 2407.16697 lists in its Table 1; tier 1 of the anomaly harvest: all 40 archives fetched, 9,262 CT volumes in the release, of which the data platform counts 7,649 CTs, and 7,835 subjects qualifying, about 570.7 GB in the source's catalogue (NIfTI); its ids are volumes, not people, so one person can hold two scans; it holds CTSpine1K's 150 MSD-T10 cases and PANORAMA's 274 MSD and NIH cases, and 200 of AMOS22's labelled CTs are its people
- Licence: CC BY-NC-SA 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched from Hugging Face in the first tier-1 launch of 2026-09-23, as the data platform's manifest at bf1432f records (40/40 archives; 7,649 CTs); on the grid at /rs/rs_grp_oschome/go2432/data/abdomenatlas3_mini, 532 GB by du in the data platform's census table of 2026-09-25; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) shows the folder at 571 GB, and the sample index of 2026-10-22 13:39 it carries counts 9,264 files, 531.4 GB, in it; the manifest records no anatomy, so the region is the abdomen the release's name gives
- Obstacles:
  - the owner's hand: the licence (CC BY-NC-SA 4.0) is non-commercial and share-alike; whether the project may use the copy on the grid under that term is his decision
- Next: the owner decides on the non-commercial term; the landing pass (#204) checks the files and their sizes
- Links: [task #255](https://github.com/OpenSpineConsortium/spine-datasets/issues/255), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/abdomenatlas3_mini.json), [source](https://huggingface.co/datasets/AbdomenAtlas/AbdomenAtlas3.0Mini)

</details>

<details><summary><b>AMOS22 CT, unlabelled (ids 5000-6899) and labelled</b> (ct, download)</summary>

- What: AMOS, a large-scale abdominal multi-organ benchmark: its unlabelled CT parts and its labelled set, Zenodo records 7262757, 7295661 and 7262581; tier 1 of the anomaly harvest: all five archives fetched, 2,400 scans listed (1,900 and 500), of which the data platform counts 723 CTs, about two thirds being thicker than 3 mm, and 2,200 subjects qualifying, about 102.6 GB in the source's catalogue (NIfTI); the unlabelled part has no patient ids, so people against volumes is unknown, and 200 of the labelled CTs are AbdomenAtlas people
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched from Zenodo in the first tier-1 launch of 2026-09-23, as the data platform's manifest at bf1432f records (5/5 archives; 723 CTs); on the grid at /rs/rs_grp_oschome/go2432/data/amos22, 96 GB by du in the data platform's census table of 2026-09-25; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) shows the folder at 103 GB, and the sample index of 2026-10-22 13:39 it carries counts 3,067 files, 95.6 GB, in it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #256](https://github.com/OpenSpineConsortium/spine-datasets/issues/256), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/amos22.json), [source](https://zenodo.org/records/7262757)

</details>

<details><summary><b>AortaSeg-60</b> (ct, download)</summary>

- What: AortaSeg-60, 60 aorta CTs, angiograms and non-contrast scans, Zenodo record 18147026; tier 1 of the anomaly harvest: the data platform counts 55 usable CTs of the 60, about 15.87 GB in the catalogue (NIfTI)
- Licence: CC0 1.0
- Status: held; task closed
- Steps so far:
  - 2026-09-24 held: fetched from Zenodo in the late tier-1 launch of 2026-09-24, as the data platform's manifest at bf1432f records (55 CTs); on the grid at /rs/rs_grp_oschome/go2432/data/aortaseg60, 15 GB by du in the data platform's census table of 2026-09-25; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) shows the folder at 16 GB, and the sample index of 2026-10-22 13:39 it carries counts 310 files, 14.8 GB, in it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #257](https://github.com/OpenSpineConsortium/spine-datasets/issues/257), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/aortaseg60.json), [source](https://zenodo.org/records/18147026)

</details>

<details><summary><b>STOIC2021 training (AWS Open Data)</b> (ct, download)</summary>

- What: STOIC2021 training set, 2,000 chest CT as MHA on AWS Open Data (s3://stoic2021-training; LICENCE.txt read 2026-09-23), about 240 GB; also inside CADS (gated) and re-packed as AUC23 'Lung CT COVID-19'
- Licence: CC BY-NC 4.0
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/aws_stoic2021, 265 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), no fetch job in the listing's window; the record states about 240 GB and 2,000 subjects; the listing's sample report counts 2,000 images; fetched by the owner's chain, not the promoter, so no manifest covers it
  - 2026-10-23 note: the link is now the bucket's page on the Registry of Open Data on AWS, read 2026-10-23, in place of its s3 address, which no page can open; the page gives CC BY-NC 4.0, 2,000 CT scans and the bucket the record's what names, as the record does
- Obstacles:
  - the owner's hand: the licence (CC BY-NC 4.0) is non-commercial; whether the project may use the copy on the grid under that term is his decision
- Next: the owner decides on the non-commercial term; the landing pass (#204) checks the files and their sizes
- Links: [task #44](https://github.com/OpenSpineConsortium/spine-datasets/issues/44), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/aws_stoic2021.json), [source](https://registry.opendata.aws/stoic2021-training/)

</details>

<details><summary><b>Barts CRL (colorectal-cancer staging CT)</b> (ct, download)</summary>

- What: Barts CRL, colorectal-cancer staging CT from three London hospitals, Zenodo record 14004841; tier 1 of the anomaly harvest: 220 CTs listed, of which the data platform counts 212 usable, and 220 subjects qualifying, about 20.32 GB in the catalogue (NIfTI)
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-24 held: fetched from Zenodo in the late tier-1 launch of 2026-09-24, as the data platform's manifest at bf1432f records (212 CTs); on the grid at /rs/rs_grp_oschome/go2432/data/barts_crl, 19 GB by du in the data platform's census table of 2026-09-25; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) shows the folder at 21 GB, and the sample index of 2026-10-22 13:39 it carries counts 222 files, 18.9 GB, in it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #258](https://github.com/OpenSpineConsortium/spine-datasets/issues/258), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/barts_crl.json), [source](https://zenodo.org/records/14004841)

</details>

<details><summary><b>CSI 2014 spine CT</b> (ct, download)</summary>

- What: CSI 2014 spine CT, Zenodo record 7049844; tier 1 of the anomaly harvest: 20 thoracolumbar spine CTs, the image files alone fetched (MHA), about 3.6 GB in the catalogue
- Licence: ODC-By
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched from Zenodo in the first tier-1 launch of 2026-09-23, as the data platform's manifest at bf1432f records (20/20; 20 CTs); on the grid at /rs/rs_grp_oschome/go2432/data/csi2014, 7 GB by du in the data platform's census table of 2026-09-25; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) shows the folder at 7 GB, and the sample index of 2026-10-22 13:39 it carries counts 42 files, 6.2 GB, in it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #263](https://github.com/OpenSpineConsortium/spine-datasets/issues/263), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/csi2014.json), [source](https://zenodo.org/records/7049844)

</details>

<details><summary><b>CTPelvic1K</b> (ct, download)</summary>

- What: 172 pelvic CT volumes of the release's datasets 6 and 7, with the pelvic masks of datasets 1 to 5 mapped back to their sources
- Licence: CC BY 4.0 by one reading, non-commercial by another; to confirm on the page
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/ctpelvic1k, downloaded from Zenodo with its md5, 2026-09-23, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
  - 2026-10-24 held: the folder is data/ctpelvic1k_clinic, as SchwingNet's data/reproduce/sources.json and the census of 2026-09-25 record (14 GB, 173 CTs): freeze job 40777657 found no data/ctpelvic1k, the path this record carried from the registry; the 36 GB full release under the home's CTSpinoPelvic1K/data/ctpelvic1k is presumed deleted on 2026-09-07 (reclaim_grid_space.sh)
- Obstacles:
  - the licence line is still to confirm on the source's page
- Next: not written yet
- Links: [task #265](https://github.com/OpenSpineConsortium/spine-datasets/issues/265), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/ctpelvic1k.json), [source](https://zenodo.org/record/4588403)

</details>

<details><summary><b>CTSpine1K</b> (ct, download)</summary>

- What: 1,005 CT volumes with vertebra masks, gathered from four public sources (MIRACLE-Center; doi:10.59275/j.melba.2025-gf84)
- Licence: CC BY-NC-SA 4.0
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/ctspine1k, downloaded from the Hugging Face copy with each file's sha256, 2026-09-23, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
  - 2026-10-25 note: 1,005 patients from the paper's Table 1, one volume each, so the feed counts its people with level truth (#252)
- Next: not written yet
- Links: [task #266](https://github.com/OpenSpineConsortium/spine-datasets/issues/266), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/ctspine1k.json), [source](https://github.com/MIRACLE-Center/CTSpine1K)

</details>

<details><summary><b>CTSpinoPelvic1K v11 (the consortium&#x27;s own release)</b> (ct, download)</summary>

- What: 802 CT volumes from TCIA sources with vertebra, sacrum and pelvis labels (Zenodo 22797014)
- Licence: labels CC BY-NC-SA 4.0; the CT images CC BY 3.0 (TCIA)
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k, built and published by the consortium; the labels from Zenodo v11, 2026-09-18, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
- Next: not written yet
- Links: [task #267](https://github.com/OpenSpineConsortium/spine-datasets/issues/267), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/ctspinopelvic1k.json), [source](https://zenodo.org/records/22797014)

</details>

<details><summary><b>CURVAS 2024</b> (ct, download)</summary>

- What: CURVAS 2024, 90 CTs under UKCHLL ids, Zenodo record 13767408; tier 1 of the anomaly harvest: the data platform counts 70 CTs, the 90 less the 20 of one archive whose Deflate64 unpacking failed, with no file saying whether it was repaired, about 29.4 GB in the catalogue (NIfTI); it may overlap CURVAS-PDACVI
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-24 held: fetched from Zenodo in the late tier-1 launch of 2026-09-24, as the data platform's manifest at bf1432f records (70 CTs); on the grid at /rs/rs_grp_oschome/go2432/data/curvas, 28 GB by du in the data platform's census table of 2026-09-25; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) shows the folder at 30 GB, and the sample index of 2026-10-22 13:39 it carries counts 284 files, 27.9 GB, in it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #268](https://github.com/OpenSpineConsortium/spine-datasets/issues/268), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/curvas.json), [source](https://zenodo.org/records/13767408)

</details>

<details><summary><b>CURVAS-PDACVI (MICCAI 2025)</b> (ct, download)</summary>

- What: CURVAS-PDACVI (MICCAI 2025), 109 CTs, Zenodo record 17552201; tier 1 of the anomaly harvest: the data platform counts 101 CTs and 109 subjects qualifying, about 15.42 GB in the catalogue (NIfTI); 78 of the 101 look like near-duplicates of CURVAS 2024's scans by a thumbnail correlation of 0.98 or more, as the overlap of the two sets would make them, and are not merged
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-24 held: fetched from Zenodo in the late tier-1 launch of 2026-09-24, as the data platform's manifest at bf1432f records (101 CTs); on the grid at /rs/rs_grp_oschome/go2432/data/curvas_pdacvi, 16 GB by du in the data platform's census table of 2026-09-25; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) shows the folder at 17 GB, and the sample index of 2026-10-22 13:39 it carries counts 875 files, 15.7 GB, in it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #269](https://github.com/OpenSpineConsortium/spine-datasets/issues/269), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/curvas_pdacvi.json), [source](https://zenodo.org/records/17552201)

</details>

<details><summary><b>DEEP-PSMA (PSMA + FDG PET/CT, mCRPC)</b> (ct, download)</summary>

- What: DEEP-PSMA, PSMA and FDG PET/CT of 100 patients with metastatic castration-resistant prostate cancer, Zenodo record 15281784; tier 1 of the anomaly harvest: 200 CTs in the release, of which the data platform counts 53, since about half the attenuation CTs are thicker than 3 mm, about 24.07 GB in the catalogue (NIfTI)
- Licence: CC BY-NC 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-24 held: fetched from Zenodo in the late tier-1 launch of 2026-09-24, as the data platform's manifest at bf1432f records (53 CTs); on the grid at /rs/rs_grp_oschome/go2432/data/deep_psma, 23 GB by du in the data platform's census table of 2026-09-25; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) shows the folder at 25 GB, and the sample index of 2026-10-22 13:39 it carries counts 1,507 files, 22.6 GB, in it
- Obstacles:
  - the owner's hand: the licence (CC BY-NC 4.0) is non-commercial; whether the project may use the copy on the grid under that term is his decision
- Next: the owner decides on the non-commercial term; the landing pass (#204) checks the files and their sizes
- Links: [task #270](https://github.com/OpenSpineConsortium/spine-datasets/issues/270), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/deep_psma.json), [source](https://zenodo.org/records/15281784)

</details>

<details><summary><b>IDC `acrin_flt_breast`</b> (ct, download)</summary>

- What: IDC v24 collection acrin_flt_breast (TCIA doi:10.7937/k9/tcia.2017.ol20zmxg), tier 1 of the anomaly harvest: 15 subjects and 15 CT series verified on fetch (DICOM), about 2.8 GB; whole body
- Licence: CC BY 3.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 15 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/acrin_flt_breast; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 5,341 DICOM files, 2.6 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #274](https://github.com/OpenSpineConsortium/spine-datasets/issues/274), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_acrin_flt_breast.json), [source](https://doi.org/10.7937/k9/tcia.2017.ol20zmxg)

</details>

<details><summary><b>IDC `acrin_nsclc_fdg_pet`</b> (ct, download)</summary>

- What: IDC v24 collection acrin_nsclc_fdg_pet (TCIA doi:10.7937/tcia.2019.30ilqfcl), tier 1 of the anomaly harvest: 131 subjects and 131 CT series verified on fetch (DICOM), about 15.4 GB; head and neck, chest, abdomen, pelvis, whole body and other
- Licence: CC BY 3.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 131 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/acrin_nsclc_fdg_pet; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 29,541 DICOM files, 14.7 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #275](https://github.com/OpenSpineConsortium/spine-datasets/issues/275), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_acrin_nsclc_fdg_pet.json), [source](https://doi.org/10.7937/tcia.2019.30ilqfcl)

</details>

<details><summary><b>IDC `adrenal_acc_ki67_seg`</b> (ct, download)</summary>

- What: IDC v24 collection adrenal_acc_ki67_seg (TCIA doi:10.7937/1fpg-vm46), tier 1 of the anomaly harvest: 29 subjects and 29 CT series verified on fetch (DICOM), about 3.5 GB; chest, abdomen and pelvis
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 29 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/adrenal_acc_ki67_seg; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 6,729 DICOM files, 3.3 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #276](https://github.com/OpenSpineConsortium/spine-datasets/issues/276), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_adrenal_acc_ki67_seg.json), [source](https://doi.org/10.7937/1fpg-vm46)

</details>

<details><summary><b>IDC `anti_pd_1_lung`</b> (ct, download)</summary>

- What: IDC v24 collection anti_pd_1_lung (TCIA doi:10.7937/tcia.2019.zjjwb9ip), tier 1 of the anomaly harvest: 34 subjects and 34 CT series verified on fetch (DICOM), about 4.2 GB; chest, abdomen, pelvis and whole body
- Licence: CC BY 3.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 34 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/anti_pd_1_lung; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 8,055 DICOM files, 4.0 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #277](https://github.com/OpenSpineConsortium/spine-datasets/issues/277), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_anti_pd_1_lung.json), [source](https://doi.org/10.7937/tcia.2019.zjjwb9ip)

</details>

<details><summary><b>IDC `cmb_brca`</b> (ct, download)</summary>

- What: IDC v24 collection cmb_brca (TCIA doi:10.7937/dx22-8j71), tier 1 of the anomaly harvest: 21 subjects and 21 CT series verified on fetch (DICOM), about 2.5 GB; chest, abdomen, pelvis and whole body
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 21 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/cmb_brca; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 4,909 DICOM files, 2.4 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #278](https://github.com/OpenSpineConsortium/spine-datasets/issues/278), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_cmb_brca.json), [source](https://doi.org/10.7937/dx22-8j71)

</details>

<details><summary><b>IDC `cmb_crc`</b> (ct, download)</summary>

- What: IDC v24 collection cmb_crc (TCIA doi:10.7937/djg7-gz87), tier 1 of the anomaly harvest: 30 subjects and 30 CT series verified on fetch (DICOM), about 5.3 GB; chest, abdomen, pelvis, whole body and other
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 30 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/cmb_crc; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 10,256 DICOM files, 5.0 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #279](https://github.com/OpenSpineConsortium/spine-datasets/issues/279), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_cmb_crc.json), [source](https://doi.org/10.7937/djg7-gz87)

</details>

<details><summary><b>IDC `cmb_lca`</b> (ct, download)</summary>

- What: IDC v24 collection cmb_lca (TCIA doi:10.7937/3cx3-s132), tier 1 of the anomaly harvest: 75 subjects and 75 CT series verified on fetch (DICOM), about 9.8 GB; chest, abdomen, pelvis, whole body and other
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 75 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/cmb_lca; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 18,851 DICOM files, 9.3 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #280](https://github.com/OpenSpineConsortium/spine-datasets/issues/280), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_cmb_lca.json), [source](https://doi.org/10.7937/3cx3-s132)

</details>

<details><summary><b>IDC `cmb_mel`</b> (ct, download)</summary>

- What: IDC v24 collection cmb_mel (TCIA doi:10.7937/gwsp-wh72), tier 1 of the anomaly harvest: 23 subjects and 23 CT series verified on fetch (DICOM), about 2.1 GB; chest, abdomen, pelvis, spine and whole body
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 23 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/cmb_mel; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 4,074 DICOM files, 2.0 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #281](https://github.com/OpenSpineConsortium/spine-datasets/issues/281), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_cmb_mel.json), [source](https://doi.org/10.7937/gwsp-wh72)

</details>

<details><summary><b>IDC `cmb_mml`</b> (ct, download)</summary>

- What: IDC v24 collection cmb_mml (TCIA doi:10.7937/szkb-sw39), tier 1 of the anomaly harvest: 16 subjects and 16 CT series verified on fetch (DICOM), about 2.3 GB; chest, abdomen, pelvis, spine, whole body and other; its CR and DX skeletal-survey films are task #184 and its XA frames task #183
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 16 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/cmb_mml; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 4,407 DICOM files, 2.2 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #282](https://github.com/OpenSpineConsortium/spine-datasets/issues/282), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_cmb_mml.json), [source](https://doi.org/10.7937/szkb-sw39)

</details>

<details><summary><b>IDC `cmb_ov`</b> (ct, download)</summary>

- What: IDC v24 collection cmb_ov (TCIA doi:10.7937/4nx6-e061), tier 1 of the anomaly harvest: 7 subjects and 7 CT series verified on fetch (DICOM), about 1 GB; chest, abdomen and pelvis
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 7 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/cmb_ov; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 1,983 DICOM files, 998.2 MB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #283](https://github.com/OpenSpineConsortium/spine-datasets/issues/283), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_cmb_ov.json), [source](https://doi.org/10.7937/4nx6-e061)

</details>

<details><summary><b>IDC `colorectal_liver_metastases` (Colorectal-Liver-Metastases)</b> (ct, download)</summary>

- What: IDC v24 collection colorectal_liver_metastases (Colorectal-Liver-Metastases; TCIA doi:10.7937/qxk2-qg03), tier 1 of the anomaly harvest: 80 subjects and 80 CT series verified on fetch (DICOM), about 6.2 GB; abdomen
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 80 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/colorectal_liver_metastases; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 11,967 DICOM files, 5.9 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #284](https://github.com/OpenSpineConsortium/spine-datasets/issues/284), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_colorectal_liver_metastases.json), [source](https://doi.org/10.7937/qxk2-qg03)

</details>

<details><summary><b>IDC `covid_19_ar`</b> (ct, download)</summary>

- What: IDC v24 collection covid_19_ar (TCIA doi:10.7937/tcia.2020.py71-5978), tier 1 of the anomaly harvest: 23 subjects and 23 CT series verified on fetch (DICOM), about 5.5 GB; chest, abdomen and pelvis
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 23 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/covid_19_ar; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 10,729 DICOM files, 5.3 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #285](https://github.com/OpenSpineConsortium/spine-datasets/issues/285), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_covid_19_ar.json), [source](https://doi.org/10.7937/tcia.2020.py71-5978)

</details>

<details><summary><b>IDC `covid_19_ny_sbu` (COVID-19-NY-SBU)</b> (ct, download)</summary>

- What: IDC v24 collection covid_19_ny_sbu (COVID-19-NY-SBU; TCIA doi:10.7937/tcia.bbag-2923), tier 1 of the anomaly harvest: 443 subjects and 443 CT series verified on fetch (DICOM), about 63.1 GB; chest, abdomen, pelvis and whole body; its CR and DX films are task #185
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 443 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/covid_19_ny_sbu; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 122,272 DICOM files, 60.2 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #286](https://github.com/OpenSpineConsortium/spine-datasets/issues/286), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_covid_19_ny_sbu.json), [source](https://doi.org/10.7937/tcia.bbag-2923)

</details>

<details><summary><b>IDC `cptac_ccrcc`</b> (ct, download)</summary>

- What: IDC v24 collection cptac_ccrcc (TCIA doi:10.7937/k9/tcia.2018.oblamn27), tier 1 of the anomaly harvest: 48 subjects and 48 CT series verified on fetch (DICOM), about 7.7 GB; chest, abdomen, pelvis and other
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 48 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/cptac_ccrcc; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 13,242 DICOM files, 7.4 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #287](https://github.com/OpenSpineConsortium/spine-datasets/issues/287), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_cptac_ccrcc.json), [source](https://doi.org/10.7937/k9/tcia.2018.oblamn27)

</details>

<details><summary><b>IDC `cptac_cm`</b> (ct, download)</summary>

- What: IDC v24 collection cptac_cm (TCIA doi:10.7937/k9/tcia.2018.odu24gze), tier 1 of the anomaly harvest: 12 subjects and 12 CT series verified on fetch (DICOM), about 4.1 GB; chest, abdomen, pelvis, whole body and other
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 12 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/cptac_cm; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 8,020 DICOM files, 3.9 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #288](https://github.com/OpenSpineConsortium/spine-datasets/issues/288), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_cptac_cm.json), [source](https://doi.org/10.7937/k9/tcia.2018.odu24gze)

</details>

<details><summary><b>IDC `cptac_lscc` (tier 2)</b> (ct, download)</summary>

- What: IDC v24 collection cptac_lscc (TCIA doi:10.7937/k9/tcia.2018.6emub5l2), tier 2 of the anomaly harvest: 32 subjects, about 8.3 GB raw plus screen; chest, abdomen, pelvis and whole body
- Licence: CC BY 4.0
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain after idc_tier2.csv is regenerated; the ranking's refusals: slice over 3.0 mm 46, non-axial reformat 29, localizer 16, not a regularly spaced 3-D volume 12
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/idc_cptac_lscc, 30 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), job 40697698 COMPLETED; more than the record's 8.3 GB raw, which leaves out the screen products the folder holds beside it; fetched by the owner's chain, not the promoter, so no manifest covers it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #45](https://github.com/OpenSpineConsortium/spine-datasets/issues/45), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_cptac_lscc.json), [source](https://doi.org/10.7937/k9/tcia.2018.6emub5l2)

</details>

<details><summary><b>IDC `cptac_luad` (tier 2)</b> (ct, download)</summary>

- What: IDC v24 collection cptac_luad (TCIA doi:10.7937/k9/tcia.2018.pat12tbs), tier 2 of the anomaly harvest: 32 subjects, about 7 GB raw plus screen; chest, abdomen and whole body
- Licence: CC BY 4.0
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain after idc_tier2.csv is regenerated; the ranking's refusals: slice over 3.0 mm 78, non-axial reformat 72, localizer 66, under 60 slices 37
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/idc_cptac_luad, 39 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), job 40697697 COMPLETED; more than the record's 7 GB raw, which leaves out the screen products the folder holds beside it; fetched by the owner's chain, not the promoter, so no manifest covers it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #46](https://github.com/OpenSpineConsortium/spine-datasets/issues/46), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_cptac_luad.json), [source](https://doi.org/10.7937/k9/tcia.2018.pat12tbs)

</details>

<details><summary><b>IDC `cptac_pda`</b> (ct, download)</summary>

- What: IDC v24 collection cptac_pda (TCIA doi:10.7937/k9/tcia.2018.sc20fo18), tier 1 of the anomaly harvest: 62 subjects and 62 CT series verified on fetch (DICOM), about 9.8 GB; chest, abdomen, pelvis and other
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 62 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/cptac_pda; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 18,952 DICOM files, 9.4 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #289](https://github.com/OpenSpineConsortium/spine-datasets/issues/289), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_cptac_pda.json), [source](https://doi.org/10.7937/k9/tcia.2018.sc20fo18)

</details>

<details><summary><b>IDC `cptac_sar`</b> (ct, download)</summary>

- What: IDC v24 collection cptac_sar (TCIA doi:10.7937/tcia.2019.9bt23r95), tier 1 of the anomaly harvest: 14 subjects and 14 CT series verified on fetch (DICOM), about 3 GB; chest, abdomen, pelvis, whole body and other
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 14 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/cptac_sar; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 4,971 DICOM files, 2.9 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #290](https://github.com/OpenSpineConsortium/spine-datasets/issues/290), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_cptac_sar.json), [source](https://doi.org/10.7937/tcia.2019.9bt23r95)

</details>

<details><summary><b>IDC `cptac_stad`</b> (ct, download)</summary>

- What: IDC v24 collection cptac_stad (TCIA doi:10.7937/jw9a-8k71), tier 1 of the anomaly harvest: 19 subjects and 19 CT series verified on fetch (DICOM), about 6.9 GB; chest, abdomen and pelvis
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 19 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/cptac_stad; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 13,485 DICOM files, 6.6 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #291](https://github.com/OpenSpineConsortium/spine-datasets/issues/291), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_cptac_stad.json), [source](https://doi.org/10.7937/jw9a-8k71)

</details>

<details><summary><b>IDC `cptac_ucec`</b> (ct, download)</summary>

- What: IDC v24 collection cptac_ucec (TCIA doi:10.7937/k9/tcia.2018.3r3juisw), tier 1 of the anomaly harvest: 66 subjects and 66 CT series verified on fetch (DICOM), about 10.3 GB; chest, abdomen, pelvis and whole body
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 66 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/cptac_ucec; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 19,942 DICOM files, 9.8 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #292](https://github.com/OpenSpineConsortium/spine-datasets/issues/292), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_cptac_ucec.json), [source](https://doi.org/10.7937/k9/tcia.2018.3r3juisw)

</details>

<details><summary><b>IDC `ct_vs_pet_ventilation_imaging`</b> (ct, download)</summary>

- What: IDC v24 collection ct_vs_pet_ventilation_imaging (TCIA doi:10.7937/3ppx-7s22), tier 1 of the anomaly harvest: 20 subjects and 20 CT series verified on fetch (DICOM), about 1.8 GB; chest and abdomen
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 20 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/ct_vs_pet_ventilation_imaging; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, has no row for the folder, while the manifest records 20 series verified on 2026-09-23
- Obstacles:
  - the sample index of 2026-10-22 lists no files in the folder, while the data platform's manifest records 20 series verified there; the landing pass shows which holds
- Next: the landing pass (#204) checks the files and their sizes, first whether the folder holds the series
- Links: [task #293](https://github.com/OpenSpineConsortium/spine-datasets/issues/293), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_ct_vs_pet_ventilation_imaging.json), [source](https://doi.org/10.7937/3ppx-7s22)

</details>

<details><summary><b>IDC `ctpred_sunitinib_pannet`</b> (ct, download)</summary>

- What: IDC v24 collection ctpred_sunitinib_pannet (TCIA doi:10.7937/spgk-0p94), tier 1 of the anomaly harvest: 34 subjects and 34 CT series verified on fetch (DICOM), about 6 GB; chest, abdomen, pelvis and other
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 34 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/ctpred_sunitinib_pannet; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 11,689 DICOM files, 5.7 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #294](https://github.com/OpenSpineConsortium/spine-datasets/issues/294), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_ctpred_sunitinib_pannet.json), [source](https://doi.org/10.7937/spgk-0p94)

</details>

<details><summary><b>IDC `eay131` (EAY131 (NCI-MATCH))</b> (ct, download)</summary>

- What: IDC v24 collection eay131 (EAY131 (NCI-MATCH); TCIA doi:10.7937/c5ke-yx42), tier 1 of the anomaly harvest: 376 subjects and 376 CT series verified on fetch (DICOM), about 36.4 GB; chest, abdomen, pelvis, spine, whole body and other
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 376 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/eay131; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 65,202 DICOM files, 34.7 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #295](https://github.com/OpenSpineConsortium/spine-datasets/issues/295), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_eay131.json), [source](https://doi.org/10.7937/c5ke-yx42)

</details>

<details><summary><b>IDC `hcc_tace_seg` (HCC-TACE-Seg)</b> (ct, download)</summary>

- What: IDC v24 collection hcc_tace_seg (HCC-TACE-Seg; TCIA doi:10.7937/tcia.5fna-0924), tier 1 of the anomaly harvest: 101 subjects and 101 CT series verified on fetch (DICOM), about 5 GB; chest, abdomen and pelvis
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 101 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/hcc_tace_seg; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 9,717 DICOM files, 4.8 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #296](https://github.com/OpenSpineConsortium/spine-datasets/issues/296), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_hcc_tace_seg.json), [source](https://doi.org/10.7937/tcia.5fna-0924)

</details>

<details><summary><b>IDC `ldct_and_projection_data` (tier 2)</b> (ct, download)</summary>

- What: IDC v24 collection ldct_and_projection_data (TCIA doi:10.7937/9npb-2637), tier 2 of the anomaly harvest: 99 subjects, about 16.5 GB raw plus screen; chest
- Licence: CC BY 4.0
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain after idc_tier2.csv is regenerated; the ranking's refusals: slice over 3.0 mm 150
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/idc_ldct_and_projection_data, 863 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), job 40697701 COMPLETED; far more than the record's 16.5 GB, so the record's size counts the CT images alone and not the projection data; the job ran 2 h 57 min; fetched by the owner's chain, not the promoter, so no manifest covers it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #47](https://github.com/OpenSpineConsortium/spine-datasets/issues/47), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_ldct_and_projection_data.json), [source](https://doi.org/10.7937/9npb-2637)

</details>

<details><summary><b>IDC `lung_pet_ct_dx` (Lung-PET-CT-Dx)</b> (ct, download)</summary>

- What: IDC v24 collection lung_pet_ct_dx (Lung-PET-CT-Dx; TCIA doi:10.7937/tcia.2020.nnc2-0461), tier 1 of the anomaly harvest: 158 subjects and 158 CT series verified on fetch (DICOM), about 29.2 GB; chest, abdomen, whole body and other
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 158 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/lung_pet_ct_dx; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 56,646 DICOM files, 27.8 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #297](https://github.com/OpenSpineConsortium/spine-datasets/issues/297), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_lung_pet_ct_dx.json), [source](https://doi.org/10.7937/tcia.2020.nnc2-0461)

</details>

<details><summary><b>IDC `mediastinal_lymph_node_seg`</b> (ct, download)</summary>

- What: IDC v24 collection mediastinal_lymph_node_seg (TCIA doi:10.7937/qvaz-ja09), tier 1 of the anomaly harvest: 316 subjects and 316 CT series verified on fetch (DICOM), about 25.1 GB; head and neck, chest, abdomen, pelvis and whole body
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 316 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/mediastinal_lymph_node_seg; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 48,770 DICOM files, 23.9 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #298](https://github.com/OpenSpineConsortium/spine-datasets/issues/298), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_mediastinal_lymph_node_seg.json), [source](https://doi.org/10.7937/qvaz-ja09)

</details>

<details><summary><b>IDC `midrc_ricord_1a`</b> (ct, download)</summary>

- What: IDC v24 collection midrc_ricord_1a (TCIA doi:10.7937/vtw4-x588), tier 1 of the anomaly harvest: 98 subjects and 98 CT series verified on fetch (DICOM), about 6.5 GB; chest, abdomen and other
- Licence: CC BY-NC 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 98 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/midrc_ricord_1a; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 14,964 DICOM files, 6.2 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Obstacles:
  - the owner's hand: the licence (CC BY-NC 4.0) is non-commercial; whether the project may use the copy on the grid under that term is his decision
- Next: the owner decides on the non-commercial term; the landing pass (#204) checks the files and their sizes
- Links: [task #299](https://github.com/OpenSpineConsortium/spine-datasets/issues/299), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_midrc_ricord_1a.json), [source](https://doi.org/10.7937/vtw4-x588)

</details>

<details><summary><b>IDC `midrc_ricord_1b` (tier 2)</b> (ct, download)</summary>

- What: IDC v24 collection midrc_ricord_1b (TCIA doi:10.7937/31v8-4a40), tier 2 of the anomaly harvest: 91 subjects, about 7 GB raw plus screen; chest, abdomen and pelvis
- Licence: CC BY-NC 4.0
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain after idc_tier2.csv is regenerated; the ranking's refusals: non-axial reformat 25, not a regularly spaced 3-D volume 1, under 60 slices 1
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/idc_midrc_ricord_1b, 9 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), job 40697699 COMPLETED; beside the record's 7 GB raw; fetched by the owner's chain, not the promoter, so no manifest covers it
- Obstacles:
  - the owner's hand: the licence (CC BY-NC 4.0) is non-commercial; whether the project may use the copy on the grid under that term is his decision
- Next: the owner decides on the non-commercial term; the landing pass (#204) checks the files and their sizes
- Links: [task #49](https://github.com/OpenSpineConsortium/spine-datasets/issues/49), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_midrc_ricord_1b.json), [source](https://doi.org/10.7937/31v8-4a40)

</details>

<details><summary><b>IDC `nsclc_radiogenomics` (tier 2)</b> (ct, download)</summary>

- What: IDC v24 collection nsclc_radiogenomics (TCIA doi:10.7937/k9/tcia.2017.7hs46erv), tier 2 of the anomaly harvest: 188 subjects, about 28 GB raw plus screen; chest, abdomen, pelvis and whole body
- Licence: CC BY 3.0
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain after idc_tier2.csv is regenerated; the ranking's refusals: slice over 3.0 mm 235, non-axial reformat 123, localizer 100, reformat or MIP series 37
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/idc_nsclc_radiogenomics, 91 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), job 40697703 COMPLETED; more than the record's 28 GB raw, which leaves out the screen products the folder holds beside it; fetched by the owner's chain, not the promoter, so no manifest covers it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #50](https://github.com/OpenSpineConsortium/spine-datasets/issues/50), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_nsclc_radiogenomics.json), [source](https://doi.org/10.7937/k9/tcia.2017.7hs46erv)

</details>

<details><summary><b>IDC `nsclc_radiomics` (tier 2)</b> (ct, download)</summary>

- What: IDC v24 collection nsclc_radiomics (TCIA doi:10.7937/k9/tcia.2015.pf0m9rei), tier 2 of the anomaly harvest: 415 subjects, about 25.8 GB raw plus screen; chest
- Licence: CC BY-NC 3.0
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain after idc_tier2.csv is regenerated; the ranking's refusals: not a regularly spaced 3-D volume 6, non-axial reformat 1
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/idc_nsclc_radiomics, 27 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), job 40697702 COMPLETED; beside the record's 25.8 GB raw; fetched by the owner's chain, not the promoter, so no manifest covers it
- Obstacles:
  - the owner's hand: the licence (CC BY-NC 3.0) is non-commercial; whether the project may use the copy on the grid under that term is his decision
- Next: the owner decides on the non-commercial term; the landing pass (#204) checks the files and their sizes
- Links: [task #51](https://github.com/OpenSpineConsortium/spine-datasets/issues/51), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_nsclc_radiomics.json), [source](https://doi.org/10.7937/k9/tcia.2015.pf0m9rei)

</details>

<details><summary><b>IDC `pancreatic_ct_cbct_seg`</b> (ct, download)</summary>

- What: IDC v24 collection pancreatic_ct_cbct_seg (TCIA doi:10.7937/tcia.eshq-4d90), tier 1 of the anomaly harvest: 40 subjects and 40 CT series verified on fetch (DICOM), about 2.9 GB; abdomen and pelvis
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 40 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/pancreatic_ct_cbct_seg; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 5,614 DICOM files, 2.8 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #300](https://github.com/OpenSpineConsortium/spine-datasets/issues/300), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_pancreatic_ct_cbct_seg.json), [source](https://doi.org/10.7937/tcia.eshq-4d90)

</details>

<details><summary><b>IDC `pediatric_ct_seg` (Pediatric-CT-SEG)</b> (ct, download)</summary>

- What: IDC v24 collection pediatric_ct_seg (Pediatric-CT-SEG; TCIA doi:10.7937/tcia.x0h0-1706), tier 1 of the anomaly harvest: 352 subjects and 352 CT series verified on fetch (DICOM), about 55.6 GB; chest, abdomen and pelvis
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 352 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/pediatric_ct_seg; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 108,019 DICOM files, 53.0 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #301](https://github.com/OpenSpineConsortium/spine-datasets/issues/301), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_pediatric_ct_seg.json), [source](https://doi.org/10.7937/tcia.x0h0-1706)

</details>

<details><summary><b>IDC `pelvic_reference_data`</b> (ct, download)</summary>

- What: IDC v24 collection pelvic_reference_data (TCIA doi:10.7937/tcia.2019.woskq5oo), tier 1 of the anomaly harvest: 58 subjects and 58 CT series verified on fetch (DICOM), about 4.4 GB; abdomen, pelvis and other
- Licence: CC BY 3.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 58 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/pelvic_reference_data; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 8,540 DICOM files, 4.2 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #302](https://github.com/OpenSpineConsortium/spine-datasets/issues/302), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_pelvic_reference_data.json), [source](https://doi.org/10.7937/tcia.2019.woskq5oo)

</details>

<details><summary><b>IDC `psma_pet_ct_lesions` (PSMA-PET-CT-Lesions (autoPET III))</b> (ct, download)</summary>

- What: IDC v24 collection psma_pet_ct_lesions (PSMA-PET-CT-Lesions (autoPET III); TCIA doi:10.7937/r7ep-3x37), tier 1 of the anomaly harvest: 374 subjects and 374 CT series verified on fetch (DICOM), about 61.7 GB; whole body
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 374 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/psma_pet_ct_lesions; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 119,632 DICOM files, 58.8 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #303](https://github.com/OpenSpineConsortium/spine-datasets/issues/303), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_psma_pet_ct_lesions.json), [source](https://doi.org/10.7937/r7ep-3x37)

</details>

<details><summary><b>IDC `rider_lung_pet_ct`</b> (ct, download)</summary>

- What: IDC v24 collection rider_lung_pet_ct (TCIA doi:10.7937/k9/tcia.2015.ofip7tvm), tier 1 of the anomaly harvest: 117 subjects and 117 CT series verified on fetch (DICOM), about 18.1 GB; chest, abdomen, pelvis and whole body
- Licence: CC BY 3.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 117 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/rider_lung_pet_ct; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 35,229 DICOM files, 17.3 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #304](https://github.com/OpenSpineConsortium/spine-datasets/issues/304), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_rider_lung_pet_ct.json), [source](https://doi.org/10.7937/k9/tcia.2015.ofip7tvm)

</details>

<details><summary><b>IDC `spinal_multiple_myeloma_seg` (tier 2)</b> (ct, download)</summary>

- What: IDC v24 collection spinal_multiple_myeloma_seg (TCIA doi:10.7937/k4qv-hh78), tier 2 of the anomaly harvest: 67 subjects, about 33.8 GB raw plus screen; spine
- Licence: CC BY 4.0
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain after idc_tier2.csv is regenerated; the ranking's refusals: non-HU reconstruction (spectral map or suppression) 288
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/idc_spinal_multiple_myeloma_seg, 298 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), no fetch job in the listing's window; more than the record's 33.8 GB raw, which leaves out the screen products the folder holds beside it; fetched by the owner's chain, not the promoter, so no manifest covers it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #53](https://github.com/OpenSpineConsortium/spine-datasets/issues/53), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_spinal_multiple_myeloma_seg.json), [source](https://doi.org/10.7937/k4qv-hh78)

</details>

<details><summary><b>IDC `spine_mets_ct_seg` (tier 2)</b> (ct, download)</summary>

- What: IDC v24 collection spine_mets_ct_seg (TCIA doi:10.7937/kh36-ds04), tier 2 of the anomaly harvest: 54 subjects, about 17.2 GB raw plus screen; spine, abdomen and pelvis
- Licence: CC BY 4.0
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain after idc_tier2.csv is regenerated; the ranking's refusals: not a regularly spaced 3-D volume 1
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/idc_spine_mets_ct_seg, 19 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), no fetch job in the listing's window; beside the record's 17.2 GB raw; the sample report counts 35,527 DICOM files, 17.4 GB; fetched by the owner's chain, not the promoter, so no manifest covers it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #54](https://github.com/OpenSpineConsortium/spine-datasets/issues/54), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_spine_mets_ct_seg.json), [source](https://doi.org/10.7937/kh36-ds04)

</details>

<details><summary><b>IDC `tcga_blca`</b> (ct, download)</summary>

- What: IDC v24 collection tcga_blca (TCIA doi:10.7937/k9/tcia.2016.8lng8xdr), tier 1 of the anomaly harvest: 79 subjects and 79 CT series verified on fetch (DICOM), about 10 GB; chest, abdomen, pelvis and whole body
- Licence: CC BY 3.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 79 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/tcga_blca; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 19,484 DICOM files, 9.6 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #305](https://github.com/OpenSpineConsortium/spine-datasets/issues/305), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_tcga_blca.json), [source](https://doi.org/10.7937/k9/tcia.2016.8lng8xdr)

</details>

<details><summary><b>IDC `tcga_esca`</b> (ct, download)</summary>

- What: IDC v24 collection tcga_esca (TCIA doi:10.7937/k9/tcia.2016.vptnrgfy), tier 1 of the anomaly harvest: 16 subjects and 16 CT series verified on fetch (DICOM), about 2.4 GB; chest, abdomen and other
- Licence: CC BY 3.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 16 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/tcga_esca; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 4,738 DICOM files, 2.3 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #306](https://github.com/OpenSpineConsortium/spine-datasets/issues/306), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_tcga_esca.json), [source](https://doi.org/10.7937/k9/tcia.2016.vptnrgfy)

</details>

<details><summary><b>IDC `tcga_kirc`</b> (ct, download)</summary>

- What: IDC v24 collection tcga_kirc (TCIA doi:10.7937/k9/tcia.2016.v6pbvtdr), tier 1 of the anomaly harvest: 129 subjects and 129 CT series verified on fetch (DICOM), about 9.7 GB; chest, abdomen and pelvis
- Licence: CC BY 3.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 129 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/tcga_kirc; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 18,869 DICOM files, 9.3 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #307](https://github.com/OpenSpineConsortium/spine-datasets/issues/307), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_tcga_kirc.json), [source](https://doi.org/10.7937/k9/tcia.2016.v6pbvtdr)

</details>

<details><summary><b>IDC `tcga_lihc`</b> (ct, download)</summary>

- What: IDC v24 collection tcga_lihc (TCIA doi:10.7937/k9/tcia.2016.immqw8uq), tier 1 of the anomaly harvest: 42 subjects and 42 CT series verified on fetch (DICOM), about 4.9 GB; chest, abdomen and pelvis
- Licence: CC BY 3.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 42 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/tcga_lihc; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 9,429 DICOM files, 4.6 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #308](https://github.com/OpenSpineConsortium/spine-datasets/issues/308), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_tcga_lihc.json), [source](https://doi.org/10.7937/k9/tcia.2016.immqw8uq)

</details>

<details><summary><b>IDC `tcga_ov`</b> (ct, download)</summary>

- What: IDC v24 collection tcga_ov (TCIA doi:10.7937/k9/tcia.2016.ndo1mdfq), tier 1 of the anomaly harvest: 24 subjects and 24 CT series verified on fetch (DICOM), about 2.4 GB; chest, abdomen and pelvis
- Licence: CC BY 3.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 24 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/tcga_ov; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 4,687 DICOM files, 2.3 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #309](https://github.com/OpenSpineConsortium/spine-datasets/issues/309), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_tcga_ov.json), [source](https://doi.org/10.7937/k9/tcia.2016.ndo1mdfq)

</details>

<details><summary><b>IDC `tcga_stad`</b> (ct, download)</summary>

- What: IDC v24 collection tcga_stad (TCIA doi:10.7937/k9/tcia.2016.gdhl9kim), tier 1 of the anomaly harvest: 45 subjects and 45 CT series verified on fetch (DICOM), about 6.3 GB; abdomen
- Licence: CC BY 3.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 45 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/tcga_stad; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 12,189 DICOM files, 6.0 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #310](https://github.com/OpenSpineConsortium/spine-datasets/issues/310), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_tcga_stad.json), [source](https://doi.org/10.7937/k9/tcia.2016.gdhl9kim)

</details>

<details><summary><b>IDC `tcga_ucec`</b> (ct, download)</summary>

- What: IDC v24 collection tcga_ucec (TCIA doi:10.7937/k9/tcia.2016.gkj0zwac), tier 1 of the anomaly harvest: 38 subjects and 38 CT series verified on fetch (DICOM), about 4.1 GB; chest, abdomen, pelvis and other
- Licence: CC BY 3.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 38 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/tcga_ucec; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 7,900 DICOM files, 3.9 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #311](https://github.com/OpenSpineConsortium/spine-datasets/issues/311), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_tcga_ucec.json), [source](https://doi.org/10.7937/k9/tcia.2016.gkj0zwac)

</details>

<details><summary><b>IDC `varepop_apollo`</b> (ct, download)</summary>

- What: IDC v24 collection varepop_apollo (TCIA doi:10.7937/ghkn-md15), tier 1 of the anomaly harvest: 35 subjects and 35 CT series verified on fetch (DICOM), about 5.4 GB; chest, abdomen, pelvis and spine
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched through IDC in the first tier-1 launch of 2026-09-23 (acquisition job 40425851), as the data platform's manifest at bf1432f records, 35 series verified; on the grid at /rs/rs_grp_oschome/go2432/data/idc/raw/varepop_apollo; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the sample index of 2026-10-22 13:39, as the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) carries it, counts 10,376 DICOM files, 5.1 GB, in the folder; the listing itself shows the pooled idc folder at 707 GB
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #312](https://github.com/OpenSpineConsortium/spine-datasets/issues/312), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/idc_varepop_apollo.json), [source](https://doi.org/10.7937/ghkn-md15)

</details>

<details><summary><b>Kidney abnormality segmentation in thorax-abdomen CT</b> (ct, download)</summary>

- What: the kidney abnormality segmentation set of thorax-abdomen CT, Zenodo record 8014290; tier 1 of the anomaly harvest: its four image archives fetched, 215 CTs in MHA, one scan per file and the people not stated, about 38.35 GB in the catalogue; one of its CTs is the same voxels as one of PANORAMA's
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-24 held: fetched from Zenodo in the late tier-1 launch of 2026-09-24, as the data platform's manifest at bf1432f records (215 CTs); on the grid at /rs/rs_grp_oschome/go2432/data/kidney_thoraxabdomen, 71 GB by du in the data platform's census table of 2026-09-25; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) shows the folder at 76 GB, and the sample index of 2026-10-22 13:39 it carries counts 432 files, 70.7 GB, in it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #314](https://github.com/OpenSpineConsortium/spine-datasets/issues/314), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/kidney_thoraxabdomen.json), [source](https://zenodo.org/records/8014290)

</details>

<details><summary><b>NLST, the seeded 500-person pilot</b> (ct, download)</summary>

- What: 500 people of the National Lung Screening Trial in IDC v24 (TCIA doi:10.7937/tcia.hmq8-j677), drawn with a fixed seed from the data platform's NLST list; tier 1 of the anomaly harvest: 500 low-dose chest CT series, 89,363 DICOM instances, about 45.8 GB in the catalogue; these 500 are people of the full trial, which idc_nlst records, so a sum over both counts them twice
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched from IDC in the first tier-1 launch of 2026-09-23, as the data platform's manifest at bf1432f records (500 series; 500 CTs); on the grid at /rs/rs_grp_oschome/go2432/data/nlst_pilot, 69 GB by du in the data platform's census table of 2026-09-25; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) shows the folder at 74 GB, and the sample index of 2026-10-22 13:39 it carries counts 89,865 files, 68.5 GB, in it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #318](https://github.com/OpenSpineConsortium/spine-datasets/issues/318), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/nlst_pilot.json), [source](https://doi.org/10.7937/tcia.hmq8-j677)

</details>

<details><summary><b>PANORAMA public set (pancreas CE-CT)</b> (ct, download)</summary>

- What: PANORAMA's public set of contrast-enhanced pancreas CT, 2,238 scans of 2,224 patient ids, from Zenodo records 13715870, 13742336, 11034011 and 10999754; tier 1 of the anomaly harvest: its four image batches fetched, of which the data platform counts 2,024 CTs so far, and 1,950 subjects qualifying, about 194.2 GB in the source's catalogue (NIfTI); 274 of its MSD and NIH cases are inside AbdomenAtlas 3.0 Mini, and one of its CTs is the same voxels as one of the kidney thorax-abdomen set's
- Licence: CC BY-NC 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-24 held: fetched from Zenodo in the late tier-1 launch of 2026-09-24, as the data platform's manifest at bf1432f records (2,024 CTs); on the grid at /rs/rs_grp_oschome/go2432/data/panorama, 182 GB by du in the data platform's census table of 2026-09-25; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) shows the folder at 195 GB, and the sample index of 2026-10-22 13:39 it carries counts 2,240 files, 181.1 GB, in it
- Obstacles:
  - the owner's hand: the licence (CC BY-NC 4.0) is non-commercial; whether the project may use the copy on the grid under that term is his decision
- Next: the owner decides on the non-commercial term; the landing pass (#204) checks the files and their sizes
- Links: [task #319](https://github.com/OpenSpineConsortium/spine-datasets/issues/319), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/panorama.json), [source](https://zenodo.org/records/13715870)

</details>

<details><summary><b>PENGWIN 2026 peripelvic fracture CT (the public cases)</b> (ct, download)</summary>

- What: PENGWIN 2026, peripelvic fracture CT, 340 public cases, Zenodo record 19732767 published 2026-04-24; tier 1 of the anomaly harvest: all four parts fetched, 340 CTs in MHA, 308 once the 32 that duplicate CTPelvic1K's clinical subset are folded, about 19.57 GB in the catalogue
- Licence: CC BY-NC-SA 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-24 held: fetched from Zenodo in the late tier-1 launch of 2026-09-24, as the data platform's manifest at bf1432f records (340 CTs); on the grid at /rs/rs_grp_oschome/go2432/data/pengwin2026, 78 GB by du in the data platform's census table of 2026-09-25; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) shows the folder at 84 GB, and the sample index of 2026-10-22 13:39 it carries counts 1,022 files, 77.8 GB, in it
- Obstacles:
  - the owner's hand: the licence (CC BY-NC-SA 4.0) is non-commercial and share-alike; whether the project may use the copy on the grid under that term is his decision
- Next: the owner decides on the non-commercial term; the landing pass (#204) checks the files and their sizes
- Links: [task #320](https://github.com/OpenSpineConsortium/spine-datasets/issues/320), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/pengwin2026.json), [source](https://zenodo.org/records/19732767)

</details>

<details><summary><b>PENGWIN 2024 Task 2 synthetic X-rays</b> (ct, download)</summary>

- What: 50,000 DeepDRR images with 2D fragment masks from 100 pelvic-fracture CTs at 500 random C-arm poses each; projections 0250-0499 add up to 10 simulated K-wires and screws; pelvis, sacrum and the lower lumbar spine are in field; Zenodo doi:10.5281/zenodo.10913195, mirrored at huggingface.co/datasets/MedOtter/PENGWIN_Task2
- Licence: Creative Commons Attribution 4.0 International (the Zenodo record 10913195's licence line, read 2026-10-22)
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; a 2D product of the challenge's CTs already on the grid; the only large public DRR set rendered with real C-arm poses and simulated hardware, so pelvic-ring and sacral appearance under instruments without any patient
  - 2026-10-22 note: read the Zenodo record doi:10.5281/zenodo.10913195: open access, CC BY 4.0, 35.0 GB in one zip archive beside a utility script and a requirements file; contact person Benjamin Killeen (Johns Hopkins, with Unberath, Armand and the Beijing Jishuitan team); the challenge page names no further terms and asks no registration for the download
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/pengwin_task2_xrays, 35 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), no fetch job in the listing's window; the record states no size; the sample report shows one zip of 32.6 GB, not unpacked; fetched by the owner's chain, not the promoter, so no manifest covers it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #30](https://github.com/OpenSpineConsortium/spine-datasets/issues/30), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/pengwin_task2_xrays.json), [source](https://pengwin.grand-challenge.org/)

</details>

<details><summary><b>QUADRA_HC total-body FDG-PET/CT, healthy controls</b> (ct, download)</summary>

- What: QUADRA_HC, total-body FDG-PET/CT of 48 healthy controls on a long-axial scanner, test and retest, Zenodo record 16686025; tier 1 of the anomaly harvest: 96 attenuation CTs in the release, of which the data platform counts 48, about 20.18 GB in the catalogue (NIfTI); most of its CT paths hold a space, so a script quotes them
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-24 held: fetched from Zenodo in the late tier-1 launch of 2026-09-24, as the data platform's manifest at bf1432f records (48 CTs); on the grid at /rs/rs_grp_oschome/go2432/data/quadra_hc, 20 GB by du in the data platform's census table of 2026-09-25; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) shows the folder at 21 GB, and the sample index of 2026-10-22 13:39 it carries counts 966 files, 19.0 GB, in it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #321](https://github.com/OpenSpineConsortium/spine-datasets/issues/321), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/quadra_hc.json), [source](https://zenodo.org/records/16686025)

</details>

<details><summary><b>RibFrac (MICCAI 2020) chest CT</b> (ct, download)</summary>

- What: 660 chest CT volumes with rib fracture labels, and the RibSeg v2 and Moller rib masks
- Licence: CC BY-NC 4.0 (RibFrac); the Moller masks CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/ribfrac, downloaded from Zenodo, 2026-09-19 to 2026-09-23, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
- Next: not written yet
- Links: [task #322](https://github.com/OpenSpineConsortium/spine-datasets/issues/322), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/ribfrac.json), [source](https://zenodo.org/records/3893508)

</details>

<details><summary><b>RSNA 2022 cervical spine fracture CT (Kaggle)</b> (ct, account, the owner)</summary>

- What: 2,019 cervical spine CT studies with fracture labels by vertebra, C1 to C7, and vertebra segmentations for part of them; one zip of 203,318,086,447 bytes
- Licence: Kaggle competition rules (non-commercial); the terms for derived labels not recorded
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/rsna_2022_cspine, downloaded with the Kaggle command line on 2026-09-19, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
- Next: unpack the zip as a grid job and write the counts it holds
- Links: [task #323](https://github.com/OpenSpineConsortium/spine-datasets/issues/323), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/rsna_2022_cervical.json), [source](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection)

</details>

<details><summary><b>RSNA pulmonary embolism CT (RSPECT)</b> (ct, agreement, Gregory-Schwing-MD-PhD)</summary>

- What: 7,279 patients; a gated anomaly-harvest collection (group B7)
- Licence: a data use agreement (non-commercial)
- Status: held; task closed
- Steps so far:
  - 2026-10-21 researched: the owner joined the competition on Kaggle on 2026-10-21; the fetch command was given (kagglehub competition_download on a compute node, the Kaggle token read from ~/.fluorocap/credentials.env, never on a command line); the token the owner pasted into the chat is to be revoked and minted again; job id not yet recorded
  - 2026-10-21 granted: The owner joined the competition on Kaggle 2026-10-21; a fresh Kaggle token is needed (the pasted one is revoked); job id not yet recorded.
  - 2026-10-22 note: the gate word fetch rsna_rspect_pe (2026-10-22 06:55 UTC) found the token file ~/.fluorocap/credentials.env and queued job 40703031, which failed after 6 s with exit 1, a 403 from Kaggle: the competition's rules are not accepted on the account the token belongs to, gregoryschwingmdphd; the owner was asked on 2026-10-23 to accept them there, after which the word is sent again
  - 2026-10-23 note: the route is the kaggle command (kaggle competitions download in SchwingNet's grid/platform-fetch.sbatch), not kagglehub as the record said; its one-line 403 fits none of the shapes the status answer keeps, which is why job 40703031's answer showed only its start line, DP_FETCH_RC=1 and two lines withheld
  - 2026-10-23 note: the owner moved the grid's Kaggle key to the account gregoryschwing, which accepted the competition's rules; the gate word fetch rsna_rspect_pe queued job 40746778
  - 2026-10-23 held: job 40746778 ended COMPLETED, exit 0, after 1 h 25 min; the explore word's job 40749098 counted the landing: 1,937,447 .dcm files (980,108.8 MB), 3 .csv files (128.4 MB) and the downloaded zip (533,676.0 MB) still beside them, folders by study and series, test/ among them with 146,853 files; the DICOM and CSV files match the 1,937,450 files and 980.24 GB on the competition's data page; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: correction: the entry above read explore's counts as files on disk; they are the zip's members, which explore counts without unpacking. The owner said to delete the zip, and SchwingNet's gate word dropzip rsna_rspect_pe (job 40751186, 1 min 29 s) kept it, since none of its 1,937,450 members sits unpacked beside it, and freed nothing; the kaggle route never unpacked the download, and the status listing's 534 GB for the set is the zip
  - 2026-10-24 note: SchwingNet's gate word unpack rsna_rspect_pe (the owner's word of 2026-10-23, one job) ran job 40754822, COMPLETED, exit 0, after 1 h 58 min: all 1,937,450 members of the zip written beside it (980.2 GB), 0.0 GB still to land, as its report read at 08:16 UTC said
  - 2026-10-24 note: the gate word dropzip rsna_rspect_pe (the owner's word, one job) ran job 40774460, COMPLETED, exit 0, after 17 min 30 s; the status word at 17:15 UTC read the set at 981 GB on the data root, down from 1,514 GB, and the room up by 534 GB, so the 533.7 GB zip is gone and the unpacked files stay
- Next: the census counts the CT volumes
- Links: [task #88](https://github.com/OpenSpineConsortium/spine-datasets/issues/88), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/rsna_rspect.json), [source](https://www.kaggle.com/competitions/rsna-str-pulmonary-embolism-detection)

</details>

<details><summary><b>FDG-PET-CT-Lesions (autoPET), TCIA through NBIA</b> (ct, download)</summary>

- What: TCIA collection FDG-PET-CT-Lesions (autoPET; doi:10.7937/gkr0-xv29), which IDC v24 does not hold, fetched through NBIA; tier 1 of the anomaly harvest: 900 subjects and the 900 CT series of their whole-body PET/CT studies, 509,282 DICOM instances, about 250.6 GB in the source's catalogue; the same Tuebingen people appear in PanTSMini and may appear in ENHANCE.PET 1.6k (scidb_enhance_pet_1_6k)
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-23 held: fetched from NBIA in the first tier-1 launch of 2026-09-23, as the data platform's manifest at bf1432f records (900 series; 900 CTs); on the grid at /rs/rs_grp_oschome/go2432/data/tcia_fdg_pet_ct_lesions, 367 GB by du in the data platform's census table of 2026-09-25; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) shows the folder at 394 GB, and the sample index of 2026-10-22 13:39 it carries counts 511,084 files, 366.8 GB, in it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #325](https://github.com/OpenSpineConsortium/spine-datasets/issues/325), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/tcia_fdg_pet_ct_lesions.json), [source](https://doi.org/10.7937/gkr0-xv29)

</details>

<details><summary><b>TotalSegmentator datasets v2.0.1 and v3.0.0</b> (ct, download)</summary>

- What: whole-body CT with every vertebra among the segmented structures: v2.0.1, 1,228 volumes (Zenodo 10047292), and v3.0.0, 1,935 volumes (Zenodo 22688904); how many of v3's are v2's is not written here
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/totalsegmentator_v201; /rs/rs_grp_oschome/go2432/data/totalsegmentator_v300, downloaded from Zenodo and checked, 2026-09-14 and 2026-09-19, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
- Next: not written yet
- Links: [task #326](https://github.com/OpenSpineConsortium/spine-datasets/issues/326), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/totalsegmentator.json), [source](https://zenodo.org/records/10047292)

</details>

<details><summary><b>VerSe 2019 and 2020</b> (ct, download)</summary>

- What: 374 CT series of 355 subjects with vertebra masks and centroids
- Licence: CC BY-SA 4.0
- Status: held; task closed
- Steps so far:
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/versefusion/raw/VerSeFusion_data/raw, downloaded and joined into one tree in May 2026, before the shared tree and its promoter existed; the record written for the census (#178) from SchwingNet's registry
- Next: not written yet
- Links: [task #327](https://github.com/OpenSpineConsortium/spine-datasets/issues/327), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/verse.json), [source](https://github.com/anjany/verse)

</details>

<details><summary><b>VerSe 2D projections with soft labels (Zenodo 8115942)</b> (ct, download, aschehr)</summary>

- What: 2D projections of the central slices of VerSe 19 and 20 vertebrae, with soft labels from proposal-based non-expert annotation ('Annotating ambiguous images', 2023); count to confirm on the page (VerSe holds 4,505 vertebrae over 374 scans)
- Licence: Other (Open) (as the Zenodo page's licence line reads for version v1.0, published 2022-10-06, read 2026-10-22); the record's license.txt names no licence for its two VerSe files
- Status: held; task closed
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; its people are already in the v9 base (verse), so train-side only: a cheap extra render arm or a sanity check of the project's own VerSe renders
  - 2026-10-22 note: read on the Zenodo page: the record is the data of a data-centric benchmark of noisy and ambiguous labels over many image sets, licence line Other (Open); its license.txt gives CC BY-SA 4.0 for the benchmark repository and CC BY-NC-SA 4.0 for CIFAR-10H but names no licence for the two VerSe files, verse_blended-vps.zip (75.7 MB, md5 5802eac308309824957278d151055bbb) and verse_mask1-vps.zip (12.0 MB, md5 7a0a6d70171925d86e18dfa67058548f); no manifest written while their licence is unstated
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/verse_2d_projections, 5 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), no fetch job in the listing's window; the record states no size; the sample report shows 12 zips, 4.1 GB; fetched by the owner's chain, not the promoter, so no manifest covers it
- Obstacles:
  - the owner's hand: the licence of the two VerSe files is unstated (the record says Other (Open) and its license.txt does not name them; VerSe itself is CC BY-SA 4.0)
- Next: the owner decides whether the record's Other (Open) line with VerSe's own CC BY-SA 4.0 covers the two VerSe files; if so, a granted step in the history lets a manifest of those two files go in; a copy on the grid grants no use: the licence decision above still waits on the owner
- Links: [task #29](https://github.com/OpenSpineConsortium/spine-datasets/issues/29), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/verse_2d_projections.json), [source](https://zenodo.org/records/8115942)

</details>

<details><summary><b>WAW-TACE (HCC multiphase CT, Warsaw)</b> (ct, download)</summary>

- What: WAW-TACE, multiphase abdominal CT of 233 patients with hepatocellular carcinoma, from Warsaw, Zenodo record 12741586; tier 1 of the anomaly harvest: 854 scans in the release's four CT archives, of which the data platform counts 228 CTs, about 47.15 GB in the catalogue (NIfTI); it is the Medical University of Warsaw part of PanTSMini
- Licence: CC BY 4.0
- Status: held; task closed
- Steps so far:
  - 2026-09-24 held: fetched from Zenodo in the late tier-1 launch of 2026-09-24, as the data platform's manifest at bf1432f records (228 CTs); on the grid at /rs/rs_grp_oschome/go2432/data/waw_tace, 44 GB by du in the data platform's census table of 2026-09-25; fetched by the owner's chain, not the promoter, so no manifest here covers it
  - 2026-10-23 note: the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b) shows the folder at 48 GB, and the sample index of 2026-10-22 13:39 it carries counts 856 files, 43.9 GB, in it
- Next: the landing pass (#204) checks the files and their sizes
- Links: [task #329](https://github.com/OpenSpineConsortium/spine-datasets/issues/329), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/waw_tace.json), [source](https://zenodo.org/records/12741586)

</details>

<details><summary><b>TotalSegmentator task data &#x27;hip_implant&#x27; (71 CT)</b> (ct, letter)</summary>

- What: TotalSegmentator task data 'hip_implant', 71 CT, Zenodo 20272031 published 2026-05-18, about 9.0 GB; the same institution as TotalSegmentator v2/v3 (on disk) with no subject map
- Licence: CC BY 4.0
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: the owner's hand: ask the TotalSegmentator authors whether these subjects overlap the public v2/v3 release (planned in the data platform at bf1432f)
  - 2026-10-21 asked: The overlap question went 2026-10-21 09:40 UTC by the owner to the corresponding author; waiting for the answer. The set itself is CC BY 4.0 and needs only a grid job; until the answer comes it is treated as overlapping v2 and v3 (no new people).
  - 2026-10-22 note: Wasserthal replied 07:32 UTC: v2 is a complete subset of v3, ids unchanged, v3 only added subjects; nothing on the task sets, so they stay counted as overlapping; a follow-up is drafted
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/zenodo_ts_task_hip_implant, 10 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), no fetch job in the listing's window; beside the record's 9.03 GB; fetched by the owner's chain, not the promoter, so no manifest covers it
  - 2026-10-24 asked: the one-line follow-up went 03:05 UTC as the owner's reply to Wasserthal alone: are the three task sets' subjects among the v2 and v3 subjects, with the same identifiers, or new people; a yes or no is enough
- Obstacles:
  - the overlap question of 2026-10-21 was answered on 2026-10-22 for v2 and v3 only; the task sets stay counted as overlapping v2 and v3 until the follow-up of 2026-10-24 is answered
- Next: wait for Wasserthal's answer to the follow-up of 2026-10-24 03:05 UTC; record it on the task sets here; the landing pass (#204) checks the files
- Links: [task #66](https://github.com/OpenSpineConsortium/spine-datasets/issues/66), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/zenodo_ts_task_hip_implant.json), [source](https://zenodo.org/records/20272031)

</details>

<details><summary><b>TotalSegmentator task data &#x27;liver_lesions&#x27; (842 CT)</b> (ct, letter)</summary>

- What: TotalSegmentator task data 'liver_lesions', 842 CT, Zenodo 20272572 published 2026-05-18, about 38.9 GB; the same institution as TotalSegmentator v2/v3 (on disk) with no subject map
- Licence: CC BY 4.0
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: the owner's hand: ask the TotalSegmentator authors whether these subjects overlap the public v2/v3 release (planned in the data platform at bf1432f)
  - 2026-10-21 asked: The overlap question went 2026-10-21 09:40 UTC by the owner to the corresponding author; waiting for the answer. The set itself is CC BY 4.0 and needs only a grid job; until the answer comes it is treated as overlapping v2 and v3 (no new people).
  - 2026-10-22 note: Wasserthal replied 07:32 UTC: v2 is a complete subset of v3, ids unchanged, v3 only added subjects; nothing on the task sets, so they stay counted as overlapping; a follow-up is drafted
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/zenodo_ts_task_liver_lesions, 40 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), no fetch job in the listing's window; beside the record's 38.87 GB; fetched by the owner's chain, not the promoter, so no manifest covers it
  - 2026-10-24 asked: the one-line follow-up went 03:05 UTC as the owner's reply to Wasserthal alone: are the three task sets' subjects among the v2 and v3 subjects, with the same identifiers, or new people; a yes or no is enough
- Obstacles:
  - the overlap question of 2026-10-21 was answered on 2026-10-22 for v2 and v3 only; the task sets stay counted as overlapping v2 and v3 until the follow-up of 2026-10-24 is answered
- Next: wait for Wasserthal's answer to the follow-up of 2026-10-24 03:05 UTC; record it on the task sets here; the landing pass (#204) checks the files
- Links: [task #67](https://github.com/OpenSpineConsortium/spine-datasets/issues/67), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/zenodo_ts_task_liver_lesions.json), [source](https://zenodo.org/records/20272572)

</details>

<details><summary><b>TotalSegmentator task data &#x27;pleural_pericard_effusion&#x27; (600 CT)</b> (ct, letter)</summary>

- What: TotalSegmentator task data 'pleural_pericard_effusion', 600 CT, Zenodo 20272295 published 2026-05-18, about 9.0 GB; the same institution as TotalSegmentator v2/v3 (on disk) with no subject map
- Licence: CC BY 4.0
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: the owner's hand: ask the TotalSegmentator authors whether these subjects overlap the public v2/v3 release (planned in the data platform at bf1432f)
  - 2026-10-21 asked: The overlap question went 2026-10-21 09:40 UTC by the owner to the corresponding author; waiting for the answer. The set itself is CC BY 4.0 and needs only a grid job; until the answer comes it is treated as overlapping v2 and v3 (no new people).
  - 2026-10-22 note: Wasserthal replied 07:32 UTC: v2 is a complete subset of v3, ids unchanged, v3 only added subjects; nothing on the task sets, so they stay counted as overlapping; a follow-up is drafted
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/zenodo_ts_task_pleural_effusion, 10 GB in the status listing of 2026-10-23 02:05 UTC (symphony-template grid branch, 26f3bde), no fetch job in the listing's window; beside the record's 8.99 GB; fetched by the owner's chain, not the promoter, so no manifest covers it
  - 2026-10-24 asked: the one-line follow-up went 03:05 UTC as the owner's reply to Wasserthal alone: are the three task sets' subjects among the v2 and v3 subjects, with the same identifiers, or new people; a yes or no is enough
- Obstacles:
  - the overlap question of 2026-10-21 was answered on 2026-10-22 for v2 and v3 only; the task sets stay counted as overlapping v2 and v3 until the follow-up of 2026-10-24 is answered
- Next: wait for Wasserthal's answer to the follow-up of 2026-10-24 03:05 UTC; record it on the task sets here; the landing pass (#204) checks the files
- Links: [task #68](https://github.com/OpenSpineConsortium/spine-datasets/issues/68), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/zenodo_ts_task_pleural_effusion.json), [source](https://zenodo.org/records/20272295)

</details>

<details><summary><b>VSDFullBody: post-mortem whole-body CT, forensic institutes Bern and Zurich</b> (ct, download)</summary>

- What: VSDFullBody post-mortem whole-body CT, 100 subjects, forensic institutes Bern and Zurich, Zenodo 8270365 published 2013-11-12, about 116 GB; the mirror notes duplicate CT datasets (100 new of 109 files)
- Licence: Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Switzerland (CC BY-NC-SA 3.0 CH), the Zenodo record 8270365's licence line, read 2026-10-22
- Status: held; task open
- Steps so far:
  - 2026-10-21 researched: planned in the data platform at bf1432f; fetch job in the 2026-10-21 chain
  - 2026-10-22 note: read the Zenodo record 8270365: open access, CC BY-NC-SA 3.0 CH, 109 zip archives, 116.3 GB, each with an md5; a mirror of the Virtual Skeleton Database's VSDFullBody, made without changes because the SMIR site was hard to reach, by an uploader not tied to SMIR; creator Michael Kistler (ISTB, University of Bern); shared after approval by the Cantonal Ethics Committee Bern; 024.zip (142 bytes) and z014, z052 and z059 (144 bytes each) are empty placeholders, and VSD_Comments.xlsx logs duplicate subjects
  - 2026-10-23 held: on the grid at /rs/rs_grp_oschome/go2432/data/zenodo_vsd_fullbody, 253 GB in the status listing of 2026-10-23 09:29 UTC (symphony-template grid branch, 1c8246b), job 40697705 COMPLETED after 7 h 14 min; more than the record's 116.3 GB of archives, which the folder may hold unpacked beside them, for the landing pass to read; fetched by the owner's chain, not the promoter, so no manifest covers it
- Obstacles:
  - the owner's hand: the licence is non-commercial and share-alike; whether the project takes the set under it is the owner's decision
- Next: the owner decides on the non-commercial, share-alike term, since a copy on the grid grants no use; the landing pass (#204) checks the files and their sizes and leaves out the four placeholder archives
- Links: [task #59](https://github.com/OpenSpineConsortium/spine-datasets/issues/59), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/zenodo_vsd_fullbody.json), [source](https://zenodo.org/records/8270365)

</details>

<details><summary><b>Veterinary: pig lower limb CT, CBCT and planar images (Goswami 2020, IEEE DataPort)</b> (future, account, Gregory-Schwing-MD-PhD)</summary>

- What: seven zips, about 205 MB: the CT of a pig lower limb phantom, two CBCTs (with and without soft tissue), 7 C-arm planar projections at different poses in each condition and the registration matrices, from 'A new workflow for image-guided intraoperative electron radiotherapy' (IEEE Access 2020, doi 10.21227/gxpd-d998); not the LevelCheck pig study this record once named, and no spine
- Licence: IEEE DataPort open access
- Status: held; task closed
- Steps so far:
  - 2026-10-21 researched: the owner's future direction of 2026-10-20: expand the workflow into veterinary medicine; the zips sit in spine-program's archive, excluded from the record, and the set is open on IEEE DataPort; the Mendeley canine thoracic set (canine_thoracic_vhs) stands beside it since the sweep of 2026-10-21
  - 2026-10-22 note: owner's sitting prepared: IEEE DataPort lists seven zips (about 186 MB) open to any logged-in user with a free IEEE account, though its access box also names a DataPort subscription; no licence line on the page
  - 2026-10-22 note: the owner confirmed the download opens free with a signed-in IEEE account and has the seven zips; no grid job can sign in to IEEE as him
  - 2026-10-22 fetching: the seven zips came down on the grid with the owner's IEEE DataPort login on his word of 23:17 UTC, into the lab's data folder (/rs/rs_grp_oschome/go2432/data/veterinary_pig_levelcheck/raw); every size matches the page and every zip passes unzip -t; meta/ holds MD5SUMS.txt, the page text and SOURCE.txt (DOI 10.21227/gxpd-d998)
  - 2026-10-22 note: the seven zips and meta/ copied into /rs/rs_grp_oschome/shared/datasets/veterinary_pig_levelcheck/ by Slurm job 40731458 on asx1, every file passing md5sum -c against MD5SUMS.txt; the files came through a login, so no public-link manifest exists for the promoter to replay
  - 2026-10-23 held: the zips came through the owner's login and were copied into the shared tree by hand (job 40731458), so no promoter manifest covers them and the status is held; the name and contents corrected from SchwingNet's registry: the pig lower-limb set of IEEE Access 2020, not the LevelCheck pig study, and no spine
- Next: nothing to fetch: the seven zips are in the shared tree, checked against MD5SUMS.txt; unzip as a grid job on the owner's word before any use
- Links: [task #22](https://github.com/OpenSpineConsortium/spine-datasets/issues/22), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/veterinary_pig_levelcheck.json), [source](https://ieee-dataport.org/open-access/pig-data-2d-3d-intensity-based-registration)

</details>


<a id="needs-owner"></a>

## Needs the owner (13)

A signature, a fee, an account or a budget decision.

<details><summary><b>CAMS-Knee (ETH Zurich and Charite Berlin, J Biomech 2017)</b> (video, agreement, the owner)</summary>

- What: 6 people with instrumented total knee replacements (Charite Berlin), measured at ETH Zurich in June 2014 during level walking, stair and ramp descent, sitting down and standing up, squats and standing: the joint loads the implants measured, a moving fluoroscope following the knee (pulsed at 25 Hz, 1000 x 1000 pixels at 12 bits, a 30.5 cm field) whose images come registered to the implant components, whole-body markers, force plates, 16-channel EMG and camera video (Taylor et al., J Biomech 2017;65:32-39, doi:10.1016/j.jbiomech.2017.09.022); the same form offers Stan (Dreyer et al., J Biomech 2022;141:111171), a reference subject made from these data, whose files are loads and kinematics alone, with no images, so it has no record of its own
- Licence: the CAMS-Knee licence agreement, which the requesting institution signs: non-commercial, scientific use without any commercial benefit, at the registered institute only, not passed on to third parties (as the data request page reads, read 2026-10-23)
- Status: needs-owner; task open
- Steps so far:
  - 2026-10-23 researched: found by checking the owner's list of fluoroscopy sets of 2026-10-23; not requested; behind a form and the CAMS-Knee licence agreement, which the requesting institution signs, for scientific use without commercial benefit
- Obstacles:
  - the owner's hand: the agreement allows scientific use without commercial benefit, at the registered institute only; whether the project takes the set under it is the owner's decision, and the agreement needs Wayne State's signature
- Next: the owner decides on the agreement's terms; if they are taken, the form goes in with the agreement and a project description
- Links: [task #260](https://github.com/OpenSpineConsortium/spine-datasets/issues/260), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/cams_knee.json), [source](https://cams-knee.orthoload.com/data/data-request/)

</details>

<details><summary><b>Guide3D (ACCV 2024, AIRVLab)</b> (video, download, aschehr)</summary>

- What: more than 8,700 bi-planar fluoroscopic frames of guidewires in a vascular phantom, two guidewires, varied flow
- Licence: CC BY-NC 4.0 (cc-by-nc-4.0, as the Hugging Face dataset airvlab/guide3d's licence line reads, read 2026-10-22)
- Status: needs-owner; task closed
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; open per the paper, licence to confirm on the page; bi-planar real fluoroscopy geometry from one device, domain and calibration value only
  - 2026-10-22 note: licence read on https://huggingface.co/datasets/airvlab/guide3d, the dataset the project page links: cc-by-nc-4.0; the project page itself names no licence and counts 8,746 samples (4,148 with fluid, 4,598 without); no manifest written, since the check takes no non-commercial licence
- Obstacles:
  - the owner's hand: the licence is non-commercial (CC BY-NC 4.0), which the manifest check refuses; whether the project takes the set under that term is his decision
- Next: the owner decides on the non-commercial term; if he takes it, a granted step in the history lets a manifest of the Hugging Face files go in
- Links: [task #40](https://github.com/OpenSpineConsortium/spine-datasets/issues/40), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/guide3d.json), [source](https://airvlab.github.io/guide3d/)

</details>

<details><summary><b>Veriserum (ETH Zurich, MICCAI 2025)</b> (video, download, aschehr)</summary>

- What: about 110,000 dual-plane fluoroscopic images of knee implant phantoms with registered poses, 200 with manual registration (ETH Research Collection doi:10.3929/ethz-b-000701146)
- Licence: In Copyright - Non-Commercial Use Permitted (as the ETH Research Collection record's rights line reads, read 2026-10-22)
- Status: needs-owner; task closed
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; freely accessible per the authors, licence to confirm on the page; real flat-panel fluoroscopy of metal implants at scale, which the project otherwise learns only from simulation
  - 2026-10-22 note: rights line read on the ETH Research Collection record doi:10.3929/ethz-b-000701146: In Copyright - Non-Commercial Use Permitted (rightsstatements.org InC-NC 1.0); the project page says 'Free for academic and research use'; the record's file list did not load (429), so no sizes are noted; no manifest written, since the check takes no non-commercial term
- Obstacles:
  - the owner's hand: the rights line is In Copyright with non-commercial use permitted, not an open licence; whether the project takes the set under it is his decision
- Next: the owner decides on the non-commercial term; if he takes it, a granted step in the history lets a manifest of the record's files go in
- Links: [task #41](https://github.com/OpenSpineConsortium/spine-datasets/issues/41), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/veriserum.json), [source](https://movement.ethz.ch/data-repository/veriserum.html)

</details>

<details><summary><b>BIMCV COVID-19+ chest films (IEEE DataPort)</b> (films, account, the owner)</summary>

- What: chest radiographs, laterals among them, and CTs of COVID-19 patients from the hospitals of the Valencian region (BIMCV COVID-19+), about 389 GB in all
- Licence: not recorded; read on the IEEE DataPort page after the login
- Status: needs-owner; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; open access on IEEE DataPort (doi:10.21227/w3aw-rv39) behind a free IEEE login; tar.gz parts of about 389 GB in all, radiographs and CTs together
- Obstacles:
  - the owner's hand: the free IEEE account, and the space decision (about 389 GB)
- Next: the owner opens the IEEE account and says how much of the set to fetch
- Links: [task #111](https://github.com/OpenSpineConsortium/spine-datasets/issues/111), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/bimcv_covid19.json), [source](https://ieee-dataport.org/open-access/bimcv-covid-19-large-annotated-dataset-rx-and-ct-images-covid-19-patients)

</details>

<details><summary><b>BRAX Brazilian chest films (PhysioNet)</b> (films, agreement, the owner)</summary>

- What: 40,967 chest radiographs from 24,959 studies at Hospital Israelita Albert Einstein, Sao Paulo, Brazil, frontal and lateral views, labelled with 14 radiological findings
- Licence: PhysioNet credentialed access (the licence line read on the project page)
- Status: needs-owner; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; PhysioNet credentialed access (Scientific Data 2022, PMC9364309); 24,959 studies and 40,967 images, frontal and lateral, from Hospital Israelita Albert Einstein, Sao Paulo
- Obstacles:
  - the owner's hand: the PhysioNet data use agreement; then PhysioNet's review of his CITI course record
- Next: the owner signs the agreement on the project page; then the grid fetch
- Links: [task #110](https://github.com/OpenSpineConsortium/spine-datasets/issues/110), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/brax.json), [source](https://physionet.org/content/brax/)

</details>

<details><summary><b>IEEE DataPort lateral full-spine X-ray dataset (236 films)</b> (films, account, the owner)</summary>

- What: 236 lateral whole-spine standing films, cervical spine to pelvis, 236 JPG files, 1.3 GB
- Licence: not recorded; downloaded under an IEEE DataPort subscription
- Status: needs-owner; task open
- Steps so far:
  - 2026-10-23 note: a copy of the 236 JPG (1.3 GB) in a project folder of the owner's grid home, as the data platform recorded it on 2026-09-13, downloaded under an IEEE DataPort subscription before 2026-09-16, before the shared tree and its promoter existed; neither the status word of 2026-10-23 nor the sample index of 2026-10-22 lists the home, so it is not counted held until a listing shows it under the data root or the shared tree; the record written for the census (#178)
- Obstacles:
  - the licence line is still to confirm on the source's page
  - the copy is the data platform's record of 2026-09-13, in a project folder of the owner's grid home that no listing has shown yet
  - the grid job that lists and moves it waits for the owner's word
- Next: the owner's word for one grid job that lists the copy and puts it, with its checksums, under the data root or the shared tree; then status held with that path
- Links: [task #313](https://github.com/OpenSpineConsortium/spine-datasets/issues/313), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/ieee_dataport_lateral_236.json), [source](https://ieee-dataport.org/documents/lateral-full-spine-x-ray-image-dataset)

</details>

<details><summary><b>Kaggle scoliosis YOLOv5 annotated spine X-ray set (salmankey)</b> (films, account, the owner)</summary>

- What: AP spine films with YOLO boxes on vertebrae and curve regions; count, source and whether the people are AASCE's to confirm on the page
- Licence: MIT in the Kaggle metadata field, while the description's own licence section says CC BY 4.0 (both read from Kaggle's dataset API on 2026-10-22); either is open
- Status: needs-owner; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; its origin is unstated, so it may be a relabel of AASCE (aasce): every image is hash-checked (filename or pixel hash) against the AASCE copy on the grid before any use, and a match excludes it as new people
  - 2026-10-22 note: read from Kaggle's dataset API: owner Muhammad Salman (salmankey), last updated 2025-11-07, 251,996,951 bytes; licence field MIT, description says CC BY 4.0; the images were boxed in Roboflow (the Roboflow link in the description is a placeholder) and the set carries augmented copies (rotation, brightness, flips, crops, noise); where the films came from is not stated anywhere, so the AASCE hash check stays; a Kaggle download needs a Kaggle login and its token
- Obstacles:
  - the owner's hand: a Kaggle download needs a Kaggle login and its token, which never enters this repository
  - the films' origin is unstated, so every image is hash-checked against the AASCE copy on the grid before any use; the augmented copies are dropped or kept apart as copies of one person
- Next: the owner fetches with the owner's Kaggle account as a grid job; then the AASCE hash check, whose match makes it a relabel of aasce
- Links: [task #23](https://github.com/OpenSpineConsortium/spine-datasets/issues/23), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/kaggle_scoliosis_yolov5.json), [source](https://www.kaggle.com/datasets/salmankey/scoliosis-yolov5-annotated-spine-x-ray-dataset)

</details>

<details><summary><b>MrOS lateral spine radiographs (Osteoporotic Fractures in Men)</b> (films, form)</summary>

- What: lateral thoracic and lumbar films of 5,994 men at six US centres, two visits (2000-2002 and about 4.6 years later), with Genant semi-quantitative vertebral fracture grades per vertebra; one deep-learning study used 4,461 subjects and 15,524 films; the image counts and the request steps to confirm on the page
- Licence: an NIA Outgoing Human Data Transfer Agreement signed by the PI and Wayne State's Signing Official: non-profit research on the approved project only, no redistribution, no re-identification, acknowledgement, 12 months renewable, destruction certified at the end
- Status: needs-owner; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; a research data request through the MrOS coordinating centre (an online application with a proposal), not sent; the images are not on dbGaP, whose phs000373 covers genotypes (to confirm on the page); older osteoporotic spines with compression fractures, the anatomy the C-arm sees in kyphoplasty
  - 2026-10-22 asked: the owner emailed MrOSData@ucsf.edu for authorization to register at MrOS Online; the coordinating centre answered the same day that MrOS Online is closed to registrations for new NIH requirements and that the study images are being added to the NIA Aging Research Biobank, where the request goes
  - 2026-10-24 note: the Biobank's request process read from its pages (symphony-template docs/research/nia-aging-research-biobank-requests.md); one Request for Materials for MrOS and SOF drafted for the owner, not submitted
- Obstacles:
  - the owner's hand: who files as Requester/PI (the Biobank takes only a permanent tenure-track professor or senior researcher; a trainee goes under Authorized Users)
  - the owner's and Wayne State tech transfer's answer to the form's required commercial-purpose question, since the agreement bars commercial use
  - an IRB determination covering data under an NIA transfer agreement (HPR 2026-269 covers only data without an agreement), a supplement as HPR 2026-330 was
  - the Biobank's form lists the study for data only, not images, on 2026-10-24; the package size is not published and is asked in the request's Comments before any download
- Next: the owner settles who files, the commercial-purpose answer and the IRB supplement, then submits the drafted Biobank request
- Links: [task #9](https://github.com/OpenSpineConsortium/spine-datasets/issues/9), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/mros_lateral_spine.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/mros_lateral_spine.md), [source](https://agingresearchbiobank.nia.nih.gov/)

</details>

<details><summary><b>Open-i Indiana chest collection</b> (films, download)</summary>

- What: 7,470 chest radiographs of 3,955 studies with reports, frontal and lateral pairs (the Indiana University collection on Open-i)
- Licence: CC BY-NC-ND 4.0 as two mirrors state (Hugging Face ykumards/open-i and Kaggle raddar/chest-xrays-indiana-university, read 2026-10-22); the Open-i FAQ itself was under maintenance, to confirm on the page
- Status: needs-owner; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; open, no agreement; small but frictionless lateral chest films for a thoracic-lateral probe before the gated sets arrive
  - 2026-10-22 note: the Open-i FAQ answered only a maintenance notice on 2026-10-22; two mirrors give the collection's licence as CC BY-NC-ND 4.0 (the Kaggle mirror is 14,185,071,106 bytes, its images resized to 2048 on the shorter side, so the archives from NLM itself are the copy to fetch); the record's 'open, no agreement' was the FAQ's word on access, not on use
- Obstacles:
  - the owner's hand: the licence is non-commercial and no-derivatives as the mirrors state it; whether the project takes the set under it is the owner's decision
  - the Open-i FAQ was under maintenance on 2026-10-22, so the licence and the archive addresses are still to read on NLM's own page
- Next: a collaborator reads the licence and the archive addresses on the Open-i FAQ once it is back; the owner decides on the non-commercial, no-derivatives term; if the owner takes it, a granted step lets a manifest of NLM's own archives go in
- Links: [task #35](https://github.com/OpenSpineConsortium/spine-datasets/issues/35), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/open_i_chest.json), [source](https://openi.nlm.nih.gov/faq)

</details>

<details><summary><b>SOF lateral spine radiographs (Study of Osteoporotic Fractures)</b> (films, form)</summary>

- What: the women's counterpart of MrOS: lateral thoracolumbar films at several visits, about 9,700 women, Genant grading per vertebra; counts to confirm on the page
- Licence: an NIA Outgoing Human Data Transfer Agreement signed by the PI and Wayne State's Signing Official: non-profit research on the approved project only, no redistribution, no re-identification, acknowledgement, 12 months renewable, destruction certified at the end
- Status: needs-owner; task open
- Steps so far:
  - 2026-10-21 researched: found by the sweep of 2026-10-21; not fetched; the same kind of request as MrOS (to confirm on the page), not sent; with MrOS the largest level-labelled lateral spine film resource that exists
  - 2026-10-22 asked: the owner emailed SOFData@ucsf.edu for authorization to register at SOF Online; the coordinating centre answered the same day that SOF Online is closed to registrations for new NIH requirements and that the study images are being added to the NIA Aging Research Biobank, where the request goes
  - 2026-10-24 note: the Biobank's request process read from its pages (symphony-template docs/research/nia-aging-research-biobank-requests.md); one Request for Materials for MrOS and SOF drafted for the owner, not submitted
- Obstacles:
  - the owner's hand: who files as Requester/PI (the Biobank takes only a permanent tenure-track professor or senior researcher; a trainee goes under Authorized Users)
  - the owner's and Wayne State tech transfer's answer to the form's required commercial-purpose question, since the agreement bars commercial use
  - an IRB determination covering data under an NIA transfer agreement (HPR 2026-269 covers only data without an agreement), a supplement as HPR 2026-330 was
  - the Biobank's form lists the study for data only, not images, on 2026-10-24; the package size is not published and is asked in the request's Comments before any download
- Next: the owner settles who files, the commercial-purpose answer and the IRB supplement, then submits the drafted Biobank request
- Links: [task #10](https://github.com/OpenSpineConsortium/spine-datasets/issues/10), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/sof_lateral_spine.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/sof_lateral_spine.md), [source](https://agingresearchbiobank.nia.nih.gov/)

</details>

<details><summary><b>MAGIC-CT (Zenodo)</b> (ct, agreement, the owner)</summary>

- What: 562 CTs; a gated anomaly-harvest collection (group B7)
- Licence: a data use agreement (non-commercial)
- Status: needs-owner; task open
- Steps so far:
  - 2026-10-21 researched: an agreement stands in front of the data; none signed; the Zenodo record (v2, 2026) is labelled CC0 yet carries a data use agreement (no re-identification, no sharing), and names maxim.popov@nu.edu.kz as contact; the record counts 562 patients, 39.1 GB, 492 with reports
  - 2026-10-21 note: the owner recalls applying for this agreement; on 2026-10-21 no application, agreement or answer about MAGIC-CT was found in his Wayne State Outlook or his Gmail, so the application is recorded as not yet made; the Zenodo record (v2) still asks for an application with proof of a human-subjects course, sent to the contact it names, before its agreement holds
- Obstacles:
  - the owner's hand: the application with proof of his human-subjects course, and the agreement's terms
- Next: the owner sends the application the Zenodo record asks for, or forwards its confirmation if he already did; then the 39.1 GB is fetched as a Slurm job and checked against the record's md5 sums
- Links: [task #7](https://github.com/OpenSpineConsortium/spine-datasets/issues/7), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/magic_ct.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/magic_ct.md), [source](https://zenodo.org/records/18389015)

</details>

<details><summary><b>Stanford AIMI INSPECT chest CT</b> (ct, agreement, the owner)</summary>

- What: 19,402 patients; a gated anomaly-harvest collection (group B7)
- Licence: a data use agreement (non-commercial)
- Status: needs-owner; task open
- Steps so far:
  - 2026-10-21 researched: an agreement stands in front of the data; none signed
  - 2026-10-21 note: dropped by the owner on 2026-10-21: too large for the shared volume (19,402 patients' CTs); never asked for, and taken up again only on his word
  - 2026-10-21 note: not dropped: the owner holds the set pending more storage (his correction of 2026-10-21 20:20 UTC); the word dropped in the note above is withdrawn
- Obstacles:
  - pending more storage: the shared volume has no room for it yet (the owner, 2026-10-21)
  - the owner's hand: the AIMI research use agreement click-through; the Azure URL that follows is a credential
- Next: when there is more storage, the owner signs the AIMI agreement and says how much of the set the volume takes; then the fetch runs as a Slurm job
- Links: [task #19](https://github.com/OpenSpineConsortium/spine-datasets/issues/19), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/stanford_aimi_inspect.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/stanford_aimi_inspect.md), [source](https://stanfordaimi.azurewebsites.net/)

</details>

<details><summary><b>Stanford AIMI Merlin abdominal CT</b> (ct, agreement, the owner)</summary>

- What: 25,494 CT of 18,317 patients; a gated anomaly-harvest collection (group B7)
- Licence: a data use agreement (non-commercial)
- Status: needs-owner; task open
- Steps so far:
  - 2026-10-21 researched: an agreement stands in front of the data; none signed
  - 2026-10-21 note: dropped by the owner on 2026-10-21: too large for the shared volume (25,494 CTs); never asked for, and taken up again only on his word
  - 2026-10-21 note: not dropped: the owner holds the set pending more storage (his correction of 2026-10-21 20:20 UTC); the word dropped in the note above is withdrawn
- Obstacles:
  - pending more storage: the shared volume has no room for it yet (the owner, 2026-10-21)
  - the owner's hand: the AIMI research use agreement click-through; the Azure URL that follows is a credential and goes in a mode-0600 file on the grid
- Next: when there is more storage, the owner signs the AIMI agreement and says how much of the set the volume takes; then the fetch runs as a Slurm job
- Links: [task #18](https://github.com/OpenSpineConsortium/spine-datasets/issues/18), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/stanford_aimi_merlin.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/stanford_aimi_merlin.md), [source](https://stanfordaimi.azurewebsites.net/datasets/60b9c7ff-877b-48ce-96c3-0194c8205c40)

</details>


<a id="refused"></a>

## Refused (2)

The source said no, or the terms cannot be met.

<details><summary><b>Balgrist ex-vivo lumbar CT plus C-arm (Jecklin)</b> (fluoro, letter)</summary>

- What: cadaver lumbar CT with real C-arm frames
- Licence: not recorded
- Status: refused; task closed
- Steps so far:
  - 2026-09-21 asked: Letter of 2026-09-21 sent 2026-10-20 by the owner to Philipp Fuernstahl and rocs@balgrist.ch (the message to Sascha Jecklin bounced); the resend through the ROCS contact form is pending; waiting for the answer.
  - 2026-10-21 researched: request drafted 2026-09-21, never sent; the authors' group is ROCS (Research in Orthopedic Computer Science, Balgrist, head Philipp Fuernstahl), whose group address is rocs@balgrist.ch; the paper is arXiv:2401.16027 (Medical Image Analysis 2024); the set is restricted for pending patents
  - 2026-10-21 refused: Fuernstahl replied 05:52 UTC: licensed out to a startup, proprietary, cannot be shared
- Obstacles:
  - proprietary: licensed by the University of Zurich to a startup
- Next: none; closed as refused
- Links: [task #69](https://github.com/OpenSpineConsortium/spine-datasets/issues/69), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/balgrist_lumbar.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/balgrist_lumbar.md), [source](https://rocs.balgrist.ch/en/contact)

</details>

<details><summary><b>LevelCheck clinical cohort (Johns Hopkins, Siewerdsen group)</b> (fluoro, letter)</summary>

- What: 178 patients with preoperative CT and 398 intraoperative radiographs (De Silva et al., Spine 2016), plus Ketcha et al. 2017's 24 thoracolumbar patients with 61 Carestream DRX-1 radiographs, and the 62-image reader set of Manbachi et al. 2018; neither paper has a data statement
- Licence: not recorded; a data use agreement with the PI is the route
- Status: refused; task open
- Steps so far:
  - 2026-10-21 researched: a letter sent 2026-10-21; no record in SchwingNet's registry yet
  - 2026-10-21 asked: Letter sent 2026-10-21 09:40 UTC by the owner to the LevelCheck authors; waiting for the answer.
  - 2026-10-21 note: Siewerdsen replied 12:48 UTC: the data are at Johns Hopkins, never made public; ask Ali Uneri (JHU faculty)
  - 2026-10-21 asked: follow-up sent 13:37 UTC to Ali Uneri, JHU BME (address from a JHU BME page), Siewerdsen copied
  - 2026-10-23 note: the link is De Silva et al.'s paper on PubMed Central (PMC5045321, Spine 2016), whose index entry read on 2026-10-23 gives 398 radiographs and 178 CT, as the record does; the record's counts add Ketcha et al. 2017's
  - 2026-10-23 refused: Uneri replied 16:00 UTC: the study's IRB expired years ago and sharing would be hard even with approval; he suggested the Harms Study Group (hsg.settingscoliosisstraight.org) and offered an introduction to its administrative team
  - 2026-10-23 note: the owner's reply to Uneri went 16:56 UTC: LevelCheck is let go, the introduction to the Harms Study Group accepted; the lead continues on hsg_ais_registry
- Obstacles:
  - the LevelCheck IRB at Johns Hopkins expired years ago; no sharing without a new approval, which Uneri called difficult
- Next: none for this set; the owner's reply to Uneri went 2026-10-23 16:56 UTC, and the Harms Study Group lead is followed on hsg_ais_registry
- Links: [task #60](https://github.com/OpenSpineConsortium/spine-datasets/issues/60), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/levelcheck_jhu.json), [letter](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/letters/levelcheck_jhu.md), [source](https://pmc.ncbi.nlm.nih.gov/articles/PMC5045321/)

</details>


<a id="later"></a>

## Later (1)

Embargoed, or nothing can be done yet.

<details><summary><b>COBRA2026 embargoed cases</b> (projections, download)</summary>

- What: the challenge's held-back cases
- Licence: CC BY-NC 4.0
- Status: todo; task open
- Steps so far:
  - 2026-10-21 researched: released on 2032-03-01
- Obstacles:
  - embargoed; the record says until when
- Next: nothing until the embargo ends
- Links: [task #92](https://github.com/OpenSpineConsortium/spine-datasets/issues/92), [record](https://github.com/OpenSpineConsortium/spine-datasets/blob/main/datasets/cobra_embargoed.json), [source](https://zenodo.org/records/21322350)

</details>
