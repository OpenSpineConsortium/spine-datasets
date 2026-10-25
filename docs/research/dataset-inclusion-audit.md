# Dataset inclusion audit

Source: the thread "Fit datasets under 20 TB", 2026-10-25, the owner's ask: "a total audit of datasets and what value each brings to the final dataset so i can choose which ones to keep, first ill need criteria for inclusion which you can use prior art to inform particularly xvr and flexray data sets, anything with either paired CT-Xr scans, annotations of any kind that are related to spine or pelvis (CT or XR), anything Fluoro (XR or video), should automatically be included". Every one of the 166 records under datasets/ at main 7dcaf05 is classified below. The counts come from the records and from tools/storage.py's value block (#249); the sizes are what the grid holds today. Nothing here deletes or fetches anything: it is the list the owner chooses from.

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

| Verdict | Sets | Held | Held size |
|---|---:|---:|---:|
| include | 95 | 47 | 4.65 TB |
| candidate: CT render source | 54 | 53 | 2.75 TB |
| candidate: spine in view, no labels | 9 | 2 | 0.19 TB |
| exclude candidate | 8 | 2 | 0.05 TB |

What this means for the space: the kept sets the grid holds take 4.65 TB, and 48 kept sets are not on the grid yet, most with no size known. The candidates the grid holds take about 3 TB, nearly all of it CT render sources. Dropping every film candidate and exclude candidate frees under 0.3 TB, so the choices that move the total are among the CT render sources (largest: idc_ldct_and_projection_data 0.86 TB, tcia_fdg_pet_ct_lesions 0.39, aws_stoic2021 0.26, panorama 0.19, ribfrac 0.16) and outside the datasets altogether (the untracked full NLST, about 3.2 TB, and the u251 work folders, about 1 TB, from the survey of 2026-10-25).

The power target the storage panel uses, a level-naming accuracy within plus or minus 5 points at 95 percent confidence, needs 385 people with read level truth; the kept sets carry about 5,990, so that target does not decide which sets stay, and the choice rests on coverage, pairing and labels.

Columns: Rules met, the criteria above; Held, the size on the grid or "not held"; Licence, open, restricted or unknown as the census classes it; People, from the record where it gives them; Level truth, read (a person named the levels), automatic, no or unknown; Prior source, yes where the set is CT with masks to render from; Flags, a body that is not a human spine, or more than 50 scans or patients shared with another set by the overlap ledger.

## The audit

### Include (95)

| Set | Rules met | Held | Licence | People | Level truth | Prior source | Flags |
|---|---|---|---|---:|---|---|---|
| rsna_rspect | spine/pelvis masks (read) | 0.98 TB | restricted |  | unknown |  |  |
| cobra2026 | paired CT-XR; spine/pelvis masks (read); fluoro | 0.81 TB | restricted | 692 | read |  |  |
| abdomenatlas3_mini | spine/pelvis masks (read) | 0.57 TB | restricted | 7,835 | automatic | yes |  |
| idc_spinal_multiple_myeloma_seg | spine/pelvis masks (automatic) | 0.30 TB | open | 67 | automatic | yes |  |
| zenodo_vsd_fullbody | spine/pelvis masks (read) | 0.25 TB | restricted | 100 | unknown |  |  |
| rsna_2022_cervical | spine/pelvis masks (read) | 0.20 TB | restricted |  | read | yes |  |
| ctspinopelvic1k | spine/pelvis masks (read) | 0.20 TB | restricted |  | read | yes | shares 526 scans with ctspine1k |
| ctspine1k | spine/pelvis masks (read) | 0.16 TB | restricted |  | read | yes | shares 526 scans with ctspinopelvic1k |
| deepfluoro | paired CT-XR; spine/pelvis masks (read); fluoro | 0.12 TB | restricted | 6 | read |  |  |
| vindr_spinexr | spine levels named | 0.11 TB | restricted |  | read |  |  |
| carmlspine | paired CT-XR; spine/pelvis masks (read); fluoro | 0.10 TB | open | 149 | read |  |  |
| zenodo_unitochest | spine/pelvis masks (read) | 0.08 TB | open | 623 | unknown |  |  |
| pengwin2026 | spine/pelvis masks (read) | 0.08 TB | restricted | 340 | automatic | yes |  |
| lumos | paired CT-XR; spine levels named; fluoro | 0.08 TB | restricted | 803 | read |  |  |
| nlst_pilot | spine/pelvis masks (automatic) | 0.07 TB | open | 500 | automatic | yes |  |
| idc_pediatric_ct_seg | spine/pelvis masks (automatic) | 0.06 TB | open | 352 | automatic | yes |  |
| cathaction | fluoro | 0.06 TB | restricted |  | no |  | no human spine in view? |
| verse | spine/pelvis masks (read) | 0.05 TB | open | 355 | read | yes |  |
| zenodo_ts_task_liver_lesions | spine/pelvis masks (read) | 0.04 TB | open | 842 | unknown |  |  |
| buu_lspine | spine levels named | 0.04 TB | restricted | 3,600 | read |  |  |
| pengwin_task2_xrays | spine/pelvis annotation (judged from the record) | 0.03 TB | open |  | no |  |  |
| zenodo_medpelvis3d | spine/pelvis masks (read) | 0.03 TB | open | 99 | unknown |  |  |
| idc_nsclc_radiomics | spine/pelvis masks (read) | 0.03 TB | restricted | 415 | unknown |  |  |
| deep_psma | spine/pelvis masks (read) | 0.02 TB | restricted | 100 | automatic | yes |  |
| quadra_hc | spine/pelvis masks (read) | 0.02 TB | open | 48 | automatic | yes |  |
| dysphagiabank | fluoro | 0.02 TB | restricted |  | no |  |  |
| idc_spine_mets_ct_seg | spine/pelvis masks (automatic) | 0.02 TB | open | 54 | automatic | yes |  |
| curvas_pdacvi | spine/pelvis masks (read) | 0.02 TB | open | 109 | automatic | yes |  |
| ctpelvic1k | spine/pelvis masks (read) | 0.01 TB | restricted |  | read | yes |  |
| zenodo_lumvbcanseg | spine/pelvis masks (read) | 0.01 TB | open | 185 | unknown |  |  |
| zenodo_ts_task_hip_implant | spine/pelvis masks (read) | 0.01 TB | open | 71 | unknown |  |  |
| zenodo_ts_task_pleural_effusion | spine/pelvis masks (read) | 0.01 TB | open | 600 | unknown |  |  |
| zenodo_tmtv_benchmark | spine/pelvis masks (read) | 0.01 TB | open | 60 | unknown |  |  |
| ipcai2025_xray_ct | paired CT-XR; fluoro | 0.01 TB | restricted | 5 | no |  | no human spine in view? |
| csi2014 | spine/pelvis masks (read) | 0.01 TB | open | 20 | read | yes |  |
| aariz_cephalograms | spine levels named | 0.01 TB | open |  | read |  |  |
| verse_2d_projections | spine/pelvis masks (read) | 0.00 TB | unknown |  | unknown |  |  |
| scidb_mtddh | spine/pelvis annotation (judged from the record) | 0.00 TB | open | 2,156 | no |  |  |
| csxa | spine levels named | 0.00 TB | open |  | read |  |  |
| nhanes2_annotated | spine levels named | 0.00 TB | open | 364 | read |  |  |
| cadica | fluoro | 0.00 TB | open | 42 | no |  | no human spine in view? |
| geneva_hip | paired CT-XR; spine/pelvis masks (read); fluoro | 0.00 TB | open | 1 | no |  |  |
| ljubljana_2d3d_gs | paired CT-XR; spine/pelvis masks (read); fluoro | 0.00 TB | restricted | 1 | read |  |  |
| veterinary_pig_levelcheck | paired CT-XR | 0.00 TB | open | 1 | no |  | no human spine in view? |
| fraiwan_spine_xray | spine/pelvis annotation (judged from the record) | 0.00 TB | open | 338 | no |  |  |
| aasce | spine levels named | 0.00 TB | restricted |  | read |  |  |
| totalsegmentator | spine/pelvis masks (automatic) | 0.00 TB | open |  | read | yes |  |
| idc_nlst | spine/pelvis masks (automatic) | not held | open | 24,713 | automatic | yes |  |
| hf_abdomenatlas2_0_mini | spine/pelvis masks (read) | not held | restricted |  | unknown |  |  |
| scidb_enhance_pet_1_6k | spine/pelvis masks (read) | not held | open |  | unknown |  |  |
| idc_prostate_anatomical_edge_cases | spine/pelvis masks (read) | not held | open | 131 | unknown |  |  |
| balgrist_lumbar | paired CT-XR; fluoro | not held | unknown |  | unknown |  |  |
| bern_myelography | spine levels named; fluoro | not held | restricted |  | read |  |  |
| bournemouth_cervical_qf | spine levels named; fluoro | not held | restricted | 63 | read |  |  |
| bournemouth_lumbar_qf | spine levels named; fluoro | not held | unknown | 127 | read |  |  |
| cads | spine/pelvis masks (read) | not held | restricted |  | unknown |  |  |
| cams_knee | paired CT-XR; fluoro | not held | restricted | 6 | no |  | no human spine in view? |
| cm_spine_drive_file | spine levels named; fluoro | not held | unknown |  | read |  |  |
| cobra_embargoed | paired CT-XR; spine/pelvis masks (read) | not held | restricted | 175 | unknown |  |  |
| coronary_angiography | fluoro | not held | unknown |  | no |  |  |
| ct_rate | spine/pelvis masks (read) | not held | restricted |  | unknown |  |  |
| daradia_vertebroplasty | fluoro | not held | unknown |  | no |  |  |
| dmx_imaging | fluoro | not held | unknown |  | no |  |  |
| faubel_painsource | fluoro | not held | unknown |  | no |  |  |
| fracatlas | spine/pelvis annotation (judged from the record) | not held | open |  | no |  | no human spine in view? |
| guide3d | fluoro | not held | restricted |  | no |  | no human spine in view? |
| hsg_ais_registry | spine/pelvis annotation (from the record text) | not held | unknown |  | unknown |  |  |
| huashan_fudan | paired CT-XR; spine levels named; fluoro | not held | restricted | 140 | read |  |  |
| jefferson_drg | spine levels named; fluoro | not held | restricted |  | read |  |  |
| kaggle_scoliosis_yolov5 | spine levels named | not held | open |  | read |  |  |
| konica_ddr | fluoro | not held | unknown |  | no |  |  |
| levelcheck_jhu | paired CT-XR; spine levels named; fluoro | not held | restricted | 202 | read |  |  |
| maastricht_cervical | spine levels named | not held | restricted |  | read |  |  |
| magic_ct | spine/pelvis masks (read) | not held | restricted |  | unknown |  |  |
| mayfield_kyphoplasty | fluoro | not held | unknown |  | unknown |  |  |
| mendeley_ddh_hips | spine/pelvis annotation (judged from the record) | not held | open |  | no |  |  |
| mros_lateral_spine | spine levels named | not held | restricted |  | read |  |  |
| mtfi_lumbar_coupling | fluoro | not held | unknown |  | no |  |  |
| neurosurgical_focus_video | spine levels named; fluoro | not held | open |  | read |  |  |
| nit_warangal_nims | paired CT-XR; spine/pelvis masks (read); fluoro | not held | restricted | 9 | read |  |  |
| pediatric_iri | fluoro | not held | unknown |  | no |  |  |
| pittsburgh_swallow | spine levels named; fluoro | not held | restricted | 335 | read |  |  |
| procedure_guide | spine levels named; fluoro | not held | restricted |  | read |  |  |
| pumch_stitching | fluoro | not held | restricted |  | no |  |  |
| radiopaedia | spine levels named; fluoro | not held | restricted |  | read |  |  |
| rsna_ratic | spine/pelvis masks (read) | not held | restricted |  | unknown |  |  |
| seattle_science_foundation | spine levels named; fluoro | not held | unknown |  | read |  |  |
| sof_lateral_spine | spine levels named | not held | restricted |  | read |  |  |
| stanford_aimi_inspect | spine/pelvis masks (read) | not held | restricted |  | unknown |  |  |
| stanford_aimi_merlin | spine/pelvis masks (read) | not held | restricted |  | unknown |  |  |
| sx_stitch | spine levels named; fluoro | not held | unknown |  | read |  |  |
| vanderbilt_tha_fluoro | spine levels named; fluoro | not held | restricted |  | read |  |  |
| veriserum | paired CT-XR; fluoro | not held | restricted |  | no |  | no human spine in view? |
| vertxnet_nhanes2_labels | spine levels named | not held | unknown |  | read |  |  |
| vfss2022 | fluoro | not held | unknown |  | no |  |  |

### Candidate: ct render source (54)

| Set | Rules met | Held | Licence | People | Level truth | Prior source | Flags |
|---|---|---|---|---:|---|---|---|
| idc_ldct_and_projection_data | - | 0.86 TB | open | 99 | unknown |  |  |
| tcia_fdg_pet_ct_lesions | - | 0.39 TB | open | 900 | automatic | yes |  |
| aws_stoic2021 | - | 0.26 TB | restricted | 2,000 | unknown |  |  |
| panorama | - | 0.19 TB | restricted | 1,950 | automatic | yes |  |
| ribfrac | - | 0.16 TB | restricted |  | no | yes |  |
| amos22 | - | 0.10 TB | open | 2,200 | automatic | yes |  |
| idc_nsclc_radiogenomics | - | 0.09 TB | open | 188 | unknown |  |  |
| kidney_thoraxabdomen | - | 0.08 TB | open | 215 | automatic | yes |  |
| idc_covid_19_ny_sbu | - | 0.06 TB | open | 443 | automatic | yes |  |
| idc_psma_pet_ct_lesions | - | 0.06 TB | open | 374 | automatic | yes |  |
| waw_tace | - | 0.05 TB | open | 233 | automatic | yes |  |
| idc_cptac_luad | - | 0.04 TB | open | 32 | unknown |  |  |
| idc_eay131 | - | 0.04 TB | open | 376 | automatic | yes |  |
| curvas | - | 0.03 TB | open | 90 | automatic | yes |  |
| idc_lung_pet_ct_dx | - | 0.03 TB | open | 158 | automatic | yes |  |
| idc_cptac_lscc | - | 0.03 TB | open | 32 | unknown |  |  |
| idc_mediastinal_lymph_node_seg | - | 0.03 TB | open | 316 | automatic | yes |  |
| barts_crl | - | 0.02 TB | open | 220 | automatic | yes |  |
| idc_rider_lung_pet_ct | - | 0.02 TB | open | 117 | automatic | yes |  |
| aortaseg60 | - | 0.02 TB | open | 60 | automatic | yes |  |
| idc_acrin_nsclc_fdg_pet | - | 0.02 TB | open | 131 | automatic | yes |  |
| idc_cptac_ucec | - | 0.01 TB | open | 66 | automatic | yes |  |
| idc_tcga_blca | - | 0.01 TB | open | 79 | automatic | yes |  |
| idc_cptac_pda | - | 0.01 TB | open | 62 | automatic | yes |  |
| idc_cmb_lca | - | 0.01 TB | open | 75 | automatic | yes |  |
| idc_tcga_kirc | - | 0.01 TB | open | 129 | automatic | yes |  |
| idc_midrc_ricord_1b | - | 0.01 TB | restricted | 91 | unknown |  |  |
| idc_cptac_ccrcc | - | 0.01 TB | open | 48 | automatic | yes |  |
| idc_cptac_stad | - | 0.01 TB | open | 19 | automatic | yes |  |
| idc_midrc_ricord_1a | - | 0.01 TB | restricted | 98 | automatic | yes |  |
| idc_tcga_stad | - | 0.01 TB | open | 45 | automatic | yes |  |
| idc_colorectal_liver_metastases | - | 0.01 TB | open | 80 | automatic | yes |  |
| idc_ctpred_sunitinib_pannet | - | 0.01 TB | open | 34 | automatic | yes |  |
| idc_covid_19_ar | - | 0.01 TB | open | 23 | automatic | yes |  |
| idc_varepop_apollo | - | 0.01 TB | open | 35 | automatic | yes |  |
| idc_cmb_crc | - | 0.01 TB | open | 30 | automatic | yes |  |
| idc_hcc_tace_seg | - | 0.01 TB | open | 101 | automatic | yes |  |
| idc_tcga_lihc | - | 0.00 TB | open | 42 | automatic | yes |  |
| idc_pelvic_reference_data | - | 0.00 TB | open | 58 | automatic | yes |  |
| idc_anti_pd_1_lung | - | 0.00 TB | open | 34 | automatic | yes |  |
| idc_cptac_cm | - | 0.00 TB | open | 12 | automatic | yes |  |
| idc_tcga_ucec | - | 0.00 TB | open | 38 | automatic | yes |  |
| idc_adrenal_acc_ki67_seg | - | 0.00 TB | open | 29 | automatic | yes |  |
| idc_cptac_sar | - | 0.00 TB | open | 14 | automatic | yes |  |
| idc_pancreatic_ct_cbct_seg | - | 0.00 TB | open | 40 | automatic | yes |  |
| idc_acrin_flt_breast | - | 0.00 TB | open | 15 | automatic | yes |  |
| idc_cmb_brca | - | 0.00 TB | open | 21 | automatic | yes |  |
| idc_tcga_esca | - | 0.00 TB | open | 16 | automatic | yes |  |
| idc_tcga_ov | - | 0.00 TB | open | 24 | automatic | yes |  |
| idc_cmb_mml | - | 0.00 TB | open | 16 | automatic | yes |  |
| idc_cmb_mel | - | 0.00 TB | open | 23 | automatic | yes |  |
| idc_ct_vs_pet_ventilation_imaging | - | 0.00 TB | open | 20 | automatic | yes |  |
| idc_cmb_ov | - | 0.00 TB | open | 7 | automatic | yes |  |
| idc_lidc_idri | - | not held | open | 997 | unknown |  |  |

### Candidate: spine in view, no labels (9)

| Set | Rules met | Held | Licence | People | Level truth | Prior source | Flags |
|---|---|---|---|---:|---|---|---|
| nhanes2_unannotated | - | 0.14 TB | open |  | no |  |  |
| kub_stonex | - | 0.06 TB | open | 1,703 | no |  |  |
| ieee_dataport_lateral_236 | - | not held | unknown | 236 | no |  |  |
| kaggle_fracture_multiregion | - | not held | open |  | no |  | no human spine in view? |
| canine_thoracic_vhs | - | not held | open |  | no |  | no human spine in view? |
| tvgh_as_spine_xray | - | not held | unknown |  | unknown |  |  |
| tvgh_spinexr | - | not held | unknown |  | unknown |  |  |
| vindr_cxr | - | not held | restricted |  | no |  |  |
| vindr_pcxr | - | not held | restricted |  | no |  |  |

### Exclude candidate (8)

| Set | Rules met | Held | Licence | People | Level truth | Prior source | Flags |
|---|---|---|---|---:|---|---|---|
| nih_chestxray14 | - | 0.05 TB | unknown | 30,805 | no |  |  |
| rexgradient_160k | - | 0.00 TB | restricted | 109,487 | no |  |  |
| bimcv_covid19 | - | not held | unknown |  | no |  |  |
| brax | - | not held | restricted |  | no |  |  |
| chexpert_plus | - | not held | restricted | 65,240 | no |  |  |
| mimic_cxr | - | not held | restricted | 65,379 | no |  |  |
| open_i_chest | - | not held | restricted |  | no |  |  |
| padchest | - | not held | restricted | 67,625 | no |  |  |
