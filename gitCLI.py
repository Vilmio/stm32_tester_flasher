import git

class Git:
    def __init__(self) -> None:
        pass

    def pull(self):
        g = git.cmd.Git()
        g.pull()