import dataclasses
import math
import time
import typing as tp

from vkapi import session
from vkapi.config import VK_CONFIG
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int,
    count: int = 5000,
    offset: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> FriendsResponse:
    query_params = {
        "user_id": user_id,
        "count": count,
        "offset": offset,
        "fields": fields,
    }

    response = session.get("friends.get", **query_params)
    try:
        response_data = response.json()["response"]
        return FriendsResponse(**response_data)
    except Exception as e:
        raise APIError.bad_request(message=str(e))


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    query_params = {
        "source_uid": source_uid,
        "target_uid": target_uid,
        "target_uids": target_uids,
        "order": order,
        "count": count,
        "offset": offset,
        "progress": progress,
    }

    requests_count = 1
    if target_uids is not None:
        target_limit = 100
        assert isinstance(target_limit, int)
        requests_count = math.ceil(len(target_uids) / target_limit)

    mutual_list = []
    for _ in range(requests_count):
        response = session.get("friends.getMutual", **query_params)
        if response.status_code == 200:
            response_data = response.json()["response"]
            mutual_list.extend(response_data)
        query_params["offset"] += 100
        time.sleep(1)

    try:
        mutual_friends_list = [MutualFriends(**item) for item in mutual_list]  # type: ignore
    except TypeError:
        return mutual_list  # type: ignore

    return mutual_friends_list
