import subprocess
import os

class Git:
    def __init__(self, repoRoot):
        self.repoRoot = repoRoot
        os.chdir(repoRoot)

    def add(self, *files):
        subprocess.run(['git', 'add'] + [os.path.join(self.repoRoot, file) for file in files])

    def commit(self, withMessage=None):
        if withMessage is None:
            withMessage = ''
        subprocess.run(['git', 'commit', '-m', withMessage])
