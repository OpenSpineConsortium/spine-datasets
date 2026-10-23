# Contributing: what you may do alone, what is the owner's, how a result is recorded

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, derived from SchwingNet's
docs/research/xray-dataset-requests.md (whose "Rules every text follows" is copied below) and
docs/research/data-access-requirements.md (the section "Who acts").

## The confidentiality rule, first

No letter, form text, issue, comment or pull request in this repository may say or imply that a
neural network, a model, machine learning, deep learning, AI or training is built or used. The
work is described only as measuring and improving how reliably automated image-analysis methods
recognise spinal anatomy (which vertebra is which, transitional variants included, the variants
behind wrong-level errors) across modalities, devices and exposures, with results reported as
per-image agreement with expert labels and confidence intervals. Before sending anything, read the
text once more for those words: neural network, model, machine learning, deep learning, AI,
training, and also detector and classifier. A text that needs one of them is wrong, not the rule.
The reason is patent confidentiality; it holds whoever the sender is and whatever the source
already knows.

## The rules every letter follows

Copied from SchwingNet's docs/research/xray-dataset-requests.md, "Rules every text follows":

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

A collaborator's letter says "I work with Dr Gregory Schwing at the Department of General Surgery,
Wayne State University ..." in place of "I am at ...", and "read only by the study team" in place of
"read by me alone", as letters/TEMPLATE.md shows; everything else holds word for word.

## What a collaborator may do alone

- Write a letter on the template (letters/TEMPLATE.md) or send the text already written for the
  dataset (letters/<id>.md), from your own institutional mailbox, with go2432@wayne.edu in copy,
  once the task is yours. The letter asks for the terms; it accepts none.
- Fill a web form that asks nothing binding: a name, an institution, an email, a purpose. The
  purpose text is the dataset's letter file or the template's paragraphs.
- Bring a plain download onto the grid, once the licence or the grant allows it and the task
  says so, by a pull request with a manifest (manifests/README.md): the file list with every
  file's link, size and checksum. The required check reviews it, the owner merges it, and the
  promoter, running as the owner's grid account, fetches it into the read-only shared tree and
  opens the record's update. Nobody but the promoter writes /rs/rs_grp_oschome/shared/datasets,
  so no collaborator needs, or asks for, write access there.
- Read a page the owner could not reach and write what it says into the record (the licence line,
  the count, the form's real fields), replacing "to confirm on the page".
- Post the result on the task and in the record, and finish the pull request.

## What is the owner's hand only

Any signature on a data use, transfer or licence agreement; any fee; any attestation or
credentialing; any licence checkbox or click-through that binds the person who ticks it; any
account that asks for the owner's identity (PhysioNet, Stanford AIMI, IEEE DataPort, MrOS and SOF
Online, Hugging Face gates, Kaggle); any token or credential; the IRB and lawyer questions; and
the word for a grid job that takes space the project has not yet budgeted. When a task reaches one
of these, comment "needs the owner" on it with exactly what is needed and the link to click,
record it in the result field, and hand the task back: take off your `worker:` label, leave the
branch and the draft pull request with the comment "finished; ready to mark", and the owner takes
it from there.

## The automated review

Every pull request runs tools/dataset_review.py as part of the required check. It fails on a
word the confidentiality rule bans in an added line of a record, a manifest or a letter, or in the
pull request's title or description; on a record whose history lost an entry; on a data file
added to the repository; on a token in the title or description; on a manifest that breaks
manifests/README.md's rules; and on a change to the promoter's own code (tools/promote.py,
grid/promote.sh, grid/promote.json) in a pull request the owner did not open, since that code runs
as the owner on the grid. It flags, for whoever merges, a line that reads as something binding
done in the owner's name, a licence or link changed other than by replacing "to confirm", and a
non-commercial or no-derivatives licence, which needs a grant before it is fetched. Its report is
on the check's summary page.

## The review record

The same required check runs tools/review_record.py, which holds every pull request marked ready,
yours, the owner's and every Claude session's alike, to a section headed `## Adversarial review`
in its description: what someone who wanted the change to fail checked, by reading it or by running
it, what they found and what was fixed. It is at least a sentence; "LGTM" does not count, and the
pull request template has the heading. A draft, a bot's pull request, the promoter's promote/
branches and a pull request opened before 2026-10-22 05:00 UTC are not asked for one. Editing the
description runs the check again; "Re-run" on an old run reads the description as it was, so edit it
or push instead. The organization's ruleset also asks one approval, given after the last push, of a
pull request from anyone but an organization owner. symphony-template's
docs/research/same-ci-for-every-contributor.md says which rules GitHub enforces on everyone and why.

## How to record a result on the task

One comment on the issue and the same line in datasets/<id>.json's `result` field, dated, in one
of the shapes README.md lists (on the grid at <path> with the job id; requested, waiting; granted,
fetch pending; refused, with the reason; needs the owner). Set `status` to the matching word
(fetched, requested, granted, refused, needs-owner, or held for a set the owner's own chain put on
the grid, with `grid_path` saying where under the owner's grid root or home or the shared tree,
which the review flags for whoever merges to check against a status listing), add one entry to the
record's `history` (the date, the step, one line) and rewrite its `obstacles` and `next`, so the
pipeline board (PIPELINE.md on the branch `pipeline`) shows the move, and keep the record's
licence and link exactly as they are. A fetch through the promoter leaves PROMOTED.json beside
raw/, and the promoter's own pull request records the result, so a manifest's pull request stops
at `fetching`. The pull request carries the record change and nothing of the data: no image, no
listing of patient identifiers, no token, no address of a private person beyond what a public page
prints.

## How to ask for a new task

Open an issue with the Task form the template brings, with the dataset's name, its link, what it
holds (modality, region, count, labels, as the page states them) and why it matters to the
measurement, and name under "Files likely touched" the record and letter files it will have:
datasets/<id>.json and letters/<id>.md. Label it todo; the board lists it and anyone may claim it.
A dataset already in datasets/ needs no new task; comment on its task instead.

## What never goes into this repository

Nothing public leaves it. No secret, token, cookie, key or presigned link in any file. No personal
data of students (no name, login or email of a student anywhere); the owner's own address
go2432@wayne.edu and the sender block's number are the one exception. No image and no file from a
dataset: the data live on the grid, the record here says where.
