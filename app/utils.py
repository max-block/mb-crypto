import click


def fatal(message: str):
    click.secho(message, fg="red")
    exit(1)
