import subprocess


git_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
