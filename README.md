# GitHub Actions Fast-Forward Merge Demo

## Overview

This project demonstrates how to perform a Fast-Forward (FF) merge using GitHub Actions workflow.

The objective is to ensure that:

* No merge commit is created
* Target branch maintains the same commit SHA as the source branch
* Repository history remains linear and clean

---

# Fast-Forward Merge

## Normal Merge

Normal merge creates an additional merge commit.

Example:

```bash
A---B-------M
     \     /
      C---D
```

Where:

* `M` = merge commit

---

## Fast-Forward Merge

Fast-forward merge does not create a merge commit.

Example:

```bash
A---B---C---D
```

The target branch simply moves forward to the latest source branch commit.

---

# Workflow File

Location:

```bash
.github/workflows/ff-merge.yml
```

Workflow:

```yaml
name: FF Merge

on:
  workflow_dispatch:

permissions:
  contents: write

jobs:
  merge:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - run: |
          git fetch origin
          git checkout main
          git merge --ff-only origin/feature
          git push origin main
```

---

# Workflow Explanation

| Step     | Description                     |
| -------- | ------------------------------- |
| Checkout | Downloads repository code       |
| Fetch    | Retrieves latest branch updates |
| Merge    | Performs FF-only merge          |
| Push     | Updates target branch           |

---

# Verification

Run the following commands after merge:

```bash
git rev-parse main
git rev-parse feature
```

Expected Result:

```bash
abc123
abc123
```

Both branches should have the same commit SHA.

---

# Benefits

* Linear Git history
* No unnecessary merge commits
* Easier rollback
* Better CI/CD traceability
* Cleaner audit history

---

# Important Notes

FF merge works only when:

* Target branch has no additional commits
* Branch history is linear

If histories diverge, merge will fail with:

```bash
fatal: Not possible to fast-forward, aborting.
```

---

# Security & Permissions

Recommended repository settings:

* Enable branch protection
* Disable direct pushes to main
* Require PR approval
* Enforce linear history

Required GitHub Actions permission:

```yaml
permissions:
  contents: write
```

---

# Demo Steps

1. Create feature branch
2. Add new commit
3. Run GitHub Actions workflow
4. Verify merge success
5. Compare commit SHAs
6. Show linear Git history

---

# Conclusion

This implementation demonstrates how GitHub Actions can automate Fast-Forward merges while preserving commit SHA consistency and maintaining a clean Git history for enterprise CI/CD workflows.
