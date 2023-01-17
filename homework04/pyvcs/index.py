import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        # PUT YOUR CODE HERE
        return (
            struct.pack(
                ">LLLLLLLLLL20sH",
                self.ctime_s,
                self.ctime_n,
                self.mtime_s,
                self.mtime_n,
                self.dev,
                self.ino,
                self.mode,
                self.uid,
                self.gid,
                self.size,
                self.sha1,
                self.flags,
            )
            + self.name.encode()
            + b"\x00" * (8 - (len(self.name) + 62) % 8)
        )

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        # PUT YOUR CODE HERE
        (
            ctime_s,
            ctime_n,
            mtime_s,
            mtime_n,
            dev,
            ino,
            mode,
            uid,
            gid,
            size,
            sha1,
            flags,
        ) = struct.unpack(">LLLLLLLLLL20sH", data[:62])
        name = data[62:].split(b"\x00")[0].decode()
        return GitIndexEntry(
            ctime_s, ctime_n, mtime_s, mtime_n, dev, ino, mode, uid, gid, size, sha1, flags, name
        )


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    index_file = gitdir / "index"
    entries = []
    try:
        with open(index_file, "rb") as f:
            data = f.read()
            signature, version, entries_count = struct.unpack(">4sLL", data[:12])
            data = data[12:]
            for _ in range(entries_count):
                entry = GitIndexEntry.unpack(data)
                entries.append(entry)
                data = data[62 + len(entry.name) + (8 - (len(entry.name) + 62) % 8) :]
    except FileNotFoundError:
        pass
    return entries


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    # PUT YOUR CODE HERE
    index_file = gitdir / "index"
    with open(index_file, "w+b") as f:
        f.write(struct.pack(">4sLL", b"DIRC", 2, len(entries)))
        for entry in entries:
            f.write(entry.pack())
        f.seek(0)
        index_sha = hashlib.sha1(f.read()).digest()
        f.write(index_sha)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    # PUT YOUR CODE HERE
    entries = read_index(gitdir)
    for entry in entries:
        if details:
            print(
                f"{entry.mode:o} {entry.sha1.hex()} 0\t{entry.name}"
            )  # entry.mode:0 - восьмеричное представление
        else:
            print(entry.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    # PUT YOUR CODE HERE
    entries = read_index(gitdir)
    for path in paths:
        with open(path, "rb") as f:
            data = f.read()
            sha1 = hash_object(data, "blob", write)
            stats = os.stat(path)
            entry = GitIndexEntry(
                0, 0, 0, 0, 0, 0, 0, 0, 0, len(data), bytes.fromhex(sha1), 0, str(path)
            )
            entry = entry._replace(
                mode=stats.st_mode,
                ino=stats.st_ino,
                uid=stats.st_uid,
                gid=stats.st_gid,
                dev=stats.st_dev,
            )
            entries.append(entry)
    entries.sort(key=operator.attrgetter("name"))
    if write:
        write_index(gitdir, entries)
