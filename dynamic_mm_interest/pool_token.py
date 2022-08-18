from dataclasses import dataclass
from math import e
from typing import List
from dynamic_mm_interest.chain import Chain

BLOCKS_PER_YEAR: float = 6307200.0


@dataclass
class Update:
    timestamp: int
    block: int
    util_rate: float
    ir: float
    market_rate: float
    rate_modifier: float
    delta_util_rate: float
    delta_ir: float
    example_loan_val: float
    cont_ex_loan_val: float
    market_loan_val: float
    cont_market_loan_val: float


class PoolToken:
    """
    Simplified pool token that calculates a dynamic interest rate
    """

    def __init__(
        self,
        chain: Chain,
        target_util: float,
        reactivity: float,
        initial_util: float,
        initial_rate: float,
        market_rate: float,
    ) -> None:
        self.chain: Chain = chain
        self.target_util: float = target_util
        self.reactivity: float = reactivity
        self.util_rate: float = initial_util
        self.ir: float = initial_rate
        self.last_rate_modifier: float = initial_rate / (initial_util**2)
        self.last_update_block: int = chain.block_num
        self.last_update_timestamp: int = chain.timestamp
        self.market_rate: float = market_rate
        self.example_loan: float = 1.0
        self.cont_example_loan: float = 1.0
        self.market_loan: float = 1.0
        self.cont_market_loan: float = 1.0
        self.updates: List[Update] = []

    def update(self, next_util: float, next_market_rate: float) -> None:
        # calculate the rate modifier
        block_dif = self.chain.block_num - self.last_update_block
        util_rate_error = block_dif * (next_util - self.target_util)
        next_rate_modifier = util_rate_error * self.reactivity + self.last_rate_modifier
        # TODO: Add bounds to next rate modifier
        next_ir = next_rate_modifier * (next_util**2)

        # accrue interest to examples
        next_example_loan = self.example_loan * (1 + self.ir * (block_dif / BLOCKS_PER_YEAR))
        next_cont_example_loan = self.cont_example_loan * pow(e, self.ir * (block_dif / BLOCKS_PER_YEAR))
        next_market_loan = self.market_loan * (1 + self.market_rate * (block_dif / BLOCKS_PER_YEAR))
        next_cont_market_loan = self.cont_market_loan * pow(e, self.market_rate * (block_dif / BLOCKS_PER_YEAR))

        # build update for graphing purposes
        next_update = Update(
            self.chain.timestamp,
            self.chain.block_num,
            next_util,
            next_ir,
            next_market_rate,
            next_rate_modifier,
            next_util - self.util_rate,
            next_ir - self.ir,
            next_example_loan,
            next_cont_example_loan,
            next_market_loan,
            next_cont_market_loan,
        )

        # store relevant info
        self.util_rate = next_util
        self.ir = next_ir
        self.market_rate = next_market_rate
        self.last_rate_modifier = next_rate_modifier
        self.last_update_block = self.chain.block_num
        self.last_update_timestamp = self.chain.timestamp
        self.example_loan = next_example_loan
        self.cont_example_loan = next_cont_example_loan
        self.market_loan = next_market_loan
        self.cont_market_loan = next_cont_market_loan
        self.updates.append(next_update)
