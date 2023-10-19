USER_LIST_QUERY = """
select
    users_user.id
,   users_user.email
,   users_user.avatar
,   users_user.first_name
,   users_user.last_name

from users_user
where users_user.id = any($1::integer[]);
"""

USER_QUERY = """
select
    users_user.id
,   users_user.email
,   users_user.avatar
,   users_user.first_name
,   users_user.last_name
from users_user
where users_user.id=$1;
"""
