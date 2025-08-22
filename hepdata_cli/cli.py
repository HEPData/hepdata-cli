# -*- coding: utf-8 -*-

import click

from .version import __version__
from .api import Client, ALLOWED_FORMATS


@click.group()
@click.version_option(None, "-v", "--version", message=__version__)
@click.option('--verbose', is_flag=True, help='Print more output.')
@click.pass_context
def cli(ctx, verbose=False):
    """CLI interface to API Client."""
    ctx.obj = Client(verbose)


@cli.command()
@click.argument('query', required=True, type=str)
@click.option('-kw', '--keyword', default=None, type=str, help='Search result filter.')
@click.option('-i', '--ids', type=str, help='Returns a list instead of dictionary. For concatenation with download.')
@click.pass_obj
def find(client, query, keyword, ids):
    """CLI interface to API client.find function."""
    click.echo(client.find(query, keyword=keyword, ids=ids))


@cli.command()
@click.argument('id_list', nargs=-1, required=True, type=str)
@click.option('-f', '--file-format', required=True, type=str, help=f'Specify file format (from {ALLOWED_FORMATS}) to be downloaded.')
@click.option('-i', '--ids', required=True, type=str, help='Specify which ids (hepdata or inspire) are given.')
@click.option('-t', '--table-name', default='', type=str, help='Specify table to be downloaded.')
@click.option('-d', '--download-dir', default='./hepdata-downloads', type=str, help='Specify where to download the files.')
@click.pass_obj
def download(client, id_list, file_format, ids, table_name, download_dir):
    """CLI interface to API client.download function."""
    client.download(id_list, file_format=file_format, ids=ids, table_name=table_name, download_dir=download_dir)


@cli.command()
@click.argument('id_list', nargs=-1, required=True, type=str)
@click.option('-i', '--ids', required=True, type=str, help='Specify which ids (hepdata or inspire) are given.')
@click.pass_obj
def fetch_names(client, id_list, ids):
    """CLI interface to API client.fetch_names function."""
    click.echo(client.fetch_names(id_list, ids=ids))


@cli.command()
@click.argument('path_to_file', required=True, type=str)
@click.option('-e', '--email', required=True, type=str, help='User email.')
@click.option('-r', '--recid', default=None, type=str, help='Record ID (if updating already existing record).')
@click.option('-i', '--invitation-cookie', default=None, type=str, help='Invitation cookie (if NOT uploading to sandbox).')
@click.option('-s', '--sandbox', default=True, type=bool, help='Whether to upload to the sandbox or not.')
@click.option('--password', '-p', prompt=True, hide_input=True, help='User password (prompt if not specified).')
@click.pass_obj
def upload(client, path_to_file, email, recid, invitation_cookie, sandbox, password):
    """CLI interface to API client.upload function."""
    client.upload(path_to_file, email, recid, invitation_cookie, sandbox, password)
