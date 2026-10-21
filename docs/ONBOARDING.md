# Onboarding: set yourself up exactly as the owner is set up

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, written when the first
collaborators were invited; the Beethoven steps follow spine-program's student onboarding guide of
2026-10-13 and Beethoven's own Install and Use guides. Read this page first, then CONTRIBUTING.md.
The owner is Dr Gregory Schwing (GitHub Gregory-Schwing-MD-PhD, go2432@wayne.edu).

The idea in one paragraph: this repository lists every spine imaging dataset the registry names
that is not yet on Wayne State's grid, one task per dataset. You take a task, your own Claude does
the drafting and the record keeping, you send the letter or fill the form from your own mailbox,
or fetch the download as a grid job, and the result goes on the task and on the pipeline board.
You bring your own accounts; nothing of yours is ever stored here, and nothing of the owner's is
lent to you.

The owner's own setup, which this page reproduces for you, is six things: a GitHub login with
Write here; a Claude Pro or Max plan; a claude.ai Project (the Projects beta) with this
repository as its only resource, where every thread is a Claude Code session on a fresh clone;
Beethoven in Chrome, which runs Claude Code on the grid in your own account; Claude in Chrome,
which lets a session use your browser; and the Symphony control panel, the web page that drives
this repository (the board, the tasks, the pull requests) as you. Sections 1 to 6 set them up in
that order; 7 to 10 are how the work goes.

## 1. Accounts, in the order to ask for them

Ask for the grid account first, since it takes the longest; everything else is minutes.

| What | Who provides it | What you do | Cost |
|---|---|---|---|
| A GitHub account with Write on OpenSpineConsortium/spine-datasets | the owner invites your login or your email | accept the invitation GitHub emailed you, or open https://github.com/OpenSpineConsortium/spine-datasets/invitations; if the invitation went to an email with no GitHub account, make one at https://github.com/signup with that email, then accept | free |
| Claude Pro or Max | you | https://claude.ai/upgrade, your own account; Claude Code is not in the free plan; Max if you will run several threads at once | Pro about US$20 a month, paid by you |
| A Wayne State grid account | Wayne State C&IT | https://tech.wayne.edu/kb/high-performance-computing, naming Gregory Schwing as sponsor (the owner has submitted the request for the first collaborators); about two business days; questions to hpc@wayne.edu | free |
| The grid's sign-in code (Google Authenticator) | you, once | install Google Authenticator on your phone; connect GlobalProtect (https://protect.wayne.edu) once; open https://ondemand.grid.wayne.edu, Interactive Apps, 2FA Setup, scan the code. Beethoven walks you through it too | free |
| Beethoven invitation and the lab volume's access list | the owner | send the owner the Google address your Chrome is signed in to; the owner adds it to Beethoven's testers group (the invitation to its private Chrome Web Store page arrives by email) and adds your AccessID to /rs/rs_grp_oschome's access list, without which every lab path answers Permission denied | free |

Two authenticator apps end up on your phone: Google Authenticator holds the grid's code, Microsoft
Authenticator approves every other Wayne State sign-in, GlobalProtect included.

## 2. Your Claude Project (once, five minutes)

A Project is your own front door to the repository: every thread you open in it starts from a
fresh clone of main and reads CLAUDE.md, the protocol, the memory and the board from the clone.
Projects are the beta on Pro and Max at https://claude.ai/code; if the sidebar there has no
Projects entry yet, the rollout has not reached your account, and section 3's first way works the
same.

1. Sign in at https://claude.ai/code with your own Claude account. Open Projects
   (https://claude.ai/code/projects/browse) and press New project. Call it spine-datasets.
2. Connect your GitHub account when asked, then add OpenSpineConsortium/spine-datasets as the
   Project's only repository. The Claude GitHub App is already on it; if claude.ai sends you to
   GitHub to install it, pick this repository.
3. Leave the Project's instructions, description and memory blank. Everything a thread needs is
   in the repository, so nothing typed there can drift from what the owner's own threads read
   (docs/setup/claude-project.md says why).
4. Open a first thread and type /board. The board that prints is the live state of the
   repository: the Queue, the claims, the pull requests, the overlaps.

A Project belongs to one account and cannot be shared, so you and the owner each have your own;
the repository is the one thing you share, and both sides see the same issues, branches and pull
requests.

## 3. Two other ways to run Claude Code

- **A cloud session without a Project**: https://claude.ai/code, Sign in with GitHub, pick this
  repository, start a session; make a cloud environment of your own when it asks.
- **On your own computer**: install Claude Code (https://code.claude.com/docs/en/quickstart),
  clone the repository, run `claude` in its top folder and sign in as yourself; `gh auth login`
  with your GitHub login, git and Python 3.12 or later. Then, once,
  `claude plugin install symphony@symphony-marketplace --scope project`, which brings /board,
  the claim skill and the push guard (the Symphony plugin, from
  https://github.com/OpenSpineConsortium/symphony-marketplace). On Windows, `python3 --version`
  must print a version in Git Bash, or the push guard silently does nothing.

Your sessions claim under your GitHub login wherever they run; the label `worker:<your login>`
appears on the board the first time you claim. No file needs to be added for you.

## 4. Beethoven: Claude Code on the grid (once, ten minutes plus the wait for a node)

Beethoven is a Chrome extension that starts a Claude Code worker in your own grid account, as a
Slurm job, and opens it in claude.ai. It is how your Claude reaches the data and submits fetch
jobs; nothing ever runs on the login node. The full guides, Install and Use, come with the
invitation; the owner's reference copies are in spine-program under
11_students_grid_access/docs/beethoven/guides/.

1. Wait for the grid account (section 1) and for the owner's word that your AccessID is on the
   lab volume's access list.
2. Set up the grid's sign-in code if you have none (section 1, row 4). Beethoven's panel offers
   the same steps.
3. Open the Beethoven invitation in Chrome, signed in to the Google account it was sent to, and
   press Add to Chrome, then Add extension. Pin it with the puzzle icon. If the page shows no
   item, Chrome is signed in to another Google account.
4. On the welcome page read the terms, tick the box and press Agree and continue. When the panel
   says One small download, once, install the helper for your system (it lets Beethoven reach
   the grid without GlobalProtect; no administrator needed; your computer warns once because it
   is unsigned, which is expected). If your computer refuses it, press Use GlobalProtect instead.
5. Sign in to the grid in the panel: your AccessID, your password, then the six-digit code from
   Google Authenticator (not Microsoft Authenticator). The panel says This computer is set up.
6. Read Where your work goes, tick the box and press Connect. A Claude tab opens: sign in with
   your own Claude account and approve.
7. The panel says In line for a computer, then Online. Press Open my session. That session is
   Claude Code running on a compute node in your account; it is also a session of your own
   claude.ai, so it shows there like any other.

Every later day is two presses: open Beethoven, press Connect or Open my session. If the panel
looks stuck (Connecting to Claude, or the grid did not accept the code), open More, Copy debug
log, and send it to the owner rather than retrying: three refused codes lock you out for fifteen
minutes.

## 5. Claude in Chrome: your browser for a session

Claude in Chrome is Anthropic's extension that lets a Claude session open pages in your own
Chrome, with your own sign-ins: a session can then read a dataset's page behind a login, fill a
request form with you watching, or check a link the cloud cannot reach. Install it from the Chrome
Web Store (search "Claude in Chrome", by Anthropic), pin it, and sign in to it with your own Claude
account; it needs Pro or Max. Keep Chrome open while a thread works; a thread says when it is
connected. It never sends a letter or ticks a binding box on its own: you do those (section 9).

## 6. The Symphony control panel

https://openspineconsortium.com/symphony/control/ is the owner's console for a Symphony
repository, as the signed-in person: press Sign in with GitHub (the SymphonyBoard App's sign-in;
no token to paste), then choose OpenSpineConsortium/spine-datasets. The tabs: Board (the same
STATE.md as /board), Tasks (the issues as columns), Pull requests, Runs, Workers, Ask Claude
(reads the repository and answers, offering the panel's actions as buttons), Share and
Repositories. The sign-in is kept in your browser only. The board itself needs no panel:
https://github.com/OpenSpineConsortium/spine-datasets/blob/board/STATE.md is the file, and the
pipeline board (section 7) is beside it.

## 7. Picking a task

The tasks are the issues titled "Obtain <dataset>", one per record in datasets/, numbered by
priority group in tasks/TASKS.md; group 1 is the most useful first. The board's Queue lists every
task nobody holds; a task labelled `worker:<your login>` is given to you and comes first. Take
one whose route you can do:

- `letter` or `form`: anyone with an institutional mailbox (section 9).
- `download`: anyone with a grid account and Beethoven (section 4), once the record's licence
  allows it.
- `account`, `agreement` or `owner-only`: these need the owner's identity or signature; leave
  them unless the task says what a collaborator can do first (reading the terms, finding the
  contact).

## 8. Claiming and finishing a task with your Claude

Open a new thread in your Project and paste this, with the issue's number for N:

```
Claim issue N with the claim skill and carry it to a ready pull request, as docs/agents/PROTOCOL.md says; work on the branch claude/N, not this session's own branch. If the push of claude/N is refused, another session holds the issue: say so in one line and stop. Do not merge.
gh issue and gh pr are refused here, so add the labels, post the plan and open the draft pull request with your GitHub tools or gh api (repos/OpenSpineConsortium/spine-datasets/issues/N/labels, repos/OpenSpineConsortium/spine-datasets/issues/N/comments, repos/OpenSpineConsortium/spine-datasets/pulls). Mark the pull request ready with your GitHub tool update_pull_request (draft false), not gh api, which cannot change a draft; if you have no such tool, comment "finished; ready to mark" on the pull request and stop before you delete the claim file.
```

(The second paragraph is only for a cloud session or a Project thread, where gh issue and gh pr
are refused; leave it out in `claude` on your own computer.)

What the session does: pushes the branch `claude/N` (the first push is the claim; a second push
of the same name is refused, so two people never hold one task), labels the issue, posts the
plan, opens a draft pull request that says "Closes #N", then does the work: drafts the letter
from letters/<id>.md or letters/TEMPLATE.md for you to send, or writes the form text, or writes
the grid job for you to submit from your Beethoven session. You do the part only a person can do,
tell the session what happened, and it records the result in datasets/<id>.json and on the task,
in one of the shapes README.md lists, deletes the claim file and marks the pull request ready.
The owner merges; the merge closes the task. A result that is "waiting" keeps the task open, as
README.md says. Other prompts, for a rebase after "main moved" or a checkpoint, are in
docs/start/prompts.md.

## 9. Letters and forms, from your own mailbox

A letter goes from your own institutional mailbox, never from a personal one and never from a
session, with go2432@wayne.edu in copy and the subject tag "[XR/CT Imaging Research]". Use the
text in letters/<id>.md where one exists, else fill letters/TEMPLATE.md; a collaborator's letter
says "I work with Dr Gregory Schwing at the Department of General Surgery, Wayne State University
...". A form that asks nothing binding (name, institution, email, purpose) you may fill yourself,
with the letter's paragraphs as the purpose. Before sending, read the text once more for the words
the confidentiality rule bans (section 11).

## 10. What stays the owner's hand

Any signature on a data use or licence agreement, any fee, any attestation, any licence checkbox
that binds the person ticking it, any account in the owner's name (PhysioNet, Stanford AIMI, IEEE
DataPort, Hugging Face gates, Kaggle), any token or credential, the IRB and lawyer questions, and
the word for a grid job that takes space not yet budgeted. When your task reaches one of these,
comment "needs the owner" on it with exactly what is needed and the link, and hand it back as
CONTRIBUTING.md says.

## 11. The two rules you must not break

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
