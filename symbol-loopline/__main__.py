import click

from . import symbol_cert

@click.group()
def loopline():
    """symbol-shoesteing サポートツール"""
    pass

@loopline.command()
@click.option('--config', required=True, help='shoestring config のパス')
@click.option('--target', default='.', help='shoestring データのパス')
def showcert(config, target):
    """証明書を表示します"""
    symbol_cert.show(config, target)

if __name__ == '__main__':
    loopline()
