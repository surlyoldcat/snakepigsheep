import json
import os
import shutil
import subprocess
import sys
from typing import List
import boto3
import deserialize

import templates.index_html
from config import AppConfig, ApiInfo

_root_dir = ""
_site_dir = ""
_swagger_filename = "exported-swagger.json"


def upload_site(config: AppConfig):
    print("uploading site to S3...")
    s3_sync_cmd = f"aws s3 sync {_site_dir} s3://{config.publish_bucket}/ --profile {config.aws_profile}"
    try:
        retcode = subprocess.call(s3_sync_cmd, shell=True)
        print("S3 sync returned ", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)


def fetch_swagger(api: ApiInfo) -> str:
    print(f"fetching swagger for {api.id}:{api.stage}")
    session = boto3.Session(profile_name=c.aws_profile)
    apig = session.client('apigateway')
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


def create_api_dir(api_dir_name: str) -> str:
    api_path = os.path.join(_site_dir, api_dir_name)
    content_path = os.path.join(_root_dir, "templates/apicontent")
    shutil.copytree(content_path, api_path)
    return api_path


def update_api_swagger(api_dir_path:str, api: ApiInfo):
    swagger = fetch_swagger(api)
    out_file = os.path.join(api_dir_path, _swagger_filename)
    with open(out_file, 'w', encoding='utf-8') as export_file:
        export_file.write(swagger)


def create_index_html(links: List[str]):
    li_template = '<li><b>{}</b></li>'
    items = [li_template.format(link) for link in links]
    links_html = "".join(items)
    doc_html = templates.index_html.index.format(api_links=links_html)

    index_path = os.path.join(_site_dir, "index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(doc_html)


def prepare_site_dir():
    # kill the pub directory if it exists, and recreate
    print(f"recreating {_site_dir}...")
    if os.path.exists(_site_dir):
        shutil.rmtree(_site_dir, ignore_errors=False)

    os.mkdir(_site_dir)


def load_config() -> AppConfig:
    config_path = os.path.join(_root_dir, "config.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config_dict = json.load(f)
        ac = deserialize.deserialize(AppConfig, config_dict)
        return ac


def create_api_link(dir_name: str, api_name:str) -> str:
    t = '<a href="{apidir}/index.html">{apiname}</a>'
    return t.format(apidir=dir_name, apiname=api_name)


def publish(config: AppConfig):
    prepare_site_dir()

    index_links = []
    for a in config.apis:
        api_nm = a.name
        print(f"processing api: {api_nm}")
        api_dir = api_nm.lower().replace(" ", "")
        index_links.append(create_api_link(api_dir, api_nm))

        api_subdir = create_api_dir(api_dir)
        update_api_swagger(api_subdir, a)

    create_index_html(index_links)
    upload_site(config)
    print("all done!")


if __name__ == '__main__':
    _root_dir = os.path.dirname(os.path.realpath(__file__))
    c = load_config()
    site_dir_name = c.output_dir
    if not site_dir_name.endswith('/'):
        site_dir_name += '/'

    _site_dir = os.path.join(_root_dir, site_dir_name)
    print(f"Root dir: {_root_dir}")
    print(f"Site dir: {_site_dir}")
    publish(c)

