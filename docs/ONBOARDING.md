# Onboarding: what a new collaborator sets up, once

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, written when the first
collaborators were invited. Read this page first, then CONTRIBUTING.md; everything else is linked
from here. The owner is Dr Gregory Schwing (GitHub Gregory-Schwing-MD-PhD, go2432@wayne.edu).

The idea in one paragraph: this repository lists every spine imaging dataset the registry names
that is not yet on Wayne State's grid, one task per dataset. You take a task, your own Claude does
the drafting and the record keeping, you send the letter or fill the form from your own mailbox or
fetch the download as a grid job, and the result goes on the task. You bring your own accounts;
nothing of yours is ever stored here, and nothing of the owner's is lent to you.

## 1. Accounts you need

| What | Why | How to get it |
|---|---|---|
| A GitHub account with Write on this repository | every claim is a branch pushed here | accept the invitation GitHub emailed you (or open https://github.com/OpenSpineConsortium/spine-datasets/invitations); if the invitation went to an email with no GitHub account, make one with that email first, then accept |
| A Claude plan of your own, Pro or Max | your sessions run on your own plan, never on anyone else's token | https://claude.ai/upgrade; Max if you will run several sessions at once |
| A Wayne State AccessID with a grid account | downloads land on the grid, never on a laptop; letters go from an institutional mailbox | the owner requests the grid account for you; you hear from Wayne State's research computing group when it exists |
| Beethoven access (the grid worker in Chrome) | runs Claude Code on the grid for you, so fetch jobs are submitted from there | tell the owner the Google account you use in Chrome; the invitation to Beethoven's private Chrome Web Store page goes to it (section 5) |
| Google Authenticator set up for the grid | the grid asks a 6-digit code at every sign-in | Beethoven shows the steps the first time; it needs GlobalProtect (Wayne State's VPN) once |

You can start on the tasks that need no grid at all (letters, forms, reading a page) as soon as the
first two rows are done.

## 2. Claude Code, three ways to run it

Any one of these is enough; most people use the first and the second.

1. **In the browser, no install**: https://claude.ai/code, press Sign in with GitHub, pick this
   repository and start a session. Make a cloud environment of your own when it asks (the defaults
   are fine). A session here already reads CLAUDE.md, the protocol and the board.
2. **A thin Project of your own** (Pro and Max): at https://claude.ai/code make a Project, link
   OpenSpineConsortium/spine-datasets as its only resource, leave its instructions and memory
   blank, and name it after the repository and yourself. Each thread is then a cloud session on a
   fresh clone. docs/setup/claude-project.md says why the fields stay blank.
3. **On your own computer**: install Claude Code (https://code.claude.com/docs/en/quickstart), run `claude`
   in a clone of the repository and sign in as yourself. You also need `gh auth login` with your
   GitHub login, git and Python 3.12 or later.

Your sessions claim under your GitHub login; the label `worker:<your login>` appears on the board
the first time you claim. No file needs to be added for you.

## 3. Picking a task

The board is the file STATE.md on the branch `board`:
https://github.com/OpenSpineConsortium/spine-datasets/blob/board/STATE.md. Its Queue lists every
task nobody holds; a task labelled `worker:<your login>` is given to you and comes first. The tasks
are the issues titled "Obtain <dataset>", numbered by priority group in tasks/TASKS.md; group 1 is
the most useful first. Take one whose route you can do:

- `letter` or `form`: anyone with an institutional mailbox (sections 4 and 6).
- `download`: anyone with a grid account and Beethoven (section 5), once the record's licence
  allows it.
- `account`, `agreement` or `owner-only`: these need the owner's identity or signature; leave them
  unless the task says what a collaborator can do first (reading the terms, finding the contact).

## 4. Claiming and finishing a task with your Claude

Paste this into a session, with the issue's number for N:

```
Claim issue N with the claim skill and carry it to a ready pull request, as docs/agents/PROTOCOL.md says; work on the branch claude/N, not this session's own branch. If the push of claude/N is refused, another session holds the issue: say so in one line and stop. Do not merge.
```

In a cloud session or a Project thread add this line after it, since gh issue and gh pr are
refused there:

```
gh issue and gh pr are refused here, so add the labels, post the plan and open the draft pull request with your GitHub tools or gh api (repos/OpenSpineConsortium/spine-datasets/issues/N/labels, repos/OpenSpineConsortium/spine-datasets/issues/N/comments, repos/OpenSpineConsortium/spine-datasets/pulls). Mark the pull request ready with your GitHub tool update_pull_request (draft false), not gh api, which cannot change a draft; if you have no such tool, comment "finished; ready to mark" on the pull request and stop before you delete the claim file.
```

What the session does: pushes the branch `claude/N` (the first push is the claim; a second push of
the same name is refused, so two people never hold one task), labels the issue, posts the plan,
opens a draft pull request that says "Closes #N", then does the work: drafts the letter from
letters/<id>.md or letters/TEMPLATE.md for you to send, or writes the form text, or writes the
grid job for you to submit. You do the part only a person can do (section 6), tell the session
what happened, and it records the result in datasets/<id>.json and on the task, in one of the
shapes README.md lists, deletes the claim file and marks the pull request ready. The owner merges;
the merge closes the task. A result that is "waiting" keeps the task open, as README.md says.

Other prompts, for a rebase after "main moved" or a checkpoint, are in docs/start/prompts.md. A
session never sends mail, ticks a box or pays anything: it drafts, you act.

## 5. The grid and Beethoven, for downloads

A plain download is a Slurm job on your own grid account, landing at
/rs/rs_grp_oschome/shared/datasets/<id>/raw with its checksums (grid/README.md has the job's
shape). Nothing runs on the login node, and nothing lands on a laptop. The way in is Beethoven, a
Chrome extension that starts a Claude Code worker in your own Claude account on the grid and opens
it at claude.ai:

1. Open the invitation to Beethoven's private Chrome Web Store page in Chrome, signed in to the
   Google account it was sent to, and press Add to Chrome. Pin it.
2. The first time: agree to the terms, install the small helper it offers (it lets Beethoven
   reach the grid without GlobalProtect; it needs no administrator) or choose GlobalProtect,
   type your AccessID, your grid password and the Google Authenticator code when the grid asks.
   If you have no grid code yet, Beethoven shows how to set one up (it needs GlobalProtect once).
3. Press Connect; the worker starts as a grid job and Beethoven shows Online with Open my
   session. Sign in to Claude with your own account when it asks.
4. In that session, clone this repository on the grid and claim the task as in section 4; the
   session writes the job file, you submit it (`sbatch`), and the job's log and FETCH.json are
   the result.

Beethoven's full guides, Install and Use, come with the invitation; the owner's reference copies
are in spine-program under 11_students_grid_access/docs/beethoven/guides/. Your access to the
shared volume is a named entry on /rs/rs_grp_oschome that the owner's approval adds; until it is
there, a job cannot write to the landing folder, and the task waits.

## 6. Letters and forms, from your own mailbox

A letter goes from your own institutional mailbox, never from a personal one and never from a
session, with go2432@wayne.edu in copy and the subject tag "[XR/CT Imaging Research]". Use the
text in letters/<id>.md where one exists, else fill letters/TEMPLATE.md; a collaborator's letter
says "I work with Dr Gregory Schwing at the Department of General Surgery, Wayne State University
...". A form that asks nothing binding (name, institution, email, purpose) you may fill yourself,
with the letter's paragraphs as the purpose. Before sending, read the text once more for the words
the confidentiality rule bans (section 8).

## 7. What stays the owner's hand

Any signature on a data use or licence agreement, any fee, any attestation, any licence checkbox
that binds the person ticking it, any account in the owner's name (PhysioNet, Stanford AIMI, IEEE
DataPort, Hugging Face gates, Kaggle), any token or credential, the IRB and lawyer questions, and
the word for a grid job that takes space not yet budgeted. When your task reaches one of these,
comment "needs the owner" on it with exactly what is needed and the link, and hand it back as
CONTRIBUTING.md says.

## 8. The two rules you must not break

- **Confidentiality.** No letter, form, issue, comment or pull request says or implies that a
  neural network, a model, machine learning, deep learning, AI or training is built or used, nor
  "detector" or "classifier". The work is described only as measuring and improving how reliably
  automated image-analysis methods recognise spinal anatomy. The reason is patent confidentiality;
  it holds whatever the source already knows.
- **Nothing private in the repository.** No token, password, key, cookie or presigned link in any
  file; no image or file from a dataset; no name, login or email of a student in any file (the
  owner's address is the one exception). A session that is given a token puts it in a file on the
  grid with mode 0600, never on a command line or in a job file, and never in a commit.

## If something is in the way

Comment on the task: the owner and every session read the issues. A question about the repository
itself goes in a new issue with the Task form.
