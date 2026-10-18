# Git workflow lab — follow in order
Use your GitHub username `Danish200170`. Create an empty GitHub repository named `Git_and_GitHub_Danish`. Do not commit private keys, access tokens, or database credentials.

## A. SSH, clone, first branch and merge
```bash
ls -la ~/.ssh
ssh-keygen -t ed25519 -C "your-github-email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
```
Add the `.pub` key in GitHub Settings → SSH and GPG keys. Never share the private key. Then:
```bash
ssh -T git@github.com
cd ~
git clone git@github.com:Danish200170/Git_and_GitHub_Danish.git
cd Git_and_GitHub_Danish
```
Copy the starter project files into this cloned folder, then:
```bash
git switch -c Danish200170
git add app.py data.json templates/index.html requirements.txt .gitignore README.md workflow
git commit -m "Add Flask To-Do application"
git push -u origin Danish200170
git switch main
git merge --no-ff Danish200170 -m "Merge initial Flask application"
git push origin main
```
If the remote default branch is `master`, rename it to `main` and push it before switching.

## B. JSON change and conflict
```bash
git switch main
git pull --ff-only origin main
git switch -c Danish200170_new
```
Edit `data.json`: set version to 2, change message to `Updated by Danish200170_new`, and add `merge resolution demo` to features. Then:
```bash
git add data.json
git commit -m "Update API JSON data"
git push -u origin Danish200170_new
git switch main
```
On main, edit the same `message` line to `Updated on main branch`, then:
```bash
git add data.json
git commit -m "Change API message on main"
git merge --no-ff Danish200170_new
```
The merge should conflict because the same line changed. Accept the incoming `_new` branch's version:
```bash
git checkout --theirs data.json
git add data.json
git commit -m "Resolve data.json conflict using Danish200170_new"
git push origin main
```
In this merge, `--theirs` means the branch being merged in. If no conflict occurs, inspect status and do not fabricate evidence.

## C. Parallel branches
```bash
git switch main
git switch -c master_1
```
Edit `templates/index.html` to make a visible frontend improvement, then:
```bash
git add templates/index.html
git commit -m "Add To-Do form frontend"
git push -u origin master_1
git switch main
git switch -c master_2
```
The Flask POST endpoint is in `app.py`. Verify or improve it, then:
```bash
git add app.py requirements.txt
git commit -m "Add MongoDB-backed POST endpoint"
git push -u origin master_2
git switch main
git merge --no-ff master_1 -m "Merge To-Do frontend"
git merge --no-ff master_2 -m "Merge MongoDB backend"
git push origin main
```
Resolve any real conflicts manually, test, stage, and commit.

## D. Three separate commits on master_1
The starter form already includes the three optional fields for a working app. For the history exercise, edit `templates/index.html` so each commit adds exactly one field:
```bash
git switch master_1
# Edit file: add only Item ID
git add templates/index.html
git commit -m "Add Item ID field"
# Edit file: add Item UUID while keeping Item ID
git add templates/index.html
git commit -m "Add Item UUID field"
# Edit file: add Item Hash while keeping prior fields
git add templates/index.html
git commit -m "Add Item Hash field"
git log --oneline --decorate -6
git push -u origin master_1
git switch main
git merge --no-ff master_1 -m "Merge sequential To-Do field commits"
git push origin main
```
Do not squash or amend these three commits.

## E. git reset --soft
Inspect history and note the hash for `Add Item ID field` (the commit before UUID and Hash). Create a safety branch:
```bash
git log --oneline --decorate --all
git switch main
git branch backup-main-before-soft-reset
git reset --soft ITEM_ID_COMMIT_HASH
git status
git commit -m "Recommit state through Item ID (soft reset demo)"
```
Replace `ITEM_ID_COMMIT_HASH` with the actual hash. `--soft` moves HEAD while leaving changes staged. This rewrites local main history. Do not force-push a shared/protected repository. Keep the backup branch. Only if this is your own assignment repository and you understand the effect, update remote main with `git push --force-with-lease origin main`.

## F. Rebase
```bash
git switch master_1
git rebase main master_1
git log --oneline --graph --decorate --all
git status
```
Do not squash; the three commits should remain separate. If conflicts occur, edit files to resolve markers, `git add <file>`, then `git rebase --continue`. To cancel: `git rebase --abort`. Since rebase changes commit IDs, only update an already-pushed branch with `git push --force-with-lease origin master_1` when appropriate.

## Evidence required
Capture real screenshots/logs for SSH test, clone, branch and merge, JSON conflict and resolution, both feature branches and merges, three sequential commits, status after reset --soft, and rebase graph. Save them in `screenshots/` and insert them into the Word report. Do not fake terminal output.
