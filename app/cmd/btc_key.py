import click
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip39WordsNum, Bip44, Bip44Changes, Bip44Coins


@click.command()
@click.option("-m", "--mnemonic")
@click.option("-p", "--passphrase", default="")
@click.option("-l", "--limit", default=5)
@click.option("--print-private/--no-print-private", default=True)
def cli(mnemonic: str, passphrase: str, limit: int, print_private: bool):
    if not mnemonic:
        mnemonic = Bip39MnemonicGenerator.FromWordsNumber(Bip39WordsNum.WORDS_NUM_24)
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate(passphrase)

    click.echo(mnemonic + "\n")

    bip_obj_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
    bip_obj_acc = bip_obj_mst.Purpose().Coin().Account(0)
    bip_obj_chain = bip_obj_acc.Change(Bip44Changes.CHAIN_EXT)

    # m/44'/0'/0'/0/i
    for i in range(limit):
        bip_obj_addr = bip_obj_chain.AddressIndex(i)
        address = bip_obj_addr.PublicKey().ToAddress()
        private = bip_obj_addr.PrivateKey().ToWif()
        acc = f"{address} / {private}" if print_private else address
        click.echo(acc)
