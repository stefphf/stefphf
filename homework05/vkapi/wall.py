import math
import time
import typing as tp

import pandas as pd  # type: ignore
from vkapi import config, session
from vkapi.exceptions import APIError

code = """
    var query_params = %s;
    var items = [];
    var iterCount = 25;
    var i = 0;
    while (i < iterCount && query_params.count > 0) {
        var responseItems = API.wall.get(query_params).items;
        items.push(responseItems);
        i = i + 1;
        query_params.count = query_params.count - 100;
        query_params.offset = query_params.offset + responseItems.length;
    }
    return items;
"""


def get_posts_2500(count: int = 2500, **kwargs: tp.Any) -> tp.List[tp.Dict[str, tp.Any]]:
    kwargs["count"] = str(count)
    code_data = code % kwargs
    request_data = {
        "access_token": config.VK_CONFIG["access_token"],
        "v": config.VK_CONFIG["version"],
        "code": code_data,
    }

    response = session.post("execute", **request_data)
    try:
        response_data = response.json()["response"]["items"]
    except Exception as e:
        raise APIError.bad_request(message=str(e))

    return response_data


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    query_params = {
        "owner_id": owner_id,
        "domain": domain,
        "offset": offset,
        "filter": filter,
        "extended": extended,
        "fields": fields,
        "v": "5.126",
    }

    wall_execute_data = []
    iter_count = math.ceil(count / max_count)
    i = 0
    start = time.time()
    while (i < iter_count) and (count > 0):
        if count >= max_count:
            posts_list = get_posts_2500(count=2500, **query_params)
            wall_execute_data += posts_list
            count -= 2500
            query_params["offset"] += 2500  # type: ignore
        else:
            posts_list = get_posts_2500(count=count, kwargs=query_params)
            wall_execute_data += posts_list
            break

        requests_delta_time = time.time() - start
        if requests_delta_time < 1:
            time.sleep(1 - requests_delta_time)
            start = time.time()

    return pd.json_normalize(wall_execute_data)