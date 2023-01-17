import os
import pathlib
import shutil
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    # PUT YOUR CODE HERE
    index = []
    for path in paths:
        if path.is_dir():
            for root, dirs, files in os.walk(path):
                for fily in files:
                    index.append(pathlib.Path(root) / fily)
        else:
            index.append(path)
    update_index(gitdir, index)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    # PUT YOUR CODE HERE
    index = read_index(gitdir)
    # print([find_object(i.sha1.hex(), gitdir) for i in index])

    tree = write_tree(gitdir, index)
    commit = commit_tree(gitdir, tree, message, author=author)
    update_ref(gitdir, "HEAD", tree)
    return commit


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    # PUT YOUR CODE HERE
    old_tree = get_ref(gitdir)
    if obj_name == "HEAD":
        head = resolve_head(gitdir)
    else:
        head = obj_name
    obj = find_object(head, gitdir) if head else None
    if obj is None:
        raise Exception(f"Object '{head}' not found")
    obj_type, obj_data = read_object(obj, gitdir)
    if obj_type == "commit":
        new_tree = commit_parse(obj_data).split("\n")[0].split()[1].strip()
    elif obj_type == "tree":
        new_tree = obj
    else:
        raise Exception(f"Object '{head}' is not a commit or tree")
    update_ref(gitdir, "HEAD", new_tree)
    if old_tree:
        tracked_files = dict(find_tree_files(old_tree, gitdir))
    else:
        tracked_files = {}
    checking_files = dict(find_tree_files(new_tree, gitdir))
    for name, sha in checking_files.items():
        if name in tracked_files.keys():
            if sha != tracked_files[name]:
                with open(gitdir / name, "wb") as f:
                    f.write(read_object(sha, gitdir)[1])
        else:
            with open(name, "wb") as f:
                f.write(read_object(sha, gitdir)[1])
    for name, sha in tracked_files.items():
        if name not in checking_files.keys():
            if os.path.isfile(name):
                os.remove(name)
            else:
                shutil.rmtree(name)
