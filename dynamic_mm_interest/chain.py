from time import time


class Chain:
    """
    Chain state for a simulation to share
    """

    def __init__(self) -> None:
        self.block_num: int = 0
        self.timestamp: int = int(0)
        self.default_sec_per_block: int = 5

    def mine(self):
        """
        Mine a block
        """
        self.block_num += 1
        self.timestamp += self.default_sec_per_block
