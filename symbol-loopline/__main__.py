import click
from . import symbol_cert

@click.group()
def loopline():
    """symbol-shoesteing サポートツール"""
    pass

@loopline.command()
@click.option('--target', default='.', help='shoestring データのパス')
def showcert(target):
    """証明書を表示します"""
    symbol_cert.show(target)

if __name__ == '__main__':
    loopline()
