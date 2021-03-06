#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

"""Diffie-Hellman elliptic curve key agreement scheme.

Implementation of the Diffie-Hellman key agreement scheme using
elliptic curve cryptography. A key agreement scheme is used
by two entities to establish shared keying data, which will be
later utilized e.g. in symmetric cryptographic scheme.

The two entities must agree on the elliptic curve and key derivation
function to use.
"""

from hashlib import sha256
from math import ceil
from typing import Optional

from .alias import HashF, Point
from .curve import Curve, mult, secp256k1


def ansi_x9_63_kdf(
    z: bytes, size: int, hf: HashF, shared_info: Optional[bytes]
) -> bytes:
    """Return keying data according to ANSI-X9.63-KDF.

    Return a keying data octet sequence of the requested size according
    to ANSI-X9.63-KDF specifications for the key derivation function.

    http://www.secg.org/sec1-v2.pdf, section 3.6.1
    """
    hsize = hf().digest_size
    max_size = hsize * (2 ** 32 - 1)
    if size > max_size:
        raise ValueError(f"cannot derive a key larger than {max_size} bytes")
    K_temp = []
    for counter in range(1, ceil(size / hsize) + 1):
        h = hf()
        hash_input = (
            z
            + counter.to_bytes(4, byteorder="big")
            + (b"" if shared_info is None else shared_info)
        )
        h.update(hash_input)
        K_temp.append(h.digest())
    return b"".join(K_temp)[:size]


def diffie_hellman(
    dU: int,
    QV: Point,
    size: int,
    shared_info: Optional[bytes] = None,
    ec: Curve = secp256k1,
    hf: HashF = sha256,
) -> bytes:
    """Diffie-Hellman elliptic curve key agreement scheme.

    http://www.secg.org/sec1-v2.pdf, section 6.1
    """

    shared_secret_point = mult(dU, QV, ec)
    assert shared_secret_point[1] != 0, "invalid (INF) key"
    shared_secret_field_element = shared_secret_point[0]
    z = shared_secret_field_element.to_bytes(ec.psize, "big")
    return ansi_x9_63_kdf(z, size, hf, shared_info)
