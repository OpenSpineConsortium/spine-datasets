# Tasks to open, one per dataset not yet held on the grid

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, derived from SchwingNet's docs/research/xray-dataset-requests.md (the request texts, copied verbatim), docs/research/data-access-requirements.md (who may act) and data/sources/<id>.json (the record).

Each block below is one GitHub issue: the heading is the title, the lines under it the body, and tasks/open_tasks.py opens them in this order with the label todo, skipping a title that already exists. The order is the priority: group 1 is a letter that can go now, group 2 a form, a gate or an account, group 3 a plain download as a grid job, group 4 a request already sent and waiting for its answer, group 5 the owner's hand only, group 6 what waits on time; inside a group the order is data-access-requirements.md's, value first; and since 2026-10-21 an X-ray set (fluoroscopy, video, projections, films) comes before a CT set whatever its group, the owner's order, which the pipeline board (PIPELINE.md on the branch `pipeline`) follows and the position numbers below, written before it, do not. A body never names a method, only the measurement, as CONTRIBUTING.md asks. Nothing below is an instruction to send anything: the task is claimed first.

## Obtain MAGIC-CT (Zenodo)

What it is: 562 CTs; a gated anomaly-harvest collection (group B7)
Link: https://zenodo.org/records/18389015
Why it matters: a Central Asian trunk CT population and scanner protocols no held collection covers
Route in: letter; status now: todo
Letter or form: letters/magic_ct.md
The owner's hand: the application goes from the owner's mailbox with the owner's CITI certificate attached; the agreement's code-release clause is a lawyer question first
Record: datasets/magic_ct.json (reach gated, licence: a data use agreement (non-commercial))
Files likely touched: datasets/magic_ct.json, letters/magic_ct.md
Priority: group 1, a letter that can go now; position 1 of 86

## Obtain cm_spine: one Google Drive file described only as 'intraoperative' (empty download)

What it is: one Google Drive file, id 1r9wX1802gkU4-EQHMMlyAlEiWXGWLhhJ, described only as 'intraoperative' by download_sources.py's get_cm_spine(); the download was empty and what the file is has never been established
Link: no link in the record; see the record's how_to_get
Why it matters: 208 intraoperative lumbar G-arm images with vertebra labels, if the Drive file is that set
Route in: owner-only; status now: todo
Letter or form: letters/cm_spine_drive_file.md
The owner's hand: the owner opens the Drive file in a browser signed in to the owner's Google account; a letter follows only if a source is found
Record: datasets/cm_spine_drive_file.json (reach get, licence: not recorded)
Files likely touched: datasets/cm_spine_drive_file.json, letters/cm_spine_drive_file.md
Priority: group 1, a letter that can go now; position 2 of 86

## Obtain MrOS lateral spine radiographs (Osteoporotic Fractures in Men)

What it is: lateral thoracic and lumbar films of 5,994 men at six US centres, two visits (2000-2002 and about 4.6 years later), with Genant semi-quantitative vertebral fracture grades per vertebra; a published study used 4,461 subjects and 15,524 films
Link: https://mrosonline.ucsf.edu/
Why it matters: the largest lateral spine film set with per-vertebra labels: older osteoporotic spines, the anatomy a C-arm sees in kyphoplasty
Route in: form; status now: todo
Letter or form: letters/mros_lateral_spine.md
The owner's hand: the MrOS Online account, the proposal filed in the owner's name, the data use agreement and any fee
Record: datasets/mros_lateral_spine.json (reach get, licence: a MrOS data request agreement; terms to confirm on the page)
Files likely touched: datasets/mros_lateral_spine.json, letters/mros_lateral_spine.md
Priority: group 2, a form, a gate or an account; position 3 of 86

## Obtain SOF lateral spine radiographs (Study of Osteoporotic Fractures)

What it is: the women's counterpart of MrOS: lateral thoracolumbar films at several visits, about 9,700 women, Genant grading per vertebra; counts to confirm on the page
Link: https://sofonline.ucsf.edu/
Why it matters: the women's counterpart of MrOS; together the largest level-labelled lateral spine film resource
Route in: form; status now: todo
Letter or form: letters/sof_lateral_spine.md
The owner's hand: the SOF Online account, the proposal filed in the owner's name, the data use agreement and any fee
Record: datasets/sof_lateral_spine.json (reach get, licence: a SOF data request agreement; terms to confirm on the page)
Files likely touched: datasets/sof_lateral_spine.json, letters/sof_lateral_spine.md
Priority: group 2, a form, a gate or an account; position 4 of 86

## Obtain ReXGradient-160K (Rajpurkar lab and Gradient Health, 2025)

What it is: 160,000 chest radiograph studies with reports from 109,487 patients at 79 US sites; several images per study, so laterals are likely included (to confirm on the page)
Link: https://huggingface.co/datasets/rajpurkarlab/ReXGradient-160K
Why it matters: 160,000 chest studies from 79 sites: 79 exposure recipes, and lateral chest films are thoracic spine laterals
Route in: form; status now: todo
Letter or form: letters/rexgradient_160k.md
The owner's hand: the gate's agreement checkbox on the owner's Hugging Face account; the clauses on derivatives are a lawyer question first
Record: datasets/rexgradient_160k.json (reach gated, licence: a non-commercial data access and use agreement on the Hugging Face page)
Files likely touched: datasets/rexgradient_160k.json, letters/rexgradient_160k.md
Priority: group 2, a form, a gate or an account; position 5 of 86

## Obtain PadChest (BIMCV, Alicante)

What it is: 160,868 chest radiographs of 67,625 patients, 109 projections including lateral (about 30 percent) and some oblique; labels include 174 findings
Link: https://bimcv.cipf.es/bimcv-projects/padchest/
Why it matters: 160,868 chest films with 109 projections including lateral and oblique, from European devices and film-era plates
Route in: form; status now: todo
Letter or form: letters/padchest.md
The owner's hand: the licence form and its signature; the derivative-works clause is a lawyer question first
Record: datasets/padchest.json (reach gated, licence: research use by request; a licence form on the page)
Files likely touched: datasets/padchest.json, letters/padchest.md
Priority: group 2, a form, a gate or an account; position 6 of 86

## Obtain CheXpert and CheXpert Plus (Stanford AIMI)

What it is: 224,316 chest radiographs of 65,240 patients, frontal and lateral (CheXpert); CheXpert Plus adds reports and DICOM
Link: https://stanfordaimi.azurewebsites.net/
Why it matters: 224,316 chest films, frontal and lateral, from the many devices of one centre
Route in: form; status now: todo
Letter or form: letters/chexpert_plus.md
The owner's hand: the AIMI research use agreement click-through on the owner's AIMI account
Record: datasets/chexpert_plus.json (reach gated, licence: Stanford AIMI research use agreement, non-commercial)
Files likely touched: datasets/chexpert_plus.json, letters/chexpert_plus.md
Priority: group 2, a form, a gate or an account; position 7 of 86

## Obtain TVGH-SpineXR

What it is: a Taiwanese spine radiograph set behind a login
Link: https://ieee-dataport.org/documents/tvgh-spinexr
Why it matters: T1 to L5 per-vertebra labels, masks and end-plates on Taiwanese spine radiographs: level truth on a new device and population
Route in: account; status now: todo
Letter or form: letters/tvgh_spinexr.md
The owner's hand: the IEEE DataPort account, any licence checkbox and a subscription fee if the record is one
Record: datasets/tvgh_spinexr.json (reach gated, licence: not recorded)
Files likely touched: datasets/tvgh_spinexr.json, letters/tvgh_spinexr.md
Priority: group 2, a form, a gate or an account; position 8 of 86

## Obtain MIMIC-CXR and MIMIC-CXR-JPG (PhysioNet)

What it is: 377,110 chest radiographs of 227,835 studies, 65,379 patients, Beth Israel Deaconess; frontal and lateral views, the lateral share roughly a third (to confirm from the metadata CSV)
Link: https://physionet.org/content/mimic-cxr/2.1.0/
Why it matters: 377,110 chest films, roughly a third lateral: the largest source of thoracic spine laterals, free once credentialed
Route in: agreement; status now: todo
Letter or form: letters/mimic_cxr.md
The owner's hand: the PhysioNet data use agreement click for this dataset (the credential is held); the IRB office is asked whether HPR 2026-330 covers it before any image is read
Record: datasets/mimic_cxr.json (reach gated, licence: PhysioNet credentialed health data licence; to confirm on the page)
Files likely touched: datasets/mimic_cxr.json, letters/mimic_cxr.md
Priority: group 2, a form, a gate or an account; position 9 of 86

## Obtain VinDr-CXR (PhysioNet)

What it is: 18,000 adult frontal chest radiographs from two Vietnamese hospitals with radiologist boxes; the same institutions and devices as VinDr-SpineXR
Link: https://physionet.org/content/vindr-cxr/1.0.0/
Why it matters: 18,000 adult frontal chest films from the same hospitals and devices as VinDr-SpineXR
Route in: agreement; status now: todo
Letter or form: letters/vindr_cxr.md
The owner's hand: the PhysioNet data use agreement click for this dataset; the IRB question as for MIMIC-CXR
Record: datasets/vindr_cxr.json (reach gated, licence: PhysioNet credentialed health data licence; to confirm on the page)
Files likely touched: datasets/vindr_cxr.json, letters/vindr_cxr.md
Priority: group 2, a form, a gate or an account; position 10 of 86

## Obtain VinDr-PCXR (PhysioNet)

What it is: 9,125 pediatric frontal chest radiographs from the VinDr hospitals with radiologist boxes; the only sizeable public pediatric spine-bearing radiograph source found
Link: https://physionet.org/content/vindr-pcxr/1.0.0/
Why it matters: 9,125 pediatric frontal chest films: the only sizeable public pediatric spine-bearing radiograph source
Route in: agreement; status now: todo
Letter or form: letters/vindr_pcxr.md
The owner's hand: the PhysioNet data use agreement click for this dataset; the IRB question as for MIMIC-CXR
Record: datasets/vindr_pcxr.json (reach gated, licence: PhysioNet credentialed health data licence; to confirm on the page)
Files likely touched: datasets/vindr_pcxr.json, letters/vindr_pcxr.md
Priority: group 2, a form, a gate or an account; position 11 of 86

## Obtain Stanford AIMI Merlin abdominal CT

What it is: 25,494 CT of 18,317 patients; a gated anomaly-harvest collection (group B7)
Link: https://stanfordaimi.azurewebsites.net/datasets/60b9c7ff-877b-48ce-96c3-0194c8205c40
Why it matters: 25,494 abdominal CTs of 18,317 patients; ranked above the whole of tier 1 for new transitional spines
Route in: agreement; status now: todo
Letter or form: letters/stanford_aimi_merlin.md
The owner's hand: the AIMI research use agreement click-through; the Azure URL that follows is a credential and goes in a mode-0600 file on the grid
Record: datasets/stanford_aimi_merlin.json (reach gated, licence: a data use agreement (non-commercial))
Files likely touched: datasets/stanford_aimi_merlin.json, letters/stanford_aimi_merlin.md
Priority: group 2, a form, a gate or an account; position 12 of 86

## Obtain Stanford AIMI INSPECT chest CT

What it is: 19,402 patients; a gated anomaly-harvest collection (group B7)
Link: https://stanfordaimi.azurewebsites.net/
Why it matters: about 19,400 CT pulmonary angiography patients: thoracic spines at CT with every scanner of one centre
Route in: agreement; status now: todo
Letter or form: letters/stanford_aimi_inspect.md
The owner's hand: the AIMI research use agreement click-through; the Azure URL that follows is a credential
Record: datasets/stanford_aimi_inspect.json (reach gated, licence: a data use agreement (non-commercial))
Files likely touched: datasets/stanford_aimi_inspect.json, letters/stanford_aimi_inspect.md
Priority: group 2, a form, a gate or an account; position 13 of 86

## Obtain DysphagiaBank (TalkBank), UNM corpus

What it is: lateral swallow videofluoroscopy of about 7 to 53 adults, cervical only, non-commercial, by registration
Link: https://dysphagia.talkbank.org/
Why it matters: videofluoroscopic swallow studies with the cervical spine in every frame; non-commercial registration
Route in: account; status now: todo
Letter or form: the registration page at https://dysphagia.talkbank.org/
The owner's hand: the registration on dysphagia.talkbank.org, in the owner's name; the count on the corpus page is checked when registering
Record: datasets/dysphagiabank.json (reach get, licence: non-commercial, by registration)
Files likely touched: datasets/dysphagiabank.json, letters/dysphagiabank.md
Priority: group 2, a form, a gate or an account; position 14 of 86

## Obtain IRI-VFI: pediatric interventional radiology image sequences (Chongqing)

What it is: 95,308 real fluoroscopy images in 1,357 sequences with the lumbar spine in field; pediatric, DSA subtraction frames to be excluded
Link: https://ieee-dataport.org/documents/iri-vfi-dataset
Why it matters: 1,357 pediatric interventional sequences, 95,308 images: a grain calibration target and an unlabelled pool
Route in: account; status now: todo
Letter or form: the record at https://doi.org/10.21227/v4kg-zp42
The owner's hand: the IEEE DataPort account and the licence line, read on the page
Record: datasets/pediatric_iri.json (reach get, licence: not recorded)
Files likely touched: datasets/pediatric_iri.json, letters/pediatric_iri.md
Priority: group 2, a form, a gate or an account; position 15 of 86

## Obtain Veterinary: pig CBCT, CT and planar images (Goswami 2020, LevelCheck)

What it is: the LevelCheck pig study's seven zips of CBCT, CT and planar images, about 205 MB, with the paper (IEEE Access 2020), 3D-to-2D intensity-based registration
Link: https://ieee-dataport.org/open-access/pig-data-2d-3d-intensity-based-registration
Why it matters: the owner's veterinary direction: pig CBCT, CT and planar images on IEEE DataPort, open access
Route in: account; status now: todo
Letter or form: the record on IEEE DataPort named in the dataset record
The owner's hand: the IEEE DataPort account; nothing to sign
Record: datasets/veterinary_pig_levelcheck.json (reach get, licence: IEEE DataPort open access)
Files likely touched: datasets/veterinary_pig_levelcheck.json, letters/veterinary_pig_levelcheck.md
Priority: group 2, a form, a gate or an account; position 16 of 86

## Obtain Kaggle scoliosis YOLOv5 annotated spine X-ray set (salmankey)

What it is: AP spine films with YOLO boxes on vertebrae and curve regions; count, source and whether the people are AASCE's to confirm on the page
Link: https://www.kaggle.com/datasets/salmankey/scoliosis-yolov5-annotated-spine-x-ray-dataset
Why it matters: AP spine films with boxes per vertebra, if the people are new; worthless if it is AASCE re-exported
Route in: account; status now: todo
Letter or form: the Kaggle page named in the dataset record
The owner's hand: the Kaggle account and the licence on the page; every image is hash-checked against the AASCE copy on the grid before any use
Record: datasets/kaggle_scoliosis_yolov5.json (reach get, licence: Kaggle; the licence on the page, to confirm)
Files likely touched: datasets/kaggle_scoliosis_yolov5.json, letters/kaggle_scoliosis_yolov5.md
Priority: group 2, a form, a gate or an account; position 17 of 86

## Obtain Kaggle bone fracture multi-region X-ray data (bmadushanirodrigo)

What it is: 10,580 radiographs in fractured and non-fractured folders over lower limbs, upper limbs, lumbar spine, hips and knees; 481 MB
Link: https://www.kaggle.com/datasets/bmadushanirodrigo/fracture-multi-region-x-ray-data
Why it matters: a lumbar-spine folder and a hip folder from unknown devices: an exposure-diversity pool only
Route in: account; status now: todo
Letter or form: the Kaggle page named in the dataset record
The owner's hand: the Kaggle account; not fetched until the images' origin is shown redistributable
Record: datasets/kaggle_fracture_multiregion.json (reach get, licence: Kaggle; the licence and the images' origin to confirm on the page)
Files likely touched: datasets/kaggle_fracture_multiregion.json, letters/kaggle_fracture_multiregion.md
Priority: group 2, a form, a gate or an account; position 18 of 86

## Obtain Aariz cephalometric benchmark (Khalid, Fraz 2023) and the ISBI 2015 cephalograms

What it is: 1,000 lateral cephalograms from 7 devices with 29 landmarks and a cervical vertebral maturation (CVM) stage per film, C2 to C4 in every image (arXiv:2302.07797; the CEPHA29 challenge at ISBI 2023); the ISBI 2015 set of 400 cephalograms with 19 landmarks and no CVM stage is openly downloadable
Link: https://doi.org/10.6084/m9.figshare.27986417
Why it matters: 1,000 lateral cephalograms from 7 devices with a CVM stage per film: pediatric C2 to C4 anchors
Route in: download; status now: todo
Letter or form: letters/aariz_cephalograms.md (not needed while the download works)
The owner's hand: nothing: the figshare record is CC BY 4.0; the letter in letters/aariz_cephalograms.md is kept only in case the download fails
Record: datasets/aariz_cephalograms.json (reach get, licence: CC BY 4.0 (the figshare record's licence field, read from the API on 2026-10-21))
Files likely touched: datasets/aariz_cephalograms.json, letters/aariz_cephalograms.md
Priority: group 3, a plain download as a grid job; position 19 of 86

## Obtain KUB-StoneX (Daffodil International University HIRL)

What it is: 2,570 AP kidney-ureter-bladder radiographs of 1,703 patients from two Bangladeshi hospitals, with pixel-level stone masks and radiomic features; a KUB film is a frontal lumbar spine and pelvis radiograph at abdominal exposure, with the iliac crests and the sacrum in field
Link: https://doi.org/10.6084/m9.figshare.32049369
Why it matters: 2,570 AP kidney-ureter-bladder films: frontal lumbar spine and pelvis at abdominal exposure, in volume
Route in: download; status now: todo
Letter or form: letters/kub_stonex.md (not needed while the download works)
The owner's hand: nothing: the figshare record is CC BY 4.0; the form text in letters/kub_stonex.md is kept only in case the page asks for one
Record: datasets/kub_stonex.json (reach get, licence: CC BY 4.0 (the figshare record's licence field, read from the API on 2026-10-21))
Files likely touched: datasets/kub_stonex.json, letters/kub_stonex.md
Priority: group 3, a plain download as a grid job; position 20 of 86

## Obtain LUMOS (Zhejiang University)

What it is: 803 living patients: 1,620 lumbar AP or lateral radiographs and 280 non-contrast lumbar CTs, anonymised DICOM and NPY; diagnostic radiography, not C-arm fluoroscopy; no pose given
Link: https://zenodo.org/records/18173664
Why it matters: an open Zenodo record of CT and 1,620 radiographs from Zhejiang University
Route in: download; status now: todo
Letter or form: the Zenodo record named in the dataset record
The owner's hand: the licence line read on the page; then nothing
Record: datasets/lumos.json (reach get, licence: not recorded on the card; to confirm on the record)
Files likely touched: datasets/lumos.json, letters/lumos.md
Priority: group 3, a plain download as a grid job; position 21 of 86

## Obtain VertXNet extra labels for NHANES II (Mo, Papiez, Chen 2023)

What it is: labels only, for films already held: 8 landmarks per vertebral body with vertebral identity on the NHANES II cervical and lumbar laterals, and the reference bodies C2 and S1 annotated by radiologists where visible; the Zenodo record 'NHANES II Spinal X-ray with Extra Labels For Reference Vertebral Bodies (C2, S1)', version 1, 2023, named in the Data availability statement of Scientific Reports 14:3341 (doi:10.1038/s41598-023-49923-3)
Link: https://doi.org/10.1038/s41598-023-49923-3
Why it matters: radiologist labels for C2 and S1 on NHANES II films already held: closes the NHANES level gap at no imaging cost
Route in: download; status now: todo
Letter or form: the Zenodo record named in the dataset record
The owner's hand: nothing; the Zenodo record number is to confirm on the page first
Record: datasets/vertxnet_nhanes2_labels.json (reach get, licence: Zenodo, open; licence to confirm on the page (the held record of the same authors is CC BY 4.0))
Files likely touched: datasets/vertxnet_nhanes2_labels.json, letters/vertxnet_nhanes2_labels.md
Priority: group 3, a plain download as a grid job; position 22 of 86

## Obtain VerSe 2D projections with soft labels (Zenodo 8115942)

What it is: 2D projections of the central slices of VerSe 19 and 20 vertebrae, with soft labels from proposal-based non-expert annotation ('Annotating ambiguous images', 2023); count to confirm on the page (VerSe holds 4,505 vertebrae over 374 scans)
Link: https://zenodo.org/records/8115942
Why it matters: 2D projections of VerSe vertebrae with soft labels: a cheap check of the project's own VerSe renders
Route in: download; status now: todo
Letter or form: https://zenodo.org/records/8115942
The owner's hand: the licence line read on the page
Record: datasets/verse_2d_projections.json (reach get, licence: to confirm on the page (VerSe itself is CC BY-SA 4.0))
Files likely touched: datasets/verse_2d_projections.json, letters/verse_2d_projections.md
Priority: group 3, a plain download as a grid job; position 23 of 86

## Obtain PENGWIN 2024 Task 2 synthetic X-rays

What it is: 50,000 DeepDRR images with 2D fragment masks from 100 pelvic-fracture CTs at 500 random C-arm poses each; projections 0250-0499 add up to 10 simulated K-wires and screws; pelvis, sacrum and the lower lumbar spine are in field; Zenodo doi:10.5281/zenodo.10913195, mirrored at huggingface.co/datasets/MedOtter/PENGWIN_Task2
Link: https://pengwin.grand-challenge.org/
Why it matters: 50,000 simulated C-arm images of pelvic fractures with hardware, from CTs already on the grid
Route in: download; status now: todo
Letter or form: the Zenodo record named in the dataset record
The owner's hand: the licence line read on the page
Record: datasets/pengwin_task2_xrays.json (reach get, licence: CC BY, to confirm on the page; the challenge page lists its terms)
Files likely touched: datasets/pengwin_task2_xrays.json, letters/pengwin_task2_xrays.md
Priority: group 3, a plain download as a grid job; position 24 of 86

## Obtain Fraiwan spine X-ray set (Mendeley xkt857dsxk)

What it is: 338 subjects' spine radiographs from King Abdullah University Hospital, Jordan, in three classes (scoliosis, spondylolisthesis, normal), original and resized (Fraiwan et al. 2022); views to confirm on the page
Link: https://data.mendeley.com/datasets/xkt857dsxk
Why it matters: 338 subjects' spine films from Jordan with spondylolisthesis cases: new people from a new centre
Route in: download; status now: todo
Letter or form: https://data.mendeley.com/datasets/xkt857dsxk
The owner's hand: the licence line read on the Mendeley page
Record: datasets/fraiwan_spine_xray.json (reach get, licence: CC BY 4.0 (Mendeley's default; to confirm on the page))
Files likely touched: datasets/fraiwan_spine_xray.json, letters/fraiwan_spine_xray.md
Priority: group 3, a plain download as a grid job; position 25 of 86

## Obtain Veterinary: canine lateral thoracic radiographs for vertebral heart size (Mendeley ktx4cj55pn)

What it is: 152 anonymised lateral thoracic radiographs of dogs; a lateral dog thorax shows T1 to L1 and the VHS method itself counts vertebrae from T4
Link: https://data.mendeley.com/datasets/ktx4cj55pn
Why it matters: 152 lateral canine thoracic radiographs: the first veterinary spine film set, for the owner's veterinary direction
Route in: download; status now: todo
Letter or form: https://data.mendeley.com/datasets/ktx4cj55pn
The owner's hand: the licence line read on the Mendeley page
Record: datasets/canine_thoracic_vhs.json (reach get, licence: CC BY 4.0 (to confirm on the page))
Files likely touched: datasets/canine_thoracic_vhs.json, letters/canine_thoracic_vhs.md
Priority: group 3, a plain download as a grid job; position 26 of 86

## Obtain Mendeley DDH hip sets (jf3pv98m9g and 4gvcb6gmh2)

What it is: infant and child AP pelvis radiographs with developmental dysplasia labels: jf3pv98m9g (Jordan, 354 subjects) and 4gvcb6gmh2 (AV-DDH, 2,417 infant hip films, updated 2026-03); the lumbosacral junction in field at low exposure
Link: https://data.mendeley.com/datasets/jf3pv98m9g
Why it matters: infant and child AP pelvis films: the only sizeable pediatric pelvic film source found
Route in: download; status now: todo
Letter or form: the two Mendeley records named in the dataset record
The owner's hand: the licence lines read on the two Mendeley pages
Record: datasets/mendeley_ddh_hips.json (reach get, licence: CC BY 4.0 (to confirm on the page))
Files likely touched: datasets/mendeley_ddh_hips.json, letters/mendeley_ddh_hips.md
Priority: group 3, a plain download as a grid job; position 27 of 86

## Obtain IPCAI 2025 paired X-ray and CT set (Zenodo 15753063)

What it is: real calibrated X-ray images with 5 CT scans, 6.7 GB, from 'Automatic multi-view X-ray/CT registration using bone substructure contours'; the anatomy, pelvis or spine, to confirm on the page
Link: https://zenodo.org/records/15753063
Why it matters: real calibrated X-rays with 5 CTs, 6.7 GB; if spine or pelvis, one more real C-arm set with a registered CT
Route in: download; status now: todo
Letter or form: https://zenodo.org/records/15753063
The owner's hand: the licence line and the anatomy read on the page
Record: datasets/ipcai2025_xray_ct.json (reach get, licence: to confirm on the page)
Files likely touched: datasets/ipcai2025_xray_ct.json, letters/ipcai2025_xray_ct.md
Priority: group 3, a plain download as a grid job; position 28 of 86

## Obtain Open-i Indiana chest collection

What it is: 7,470 chest radiographs of 3,955 studies with reports, frontal and lateral pairs (the Indiana University collection on Open-i)
Link: https://openi.nlm.nih.gov/faq
Why it matters: 7,470 chest films in frontal and lateral pairs, open: a quick thoracic-lateral probe
Route in: download; status now: todo
Letter or form: https://openi.nlm.nih.gov/faq
The owner's hand: nothing
Record: datasets/open_i_chest.json (reach get, licence: open, no agreement (the Open-i FAQ); to confirm on the page)
Files likely touched: datasets/open_i_chest.json, letters/open_i_chest.md
Priority: group 3, a plain download as a grid job; position 29 of 86

## Obtain FracAtlas (Abedeen 2023, Scientific Data)

What it is: 4,083 musculoskeletal radiographs from three Bangladeshi hospitals (hand, leg, hip, shoulder), 717 with 922 fracture instances, boxes and masks; the hip and pelvis films show the sacrum and L5
Link: https://figshare.com/articles/dataset/The_dataset/22363012
Why it matters: 4,083 musculoskeletal films from Bangladesh, CC BY 4.0; hip films show the sacrum and L5
Route in: download; status now: todo
Letter or form: the figshare record named in the dataset record
The owner's hand: nothing
Record: datasets/fracatlas.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/fracatlas.json, letters/fracatlas.md
Priority: group 3, a plain download as a grid job; position 30 of 86

## Obtain NIH ChestX-ray14 and the RSNA pneumonia subset

What it is: 112,120 frontal chest films of 30,805 patients; the RSNA pneumonia detection challenge on Kaggle used 30,000 of them
Link: https://nihcc.app.box.com/v/ChestXray-NIHCC
Why it matters: 112,120 frontal chest films, open: the frontal thoracic spine at chest exposure in volume
Route in: download; status now: todo
Letter or form: https://nihcc.app.box.com/v/ChestXray-NIHCC
The owner's hand: the twelve Box URLs and md5s copied from the NIH page into the fetch entry; the RSNA subset needs a Kaggle account
Record: datasets/nih_chestxray14.json (reach get, licence: open (NIH); Kaggle competition rules for the RSNA subset)
Files likely touched: datasets/nih_chestxray14.json, letters/nih_chestxray14.md
Priority: group 3, a plain download as a grid job; position 31 of 86

## Obtain Coronary angiography sets (CADICA, ARCADE, XCAD, AngioCAD)

What it is: real fluoroscopy video with the thoracic spine in the background: CADICA 42 patients DICOM at 10 fps, ARCADE 3,000 images, XCAD 1,747 images, AngioCAD 413 patients; heavy contrast, LAO/RAO rotation
Link: https://github.com/AISIGSJTU/SSVS
Why it matters: the only large real thoracic fluoroscopy without an agreement (CADICA, ARCADE, XCAD, AngioCAD)
Route in: download; status now: todo
Letter or form: the four links named in the dataset record
The owner's hand: each set's own licence read before fetching
Record: datasets/coronary_angiography.json (reach get, licence: varies by set)
Files likely touched: datasets/coronary_angiography.json, letters/coronary_angiography.md
Priority: group 3, a plain download as a grid job; position 32 of 86

## Obtain CathAction (Jianu et al. 2024, AIRVLab)

What it is: about 500,000 fluoroscopy frames (600,000 in the 2026 revision) of endovascular catheterisation, animal and phantom, with action labels, collision labels and 25,000 to 40,000 catheter and guidewire masks; two zips, 4.35 GB and 9.88 GB
Link: https://huggingface.co/datasets/airvlab/CathAction
Why it matters: about 500,000 real fluoroscopy frames from clinical C-arms with live instruments: an exposure and device pool
Route in: download; status now: todo
Letter or form: https://huggingface.co/datasets/airvlab/CathAction
The owner's hand: the licence line read on the Hugging Face page
Record: datasets/cathaction.json (reach get, licence: to confirm on the page)
Files likely touched: datasets/cathaction.json, letters/cathaction.md
Priority: group 3, a plain download as a grid job; position 33 of 86

## Obtain Guide3D (ACCV 2024, AIRVLab)

What it is: more than 8,700 bi-planar fluoroscopic frames of guidewires in a vascular phantom, two guidewires, varied flow
Link: https://airvlab.github.io/guide3d/
Why it matters: 8,700 bi-planar fluoroscopic frames of a vascular phantom: real bi-planar geometry from one device
Route in: download; status now: todo
Letter or form: https://airvlab.github.io/guide3d/
The owner's hand: the licence line read on the page
Record: datasets/guide3d.json (reach get, licence: to confirm on the page)
Files likely touched: datasets/guide3d.json, letters/guide3d.md
Priority: group 3, a plain download as a grid job; position 34 of 86

## Obtain Veriserum (ETH Zurich, MICCAI 2025)

What it is: about 110,000 dual-plane fluoroscopic images of knee implant phantoms with registered poses, 200 with manual registration (ETH Research Collection doi:10.3929/ethz-b-000701146)
Link: https://movement.ethz.ch/data-repository/veriserum.html
Why it matters: 110,000 dual-plane fluoroscopic images of knee implant phantoms: real hardware under real exposure at scale
Route in: download; status now: todo
Letter or form: the ETH Research Collection record named in the dataset record
The owner's hand: the licence line read on the page
Record: datasets/veriserum.json (reach get, licence: to confirm on the page)
Files likely touched: datasets/veriserum.json, letters/veriserum.md
Priority: group 3, a plain download as a grid job; position 35 of 86

## Obtain VFSS2022 videofluoroscopic swallow frames (TIB)

What it is: 440 videofluoroscopic swallow frames with instance masks of the bolus and pharynx, the cervical spine in every frame (doi:10.57702/w1ye2nim; Video-TransUNet)
Link: https://service.tib.eu/ldmservice/dataset/vfss2022-dataset
Why it matters: 440 videofluoroscopic swallow frames with masks, the cervical spine in every frame
Route in: download; status now: todo
Letter or form: https://service.tib.eu/ldmservice/dataset/vfss2022-dataset
The owner's hand: the licence line and the download link read on the page (the fetch entry has none yet)
Record: datasets/vfss2022.json (reach get, licence: to confirm on the page)
Files likely touched: datasets/vfss2022.json, letters/vfss2022.md
Priority: group 3, a plain download as a grid job; position 36 of 86

## Obtain Neurosurgical Focus: Video (every article CC BY 4.0)

What it is: a library of spine-surgery videos PMC serves as MP4; the one checked (PMC13418632, 200 MB, 8 min) shows saved C-arm stills under a tracking overlay, not cine; the rest unscreened
Link: https://thejns.org/page/72659
Why it matters: surgical videos under CC BY 4.0 with live fluoroscopy to screen for
Route in: download; status now: todo
Letter or form: the PMC pages named in the dataset record
The owner's hand: a browser download from PMC, since a proof-of-work gate stops scripts; the publisher's text-and-data-mining footer is a lawyer question
Record: datasets/neurosurgical_focus_video.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/neurosurgical_focus_video.json, letters/neurosurgical_focus_video.md
Priority: group 3, a plain download as a grid job; position 37 of 86

## Obtain STOIC2021 public release (AWS Open Data)

What it is: the public STOIC2021 release of 2,000 chest CT as MHA on AWS Open Data (s3://stoic2021-training; LICENCE.txt read 2026-09-23), about 240 GB; also inside CADS (gated) and re-packed as AUC23 'Lung CT COVID-19'
Link: s3://stoic2021-training
Why it matters: 240 GB of chest CT on AWS Open Data, planned in the data platform
Route in: download; status now: todo
Letter or form: the AWS bucket named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/aws_stoic2021.json (reach get, licence: CC BY-NC 4.0)
Files likely touched: datasets/aws_stoic2021.json, letters/aws_stoic2021.md
Priority: group 3, a plain download as a grid job; position 38 of 86

## Obtain IDC `cptac_lscc` (tier 2)

What it is: IDC v24 collection cptac_lscc (TCIA doi:10.7937/k9/tcia.2018.6emub5l2), tier 2 of the anomaly harvest: 32 subjects, about 8.3 GB raw plus screen; chest, abdomen, pelvis and whole body
Link: https://doi.org/10.7937/k9/tcia.2018.6emub5l2
Why it matters: an IDC tier-2 CT collection planned in the data platform
Route in: download; status now: todo
Letter or form: the IDC collection named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/idc_cptac_lscc.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/idc_cptac_lscc.json, letters/idc_cptac_lscc.md
Priority: group 3, a plain download as a grid job; position 39 of 86

## Obtain IDC `cptac_luad` (tier 2)

What it is: IDC v24 collection cptac_luad (TCIA doi:10.7937/k9/tcia.2018.pat12tbs), tier 2 of the anomaly harvest: 32 subjects, about 7 GB raw plus screen; chest, abdomen and whole body
Link: https://doi.org/10.7937/k9/tcia.2018.pat12tbs
Why it matters: an IDC tier-2 CT collection planned in the data platform
Route in: download; status now: todo
Letter or form: the IDC collection named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/idc_cptac_luad.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/idc_cptac_luad.json, letters/idc_cptac_luad.md
Priority: group 3, a plain download as a grid job; position 40 of 86

## Obtain IDC `ldct_and_projection_data` (tier 2)

What it is: IDC v24 collection ldct_and_projection_data (TCIA doi:10.7937/9npb-2637), tier 2 of the anomaly harvest: 99 subjects, about 16.5 GB raw plus screen; chest
Link: https://doi.org/10.7937/9npb-2637
Why it matters: an IDC tier-2 CT collection planned in the data platform
Route in: download; status now: todo
Letter or form: the IDC collection named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/idc_ldct_and_projection_data.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/idc_ldct_and_projection_data.json, letters/idc_ldct_and_projection_data.md
Priority: group 3, a plain download as a grid job; position 41 of 86

## Obtain IDC `lidc_idri` (tier 2)

What it is: IDC v24 collection lidc_idri (TCIA doi:10.7937/k9/tcia.2015.lo9ql9sx), tier 2 of the anomaly harvest: 997 subjects, about 123.3 GB raw plus screen; chest, abdomen and pelvis
Link: https://doi.org/10.7937/k9/tcia.2015.lo9ql9sx
Why it matters: an IDC tier-2 CT collection of 123 GB planned in the data platform
Route in: download; status now: todo
Letter or form: the IDC collection named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/idc_lidc_idri.json (reach get, licence: CC BY 3.0)
Files likely touched: datasets/idc_lidc_idri.json, letters/idc_lidc_idri.md
Priority: group 3, a plain download as a grid job; position 42 of 86

## Obtain IDC `midrc_ricord_1b` (tier 2)

What it is: IDC v24 collection midrc_ricord_1b (TCIA doi:10.7937/31v8-4a40), tier 2 of the anomaly harvest: 91 subjects, about 7 GB raw plus screen; chest, abdomen and pelvis
Link: https://doi.org/10.7937/31v8-4a40
Why it matters: an IDC tier-2 CT collection planned in the data platform
Route in: download; status now: todo
Letter or form: the IDC collection named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/idc_midrc_ricord_1b.json (reach get, licence: CC BY-NC 4.0)
Files likely touched: datasets/idc_midrc_ricord_1b.json, letters/idc_midrc_ricord_1b.md
Priority: group 3, a plain download as a grid job; position 43 of 86

## Obtain IDC `nsclc_radiogenomics` (tier 2)

What it is: IDC v24 collection nsclc_radiogenomics (TCIA doi:10.7937/k9/tcia.2017.7hs46erv), tier 2 of the anomaly harvest: 188 subjects, about 28 GB raw plus screen; chest, abdomen, pelvis and whole body
Link: https://doi.org/10.7937/k9/tcia.2017.7hs46erv
Why it matters: an IDC tier-2 CT collection planned in the data platform
Route in: download; status now: todo
Letter or form: the IDC collection named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/idc_nsclc_radiogenomics.json (reach get, licence: CC BY 3.0)
Files likely touched: datasets/idc_nsclc_radiogenomics.json, letters/idc_nsclc_radiogenomics.md
Priority: group 3, a plain download as a grid job; position 44 of 86

## Obtain IDC `nsclc_radiomics` (tier 2)

What it is: IDC v24 collection nsclc_radiomics (TCIA doi:10.7937/k9/tcia.2015.pf0m9rei), tier 2 of the anomaly harvest: 415 subjects, about 25.8 GB raw plus screen; chest
Link: https://doi.org/10.7937/k9/tcia.2015.pf0m9rei
Why it matters: an IDC tier-2 CT collection planned in the data platform
Route in: download; status now: todo
Letter or form: the IDC collection named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/idc_nsclc_radiomics.json (reach get, licence: CC BY-NC 3.0)
Files likely touched: datasets/idc_nsclc_radiomics.json, letters/idc_nsclc_radiomics.md
Priority: group 3, a plain download as a grid job; position 45 of 86

## Obtain IDC `prostate_anatomical_edge_cases` (tier 2)

What it is: IDC v24 collection prostate_anatomical_edge_cases (TCIA doi:10.7937/qstf-st65), tier 2 of the anomaly harvest: 131 subjects, about 16.6 GB raw plus screen; pelvis
Link: https://doi.org/10.7937/qstf-st65
Why it matters: an IDC tier-2 CT collection planned in the data platform
Route in: download; status now: todo
Letter or form: the IDC collection named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/idc_prostate_anatomical_edge_cases.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/idc_prostate_anatomical_edge_cases.json, letters/idc_prostate_anatomical_edge_cases.md
Priority: group 3, a plain download as a grid job; position 46 of 86

## Obtain IDC `spinal_multiple_myeloma_seg` (tier 2)

What it is: IDC v24 collection spinal_multiple_myeloma_seg (TCIA doi:10.7937/k4qv-hh78), tier 2 of the anomaly harvest: 67 subjects, about 33.8 GB raw plus screen; spine
Link: https://doi.org/10.7937/k4qv-hh78
Why it matters: an IDC spine CT collection planned in the data platform
Route in: download; status now: todo
Letter or form: the IDC collection named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/idc_spinal_multiple_myeloma_seg.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/idc_spinal_multiple_myeloma_seg.json, letters/idc_spinal_multiple_myeloma_seg.md
Priority: group 3, a plain download as a grid job; position 47 of 86

## Obtain IDC `spine_mets_ct_seg` (tier 2)

What it is: IDC v24 collection spine_mets_ct_seg (TCIA doi:10.7937/kh36-ds04), tier 2 of the anomaly harvest: 54 subjects, about 17.2 GB raw plus screen; spine, abdomen and pelvis
Link: https://doi.org/10.7937/kh36-ds04
Why it matters: an IDC spine CT collection planned in the data platform
Route in: download; status now: todo
Letter or form: the IDC collection named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/idc_spine_mets_ct_seg.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/idc_spine_mets_ct_seg.json, letters/idc_spine_mets_ct_seg.md
Priority: group 3, a plain download as a grid job; position 48 of 86

## Obtain LumVBCanSeg lumbar CT (185, ShengJing Hospital)

What it is: LumVBCanSeg lumbar CT, 185 subjects, ShengJing Hospital, Zenodo 8181250 published 2023-07-25, about 10.1 GB
Link: https://zenodo.org/records/8181250
Why it matters: 185 lumbar CTs from ShengJing Hospital, open on Zenodo
Route in: download; status now: todo
Letter or form: the Zenodo record named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/zenodo_lumvbcanseg.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/zenodo_lumvbcanseg.json, letters/zenodo_lumvbcanseg.md
Priority: group 3, a plain download as a grid job; position 49 of 86

## Obtain MedPelvis3D pelvic CT (99, PLA General Hospital)

What it is: MedPelvis3D pelvic CT, 99 subjects, PLA General Hospital, Zenodo 21757686 published 2026-08-02, about 15.1 GB
Link: https://zenodo.org/records/21757686
Why it matters: 99 pelvic CTs from PLA General Hospital, open on Zenodo
Route in: download; status now: todo
Letter or form: the Zenodo record named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/zenodo_medpelvis3d.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/zenodo_medpelvis3d.json, letters/zenodo_medpelvis3d.md
Priority: group 3, a plain download as a grid job; position 50 of 86

## Obtain International TMTV Benchmark, lymphoma FDG PET/CT (60)

What it is: International TMTV Benchmark, lymphoma FDG PET/CT, 60 subjects, Zenodo 13255214 published 2024-08-07, about 6.9 GB; the NIfTI CTs on the PET grid are over 3 mm, so the DICOM is wanted
Link: https://zenodo.org/records/13255214
Why it matters: 60 lymphoma FDG PET/CT studies, open on Zenodo; needs a zipped-DICOM convert route
Route in: download; status now: todo
Letter or form: the Zenodo record named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/zenodo_tmtv_benchmark.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/zenodo_tmtv_benchmark.json, letters/zenodo_tmtv_benchmark.md
Priority: group 3, a plain download as a grid job; position 51 of 86

## Obtain UniToChest chest CT (623 patients; distributed as slices)

What it is: UniToChest chest CT, 623 patients, distributed as slices, Zenodo 5797912 published 2021-12-22, about 84 GB
Link: https://zenodo.org/records/5797912
Why it matters: 623 patients' chest CT distributed as slices, open on Zenodo
Route in: download; status now: todo
Letter or form: the Zenodo record named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/zenodo_unitochest.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/zenodo_unitochest.json, letters/zenodo_unitochest.md
Priority: group 3, a plain download as a grid job; position 52 of 86

## Obtain VSDFullBody: post-mortem whole-body CT, forensic institutes Bern and Zurich

What it is: VSDFullBody post-mortem whole-body CT, 100 subjects, forensic institutes Bern and Zurich, Zenodo 8270365 published 2013-11-12, about 116 GB; the mirror notes duplicate CT datasets (100 new of 109 files)
Link: https://zenodo.org/records/8270365
Why it matters: post-mortem whole-body CT from forensic institutes, 116 GB, open on Zenodo
Route in: download; status now: todo
Letter or form: the Zenodo record named in the dataset record
The owner's hand: nothing; a grid job on the owner's word
Record: datasets/zenodo_vsd_fullbody.json (reach get, licence: CC BY-NC-SA per the record's text (the record's licence field is empty))
Files likely touched: datasets/zenodo_vsd_fullbody.json, letters/zenodo_vsd_fullbody.md
Priority: group 3, a plain download as a grid job; position 53 of 86

## Obtain LevelCheck clinical cohort (Johns Hopkins, Siewerdsen group)

What it is: 178 patients with preoperative CT and 398 intraoperative radiographs (De Silva et al., Spine 2016), plus Ketcha et al. 2017's 24 thoracolumbar patients with 61 Carestream DRX-1 radiographs, and the 62-image reader set of Manbachi et al. 2018; neither paper has a data statement
Link: no link in the record; see the record's how_to_get
Why it matters: 178 CTs and 398 intraoperative radiographs with the level of each vertebra known from the registered CT: the only collection of that kind and size
Route in: letter; status now: requested; Letter sent 2026-10-21 09:46 UTC by the owner to the LevelCheck authors; waiting for the answer.
Letter or form: letters/levelcheck_jhu.md
The owner's hand: the data use agreement with Johns Hopkins or MD Anderson, if one is offered
Record: datasets/levelcheck_jhu.json (reach get, licence: not recorded; a data use agreement with the PI is the route)
Files likely touched: datasets/levelcheck_jhu.json, letters/levelcheck_jhu.md
Priority: group 4, sent, waiting for the answer; position 54 of 86

## Obtain Huashan Hospital, Fudan University, intraoperative lumbar films with preoperative CT (Shao et al. 2024)

What it is: 140 living lumbar patients (January 2020 to December 2023) with preoperative CT and intraoperative AP and lateral films of L1 to L5; the device is unnamed; two co-authors are from Shanghai Maestro Surgical Robotics; no data statement
Link: no link in the record; see the record's how_to_get
Why it matters: 140 lumbar patients with preoperative CT and intraoperative AP and lateral films: the largest series of its kind found
Route in: letter; status now: requested; Letter sent 2026-10-21 09:46 UTC by the owner to the corresponding author; waiting for the answer.
Letter or form: letters/huashan_fudan.md
The owner's hand: the data use agreement, if one is offered
Record: datasets/huashan_fudan.json (reach get, licence: not recorded; a data use agreement is the route)
Files likely touched: datasets/huashan_fudan.json, letters/huashan_fudan.md
Priority: group 4, sent, waiting for the answer; position 55 of 86

## Obtain SX-Stitch intraoperative C-arm series (Li 2024, PUMCH)

What it is: intraoperative C-arm series translated along the spine for stitching
Link: https://arxiv.org/abs/2409.05681
Why it matters: 1,032 intraoperative C-arm images in overlapping series with vertebra masks: the only such collection published
Route in: letter; status now: requested; Letter sent 2026-10-21 09:46 UTC by the owner; waiting for the answer (the paper's data statement makes success unlikely).
Letter or form: letters/sx_stitch.md
The owner's hand: the data use agreement, if one is offered
Record: datasets/sx_stitch.json (reach get, licence: not recorded)
Files likely touched: datasets/sx_stitch.json, letters/sx_stitch.md
Priority: group 4, sent, waiting for the answer; position 56 of 86

## Obtain PUMCH stitching series (Liu et al., Eur Spine J 2026)

What it is: 43 scoliosis patients, four to six overlapping prone AP exposures each on a Philips Zenition 70; the shift between shots estimated, not recorded; no labels stated; the paper says no datasets were generated or analysed
Link: no link in the record; see the record's how_to_get
Why it matters: 43 scoliosis patients with four to six overlapping prone exposures each: one of two such collections anywhere
Route in: letter; status now: requested; Letter sent 2026-10-21 09:46 UTC by the owner; waiting for the answer.
Letter or form: letters/pumch_stitching.md
The owner's hand: the data use agreement, if one is offered
Record: datasets/pumch_stitching.json (reach get, licence: not recorded; a data use agreement is the route)
Files likely touched: datasets/pumch_stitching.json, letters/pumch_stitching.md
Priority: group 4, sent, waiting for the answer; position 57 of 86

## Obtain NIT Warangal and NIMS Hyderabad intraoperative C-arm sets (2D-3D-sci-registration)

What it is: nine living patients and 51 AP and lateral C-arm sets in the repository's README (at most 49 unique frames), a Ziehm C-arm, preoperative CT with level-named L1 to L5 centroids; the 60 centroid files and 54 overlay PNGs (the real frame at 8 bits beside a simulated projection) are public on the repository, the CT and raw X-rays available upon reasonable request
Link: no link in the record; see the record's how_to_get
Why it matters: nine patients' AP and lateral C-arm sets on a Ziehm C-arm with level-named L1 to L5 centroids from CT
Route in: letter; status now: requested; Letter sent 2026-10-21 09:46 UTC by the owner; waiting for the answer.
Letter or form: letters/nit_warangal_nims.md
The owner's hand: whatever agreement the authors ask for
Record: datasets/nit_warangal_nims.json (reach get, licence: not recorded; the raw frames and CTs are available upon reasonable request)
Files likely touched: datasets/nit_warangal_nims.json, letters/nit_warangal_nims.md
Priority: group 4, sent, waiting for the answer; position 58 of 86

## Obtain Vanderbilt intraoperative THA fluoroscopy (Chan et al., J Arthroplasty 2025)

What it is: 146 living patients, 161 anterior-approach hips, 336 AP frames with eight bony landmarks including midline L5/S1 and both sacroiliac joints, plus 84 cup frames; AP only; the C-arm is not reported; no data statement, code only at github.com/vine-lab-vu/Label-Augmentation (doi:10.1016/j.arth.2025.01.032)
Link: https://doi.org/10.1016/j.arth.2025.01.032
Why it matters: 336 intraoperative pelvic frames with midline L5/S1 and both sacroiliac joints marked: the anchors the lumbar count starts from
Route in: letter; status now: requested; Letter sent 2026-10-21 12:30 UTC by the owner to the senior authors; waiting for the answer.
Letter or form: letters/vanderbilt_tha_fluoro.md
The owner's hand: the data use agreement with Vanderbilt, if one is offered
Record: datasets/vanderbilt_tha_fluoro.json (reach get, licence: not recorded; a data use agreement with Vanderbilt is the route)
Files likely touched: datasets/vanderbilt_tha_fluoro.json, letters/vanderbilt_tha_fluoro.md
Priority: group 4, sent, waiting for the answer; position 59 of 86

## Obtain TotalSegmentator task data 'hip_implant' (71 CT)

What it is: TotalSegmentator task data 'hip_implant', 71 CT, Zenodo 20272031 published 2026-05-18, about 9.0 GB; the same institution as TotalSegmentator v2/v3 (on disk) with no subject map
Link: https://zenodo.org/records/20272031
Why it matters: 71 CTs with hip implants, CC BY 4.0; whether its subjects repeat the held v2 and v3 releases decides whether it adds people
Route in: letter; status now: requested; The overlap question went 2026-10-21 09:46 UTC by the owner to the corresponding author; waiting for the answer. The set itself is CC BY 4.0 and needs only a grid job; until the answer comes it is treated as overlapping v2 and v3 (no new people).
Letter or form: letters/totalsegmentator_tasks.md
The owner's hand: nothing binding; the fetch is a grid job on the owner's word
Record: datasets/zenodo_ts_task_hip_implant.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/zenodo_ts_task_hip_implant.json, letters/zenodo_ts_task_hip_implant.md
Priority: group 4, sent, waiting for the answer; position 60 of 86

## Obtain TotalSegmentator task data 'liver_lesions' (842 CT)

What it is: TotalSegmentator task data 'liver_lesions', 842 CT, Zenodo 20272572 published 2026-05-18, about 38.9 GB; the same institution as TotalSegmentator v2/v3 (on disk) with no subject map
Link: https://zenodo.org/records/20272572
Why it matters: 842 CTs, CC BY 4.0; whether its subjects repeat the held v2 and v3 releases decides whether it adds people
Route in: letter; status now: requested; The overlap question went 2026-10-21 09:46 UTC by the owner to the corresponding author; waiting for the answer. The set itself is CC BY 4.0 and needs only a grid job; until the answer comes it is treated as overlapping v2 and v3 (no new people).
Letter or form: letters/totalsegmentator_tasks.md
The owner's hand: nothing binding; the fetch is a grid job on the owner's word
Record: datasets/zenodo_ts_task_liver_lesions.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/zenodo_ts_task_liver_lesions.json, letters/zenodo_ts_task_liver_lesions.md
Priority: group 4, sent, waiting for the answer; position 61 of 86

## Obtain TotalSegmentator task data 'pleural_pericard_effusion' (600 CT)

What it is: TotalSegmentator task data 'pleural_pericard_effusion', 600 CT, Zenodo 20272295 published 2026-05-18, about 9.0 GB; the same institution as TotalSegmentator v2/v3 (on disk) with no subject map
Link: https://zenodo.org/records/20272295
Why it matters: 600 CTs, CC BY 4.0; whether its subjects repeat the held v2 and v3 releases decides whether it adds people
Route in: letter; status now: requested; The overlap question went 2026-10-21 09:46 UTC by the owner to the corresponding author; waiting for the answer. The set itself is CC BY 4.0 and needs only a grid job; until the answer comes it is treated as overlapping v2 and v3 (no new people).
Letter or form: letters/totalsegmentator_tasks.md
The owner's hand: nothing binding; the fetch is a grid job on the owner's word
Record: datasets/zenodo_ts_task_pleural_effusion.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/zenodo_ts_task_pleural_effusion.json, letters/zenodo_ts_task_pleural_effusion.md
Priority: group 4, sent, waiting for the answer; position 62 of 86

## Obtain Balgrist ex-vivo lumbar CT plus C-arm (Jecklin)

What it is: cadaver lumbar CT with real C-arm frames
Link: https://rocs.balgrist.ch/en/contact
Why it matters: 13 cadaver torsos with CT, real images from three mobile C-arms and the projection geometry: the only ex-vivo set on three C-arms
Route in: letter; status now: requested; Letter of 2026-09-21 sent 2026-10-20 by the owner to Philipp Fuernstahl and rocs@balgrist.ch (the message to Sascha Jecklin bounced); the resend through the ROCS contact form is pending; waiting for the answer.
Letter or form: letters/balgrist_lumbar.md
The owner's hand: the ROCS contact form resend, and the data transfer agreement, which Wayne State's institutional official may countersign
Record: datasets/balgrist_lumbar.json (reach get, licence: not recorded)
Files likely touched: datasets/balgrist_lumbar.json, letters/balgrist_lumbar.md
Priority: group 4, sent, waiting for the answer; position 63 of 86

## Obtain Bournemouth cervical quantitative fluoroscopy (BORDaR 385)

What it is: 252 lateral flexion and extension sequences from 63 people at 15 fps, 1024 x 1024 16-bit DICOM; the deposit holds the per-frame vertebral corner tracks (.mat, 24 MB) and no pixels
Link: https://bordar.bournemouth.ac.uk/385/
Why it matters: the Bournemouth cervical quantitative fluoroscopy cine (BORDaR 385), the DICOM behind tracks already held
Route in: letter; status now: requested; Request 1 of the 2026-09-26 sheet sent 2026-10-20 by the owner and forwarded to ckaching.cheung@polyu.edu.hk on 2026-10-21 03:57 UTC; waiting for the answer. The letter text is spine-program's and is not in this repository.
Letter or form: no letter file here (request 1 of spine-program's 2026-09-26 sheet)
The owner's hand: a UK data-sharing agreement, which Wayne State's institutional official signs
Record: datasets/bournemouth_cervical_qf.json (reach get, licence: CC BY 4.0 (the tracks); README.rtf CC BY-ND)
Files likely touched: datasets/bournemouth_cervical_qf.json, letters/bournemouth_cervical_qf.md
Priority: group 4, sent, waiting for the answer; position 64 of 86

## Obtain Bournemouth lumbar quantitative fluoroscopy (Breen 2021)

What it is: weight-bearing and recumbent L2 to S1 flexion and extension cine of 127 subjects at 15 fps, 60 degrees at 6 degrees a second; only per-frame angles are public on OSF
Link: https://osf.io/a27py/
Why it matters: the only confirmed lumbar cine with per-frame level truth
Route in: letter; status now: requested; Asked for in request 1, sent 2026-10-20 by the owner and forwarded to ckaching.cheung@polyu.edu.hk on 2026-10-21 03:57 UTC; waiting for the answer.
Letter or form: no letter file here (request 1 of spine-program's 2026-09-26 sheet)
The owner's hand: a UK data-sharing agreement, which Wayne State's institutional official signs
Record: datasets/bournemouth_lumbar_qf.json (reach get, licence: not recorded (OSF holds derived tables only))
Files likely touched: datasets/bournemouth_lumbar_qf.json, letters/bournemouth_lumbar_qf.md
Priority: group 4, sent, waiting for the answer; position 65 of 86

## Obtain Maastricht UMC+ cervical flexion-extension cine (van Santbrink 2026)

What it is: 112 lateral cervical recordings at 1024 x 1024, 15 fps, uncompressed, with C0 to C7 contours on every frame carrying identity through the sequence
Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC13024292/
Why it matters: cervical flexion-extension cine, on request only
Route in: letter; status now: requested; Request 2 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer. The SchwingNet record of 2026-10-21 still says drafted, so confirm the date in the owner's Sent folder.
Letter or form: no letter file here (request 2 of spine-program's 2026-09-26 sheet)
The owner's hand: a GDPR data transfer agreement under the Dutch WMO framework
Record: datasets/maastricht_cervical.json (reach get, licence: available on request under privacy restrictions; a Dutch WMO/GDPR data transfer agreement is expected)
Files likely touched: datasets/maastricht_cervical.json, letters/maastricht_cervical.md
Priority: group 4, sent, waiting for the answer; position 66 of 86

## Obtain Inselspital Bern dynamic myelography (Piechowiak 2021)

What it is: four pulsed fluoroscopy runs at 7.5 frames a second, the image receptor moved cranially along the spine during tilting: the only overlapping travelling frames found; the published MP4s are on the grid, the native DICOM is not
Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC8463391/
Why it matters: dynamic myelography DICOM behind videos already held under CC BY
Route in: letter; status now: requested; Request 3 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer. The published videos are already held under CC BY; the request is for the native DICOM.
Letter or form: no letter file here (request 3 of spine-program's 2026-09-26 sheet)
The owner's hand: a Swiss data transfer agreement, perhaps KEK Bern
Record: datasets/bern_myelography.json (reach get, licence: CC BY 4.0 (the article's videos); native DICOM available on reasonable request under Swiss law)
Files likely touched: datasets/bern_myelography.json, letters/bern_myelography.md
Priority: group 4, sent, waiting for the answer; position 67 of 86

## Obtain Pittsburgh videofluoroscopic swallow corpus (Sejdic, Coyle)

What it is: about 1,500 lateral swallow clips at 30 fps captured by video card, 265 patients and 70 volunteers on two machines
Link: https://doi.org/10.1016/j.media.2021.102218
Why it matters: a videofluoroscopic swallow corpus with the cervical spine in every frame
Route in: letter; status now: requested; Request 4 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer.
Letter or form: no letter file here (request 4 of spine-program's 2026-09-26 sheet)
The owner's hand: a University of Pittsburgh data use agreement
Record: datasets/pittsburgh_swallow.json (reach get, licence: by request)
Files likely touched: datasets/pittsburgh_swallow.json, letters/pittsburgh_swallow.md
Priority: group 4, sent, waiting for the answer; position 68 of 86

## Obtain Seattle Science Foundation spine videos

What it is: 12 YouTube surgical teaching videos with live C-arm feeds (spinal cord stimulator trials, kyphoplasty); re-encodes on the grid
Link: https://www.seattlesciencefoundation.org/
Why it matters: 12 spine videos; one request covers all
Route in: letter; status now: requested; Request 5 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer.
Letter or form: no letter file here (request 5 of spine-program's 2026-09-26 sheet)
The owner's hand: permission, and whether the labs were cadaveric
Record: datasets/seattle_science_foundation.json (reach get, licence: unknown; embedding disabled)
Files likely touched: datasets/seattle_science_foundation.json, letters/seattle_science_foundation.md
Priority: group 4, sent, waiting for the answer; position 69 of 86

## Obtain Mayfield Brain and Spine kyphoplasty alignment series

What it is: two native DICOM C-arm alignment series played in OsiriX on YouTube: AP 98 frames, lateral 65 frames; a birth date is burned in
Link: https://www.youtube.com/watch?v=fkRFgkESCgQ
Why it matters: a kyphoplasty alignment series
Route in: letter; status now: requested; Request 6 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer.
Letter or form: no letter file here (request 6 of spine-program's 2026-09-26 sheet)
The owner's hand: HIPAA de-identification on the source's side
Record: datasets/mayfield_kyphoplasty.json (reach get, licence: unknown)
Files likely touched: datasets/mayfield_kyphoplasty.json, letters/mayfield_kyphoplasty.md
Priority: group 4, sent, waiting for the answer; position 70 of 86

## Obtain DMX Imaging digital motion X-ray

What it is: lateral lumbar flexion-extension at 30 frames a second, a commercial practice's YouTube video
Link: https://www.dmxworks.com/
Why it matters: digital motion X-ray sequences from a vendor
Route in: letter; status now: requested; Request 7 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer.
Letter or form: no letter file here (request 7 of spine-program's 2026-09-26 sheet)
The owner's hand: perhaps an NDA
Record: datasets/dmx_imaging.json (reach get, licence: unknown)
Files likely touched: datasets/dmx_imaging.json, letters/dmx_imaging.md
Priority: group 4, sent, waiting for the answer; position 71 of 86

## Obtain The Procedure Guide (Puranik) live fluoroscopy clips

What it is: four YouTube clips of live fluoroscopy under a CC BY-NC-SA 4.0 site licence whose reach to the clips is unstated
Link: https://theprocedureguide.com/contact
Why it matters: live fluoroscopy clips under CC BY-NC-SA, if the licence covers them
Route in: form; status now: requested; Request 9 (a contact form) pasted 2026-10-20 by the owner; waiting for the answer.
Letter or form: no letter file here (request 9 of spine-program's 2026-09-26 sheet)
The owner's hand: whether CC BY-NC-SA covers the clips; the form asks nothing binding
Record: datasets/procedure_guide.json (reach get, licence: CC BY-NC-SA 4.0 (site))
Files likely touched: datasets/procedure_guide.json, letters/procedure_guide.md
Priority: group 4, sent, waiting for the answer; position 72 of 86

## Obtain Konica Minolta dynamic digital radiography sequences

What it is: flat-panel lumbar motion sequences shown in a marketing video; not fluoroscopy, a separate arm
Link: https://healthcare.konicaminolta.us/contact-us
Why it matters: dynamic digital radiography sequences from the vendor
Route in: letter; status now: requested; Request 10 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer.
Letter or form: no letter file here (request 10 of spine-program's 2026-09-26 sheet)
The owner's hand: likely an NDA or a pointer to a clinical site
Record: datasets/konica_ddr.json (reach get, licence: unknown)
Files likely touched: datasets/konica_ddr.json, letters/konica_ddr.md
Priority: group 4, sent, waiting for the answer; position 73 of 86

## Obtain Jefferson Neurosurgery DRG stimulation video (Hines 2020)

What it is: a Neurosurgical Focus Video article with lumbosacral fluoroscopy; the YouTube copy carries a CC BY licence and is on the grid
Link: https://doi.org/10.3171/2020.7.FOCVID2034
Why it matters: a DRG stimulation video usable now under CC BY; the request asks which licence applies
Route in: letter; status now: requested; Request 11 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer. The copy is usable now under CC BY.
Letter or form: no letter file here (request 11 of spine-program's 2026-09-26 sheet)
The owner's hand: nothing binding
Record: datasets/jefferson_drg.json (reach get, licence: CC BY (YouTube copy); the article text says CC BY-NC-ND while linking CC BY 4.0)
Files likely touched: datasets/jefferson_drg.json, letters/jefferson_drg.md
Priority: group 4, sent, waiting for the answer; position 74 of 86

## Obtain Manual Therapy Foundation of India lumbar coupling video

What it is: AP lumbar side-bending with rotation under video fluoroscopy, a view the project lacks
Link: https://www.mtfi.net/
Why it matters: a lumbar coupling video; low value
Route in: letter; status now: requested; Request 12 of the 2026-09-26 sheet sent 2026-10-20 by the owner; waiting for the answer.
Letter or form: no letter file here (request 12 of spine-program's 2026-09-26 sheet)
The owner's hand: nothing binding
Record: datasets/mtfi_lumbar_coupling.json (reach get, licence: unknown)
Files likely touched: datasets/mtfi_lumbar_coupling.json, letters/mtfi_lumbar_coupling.md
Priority: group 4, sent, waiting for the answer; position 75 of 86

## Obtain ThePainSource (Faubel) fluoroscopy clips

What it is: pain-procedure fluoroscopy clips on YouTube; fax or phone only
Link: https://www.faubelmd.com/contact-us
Why it matters: fluoroscopy clips from a pain-medicine site; low value
Route in: letter; status now: requested; Request 13 sent 2026-10-21 04:03 UTC by the owner to thepainsource@gmail.com (fax fallback 815-381-7498, to confirm); waiting for the answer.
Letter or form: no letter file here (request 13 of spine-program's 2026-09-26 sheet)
The owner's hand: nothing binding
Record: datasets/faubel_painsource.json (reach get, licence: unknown)
Files likely touched: datasets/faubel_painsource.json, letters/faubel_painsource.md
Priority: group 4, sent, waiting for the answer; position 76 of 86

## Obtain DARADIA vertebroplasty video (Kolkata)

What it is: a step-by-step percutaneous vertebroplasty under fluoroscopy on YouTube
Link: https://daradia.com/
Why it matters: a vertebroplasty video
Route in: letter; status now: requested; Request 14 of the 2026-09-26 sheet sent 2026-10-20 by the owner to info@daradia.com; waiting for the answer.
Letter or form: no letter file here (request 14 of spine-program's 2026-09-26 sheet)
The owner's hand: consent status on the source's side
Record: datasets/daradia_vertebroplasty.json (reach get, licence: unknown)
Files likely touched: datasets/daradia_vertebroplasty.json, letters/daradia_vertebroplasty.md
Priority: group 4, sent, waiting for the answer; position 77 of 86

## Obtain Radiopaedia spine cases

What it is: every case whose body system is Spine (and musculoskeletal cases whose images show the spine), in every modality, with the reference articles on vertebral numbering and transitional vertebrae; the seven fluoroscopy cases first identified (rID 24796, rID 90103, rID 21585 and four fluoroscopy-guided injection cases) are within it; the count is Radiopaedia's to state at approval
Link: https://radiopaedia.org/licence
Why it matters: the whole Spine system of Radiopaedia cases under its non-commercial licence
Route in: agreement; status now: requested; Licence application signed and submitted 2026-10-21 03:36 UTC by the owner, fee paid (receipt 1967-5247); pending Radiopaedia's countersignature; the full text of two cut-off fields goes to license@radiopaedia.org.
Letter or form: the application at https://radiopaedia.org/licence (already submitted)
The owner's hand: everything: the countersigned copy, the agreement ID, and the follow-up to license@radiopaedia.org; never fetched by script
Record: datasets/radiopaedia.json (reach gated, licence: CC BY-NC-SA 3.0 (the site); ML use by application)
Files likely touched: datasets/radiopaedia.json, letters/radiopaedia.md
Priority: group 4, sent, waiting for the answer; position 78 of 86

## Obtain CT-RATE chest CT

What it is: 25,692 CT of 21,304 patients; a gated anomaly-harvest collection (group B7)
Link: https://huggingface.co/datasets/ibrahimhamamci/CT-RATE
Why it matters: chest CT in volume, granted; 21.3 TB
Route in: agreement; status now: granted; Access granted on the owner's Hugging Face account 2026-10-21; the fetch (21.3 TB) waits for the owner's word on how much Ceph space it may take.
Letter or form: nothing to send
The owner's hand: the Ceph space decision and the word for the job; the token in ~/.hf/token.env on the owner's grid account
Record: datasets/ct_rate.json (reach gated, licence: a data use agreement (non-commercial))
Files likely touched: datasets/ct_rate.json, letters/ct_rate.md
Priority: group 5, the owner's hand only; position 79 of 86

## Obtain CADS CT (unique cases)

What it is: 753 CTs; a gated anomaly-harvest collection (group B7)
Link: https://huggingface.co/datasets/mrmrx/CADS-dataset
Why it matters: CT with CT-TRI and VISCERAL labels, granted
Route in: agreement; status now: granted; Access granted on the owner's Hugging Face account 2026-10-21; not yet fetched.
Letter or form: nothing to send
The owner's hand: the word for the job; the token in ~/.hf/token.env on the owner's grid account
Record: datasets/cads.json (reach gated, licence: a data use agreement (non-commercial))
Files likely touched: datasets/cads.json, letters/cads.md
Priority: group 5, the owner's hand only; position 80 of 86

## Obtain RSNA abdominal trauma CT (RATIC)

What it is: 3,147 patients, 4,711 series; a gated anomaly-harvest collection (group B7)
Link: https://mira.rsna.org/dataset/5
Why it matters: abdominal trauma CT, granted; the link expires 2026-10-28
Route in: agreement; status now: granted; RSNA's terms accepted 2026-10-21; a presigned link valid until 2026-10-28 02:38 UTC is in the owner's ~/.rsna/ratic_link; job id not yet recorded.
Letter or form: nothing to send
The owner's hand: the sbatch from the owner's grid account before the link expires; the job id goes in the record
Record: datasets/rsna_ratic.json (reach gated, licence: a data use agreement (non-commercial))
Files likely touched: datasets/rsna_ratic.json, letters/rsna_ratic.md
Priority: group 5, the owner's hand only; position 81 of 86

## Obtain RSNA pulmonary embolism CT (RSPECT)

What it is: 7,279 patients; a gated anomaly-harvest collection (group B7)
Link: https://www.kaggle.com/competitions/rsna-str-pulmonary-embolism-detection
Why it matters: pulmonary embolism CT, granted through Kaggle
Route in: agreement; status now: granted; The owner joined the competition on Kaggle 2026-10-21; a fresh Kaggle token is needed (the pasted one is revoked); job id not yet recorded.
Letter or form: nothing to send
The owner's hand: a fresh Kaggle token in ~/.fluorocap/credentials.env and the sbatch; the job id goes in the record
Record: datasets/rsna_rspect.json (reach gated, licence: a data use agreement (non-commercial))
Files likely touched: datasets/rsna_rspect.json, letters/rsna_rspect.md
Priority: group 5, the owner's hand only; position 82 of 86

## Obtain AbdomenAtlas 2.0 Mini (10,135 CT)

What it is: AbdomenAtlas 2.0 Mini, 10,135 CT in 21 tars, about 620 GB on Hugging Face (tree read 2026-09-24); no card, no metadata; the AbdomenAtlas line aggregates public sets, 3.0 Mini (9,262) is already fetched and the other about 873 are unidentified
Link: https://huggingface.co/datasets/AbdomenAtlas/AbdomenAtlas2.0Mini
Why it matters: 10,135 CTs, 620 GB; no card and no metadata, so an id map against AbdomenAtlas 3.0 Mini comes first
Route in: owner-only; status now: todo
Letter or form: nothing to send
The owner's hand: the id map decision; then a grid job
Record: datasets/hf_abdomenatlas2_0_mini.json (reach get, licence: CC BY-NC-SA 4.0)
Files likely touched: datasets/hf_abdomenatlas2_0_mini.json, letters/hf_abdomenatlas2_0_mini.md
Priority: group 5, the owner's hand only; position 83 of 86

## Obtain ENHANCE.PET 1.6k: whole-/total-body FDG-PET/CT, 1,683 studies (NIfTI)

What it is: ENHANCE.PET 1.6k, whole- and total-body FDG-PET/CT, 1,683 studies as NIfTI (Science Data Bank doi:10.57760/sciencedb.34150), about 286 GB; multi-centre (Vienna, UC Davis, Careggi, Leipzig, Tuebingen), so Tuebingen may be autoPET and Vienna's healthy controls QUADRA_HC, both tier 1, which the landing dedupe would find; the slice thickness per study is in its CT-details.xlsx, not read
Link: https://doi.org/10.57760/sciencedb.34150
Why it matters: 1,683 whole-body PET/CT studies on Science Data Bank; whether a login is needed is unknown
Route in: owner-only; status now: todo
Letter or form: nothing to send yet
The owner's hand: confirm whether Science Data Bank asks for a login and read CT-details.xlsx; no fetch route exists yet
Record: datasets/scidb_enhance_pet_1_6k.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/scidb_enhance_pet_1_6k.json, letters/scidb_enhance_pet_1_6k.md
Priority: group 5, the owner's hand only; position 84 of 86

## Obtain NLST, full (tier 2; 500-person pilot fetched)

What it is: the National Lung Screening Trial in IDC v24 (TCIA doi:10.7937/tcia.hmq8-j677), full: 24,713 subjects, about 2,305 GB raw plus screen; the 500-person pilot is fetched (the manifest's nlst_pilot, in the harvest)
Link: https://doi.org/10.7937/tcia.hmq8-j677
Why it matters: the full NLST, 2.3 TB for about 110 people of the only yield; refused as it stands by the stopping rule
Route in: owner-only; status now: todo
Letter or form: nothing to send
The owner's hand: lifting the stopping rule; no fetch job until then
Record: datasets/idc_nlst.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/idc_nlst.json, letters/idc_nlst.md
Priority: group 5, the owner's hand only; position 85 of 86

## Obtain COBRA2026 embargoed cases

What it is: the challenge's held-back cases
Link: https://zenodo.org/records/21322350
Why it matters: the embargoed COBRA2026 cases, released on 2032-03-01
Route in: download; status now: todo; Embargoed until 2032-03-01; nothing to do before then.
Letter or form: nothing to send
The owner's hand: nothing until 2032
Record: datasets/cobra_embargoed.json (reach embargoed, licence: CC BY-NC 4.0)
Files likely touched: datasets/cobra_embargoed.json, letters/cobra_embargoed.md
Priority: group 6, waits on time; position 86 of 86

## Obtain TVGH ankylosing spondylitis cervical and lumbar spine films (Taiwan medical data portal, data set d08)

What it is: paired cervical and lumbar spine radiograph series in DICOM from Taipei Veterans General Hospital, in patients with ankylosing spondylitis, listed on the Taiwan medical data portal at data.dmc.nycu.edu.tw (data set d08); the portal shows no files to a visitor
Link: https://data.dmc.nycu.edu.tw/dataset/d08-x-ray
Why it matters: fused and bridged spines, the hardest films for telling one vertebra from the next, from a Taiwanese centre none of the held sets covers
Route in: letter; status now: requested (sent 2026-10-21)
Letter or form: letters/tvgh_as_spine_xray.md, sent to the portal's contacts at Taipei Veterans General Hospital
The owner's hand: any data use agreement the hospital asks for
Record: datasets/tvgh_as_spine_xray.json (reach gated, licence: not recorded)
Files likely touched: datasets/tvgh_as_spine_xray.json, letters/tvgh_as_spine_xray.md
Priority: group 4, a request already sent and waiting for its answer; found by the sweep of 2026-10-21

## Obtain CADICA invasive coronary angiography sequences (Mendeley p9bpx9ctcv)

What it is: invasive coronary angiography videos of 42 patients as PNG frames (512 x 512, 10 frames per second, 1 to 151 frames a video) from a Siemens Artis Zee at Hospital Universitario Virgen de la Victoria, Malaga, with lesion boxes and clinical features; one zip of 3,076,112,179 bytes (version 5)
Link: https://data.mendeley.com/datasets/p9bpx9ctcv
Why it matters: real C-arm fluoroscopy sequences from a modern Siemens system with their exposure range stated: a device and dose arm outside the spine
Route in: download; status now: fetching (manifest ready; the promoter fetches after merge)
Letter or form: nothing to send; the licence is CC BY 4.0 on the Mendeley page
The owner's hand: nothing
Record: datasets/cadica.json (reach get, licence: CC BY 4.0)
Files likely touched: datasets/cadica.json, manifests/cadica.json
Priority: group 3, a plain download as a grid job; found by the sweep of 2026-10-21, fluoroscopy, so first

## Obtain BRAX Brazilian chest films (PhysioNet)

What it is: 40,967 chest radiographs from 24,959 studies at Hospital Israelita Albert Einstein, Sao Paulo, frontal and lateral views, labelled with 14 radiological findings; PhysioNet credentialed access
Link: https://physionet.org/content/brax/
Why it matters: lateral chest films show the thoracic spine end on, from a South American population none of the held sets covers
Route in: agreement; status now: needs-owner
Letter or form: the PhysioNet project page's data use agreement
The owner's hand: the PhysioNet data use agreement on the project page; access may then wait on PhysioNet's review of his CITI course record, as MIMIC-CXR does
Record: datasets/brax.json (reach gated, licence: PhysioNet Credentialed Health Data License)
Files likely touched: datasets/brax.json
Priority: group 2, a form, a gate or an account; found by the sweep of 2026-10-21

## Obtain BIMCV COVID-19+ chest films (IEEE DataPort)

What it is: chest radiographs, laterals among them, and CTs of COVID-19 patients from the Valencian region's hospitals (BIMCV), open access on IEEE DataPort (doi:10.21227/w3aw-rv39) as tar.gz parts of about 389 GB in all
Link: https://ieee-dataport.org/open-access/bimcv-covid-19-large-annotated-dataset-rx-and-ct-images-covid-19-patients
Why it matters: lateral chest films from a Spanish population; a large pool of thoracic spine views
Route in: account; status now: needs-owner
Letter or form: the IEEE DataPort page, signed in to a free IEEE account
The owner's hand: the free IEEE account, and the space decision: about 389 GB is over the promoter's 100 GB budget
Record: datasets/bimcv_covid19.json (reach get, licence: not recorded; read on the page after the login)
Files likely touched: datasets/bimcv_covid19.json
Priority: group 2, a form, a gate or an account; found by the sweep of 2026-10-21
