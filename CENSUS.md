# Census: every dataset, counted from its record

Written by tools/census.py on 2026-10-23 from the 166 records under datasets/ of
https://github.com/OpenSpineConsortium/spine-datasets; nobody edits it by hand. Each dataset is one record; the census reads
the records alone, never a dataset's files, and folds in only the records that are new or changed
since the last run. The page with filters is census.html beside this file, served by the docs site.

## In numbers

| | |
|---|---|
| Datasets with a record | 166 |
| On the grid (shared tree and the owner's root) | 102 |
| Size on the grid | 3.9 TB (83 of 102 sets counted) |
| Frozen on the grid, every file hashed (tools/freeze.py) | 0 of 102 |
| Subjects on the grid | 62,843 (86 of 102 sets counted) |
| X-ray images on the grid | 160,879 (16 of 102 sets counted) |
| X-ray videos and sweeps on the grid | 694 (2 of 102 sets counted) |
| Frames inside those videos and sweeps | 376,220 (2 of 102 sets counted) |
| CT volumes on the grid | 24,959 (70 of 102 sets counted) |
| Real spine X-ray and CT pairs on the grid | 5 sets, 1,651 subjects |

| Stage | Datasets |
|---|---|
| Downloadable now | 9 |
| To ask | 10 |
| Asked, waiting | 26 |
| Granted, fetch pending | 5 |
| Fetching | 0 |
| On the grid | 6 |
| Held by the owner | 96 |
| Needs the owner | 11 |
| Refused | 2 |
| Later | 1 |

## Paired CT and X-ray

Every record with a pairing block: real X-ray frames, films or projections with the same subject's
CT or CBCT. The tier follows the record's status by itself.

### A. On the grid (5)

Real spine X-rays with the same subject's CT, held now: the annotation starts here.

| Set | Region | X-rays | CT | Subjects | Pose | Masks shipped | What annotation adds | Pair key | Task |
|---|---|---|---|---|---|---|---|---|---|
| C-ArmLSpine (Zhang et al., Medical Image Analysis 2024) | lumbar | 299 AP and lateral spot frames, and two CBCT projection sweeps of 301 frames | an intraoperative CBCT of every case, from the same C-arm | 149 patients | not shipped for the spot frames; the sweeps carry their gantry angles | none shipped for the vertebral bodies | a mask for each vertebral body, L1 to S1, on each CBCT, read by a person and checked by a second reader | the case number: a case's spot frames and its CBCT share one case folder |  |
| COBRA2026 public cases (Elekta and Varian) | lumbosacral spine and pelvis | 375,618 raw kV projections, a full CBCT sweep a case | the planning CT, deformably registered, and the CBCT reconstruction | 692 patients | stored: each case ships its projection geometry | none for the vertebrae | masks on each planning CT, L3 to S1 and the pelvis | the case id: a case's projections, CBCT and planning CT share it |  |
| DeepFluoro (Grupp et al., IPCAI 2020): the H5 release and the vendor DICOMs | pelvis, hip and lower lumbar spine | 366 frames with registered poses (H5), and 2,659 vendor frames | 6 CTs with the H5 set, one per specimen, and 19 CT files in the vendor deposit | 6 cadaver specimens | shipped for the 366 H5 frames | 7 classes in 3D and per frame in 2D; the vertebrae are one class, with the upper sacrum | split the vertebrae class into named lumbar bodies | the specimen number |  |
| Ljubljana 2D/3D registration gold standard (PIXIUM 4600) | lumbar, L1 to L5 | 18 X-ray images | five CT volumes, one per vertebra L1 to L5, and five MR volumes the same way | 1 cadaver | stored: a gold-standard rigid transform for each vertebra's CT and MR volume, and each X-ray's sensor pose and source position in its header | none shipped; each vertebra comes as a volume of its own | five body masks kept beside the set, never inside it and never shared, since the licence allows no derivatives | one specimen: every X-ray pairs with the five vertebra volumes through their transforms |  |
| LUMOS (Zhejiang University) | lumbar | 1,620 AP or lateral diagnostic radiographs | 280 non-contrast lumbar CTs | 803 patients, 280 of them with a CT | none given: each film is registered to its CT | to confirm on the record | masks on the 280 CTs, then each film registered to its CT | to confirm: whether a film and a CT of the same id are one patient | [#27](https://github.com/OpenSpineConsortium/spine-datasets/issues/27) |

### B. Open or granted, not yet on the grid (0)

A download or a fetch away.

None yet.

### C. Behind a letter, an agreement or the owner's hand (2)

Asked, or still to ask.

| Set | Region | X-rays | CT | Subjects | Pose | Masks shipped | What annotation adds | Pair key | Task |
|---|---|---|---|---|---|---|---|---|---|
| Huashan Hospital, Fudan University, intraoperative lumbar films with preoperative CT (Shao et al. 2024) | lumbar, L1 to L5 | intraoperative AP and lateral films | the preoperative CT of each patient | 140 patients | none stated | none stated | to read once the set is in hand | the patient | [#61](https://github.com/OpenSpineConsortium/spine-datasets/issues/61) |
| NIT Warangal and NIMS Hyderabad intraoperative C-arm sets (2D-3D-sci-registration) | lumbar, L1 to L5 | 51 AP and lateral C-arm sets on a Ziehm C-arm, at most 49 unique frames | the preoperative CT, with L1 to L5 centroids named by level | 9 patients | the public overlays set each real frame beside a simulated projection | level-named centroids; no masks | to read once the set is in hand | the patient | [#64](https://github.com/OpenSpineConsortium/spine-datasets/issues/64) |

### D. Refused, embargoed or never released (3)

Kept so nobody asks twice.

| Set | Region | X-rays | CT | Subjects | Pose | Masks shipped | What annotation adds | Pair key | Task |
|---|---|---|---|---|---|---|---|---|---|
| Balgrist ex-vivo lumbar CT plus C-arm (Jecklin) | lumbar spine of cadavers | real C-arm frames | the cadavers' CT | not stated | not stated | not stated | none: the source declined | not stated | [#69](https://github.com/OpenSpineConsortium/spine-datasets/issues/69) |
| COBRA2026 embargoed cases | lumbosacral spine and pelvis | raw kV projections, as the public cases | the planning CT and the CBCT, as the public cases | 175 patients | stored, as the public cases | none for the vertebrae | as COBRA2026's public cases, once the embargo ends on 2032-03-01 | the case id | [#92](https://github.com/OpenSpineConsortium/spine-datasets/issues/92) |
| LevelCheck clinical cohort (Johns Hopkins, Siewerdsen group) | thoracic and lumbar spine | 398 intraoperative radiographs (De Silva 2016), and 61 more (Ketcha 2017) | the preoperative CT of each patient | 178 patients, and 24 more | not shipped; each level is placed by registration to the CT | levels labelled on the preoperative CT | to read once the set is in hand | the patient | [#60](https://github.com/OpenSpineConsortium/spine-datasets/issues/60) |

### E. Real pairs of something other than the spine (5)

Frames shipped with a CT or an exact pose: the registration code's truth, not spine labels.

| Set | Region | X-rays | CT | Subjects | Pose | Masks shipped | What annotation adds | Pair key | Task |
|---|---|---|---|---|---|---|---|---|---|
| CAMS-Knee (ETH Zurich and Charite Berlin, J Biomech 2017) | instrumented total knee replacements in living subjects | fluoroscopic image series from a moving fluoroscope that follows the knee, at 25 Hz, registered to the implant components | the implant components' CAD files, not a CT | 6 people with instrumented knee implants | the tibial and femoral 4 x 4 poses at every fluoroscope capture, shipped | none; the registered images carry the implant components | nothing for the spine; fluoroscopy of metal implants in living subjects during daily activities | the trial's own registered poses |  |
| Geneva hip phantom (BV Pulsera; D'Isidoro et al., Medical Physics 2021) | pelvis and hip, a phantom | 116 frames | the phantom's CT | 1 phantom | stored: gold-standard rigid transforms and the projection matrix | none shipped | nothing for the spine; a registration check on a C-arm no other set comes from | one phantom: every frame pairs with its one CT |  |
| IPCAI 2025 paired X-ray and CT set of the distal femur (Flepp 2025, Zenodo 15753063) | distal femur, five cadaveric specimens | 50 calibrated X-rays, ten views of each specimen about 9 degrees apart (Siemens Fluorospot) | 5 CTs at 0.2 mm slices | 5 cadaveric distal femora | stored | contour masks and bone surface meshes | nothing for the spine; a registration benchmark | the specimen: its ten views and its CT | [#34](https://github.com/OpenSpineConsortium/spine-datasets/issues/34) |
| Veriserum (ETH Zurich, MICCAI 2025) | knee implant phantoms | about 110,000 dual-plane fluoroscopic images | the implants' 3D shapes as CAD meshes, not a CT | phantoms | registered for every image, 200 by hand | implant poses | nothing for the spine; real flat-panel noise and metal at scale | the image's own registered pose | [#41](https://github.com/OpenSpineConsortium/spine-datasets/issues/41) |
| Veterinary: pig lower limb CT, CBCT and planar images (Goswami 2020, IEEE DataPort) | pig lower limb, a phantom; no spine | 14 C-arm planar projections: 7 poses with soft tissue and 7 without | a CT and two CBCTs, with and without soft tissue | 1 phantom | registration matrices shipped | none | nothing for the spine; a registration benchmark | one phantom: every projection pairs with its CT | [#22](https://github.com/OpenSpineConsortium/spine-datasets/issues/22) |

### Pairs asked for, no record yet

- [#182](https://github.com/OpenSpineConsortium/spine-datasets/issues/182) Obtain the Loop-X lower-torso cadaver frames of Zenodo 10390295 (Killeen, Unberath et al., JHU ARCADE), or show they are #170's cadaver
- [#183](https://github.com/OpenSpineConsortium/spine-datasets/issues/183) Obtain the interventional XA frames of TCIA's CMB-MML and CMB-AML collections, with the same patients' CT
- [#184](https://github.com/OpenSpineConsortium/spine-datasets/issues/184) Obtain the CMB-MML skeletal-survey radiographs for the patients whose CT is in the same collection
- [#185](https://github.com/OpenSpineConsortium/spine-datasets/issues/185) Obtain the COVID-19-NY-SBU films of the patients whose CT is held, the 27 abdominal pairs first
- [#186](https://github.com/OpenSpineConsortium/spine-datasets/issues/186) Find the CT localizers of TCIA's CT COLONOGRAPHY and other held CT collections, and fetch those missing
- [#187](https://github.com/OpenSpineConsortium/spine-datasets/issues/187) Obtain US-X Complete (TUM CAMP): lumbar phantoms with Loop-X lateral X-rays and co-registered CBCT
- [#188](https://github.com/OpenSpineConsortium/spine-datasets/issues/188) Obtain MIDRC Open Data Commons cases with both CT and CR or DX, the spine-labelled studies first
- [#189](https://github.com/OpenSpineConsortium/spine-datasets/issues/189) Ask for the UCLA spine radiotherapy setup radiographs with their planning CTs (Charters et al. 2024)
- [#190](https://github.com/OpenSpineConsortium/spine-datasets/issues/190) Ask for the ExacTrac spine radiotherapy kV images with planning CTs (Petragallo, Lamb et al. 2023)
- [#191](https://github.com/OpenSpineConsortium/spine-datasets/issues/191) Ask for the standing biplanar lumbar radiographs with CT (Yu, Tsai et al., Med Phys 2026)
- [#192](https://github.com/OpenSpineConsortium/spine-datasets/issues/192) Ask FAU or Siemens Healthineers for the thoracolumbar CBCT sweeps (Jaganathan, Maier et al.)
- [#193](https://github.com/OpenSpineConsortium/spine-datasets/issues/193) Ask the Siewerdsen and Zbijewski groups for their cadaver frames with CT (Otake 2013, Huang 2022)
- [#194](https://github.com/OpenSpineConsortium/spine-datasets/issues/194) Ask for the intraoperative spine cases of RadGS-Reg (MICCAI 2025)
- [#196](https://github.com/OpenSpineConsortium/spine-datasets/issues/196) Ask the Framingham Heart Study for the CT scouts of its MDCT cohort (low priority)
- [#197](https://github.com/OpenSpineConsortium/spine-datasets/issues/197) Ask AGES-Reykjavik for the CT scouts of its cohort (low priority)
- [#198](https://github.com/OpenSpineConsortium/spine-datasets/issues/198) Ask for the Spine-DART cadaver frames with their Loop-X CT (Johns Hopkins 2026)
- [#199](https://github.com/OpenSpineConsortium/spine-datasets/issues/199) Ask for the UC Davis and Augmedics cadaver screw study's frames with CT (Global Spine J 2025)
- [#200](https://github.com/OpenSpineConsortium/spine-datasets/issues/200) Ask Giessen and Jena for the canine biplanar fluoroscopy of the lumbosacral spine with CT (Front Vet Sci 2021)
- [#201](https://github.com/OpenSpineConsortium/spine-datasets/issues/201) Ask for SheepSpineX: ovine cervical AP and lateral films with CT (Shanghai Jiao Tong University)

## Every dataset

| Dataset | Kind | Stage | Licence | Subjects | X-ray images | Videos and sweeps | Their frames | CT volumes | Size | Task |
|---|---|---|---|---|---|---|---|---|---|---|
| Balgrist ex-vivo lumbar CT plus C-arm (Jecklin) | Fluoroscopy | Refused | unknown |  |  |  |  |  |  | [#69](https://github.com/OpenSpineConsortium/spine-datasets/issues/69) |
| C-ArmLSpine (Zhang et al., Medical Image Analysis 2024) | Fluoroscopy | Held by the owner | open | 149 | 299 | 2 | 602 | 149 | 86.8 GB |  |
| CM Spine (Zeng et al., Electronics 2024): 208 intraoperative lumbar G-arm images | Fluoroscopy | Asked, waiting | unknown |  | 208 |  |  |  |  | [#8](https://github.com/OpenSpineConsortium/spine-datasets/issues/8) |
| DeepFluoro (Grupp et al., IPCAI 2020): the H5 release and the vendor DICOMs | Fluoroscopy | Held by the owner | restricted | 6 | 2,659 |  |  | 19 | 116.3 GB |  |
| Geneva hip phantom (BV Pulsera; D'Isidoro et al., Medical Physics 2021) | Fluoroscopy | Held by the owner | open | 1 | 116 |  |  | 1 |  |  |
| Huashan Hospital, Fudan University, intraoperative lumbar films with preoperative CT (Shao et al. 2024) | Fluoroscopy | Asked, waiting | restricted | 140 |  |  |  | 140 |  | [#61](https://github.com/OpenSpineConsortium/spine-datasets/issues/61) |
| LevelCheck clinical cohort (Johns Hopkins, Siewerdsen group) | Fluoroscopy | Refused | restricted | 202 | 459 |  |  | 202 |  | [#60](https://github.com/OpenSpineConsortium/spine-datasets/issues/60) |
| Ljubljana 2D/3D registration gold standard (PIXIUM 4600) | Fluoroscopy | Held by the owner | restricted | 1 | 18 |  |  | 5 |  |  |
| LUMOS (Zhejiang University) | Fluoroscopy | Held by the owner | restricted | 803 | 1,620 |  |  | 280 | 46.4 GB | [#27](https://github.com/OpenSpineConsortium/spine-datasets/issues/27) |
| NIT Warangal and NIMS Hyderabad intraoperative C-arm sets (2D-3D-sci-registration) | Fluoroscopy | Asked, waiting | restricted | 9 | 49 |  |  | 9 |  | [#64](https://github.com/OpenSpineConsortium/spine-datasets/issues/64) |
| PUMCH stitching series (Liu et al., Eur Spine J 2026) | Fluoroscopy | Asked, waiting | restricted |  |  |  |  |  |  | [#63](https://github.com/OpenSpineConsortium/spine-datasets/issues/63) |
| SX-Stitch intraoperative C-arm series (Li 2024, PUMCH) | Fluoroscopy | Asked, waiting | unknown |  |  |  |  |  |  | [#62](https://github.com/OpenSpineConsortium/spine-datasets/issues/62) |
| Vanderbilt intraoperative THA fluoroscopy (Chan et al., J Arthroplasty 2025) | Fluoroscopy | Asked, waiting | restricted |  |  |  |  |  |  | [#65](https://github.com/OpenSpineConsortium/spine-datasets/issues/65) |
| Inselspital Bern dynamic myelography (Piechowiak 2021) | Fluoroscopy video | Asked, waiting | restricted |  |  | 4 |  |  |  | [#73](https://github.com/OpenSpineConsortium/spine-datasets/issues/73) |
| Bournemouth cervical quantitative fluoroscopy (BORDaR 385) | Fluoroscopy video | Asked, waiting | restricted | 63 |  | 252 |  |  |  | [#70](https://github.com/OpenSpineConsortium/spine-datasets/issues/70) |
| Bournemouth lumbar quantitative fluoroscopy (Breen 2021) | Fluoroscopy video | Asked, waiting | unknown | 127 |  |  |  |  |  | [#71](https://github.com/OpenSpineConsortium/spine-datasets/issues/71) |
| CADICA invasive coronary angiography sequences (Mendeley p9bpx9ctcv) | Fluoroscopy video | On the grid | open | 42 |  |  |  |  | 3.1 GB | [#109](https://github.com/OpenSpineConsortium/spine-datasets/issues/109) |
| CAMS-Knee (ETH Zurich and Charite Berlin, J Biomech 2017) | Fluoroscopy video | Needs the owner | restricted | 6 |  |  |  |  |  |  |
| CathAction (Jianu et al. 2024, AIRVLab) | Fluoroscopy video | Held by the owner | restricted |  |  |  |  |  |  | [#39](https://github.com/OpenSpineConsortium/spine-datasets/issues/39) |
| Coronary angiography sets (CADICA, ARCADE, XCAD, AngioCAD) | Fluoroscopy video | Downloadable now | unknown |  |  |  |  |  |  | [#38](https://github.com/OpenSpineConsortium/spine-datasets/issues/38) |
| DARADIA vertebroplasty video (Kolkata) | Fluoroscopy video | Asked, waiting | unknown |  |  |  |  |  |  | [#83](https://github.com/OpenSpineConsortium/spine-datasets/issues/83) |
| DMX Imaging digital motion X-ray | Fluoroscopy video | Asked, waiting | unknown |  |  |  |  |  |  | [#77](https://github.com/OpenSpineConsortium/spine-datasets/issues/77) |
| DysphagiaBank (TalkBank), UNM corpus | Fluoroscopy video | Held by the owner | restricted |  |  |  |  |  | 19.0 GB | [#20](https://github.com/OpenSpineConsortium/spine-datasets/issues/20) |
| ThePainSource (Faubel) fluoroscopy clips | Fluoroscopy video | Asked, waiting | unknown |  |  |  |  |  |  | [#82](https://github.com/OpenSpineConsortium/spine-datasets/issues/82) |
| Guide3D (ACCV 2024, AIRVLab) | Fluoroscopy video | Needs the owner | restricted |  |  |  |  |  |  | [#40](https://github.com/OpenSpineConsortium/spine-datasets/issues/40) |
| Jefferson Neurosurgery DRG stimulation video (Hines 2020) | Fluoroscopy video | Asked, waiting | restricted |  |  | 1 |  |  |  | [#80](https://github.com/OpenSpineConsortium/spine-datasets/issues/80) |
| Konica Minolta dynamic digital radiography sequences | Fluoroscopy video | Asked, waiting | unknown |  |  |  |  |  |  | [#79](https://github.com/OpenSpineConsortium/spine-datasets/issues/79) |
| Maastricht UMC+ cervical flexion-extension cine (van Santbrink 2026) | Fluoroscopy video | Asked, waiting | restricted |  |  | 112 |  |  |  | [#72](https://github.com/OpenSpineConsortium/spine-datasets/issues/72) |
| Mayfield Brain and Spine kyphoplasty alignment series | Fluoroscopy video | Asked, waiting | unknown |  |  | 2 | 163 |  |  | [#76](https://github.com/OpenSpineConsortium/spine-datasets/issues/76) |
| Manual Therapy Foundation of India lumbar coupling video | Fluoroscopy video | Asked, waiting | unknown |  |  |  |  |  |  | [#81](https://github.com/OpenSpineConsortium/spine-datasets/issues/81) |
| Neurosurgical Focus: Video (every article CC BY 4.0) | Fluoroscopy video | Downloadable now | open |  |  |  |  |  |  | [#43](https://github.com/OpenSpineConsortium/spine-datasets/issues/43) |
| IRI-VFI: pediatric interventional radiology image sequences (Chongqing) | Fluoroscopy video | Asked, waiting | unknown |  |  | 1,357 | 95,308 |  |  | [#21](https://github.com/OpenSpineConsortium/spine-datasets/issues/21) |
| Pittsburgh videofluoroscopic swallow corpus (Sejdic, Coyle) | Fluoroscopy video | Asked, waiting | restricted | 335 |  | 1,500 |  |  |  | [#74](https://github.com/OpenSpineConsortium/spine-datasets/issues/74) |
| The Procedure Guide (Puranik) live fluoroscopy clips | Fluoroscopy video | Asked, waiting | restricted |  |  | 4 |  |  |  | [#78](https://github.com/OpenSpineConsortium/spine-datasets/issues/78) |
| Radiopaedia spine cases | Fluoroscopy video | Granted, fetch pending | restricted |  |  |  |  |  |  | [#84](https://github.com/OpenSpineConsortium/spine-datasets/issues/84) |
| Seattle Science Foundation spine videos | Fluoroscopy video | Asked, waiting | unknown |  |  | 12 |  |  |  | [#75](https://github.com/OpenSpineConsortium/spine-datasets/issues/75) |
| Veriserum (ETH Zurich, MICCAI 2025) | Fluoroscopy video | Needs the owner | restricted |  |  |  |  |  |  | [#41](https://github.com/OpenSpineConsortium/spine-datasets/issues/41) |
| VFSS2022 videofluoroscopic swallow frames (TIB) | Fluoroscopy video | Downloadable now | unknown |  |  |  | 440 |  |  | [#42](https://github.com/OpenSpineConsortium/spine-datasets/issues/42) |
| COBRA2026 public cases (Elekta and Varian) | CBCT projections | Held by the owner | restricted | 692 |  | 692 | 375,618 | 692 | 808.6 GB |  |
| COBRA2026 embargoed cases | CBCT projections | Later | restricted | 175 |  |  |  |  |  | [#92](https://github.com/OpenSpineConsortium/spine-datasets/issues/92) |
| IPCAI 2025 paired X-ray and CT set of the distal femur (Flepp 2025, Zenodo 15753063) | CBCT projections | Held by the owner | restricted | 5 | 50 |  |  | 5 | 6.7 GB | [#34](https://github.com/OpenSpineConsortium/spine-datasets/issues/34) |
| Aariz cephalometric benchmark (Khalid, Fraz 2023) and the ISBI 2015 cephalograms | Radiographs | Held by the owner | open |  | 1,000 |  |  |  | 2.1 GB | [#25](https://github.com/OpenSpineConsortium/spine-datasets/issues/25) |
| AASCE 2019 / BoostNet AP whole-spine films | Radiographs | Held by the owner | restricted |  | 707 |  |  |  |  |  |
| BIMCV COVID-19+ chest films (IEEE DataPort) | Radiographs | Needs the owner | unknown |  |  |  |  |  |  | [#111](https://github.com/OpenSpineConsortium/spine-datasets/issues/111) |
| BRAX Brazilian chest films (PhysioNet) | Radiographs | Needs the owner | restricted |  | 40,967 |  |  |  |  | [#110](https://github.com/OpenSpineConsortium/spine-datasets/issues/110) |
| BUU-LSPINE (Klinwichit et al., Applied Sciences 2023) | Radiographs | Held by the owner | restricted | 3,600 | 7,203 |  |  |  |  |  |
| CheXpert and CheXpert Plus (Stanford AIMI) | Radiographs | To ask | restricted | 65,240 | 224,316 |  |  |  |  | [#13](https://github.com/OpenSpineConsortium/spine-datasets/issues/13) |
| CSXA, the Cervical Spine X-ray Atlas V3.0 (Ran et al., Scientific Data 2024) | Radiographs | Held by the owner | open |  | 4,963 |  |  |  |  |  |
| FracAtlas (Abedeen 2023, Scientific Data) | Radiographs | Downloadable now | open |  | 4,083 |  |  |  |  | [#36](https://github.com/OpenSpineConsortium/spine-datasets/issues/36) |
| Fraiwan spine X-ray set (Mendeley xkt857dsxk) | Radiographs | On the grid | open | 338 |  |  |  |  | 85.6 MB | [#31](https://github.com/OpenSpineConsortium/spine-datasets/issues/31) |
| Harms Study Group registries (adolescent idiopathic scoliosis and other pediatric spinal deformity) | Radiographs | To ask | unknown |  |  |  |  |  |  |  |
| IEEE DataPort lateral full-spine X-ray dataset (236 films) | Radiographs | Needs the owner | unknown | 236 | 236 |  |  |  | 1.3 GB |  |
| Kaggle bone fracture multi-region X-ray data (bmadushanirodrigo) | Radiographs | To ask | open |  | 10,580 |  |  |  | 481.0 MB | [#24](https://github.com/OpenSpineConsortium/spine-datasets/issues/24) |
| Kaggle scoliosis YOLOv5 annotated spine X-ray set (salmankey) | Radiographs | Needs the owner | open |  |  |  |  |  |  | [#23](https://github.com/OpenSpineConsortium/spine-datasets/issues/23) |
| KUB-StoneX (Daffodil International University HIRL) | Radiographs | Held by the owner | open | 1,703 | 2,570 |  |  |  | 20.8 GB | [#26](https://github.com/OpenSpineConsortium/spine-datasets/issues/26) |
| Mendeley DDH hip sets (jf3pv98m9g and 4gvcb6gmh2) | Radiographs | Downloadable now | open |  |  |  |  |  |  | [#33](https://github.com/OpenSpineConsortium/spine-datasets/issues/33) |
| MIMIC-CXR and MIMIC-CXR-JPG (PhysioNet) | Radiographs | Asked, waiting | restricted | 65,379 | 377,110 |  |  |  |  | [#15](https://github.com/OpenSpineConsortium/spine-datasets/issues/15) |
| MrOS lateral spine radiographs (Osteoporotic Fractures in Men) | Radiographs | To ask | restricted | 5,994 |  |  |  |  |  | [#9](https://github.com/OpenSpineConsortium/spine-datasets/issues/9) |
| NHANES II spinal films with landmarks (Mo, Papiez, Chen et al., Zenodo) | Radiographs | Held by the owner | open | 364 | 543 |  |  |  |  |  |
| NHANES II cervical and lumbar spine films (NCHS, 1976 to 1980) | Radiographs | Held by the owner | open |  | 16,531 |  |  |  |  |  |
| NIH ChestX-ray14 and the RSNA pneumonia subset | Radiographs | Held by the owner | unknown | 30,805 | 112,120 |  |  |  |  | [#37](https://github.com/OpenSpineConsortium/spine-datasets/issues/37) |
| Open-i Indiana chest collection | Radiographs | Needs the owner | restricted |  | 7,470 |  |  |  |  | [#35](https://github.com/OpenSpineConsortium/spine-datasets/issues/35) |
| PadChest (BIMCV, Alicante) | Radiographs | To ask | restricted | 67,625 | 160,868 |  |  |  |  | [#12](https://github.com/OpenSpineConsortium/spine-datasets/issues/12) |
| ReXGradient-160K (Rajpurkar lab and Gradient Health, 2025) | Radiographs | To ask | restricted | 109,487 |  |  |  |  |  | [#11](https://github.com/OpenSpineConsortium/spine-datasets/issues/11) |
| MTDDH paediatric pelvic X-rays with hip dysplasia key points (Qi et al., Science Data Bank 2025) | Radiographs | To ask | open |  | 2,156 |  |  |  | 4.0 GB |  |
| SOF lateral spine radiographs (Study of Osteoporotic Fractures) | Radiographs | To ask | restricted |  |  |  |  |  |  | [#10](https://github.com/OpenSpineConsortium/spine-datasets/issues/10) |
| TVGH ankylosing spondylitis cervical and lumbar spine films | Radiographs | Asked, waiting | unknown |  |  |  |  |  |  | [#108](https://github.com/OpenSpineConsortium/spine-datasets/issues/108) |
| TVGH-SpineXR | Radiographs | Asked, waiting | unknown |  |  |  |  |  |  | [#14](https://github.com/OpenSpineConsortium/spine-datasets/issues/14) |
| VertXNet extra labels for NHANES II (Mo, Papiez, Chen 2023) | Radiographs | Downloadable now | unknown |  |  |  |  |  |  | [#28](https://github.com/OpenSpineConsortium/spine-datasets/issues/28) |
| VinDr-CXR (PhysioNet) | Radiographs | Asked, waiting | restricted |  | 18,000 |  |  |  |  | [#16](https://github.com/OpenSpineConsortium/spine-datasets/issues/16) |
| VinDr-PCXR (PhysioNet) | Radiographs | Granted, fetch pending | restricted |  | 9,125 |  |  |  |  | [#17](https://github.com/OpenSpineConsortium/spine-datasets/issues/17) |
| VinDr-SpineXR (Nguyen et al., MICCAI 2021) | Radiographs | Held by the owner | restricted |  | 10,466 |  |  |  |  |  |
| AbdomenAtlas 3.0 Mini (= AbdomenAtlas 1.1 images) | CT | Held by the owner | restricted | 7,835 |  |  |  | 7,649 | 570.7 GB |  |
| AMOS22 CT, unlabelled (ids 5000-6899) and labelled | CT | Held by the owner | open | 2,200 |  |  |  | 723 | 102.6 GB |  |
| AortaSeg-60 | CT | Held by the owner | open | 60 |  |  |  | 55 | 15.9 GB |  |
| STOIC2021 training (AWS Open Data) | CT | Held by the owner | restricted | 2,000 |  |  |  |  | 240.0 GB | [#44](https://github.com/OpenSpineConsortium/spine-datasets/issues/44) |
| Barts CRL (colorectal-cancer staging CT) | CT | Held by the owner | open | 220 |  |  |  | 212 | 20.3 GB |  |
| CADS CT (unique cases) | CT | Granted, fetch pending | restricted |  |  |  |  |  |  | [#86](https://github.com/OpenSpineConsortium/spine-datasets/issues/86) |
| CSI 2014 spine CT | CT | Held by the owner | open | 20 |  |  |  | 20 | 3.6 GB |  |
| CT-RATE chest CT | CT | Granted, fetch pending | restricted |  |  |  |  |  |  | [#85](https://github.com/OpenSpineConsortium/spine-datasets/issues/85) |
| CTPelvic1K | CT | Held by the owner | restricted |  |  |  |  | 172 |  |  |
| CTSpine1K | CT | Held by the owner | restricted |  |  |  |  | 1,005 |  |  |
| CTSpinoPelvic1K v11 (the consortium's own release) | CT | Held by the owner | restricted |  |  |  |  | 802 |  |  |
| CURVAS 2024 | CT | Held by the owner | open | 90 |  |  |  | 70 | 29.4 GB |  |
| CURVAS-PDACVI (MICCAI 2025) | CT | Held by the owner | open | 109 |  |  |  | 101 | 15.4 GB |  |
| DEEP-PSMA (PSMA + FDG PET/CT, mCRPC) | CT | Held by the owner | restricted | 100 |  |  |  | 53 | 24.1 GB |  |
| AbdomenAtlas 2.0 Mini (10,135 CT) | CT | Asked, waiting | restricted |  |  |  |  | 10,135 | 620.4 GB | [#89](https://github.com/OpenSpineConsortium/spine-datasets/issues/89) |
| IDC `acrin_flt_breast` | CT | Held by the owner | open | 15 |  |  |  | 15 | 2.8 GB |  |
| IDC `acrin_nsclc_fdg_pet` | CT | Held by the owner | open | 131 |  |  |  | 131 | 15.4 GB |  |
| IDC `adrenal_acc_ki67_seg` | CT | Held by the owner | open | 29 |  |  |  | 29 | 3.5 GB |  |
| IDC `anti_pd_1_lung` | CT | Held by the owner | open | 34 |  |  |  | 34 | 4.2 GB |  |
| IDC `cmb_brca` | CT | Held by the owner | open | 21 |  |  |  | 21 | 2.5 GB |  |
| IDC `cmb_crc` | CT | Held by the owner | open | 30 |  |  |  | 30 | 5.3 GB |  |
| IDC `cmb_lca` | CT | Held by the owner | open | 75 |  |  |  | 75 | 9.8 GB |  |
| IDC `cmb_mel` | CT | Held by the owner | open | 23 |  |  |  | 23 | 2.1 GB |  |
| IDC `cmb_mml` | CT | Held by the owner | open | 16 |  |  |  | 16 | 2.3 GB |  |
| IDC `cmb_ov` | CT | Held by the owner | open | 7 |  |  |  | 7 | 1.0 GB |  |
| IDC `colorectal_liver_metastases` (Colorectal-Liver-Metastases) | CT | Held by the owner | open | 80 |  |  |  | 80 | 6.2 GB |  |
| IDC `covid_19_ar` | CT | Held by the owner | open | 23 |  |  |  | 23 | 5.5 GB |  |
| IDC `covid_19_ny_sbu` (COVID-19-NY-SBU) | CT | Held by the owner | open | 443 |  |  |  | 443 | 63.1 GB |  |
| IDC `cptac_ccrcc` | CT | Held by the owner | open | 48 |  |  |  | 48 | 7.7 GB |  |
| IDC `cptac_cm` | CT | Held by the owner | open | 12 |  |  |  | 12 | 4.1 GB |  |
| IDC `cptac_lscc` (tier 2) | CT | Held by the owner | open | 32 |  |  |  |  | 8.3 GB | [#45](https://github.com/OpenSpineConsortium/spine-datasets/issues/45) |
| IDC `cptac_luad` (tier 2) | CT | Held by the owner | open | 32 |  |  |  |  | 7.0 GB | [#46](https://github.com/OpenSpineConsortium/spine-datasets/issues/46) |
| IDC `cptac_pda` | CT | Held by the owner | open | 62 |  |  |  | 62 | 9.8 GB |  |
| IDC `cptac_sar` | CT | Held by the owner | open | 14 |  |  |  | 14 | 3.0 GB |  |
| IDC `cptac_stad` | CT | Held by the owner | open | 19 |  |  |  | 19 | 6.9 GB |  |
| IDC `cptac_ucec` | CT | Held by the owner | open | 66 |  |  |  | 66 | 10.3 GB |  |
| IDC `ct_vs_pet_ventilation_imaging` | CT | Held by the owner | open | 20 |  |  |  | 20 | 1.8 GB |  |
| IDC `ctpred_sunitinib_pannet` | CT | Held by the owner | open | 34 |  |  |  | 34 | 6.0 GB |  |
| IDC `eay131` (EAY131 (NCI-MATCH)) | CT | Held by the owner | open | 376 |  |  |  | 376 | 36.4 GB |  |
| IDC `hcc_tace_seg` (HCC-TACE-Seg) | CT | Held by the owner | open | 101 |  |  |  | 101 | 5.0 GB |  |
| IDC `ldct_and_projection_data` (tier 2) | CT | Held by the owner | open | 99 |  |  |  |  | 16.5 GB | [#47](https://github.com/OpenSpineConsortium/spine-datasets/issues/47) |
| IDC `lidc_idri` (tier 2) | CT | Downloadable now | open | 997 |  |  |  |  | 123.3 GB | [#48](https://github.com/OpenSpineConsortium/spine-datasets/issues/48) |
| IDC `lung_pet_ct_dx` (Lung-PET-CT-Dx) | CT | Held by the owner | open | 158 |  |  |  | 158 | 29.2 GB |  |
| IDC `mediastinal_lymph_node_seg` | CT | Held by the owner | open | 316 |  |  |  | 316 | 25.1 GB |  |
| IDC `midrc_ricord_1a` | CT | Held by the owner | restricted | 98 |  |  |  | 98 | 6.5 GB |  |
| IDC `midrc_ricord_1b` (tier 2) | CT | Held by the owner | restricted | 91 |  |  |  |  | 7.0 GB | [#49](https://github.com/OpenSpineConsortium/spine-datasets/issues/49) |
| NLST, full (tier 2; 500-person pilot fetched) | CT | To ask | open | 24,713 |  |  |  |  | 2.3 TB | [#91](https://github.com/OpenSpineConsortium/spine-datasets/issues/91) |
| IDC `nsclc_radiogenomics` (tier 2) | CT | Held by the owner | open | 188 |  |  |  |  | 28.0 GB | [#50](https://github.com/OpenSpineConsortium/spine-datasets/issues/50) |
| IDC `nsclc_radiomics` (tier 2) | CT | Held by the owner | restricted | 415 |  |  |  |  | 25.8 GB | [#51](https://github.com/OpenSpineConsortium/spine-datasets/issues/51) |
| IDC `pancreatic_ct_cbct_seg` | CT | Held by the owner | open | 40 |  |  |  | 40 | 2.9 GB |  |
| IDC `pediatric_ct_seg` (Pediatric-CT-SEG) | CT | Held by the owner | open | 352 |  |  |  | 352 | 55.6 GB |  |
| IDC `pelvic_reference_data` | CT | Held by the owner | open | 58 |  |  |  | 58 | 4.4 GB |  |
| IDC `prostate_anatomical_edge_cases` (tier 2) | CT | Downloadable now | open | 131 |  |  |  |  | 16.6 GB | [#52](https://github.com/OpenSpineConsortium/spine-datasets/issues/52) |
| IDC `psma_pet_ct_lesions` (PSMA-PET-CT-Lesions (autoPET III)) | CT | Held by the owner | open | 374 |  |  |  | 374 | 61.7 GB |  |
| IDC `rider_lung_pet_ct` | CT | Held by the owner | open | 117 |  |  |  | 117 | 18.1 GB |  |
| IDC `spinal_multiple_myeloma_seg` (tier 2) | CT | Held by the owner | open | 67 |  |  |  |  | 33.8 GB | [#53](https://github.com/OpenSpineConsortium/spine-datasets/issues/53) |
| IDC `spine_mets_ct_seg` (tier 2) | CT | Held by the owner | open | 54 |  |  |  |  | 17.2 GB | [#54](https://github.com/OpenSpineConsortium/spine-datasets/issues/54) |
| IDC `tcga_blca` | CT | Held by the owner | open | 79 |  |  |  | 79 | 10.0 GB |  |
| IDC `tcga_esca` | CT | Held by the owner | open | 16 |  |  |  | 16 | 2.4 GB |  |
| IDC `tcga_kirc` | CT | Held by the owner | open | 129 |  |  |  | 129 | 9.7 GB |  |
| IDC `tcga_lihc` | CT | Held by the owner | open | 42 |  |  |  | 42 | 4.9 GB |  |
| IDC `tcga_ov` | CT | Held by the owner | open | 24 |  |  |  | 24 | 2.4 GB |  |
| IDC `tcga_stad` | CT | Held by the owner | open | 45 |  |  |  | 45 | 6.3 GB |  |
| IDC `tcga_ucec` | CT | Held by the owner | open | 38 |  |  |  | 38 | 4.1 GB |  |
| IDC `varepop_apollo` | CT | Held by the owner | open | 35 |  |  |  | 35 | 5.4 GB |  |
| Kidney abnormality segmentation in thorax-abdomen CT | CT | Held by the owner | open | 215 |  |  |  | 215 | 38.4 GB |  |
| MAGIC-CT (Zenodo) | CT | Needs the owner | restricted |  |  |  |  |  |  | [#7](https://github.com/OpenSpineConsortium/spine-datasets/issues/7) |
| NLST, the seeded 500-person pilot | CT | Held by the owner | open | 500 |  |  |  | 500 | 45.8 GB |  |
| PANORAMA public set (pancreas CE-CT) | CT | Held by the owner | restricted | 1,950 |  |  |  | 2,024 | 194.2 GB |  |
| PENGWIN 2026 peripelvic fracture CT (the public cases) | CT | Held by the owner | restricted | 340 |  |  |  | 340 | 19.6 GB |  |
| PENGWIN 2024 Task 2 synthetic X-rays | CT | Held by the owner | open |  |  |  |  | 100 |  | [#30](https://github.com/OpenSpineConsortium/spine-datasets/issues/30) |
| QUADRA_HC total-body FDG-PET/CT, healthy controls | CT | Held by the owner | open | 48 |  |  |  | 48 | 20.2 GB |  |
| RibFrac (MICCAI 2020) chest CT | CT | Held by the owner | restricted |  |  |  |  | 660 |  |  |
| RSNA 2022 cervical spine fracture CT (Kaggle) | CT | Held by the owner | restricted |  |  |  |  | 2,019 | 203.3 GB |  |
| RSNA abdominal trauma CT (RATIC) | CT | Granted, fetch pending | restricted |  |  |  |  |  |  | [#87](https://github.com/OpenSpineConsortium/spine-datasets/issues/87) |
| RSNA pulmonary embolism CT (RSPECT) | CT | Held by the owner | restricted |  |  |  |  |  |  | [#88](https://github.com/OpenSpineConsortium/spine-datasets/issues/88) |
| ENHANCE.PET 1.6k: whole-/total-body FDG-PET/CT, 1,683 studies (NIfTI) | CT | To ask | open |  |  |  |  |  | 286.3 GB | [#90](https://github.com/OpenSpineConsortium/spine-datasets/issues/90) |
| Stanford AIMI INSPECT chest CT | CT | Needs the owner | restricted |  |  |  |  |  |  | [#19](https://github.com/OpenSpineConsortium/spine-datasets/issues/19) |
| Stanford AIMI Merlin abdominal CT | CT | Needs the owner | restricted |  |  |  |  |  |  | [#18](https://github.com/OpenSpineConsortium/spine-datasets/issues/18) |
| FDG-PET-CT-Lesions (autoPET), TCIA through NBIA | CT | Held by the owner | open | 900 |  |  |  | 900 | 250.6 GB |  |
| TotalSegmentator datasets v2.0.1 and v3.0.0 | CT | Held by the owner | open |  |  |  |  | 1,935 |  |  |
| VerSe 2019 and 2020 | CT | Held by the owner | open | 355 |  |  |  | 374 |  |  |
| VerSe 2D projections with soft labels (Zenodo 8115942) | CT | Held by the owner | unknown |  |  |  |  |  |  | [#29](https://github.com/OpenSpineConsortium/spine-datasets/issues/29) |
| WAW-TACE (HCC multiphase CT, Warsaw) | CT | Held by the owner | open | 233 |  |  |  | 228 | 47.1 GB |  |
| LumVBCanSeg lumbar CT (185, ShengJing Hospital) | CT | On the grid | open | 185 |  |  |  |  | 10.1 GB | [#55](https://github.com/OpenSpineConsortium/spine-datasets/issues/55) |
| MedPelvis3D pelvic CT (99, PLA General Hospital) | CT | On the grid | open | 99 |  |  |  |  | 31.4 GB | [#56](https://github.com/OpenSpineConsortium/spine-datasets/issues/56) |
| International TMTV Benchmark, lymphoma FDG PET/CT (60) | CT | On the grid | open | 60 |  |  |  |  | 6.8 GB | [#57](https://github.com/OpenSpineConsortium/spine-datasets/issues/57) |
| TotalSegmentator task data 'hip_implant' (71 CT) | CT | Held by the owner | open | 71 |  |  |  |  | 9.0 GB | [#66](https://github.com/OpenSpineConsortium/spine-datasets/issues/66) |
| TotalSegmentator task data 'liver_lesions' (842 CT) | CT | Held by the owner | open | 842 |  |  |  |  | 38.9 GB | [#67](https://github.com/OpenSpineConsortium/spine-datasets/issues/67) |
| TotalSegmentator task data 'pleural_pericard_effusion' (600 CT) | CT | Held by the owner | open | 600 |  |  |  |  | 9.0 GB | [#68](https://github.com/OpenSpineConsortium/spine-datasets/issues/68) |
| UniToChest chest CT (623 patients; distributed as slices) | CT | On the grid | open | 623 |  |  |  |  | 84.1 GB | [#58](https://github.com/OpenSpineConsortium/spine-datasets/issues/58) |
| VSDFullBody: post-mortem whole-body CT, forensic institutes Bern and Zurich | CT | Held by the owner | restricted | 100 |  |  |  |  | 116.3 GB | [#59](https://github.com/OpenSpineConsortium/spine-datasets/issues/59) |
| Veterinary: canine lateral thoracic radiographs for vertebral heart size (Mendeley ktx4cj55pn) | Veterinary and later | Downloadable now | open |  | 152 |  |  |  |  | [#32](https://github.com/OpenSpineConsortium/spine-datasets/issues/32) |
| Veterinary: pig lower limb CT, CBCT and planar images (Goswami 2020, IEEE DataPort) | Veterinary and later | Held by the owner | open | 1 | 14 |  |  | 3 | 205.0 MB | [#22](https://github.com/OpenSpineConsortium/spine-datasets/issues/22) |

Tasks whose record is not written yet:

- [#170](https://github.com/OpenSpineConsortium/spine-datasets/issues/170) Obtain the IPCAI 2025 language digital twin cadaver set (Killeen 2025, Google Drive, 845 MB)
- [#171](https://github.com/OpenSpineConsortium/spine-datasets/issues/171) Obtain FluoroSeg (Killeen 2025, Hugging Face, gated; CC BY-NC-SA 4.0 per its code repository, card to confirm): 2.95 million synthetic X-rays with masks, text and poses from 1,621 CTs
- [#195](https://github.com/OpenSpineConsortium/spine-datasets/issues/195) Ask BG Klinik Ludwigshafen for the MINTOS cadaver series on three C-arms (Brunken et al. 2026)

## CT, by region and masks

Every record that holds CT: 105 sets, 89 of them on the grid. A set counts in
each region its field of view covers; a sum counts a CT twice where two records hold it. The page
with filters, and each set's masks in full, is census-ct.html beside this file.

| | |
|---|---|
| Sets that hold CT | 105 |
| On the grid | 89 |
| CT volumes on the grid | 24,959 (70 of 89 sets counted) |
| Subjects on the grid | 25,991 (80 of 89 sets counted) |
| Size on the grid | 3.8 TB (78 of 89 sets counted) |
| On the grid with the source's vertebra masks by level | 4,208 CT volumes in 6 sets |
| On the grid with masks made on the grid | 15,753 CT volumes in 62 sets, 20 of them counted |
| Sets whose masks are surveyed | 105 of 105 |

| Region | Sets | On the grid | CT volumes on the grid |
|---|---|---|---|
| head and neck | 4 | 4 | 3,387 |
| chest | 60 | 54 | 10,567 (44 of 54 sets counted) |
| abdomen | 60 | 55 | 18,230 (49 of 55 sets counted) |
| pelvis | 55 | 50 | 9,317 (44 of 50 sets counted) |
| spine | 28 | 23 | 8,683 (19 of 23 sets counted) |
| whole body | 30 | 28 | 5,306 (23 of 28 sets counted) |
| other | 22 | 21 | 1,674 (18 of 21 sets counted) |

| Dataset | Stage | CT volumes | Regions | Masks | Task |
|---|---|---|---|---|---|
| AbdomenAtlas 3.0 Mini (= AbdomenAtlas 1.1 images) | Held by the owner | 7,649 | abdomen | from the source: not recorded; made on the grid: vertebrae by level, on the grid |  |
| PANORAMA public set (pancreas CE-CT) | Held by the owner | 2,024 | chest, abdomen, pelvis | from the source: not recorded; made on the grid: vertebrae by level, on the grid |  |
| RSNA 2022 cervical spine fracture CT (Kaggle) | Held by the owner | 2,019 | spine | from the source: vertebrae by level, on the grid; made on the grid: vertebrae by level, on the grid |  |
| TotalSegmentator datasets v2.0.1 and v3.0.0 | Held by the owner | 1,935 | head and neck, chest, abdomen, pelvis, spine, whole body | from the source: vertebrae by level, on the grid; from the source: vertebrae by level, on the grid; made on the grid: vertebrae by level, on the grid; made on the grid: vertebrae by level, on the grid; made on the grid: vertebrae by level, on the grid |  |
| CTSpine1K | Held by the owner | 1,005 | head and neck, chest, abdomen, spine | from the source: vertebrae by level, on the grid |  |
| FDG-PET-CT-Lesions (autoPET), TCIA through NBIA | Held by the owner | 900 | whole body | from the source: not recorded; made on the grid: vertebrae by level, on the grid |  |
| CTSpinoPelvic1K v11 (the consortium's own release) | Held by the owner | 802 | chest, abdomen, pelvis, spine | from the source: vertebrae by level, on the grid; made on the grid: vertebrae by level, on the grid; made on the grid: vertebrae by level, on the grid |  |
| AMOS22 CT, unlabelled (ids 5000-6899) and labelled | Held by the owner | 723 | abdomen | from the source: vertebrae not recorded, on the grid; made on the grid: vertebrae by level, on the grid |  |
| COBRA2026 public cases (Elekta and Varian) | Held by the owner | 692 | pelvis, spine | from the source: none; made on the grid: vertebrae by level, on the grid; made on the grid: vertebrae by level, on the grid; made on the grid: vertebrae by level, on the grid |  |
| RibFrac (MICCAI 2020) chest CT | Held by the owner | 660 | chest, spine | from the source: no vertebrae, on the grid; from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| NLST, the seeded 500-person pilot | Held by the owner | 500 | chest, other | from the source: no vertebrae; from the source: no vertebrae; from the source: vertebrae by level; from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| IDC `covid_19_ny_sbu` (COVID-19-NY-SBU) | Held by the owner | 443 | chest, abdomen, pelvis, whole body | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `eay131` (EAY131 (NCI-MATCH)) | Held by the owner | 376 | chest, abdomen, pelvis, spine, whole body, other | from the source: no vertebrae; from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| IDC `psma_pet_ct_lesions` (PSMA-PET-CT-Lesions (autoPET III)) | Held by the owner | 374 | whole body | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| VerSe 2019 and 2020 | Held by the owner | 374 | spine | from the source: vertebrae by level, on the grid; made on the grid: vertebrae by level, on the grid; made on the grid: vertebrae by level, on the grid |  |
| IDC `pediatric_ct_seg` (Pediatric-CT-SEG) | Held by the owner | 352 | chest, abdomen, pelvis | from the source: vertebrae as one; made on the grid: vertebrae by level, on the grid |  |
| PENGWIN 2026 peripelvic fracture CT (the public cases) | Held by the owner | 340 | pelvis | from the source: vertebrae not recorded, on the grid; made on the grid: vertebrae by level, on the grid |  |
| IDC `mediastinal_lymph_node_seg` | Held by the owner | 316 | head and neck, chest, abdomen, pelvis, whole body | from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| LUMOS (Zhejiang University) | Held by the owner | 280 | spine | from the source: not recorded | [#27](https://github.com/OpenSpineConsortium/spine-datasets/issues/27) |
| WAW-TACE (HCC multiphase CT, Warsaw) | Held by the owner | 228 | abdomen | from the source: not recorded; made on the grid: vertebrae by level, on the grid |  |
| Kidney abnormality segmentation in thorax-abdomen CT | Held by the owner | 215 | chest, abdomen | from the source: vertebrae not recorded; made on the grid: vertebrae by level, on the grid |  |
| Barts CRL (colorectal-cancer staging CT) | Held by the owner | 212 | chest, abdomen, pelvis | from the source: not recorded; made on the grid: vertebrae by level, on the grid |  |
| CTPelvic1K | Held by the owner | 172 | pelvis, spine | from the source: vertebrae as one, on the grid; made on the grid: vertebrae by level, on the grid |  |
| IDC `lung_pet_ct_dx` (Lung-PET-CT-Dx) | Held by the owner | 158 | chest, abdomen, whole body, other | from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| C-ArmLSpine (Zhang et al., Medical Image Analysis 2024) | Held by the owner | 149 | spine | from the source: none; made on the grid: vertebrae by level, on the grid; made on the grid: vertebrae by level, on the grid |  |
| IDC `acrin_nsclc_fdg_pet` | Held by the owner | 131 | head and neck, chest, abdomen, pelvis, whole body, other | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `tcga_kirc` | Held by the owner | 129 | chest, abdomen, pelvis | from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| IDC `rider_lung_pet_ct` | Held by the owner | 117 | chest, abdomen, pelvis, whole body | from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| CURVAS-PDACVI (MICCAI 2025) | Held by the owner | 101 | chest, abdomen, pelvis | from the source: not recorded, on the grid; made on the grid: vertebrae by level, on the grid |  |
| IDC `hcc_tace_seg` (HCC-TACE-Seg) | Held by the owner | 101 | chest, abdomen, pelvis | from the source: no vertebrae; from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| PENGWIN 2024 Task 2 synthetic X-rays | Held by the owner | 100 | pelvis, spine | from the source: vertebrae not recorded, on the grid | [#30](https://github.com/OpenSpineConsortium/spine-datasets/issues/30) |
| IDC `midrc_ricord_1a` | Held by the owner | 98 | chest, abdomen, other | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `colorectal_liver_metastases` (Colorectal-Liver-Metastases) | Held by the owner | 80 | abdomen | from the source: no vertebrae; from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| IDC `tcga_blca` | Held by the owner | 79 | chest, abdomen, pelvis, whole body | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `cmb_lca` | Held by the owner | 75 | chest, abdomen, pelvis, whole body, other | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| CURVAS 2024 | Held by the owner | 70 | chest, abdomen, pelvis, whole body | from the source: not recorded, on the grid; made on the grid: vertebrae by level, on the grid |  |
| IDC `cptac_ucec` | Held by the owner | 66 | chest, abdomen, pelvis, whole body | from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| IDC `cptac_pda` | Held by the owner | 62 | chest, abdomen, pelvis, other | from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| IDC `pelvic_reference_data` | Held by the owner | 58 | abdomen, pelvis, other | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| AortaSeg-60 | Held by the owner | 55 | chest, abdomen, pelvis | from the source: not recorded; made on the grid: vertebrae by level, on the grid |  |
| DEEP-PSMA (PSMA + FDG PET/CT, mCRPC) | Held by the owner | 53 | whole body | from the source: not recorded, on the grid; made on the grid: vertebrae by level, on the grid |  |
| IDC `cptac_ccrcc` | Held by the owner | 48 | chest, abdomen, pelvis, other | from the source: no vertebrae; from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| QUADRA_HC total-body FDG-PET/CT, healthy controls | Held by the owner | 48 | whole body | from the source: not recorded, on the grid; made on the grid: vertebrae by level, on the grid |  |
| IDC `tcga_stad` | Held by the owner | 45 | abdomen | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `tcga_lihc` | Held by the owner | 42 | chest, abdomen, pelvis | from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| IDC `pancreatic_ct_cbct_seg` | Held by the owner | 40 | abdomen, pelvis | from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| IDC `tcga_ucec` | Held by the owner | 38 | chest, abdomen, pelvis, other | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `varepop_apollo` | Held by the owner | 35 | chest, abdomen, pelvis, spine | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `anti_pd_1_lung` | Held by the owner | 34 | chest, abdomen, pelvis, whole body | from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| IDC `ctpred_sunitinib_pannet` | Held by the owner | 34 | chest, abdomen, pelvis, other | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `cmb_crc` | Held by the owner | 30 | chest, abdomen, pelvis, whole body, other | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `adrenal_acc_ki67_seg` | Held by the owner | 29 | chest, abdomen, pelvis | from the source: no vertebrae; made on the grid: vertebrae by level, on the grid |  |
| IDC `tcga_ov` | Held by the owner | 24 | chest, abdomen, pelvis | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `cmb_mel` | Held by the owner | 23 | chest, abdomen, pelvis, spine, whole body | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `covid_19_ar` | Held by the owner | 23 | chest, abdomen, pelvis | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `cmb_brca` | Held by the owner | 21 | chest, abdomen, pelvis, whole body | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| CSI 2014 spine CT | Held by the owner | 20 | spine | from the source: not recorded; made on the grid: vertebrae by level, on the grid |  |
| IDC `ct_vs_pet_ventilation_imaging` | Held by the owner | 20 | chest, abdomen | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| DeepFluoro (Grupp et al., IPCAI 2020): the H5 release and the vendor DICOMs | Held by the owner | 19 | pelvis, spine | from the source: vertebrae as one, on the grid; made on the grid: vertebrae not recorded |  |
| IDC `cptac_stad` | Held by the owner | 19 | chest, abdomen, pelvis | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `cmb_mml` | Held by the owner | 16 | chest, abdomen, pelvis, spine, whole body, other | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `tcga_esca` | Held by the owner | 16 | chest, abdomen, other | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `acrin_flt_breast` | Held by the owner | 15 | whole body | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `cptac_sar` | Held by the owner | 14 | chest, abdomen, pelvis, whole body, other | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `cptac_cm` | Held by the owner | 12 | chest, abdomen, pelvis, whole body, other | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IDC `cmb_ov` | Held by the owner | 7 | chest, abdomen, pelvis | from the source: none; made on the grid: vertebrae by level, on the grid |  |
| IPCAI 2025 paired X-ray and CT set of the distal femur (Flepp 2025, Zenodo 15753063) | Held by the owner | 5 | other | from the source: no vertebrae, on the grid | [#34](https://github.com/OpenSpineConsortium/spine-datasets/issues/34) |
| Ljubljana 2D/3D registration gold standard (PIXIUM 4600) | Held by the owner | 5 | spine | from the source: vertebrae by level, on the grid |  |
| Veterinary: pig lower limb CT, CBCT and planar images (Goswami 2020, IEEE DataPort) | Held by the owner | 3 | other | from the source: none | [#22](https://github.com/OpenSpineConsortium/spine-datasets/issues/22) |
| Geneva hip phantom (BV Pulsera; D'Isidoro et al., Medical Physics 2021) | Held by the owner | 1 | pelvis, spine | from the source: none; made on the grid: vertebrae not recorded |  |
| IDC `cptac_lscc` (tier 2) | Held by the owner |  | chest, abdomen, pelvis, whole body, other | from the source: none | [#45](https://github.com/OpenSpineConsortium/spine-datasets/issues/45) |
| IDC `cptac_luad` (tier 2) | Held by the owner |  | chest, abdomen, whole body, other | from the source: none | [#46](https://github.com/OpenSpineConsortium/spine-datasets/issues/46) |
| IDC `ldct_and_projection_data` (tier 2) | Held by the owner |  | chest | from the source: none | [#47](https://github.com/OpenSpineConsortium/spine-datasets/issues/47) |
| IDC `midrc_ricord_1b` (tier 2) | Held by the owner |  | chest, abdomen, pelvis, other | from the source: none | [#49](https://github.com/OpenSpineConsortium/spine-datasets/issues/49) |
| IDC `nsclc_radiogenomics` (tier 2) | Held by the owner |  | chest, abdomen, pelvis, whole body | from the source: no vertebrae; from the source: no vertebrae | [#50](https://github.com/OpenSpineConsortium/spine-datasets/issues/50) |
| IDC `nsclc_radiomics` (tier 2) | Held by the owner |  | chest | from the source: no vertebrae; from the source: no vertebrae; from the source: no vertebrae | [#51](https://github.com/OpenSpineConsortium/spine-datasets/issues/51) |
| IDC `spinal_multiple_myeloma_seg` (tier 2) | Held by the owner |  | spine | from the source: vertebrae by level | [#53](https://github.com/OpenSpineConsortium/spine-datasets/issues/53) |
| IDC `spine_mets_ct_seg` (tier 2) | Held by the owner |  | abdomen, pelvis, spine | from the source: vertebrae by level | [#54](https://github.com/OpenSpineConsortium/spine-datasets/issues/54) |
| International TMTV Benchmark, lymphoma FDG PET/CT (60) | On the grid |  | whole body | from the source: not recorded, on the grid | [#57](https://github.com/OpenSpineConsortium/spine-datasets/issues/57) |
| LumVBCanSeg lumbar CT (185, ShengJing Hospital) | On the grid |  | spine | from the source: not recorded, on the grid | [#55](https://github.com/OpenSpineConsortium/spine-datasets/issues/55) |
| MedPelvis3D pelvic CT (99, PLA General Hospital) | On the grid |  | pelvis | from the source: not recorded, on the grid | [#56](https://github.com/OpenSpineConsortium/spine-datasets/issues/56) |
| RSNA pulmonary embolism CT (RSPECT) | Held by the owner |  | chest | from the source: not recorded | [#88](https://github.com/OpenSpineConsortium/spine-datasets/issues/88) |
| STOIC2021 training (AWS Open Data) | Held by the owner |  | chest | from the source: not recorded | [#44](https://github.com/OpenSpineConsortium/spine-datasets/issues/44) |
| TotalSegmentator task data 'hip_implant' (71 CT) | Held by the owner |  | pelvis | from the source: not recorded | [#66](https://github.com/OpenSpineConsortium/spine-datasets/issues/66) |
| TotalSegmentator task data 'liver_lesions' (842 CT) | Held by the owner |  | abdomen | from the source: not recorded | [#67](https://github.com/OpenSpineConsortium/spine-datasets/issues/67) |
| TotalSegmentator task data 'pleural_pericard_effusion' (600 CT) | Held by the owner |  | chest | from the source: not recorded | [#68](https://github.com/OpenSpineConsortium/spine-datasets/issues/68) |
| UniToChest chest CT (623 patients; distributed as slices) | On the grid |  | chest | from the source: not recorded, on the grid | [#58](https://github.com/OpenSpineConsortium/spine-datasets/issues/58) |
| VerSe 2D projections with soft labels (Zenodo 8115942) | Held by the owner |  | spine | from the source: none | [#29](https://github.com/OpenSpineConsortium/spine-datasets/issues/29) |
| VSDFullBody: post-mortem whole-body CT, forensic institutes Bern and Zurich | Held by the owner |  | whole body | from the source: not recorded | [#59](https://github.com/OpenSpineConsortium/spine-datasets/issues/59) |
| AbdomenAtlas 2.0 Mini (10,135 CT) | Asked, waiting | 10,135 | abdomen | from the source: not recorded | [#89](https://github.com/OpenSpineConsortium/spine-datasets/issues/89) |
| LevelCheck clinical cohort (Johns Hopkins, Siewerdsen group) | Refused | 202 | spine | from the source: not recorded | [#60](https://github.com/OpenSpineConsortium/spine-datasets/issues/60) |
| Huashan Hospital, Fudan University, intraoperative lumbar films with preoperative CT (Shao et al. 2024) | Asked, waiting | 140 | spine | from the source: not recorded | [#61](https://github.com/OpenSpineConsortium/spine-datasets/issues/61) |
| NIT Warangal and NIMS Hyderabad intraoperative C-arm sets (2D-3D-sci-registration) | Asked, waiting | 9 | spine | from the source: none | [#64](https://github.com/OpenSpineConsortium/spine-datasets/issues/64) |
| Balgrist ex-vivo lumbar CT plus C-arm (Jecklin) | Refused |  | spine | from the source: not recorded | [#69](https://github.com/OpenSpineConsortium/spine-datasets/issues/69) |
| CADS CT (unique cases) | Granted, fetch pending |  | whole body | from the source: not recorded | [#86](https://github.com/OpenSpineConsortium/spine-datasets/issues/86) |
| COBRA2026 embargoed cases | Later |  | pelvis, spine | from the source: none | [#92](https://github.com/OpenSpineConsortium/spine-datasets/issues/92) |
| CT-RATE chest CT | Granted, fetch pending |  | chest | from the source: not recorded | [#85](https://github.com/OpenSpineConsortium/spine-datasets/issues/85) |
| ENHANCE.PET 1.6k: whole-/total-body FDG-PET/CT, 1,683 studies (NIfTI) | To ask |  | whole body | from the source: not recorded | [#90](https://github.com/OpenSpineConsortium/spine-datasets/issues/90) |
| IDC `lidc_idri` (tier 2) | Downloadable now |  | chest, abdomen, pelvis | from the source: no vertebrae; from the source: no vertebrae | [#48](https://github.com/OpenSpineConsortium/spine-datasets/issues/48) |
| IDC `prostate_anatomical_edge_cases` (tier 2) | Downloadable now |  | pelvis | from the source: no vertebrae | [#52](https://github.com/OpenSpineConsortium/spine-datasets/issues/52) |
| MAGIC-CT (Zenodo) | Needs the owner |  | chest, abdomen | from the source: not recorded | [#7](https://github.com/OpenSpineConsortium/spine-datasets/issues/7) |
| NLST, full (tier 2; 500-person pilot fetched) | To ask |  | chest, other | from the source: no vertebrae; from the source: no vertebrae; from the source: vertebrae by level; from the source: no vertebrae | [#91](https://github.com/OpenSpineConsortium/spine-datasets/issues/91) |
| RSNA abdominal trauma CT (RATIC) | Granted, fetch pending |  | chest, abdomen, pelvis | from the source: not recorded | [#87](https://github.com/OpenSpineConsortium/spine-datasets/issues/87) |
| Stanford AIMI INSPECT chest CT | Needs the owner |  | chest | from the source: not recorded | [#19](https://github.com/OpenSpineConsortium/spine-datasets/issues/19) |
| Stanford AIMI Merlin abdominal CT | Needs the owner |  | abdomen, pelvis | from the source: not recorded | [#18](https://github.com/OpenSpineConsortium/spine-datasets/issues/18) |

What the CT records still lack:

- LUMOS (Zhejiang University): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- AbdomenAtlas 3.0 Mini (= AbdomenAtlas 1.1 images): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- AortaSeg-60: on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- STOIC2021 training (AWS Open Data): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- Barts CRL (colorectal-cancer staging CT): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- CSI 2014 spine CT: on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- CURVAS 2024: on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- CURVAS-PDACVI (MICCAI 2025): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- DEEP-PSMA (PSMA + FDG PET/CT, mCRPC): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- PANORAMA public set (pancreas CE-CT): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- QUADRA_HC total-body FDG-PET/CT, healthy controls: on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- RSNA pulmonary embolism CT (RSPECT): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- FDG-PET-CT-Lesions (autoPET), TCIA through NBIA: on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- WAW-TACE (HCC multiphase CT, Warsaw): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- LumVBCanSeg lumbar CT (185, ShengJing Hospital): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- MedPelvis3D pelvic CT (99, PLA General Hospital): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- International TMTV Benchmark, lymphoma FDG PET/CT (60): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- TotalSegmentator task data 'hip_implant' (71 CT): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- TotalSegmentator task data 'liver_lesions' (842 CT): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- TotalSegmentator task data 'pleural_pericard_effusion' (600 CT): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- UniToChest chest CT (623 patients; distributed as slices): on the grid, and what masks its source ships is not recorded yet; its entry says where to look
- VSDFullBody: post-mortem whole-body CT, forensic institutes Bern and Zurich: on the grid, and what masks its source ships is not recorded yet; its entry says where to look

## What the records still lack

- Balgrist ex-vivo lumbar CT plus C-arm (Jecklin): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- C-ArmLSpine (Zhang et al., Medical Image Analysis 2024): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- DeepFluoro (Grupp et al., IPCAI 2020): the H5 release and the vendor DICOMs: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- Geneva hip phantom (BV Pulsera; D'Isidoro et al., Medical Physics 2021): on the grid with no size: write the landing pass's bytes into measured
- Geneva hip phantom (BV Pulsera; D'Isidoro et al., Medical Physics 2021): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- Ljubljana 2D/3D registration gold standard (PIXIUM 4600): on the grid with no size: write the landing pass's bytes into measured
- Ljubljana 2D/3D registration gold standard (PIXIUM 4600): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- LUMOS (Zhejiang University): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- PUMCH stitching series (Liu et al., Eur Spine J 2026): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- SX-Stitch intraoperative C-arm series (Li 2024, PUMCH): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- Vanderbilt intraoperative THA fluoroscopy (Chan et al., J Arthroplasty 2025): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- CADICA invasive coronary angiography sequences (Mendeley p9bpx9ctcv): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- CathAction (Jianu et al. 2024, AIRVLab): on the grid with no size: write the landing pass's bytes into measured
- CathAction (Jianu et al. 2024, AIRVLab): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- CathAction (Jianu et al. 2024, AIRVLab): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- Coronary angiography sets (CADICA, ARCADE, XCAD, AngioCAD): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- DARADIA vertebroplasty video (Kolkata): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- DMX Imaging digital motion X-ray: no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- DysphagiaBank (TalkBank), UNM corpus: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- DysphagiaBank (TalkBank), UNM corpus: no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- ThePainSource (Faubel) fluoroscopy clips: no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- Guide3D (ACCV 2024, AIRVLab): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- Konica Minolta dynamic digital radiography sequences: no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- Manual Therapy Foundation of India lumbar coupling video: no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- Neurosurgical Focus: Video (every article CC BY 4.0): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- Radiopaedia spine cases: no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- Veriserum (ETH Zurich, MICCAI 2025): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- VFSS2022 videofluoroscopic swallow frames (TIB): the licence is still to confirm on the source's page
- COBRA2026 public cases (Elekta and Varian): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IPCAI 2025 paired X-ray and CT set of the distal femur (Flepp 2025, Zenodo 15753063): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- Aariz cephalometric benchmark (Khalid, Fraz 2023) and the ISBI 2015 cephalograms: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- AASCE 2019 / BoostNet AP whole-spine films: on the grid with no size: write the landing pass's bytes into measured
- AASCE 2019 / BoostNet AP whole-spine films: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- BIMCV COVID-19+ chest films (IEEE DataPort): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- BUU-LSPINE (Klinwichit et al., Applied Sciences 2023): on the grid with no size: write the landing pass's bytes into measured
- BUU-LSPINE (Klinwichit et al., Applied Sciences 2023): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- CSXA, the Cervical Spine X-ray Atlas V3.0 (Ran et al., Scientific Data 2024): on the grid with no size: write the landing pass's bytes into measured
- CSXA, the Cervical Spine X-ray Atlas V3.0 (Ran et al., Scientific Data 2024): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- Fraiwan spine X-ray set (Mendeley xkt857dsxk): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- Harms Study Group registries (adolescent idiopathic scoliosis and other pediatric spinal deformity): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- Kaggle scoliosis YOLOv5 annotated spine X-ray set (salmankey): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- KUB-StoneX (Daffodil International University HIRL): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- Mendeley DDH hip sets (jf3pv98m9g and 4gvcb6gmh2): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- Mendeley DDH hip sets (jf3pv98m9g and 4gvcb6gmh2): the licence is still to confirm on the source's page
- MIMIC-CXR and MIMIC-CXR-JPG (PhysioNet): the licence is still to confirm on the source's page
- MrOS lateral spine radiographs (Osteoporotic Fractures in Men): the licence is still to confirm on the source's page
- NHANES II spinal films with landmarks (Mo, Papiez, Chen et al., Zenodo): on the grid with no size: write the landing pass's bytes into measured
- NHANES II spinal films with landmarks (Mo, Papiez, Chen et al., Zenodo): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- NHANES II cervical and lumbar spine films (NCHS, 1976 to 1980): on the grid with no size: write the landing pass's bytes into measured
- NHANES II cervical and lumbar spine films (NCHS, 1976 to 1980): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- NIH ChestX-ray14 and the RSNA pneumonia subset: on the grid with no size: write the landing pass's bytes into measured
- NIH ChestX-ray14 and the RSNA pneumonia subset: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- Open-i Indiana chest collection: the licence is still to confirm on the source's page
- SOF lateral spine radiographs (Study of Osteoporotic Fractures): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- SOF lateral spine radiographs (Study of Osteoporotic Fractures): the licence is still to confirm on the source's page
- TVGH ankylosing spondylitis cervical and lumbar spine films: no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- TVGH-SpineXR: no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- VertXNet extra labels for NHANES II (Mo, Papiez, Chen 2023): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- VertXNet extra labels for NHANES II (Mo, Papiez, Chen 2023): the licence is still to confirm on the source's page
- VinDr-CXR (PhysioNet): the licence is still to confirm on the source's page
- VinDr-SpineXR (Nguyen et al., MICCAI 2021): on the grid with no size: write the landing pass's bytes into measured
- VinDr-SpineXR (Nguyen et al., MICCAI 2021): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- AbdomenAtlas 3.0 Mini (= AbdomenAtlas 1.1 images): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- AMOS22 CT, unlabelled (ids 5000-6899) and labelled: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- AortaSeg-60: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- STOIC2021 training (AWS Open Data): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- Barts CRL (colorectal-cancer staging CT): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- CADS CT (unique cases): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- CSI 2014 spine CT: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- CT-RATE chest CT: no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- CTPelvic1K: on the grid with no size: write the landing pass's bytes into measured
- CTPelvic1K: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- CTPelvic1K: the licence is still to confirm on the source's page
- CTSpine1K: on the grid with no size: write the landing pass's bytes into measured
- CTSpine1K: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- CTSpinoPelvic1K v11 (the consortium's own release): on the grid with no size: write the landing pass's bytes into measured
- CTSpinoPelvic1K v11 (the consortium's own release): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- CURVAS 2024: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- CURVAS-PDACVI (MICCAI 2025): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- DEEP-PSMA (PSMA + FDG PET/CT, mCRPC): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `acrin_flt_breast`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `acrin_nsclc_fdg_pet`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `adrenal_acc_ki67_seg`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `anti_pd_1_lung`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `cmb_brca`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `cmb_crc`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `cmb_lca`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `cmb_mel`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `cmb_mml`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `cmb_ov`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `colorectal_liver_metastases` (Colorectal-Liver-Metastases): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `covid_19_ar`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `covid_19_ny_sbu` (COVID-19-NY-SBU): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `cptac_ccrcc`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `cptac_cm`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `cptac_lscc` (tier 2): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `cptac_luad` (tier 2): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `cptac_pda`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `cptac_sar`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `cptac_stad`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `cptac_ucec`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `ct_vs_pet_ventilation_imaging`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `ctpred_sunitinib_pannet`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `eay131` (EAY131 (NCI-MATCH)): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `hcc_tace_seg` (HCC-TACE-Seg): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `ldct_and_projection_data` (tier 2): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `lung_pet_ct_dx` (Lung-PET-CT-Dx): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `mediastinal_lymph_node_seg`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `midrc_ricord_1a`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `midrc_ricord_1b` (tier 2): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `nsclc_radiogenomics` (tier 2): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `nsclc_radiomics` (tier 2): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `pancreatic_ct_cbct_seg`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `pediatric_ct_seg` (Pediatric-CT-SEG): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `pelvic_reference_data`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `psma_pet_ct_lesions` (PSMA-PET-CT-Lesions (autoPET III)): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `rider_lung_pet_ct`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `spinal_multiple_myeloma_seg` (tier 2): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `spine_mets_ct_seg` (tier 2): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `tcga_blca`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `tcga_esca`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `tcga_kirc`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `tcga_lihc`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `tcga_ov`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `tcga_stad`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `tcga_ucec`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- IDC `varepop_apollo`: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- Kidney abnormality segmentation in thorax-abdomen CT: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- MAGIC-CT (Zenodo): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- NLST, the seeded 500-person pilot: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- PANORAMA public set (pancreas CE-CT): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- PENGWIN 2026 peripelvic fracture CT (the public cases): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- PENGWIN 2024 Task 2 synthetic X-rays: on the grid with no size: write the landing pass's bytes into measured
- PENGWIN 2024 Task 2 synthetic X-rays: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- QUADRA_HC total-body FDG-PET/CT, healthy controls: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- RibFrac (MICCAI 2020) chest CT: on the grid with no size: write the landing pass's bytes into measured
- RibFrac (MICCAI 2020) chest CT: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- RSNA 2022 cervical spine fracture CT (Kaggle): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- RSNA abdominal trauma CT (RATIC): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- RSNA pulmonary embolism CT (RSPECT): on the grid with no size: write the landing pass's bytes into measured
- RSNA pulmonary embolism CT (RSPECT): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- RSNA pulmonary embolism CT (RSPECT): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- ENHANCE.PET 1.6k: whole-/total-body FDG-PET/CT, 1,683 studies (NIfTI): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- Stanford AIMI INSPECT chest CT: no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- Stanford AIMI Merlin abdominal CT: no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- FDG-PET-CT-Lesions (autoPET), TCIA through NBIA: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- TotalSegmentator datasets v2.0.1 and v3.0.0: on the grid with no size: write the landing pass's bytes into measured
- TotalSegmentator datasets v2.0.1 and v3.0.0: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- VerSe 2019 and 2020: on the grid with no size: write the landing pass's bytes into measured
- VerSe 2019 and 2020: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- VerSe 2D projections with soft labels (Zenodo 8115942): on the grid with no size: write the landing pass's bytes into measured
- VerSe 2D projections with soft labels (Zenodo 8115942): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- VerSe 2D projections with soft labels (Zenodo 8115942): no count the census can read: add subjects, xray_images, videos, run_frames or ct_volumes to counts
- WAW-TACE (HCC multiphase CT, Warsaw): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- LumVBCanSeg lumbar CT (185, ShengJing Hospital): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- MedPelvis3D pelvic CT (99, PLA General Hospital): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- International TMTV Benchmark, lymphoma FDG PET/CT (60): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- TotalSegmentator task data 'hip_implant' (71 CT): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- TotalSegmentator task data 'liver_lesions' (842 CT): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- TotalSegmentator task data 'pleural_pericard_effusion' (600 CT): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- UniToChest chest CT (623 patients; distributed as slices): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- VSDFullBody: post-mortem whole-body CT, forensic institutes Bern and Zurich: on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it
- Veterinary: pig lower limb CT, CBCT and planar images (Goswami 2020, IEEE DataPort): on the grid and not frozen: run tools/freeze.py on its folder and write frozen/<id>.json and measured from it

## Changes, newest first

- 2026-10-23 RSNA pulmonary embolism CT (RSPECT): grid_path none to /rs/rs_grp_oschome/go2432/data/rsna_rspect_pe/raw; stage granted to held; status granted to held
- 2026-10-23 MTDDH paediatric pelvic X-rays with hip dysplasia key points (Qi et al., Science Data Bank 2025): record added
- 2026-10-23 Harms Study Group registries (adolescent idiopathic scoliosis and other pediatric spinal deformity): record added
- 2026-10-23 Radiopaedia spine cases: stage asked to granted; status requested to granted
- 2026-10-23 LevelCheck clinical cohort (Johns Hopkins, Siewerdsen group): stage asked to refused; status requested to refused; tier C to D
- 2026-10-23 CM Spine (Zeng et al., Electronics 2024): 208 intraoperative lumbar G-arm images: stage to-ask to asked; status todo to requested
- 2026-10-23 CM Spine (Zeng et al., Electronics 2024): 208 intraoperative lumbar G-arm images: route owner-only to letter
- 2026-10-23 CAMS-Knee (ETH Zurich and Charite Berlin, J Biomech 2017): record added
- 2026-10-23 CM Spine (Zeng et al., Electronics 2024): 208 intraoperative lumbar G-arm images: licence not recorded to none stated: the paper's data statement and its repository's README name no licence, and the repository has no licence file (read 2026-10-23); xray_images none to 208
- 2026-10-23 the census rules changed; every row was derived afresh
- 2026-10-23 the census rules changed; every row was derived afresh
- 2026-10-23 WAW-TACE (HCC multiphase CT, Warsaw): record added
- 2026-10-23 FDG-PET-CT-Lesions (autoPET), TCIA through NBIA: record added
- 2026-10-23 QUADRA_HC total-body FDG-PET/CT, healthy controls: record added
- 2026-10-23 PENGWIN 2026 peripelvic fracture CT (the public cases): record added
- 2026-10-23 PANORAMA public set (pancreas CE-CT): record added
- 2026-10-23 NLST, the seeded 500-person pilot: record added
- 2026-10-23 Kidney abnormality segmentation in thorax-abdomen CT: record added
- 2026-10-23 IDC `varepop_apollo`: record added
- 2026-10-23 IDC `tcga_ucec`: record added
- 2026-10-23 IDC `tcga_stad`: record added
- 2026-10-23 IDC `tcga_ov`: record added
- 2026-10-23 IDC `tcga_lihc`: record added
- 2026-10-23 IDC `tcga_kirc`: record added
- 2026-10-23 IDC `tcga_esca`: record added
- 2026-10-23 IDC `tcga_blca`: record added
- 2026-10-23 IDC `rider_lung_pet_ct`: record added
- 2026-10-23 IDC `psma_pet_ct_lesions` (PSMA-PET-CT-Lesions (autoPET III)): record added
- 2026-10-23 IDC `pelvic_reference_data`: record added
- 2026-10-23 IDC `pediatric_ct_seg` (Pediatric-CT-SEG): record added
- 2026-10-23 IDC `pancreatic_ct_cbct_seg`: record added
- 2026-10-23 IDC `midrc_ricord_1a`: record added
- 2026-10-23 IDC `mediastinal_lymph_node_seg`: record added
- 2026-10-23 IDC `lung_pet_ct_dx` (Lung-PET-CT-Dx): record added
- 2026-10-23 IDC `hcc_tace_seg` (HCC-TACE-Seg): record added
- 2026-10-23 IDC `eay131` (EAY131 (NCI-MATCH)): record added
- 2026-10-23 IDC `ctpred_sunitinib_pannet`: record added
- 2026-10-23 IDC `ct_vs_pet_ventilation_imaging`: record added
- 2026-10-23 IDC `cptac_ucec`: record added
- 2026-10-23 IDC `cptac_stad`: record added
- 2026-10-23 IDC `cptac_sar`: record added
- 2026-10-23 IDC `cptac_pda`: record added
- 2026-10-23 IDC `cptac_cm`: record added
- 2026-10-23 IDC `cptac_ccrcc`: record added
- 2026-10-23 IDC `covid_19_ny_sbu` (COVID-19-NY-SBU): record added
- 2026-10-23 IDC `covid_19_ar`: record added
- 2026-10-23 IDC `colorectal_liver_metastases` (Colorectal-Liver-Metastases): record added
- 2026-10-23 IDC `cmb_ov`: record added
- 2026-10-23 IDC `cmb_mml`: record added
- 2026-10-23 IDC `cmb_mel`: record added
- 2026-10-23 IDC `cmb_lca`: record added
- 2026-10-23 IDC `cmb_crc`: record added
- 2026-10-23 IDC `cmb_brca`: record added
- 2026-10-23 IDC `anti_pd_1_lung`: record added
- 2026-10-23 IDC `adrenal_acc_ki67_seg`: record added
- 2026-10-23 IDC `acrin_nsclc_fdg_pet`: record added
- 2026-10-23 IDC `acrin_flt_breast`: record added
- 2026-10-23 DEEP-PSMA (PSMA + FDG PET/CT, mCRPC): record added
- 2026-10-23 CURVAS-PDACVI (MICCAI 2025): record added
- 2026-10-23 CURVAS 2024: record added
- 2026-10-23 CSI 2014 spine CT: record added
- 2026-10-23 Barts CRL (colorectal-cancer staging CT): record added
- 2026-10-23 AortaSeg-60: record added
- 2026-10-23 AMOS22 CT, unlabelled (ids 5000-6899) and labelled: record added
- 2026-10-23 AbdomenAtlas 3.0 Mini (= AbdomenAtlas 1.1 images): record added
- 2026-10-23 VSDFullBody: post-mortem whole-body CT, forensic institutes Bern and Zurich: grid_path none to /rs/rs_grp_oschome/go2432/data/zenodo_vsd_fullbody; stage needs-owner to held; status needs-owner to held
- 2026-10-23 Ljubljana 2D/3D registration gold standard (PIXIUM 4600): ct_volumes 1 to 5; licence ND (no derivatives), read-only, as SchwingNet's registry records it; to confirm on the source's page to CC BY-NC-ND, as the source's page gives it (read 2026-10-23); the user guide that comes with the set says the data are used only under an agreement form between the user and the Laboratory of Imaging Technologies, and never redistributed
- 2026-10-23 Geneva hip phantom (BV Pulsera; D'Isidoro et al., Medical Physics 2021): licence not recorded; to confirm on the source's page to CC BY-SA 4.0, as the source's page gives it (read 2026-10-23), which also lists a 'Contract on the use of data' and shows none of its terms
- 2026-10-23 the census rules changed; every row was derived afresh
- 2026-10-23 TotalSegmentator task data 'pleural_pericard_effusion' (600 CT): grid_path none to /rs/rs_grp_oschome/go2432/data/zenodo_ts_task_pleural_effusion; stage asked to held; status requested to held
- 2026-10-23 TotalSegmentator task data 'liver_lesions' (842 CT): grid_path none to /rs/rs_grp_oschome/go2432/data/zenodo_ts_task_liver_lesions; stage asked to held; status requested to held
- 2026-10-23 TotalSegmentator task data 'hip_implant' (71 CT): grid_path none to /rs/rs_grp_oschome/go2432/data/zenodo_ts_task_hip_implant; stage asked to held; status requested to held
- 2026-10-23 VerSe 2D projections with soft labels (Zenodo 8115942): grid_path none to /rs/rs_grp_oschome/go2432/data/verse_2d_projections; stage needs-owner to held; status needs-owner to held
- 2026-10-23 PENGWIN 2024 Task 2 synthetic X-rays: grid_path none to /rs/rs_grp_oschome/go2432/data/pengwin_task2_xrays; stage downloadable to held; status todo to held
- 2026-10-23 IDC `spine_mets_ct_seg` (tier 2): grid_path none to /rs/rs_grp_oschome/go2432/data/idc_spine_mets_ct_seg; stage downloadable to held; status todo to held
- 2026-10-23 IDC `spinal_multiple_myeloma_seg` (tier 2): grid_path none to /rs/rs_grp_oschome/go2432/data/idc_spinal_multiple_myeloma_seg; stage downloadable to held; status todo to held
- 2026-10-23 IDC `nsclc_radiomics` (tier 2): grid_path none to /rs/rs_grp_oschome/go2432/data/idc_nsclc_radiomics; stage downloadable to held; status todo to held
- 2026-10-23 IDC `nsclc_radiogenomics` (tier 2): grid_path none to /rs/rs_grp_oschome/go2432/data/idc_nsclc_radiogenomics; stage downloadable to held; status todo to held
- 2026-10-23 IDC `midrc_ricord_1b` (tier 2): grid_path none to /rs/rs_grp_oschome/go2432/data/idc_midrc_ricord_1b; stage downloadable to held; status todo to held
- 2026-10-23 IDC `ldct_and_projection_data` (tier 2): grid_path none to /rs/rs_grp_oschome/go2432/data/idc_ldct_and_projection_data; stage downloadable to held; status todo to held
- 2026-10-23 IDC `cptac_luad` (tier 2): grid_path none to /rs/rs_grp_oschome/go2432/data/idc_cptac_luad; stage downloadable to held; status todo to held
- 2026-10-23 IDC `cptac_lscc` (tier 2): grid_path none to /rs/rs_grp_oschome/go2432/data/idc_cptac_lscc; stage downloadable to held; status todo to held
- 2026-10-23 STOIC2021 training (AWS Open Data): grid_path none to /rs/rs_grp_oschome/go2432/data/aws_stoic2021; stage downloadable to held; status todo to held
- 2026-10-23 NIH ChestX-ray14 and the RSNA pneumonia subset: grid_path none to /rs/rs_grp_oschome/go2432/data/nih_chestxray14; stage downloadable to held; status todo to held
- 2026-10-23 KUB-StoneX (Daffodil International University HIRL): grid_path none to /rs/rs_grp_oschome/go2432/data/kub_stonex; stage downloadable to held; status todo to held
- 2026-10-23 CathAction (Jianu et al. 2024, AIRVLab): grid_path none to /rs/rs_grp_oschome/go2432/data/cathaction; stage needs-owner to held; status needs-owner to held
- 2026-10-23 LUMOS (Zhejiang University): grid_path none to /rs/rs_grp_oschome/go2432/data/zenodo_lumos; stage needs-owner to held; status needs-owner to held; tier C to A
- 2026-10-23 the census began with 109 records
