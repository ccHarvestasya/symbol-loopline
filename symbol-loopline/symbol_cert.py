import os
import click
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from symbolchain.facade.SymbolFacade import SymbolFacade
from symbolchain.sc import PublicKey
from collections import namedtuple

CertInfo = namedtuple("CertInfo", ["publicKey", "address", "validUntil"])

def get_cert_info(network_type, cert_path):
    # ファイルが存在するか確認
    if not os.path.exists(cert_path):
        click.echo(f"Error: Certificate file does not exist at {cert_path}")
        return

    # PEM形式の証明書ファイルを読み込む
    with open(cert_path, "rb") as f:
        pem_data = f.read()

    # 証明書をパース
    cert = x509.load_pem_x509_certificate(pem_data, default_backend())

    # 公開鍵を取得
    public_key = cert.public_key()

    # 公開鍵を16進数文字列で出力
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    hex_public_key = public_key_bytes.hex()

    # 公開鍵の先頭32文字を除外し、大文字に変換
    truncated_hex_public_key = hex_public_key[24:].upper()

    # 証明書の有効期限を取得
    # not_valid_before = cert.not_valid_before
    not_valid_after = cert.not_valid_after_utc

    # 公開鍵をSymbolFacadeを使用してアドレスに変換
    facade = SymbolFacade(network_type)
    address = facade.network.public_key_to_address(PublicKey(truncated_hex_public_key))

    return CertInfo(
        publicKey=truncated_hex_public_key,
        address=address,
        validUntil=not_valid_after
    )
    

def show(target):
    # targetの末尾に/がある場合は削除
    if target.endswith('/'):
        target = target[:-1]

    # certInfoを取得
    main_cert = get_cert_info("testnet", os.path.join(target, "keys/cert/ca.crt.pem"))
    node_cert = get_cert_info("testnet", os.path.join(target, "keys/cert/node.crt.pem"))

    # 結果を出力
    click.echo(f"Main Certificate:")
    click.echo(f"  Public Key  : {main_cert.publicKey}")
    click.echo(f"  Address     : {main_cert.address}")
    click.echo(f"  Valid Until : {main_cert.validUntil}")
    click.echo(f"Node Certificate:")
    click.echo(f"  Public Key  : {node_cert.publicKey}")
    click.echo(f"  Address     : {node_cert.address}")
    click.echo(f"  Valid Until : {node_cert.validUntil}")
