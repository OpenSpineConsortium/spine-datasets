# mimic_cxr: the request text

Not sent.

To: PhysioNet, the MIMIC-CXR-JPG record page.
Route: the data use agreement click for this dataset on the owner's credentialed PhysioNet account, the owner's hand only.

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, derived from SchwingNet's docs/research/xray-dataset-requests.md (the request texts, copied verbatim), docs/research/data-access-requirements.md (who may act) and data/sources/<id>.json (the record). The text below is that file's, verbatim, headings included; the numbered section is the one it holds there. The rules every text follows and the sender block are in letters/TEMPLATE.md; the shared blocks it names (the project title, the lay summary, the data security, IRB, analysis plan and credit paragraphs) are there too.

## 7. MIMIC-CXR-JPG (PhysioNet, credentialed)

Page to open: https://physionet.org/content/mimic-cxr-jpg/2.1.0/ (and
https://physionet.org/content/mimic-cxr/2.1.0/ for the DICOM). The owner already holds PhysioNet
credentialing (the CITI course on file) and signed the VinDr-SpineXR agreement, so this needs only
the per-project step: on the record page, "Sign the data use agreement" for this dataset, which is
PhysioNet's standard credentialed health data agreement, plus, for MIMIC, the required-course
line, which the existing CITI course satisfies.

Fields: none beyond the agreement; the credentialing application already holds the reference and
the research summary. If PhysioNet asks for a project description on re-credentialing, paste the
shared aims block.

Binding, the owner's hand only: the DUA click, which attests to the terms for this dataset alone.
Fee: none. What to expect back: access at once; the files (about 570 GB of JPG) are fetched with
`wget --user` or the AWS mirror as a grid job on the owner's word, and the lateral share is read
from mimic-cxr-2.0.0-metadata.csv (ViewPosition) before anything else is downloaded. The IRB
supplement HPR 2026-330 names VinDr-SpineXR; whether it covers a second PhysioNet set or needs a
line added is a question for the IRB office before the images are read, not before the click.
