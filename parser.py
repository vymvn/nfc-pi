import codecs
import copy
import sys
from collections import defaultdict
import re

from bitstring import BitArray

uid = ""
strings = ""


def find_strings(data):
    data_string = data.decode('ascii', errors='ignore')  # Ignore non-ASCII characters

    ascii_strings = "\n\t".join( re.findall(r'[ -~]{4,}', data_string) )  # Match sequences of printable ASCII characters of length 4 or more

    return ascii_strings

def parse(data):
    blocksmatrix = []
    blockrights = {}
    block_number = 0
    card_type = "Mifare classic"

    strings = find_strings(data) 

    data_size = len(data)

    if data_size not in {4096, 1024, 320}:
        return "unsupported card"

    if data_size == 1024:
        card_type += " 1k"
    elif data_size == 4096:
        card_type += " 4k"


    # read all sectors
    sector_number = 0
    start = 0
    end = 64
    while True:
        sector = data[start:end]
        sector = codecs.encode(sector, 'hex')
        if not isinstance(sector, str):
            sector = str(sector, 'ascii')
        sectors = [sector[x:x + 32] for x in range(0, len(sector), 32)]

        blocksmatrix.append(sectors)

        # after 32 sectors each sector has 16 blocks instead of 4
        sector_number += 1
        if sector_number < 32:
            start += 64
            end += 64
        elif sector_number == 32:
            start += 64
            end += 256
        else:
            start += 256
            end += 256

        if start == data_size:
            break

    # blocksmatrix_clear = copy.deepcopy(blocksmatrix)

    uid = blocksmatrix[0][0][0:8]


    return uid, card_type, strings



if __name__ == "__main__":
    with open("./cards/blue", "rb") as f:
        data = f.read()
        print(parse(data))