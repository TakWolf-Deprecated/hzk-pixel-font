
_block_offset = 0xA0

alphabet_other_count = 682
alphabet_level_1_count = 3755
alphabet_level_2_count = 3008


def query_chr(zone_1, zone_2):
    """
    按照 GB2312 分区规则查询字符串
    """
    return bytes([zone_1 + _block_offset, zone_2 + _block_offset]).decode('gb2312')
