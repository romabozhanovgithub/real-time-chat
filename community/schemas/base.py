from pydantic.utils import to_lower_camel


class BaseConfig:
    alias_generator = to_lower_camel
    allow_population_by_field_name = True
