# Dataset inclusion audit

Source: the thread "Fit datasets under 20 TB", 2026-10-25, the owner's ask: "a total audit of datasets and what value each brings to the final dataset so i can choose which ones to keep, first ill need criteria for inclusion which you can use prior art to inform particularly xvr and flexray data sets, anything with either paired CT-Xr scans, annotations of any kind that are related to spine or pelvis (CT or XR), anything Fluoro (XR or video), should automatically be included". Every one of the 166 records under datasets/ at main 7dcaf05 is classified below. The counts come from the records and from tools/storage.py's value block (#249). Updated the same day from the full grid census, spine-datasets grid/folders.json at c740a18 (#369, SchwingNet's folder report of grid job 40780668): every size and every on-the-grid mark below is the census's, and the records not on the grid are listed with where each stands. Nothing here deletes or fetches anything: it is the list the owner chooses from.

## What prior art keeps

Two recent public lines of work set what a spine and pelvis X-ray collection must hold.

- xvr (Gopalakrishnan et al., github.com/eigenvivek/xvr) registers a patient's X-ray to that patient's own CT. Every set it is scored on pairs real X-rays with the CT of the same body and a known pose: DeepFluoro (Grupp et al. 2020, six cadaveric pelves, 366 fluoroscopic frames on a Siemens Cios Fusion, with CT, pelvis and lumbar masks and 14 landmarks), a distal femur set of five cadavers (held here as ipcai2025_xray_ct), and a Ljubljana set of ten (the University of Ljubljana's 2D/3D gold standards; the one held here, ljubljana_2d3d_gs, is its cadaver lumbar spine, L1 to L5, and whether it is the same set xvr scores on was not checked). A pair of this kind cannot be made later from unpaired data, so it is the scarcest thing a collection can hold.
- FleXray (Butoi, Gopalakrishnan, Guttag, Dalca, Dey; arXiv 2609.26756, MIT) builds its X-ray labels by rendering segmented CT and editing the renders toward clinical appearance, and scores the result on real images it never saw: AASCE's 218 spine radiographs with Cobb angles, and DeepFluoro's frames. SyntheX and FluoroSAM from the ARCADE lab do the same from decedent CT (NMDID) and TotalSegmentator, labelled by TotalSegmentator and rendered with DeepDRR, and test on DeepFluoro. So the two things that carry this approach are CT with spine and pelvis masks, the source of every rendered label, and real X-rays with human labels, the only honest test.

Read together, they give the reasons a set earns its space: a real CT and X-ray pair; labels a person made on spine or pelvis anatomy; real fluoroscopy, which renders imitate and never replace; and CT that can be rendered once it is segmented.

## Criteria

A set is kept without question when it meets any one of these, the owner's three rules:

1. Paired CT and X-ray: real X-rays (films, fluoroscopy or projections) with a CT of the same body, whether or not the pose is given. DeepFluoro, ljubljana_2d3d_gs and the femur set xvr uses are this kind. A pair of a non-spine body (a femur, a knee, a pig limb) is kept by this rule and flagged, since it serves registration and appearance, not level naming.
2. Annotations of any kind on spine or pelvis, CT or X-ray: masks that came with the release (vertebrae by level or together, pelvis, sacrum, hip), named vertebral levels, landmarks or keypoints, Cobb angles, grades or class labels of a spine or pelvic finding. Masks the release made with an automatic tool count and are marked automatic; masks this project made do not count, because they can be made again from the images. A set whose only labels are of other anatomy (kidney stones, ribs, chest findings) does not meet this rule.
3. Fluoroscopy, still or video, of any anatomy. Non-spine fluoroscopy (coronary angiography, knee implants, catheters) is kept by the rule and flagged.

The rest are candidates, which the owner keeps or drops:

- CT render source: CT whose field shows spine or pelvis but whose release carries no spine labels. Its value is as a source of rendered X-rays once segmented, the FleXray and SyntheX route, so it is worth its space in proportion to the people it adds and to whether those people are already held elsewhere.
- Spine in view, no labels: real spine or pelvic films with no labels; they add real appearance, never truth.
- Exclude candidate: sets whose spine is incidental (chest radiograph collections) and which meet no rule.

How the rules were read: a set's rules come from its record's group, its pairing block, its segmentations (origin release, vertebrae by level or together, or a mask list naming spine or pelvic anatomy), its level truth, and, for records outside the CT group, its description naming both an annotation and spine or pelvic anatomy. Eight records were ruled by hand from their text: pengwin_task2_xrays (pelvic fragment masks on renders), mendeley_ddh_hips and scidb_mtddh (hip keypoints and dysplasia labels), fraiwan_spine_xray (scoliosis and spondylolisthesis classes) and fracatlas (hip and pelvic fracture masks) in; kub_stonex, vindr_cxr and ribfrac out of rule 2, their labels being of other anatomy.

## Summary

| Verdict | Sets | On the grid | Grid size | Not on the grid |
|---|---:|---:|---:|---:|
| include | 95 | 52 | 8.63 TB | 43 |
| candidate: CT render source | 54 | 53 | 2.66 TB | 1 |
| candidate: spine in view, no labels | 9 | 4 | 0.18 TB | 5 |
| exclude candidate | 8 | 3 | 0.20 TB | 5 |

The census: the data root holds 111 folders (one of them the 17 GB folder whose name the readout hides), 14.04 TB. Dataset records account for 77 of them, 12.08 TB, holding 112 of the 166 records (a folder shared by several sets, idc/ with 39 and external/ with 2, is counted once in the totals and each set shows its own size where its record gives one). The other 34 folders, 1.98 TB, are no dataset's (section On the grid with no dataset record). 54 records are not on the grid. Three records say they are held but have no folder in the data root, so they sit elsewhere or were never unpacked: cadica, scidb_mtddh, veterinary_pig_levelcheck.

What this means for the space: the kept sets the grid holds take 8.63 TB and 43 kept sets are still to obtain. The candidates the grid holds take 3.04 TB; the largest are idc_ldct_and_projection_data 0.86 TB, tcia_fdg_pet_ct_lesions 0.37 TB, aws_stoic2021 0.25 TB, panorama 0.18 TB, rexgradient_160k 0.16 TB, ribfrac 0.15 TB. The derived banks take 1.62 TB (or_ready 0.81 and multisource_banks 0.32 the largest), all of it made from held sets and so rebuildable.

The power target the storage panel uses, a level-naming accuracy within plus or minus 5 points at 95 percent confidence, needs 385 people with read level truth; the kept sets carry about 5,990, so that target does not decide which sets stay, and the choice rests on coverage, pairing and labels.

Columns: Rules met, the criteria above; Grid (census), the census size or "not on grid" with the record's status; Licence, open, restricted or unknown as the census classes it; People, from the record where it gives them; Level truth, read (a person named the levels), automatic, no or unknown; Prior source, yes where the set is CT with masks to render from; Flags, a body that is not a human spine, or more than 50 scans or patients shared with another set by the overlap ledger.

## The audit

### Include (95)

| Set | Rules met | Grid (census) | Licence | People | Level truth | Prior source | Flags |
|---|---|---|---|---:|---|---|---|
| idc_nlst | spine/pelvis masks (automatic) | 3.17 TB | open | 24,713 | automatic | yes |  |
| rsna_rspect | spine/pelvis masks (read) | 0.98 TB | restricted |  | unknown |  |  |
| cobra2026 | paired CT-XR; spine/pelvis masks (read); fluoro | 0.75 TB | restricted | 692 | read |  |  |
| abdomenatlas3_mini | spine/pelvis masks (read) | 0.53 TB | restricted | 7,835 | automatic | yes |  |
| verse | spine/pelvis masks (read) | 0.38 TB | open | 355 | read | yes |  |
| hf_abdomenatlas2_0_mini | spine/pelvis masks (read) | 0.33 TB | restricted |  | unknown |  |  |
| idc_spinal_multiple_myeloma_seg | spine/pelvis masks (automatic) | 0.30 TB | open | 67 | automatic | yes |  |
| zenodo_vsd_fullbody | spine/pelvis masks (read) | 0.25 TB | restricted | 100 | unknown |  |  |
| rsna_2022_cervical | spine/pelvis masks (read) | 0.19 TB | restricted |  | read | yes |  |
| ctspinopelvic1k | spine/pelvis masks (read) | 0.19 TB | restricted |  | read | yes | shares 526 scans with ctspine1k |
| zenodo_unitochest | spine/pelvis masks (read) | 0.16 TB | open | 623 | unknown |  |  |
| ctspine1k | spine/pelvis masks (read) | 0.15 TB | restricted |  | read | yes | shares 526 scans with ctspinopelvic1k |
| deepfluoro | paired CT-XR; spine/pelvis masks (read); fluoro | 0.11 TB | restricted | 6 | read |  |  |
| vindr_spinexr | spine levels named | 0.11 TB | restricted |  | read |  |  |
| carmlspine | paired CT-XR; spine/pelvis masks (read); fluoro | 0.10 TB | open | 149 | read |  |  |
| cads | spine/pelvis masks (read) | 0.09 TB | restricted |  | unknown |  |  |
| totalsegmentator | spine/pelvis masks (automatic) | 0.09 TB | open |  | read | yes |  |
| pengwin2026 | spine/pelvis masks (read) | 0.08 TB | restricted | 340 | automatic | yes |  |
| lumos | paired CT-XR; spine levels named; fluoro | 0.08 TB | restricted | 803 | read |  |  |
| nlst_pilot | spine/pelvis masks (automatic) | 0.07 TB | open | 500 | automatic | yes |  |
| idc_pediatric_ct_seg | spine/pelvis masks (automatic) | 0.06 TB (in idc/, shared by 39 sets) | open | 352 | automatic | yes |  |
| cathaction | fluoro | 0.05 TB | restricted |  | no |  | no human spine in view? |
| buu_lspine | spine levels named | 0.04 TB | restricted | 3,600 | read |  |  |
| magic_ct | spine/pelvis masks (read) | 0.04 TB | restricted |  | unknown |  |  |
| zenodo_ts_task_liver_lesions | spine/pelvis masks (read) | 0.04 TB | open | 842 | unknown |  |  |
| zenodo_medpelvis3d | spine/pelvis masks (read) | 0.04 TB | open | 99 | unknown |  |  |
| pengwin_task2_xrays | spine/pelvis annotation (judged from the record) | 0.03 TB | open |  | no |  |  |
| idc_nsclc_radiomics | spine/pelvis masks (read) | 0.03 TB | restricted | 415 | unknown |  |  |
| deep_psma | spine/pelvis masks (read) | 0.02 TB | restricted | 100 | automatic | yes |  |
| zenodo_tmtv_benchmark | spine/pelvis masks (read) | 0.02 TB | open | 60 | unknown |  |  |
| dysphagiabank | fluoro | 0.02 TB (in external/, shared by 2 sets) | restricted |  | no |  |  |
| quadra_hc | spine/pelvis masks (read) | 0.02 TB | open | 48 | automatic | yes |  |
| idc_spine_mets_ct_seg | spine/pelvis masks (automatic) | 0.02 TB | open | 54 | automatic | yes |  |
| curvas_pdacvi | spine/pelvis masks (read) | 0.02 TB | open | 109 | automatic | yes |  |
| ctpelvic1k | spine/pelvis masks (read) | 0.01 TB | restricted |  | read | yes |  |
| zenodo_lumvbcanseg | spine/pelvis masks (read) | 0.01 TB | open | 185 | unknown |  |  |
| zenodo_ts_task_hip_implant | spine/pelvis masks (read) | 0.01 TB | open | 71 | unknown |  |  |
| zenodo_ts_task_pleural_effusion | spine/pelvis masks (read) | 0.01 TB | open | 600 | unknown |  |  |
| csi2014 | spine/pelvis masks (read) | <0.01 TB | open | 20 | read | yes |  |
| ipcai2025_xray_ct | paired CT-XR; fluoro | <0.01 TB | restricted | 5 | no |  | no human spine in view? |
| aariz_cephalograms | spine levels named | <0.01 TB | open |  | read |  |  |
| verse_2d_projections | spine/pelvis masks (read) | <0.01 TB | unknown |  | unknown |  |  |
| csxa | spine levels named | <0.01 TB | open |  | read |  |  |
| bournemouth_cervical_qf | spine levels named; fluoro | <0.01 TB | restricted | 63 | read |  |  |
| nhanes2_annotated | spine levels named | <0.01 TB | open | 364 | read |  |  |
| aasce | spine levels named | <0.01 TB | restricted |  | read |  |  |
| geneva_hip | paired CT-XR; spine/pelvis masks (read); fluoro | <0.01 TB | open | 1 | no |  |  |
| ljubljana_2d3d_gs | paired CT-XR; spine/pelvis masks (read); fluoro | <0.01 TB | restricted | 1 | read |  |  |
| kaggle_scoliosis_yolov5 | spine levels named | <0.01 TB | open |  | read |  |  |
| fracatlas | spine/pelvis annotation (judged from the record) | <0.01 TB | open |  | no |  | no human spine in view? |
| fraiwan_spine_xray | spine/pelvis annotation (judged from the record) | <0.01 TB | open | 338 | no |  |  |
| bern_myelography | spine levels named; fluoro | size unknown (in external/, shared by 2 sets) | restricted |  | read |  |  |
| balgrist_lumbar | paired CT-XR; fluoro | not on grid (refused) | unknown |  | unknown |  |  |
| bournemouth_lumbar_qf | spine levels named; fluoro | not on grid (requested) | unknown | 127 | read |  |  |
| cadica | fluoro | not on grid (fetched) | open | 42 | no |  | no human spine in view? |
| cams_knee | paired CT-XR; fluoro | not on grid (needs-owner) | restricted | 6 | no |  | no human spine in view? |
| cm_spine_drive_file | spine levels named; fluoro | not on grid (requested) | unknown |  | read |  |  |
| cobra_embargoed | paired CT-XR; spine/pelvis masks (read) | not on grid (todo) | restricted | 175 | unknown |  |  |
| coronary_angiography | fluoro | not on grid (todo) | unknown |  | no |  |  |
| ct_rate | spine/pelvis masks (read) | not on grid (granted) | restricted |  | unknown |  |  |
| daradia_vertebroplasty | fluoro | not on grid (requested) | unknown |  | no |  |  |
| dmx_imaging | fluoro | not on grid (requested) | unknown |  | no |  |  |
| faubel_painsource | fluoro | not on grid (requested) | unknown |  | no |  |  |
| guide3d | fluoro | not on grid (needs-owner) | restricted |  | no |  | no human spine in view? |
| hsg_ais_registry | spine/pelvis annotation (from the record text) | not on grid (requested) | unknown |  | unknown |  |  |
| huashan_fudan | paired CT-XR; spine levels named; fluoro | not on grid (requested) | restricted | 140 | read |  |  |
| idc_prostate_anatomical_edge_cases | spine/pelvis masks (read) | not on grid (todo) | open | 131 | unknown |  |  |
| jefferson_drg | spine levels named; fluoro | not on grid (requested) | restricted |  | read |  |  |
| konica_ddr | fluoro | not on grid (requested) | unknown |  | no |  |  |
| levelcheck_jhu | paired CT-XR; spine levels named; fluoro | not on grid (refused) | restricted | 202 | read |  |  |
| maastricht_cervical | spine levels named | not on grid (requested) | restricted |  | read |  |  |
| mayfield_kyphoplasty | fluoro | not on grid (requested) | unknown |  | unknown |  |  |
| mendeley_ddh_hips | spine/pelvis annotation (judged from the record) | not on grid (todo) | open |  | no |  |  |
| mros_lateral_spine | spine levels named | not on grid (needs-owner) | restricted |  | read |  |  |
| mtfi_lumbar_coupling | fluoro | not on grid (requested) | unknown |  | no |  |  |
| neurosurgical_focus_video | spine levels named; fluoro | not on grid (todo) | open |  | read |  |  |
| nit_warangal_nims | paired CT-XR; spine/pelvis masks (read); fluoro | not on grid (requested) | restricted | 9 | read |  |  |
| pediatric_iri | fluoro | not on grid (requested) | unknown |  | no |  |  |
| pittsburgh_swallow | spine levels named; fluoro | not on grid (requested) | restricted | 335 | read |  |  |
| procedure_guide | spine levels named; fluoro | not on grid (requested) | restricted |  | read |  |  |
| pumch_stitching | fluoro | not on grid (requested) | restricted |  | no |  |  |
| radiopaedia | spine levels named; fluoro | not on grid (granted) | restricted |  | read |  |  |
| rsna_ratic | spine/pelvis masks (read) | not on grid (granted) | restricted |  | unknown |  |  |
| scidb_enhance_pet_1_6k | spine/pelvis masks (read) | not on grid (todo) | open |  | unknown |  |  |
| scidb_mtddh | spine/pelvis annotation (judged from the record) | not on grid (fetched) | open | 2,156 | no |  |  |
| seattle_science_foundation | spine levels named; fluoro | not on grid (requested) | unknown |  | read |  |  |
| sof_lateral_spine | spine levels named | not on grid (needs-owner) | restricted |  | read |  |  |
| stanford_aimi_inspect | spine/pelvis masks (read) | not on grid (needs-owner) | restricted |  | unknown |  |  |
| stanford_aimi_merlin | spine/pelvis masks (read) | not on grid (needs-owner) | restricted |  | unknown |  |  |
| sx_stitch | spine levels named; fluoro | not on grid (requested) | unknown |  | read |  |  |
| vanderbilt_tha_fluoro | spine levels named; fluoro | not on grid (requested) | restricted |  | read |  |  |
| veriserum | paired CT-XR; fluoro | not on grid (needs-owner) | restricted |  | no |  | no human spine in view? |
| vertxnet_nhanes2_labels | spine levels named | not on grid (todo) | unknown |  | read |  |  |
| veterinary_pig_levelcheck | paired CT-XR | not on grid (held) | open | 1 | no |  | no human spine in view? |
| vfss2022 | fluoro | not on grid (todo) | unknown |  | no |  |  |

### Candidate: ct render source (54)

| Set | Rules met | Grid (census) | Licence | People | Level truth | Prior source | Flags |
|---|---|---|---|---:|---|---|---|
| idc_ldct_and_projection_data | - | 0.86 TB | open | 99 | unknown |  |  |
| tcia_fdg_pet_ct_lesions | - | 0.37 TB | open | 900 | automatic | yes |  |
| aws_stoic2021 | - | 0.25 TB | restricted | 2,000 | unknown |  |  |
| panorama | - | 0.18 TB | restricted | 1,950 | automatic | yes |  |
| ribfrac | - | 0.15 TB | restricted |  | no | yes |  |
| amos22 | - | 0.10 TB | open | 2,200 | automatic | yes |  |
| idc_nsclc_radiogenomics | - | 0.09 TB | open | 188 | unknown |  |  |
| kidney_thoraxabdomen | - | 0.07 TB | open | 215 | automatic | yes |  |
| idc_covid_19_ny_sbu | - | 0.06 TB (in idc/, shared by 39 sets) | open | 443 | automatic | yes |  |
| idc_psma_pet_ct_lesions | - | 0.06 TB (in idc/, shared by 39 sets) | open | 374 | automatic | yes |  |
| waw_tace | - | 0.04 TB | open | 233 | automatic | yes |  |
| idc_cptac_luad | - | 0.04 TB | open | 32 | unknown |  |  |
| idc_eay131 | - | 0.04 TB (in idc/, shared by 39 sets) | open | 376 | automatic | yes |  |
| idc_cptac_lscc | - | 0.03 TB | open | 32 | unknown |  |  |
| idc_lung_pet_ct_dx | - | 0.03 TB (in idc/, shared by 39 sets) | open | 158 | automatic | yes |  |
| curvas | - | 0.03 TB | open | 90 | automatic | yes |  |
| idc_mediastinal_lymph_node_seg | - | 0.03 TB (in idc/, shared by 39 sets) | open | 316 | automatic | yes |  |
| barts_crl | - | 0.02 TB | open | 220 | automatic | yes |  |
| idc_rider_lung_pet_ct | - | 0.02 TB (in idc/, shared by 39 sets) | open | 117 | automatic | yes |  |
| idc_acrin_nsclc_fdg_pet | - | 0.02 TB (in idc/, shared by 39 sets) | open | 131 | automatic | yes |  |
| aortaseg60 | - | 0.01 TB | open | 60 | automatic | yes |  |
| idc_cptac_ucec | - | 0.01 TB (in idc/, shared by 39 sets) | open | 66 | automatic | yes |  |
| idc_tcga_blca | - | 0.01 TB (in idc/, shared by 39 sets) | open | 79 | automatic | yes |  |
| idc_cptac_pda | - | 0.01 TB (in idc/, shared by 39 sets) | open | 62 | automatic | yes |  |
| idc_cmb_lca | - | 0.01 TB (in idc/, shared by 39 sets) | open | 75 | automatic | yes |  |
| idc_tcga_kirc | - | <0.01 TB (in idc/, shared by 39 sets) | open | 129 | automatic | yes |  |
| idc_midrc_ricord_1b | - | <0.01 TB | restricted | 91 | unknown |  |  |
| idc_cptac_ccrcc | - | <0.01 TB (in idc/, shared by 39 sets) | open | 48 | automatic | yes |  |
| idc_cptac_stad | - | <0.01 TB (in idc/, shared by 39 sets) | open | 19 | automatic | yes |  |
| idc_midrc_ricord_1a | - | <0.01 TB (in idc/, shared by 39 sets) | restricted | 98 | automatic | yes |  |
| idc_tcga_stad | - | <0.01 TB (in idc/, shared by 39 sets) | open | 45 | automatic | yes |  |
| idc_colorectal_liver_metastases | - | <0.01 TB (in idc/, shared by 39 sets) | open | 80 | automatic | yes |  |
| idc_ctpred_sunitinib_pannet | - | <0.01 TB (in idc/, shared by 39 sets) | open | 34 | automatic | yes |  |
| idc_covid_19_ar | - | <0.01 TB (in idc/, shared by 39 sets) | open | 23 | automatic | yes |  |
| idc_varepop_apollo | - | <0.01 TB (in idc/, shared by 39 sets) | open | 35 | automatic | yes |  |
| idc_cmb_crc | - | <0.01 TB (in idc/, shared by 39 sets) | open | 30 | automatic | yes |  |
| idc_hcc_tace_seg | - | <0.01 TB (in idc/, shared by 39 sets) | open | 101 | automatic | yes |  |
| idc_tcga_lihc | - | <0.01 TB (in idc/, shared by 39 sets) | open | 42 | automatic | yes |  |
| idc_pelvic_reference_data | - | <0.01 TB (in idc/, shared by 39 sets) | open | 58 | automatic | yes |  |
| idc_anti_pd_1_lung | - | <0.01 TB (in idc/, shared by 39 sets) | open | 34 | automatic | yes |  |
| idc_cptac_cm | - | <0.01 TB (in idc/, shared by 39 sets) | open | 12 | automatic | yes |  |
| idc_tcga_ucec | - | <0.01 TB (in idc/, shared by 39 sets) | open | 38 | automatic | yes |  |
| idc_adrenal_acc_ki67_seg | - | <0.01 TB (in idc/, shared by 39 sets) | open | 29 | automatic | yes |  |
| idc_cptac_sar | - | <0.01 TB (in idc/, shared by 39 sets) | open | 14 | automatic | yes |  |
| idc_pancreatic_ct_cbct_seg | - | <0.01 TB (in idc/, shared by 39 sets) | open | 40 | automatic | yes |  |
| idc_acrin_flt_breast | - | <0.01 TB (in idc/, shared by 39 sets) | open | 15 | automatic | yes |  |
| idc_cmb_brca | - | <0.01 TB (in idc/, shared by 39 sets) | open | 21 | automatic | yes |  |
| idc_tcga_esca | - | <0.01 TB (in idc/, shared by 39 sets) | open | 16 | automatic | yes |  |
| idc_tcga_ov | - | <0.01 TB (in idc/, shared by 39 sets) | open | 24 | automatic | yes |  |
| idc_cmb_mml | - | <0.01 TB (in idc/, shared by 39 sets) | open | 16 | automatic | yes |  |
| idc_cmb_mel | - | <0.01 TB (in idc/, shared by 39 sets) | open | 23 | automatic | yes |  |
| idc_ct_vs_pet_ventilation_imaging | - | <0.01 TB (in idc/, shared by 39 sets) | open | 20 | automatic | yes |  |
| idc_cmb_ov | - | <0.01 TB (in idc/, shared by 39 sets) | open | 7 | automatic | yes |  |
| idc_lidc_idri | - | not on grid (todo) | open | 997 | unknown |  |  |

### Candidate: spine in view, no labels (9)

| Set | Rules met | Grid (census) | Licence | People | Level truth | Prior source | Flags |
|---|---|---|---|---:|---|---|---|
| nhanes2_unannotated | - | 0.13 TB | open |  | no |  |  |
| kub_stonex | - | 0.05 TB | open | 1,703 | no |  |  |
| vindr_pcxr | - | <0.01 TB | restricted |  | no |  |  |
| canine_thoracic_vhs | - | <0.01 TB | open |  | no |  | no human spine in view? |
| ieee_dataport_lateral_236 | - | not on grid (needs-owner) | unknown | 236 | no |  |  |
| kaggle_fracture_multiregion | - | not on grid (todo) | open |  | no |  | no human spine in view? |
| tvgh_as_spine_xray | - | not on grid (requested) | unknown |  | unknown |  |  |
| tvgh_spinexr | - | not on grid (requested) | unknown |  | unknown |  |  |
| vindr_cxr | - | not on grid (requested) | restricted |  | no |  |  |

### Exclude candidate (8)

| Set | Rules met | Grid (census) | Licence | People | Level truth | Prior source | Flags |
|---|---|---|---|---:|---|---|---|
| rexgradient_160k | - | 0.16 TB | restricted | 109,487 | no |  |  |
| nih_chestxray14 | - | 0.04 TB | unknown | 30,805 | no |  |  |
| open_i_chest | - | <0.01 TB | restricted |  | no |  |  |
| bimcv_covid19 | - | not on grid (needs-owner) | unknown |  | no |  |  |
| brax | - | not on grid (needs-owner) | restricted |  | no |  |  |
| chexpert_plus | - | not on grid (todo) | restricted | 65,240 | no |  |  |
| mimic_cxr | - | not on grid (requested) | restricted | 65,379 | no |  |  |
| padchest | - | not on grid (todo) | restricted | 67,625 | no |  |  |

### Not on the grid (54)

Every record with no folder in the census, by where it stands. The verdict says whether it would be kept once obtained.

| Set | Status | Verdict | Recipe call |
|---|---|---|---|
| veterinary_pig_levelcheck | held | include | keep |
| cadica | fetched | include | keep |
| scidb_mtddh | fetched | include | maybe |
| ct_rate | granted | include | defer |
| radiopaedia | granted | include | defer |
| rsna_ratic | granted | include | defer |
| bournemouth_lumbar_qf | requested | include | keep |
| cm_spine_drive_file | requested | include | acquire |
| daradia_vertebroplasty | requested | include | defer |
| dmx_imaging | requested | include | defer |
| faubel_painsource | requested | include | defer |
| hsg_ais_registry | requested | include | maybe |
| huashan_fudan | requested | include | acquire |
| jefferson_drg | requested | include | maybe |
| konica_ddr | requested | include | defer |
| maastricht_cervical | requested | include | acquire |
| mayfield_kyphoplasty | requested | include | maybe |
| mimic_cxr | requested | exclude candidate | drop |
| mtfi_lumbar_coupling | requested | include | defer |
| nit_warangal_nims | requested | include | acquire |
| pediatric_iri | requested | include | maybe |
| pittsburgh_swallow | requested | include | acquire |
| procedure_guide | requested | include | maybe |
| pumch_stitching | requested | include | maybe |
| seattle_science_foundation | requested | include | maybe |
| sx_stitch | requested | include | maybe |
| tvgh_as_spine_xray | requested | candidate: spine in view, no labels | defer |
| tvgh_spinexr | requested | candidate: spine in view, no labels | defer |
| vanderbilt_tha_fluoro | requested | include | acquire |
| vindr_cxr | requested | candidate: spine in view, no labels | drop |
| bimcv_covid19 | needs-owner | exclude candidate | drop |
| brax | needs-owner | exclude candidate | drop |
| cams_knee | needs-owner | include | maybe |
| guide3d | needs-owner | include | maybe |
| ieee_dataport_lateral_236 | needs-owner | candidate: spine in view, no labels | acquire |
| mros_lateral_spine | needs-owner | include | acquire |
| sof_lateral_spine | needs-owner | include | acquire |
| stanford_aimi_inspect | needs-owner | include | defer |
| stanford_aimi_merlin | needs-owner | include | defer |
| veriserum | needs-owner | include | maybe |
| chexpert_plus | todo | exclude candidate | drop |
| cobra_embargoed | todo | include | defer |
| coronary_angiography | todo | include | keep |
| idc_lidc_idri | todo | candidate: CT render source | drop |
| idc_prostate_anatomical_edge_cases | todo | include | maybe |
| kaggle_fracture_multiregion | todo | candidate: spine in view, no labels | drop |
| mendeley_ddh_hips | todo | include | maybe |
| neurosurgical_focus_video | todo | include | maybe |
| padchest | todo | exclude candidate | drop |
| scidb_enhance_pet_1_6k | todo | include | defer |
| vertxnet_nhanes2_labels | todo | include | acquire |
| vfss2022 | todo | include | keep |
| balgrist_lumbar | refused | include | acquire |
| levelcheck_jhu | refused | include | acquire |

### On the grid with no dataset record (34)

Folders of the data root that are not a dataset: what the project made from held sets (derived), its working folders, empties, five held sets still without a record (unrecorded), and one folder whose name the readout hides. Each has its spine-datasets task.

| Folder | Kind | Task | Size | What |
|---|---|---:|---:|---|
| or_ready | derived | #354 | 0.81 TB | the operating-room banks: 368,455 files, 808 GB, in 55 folders (indomain, wholespine, crossdev, auto_reference and others), frames and labels derived from held sets |
| multisource_banks | derived | #353 | 0.32 TB | the multi-source banks: 208,029 files, 316 GB, film and DRR banks derived from the held sets (and the implant_ct_synthetic group) |
| anomaly_harvest | derived | #334 | 0.30 TB | the anomaly harvest: 1,063,032 files, 303 GB, banks cut from the held CT sets for the transitional-anatomy census |
| ctsp_april | derived | #338 | 0.08 TB | the April CTSpinoPelvic1K build: 351 CT volumes, 1,153 label maps and its dry run, 81 GB |
| spine_detector_corpus | derived | #361 | 0.06 TB | the spine detector corpus: 530,722 files, 56 GB, images and YOLO labels gathered from the held film sets |
| devcorpus | derived | #341 | 0.02 TB | the development corpus: 99,553 files, 17 GB, styled and rendered DRRs with their poses and lists |
| ctspinopelvic1k_build_tree | derived | #339 | <0.01 TB | the CTSpinoPelvic1K build tree: 3,340 files, 9.9 GB, label maps and their records |
| spineps | derived | #362 | <0.01 TB | SPINEPS outputs: 41,571 files, 8.2 GB, vertebral bodies and centroids relabelled from held CTs |
| fluorogen_synthetic | derived | #347 | <0.01 TB | synthetic fluoroscopy: 30,035 files, 7.9 GB, 3,001 generated frames with labels |
| rare_class | derived | #357 | <0.01 TB | the rare-class DRR banks: 44,243 files, 5.4 GB, DRRs from VerSe, CTSpinoPelvic1K and TotalSegmentator |
| xrspinopelvic1k | derived | #367 | <0.01 TB | XRSpinoPelvic1K: 32,097 files, 4.3 GB, the private film set's derived banks |
| devcorpus_arc | derived | #342 | <0.01 TB | the angle-sweep corpus: 13,075 files, 688 MB, renders at swept C-arm angles; its void evaluation is kept and never quoted |
| cm_spine_drive_file | empty | #336 | <0.01 TB | an empty folder |
| morphdef | empty | #352 | <0.01 TB | an empty folder |
| [hidden] | unnamed | #368 | 0.02 TB | a folder of about 17 GB whose name the grid readout withholds as [hidden] |
| fluorocap | unrecorded | #346 | 0.20 TB | FluoroCap: 361,567 fluoroscopy images (PNG and JPEG, with PDFs) from published figures and their captions, 202 GB, with 1,500 derived frames; private, a test set at most and never training; held, with no record here yet |
| ieee_dataport_lateral_fullspine_236 | unrecorded | #349 | <0.01 TB | IEEE DataPort lateral full-spine films: 236 JPEG films (1528-3056 x 2845-8826) and their derived arrays, 5.7 GB; held, with no record here yet |
| spinesac | unrecorded | #363 | <0.01 TB | SpineSAC: 5,566 files, 4.0 GB, named in SchwingNet's registry; held, with no record here yet |
| spinal_ai2024 | unrecorded | #360 | <0.01 TB | Spinal-AI2024: 20,000 JPEG spine radiographs (512-960 x 241-512) with 16,716 derived landmark files; held, with no record here yet |
| mendeley_5jdfdgp762 | unrecorded | #351 | <0.01 TB | Mendeley Data 5jdfdgp762: 714 JPEG radiographs (640-2464 x 640-3036) with labels, and their derived arrays; held, with no record here yet |
| polypose | working | #356 | 0.08 TB | PolyPose: 118,395 files, 82 GB, the method's environment, weights and validation volumes |
| _samples | working | #333 | 0.03 TB | the sample index's runs: samples.sqlite and its manifest, 28 GB |
| fig6 | working | #344 | 0.01 TB | figure 6: 108,412 files, 13 GB, the evaluation sets, detectors and outputs of SchwingNet's figure 6 |
| ctsp0533_repair | working | #337 | <0.01 TB | a repair of CTSpinoPelvic1K case 0533: 577 DICOM slices and its volume, 576 MB |
| realxray_work | working | #359 | <0.01 TB | real X-ray working copies: 248 files, 310 MB, DeepFluoro and Geneva hip volumes being converted |
| gallery | working | #348 | <0.01 TB | the gallery: 472 files, 101 MB, figure panels |
| figure1 | working | #345 | <0.01 TB | figure 1: 94 files, 26 MB, its panels |
| tcia_ct_colonography | working | #364 | <0.01 TB | TCIA CT colonography: a manifest only, 3 files, 12 MB; no images were fetched |
| inventory | working | #350 | <0.01 TB | inventories: 34 files, 7 MB, the census of 2026-10-07 and film lists |
| vindr | working | #366 | <0.01 TB | VinDr identity and audit: 3 files, 1.5 MB, the identity table for the VinDr sets |
| d815_repair | working | #340 | <0.01 TB | a repair of case 815: 11 files, 1 MB |
| outline_conv | working | #355 | <0.01 TB | outline conversions: 486 files, 73 KB, label conversions for the real X-ray banks |
| buu_lspine_v1_smoke | working | #335 | <0.01 TB | a smoke-test subset of BUU-LSPINE: 77 links, 7 KB |
| validation_ts | working | #365 | <0.01 TB | a validation list: 70 links, 4 KB, into TotalSegmentator |
