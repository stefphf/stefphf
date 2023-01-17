import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    # PUT YOUR CODE HERE
    with open(gitdir / ref, "w") as f:
        f.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    # PUT YOUR CODE HERE
    with open(gitdir / name, "w") as f:
        f.write(f"ref: {ref}")


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    # PUT YOUR CODE HERE
    if refname == "HEAD":
        refname = get_ref(gitdir)
    with open(gitdir / refname) as f:
        return f.read().strip()


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    # PUT YOUR CODE HERE
    try:
        return ref_resolve(gitdir, "HEAD")
    except FileNotFoundError:
        return None


def is_detached(gitdir: pathlib.Path) -> bool:
    # PUT YOUR CODE HERE
    if "/" in get_ref(gitdir):
        return False
    else:
        return True


def get_ref(gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    with open(gitdir / "HEAD") as f:
        data = f.read()
        if "ref:" in data:
            return data.split()[1]
        else:
            return data.strip()
