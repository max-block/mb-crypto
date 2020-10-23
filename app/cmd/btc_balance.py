import click

from app import blockcypher


@click.command()
@click.argument("addresses", type=click.File())
@click.option("--hide-empty/--no-hide-empty", default=False)
@click.option("--satoshi/--no-satoshi", default=False)
def cli(addresses, hide_empty: bool, satoshi: bool):
    addresses = addresses.read()
    for address in addresses.split("\n"):
        if not address:
            continue
        res = blockcypher.get_btc_balance(address)
        if res.is_ok() and res.value == 0 and hide_empty:
            continue

        # print(address, res)
