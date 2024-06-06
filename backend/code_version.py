import subprocess
import os

# TODO: Refactor all of this. I want the service to know its version so that we can trace back from any weird output to the specific version, but also Docker doesn't have the git info at all


git_sha = os.environ["GIT_SHA"]

if not git_sha:
    git_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
