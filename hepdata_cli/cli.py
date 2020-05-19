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
@click.pass_obj
def find(client, query):
    click.echo(client.find(query))
