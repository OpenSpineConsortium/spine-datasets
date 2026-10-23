# Which datasets answer which question

Source: the thread "Spine knowledge synthesis", 2026-10-23, step 4 of track #175 ("per question syntheses: for each research question, which sets answer it, how many people, at what level truth"). Read from this repository's records, datasets/*.json at main b44ba32, and, for the sets already held before this repository existed, from the counts of SchwingNet's sample index of 2026-10-22 (its docs/research/data-manifest/README.md), which are counts only. Nothing was fetched or sent for it. Dataset facts only, under CONTRIBUTING.md's confidentiality rule.

The census (#178, tools/census.py) will generate the tables of what is held and what waits on whom from the records. This note does not repeat those tables. It groups the sets by the question each can answer, so a reader can see which question is short of data and which request would close the gap.

Status words are the records' own: held means on the grid before this repository's records began; fetched, granted, requested, todo, needs-owner and refused are a record's `status`.

## 1. Which vertebra is which above L1, on real images

Above L1 is where the counting is hardest: a spot image of the mid-thoracic or mid-cervical spine shows neither C2 nor the sacrum.

| Set | Status | People or images | Level truth | Region |
| --- | --- | --- | --- | --- |
| CSXA lateral cervical films | held | 4,963 films | corners per body, C1 to C7 | cervical |
| NHANES II films | held | 17,073 films, 543 with landmarks (364 persons) | landmarks; identity with the VertXNet labels below | cervical and lumbar |
| Aariz cephalograms | held per the sample index; the record says todo (section 5) | 1,000 films, 7 devices | C2 to C4 by maturation stage | upper cervical |
| AASCE 2019 | held | 609 AP films | four corners of T1 to L5 | thoracic, AP |
| Bournemouth cervical | requested (the tracks are held, the cine is not) | 252 sequences of 63 people | level-named corner tracks C0 to T1 on every frame | cervical, fluoroscopy |
| Maastricht cervical | requested | 112 recordings | C0 to C7 contours on every frame | cervical, fluoroscopy |
| VertXNet NHANES II labels | todo | labels for films held | identity per body, C2 and S1 as references | cervical and lumbar |
| MrOS lateral spine | todo (a data request) | 5,994 men, two visits | Genant grade per named level | thoracic and lumbar |
| SOF lateral spine | todo (a data request) | about 9,700 women | Genant grade per named level | thoracic and lumbar |
| LevelCheck cohort (Johns Hopkins) | requested | 178 patients, 398 radiographs | each level placed by registration to the labelled preoperative CT | cervical to lumbar |
| Bern myelography | requested (the MP4s are held) | 4 runs | thoracic levels named in the captions | thoracic, fluoroscopy |

Read together:

- The held level truth above L1 is on films, not on intraoperative images. The only intraoperative sets with level truth above L1 are requested: Bournemouth's and Maastricht's cine, the LevelCheck cohort and the Bern runs.
- The LevelCheck cohort is the one request that would bring intraoperative radiographs with a CT of the same patient from the cervical to the lumbar spine. It waits on Ali Uneri's answer, and any data use agreement is the owner's to sign.
- MrOS and SOF together would add about 15,700 people with a named level on every graded vertebra of the thoracic and lumbar spine, more than every held film set above L1 together. Both wait on the owner's data request (the NIA Aging Research Biobank, owner-paperwork-sitting.md in symphony-template).
- The chest film sets (MIMIC-CXR, CheXpert Plus, PadChest, BRAX, Open-i, NIH ChestX-ray14, ReXGradient, VinDr-CXR, VinDr-PCXR, BIMCV COVID-19+) show the thoracic spine on hundreds of thousands of images and carry no level truth. They answer the question only after someone reads the levels.

## 2. Agreement across devices and exposures

The question is whether the same anatomy reads the same through different hardware. It needs real images from many devices, with labels or at least with the device named.

| Set | Status | Size | Device facts | Spine labels |
| --- | --- | --- | --- | --- |
| Aariz cephalograms | see section 1 | 1,000 films | 7 devices | C2 to C4 |
| Pediatric IRI | requested | 95,308 fluoroscopy images in 1,357 sequences | not recorded | none; lumbar spine in the field |
| Vanderbilt hip fluoroscopy | requested | 336 AP frames of 146 patients | not recorded | midline L5/S1 and both sacroiliac joints |
| PUMCH stitching | requested | 43 patients, 4 to 6 exposures each | Philips Zenition 70 | none stated |
| Mayfield kyphoplasty | requested | 163 DICOM C-arm frames | native DICOM | thoracolumbar, unnamed |
| CADICA | fetched | 42 patients | Siemens Artis Zee | none; spine in the background |
| CathAction | needs-owner | about 500,000 frames | not recorded | none; no spine, much of it animal |
| Veriserum | needs-owner | about 110,000 dual-plane frames | registered poses | none; knee phantoms |
| The chest film sets of section 1 | various | over 1,000,000 films | many devices and sites | none |

Read together: the device question has volume, and almost none of it carries a spine label. The labelled sets from several devices are Aariz (7 devices, upper cervical only) and the held C-arm sets (C-ArmLSpine, COBRA's projections and DeepFluoro, each from a different machine, per SchwingNet's records). So the measurement this question needs is leave-one-device-out agreement over the held labelled sets. The unlabelled pools serve only once their device field has been read from the files, which the sample index does for DICOM sets.

## 3. Transitional variants: counting the whole column

A transitional spine (L6, T13, a sacralised L5, eleven or thirteen rib pairs) is called reliably only where the whole column is in view, from C2 to the sacrum. That is CT, whole-body or chest-abdomen-pelvis, so this question is answered by CT collections first and by films second.

| Set | Status | Subjects | Coverage |
| --- | --- | --- | --- |
| CT-RATE | granted | 21,304 patients | chest |
| RSNA RSPECT | granted | 7,279 patients | chest |
| RSNA RATIC | granted | 3,147 patients | abdomen and trauma |
| CADS | granted | 753 CTs | as the collection gives |
| MAGIC-CT | needs-owner (approved 2026-10-22 per SchwingNet's records; the record has not caught up) | 562 CTs | as the collection gives |
| Stanford AIMI Merlin | needs-owner (held pending storage) | 18,317 patients | abdomen |
| Stanford AIMI INSPECT | needs-owner (held pending storage) | 19,402 patients | chest |
| NLST | todo; 500-person pilot fetched | 24,713 subjects | chest |
| VSDFullBody | needs-owner | 100 subjects | whole body, post-mortem |
| ENHANCE.PET 1.6k | todo | 1,683 studies | whole and total body |
| The IDC tier 2 collections (ten records) | todo | 32 to 997 subjects each | chest, abdomen, pelvis or spine |
| MrOS and SOF films | todo | about 15,700 people | thoracic and lumbar laterals, named levels |

Read together:

- Every CT record above says its level truth is "counted by the census pipeline once fetched", so none of them has a count of transitional spines yet. The prevalence the literature gives (VerSe: 53 of 374 CTs with T13 or L6) is for a collection gathered for the spine. A collection screened whole is what gives honest odds, which is a reason to prefer the large unselected sets (NLST, CT-RATE, Merlin, INSPECT) once storage allows.
- Chest-only coverage sees the thoracic count and the first lumbar bodies, and abdomen-only coverage sees the lumbosacral junction. Only whole-body sets (VSDFullBody, ENHANCE.PET) and chest-abdomen-pelvis studies see both junctions at once, so they are the ones that settle a column's count without a second study of the same person.
- The real transitional cases with an intraoperative image are few. SchwingNet's records hold three persons with an L6 on C-arm images. No record here promises more, so new real cases come from the owner's own annotation or from the LevelCheck and Huashan requests below.

## 4. A real X-ray with a CT of the same person

This is the breakout the owner asked for on 2026-10-23, to plan annotating the paired data. SchwingNet's benchmarks note lists ten paired sets, held or open. The records here add the requested ones, which that list leaves out.

| Set | Status | People | Real images | Region | Pose shipped |
| --- | --- | --- | --- | --- | --- |
| C-ArmLSpine | held | 149 cases | 299 spot frames, 2 sweeps | lumbar | registered by the project |
| COBRA | held | 692 cases | 375,618 CBCT projections | lumbosacral and pelvis | geometry stored |
| DeepFluoro | held | 6 specimens | 366 frames, 2,659 vendor frames | pelvis and low lumbar | for the H5 frames |
| Ljubljana gold standard | held | 1 cadaver | 18 frames | L1 to L5 | yes |
| Geneva hip phantom | held | 1 phantom | 116 frames | pelvis | yes |
| The digital twin's cadaver | its fetch waits on the owner's word (#170) | 1 specimen | 80 frames | mid-femur to T2 | by navigation |
| LUMOS | needs-owner (non-commercial licence) | 803 patients, 280 with a CT | 1,620 radiographs | lumbar | no |
| LevelCheck cohort | requested | 178 patients | 398 radiographs | cervical to lumbar | by registration |
| Huashan Fudan | requested | 140 patients | AP and lateral intraoperative films | L1 to L5 | no |
| NIT Warangal NIMS | requested | 9 patients | 51 AP and lateral C-arm sets on a Ziehm | L1 to L5 | no; level-named CT centroids public |
| SX stitch | requested | not recorded | C-arm series moved along the spine | not recorded | not recorded |
| Balgrist lumbar | refused | | cadaver C-arm frames | lumbar | |
| IPCAI 2025 (Flepp) | on the grid; the record says needs-owner (section 5) | 5 specimens | 50 calibrated X-rays | distal femur, no spine | yes |
| Pig lower limb (IEEE DataPort) | on the grid; the record says fetching | 1 animal | 7 projections | lower limb, no spine | matrices shipped |
| Veriserum | needs-owner | phantoms | about 110,000 frames | knee implants, no spine | yes |

Read together:

- Held, the spine pairs are lumbar or lumbosacral, and one cadaver reaches T2. No held pair is cervical.
- Requested, the LevelCheck cohort would be the first cervical-to-lumbar pair, and the largest paired set of intraoperative radiographs: 178 patients against C-ArmLSpine's 149 cases. Huashan would add 140 lumbar patients with both views. These two requests matter more to the paired work than any other open request.
- LUMOS is the largest lumbar pair that is open to download, and it waits on one decision: whether the project takes a non-commercial licence. COBRA (CC BY-NC) and DeepFluoro (CC BY-NC-SA) are already held under such terms, so the decision is one the project has made twice already. The manifest check refuses it until the owner records it.
- No paired spine set ships body masks by level, so every pair needs its CT segmented and read before its X-rays carry per-pixel truth. SchwingNet's issue #127 holds that plan.

## 5. Where the records disagree with what is known elsewhere

These are reconciliation findings for step 1 of #175. They were sent to the census thread rather than edited here, since that thread writes the records:

- ipcai2025_xray_ct still says "the anatomy, pelvis or spine, to confirm" and needs-owner on its licence. SchwingNet's record was corrected on 2026-10-23: the set is the distal femur, it is already on the grid, still zipped, and it enters no spine work.
- veterinary_pig_levelcheck is named "the LevelCheck pig study". SchwingNet's retraining plan (section 10) records it as Goswami 2020's lower-limb registration phantom with no spine, not the LevelCheck study. The handoff of 2026-10-23 says the zips are on the grid while the status says fetching (the record's next step explains why: a set behind a login has no promoter manifest).
- aariz_cephalograms says todo, while SchwingNet's sample index of 2026-10-22 counts 1,000 Aariz cephalograms on the volume.
- magic_ct says needs-owner, while SchwingNet's benchmarks note records its data-use application approved on 2026-10-22.
- Merlin and INSPECT are "held pending storage" (spine-dataset-status-audit.md in symphony-template). The volume held 9,605 GB of a 21,991 GB quota on 2026-10-23, so storage is now a number the owner can weigh against their sizes rather than a blanket stop.
