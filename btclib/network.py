#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

"""Network constants and associated functions."""


import json
from collections import defaultdict
from dataclasses import dataclass, field
from os import path
from typing import Dict, List, Union

from dataclasses_json import DataClassJsonMixin, config

from .curve import CURVES, Curve


@dataclass(frozen=True)
class Network(DataClassJsonMixin):
    curve: Curve = field(
        metadata=config(encoder=lambda v: v.name, decoder=lambda v: CURVES[v])
    )
    # base58wif starts with 'K' or 'L' if compressed else '5'
    wif: bytes = field(
        metadata=config(encoder=lambda v: v.hex(), decoder=bytes.fromhex)
    )
    # base58address starts with '1'
    p2pkh: bytes = field(
        metadata=config(encoder=lambda v: v.hex(), decoder=bytes.fromhex)
    )
    # base58address starts with '3'
    p2sh: bytes = field(
        metadata=config(encoder=lambda v: v.hex(), decoder=bytes.fromhex)
    )
    # bech32address starts with 'bc1'
    p2w: str
    # slip132 "m / 44h / 0h" p2pkh or p2sh
    bip32_prv: bytes = field(
        metadata=config(encoder=lambda v: v.hex(), decoder=bytes.fromhex)
    )
    bip32_pub: bytes = field(
        metadata=config(encoder=lambda v: v.hex(), decoder=bytes.fromhex)
    )
    # slip132 "m / 49h / 0h" p2wpkh-p2sh (p2sh-wrapped legacy-segwit p2wpkh)
    slip132_p2wpkh_prv: bytes = field(
        metadata=config(encoder=lambda v: v.hex(), decoder=bytes.fromhex)
    )
    slip132_p2wpkh_pub: bytes = field(
        metadata=config(encoder=lambda v: v.hex(), decoder=bytes.fromhex)
    )
    # slip132 p2wsh-p2sh (p2sh-wrapped legacy-segwit p2wsh)
    slip132_p2wpkh_p2sh_prv: bytes = field(
        metadata=config(encoder=lambda v: v.hex(), decoder=bytes.fromhex)
    )
    slip132_p2wpkh_p2sh_pub: bytes = field(
        metadata=config(encoder=lambda v: v.hex(), decoder=bytes.fromhex)
    )
    # slip132 "m / 84h / 0h" p2wpkh (native-segwit p2wpkh)
    slip132_p2wsh_prv: bytes = field(
        metadata=config(encoder=lambda v: v.hex(), decoder=bytes.fromhex)
    )
    slip132_p2wsh_pub: bytes = field(
        metadata=config(encoder=lambda v: v.hex(), decoder=bytes.fromhex)
    )
    # slip132 p2wsh (native-segwit p2wsh)
    slip132_p2wsh_p2sh_prv: bytes = field(
        metadata=config(encoder=lambda v: v.hex(), decoder=bytes.fromhex)
    )
    slip132_p2wsh_p2sh_pub: bytes = field(
        metadata=config(encoder=lambda v: v.hex(), decoder=bytes.fromhex)
    )


NETWORKS: Dict[str, Network] = defaultdict()
datadir = path.join(path.dirname(__file__), "data")
for net in ("mainnet", "testnet", "regtest"):
    filename = path.join(datadir, net + ".json")
    with open(filename, "r") as f:
        NETWORKS[net] = Network.from_dict(json.load(f))


def network_from_key_value(key: str, prefix: Union[str, bytes, Curve]) -> str:
    """Return network string from (key, value) pair.

    Warning: when used on 'regtest' it mostly returns 'testnet',
    which is not a problem as long as it is used for
    WIF/Base58Address/BIP32xkey
    because the two networks share the same prefixes.
    """
    for net in NETWORKS:
        if getattr(NETWORKS[net], key) == prefix:
            return net
    raise ValueError(f"invalid value for network keyword '{key}': {prefix!r}")


_NETWORKS = [net for net in NETWORKS]
_P2PKH_PREFIXES = [NETWORKS[net].p2pkh for net in NETWORKS]
_P2SH_PREFIXES = [NETWORKS[net].p2sh for net in NETWORKS]

_XPRV_PREFIXES = [NETWORKS[net].bip32_prv for net in NETWORKS]
_XPUB_PREFIXES = [NETWORKS[net].bip32_pub for net in NETWORKS]

_P2WPKH_P2SH_PUB_PREFIXES = [NETWORKS[net].slip132_p2wpkh_p2sh_pub for net in NETWORKS]

_P2WPKH_PRV_PREFIXES = [NETWORKS[net].slip132_p2wpkh_prv for net in NETWORKS]
_P2WPKH_PUB_PREFIXES = [NETWORKS[net].slip132_p2wpkh_pub for net in NETWORKS]


def xpubversions_from_network(network: str) -> List[bytes]:
    network = network.strip().lower()
    return [
        NETWORKS[network].bip32_pub,
        NETWORKS[network].slip132_p2wsh_p2sh_pub,
        NETWORKS[network].slip132_p2wpkh_p2sh_pub,
        NETWORKS[network].slip132_p2wpkh_pub,
        NETWORKS[network].slip132_p2wsh_pub,
    ]


def xprvversions_from_network(network: str) -> List[bytes]:
    network = network.strip().lower()
    return [
        NETWORKS[network].bip32_prv,
        NETWORKS[network].slip132_p2wsh_p2sh_prv,
        NETWORKS[network].slip132_p2wpkh_p2sh_prv,
        NETWORKS[network].slip132_p2wpkh_prv,
        NETWORKS[network].slip132_p2wsh_prv,
    ]


_XPRV_VERSIONS_ALL = (
    xprvversions_from_network("mainnet") + xprvversions_from_network("testnet") * 2
)
_XPUB_VERSIONS_ALL = (
    xpubversions_from_network("mainnet") + xpubversions_from_network("testnet") * 2
)
n_versions = len(xprvversions_from_network("mainnet"))
_REPEATED_NETWORKS = (
    [_NETWORKS[0]] * n_versions
    + [_NETWORKS[1]] * n_versions
    + [_NETWORKS[2]] * n_versions
)


def network_from_xkeyversion(xkeyversion: bytes) -> str:
    """Return network string from the xkey version prefix.

    Warning: when used on 'regtest' it returns 'testnet', which is not
    a problem as long as it is used for WIF/Base58Address/BIP32Key
    because the two networks share the same prefixes.
    """
    try:
        index = _XPRV_VERSIONS_ALL.index(xkeyversion)
    except Exception:
        index = _XPUB_VERSIONS_ALL.index(xkeyversion)

    return _REPEATED_NETWORKS[index]


def curve_from_xkeyversion(xkeyversion: bytes) -> Curve:
    network = network_from_xkeyversion(xkeyversion)
    return NETWORKS[network].curve
