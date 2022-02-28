
_block_offset = 0xA0


def query_chr(zone_1, zone_2):
    """
    按照 GB2312 区域规则查询字符串
    """
    return bytes([zone_1 + _block_offset, zone_2 + _block_offset]).decode("gb2312")
