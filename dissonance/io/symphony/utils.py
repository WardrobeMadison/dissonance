import logging

import numpy as np


logger = logging.getLogger(__name__)


S1 = np.dtype("|S1")


def convert_if_bytes(attr):
    if isinstance(attr, np.bytes_):
        return attr.decode()
    else:
        return attr
