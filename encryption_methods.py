import base64
import codecs

# ══════════════════════════════════════════════════════════════════════
#  BASE ENCODINGS
# ══════════════════════════════════════════════════════════════════════

# ── Base16 (Hexadecimal) ──────────────────────────────────────────────
def base16_encode(text):
    return base64.b16encode(text.encode()).decode()

def base16_decode(text):
    return base64.b16decode(text.upper().encode()).decode()


# ── Base32 ────────────────────────────────────────────────────────────
def base32_encode(text):
    return base64.b32encode(text.encode()).decode()

def base32_decode(text):
    return base64.b32decode(text.upper().encode()).decode()


# ── Base64 ────────────────────────────────────────────────────────────
def base64_encode(text):
    return base64.b64encode(text.encode()).decode()

def base64_decode(text):
    return base64.b64decode(text.encode()).decode()


# ── Base62 ────────────────────────────────────────────────────────────
_B62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62_encode(text):
    data = text.encode("utf-8")
    num = int.from_bytes(data, "big")
    if num == 0:
        return _B62[0]
    result = []
    while num:
        result.append(_B62[num % 62])
        num //= 62
    return "".join(reversed(result))

def base62_decode(text):
    num = 0
    for ch in text:
        num = num * 62 + _B62.index(ch)
    length = (num.bit_length() + 7) // 8
    return num.to_bytes(length, "big").decode("utf-8")



# ── Base58 (Bitcoin alphabet) ─────────────────────────────────────────
_B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def base58_encode(text):
    data = text.encode("utf-8")
    num = int.from_bytes(data, "big")
    result = []
    while num:
        result.append(_B58[num % 58])
        num //= 58
    return "".join(reversed(result)) or _B58[0]

def base58_decode(text):
    num = 0
    for ch in text:
        num = num * 58 + _B58.index(ch)
    length = (num.bit_length() + 7) // 8
    return num.to_bytes(length, "big").decode("utf-8")



# ── Base85 (RFC 1924) ─────────────────────────────────────────────────
def base85_encode(text):
    return base64.b85encode(text.encode()).decode()

def base85_decode(text):
    return base64.b85decode(text.encode()).decode()


# ── Base91 ────────────────────────────────────────────────────────────
_B91 = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    "0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~\""
)
_B91_DEC = {c: i for i, c in enumerate(_B91)}

def base91_encode(text):
    data = text.encode("utf-8")
    b = n = 0
    out = []
    for byte in data:
        b |= byte << n
        n += 8
        if n > 13:
            v = b & 8191
            if v > 88:
                b >>= 13
                n -= 13
            else:
                v = b & 16383
                b >>= 14
                n -= 14
            out.append(_B91[v % 91])
            out.append(_B91[v // 91])
    if n:
        out.append(_B91[b % 91])
        if n > 7 or b > 90:
            out.append(_B91[b // 91])
    return "".join(out)

def base91_decode(text):
    v = -1
    b = n = 0
    out = bytearray()
    for ch in text:
        p = _B91_DEC.get(ch, -1)
        if p == -1:
            continue
        if v < 0:
            v = p
        else:
            v += p * 91
            b |= v << n
            n += 13 if (v & 8191) > 88 else 14
            v = -1
            while n > 7:
                out.append(b & 255)
                b >>= 8
                n -= 8
    if v > -1:
        out.append((b | v << n) & 255)
    return out.decode("utf-8")


# ══════════════════════════════════════════════════════════════════════
#  ROT ENCODINGS
# ══════════════════════════════════════════════════════════════════════

# ── ROT-N  (letters only, N = 1..25) ─────────────────────────────────
def rot_n_encode(text, n):
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + n) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)

def rot_n_decode(text, n):
    return rot_n_encode(text, -n)   # reverse the shift


# ── ROT13  (letters, shift 13 — own inverse) ──────────────────────────
def rot13_encode(text):
    return rot_n_encode(text, 13)

def rot13_decode(text):
    return rot13_encode(text)       # ROT13 is its own inverse


# ── ROT5   (digits only, shift 5 — own inverse) ───────────────────────
def rot5_encode(text):
    return "".join(str((int(c) + 5) % 10) if c.isdigit() else c for c in text)

def rot5_decode(text):
    return rot5_encode(text)        # 5 + 5 = 10 → own inverse


# ── ROT18  (ROT13 for letters + ROT5 for digits — own inverse) ────────
def rot18_encode(text):
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + 13) % 26 + base))
        elif ch.isdigit():
            result.append(str((int(ch) + 5) % 10))
        else:
            result.append(ch)
    return "".join(result)

def rot18_decode(text):
    return rot18_encode(text)       # own inverse


# ── ROT47  (94 printable ASCII chars, shift 47 — own inverse) ─────────
def rot47_encode(text):
    return "".join(
        chr(33 + (ord(c) - 33 + 47) % 94) if 33 <= ord(c) <= 126 else c
        for c in text
    )

def rot47_decode(text):
    return rot47_encode(text)       # 47 + 47 = 94 → own inverse