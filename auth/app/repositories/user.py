from community.repositories.dynamodb import BaseRepository


class UserRepository(BaseRepository):
    table_name = "users"
    partition_key = "id"
    sort_key = "username"
