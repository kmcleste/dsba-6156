# Contributing to DSBA 6156: Applied Machine Learning

## Setting up your development environment

As this project is primarily built on Haystack, we must also follow their suggested configuration. Development will be best supported on Linux and macOS. You are free to use Windows, but understand you may run into some issues. To reduce the chances of any major breaking conflicts, consider using WSL for Windows development.

The following instructions are tested on **macOS Monterey v12.6**

### Prerequisites

Per Haystack's documentation, make sure your system packages are up-to-date and that a few dependencies are installed. From the terminal, run:

```bash
# macOS
brew update && brew install libsndfile1 ffmpeg

# linux
sudo apt update && sudo apt-get install libsndfile1 ffpmeg
```

You may need additional dependencies depending on your environment, but these should get you started.

### Installation

Now clone the repo and create a new branch. From the terminal, run:

```bash
git clone https://github.com/kmcleste/dsba-6156.git

git checkout -b $your_branch_name
```

To switch between branches, you can run:

```bash
# list all branches
git branch -a

# if branch has already been checked out
git switch $branch_name_here

# else
git checkout $branch_name_here
```

Then move into your cloned folder, create a virtual environment, and install the requirements:

```bash
# Move into cloned folder
cd dsba-6156/

# Create a virtual environment
python3 -m venv .venv

# Activate the environment
source .venv/bin/activate

# Upgrade pip
python3 -m pip install -U pip

# Install requirements - this will also install pre-commit hooks
make pip-install
```

Your environment should now be configured and you can begin preparing your first commit.

## Making your first commit

Once you are satisfied with the changes you have made, run the following:

```bash
# add changes to staging area
git add .

# commit changes
git commit -m "Some insightful commit message"

# your first push will require you to set upstream branch to track
git push --set-upstream origin $your_branch_name

# for subsequent pushes, you can just run
git push
```

For more info on using GitHub, here is a list of [some handy git commands](https://education.github.com/git-cheat-sheet-education.pdf).

## Formatting Pull Requests

To actually see your code get merged into the overall project, you will need to create a pull request (PR). A PR allows other contributors to review and either approve or reject your code. If your code gets rejected, do not take it personally -- simply fix the issues outlined in the comments provided by the reviewer. Once you have made the necessary changes, you can request another review.

When titling your PR, use the conventions outlined in [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```bash
<type>[optional scope]: <description>
```

Common types are:

- `feat` (for enhancements)
- `bug` (for bug fixes)
- `docs` (for change to documentation)
- `refactor` (for code refactorings)

Examples:

- `feat: add json logging to search module`
- `bug: fix unhandled value error in search.py`
- `docs: updated streamlit ui documentation`

### PR Description

Please include the following in your PR:

- What is changing?
- Why is it changing?
- How was it tested?
- Any further details
