# -*- coding: utf-8 -*-

"""Console script for aiscalator."""
import sys
import click
from .config import AiscalatorConfig
from .docker_command import docker_run_lab, docker_run_papermill


@click.group()
def main():
    """
    Command Line Interface to Aiscalate your data pipelines
    """
    pass


@main.command()
@click.argument('conf')
@click.argument('notebook')
# TODO add parameters override from CLI
def edit(conf, notebook):
    """CLI to Open an environment to edit step's code"""
    click.echo(docker_run_lab(AiscalatorConfig(conf, notebook)))


@main.command()
@click.argument('conf')
@click.argument('notebook')
# TODO add parameters override from CLI
def run(conf, notebook):
    """CLI Run step's code without GUI"""
    # TODO run multiple notebooks
    # we have to stage notebooks with same dockerfile together,
    # merge their requirements so that groups of notebooks can be
    # run together in the same container sequentially
    click.echo(docker_run_papermill(AiscalatorConfig(conf, notebook)))


# TODO pull run docker pull to download all images that might be needed

# TODO startproject command like cookiecutter to easily start a new pipeline or step
# TODO store config file path globally with an alias and use those shorter alias for easier commands
# TODO list steps/pipelines/data/etc


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
