# -*- coding: utf-8 -*-

import click

from api import Client


@click.group()
@click.option('-v', '--verbose', is_flag=True, help='Print more output.')
@click.pass_context
def cli(ctx, verbose=False):
    ctx.obj = Client(verbose)


@cli.command()
@click.argument('query', required=True, type=str)
@click.option('-kw', '--keyword', default=None, type=str, help='Search result filter.')
@click.option('-i', '--ids', type=str, help='Returns a list instead of dictionary. For concatenation with download.')
@click.pass_obj
def find(client, query, keyword, ids):
    click.echo(client.find(query, keyword=keyword, ids=ids))


@cli.command()
@click.argument('id_list', nargs=-1, required=True, type=str)
@click.option('-f', '--file-format', required=True, type=str, help='Specify file format (csv, root, yaml, yoda, or json) to be downloaded.')
@click.option('-i', '--ids', required=True, type=str, help='Specify which ids (hepdata or inspire) are given.')
@click.option('-t', '--table', default=None, help='Specify table to be downloaded.')
@click.pass_obj
def download(client, id_list, file_format, table, ids):
    client.download(id_list, file_format=file_format, ids=ids, table=table)
