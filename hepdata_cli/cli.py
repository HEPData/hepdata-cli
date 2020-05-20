# -*- coding: utf-8 -*-

import click

from api import Client


@click.group()
@click.option('--verbose', '-v', is_flag=True, help="Print more output.")
@click.pass_context
def cli(ctx, verbose=False):
    ctx.obj = Client(verbose)


@cli.command()
@click.argument('query')
@click.option('-kw', "--keyword", default="All", type=str)
@click.pass_obj
def find(client, query, keyword):
    click.echo(client.find(query, keyword))


@cli.command()
@click.argument('query')
@click.option('--csv', is_flag=True, help="Download type.")
@click.option('--root', is_flag=True, help="Download type.")
@click.option('--yaml', is_flag=True, help="Download type.")
@click.option('--yoda', is_flag=True, help="Download type.")
@click.pass_obj
def download(client, query, csv=False, root=False, yaml=False, yoda=False):
    client.download(query, csv=csv, root=root, yaml=yaml, yoda=yoda)
