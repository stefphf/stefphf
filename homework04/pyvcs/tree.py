import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    content: tp.List[tp.Tuple[int, str, bytes]] = []
    for entry in index:
        if entry.name.startswith(dirname):
            if entry.name[len(dirname) :].count("/") == 0:
                content.append((entry.mode, entry.name[len(dirname) :], entry.sha1))
            else:
                new_dirname = dirname + entry.name[len(dirname) :].split("/")[0] + "/"
                tree_sha = bytes.fromhex(write_tree(gitdir, index, new_dirname))
                content.append((stat.S_IFDIR, entry.name[len(dirname) :].split("/")[0], tree_sha))

    content_binary = b"".join(
        f"{mode:o} {name}".encode() + b"\0" + sha1 for mode, name, sha1 in content
    )
    return hash_object(content_binary, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    commit_time = int(time.mktime(time.localtime()))
    commit_timezone = time.strftime("%z", time.localtime())
    parent_str = f"\nparent {parent}" if parent else ""
    content = (
        f"tree {tree}"
        + parent_str
        + f"\nauthor {author} {commit_time} {commit_timezone}\ncommitter {author} {commit_time} {commit_timezone}\n\n{message}\n"
    )
    commit_sha = hash_object(content.encode(), "commit", write=True)
    return commit_sha
