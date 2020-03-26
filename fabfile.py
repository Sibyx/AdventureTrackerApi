import datetime
import json
import os
import warnings

from dotenv import load_dotenv
from fabric import Connection, task
from invoke import Context

warnings.filterwarnings(action='ignore', module='.*paramiko.*')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_NAME = 'adventure_tracker_api'
REPO_URL = 'https://github.com/Sibyx/AdventureTrackerApi.git'
KEEP_RELEASES = 5


def _get_connection(ctx: Context, config: dict) -> Connection:
    ctx.host = config['host']
    ctx.user = config['user']
    ctx.port = config['port']

    if 'ssh_key' in config:
        ctx.connect_kwargs.key_filename = config['ssh_key']
    elif 'password' in config:
        ctx.connect_kwargs.password = config['password']

    ctx = Connection(
        host=ctx.host,
        user=ctx.user,
        port=ctx.port,
        connect_kwargs=ctx.connect_kwargs,
    )

    ctx.config['run']['echo'] = True

    return ctx


def _parse_config(destination: str) -> dict:
    with open(f"{BASE_DIR}/.deploy/{destination}.json") as conf_file:
        return json.load(conf_file)


@task
def check(ctx, destination):
    config = _parse_config(destination)
    ctx = _get_connection(ctx, config['ssh'])

    ctx.run(f"{config['python']} --version")


@task
def setup(ctx, destination):
    config = _parse_config(destination)
    ctx = _get_connection(ctx, config['ssh'])
    shared_env = f"{config['deploy_to']}/shared/env"

    ctx.run(f"mkdir {config['deploy_to']}")

    with ctx.cd(config['deploy_to']):
        # Create directory structure
        ctx.run(f"mkdir shared")
        ctx.run(f"mkdir shared/media")
        ctx.run(f"mkdir releases")

        # Create Python virtualenv
        ctx.run(f"{config['python']} -m venv shared/env")

        # Install deployment tools
        ctx.run(f"{shared_env}/bin/pip install poetry")


@task
def deploy(ctx, destination):
    config = _parse_config(destination)
    ctx = _get_connection(ctx, config['ssh'])

    release = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    shared = f"{config['deploy_to']}/shared"

    # Set deploy to as current directory
    with ctx.cd(f"{config['deploy_to']}/releases"):
        # Clone repository
        ctx.run(f"git clone {REPO_URL} {release}", pty=True)

    # Set current release directory as working directory
    with ctx.cd(f"{config['deploy_to']}/releases/{release}"):
        # Checkout correct revision
        ctx.run(f"git checkout {config['revision']}")
        # Just to be sure, run git pull
        ctx.run("git pull")

        # Install dependencies
        ctx.run(f"{shared}/env/bin/pip install --upgrade pip")
        ctx.run(f"{shared}/env/bin/poetry export -f requirements.txt > requirements.txt")
        ctx.run(f"{shared}/env/bin/pip install -r requirements.txt")

        # Create .env file
        ctx.run("touch .env")
        for key, value in config['env'].items():
            ctx.run(f'echo "{key}=\'{value}\'" >> .env')

        # Migrate
        ctx.run(
            f"DJANGO_SETTINGS_MODULE={config['env']['DJANGO_SETTINGS_MODULE']} {shared}/env/bin/python manage.py migrate --no-input")

        # Fixtures
        ctx.run(
            f"DJANGO_SETTINGS_MODULE={config['env']['DJANGO_SETTINGS_MODULE']} {shared}/env/bin/python manage.py loaddata core/fixtures/initial.json")

        # Remove sensitive and useless files
        ctx.run("rm -rf .deploy media")

        # Link shared data
        ctx.run(f"ln -s {shared}/media media")

    # Publish release
    with ctx.cd(config['deploy_to']):
        # Remove old symlink
        ctx.run("rm -f current")
        # Create symlink to the latest release
        ctx.run(f"ln -s {config['deploy_to']}/releases/{release} current")

    # Clean old releases
    with ctx.cd(f"{config['deploy_to']}/releases"):
        ctx.run(f"ls -t . | sort -r | tail -n +{KEEP_RELEASES + 1} | xargs rm -rf --")


@task
def clean(ctx, destination):
    config = _parse_config(destination)
    ctx = _get_connection(ctx, config['ssh'])

    ctx.run(f"rm -rf {config['deploy_to']}")
