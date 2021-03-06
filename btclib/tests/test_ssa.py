#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

"Tests for `btclib.ssa` module."

import csv
import secrets
from hashlib import sha256 as hf
from os import path
from typing import List

import pytest

from btclib import ssa
from btclib.alias import INF, Point
from btclib.bip32 import BIP32KeyData
from btclib.curve import CURVES, double_mult, mult
from btclib.curvegroup import _mult
from btclib.numbertheory import mod_inv
from btclib.pedersen import second_generator
from btclib.secpoint import bytes_from_point
from btclib.tests.test_curve import low_card_curves
from btclib.utils import int_from_bits


def test_signature() -> None:
    ec = CURVES["secp256k1"]
    msg = "Satoshi Nakamoto"

    q, x_Q = ssa.gen_keys(0x01)
    sig = ssa.sign(msg, q)
    assert ssa.verify(msg, x_Q, sig)

    assert sig == ssa.deserialize(sig)

    ssa.assert_as_valid(msg, x_Q, sig)
    ssa.assert_as_valid(msg, x_Q, ssa.serialize(*sig))
    ssa.assert_as_valid(msg, x_Q, ssa.serialize(*sig).hex())

    msg_fake = "Craig Wright"
    assert not ssa.verify(msg_fake, x_Q, sig)
    err_msg = "signature verification failed"
    with pytest.raises(AssertionError, match=err_msg):
        ssa.assert_as_valid(msg_fake, x_Q, sig)

    _, x_Q_fake = ssa.gen_keys(0x02)
    assert not ssa.verify(msg, x_Q_fake, sig)
    err_msg = "y_K is not a quadratic residue"
    with pytest.raises(RuntimeError, match=err_msg):
        ssa.assert_as_valid(msg, x_Q_fake, sig)

    _, x_Q_fake = ssa.gen_keys(0x4)
    assert not ssa.verify(msg, x_Q_fake, sig)
    err_msg = "signature verification failed"
    with pytest.raises(AssertionError, match=err_msg):
        ssa.assert_as_valid(msg, x_Q_fake, sig)

    err_msg = "not a BIP340 public key"
    with pytest.raises(ValueError, match=err_msg):
        ssa.assert_as_valid(msg, INF, sig)  # type: ignore
    with pytest.raises(ValueError, match=err_msg):
        ssa.point_from_bip340pubkey(INF)  # type: ignore

    assert not ssa.verify(msg, x_Q, sig, CURVES["secp224k1"], hf)
    err_msg = "field prime is not equal to 3 mod 4: "
    with pytest.raises(ValueError, match=err_msg):
        ssa.assert_as_valid(msg, x_Q, sig, CURVES["secp224k1"], hf)

    sig_fake = (sig[0], sig[1], sig[1])
    assert not ssa.verify(msg, x_Q, sig_fake)  # type: ignore
    err_msg = "too many values to unpack "
    with pytest.raises(ValueError, match=err_msg):
        ssa.assert_as_valid(msg, x_Q, sig_fake)  # type: ignore

    sig_invalid = ec.p, sig[1]
    assert not ssa.verify(msg, x_Q, sig_invalid)
    err_msg = "x-coordinate not in 0..p-1: "
    with pytest.raises(ValueError, match=err_msg):
        ssa.assert_as_valid(msg, x_Q, sig_invalid)

    sig_invalid = sig[0], ec.p
    assert not ssa.verify(msg, x_Q, sig_invalid)
    err_msg = "scalar s not in 0..n-1: "
    with pytest.raises(ValueError, match=err_msg):
        ssa.assert_as_valid(msg, x_Q, sig_invalid)

    m_fake = b"\x00" * 31
    err_msg = "invalid size: 31 bytes instead of 32"
    with pytest.raises(ValueError, match=err_msg):
        ssa._assert_as_valid(m_fake, x_Q, sig)

    with pytest.raises(ValueError, match=err_msg):
        ssa._sign(m_fake, q)

    err_msg = "private key not in 1..n-1: "
    with pytest.raises(ValueError, match=err_msg):
        ssa.sign(msg, 0)

    # ephemeral key not in 1..n-1
    err_msg = "private key not in 1..n-1: "
    with pytest.raises(ValueError, match=err_msg):
        ssa.sign(msg, q, 0)
    with pytest.raises(ValueError, match=err_msg):
        ssa.sign(msg, q, ec.n)

    err_msg = "invalid zero challenge"
    with pytest.raises(ValueError, match=err_msg):
        ssa.__recover_pubkey(0, sig[0], sig[1], ec)


def test_bip340_vectors() -> None:
    """BIP340 (Schnorr) test vectors.

    https://github.com/bitcoin/bips/blob/master/bip-0340/test-vectors.csv
    """
    fname = "bip340_test_vectors.csv"
    filename = path.join(path.dirname(__file__), "test_data", fname)
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        # skip column headers while checking that there are 7 columns
        _, _, _, _, _, _, _ = reader.__next__()
        for row in reader:
            (index, seckey, pubkey, m, sig, result, comment) = row
            err_msg = f"Test vector #{int(index)}"
            if seckey != "":
                _, pubkey_actual = ssa.gen_keys(seckey)
                assert pubkey == hex(pubkey_actual).upper()[2:], err_msg

                sig_actual = ssa.serialize(*ssa._sign(m, seckey))
                assert sig == sig_actual.hex().upper(), err_msg

            if comment:
                err_msg += ": " + comment
            # TODO what's worng with xor-ing ?
            # assert (result == "TRUE") ^ ssa._verify(m, pubkey, sig), err_msg
            if result == "TRUE":
                assert ssa._verify(m, pubkey, sig), err_msg
            else:
                assert not ssa._verify(m, pubkey, sig), err_msg


def test_point_from_bip340pubkey() -> None:

    q, x_Q = ssa.gen_keys()
    P = mult(q)
    # Integer (int)
    assert ssa.point_from_bip340pubkey(x_Q) == P
    # Integer (bytes)
    assert ssa.point_from_bip340pubkey(x_Q.to_bytes(32, byteorder="big")) == P
    # Integer (hex-str)
    assert ssa.point_from_bip340pubkey(x_Q.to_bytes(32, byteorder="big").hex()) == P
    # tuple Point
    assert ssa.point_from_bip340pubkey(P) == P
    # 33 bytes
    assert ssa.point_from_bip340pubkey(bytes_from_point(P)) == P
    # 33 bytes hex-string
    assert ssa.point_from_bip340pubkey(bytes_from_point(P).hex()) == P
    # 65 bytes
    assert ssa.point_from_bip340pubkey(bytes_from_point(P, compressed=False)) == P
    # 65 bytes hex-string
    assert ssa.point_from_bip340pubkey(bytes_from_point(P, compressed=False).hex()) == P

    xpub_data = BIP32KeyData.deserialize(
        "xpub6H1LXWLaKsWFhvm6RVpEL9P4KfRZSW7abD2ttkWP3SSQvnyA8FSVqNTEcYFgJS2UaFcxupHiYkro49S8yGasTvXEYBVPamhGW6cFJodrTHy"
    )
    xpub_data.key = bytes_from_point(P)
    # BIP32KeyData
    assert ssa.point_from_bip340pubkey(xpub_data) == P
    # BIP32Key encoded str
    xpub = xpub_data.serialize()
    assert ssa.point_from_bip340pubkey(xpub) == P
    # BIP32Key str
    assert ssa.point_from_bip340pubkey(xpub.decode("ascii")) == P


def test_low_cardinality() -> None:
    "test low-cardinality curves for all msg/key pairs."

    # ec.n has to be prime to sign
    test_curves = [
        low_card_curves["ec13_11"],
        low_card_curves["ec13_19"],
        low_card_curves["ec17_13"],
        low_card_curves["ec17_23"],
        low_card_curves["ec19_13"],
        low_card_curves["ec19_23"],
        low_card_curves["ec23_19"],
        low_card_curves["ec23_31"],
    ]

    # only low cardinality test curves or it would take forever
    for ec in test_curves:
        # BIP340 Schnorr only applies to curve whose prime p = 3 %4
        if not ec.pIsThreeModFour:
            err_msg = "field prime is not equal to 3 mod 4: "
            with pytest.raises(ValueError, match=err_msg):
                ssa._sign(32 * b"\x00", 1, None, ec)
            continue
        for q in range(1, ec.n // 2):  # all possible private keys
            QJ = _mult(q, ec.GJ, ec)  # public key
            x_Q = ec._x_aff_from_jac(QJ)
            if not ec.has_square_y(QJ):
                q = ec.n - q
                QJ = ec.negate_jac(QJ)
            for k in range(1, ec.n // 2):  # all possible ephemeral keys
                RJ = _mult(k, ec.GJ, ec)
                r = ec._x_aff_from_jac(RJ)
                if not ec.has_square_y(RJ):
                    k = ec.n - k
                for e in range(ec.n):  # all possible challenges
                    s = (k + e * q) % ec.n

                    sig = ssa.__sign(e, q, k, r, ec)
                    assert (r, s) == sig
                    # valid signature must validate
                    ssa.__assert_as_valid(e, QJ, r, s, ec)

                    # if e == 0 then the sig is valid for all {q, Q}
                    # no public key can be recovered
                    if e == 0:
                        err_msg = "invalid zero challenge"
                        with pytest.raises(ValueError, match=err_msg):
                            ssa.__recover_pubkey(e, r, s, ec)
                    else:
                        assert x_Q == ssa.__recover_pubkey(e, r, s, ec)


def test_crack_prvkey() -> None:

    ec = CURVES["secp256k1"]

    q = 0x19E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725
    x_Q = mult(q)[0]

    msg1_str = "Paolo is afraid of ephemeral random numbers"
    msg1 = hf(msg1_str.encode()).digest()
    k, _ = ssa._det_nonce(msg1, q)
    sig1 = ssa._sign(msg1, q, k)

    msg2_str = "and Paolo is right to be afraid"
    msg2 = hf(msg2_str.encode()).digest()
    # reuse same k
    sig2 = ssa._sign(msg2, q, k)

    qc, kc = ssa._crack_prvkey(msg1, sig1, msg2, sig2, x_Q)
    assert q in (qc, ec.n - qc)
    assert k in (kc, ec.n - kc)

    with pytest.raises(ValueError, match="not the same r in signatures"):
        ssa._crack_prvkey(msg1, sig1, msg2, (16, sig1[1]), x_Q)

    with pytest.raises(ValueError, match="identical signatures"):
        ssa._crack_prvkey(msg1, sig1, msg1, sig1, x_Q)


def test_batch_validation() -> None:

    ec = CURVES["secp256k1"]

    hsize = hf().digest_size
    hlen = hsize * 8

    ms = []
    Qs = []
    sigs = []
    ms.append(secrets.randbits(hlen).to_bytes(hsize, "big"))
    q = 1 + secrets.randbelow(ec.n - 1)
    # bytes version
    Qs.append(mult(q, ec.G, ec)[0])
    sigs.append(ssa._sign(ms[0], q, None, ec, hf))
    # test with only 1 sig
    ssa._batch_verify(ms, Qs, sigs, ec, hf)
    for _ in range(3):
        m = secrets.randbits(hlen).to_bytes(hsize, "big")
        ms.append(m)
        q = 1 + secrets.randbelow(ec.n - 1)
        # Point version
        Qs.append(mult(q, ec.G, ec)[0])
        sigs.append(ssa._sign(m, q, None, ec, hf))
    ssa._batch_verify(ms, Qs, sigs, ec, hf)
    assert ssa.batch_verify(ms, Qs, sigs, ec, hf)

    ms.append(ms[0])
    sigs.append(sigs[1])
    Qs.append(Qs[0])
    assert not ssa.batch_verify(ms, Qs, sigs, ec, hf)
    err_msg = "signature verification precondition failed"
    with pytest.raises(ValueError, match=err_msg):
        ssa._batch_verify(ms, Qs, sigs, ec, hf)
    sigs[-1] = sigs[0]  # valid again

    ms[-1] = ms[0][:-1]
    err_msg = "invalid size: 31 bytes instead of 32"
    with pytest.raises(ValueError, match=err_msg):
        ssa._batch_verify(ms, Qs, sigs, ec, hf)
    ms[-1] = ms[0]  # valid again

    ms.append(ms[0])  # add extra message
    err_msg = "mismatch between number of pubkeys "
    with pytest.raises(ValueError, match=err_msg):
        ssa._batch_verify(ms, Qs, sigs, ec, hf)
    ms.pop()  # valid again

    sigs.append(sigs[0])  # add extra sig
    err_msg = "mismatch between number of pubkeys "
    with pytest.raises(ValueError, match=err_msg):
        ssa._batch_verify(ms, Qs, sigs, ec, hf)
    sigs.pop()  # valid again

    err_msg = "field prime is not equal to 3 mod 4: "
    with pytest.raises(ValueError, match=err_msg):
        ssa._batch_verify(ms, Qs, sigs, CURVES["secp224k1"], hf)


def test_musig() -> None:
    """testing 3-of-3 MuSig.

    https://github.com/ElementsProject/secp256k1-zkp/blob/secp256k1-zkp/src/modules/musig/musig.md
    https://blockstream.com/2019/02/18/musig-a-new-multisignature-standard/
    https://eprint.iacr.org/2018/068
    https://blockstream.com/2018/01/23/musig-key-aggregation-schnorr-signatures.html
    https://medium.com/@snigirev.stepan/how-schnorr-signatures-may-improve-bitcoin-91655bcb4744
    """

    ec = CURVES["secp256k1"]

    m = hf(b"message to sign").digest()

    # the signers private and public keys,
    # including both the curve Point and the BIP340-Schnorr public key
    q1, x_Q1_int = ssa.gen_keys()
    x_Q1 = x_Q1_int.to_bytes(ec.psize, "big")

    q2, x_Q2_int = ssa.gen_keys()
    x_Q2 = x_Q2_int.to_bytes(ec.psize, "big")

    q3, x_Q3_int = ssa.gen_keys()
    x_Q3 = x_Q3_int.to_bytes(ec.psize, "big")

    # (non interactive) key setup
    # this is MuSig core: the rest is just Schnorr signature additivity
    # 1. lexicographic sorting of public keys
    keys: List[bytes] = list()
    keys.append(x_Q1)
    keys.append(x_Q2)
    keys.append(x_Q3)
    keys.sort()
    # 2. coefficients
    prefix = b"".join(keys)
    a1 = int_from_bits(hf(prefix + x_Q1).digest(), ec.nlen) % ec.n
    a2 = int_from_bits(hf(prefix + x_Q2).digest(), ec.nlen) % ec.n
    a3 = int_from_bits(hf(prefix + x_Q3).digest(), ec.nlen) % ec.n
    # 3. aggregated public key
    Q1 = mult(q1)
    Q2 = mult(q2)
    Q3 = mult(q3)
    Q = ec.add(double_mult(a1, Q1, a2, Q2), mult(a3, Q3))
    if not ec.has_square_y(Q):
        # print("Q has been negated")
        a1 = ec.n - a1  # pragma: no cover
        a2 = ec.n - a2  # pragma: no cover
        a3 = ec.n - a3  # pragma: no cover

    # ready to sign: nonces and nonce commitments
    k1, _ = ssa.gen_keys()
    K1 = mult(k1)

    k2, _ = ssa.gen_keys()
    K2 = mult(k2)

    k3, _ = ssa.gen_keys()
    K3 = mult(k3)

    # exchange {K_i} (interactive)

    # computes s_i (non interactive)
    # WARNING: signers must exchange the nonces commitments {K_i}
    # before sharing {s_i}

    # same for all signers
    K = ec.add(ec.add(K1, K2), K3)
    if not ec.has_square_y(K):
        k1 = ec.n - k1  # pragma: no cover
        k2 = ec.n - k2  # pragma: no cover
        k3 = ec.n - k3  # pragma: no cover
    r = K[0]
    e = ssa._challenge(m, Q[0], r, ec, hf)
    s1 = (k1 + e * a1 * q1) % ec.n
    s2 = (k2 + e * a2 * q2) % ec.n
    s3 = (k3 + e * a3 * q3) % ec.n

    # exchange s_i (interactive)

    # finalize signature (non interactive)
    s = (s1 + s2 + s3) % ec.n
    sig = r, s
    # check signature is valid
    ssa._assert_as_valid(m, Q[0], sig, ec, hf)


def test_threshold() -> None:
    "testing 2-of-3 threshold signature (Pedersen secret sharing)"

    ec = CURVES["secp256k1"]

    # parameters
    m = 2
    H = second_generator(ec, hf)

    # FIRST PHASE: key pair generation ###################################

    # 1.1 signer one acting as the dealer
    commits1: List[Point] = list()
    q1, _ = ssa.gen_keys()
    q1_prime, _ = ssa.gen_keys()
    commits1.append(double_mult(q1_prime, H, q1, ec.G))
    # sharing polynomials
    f1 = [q1]
    f1_prime = [q1_prime]
    for i in range(1, m):
        f1.append(ssa.gen_keys()[0])
        f1_prime.append(ssa.gen_keys()[0])
        commits1.append(double_mult(f1_prime[i], H, f1[i], ec.G))
    # shares of the secret
    alpha12 = 0  # share of q1 belonging to signer two
    alpha12_prime = 0
    alpha13 = 0  # share of q1 belonging to signer three
    alpha13_prime = 0
    for i in range(m):
        alpha12 += (f1[i] * pow(2, i)) % ec.n
        alpha12_prime += (f1_prime[i] * pow(2, i)) % ec.n
        alpha13 += (f1[i] * pow(3, i)) % ec.n
        alpha13_prime += (f1_prime[i] * pow(3, i)) % ec.n
    # signer two verifies consistency of his share
    RHS = INF
    for i in range(m):
        RHS = ec.add(RHS, mult(pow(2, i), commits1[i]))
    t = double_mult(alpha12_prime, H, alpha12, ec.G)
    assert t == RHS, "signer one is cheating"
    # signer three verifies consistency of his share
    RHS = INF
    for i in range(m):
        RHS = ec.add(RHS, mult(pow(3, i), commits1[i]))
    t = double_mult(alpha13_prime, H, alpha13, ec.G)
    assert t == RHS, "signer one is cheating"

    # 1.2 signer two acting as the dealer
    commits2: List[Point] = list()
    q2, _ = ssa.gen_keys()
    q2_prime, _ = ssa.gen_keys()
    commits2.append(double_mult(q2_prime, H, q2, ec.G))
    # sharing polynomials
    f2 = [q2]
    f2_prime = [q2_prime]
    for i in range(1, m):
        f2.append(ssa.gen_keys()[0])
        f2_prime.append(ssa.gen_keys()[0])
        commits2.append(double_mult(f2_prime[i], H, f2[i], ec.G))
    # shares of the secret
    alpha21 = 0  # share of q2 belonging to signer one
    alpha21_prime = 0
    alpha23 = 0  # share of q2 belonging to signer three
    alpha23_prime = 0
    for i in range(m):
        alpha21 += (f2[i] * pow(1, i)) % ec.n
        alpha21_prime += (f2_prime[i] * pow(1, i)) % ec.n
        alpha23 += (f2[i] * pow(3, i)) % ec.n
        alpha23_prime += (f2_prime[i] * pow(3, i)) % ec.n
    # signer one verifies consistency of his share
    RHS = INF
    for i in range(m):
        RHS = ec.add(RHS, mult(pow(1, i), commits2[i]))
    t = double_mult(alpha21_prime, H, alpha21, ec.G)
    assert t == RHS, "signer two is cheating"
    # signer three verifies consistency of his share
    RHS = INF
    for i in range(m):
        RHS = ec.add(RHS, mult(pow(3, i), commits2[i]))
    t = double_mult(alpha23_prime, H, alpha23, ec.G)
    assert t == RHS, "signer two is cheating"

    # 1.3 signer three acting as the dealer
    commits3: List[Point] = list()
    q3, _ = ssa.gen_keys()
    q3_prime, _ = ssa.gen_keys()
    commits3.append(double_mult(q3_prime, H, q3, ec.G))
    # sharing polynomials
    f3 = [q3]
    f3_prime = [q3_prime]
    for i in range(1, m):
        f3.append(ssa.gen_keys()[0])
        f3_prime.append(ssa.gen_keys()[0])
        commits3.append(double_mult(f3_prime[i], H, f3[i], ec.G))
    # shares of the secret
    alpha31 = 0  # share of q3 belonging to signer one
    alpha31_prime = 0
    alpha32 = 0  # share of q3 belonging to signer two
    alpha32_prime = 0
    for i in range(m):
        alpha31 += (f3[i] * pow(1, i)) % ec.n
        alpha31_prime += (f3_prime[i] * pow(1, i)) % ec.n
        alpha32 += (f3[i] * pow(2, i)) % ec.n
        alpha32_prime += (f3_prime[i] * pow(2, i)) % ec.n
    # signer one verifies consistency of his share
    RHS = INF
    for i in range(m):
        RHS = ec.add(RHS, mult(pow(1, i), commits3[i]))
    t = double_mult(alpha31_prime, H, alpha31, ec.G)
    assert t == RHS, "signer three is cheating"
    # signer two verifies consistency of his share
    RHS = INF
    for i in range(m):
        RHS = ec.add(RHS, mult(pow(2, i), commits3[i]))
    t = double_mult(alpha32_prime, H, alpha32, ec.G)
    assert t == RHS, "signer three is cheating"
    # shares of the secret key q = q1 + q2 + q3
    alpha1 = (alpha21 + alpha31) % ec.n
    alpha2 = (alpha12 + alpha32) % ec.n
    alpha3 = (alpha13 + alpha23) % ec.n
    for i in range(m):
        alpha1 += (f1[i] * pow(1, i)) % ec.n
        alpha2 += (f2[i] * pow(2, i)) % ec.n
        alpha3 += (f3[i] * pow(3, i)) % ec.n

    # 1.4 it's time to recover the public key
    # each participant i = 1, 2, 3 shares Qi as follows
    # Q = Q1 + Q2 + Q3 = (q1 + q2 + q3) G
    A1: List[Point] = list()
    A2: List[Point] = list()
    A3: List[Point] = list()
    for i in range(m):
        A1.append(mult(f1[i]))
        A2.append(mult(f2[i]))
        A3.append(mult(f3[i]))
    # signer one checks others' values
    RHS2 = INF
    RHS3 = INF
    for i in range(m):
        RHS2 = ec.add(RHS2, mult(pow(1, i), A2[i]))
        RHS3 = ec.add(RHS3, mult(pow(1, i), A3[i]))
    assert mult(alpha21) == RHS2, "signer two is cheating"
    assert mult(alpha31) == RHS3, "signer three is cheating"
    # signer two checks others' values
    RHS1 = INF
    RHS3 = INF
    for i in range(m):
        RHS1 = ec.add(RHS1, mult(pow(2, i), A1[i]))
        RHS3 = ec.add(RHS3, mult(pow(2, i), A3[i]))
    assert mult(alpha12) == RHS1, "signer one is cheating"
    assert mult(alpha32) == RHS3, "signer three is cheating"
    # signer three checks others' values
    RHS1 = INF
    RHS2 = INF
    for i in range(m):
        RHS1 = ec.add(RHS1, mult(pow(3, i), A1[i]))
        RHS2 = ec.add(RHS2, mult(pow(3, i), A2[i]))
    assert mult(alpha13) == RHS1, "signer one is cheating"
    assert mult(alpha23) == RHS2, "signer two is cheating"
    # commitment at the global sharing polynomial
    A: List[Point] = list()
    for i in range(m):
        A.append(ec.add(A1[i], ec.add(A2[i], A3[i])))

    # aggregated public key
    Q = A[0]
    if not ec.has_square_y(Q):
        # print('Q has been negated')
        A[1] = ec.negate(A[1])  # pragma: no cover
        alpha1 = ec.n - alpha1  # pragma: no cover
        alpha2 = ec.n - alpha2  # pragma: no cover
        alpha3 = ec.n - alpha3  # pragma: no cover
        Q = ec.negate(Q)  # pragma: no cover

    # SECOND PHASE: generation of the nonces' pair  ######################
    # Assume signer one and three want to sign

    msg = "message to sign"

    # 2.1 signer one acting as the dealer
    commits1 = []
    k1, _ = ssa.det_nonce(msg, q1, ec, hf)
    k1_prime, _ = ssa.det_nonce(msg, q1_prime, ec, hf)
    commits1.append(double_mult(k1_prime, H, k1, ec.G))
    # sharing polynomials
    f1 = [k1]
    f1_prime = [k1_prime]
    for i in range(1, m):
        f1.append(ssa.gen_keys()[0])
        f1_prime.append(ssa.gen_keys()[0])
        commits1.append(double_mult(f1_prime[i], H, f1[i], ec.G))
    # shares of the secret
    beta13 = 0  # share of k1 belonging to signer three
    beta13_prime = 0
    for i in range(m):
        beta13 += (f1[i] * pow(3, i)) % ec.n
        beta13_prime += (f1_prime[i] * pow(3, i)) % ec.n
    # signer three verifies consistency of his share
    RHS = INF
    for i in range(m):
        RHS = ec.add(RHS, mult(pow(3, i), commits1[i]))
    t = double_mult(beta13_prime, H, beta13, ec.G)
    assert t == RHS, "signer one is cheating"

    # 2.2 signer three acting as the dealer
    commits3 = []
    k3, _ = ssa.det_nonce(msg, q3, ec, hf)
    k3_prime, _ = ssa.det_nonce(msg, q3_prime, ec, hf)
    commits3.append(double_mult(k3_prime, H, k3, ec.G))
    # sharing polynomials
    f3 = [k3]
    f3_prime = [k3_prime]
    for i in range(1, m):
        f3.append(ssa.gen_keys()[0])
        f3_prime.append(ssa.gen_keys()[0])
        commits3.append(double_mult(f3_prime[i], H, f3[i], ec.G))
    # shares of the secret
    beta31 = 0  # share of k3 belonging to signer one
    beta31_prime = 0
    for i in range(m):
        beta31 += (f3[i] * pow(1, i)) % ec.n
        beta31_prime += (f3_prime[i] * pow(1, i)) % ec.n
    # signer one verifies consistency of his share
    RHS = INF
    for i in range(m):
        RHS = ec.add(RHS, mult(pow(1, i), commits3[i]))
    t = double_mult(beta31_prime, H, beta31, ec.G)
    assert t == RHS, "signer three is cheating"

    # 2.3 shares of the secret nonce
    beta1 = beta31 % ec.n
    beta3 = beta13 % ec.n
    for i in range(m):
        beta1 += (f1[i] * pow(1, i)) % ec.n
        beta3 += (f3[i] * pow(3, i)) % ec.n

    # 2.4 it's time to recover the public nonce
    # each participant i = 1, 3 shares Qi as follows
    B1: List[Point] = list()
    B3: List[Point] = list()
    for i in range(m):
        B1.append(mult(f1[i]))
        B3.append(mult(f3[i]))

    # signer one checks values from signer three
    RHS3 = INF
    for i in range(m):
        RHS3 = ec.add(RHS3, mult(pow(1, i), B3[i]))
    assert mult(beta31) == RHS3, "signer three is cheating"

    # signer three checks values from signer one
    RHS1 = INF
    for i in range(m):
        RHS1 = ec.add(RHS1, mult(pow(3, i), B1[i]))
    assert mult(beta13) == RHS1, "signer one is cheating"

    # commitment at the global sharing polynomial
    B: List[Point] = list()
    for i in range(m):
        B.append(ec.add(B1[i], B3[i]))

    # aggregated public nonce
    K = B[0]
    if not ec.has_square_y(K):
        # print('K has been negated')
        B[1] = ec.negate(B[1])  # pragma: no cover
        beta1 = ec.n - beta1  # pragma: no cover
        beta3 = ec.n - beta3  # pragma: no cover
        K = ec.negate(K)  # pragma: no cover

    # PHASE THREE: signature generation ###

    # partial signatures
    e = ssa.challenge(msg, Q[0], K[0], ec, hf)
    gamma1 = (beta1 + e * alpha1) % ec.n
    gamma3 = (beta3 + e * alpha3) % ec.n

    # each participant verifies the other partial signatures

    # signer one
    RHS3 = ec.add(K, mult(e, Q))
    for i in range(1, m):
        temp = double_mult(pow(3, i), B[i], e * pow(3, i), A[i])
        RHS3 = ec.add(RHS3, temp)
    assert mult(gamma3) == RHS3, "signer three is cheating"

    # signer three
    RHS1 = ec.add(K, mult(e, Q))
    for i in range(1, m):
        temp = double_mult(pow(1, i), B[i], e * pow(1, i), A[i])
        RHS1 = ec.add(RHS1, temp)
    assert mult(gamma1) == RHS1, "signer one is cheating"

    # PHASE FOUR: aggregating the signature ###
    omega1 = 3 * mod_inv(3 - 1, ec.n) % ec.n
    omega3 = 1 * mod_inv(1 - 3, ec.n) % ec.n
    sigma = (gamma1 * omega1 + gamma3 * omega3) % ec.n

    sig = K[0], sigma

    assert ssa.verify(msg, Q[0], sig)

    # ADDITIONAL PHASE: reconstruction of the private key ###
    secret = (omega1 * alpha1 + omega3 * alpha3) % ec.n
    assert (q1 + q2 + q3) % ec.n in (secret, ec.n - secret)
