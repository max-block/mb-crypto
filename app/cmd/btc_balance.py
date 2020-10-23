import click

from app import blockcypher


@click.command()
@click.argument("addresses", type=click.File())
@click.option("--hide-empty/--no-hide-empty", default=False)
@click.option("--satoshi/--no-satoshi", default=False)
@click.option("--round", "round_digits", default=8)
def cli(addresses, hide_empty: bool, satoshi: bool, round_digits: int):
    addresses = addresses.read()
    for address in addresses.split("\n"):
        if not address:
            continue
        res = blockcypher.get_btc_balance(address)
        if res.is_ok() and res.value == 0 and hide_empty:
            continue
        if res.is_err():
            value = res.value
        elif satoshi:
            value = f"{res.value} sat"
        else:
            value = f"{round(res.value / 100_000_000, ndigits=round_digits)} btc"

        click.echo(f"{address} / {value}")
