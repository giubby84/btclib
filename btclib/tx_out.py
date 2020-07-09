#!/usr/bin/env python3

# Copyright (C) 2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

from typing import List, TypeVar, Type
from dataclasses import dataclass

from . import script, varint
from .alias import Token, BinaryData
from .utils import binaryio_from_binarydata

_TxOut = TypeVar("_TxOut", bound="TxOut")


@dataclass
class TxOut:
    nValue: int  # satoshis
    scriptPubKey: List[Token]

    @classmethod
    def deserialize(cls: Type[_TxOut], data: BinaryData) -> _TxOut:
        stream = binaryio_from_binarydata(data)
        nValue = int.from_bytes(stream.read(8), "little")
        script_length = varint.decode(stream)
        scriptPubKey = script.decode(stream.read(script_length))
        tx_out = cls(nValue=nValue, scriptPubKey=scriptPubKey)
        tx_out.assert_valid()
        return tx_out

    def serialize(self) -> bytes:
        out = self.nValue.to_bytes(8, "little")
        script_bytes = script.encode(self.scriptPubKey)
        out += varint.encode(len(script_bytes))
        out += script_bytes
        return out

    def assert_valid(self) -> None:
        if self.nValue < 0:
            raise ValueError(f"negative value: {self.nValue}")
        if 2099999997690000 < self.nValue:
            raise ValueError(f"value too high: {self.nValue}")
        if len(self.scriptPubKey) == 0:
            raise ValueError(f"empty scriptPubKey: {self.scriptPubKey}")
