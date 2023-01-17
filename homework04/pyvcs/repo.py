import os
import pathlib
import typing as tp


class NotGitRepo(Exception):
    pass


def repo_find(workdir: str = ".") -> pathlib.Path:
    # PUT YOUR CODE HERE
    workdir_path: pathlib.Path = pathlib.Path(workdir).absolute()
    git_dir_name = os.environ.get("GIT_DIR", ".git")
    if git_dir_name in workdir_path.parts[1:]:
        gitdir = workdir_path.parts[0] + "/".join(
            workdir_path.parts[1 : workdir_path.parts.index(git_dir_name) + 1]
        )
        gitdir_path = pathlib.Path(gitdir)
    else:
        gitdir_path = workdir_path / git_dir_name
    if os.path.exists(gitdir_path):
        return pathlib.Path(gitdir_path)
    else:
        raise NotGitRepo("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    # PUT YOUR CODE HERE
    workdir = pathlib.Path(workdir)
    if os.path.isfile(workdir):
        raise Exception(f"{workdir} is not a directory")
    else:
        git_dir_name = os.environ.get("GIT_DIR", ".git")
        gitdir = workdir / git_dir_name
        os.mkdir(gitdir)
        os.mkdir(gitdir / "branches")
        os.mkdir(gitdir / "objects")
        os.mkdir(gitdir / "objects" / "pack")
        os.mkdir(gitdir / "refs")
        os.mkdir(gitdir / "refs" / "heads")
        os.mkdir(gitdir / "refs" / "tags")
        with open(gitdir / "HEAD", "w") as f:
            f.write("ref: refs/heads/master\n")
        with open(gitdir / "config", "w") as f:
            f.write(
                "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
            )
        with open(gitdir / "description", "w") as f:
            f.write("Unnamed pyvcs repository.\n")
        return gitdir
