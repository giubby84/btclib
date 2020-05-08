#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

"""Elliptic curves.

* SEC 2 v.2 curves
  http://www.secg.org/sec2-v2.pdf
* SEC 2 v.1 curves, removed from SEC 2 v.2 as insecure ones
  http://www.secg.org/SEC2-Ver-1.0.pdf
* Federal Information Processing Standards Publication 186-4
  (NIST) curves
  https://oag.ca.gov/sites/all/files/agweb/pdfs/erds1/fips_pub_07_2013.pdf
* Brainpool standard curves
  https://tools.ietf.org/html/rfc5639
* test curves with very low cardinality

"""

# scroll down at the end of the file for 'relevant' code

from .curve import Curve

# SEC 2 v.1 curves, removed from SEC 2 v.2 as insecure ones
# http://www.secg.org/SEC2-Ver-1.0.pdf

__p = (2**128 - 3) // 76439
__a = 0xDB7C2ABF62E35E668076BEAD2088
__b = 0x659EF8BA043916EEDE8911702B22
__Gx = 0x09487239995A5EE76B55F9C2F098
__Gy = 0xA89CE5AF8724C0A23E0E0FF77500
__n = 0xDB7C2ABF62E35E7628DFAC6561C5
__h = 1
secp112r1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__p = (2**128 - 3) // 76439
__a = 0x6127C24C05F38A0AAAF65C0EF02C
__b = 0x51DEF1815DB5ED74FCC34C85D709
__Gx = 0x4BA30AB5E892B4E1649DD0928643
__Gy = 0xADCD46F5882E3747DEF36E956E97
__n = 0x36DF0AAFD8B8D7597CA10520D04B
__h = 4
secp112r2 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, False)

__p = 2**128 - 2**97 - 1
__a = 0xFFFFFFFDFFFFFFFFFFFFFFFFFFFFFFFC
__b = 0xE87579C11079F43DD824993C2CEE5ED3
__Gx = 0x161FF7528B899B2D0C28607CA52C5B86
__Gy = 0xCF5AC8395BAFEB13C02DA292DDED7A83
__n = 0xFFFFFFFE0000000075A30D1B9038A115
__h = 1
secp128r1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__p = 2**128 - 2**97 - 1
__a = 0xD6031998D1B3BBFEBF59CC9BBFF9AEE1
__b = 0x5EEEFCA380D02919DC2C6558BB6D8A5D
__Gx = 0x7B6AA5D85E572983E6FB32A7CDEBC140
__Gy = 0x27B6916A894D3AEE7106FE805FC34B44
__n = 0x3FFFFFFF7FFFFFFFBE0024720613B5A3
__h = 4
secp128r2 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, False)

__p = 2**160 - 2**32 - 2**14 - 2**12 - 2**9 - 2**8 - 2**7 - 2**3 - 2**2 - 1
__a = 0x0000000000000000000000000000000000000000
__b = 0x0000000000000000000000000000000000000007
__Gx = 0x3B4C382CE37AA192A4019E763036F4F5DD4D7EBB
__Gy = 0x938CF935318FDCED6BC28286531733C3F03C4FEE
__n = 0x0100000000000000000001B8FA16DFAB9ACA16B6B3
__h = 1
secp160k1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__p = 2**160 - 2**31 - 1
__a = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7FFFFFFC
__b = 0x1C97BEFC54BD7A8B65ACF89F81D4D4ADC565FA45
__Gx = 0x4A96B5688EF573284664698968C38BB913CBFC82
__Gy = 0x23A628553168947D59DCC912042351377AC5FB32
__n = 0x0100000000000000000001F4C8F927AED3CA752257
__h = 1
secp160r1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__p = 2**160 - 2**32 - 2**14 - 2**12 - 2**9 - 2**8 - 2**7 - 2**3 - 2**2 - 1
__a = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFAC70
__b = 0xB4E134D3FB59EB8BAB57274904664D5AF50388BA
__Gx = 0x52DCB034293A117E1F4FF11B30F7199D3144CE6D
__Gy = 0xFEAFFEF2E331F296E071FA0DF9982CFEA7D43F2E
__n = 0x0100000000000000000000351EE786A818F3A1A16B
__h = 1
secp160r2 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)


# curves included in both SEC 2 v.1 and SEC 2 v.2
# http://www.secg.org/sec2-v2.pdf

__p = 2**192 - 2**32 - 2**12 - 2**8 - 2**7 - 2**6 - 2**3 - 1
__a = 0
__b = 3
__Gx = 0xDB4FF10EC057E9AE26B07D0280B7F4341DA5D1B1EAE06C7D
__Gy = 0x9B2F2F6D9C5628A7844163D015BE86344082AA88D95E2F9D
__n = 0xFFFFFFFFFFFFFFFFFFFFFFFE26F2FC170F69466A74DEFD8D
__h = 1
secp192k1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__p = 2**192 - 2**64 - 1
__a = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFC
__b = 0x64210519E59C80E70FA7E9AB72243049FEB8DEECC146B9B1
__Gx = 0x188DA80EB03090F67CBF20EB43A18800F4FF0AFD82FF1012
__Gy = 0x07192B95FFC8DA78631011ED6B24CDD573F977A11E794811
__n = 0xFFFFFFFFFFFFFFFFFFFFFFFF99DEF836146BC9B1B4D22831
__h = 1
secp192r1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__p = 2**224 - 2**32 - 2**12 - 2**11 - 2**9 - 2**7 - 2**4 - 2 - 1
__a = 0
__b = 5
__Gx = 0xA1455B334DF099DF30FC28A169A467E9E47075A90F7E650EB6B7A45C
__Gy = 0x7E089FED7FBA344282CAFBD6F7E319F7C0B0BD59E2CA4BDB556D61A5
__n = 0x010000000000000000000000000001DCE8D2EC6184CAF0A971769FB1F7
__h = 1
secp224k1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__p = 2**224 - 2**96 + 1
__a = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFE
__b = 0xB4050A850C04B3ABF54132565044B0B7D7BFD8BA270B39432355FFB4
__Gx = 0xB70E0CBD6BB4BF7F321390B94A03C1D356C21122343280D6115C1D21
__Gy = 0xBD376388B5F723FB4C22DFE6CD4375A05A07476444D5819985007E34
__n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFF16A2E0B8F03E13DD29455C5C2A3D
__h = 1
secp224r1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

# bitcoin curve
__p = 2**256 - 2**32 - 977
__a = 0
__b = 7
__Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
__Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
__n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
__h = 1
secp256k1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__p = 2**256 - 2**224 + 2**192 + 2**96 - 1
__a = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
__b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
__Gx = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
__Gy = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5
__n = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
__h = 1
secp256r1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__p = 2**384 - 2**128 - 2**96 + 2**32 - 1
__a = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFC
__b = 0xB3312FA7E23EE7E4988E056BE3F82D19181D9C6EFE8141120314088F5013875AC656398D8A2ED19D2A85C8EDD3EC2AEF
__Gx = 0xAA87CA22BE8B05378EB1C71EF320AD746E1D3B628BA79B9859F741E082542A385502F25DBF55296C3A545E3872760AB7
__Gy = 0x3617DE4A96262C6F5D9E98BF9292DC29F8F41DBD289A147CE9DA3113B5F0B8C00A60B1CE1D7E819D7A431D7C90EA0E5F
__n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF581A0DB248B0A77AECEC196ACCC52973
__h = 1
secp384r1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__p = 2**521 - 1
__a = 0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC
__b = 0x0051953EB9618E1C9A1F929A21A0B68540EEA2DA725B99B315F3B8B489918EF109E156193951EC7E937B1652C0BD3BB1BF073573DF883D2C34F1EF451FD46B503F00
__Gx = 0x00C6858E06B70404E9CD9E3ECB662395B4429C648139053FB521F828AF606B4D3DBAA14B5E77EFE75928FE1DC127A2FFA8DE3348B3C1856A429BF97E7E31C2E5BD66
__Gy = 0x011839296A789A3BC0045C8A5FB42C7D1BD998F54449579B446817AFBD17273E662C97EE72995EF42640C550B9013FAD0761353C7086A272C24088BE94769FD16650
__n = 0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA51868783BF2F966B7FCC0148F709A5D03BB5C9B8899C47AEBB6FB71E91386409
__h = 1
secp521r1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

# FIPS PUB 186-4
# FEDERAL INFORMATION PROCESSING STANDARDS PUBLICATION
# Digital Signature Standard (DSS)
# https://oag.ca.gov/sites/all/files/agweb/pdfs/erds1/fips_pub_07_2013.pdf

__p = 6277101735386680763835789423207666416083908700390324961279
__n = 6277101735386680763835789423176059013767194773182842284081
__SEED = 0x3045ae6fc8422f64ed579528d38120eae12196d5
__c = 0x3099d2bbbfcb2538542dcd5fb078b6ef5f3d6fe2c745de65
__b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1
__Gx = 0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012
__Gy = 0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811
nistp192 = Curve(__p, __p - 3, __b, (__Gx, __Gy), __n, 1, True)

__p = 26959946667150639794667015087019630673557916260026308143510066298881
__n = 26959946667150639794667015087019625940457807714424391721682722368061
__SEED = 0xbd71344799d5c7fcdc45b59fa3b9ab8f6a948bc5
__c = 0x5b056c7e11dd68f40469ee7f3c7a7d74f7d121116506d031218291fb
__b = 0xb4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4
__Gx = 0xb70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21
__Gy = 0xbd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34
nistp224 = Curve(__p, __p - 3, __b, (__Gx, __Gy), __n, 1, True)

__p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
__n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
__SEED = 0xc49d360886e704936a6678e1139d26b7819f7e90
__c = 0x7efba1662985be9403cb055c75d4f7e0ce8d84a9c5114abcaf3177680104fa0d
__b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
__Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
__Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
nistp256 = Curve(__p, __p - 3, __b, (__Gx, __Gy), __n, 1, True)

__p = 39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112319
__n = 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643
__SEED = 0xa335926aa319a27a1d00896a6773a4827acdac73
__c = 0x79d1e655f868f02fff48dcdee14151ddb80643c1406d0ca10dfe6fc52009540a495e8042ea5f744f6e184667cc722483
__b = 0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef
__Gx = 0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7
__Gy = 0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f
nistp384 = Curve(__p, __p - 3, __b, (__Gx, __Gy), __n, 1, True)

__p = 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151
__n = 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449
__SEED = 0xd09e8800291cb85396cc6717393284aaa0da64ba
__c = 0x0b48bfa5f420a34949539d2bdfc264eeeeb077688e44fbf0ad8f6d0edb37bd6b533281000518e19f1b9ffbe0fe9ed8a3c2200b8f875e523868c70c1e5bf55bad637
__b = 0x051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00
__Gx = 0x0c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66
__Gy = 0x11839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650
nistp521 = Curve(__p, __p - 3, __b, (__Gx, __Gy), __n, 1, True)


# Elliptic Curve Cryptography (ECC)
# Brainpool Standard Curves and Curve Generation
# https://tools.ietf.org/html/rfc5639


__p = 0xE95E4A5F737059DC60DFC7AD95B3D8139515620F
__a = 0x340E7BE2A280EB74E2BE61BADA745D97E8F7C300
__b = 0x1E589A8595423412134FAA2DBDEC95C8D8675E58
__Gx = 0xBED5AF16EA3F6A4F62938C4631EB5AF7BDBCDBC3
__Gy = 0x1667CB477A1A8EC338F94741669C976316DA6321
__n = 0xE95E4A5F737059DC60DF5991D45029409E60FC09
__h = 1
bpp160r1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__Z = 0x24DBFF5DEC9B986BBFE5295A29BFBAE45E0F5D0B
__a = 0xE95E4A5F737059DC60DFC7AD95B3D8139515620C
__b = 0x7A556B6DAE535B7B51ED2C4D7DAA7A0B5C55F380
__Gx = 0xB199B13B9B34EFC1397E64BAEB05ACC265FF2378
__Gy = 0xADD6718B7C7C1961F0991B842443772152C9E0AD
__n = 0xE95E4A5F737059DC60DF5991D45029409E60FC09
__h = 1
# bpp160t1

__p = 0xC302F41D932A36CDA7A3463093D18DB78FCE476DE1A86297
__a = 0x6A91174076B1E0E19C39C031FE8685C1CAE040E5C69A28EF
__b = 0x469A28EF7C28CCA3DC721D044F4496BCCA7EF4146FBF25C9
__Gx = 0xC0A0647EAAB6A48753B033C56CB0F0900A2F5C4853375FD6
__Gy = 0x14B690866ABD5BB88B5F4828C1490002E6773FA2FA299B8F
__n = 0xC302F41D932A36CDA7A3462F9E9E916B5BE8F1029AC4ACC1
__h = 1
bpp192r1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__Z = 0x1B6F5CC8DB4DC7AF19458A9CB80DC2295E5EB9C3732104CB
__a = 0xC302F41D932A36CDA7A3463093D18DB78FCE476DE1A86294
__b = 0x13D56FFAEC78681E68F9DEB43B35BEC2FB68542E27897B79
__Gx = 0x3AE9E58C82F63C30282E1FE7BBF43FA72C446AF6F4618129
__Gy = 0x097E2C5667C2223A902AB5CA449D0084B7E5B3DE7CCC01C9
__n = 0xC302F41D932A36CDA7A3462F9E9E916B5BE8F1029AC4ACC1
__h = 1
# bpp192t1

__p = 0xD7C134AA264366862A18302575D1D787B09F075797DA89F57EC8C0FF
__a = 0x68A5E62CA9CE6C1C299803A6C1530B514E182AD8B0042A59CAD29F43
__b = 0x2580F63CCFE44138870713B1A92369E33E2135D266DBB372386C400B
__Gx = 0x0D9029AD2C7E5CF4340823B2A87DC68C9E4CE3174C1E6EFDEE12C07D
__Gy = 0x58AA56F772C0726F24C6B89E4ECDAC24354B9E99CAA3F6D3761402CD
__n = 0xD7C134AA264366862A18302575D0FB98D116BC4B6DDEBCA3A5A7939F
__h = 1
bpp224r1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)


__Z = 0x2DF271E14427A346910CF7A2E6CFA7B3F484E5C2CCE1C8B730E28B3F
__a = 0xD7C134AA264366862A18302575D1D787B09F075797DA89F57EC8C0FC
__b = 0x4B337D934104CD7BEF271BF60CED1ED20DA14C08B3BB64F18A60888D
__Gx = 0x6AB1E344CE25FF3896424E7FFE14762ECB49F8928AC0C76029B4D580
__Gy = 0x0374E9F5143E568CD23F3F4D7C0D4B1E41C8CC0D1C6ABD5F1A46DB4C
__n = 0xD7C134AA264366862A18302575D0FB98D116BC4B6DDEBCA3A5A7939F
__h = 1
# bpp224t1

__p = 0xA9FB57DBA1EEA9BC3E660A909D838D726E3BF623D52620282013481D1F6E5377
__a = 0x7D5A0975FC2C3057EEF67530417AFFE7FB8055C126DC5C6CE94A4B44F330B5D9
__b = 0x26DC5C6CE94A4B44F330B5D9BBD77CBF958416295CF7E1CE6BCCDC18FF8C07B6
__Gx = 0x8BD2AEB9CB7E57CB2C4B482FFC81B7AFB9DE27E1E3BD23C23A4453BD9ACE3262
__Gy = 0x547EF835C3DAC4FD97F8461A14611DC9C27745132DED8E545C1D54C72F046997
__n = 0xA9FB57DBA1EEA9BC3E660A909D838D718C397AA3B561A6F7901E0E82974856A7
__h = 1
bpp256r1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__Z = 0x3E2D4BD9597B58639AE7AA669CAB9837CF5CF20A2C852D10F655668DFC150EF0
__a = 0xA9FB57DBA1EEA9BC3E660A909D838D726E3BF623D52620282013481D1F6E5374
__b = 0x662C61C430D84EA4FE66A7733D0B76B7BF93EBC4AF2F49256AE58101FEE92B04
__Gx = 0xA3E8EB3CC1CFE7B7732213B23A656149AFA142C47AAFBC2B79A191562E1305F4
__Gy = 0x2D996C823439C56D7F7B22E14644417E69BCB6DE39D027001DABE8F35B25C9BE
__n = 0xA9FB57DBA1EEA9BC3E660A909D838D718C397AA3B561A6F7901E0E82974856A7
__h = 1
# bpp256t1

__p = 0xD35E472036BC4FB7E13C785ED201E065F98FCFA6F6F40DEF4F92B9EC7893EC28FCD412B1F1B32E27
__a = 0x3EE30B568FBAB0F883CCEBD46D3F3BB8A2A73513F5EB79DA66190EB085FFA9F492F375A97D860EB4
__b = 0x520883949DFDBC42D3AD198640688A6FE13F41349554B49ACC31DCCD884539816F5EB4AC8FB1F1A6
__Gx = 0x43BD7E9AFB53D8B85289BCC48EE5BFE6F20137D10A087EB6E7871E2A10A599C710AF8D0D39E20611
__Gy = 0x14FDD05545EC1CC8AB4093247F77275E0743FFED117182EAA9C77877AAAC6AC7D35245D1692E8EE1
__n = 0xD35E472036BC4FB7E13C785ED201E065F98FCFA5B68F12A32D482EC7EE8658E98691555B44C59311
__h = 1
bpp320r1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__Z = 0x15F75CAF668077F7E85B42EB01F0A81FF56ECD6191D55CB82B7D861458A18FEFC3E5AB7496F3C7B1
__a = 0xD35E472036BC4FB7E13C785ED201E065F98FCFA6F6F40DEF4F92B9EC7893EC28FCD412B1F1B32E24
__b = 0xA7F561E038EB1ED560B3D147DB782013064C19F27ED27C6780AAF77FB8A547CEB5B4FEF422340353
__Gx = 0x925BE9FB01AFC6FB4D3E7D4990010F813408AB106C4F09CB7EE07868CC136FFF3357F624A21BED52
__Gy = 0x63BA3A7A27483EBF6671DBEF7ABB30EBEE084E58A0B077AD42A5A0989D1EE71B1B9BC0455FB0D2C3
__n = 0xD35E472036BC4FB7E13C785ED201E065F98FCFA5B68F12A32D482EC7EE8658E98691555B44C59311
__h = 1
# bpp320t1

__p = 0x8CB91E82A3386D280F5D6F7E50E641DF152F7109ED5456B412B1DA197FB71123ACD3A729901D1A71874700133107EC53
__a = 0x7BC382C63D8C150C3C72080ACE05AFA0C2BEA28E4FB22787139165EFBA91F90F8AA5814A503AD4EB04A8C7DD22CE2826
__b = 0x04A8C7DD22CE28268B39B55416F0447C2FB77DE107DCD2A62E880EA53EEB62D57CB4390295DBC9943AB78696FA504C11
__Gx = 0x1D1C64F068CF45FFA2A63A81B7C13F6B8847A3E77EF14FE3DB7FCAFE0CBD10E8E826E03436D646AAEF87B2E247D4AF1E
__Gy = 0x8ABE1D7520F9C2A45CB1EB8E95CFD55262B70B29FEEC5864E19C054FF99129280E4646217791811142820341263C5315
__n = 0x8CB91E82A3386D280F5D6F7E50E641DF152F7109ED5456B31F166E6CAC0425A7CF3AB6AF6B7FC3103B883202E9046565
__h = 1
bpp384r1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__Z = 0x41DFE8DD399331F7166A66076734A89CD0D2BCDB7D068E44E1F378F41ECBAE97D2D63DBC87BCCDDCCC5DA39E8589291C
__a = 0x8CB91E82A3386D280F5D6F7E50E641DF152F7109ED5456B412B1DA197FB71123ACD3A729901D1A71874700133107EC50
__b = 0x7F519EADA7BDA81BD826DBA647910F8C4B9346ED8CCDC64E4B1ABD11756DCE1D2074AA263B88805CED70355A33B471EE
__Gx = 0x18DE98B02DB9A306F2AFCD7235F72A819B80AB12EBD653172476FECD462AABFFC4FF191B946A5F54D8D0AA2F418808CC
__Gy = 0x25AB056962D30651A114AFD2755AD336747F93475B7A1FCA3B88F2B6A208CCFE469408584DC2B2912675BF5B9E582928
__n = 0x8CB91E82A3386D280F5D6F7E50E641DF152F7109ED5456B31F166E6CAC0425A7CF3AB6AF6B7FC3103B883202E9046565
__h = 1
# bpp384t1

__p = 0xAADD9DB8DBE9C48B3FD4E6AE33C9FC07CB308DB3B3C9D20ED6639CCA703308717D4D9B009BC66842AECDA12AE6A380E62881FF2F2D82C68528AA6056583A48F3
__a = 0x7830A3318B603B89E2327145AC234CC594CBDD8D3DF91610A83441CAEA9863BC2DED5D5AA8253AA10A2EF1C98B9AC8B57F1117A72BF2C7B9E7C1AC4D77FC94CA
__b = 0x3DF91610A83441CAEA9863BC2DED5D5AA8253AA10A2EF1C98B9AC8B57F1117A72BF2C7B9E7C1AC4D77FC94CADC083E67984050B75EBAE5DD2809BD638016F723
__Gx = 0x81AEE4BDD82ED9645A21322E9C4C6A9385ED9F70B5D916C1B43B62EEF4D0098EFF3B1F78E2D0D48D50D1687B93B97D5F7C6D5047406A5E688B352209BCB9F822
__Gy = 0x7DDE385D566332ECC0EABFA9CF7822FDF209F70024A57B1AA000C55B881F8111B2DCDE494A5F485E5BCA4BD88A2763AED1CA2B2FA8F0540678CD1E0F3AD80892
__n = 0xAADD9DB8DBE9C48B3FD4E6AE33C9FC07CB308DB3B3C9D20ED6639CCA70330870553E5C414CA92619418661197FAC10471DB1D381085DDADDB58796829CA90069
__h = 1
bpp512r1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, True)

__Z = 0x12EE58E6764838B69782136F0F2D3BA06E27695716054092E60A80BEDB212B64E585D90BCE13761F85C3F1D2A64E3BE8FEA2220F01EBA5EEB0F35DBD29D922AB
__a = 0xAADD9DB8DBE9C48B3FD4E6AE33C9FC07CB308DB3B3C9D20ED6639CCA703308717D4D9B009BC66842AECDA12AE6A380E62881FF2F2D82C68528AA6056583A48F0
__b = 0x7CBBBCF9441CFAB76E1890E46884EAE321F70C0BCB4981527897504BEC3E36A62BCDFA2304976540F6450085F2DAE145C22553B465763689180EA2571867423E
__Gx = 0x640ECE5C12788717B9C1BA06CBC2A6FEBA85842458C56DDE9DB1758D39C0313D82BA51735CDB3EA499AA77A7D6943A64F7A3F25FE26F06B51BAA2696FA9035DA
__Gy = 0x5B534BD595F5AF0FA2C892376C84ACE1BB4E3019B71634C01131159CAE03CEE9D9932184BEEF216BD71DF2DADF86A627306ECFF96DBB8BACE198B61E00F8B332
__n = 0xAADD9DB8DBE9C48B3FD4E6AE33C9FC07CB308DB3B3C9D20ED6639CCA70330870553E5C414CA92619418661197FAC10471DB1D381085DDADDB58796829CA90069
__h = 1
# bpp512t1


# curve sets

SEC2V2_curves = [secp192k1, secp192r1,
                 secp224k1, secp224r1,
                 secp256k1, secp256r1,
                 secp384r1,
                 secp521r1]

SEC2V1_curves = [secp112r1, secp112r2,
                 secp128r1, secp128r2,
                 secp160k1, secp160r1, secp160r2] + SEC2V2_curves

NIST_curves = [nistp192, nistp224, nistp256, nistp384, nistp521]

BP_curves = [
    bpp160r1, bpp192r1, bpp224r1, bpp256r1,
    bpp320r1, bpp384r1, bpp512r1]
