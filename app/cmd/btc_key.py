import click
from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39MnemonicValidator,
    Bip39SeedGenerator,
    Bip39WordsNum,
    Bip44,
    Bip44Changes,
    Bip44Coins,
)

from app.utils import fatal


@click.command()
@click.option("-m", "--mnemonic")
@click.option("-p", "--passphrase", default="")
@click.option("--prompt-mnemonic", is_flag=True)
@click.option("--prompt-passphrase", is_flag=True)
@click.option("--hide-mnemonic", is_flag=True)
@click.option("--hide-private", is_flag=True)
@click.option("-l", "--limit", default=5)
def cli(
    mnemonic: str,
    passphrase: str,
    limit: int,
    prompt_mnemonic: bool,
    prompt_passphrase: bool,
    hide_mnemonic: bool,
    hide_private: bool,
):
    if prompt_passphrase:
        passphrase = click.prompt("passphrase", hide_input=True)
    if prompt_mnemonic:
        mnemonic = click.prompt("mnemonic", hide_input=True)

    if not mnemonic:
        mnemonic = Bip39MnemonicGenerator.FromWordsNumber(Bip39WordsNum.WORDS_NUM_24)

    if not Bip39MnemonicValidator(mnemonic).Validate():
        return fatal("Invalid mnemonic")

    seed_bytes = Bip39SeedGenerator(mnemonic).Generate(passphrase)

    if not hide_mnemonic:
        click.echo(mnemonic + "\n")

    bip_obj_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
    bip_obj_acc = bip_obj_mst.Purpose().Coin().Account(0)
    bip_obj_chain = bip_obj_acc.Change(Bip44Changes.CHAIN_EXT)

    # m/44'/0'/0'/0/i
    for i in range(limit):
        bip_obj_addr = bip_obj_chain.AddressIndex(i)
        address = bip_obj_addr.PublicKey().ToAddress()
        private = bip_obj_addr.PrivateKey().ToWif()
        acc = address if hide_private else f"{address} / {private}"
        click.echo(acc)
