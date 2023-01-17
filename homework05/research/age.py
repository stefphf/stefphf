import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def _get_average_friends_age(date_list: tp.List[str]) -> tp.Optional[float]:
    friends_count = 0
    age_sum = 0
    for d in date_list:
        try:
            date_of_birth = dt.datetime.strptime(d.replace(".", ""), r"%d%m%Y").date()
        except (ValueError, AttributeError):
            continue
        else:
            friends_count += 1
            age = (dt.datetime.now().date() - date_of_birth).days // 365
            age_sum += age

    return (age_sum / friends_count) if friends_count != 0 else None


def age_predict(user_id: int) -> tp.Optional[float]:
    frields_list = get_friends(
        user_id,
        fields=["bdate"],
    )
    date_payload_list = [
        friend.get("bdate", None) for friend in frields_list.items if isinstance(friend, dict)
    ]
    average_friends_age = _get_average_friends_age(date_payload_list)

    return average_friends_age
