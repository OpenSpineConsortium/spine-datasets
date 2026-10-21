# spine-datasets: obtaining, together, every dataset not yet on the grid

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, and the SchwingNet files
it was derived from: docs/research/data-access-requirements.md (the unheld sources and who may act
on each), docs/research/xray-datasets-missing.md (the sweep of 2026-10-21),
docs/research/xray-dataset-requests.md (the request texts), data/sources/*.json (the registry) and
grid/README.md (the fetch chain). This repository is private and stays private.

## What this repository is for

Wayne State's grid holds 26 of the 111 imaging sources the spine registry lists. The other 85, and
five intraoperative sets the literature names without a record, are spine and related imaging
datasets that exist somewhere behind a download, a form, an account, a letter or an agreement. This
repository is where the owner, Ashley and every other collaborator obtain them together: one task
per dataset, claimed and worked by the Symphony protocol that the template brings (CLAUDE.md,
docs/agents/PROTOCOL.md), with Claude sessions doing the drafting and the grid doing the fetching.
Where a dataset cannot be obtained, the task records why, so nobody asks twice.

What is here:

- datasets/: one record per dataset not yet held, copied from SchwingNet's registry with three
  fields added (route, status, result); datasets/README.md says what each field means.
- letters/: the request texts already written, one file per dataset, each saying who it goes to,
  by what route and whether it was sent; letters/TEMPLATE.md is the fill-in letter for any
  dataset without one, with the rules every letter follows.
- tasks/: tasks/TASKS.md lists the task for every dataset in priority order, and
  tasks/open_tasks.py opens them as issues once the repository exists.
- grid/: how a collaborator with a grid account fetches a plain-download set onto the shared
  volume, and what nobody does.
- CONTRIBUTING.md: what a collaborator may do alone, what is the owner's hand only, how a result
  is recorded, how to ask for a new task, and the confidentiality rule.

## How a collaborator joins, in five steps

New here? docs/ONBOARDING.md is the longer version of these five steps: the accounts to get,
Claude Code, Beethoven for the grid, the prompts to paste and what stays the owner's hand.

1. Accept the invitation to the repository (an email from GitHub; the owner invites by GitHub
   login). Read CONTRIBUTING.md once.
2. Open the board: the file STATE.md on the branch `board` (on GitHub, switch the branch to
   `board` and open STATE.md), or the control panel the owner links in the invitation. It lists
   every task, who holds it and what is free.
3. Pick a task labelled todo that nobody holds: no `worker:<name>` label but yours, no branch
   `claude/<issue>` on origin, not an epic, not labelled blocked. A task given to you by name
   comes first.
4. Claim it by the protocol: a Claude session runs the claim skill (.claude/skills/claim); a
   person pushes a branch `claude/<issue number>` from the default branch whose first commit adds
   docs/agents/claims/<issue number>.md (the template's shape), adds the labels claimed and
   `worker:<your login>`, posts the plan as a comment, and opens a draft pull request that says
   "Closes #<issue>". The first push of the branch is the claim; a second push of the same name is
   refused, so two people never hold one task.
5. Do the route the task names (a letter from your own mailbox, a form, a download as a grid
   job), post the result on the task, update datasets/<id>.json, delete the claim file, mark the
   pull request ready. The owner merges, and the merge closes the task.

## What a task's result looks like

The result is one line in the task's comment and in the record's `result` field, in one of these
shapes, with the date:

- on the grid at /rs/rs_grp_oschome/shared/datasets/<id>/raw, job id <N>, <bytes> bytes, checksums
  verified (the FETCH.json beside the download says the rest);
- requested on <date> by <who>, to <whom>, waiting;
- granted on <date>, fetch pending (and what the fetch needs: a link, a token file, a space
  decision);
- refused on <date>, with the reason the source gave;
- needs the owner: a signature, a fee, an attestation, a licence checkbox or an account in the
  owner's name (the task is labelled with a comment "needs the owner" and handed back).

A result that is "waiting" keeps the task open: the branch stays, the pull request stays a draft
with the comment "finished; ready to mark" so the protocol does not release the claim, and the
answer, when it comes, is the next result.

## The rules in one breath

Nothing public; no credential in any file; no personal data of students; images stay on the grid;
every letter under the rules in letters/TEMPLATE.md; anything binding is the owner's hand; and no
text ever says what is built, only what is measured (CONTRIBUTING.md).

## The template underneath

The repository was made from OpenSpineConsortium/symphony-template, which brings the claim protocol, the board, the checks and the workflows. docs/start/README.md says how the template works and docs/setup/ how it is set up; the "Set up this project" issue lists what is left to do.
