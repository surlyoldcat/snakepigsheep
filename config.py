from typing import List


class ApiInfo:
    id: str
    name: str
    stage: str


class AppConfig:
    publish_bucket: str
    aws_profile: str
    output_dir: str
    apis: List[ApiInfo]

