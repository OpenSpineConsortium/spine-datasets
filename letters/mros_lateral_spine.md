# mros_lateral_spine: the request text

Not sent.

To: the MrOS coordinating centre (San Francisco Coordinating Center, UCSF), through the data request portal at https://mrosonline.ucsf.edu/.
Route: web form, with an account first; the proposal is filed in the owner's name and the data use agreement that follows is the owner's hand only.

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, derived from SchwingNet's docs/research/xray-dataset-requests.md (the request texts, copied verbatim), docs/research/data-access-requirements.md (who may act) and data/sources/<id>.json (the record). The text below is that file's, verbatim, headings included; the numbered section is the one it holds there. The rules every text follows and the sender block are in letters/TEMPLATE.md; the shared blocks it names (the project title, the lay summary, the data security, IRB, analysis plan and credit paragraphs) are there too.

## 1. MrOS lateral spine radiographs (UCSF)

Page to open: https://mrosonline.ucsf.edu/ (to confirm; the sweep names it as the study's data
request portal). MrOS Online is run by the San Francisco Coordinating Center; the images are not on
dbGaP, whose phs000373 holds genotypes. Expect an account to create first, then a "proposal" or
"analysis request" form; some cohort portals also ask for a short CV. To confirm on the page.

Fields the form is likely to ask, and the text for each:

- Proposal title: the shared title above, or the MrOS-specific one:

```text
Vertebral-level recognition on lateral spine radiographs of older men: reliability of automated identification across six clinical sites and two visits
```

- Background and aims:

```text
I study the application of computer science to improving spinal health, and my current work needs lateral thoracic and lumbar radiographs of older men in which each vertebra has already been named and graded by an expert. Wrong-level errors in spine care arise where the vertebra counted on an image is not the vertebra it was taken for, and they are commonest exactly where MrOS films are richest: osteoporotic spines with compression fractures, kyphosis and degenerative change, which is the anatomy an operating-room C-arm shows during vertebral augmentation and fixation. The Genant semi-quantitative grades of MrOS sit on named levels, so each film carries a per-vertebra level truth of a kind no other public radiograph set of this size has. The aim is to measure how reliably automated image-analysis methods recognise which vertebra is which on these films, across the six sites' devices and the two visits, and how the reliability changes with fracture grade, and to report per-image agreement with the expert labels and confidence intervals by site, visit and grade.
```

- Data requested (name the files, not the outcomes):

```text
The lateral thoracic and lumbar spine radiograph images from the baseline visit and the second spine-film visit, in the original or highest available resolution (DICOM where it exists); the vertebral-level reading tables for those films (the Genant semi-quantitative grade and any prevalent or incident fracture flag per vertebra, with the vertebra's name and any note of non-evaluable levels or transitional anatomy); and the image metadata (site, visit, acquisition date or interval, device or film type, and pixel spacing or calibration). No clinical outcome, questionnaire, laboratory, DXA or genotype variable is requested; a participant key is needed only to join the films to the reading tables and to keep the same man's two visits together.
```

- Analysis plan: the shared block.
- IRB status: the shared block.
- Data security: the shared block.
- Publication and acknowledgement: the shared block, plus the sentence "I will follow MrOS's
  publication and authorship policy and submit any manuscript for the required review."
- Funding: "No external funding; departmental support." (to confirm what the form wants.)

Binding, the owner's hand only: the MrOS data use agreement (an institutional signature is usual
for cohort data; Wayne State's sponsored programs office may have to countersign), any fee the
portal names (none is known; to confirm on the page), and the account itself.

What to expect back: a review by the MrOS publications or data committee, typically weeks; a
signed agreement; then a download link or a shipped drive for the images, since the film set is
large, and the reading tables as CSV with a data dictionary. Some cohort portals grant tabular data
through the site and ask for a separate request for images; if so, send the data-requested text
above as the image request.
