import hashlib
import os
import pathlib
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    # PUT YOUR CODE HERE
    content = data
    header = f"{fmt} {len(content)}\0".encode()
    store = header + content
    filename = hashlib.sha1(store).hexdigest()
    if write:
        gitdir = repo_find()
        os.makedirs(gitdir / "objects" / filename[:2], exist_ok=True)
        with open(gitdir / "objects" / filename[:2] / filename[2:], "wb") as f:
            f.write(zlib.compress(store))
    return filename


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    objs_dir = gitdir / "objects" / obj_name[:2]
    ans = []
    if len(obj_name) == 40:
        ans = [obj_name]
    elif len(obj_name) >= 4:
        ans = [
            obj_name[:2] + obj.name
            for obj in objs_dir.iterdir()
            if obj.name.startswith(obj_name[2:])
        ]
    if len(ans) == 0:
        raise Exception(f"Not a valid object name {obj_name}")
    return ans


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    obj_path = gitdir / "objects" / obj_name[:2] / obj_name[2:]
    if obj_path.exists():
        return obj_name
    else:
        return ""


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    # PUT YOUR CODE HERE
    path = gitdir / "objects" / sha[:2] / sha[2:]
    with open(path, mode="rb") as f:
        obj_data = zlib.decompress(f.read())
        obj_type, obj_data = obj_data.split(b"\0", maxsplit=1)
        obj_type_str = obj_type.decode().split()[0]
        return obj_type_str, obj_data


def read_tree(data: bytes) -> str:
    # PUT YOUR CODE HERE
    contents = data
    ans = []
    while contents != b"":
        filemode_bytes, contents_bytes = contents.split(b" ", maxsplit=1)
        filename_bytes, contents_bytes = contents_bytes.split(b"\x00", maxsplit=1)
        sha1, contents = contents_bytes[:20], contents_bytes[20:]
        filemode = filemode_bytes.decode()
        filename = filename_bytes.decode()
        sha1_str = sha1.hex()
        fmt, _ = read_object(sha1_str, repo_find())
        ans.append((filemode, fmt, sha1_str, filename))

    result = list()
    for tree_item in ans:
        result.append(
            "{filemode:0>6} {obj_type} {sha1}\t{filename}".format(
                filemode=tree_item[0],
                obj_type=tree_item[1],
                sha1=tree_item[2],
                filename=tree_item[3],
            )
        )
    return "\n".join(result)


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    fmt, data = read_object(obj_name, repo_find())
    if fmt == "commit":
        print(commit_parse(data))
    elif fmt == "tree":
        print(read_tree(data))
    elif fmt == "blob":
        print(data.decode())
    else:
        raise Exception(f"Not a valid object name {obj_name}")


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    fmt, data = read_object(tree_sha, repo_find())
    if fmt != "tree":
        raise Exception(f"Not a tree {tree_sha}")

    tree_items = read_tree(data).split("\n")
    ans = [(name, sha) for _, _, sha, name in map(lambda x: x.split(), tree_items)]
    return ans


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    return raw.decode()
