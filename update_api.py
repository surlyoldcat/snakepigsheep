
#this should grab swagger for a single API, and push it up to the right place in S3
import os
import sys
import json
import deserialize
from config import AppConfig, ApiInfo
import boto3

_root_dir = ""
_swagger_filename = "exported-swagger.json"
_config: AppConfig
_session: boto3.session.Session


def upload_swagger_to_s3(swagger: str, key: str):
    pass


def build_s3_key(api: ApiInfo) -> str:
    api_dir = api.name.lower().replace(" ", "")
    key = f"{api_dir}/{_swagger_filename}"
    return key


def fetch_swagger(api: ApiInfo) -> str:
    print(f"fetching swagger for {api.id}:{api.stage}")
    apig = _session.client('apigateway')
    response = apig.get_export(
        restApiId=api.id,
        stageName=api.stage,
        exportType='swagger',
        parameters={
            'extension': 'apigateway'
        }
    )
    swag = response.get('body').read().decode("utf-8")
    return str(swag)


def load_config() -> AppConfig:
    config_path = os.path.join(_root_dir, "config.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config_dict = json.load(f)
        ac = deserialize.deserialize(AppConfig, config_dict)
        return ac


def publish(api_id: str):
    # fetch swagger from APIG
    # determine the key/path for the file in S3
    # upload the swagger
    pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('API ID needs to be passed as command line parameter')
        exit(1)

    api_id = sys.argv[1]
    _root_dir = os.path.dirname(os.path.realpath(__file__))
    _config = load_config()
    _session = boto3.Session(profile_name=_config.aws_profile)
    publish(api_id)


