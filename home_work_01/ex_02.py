def int32_to_ip(int32: int) -> str:
    return ".".join([str(int32 >> 24 & 255),
                     str(int32 >> 16 & 255),
                     str(int32 >> 8 & 255),
                     str(int32 & 255)])
