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


# Interest calculators to test


def calc_exp_interest(util: float, rate_modifier: float) -> float:
    return rate_modifier * ((util) ** 2)


def calc_piecewise_exp_interest(target: float, util: float, rate_modifier: float) -> float:
    r_0 = 0.01
    r_1 = 0.05
    r_2 = 0.5
    r_3 = 1.5
    ir = 0.0
    if util <= target:
        ir = rate_modifier * (r_0 + (util / target) * r_1)
    elif util <= 0.95:
        ir = rate_modifier * (r_0 + r_1 + ((util - target) / (0.95 - target)) * r_2)
    else:
        ir = rate_modifier * (r_0 + r_1 + r_2) + ((util - 0.95) / (0.05)) * r_3
    return ir


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
        self.last_rate_modifier: float = initial_rate / calc_piecewise_exp_interest(target_util, initial_util, 1)
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
        next_rate_modifier = max(util_rate_error * self.reactivity + self.last_rate_modifier, 0)
        # TODO: Add bounds to next rate modifier
        next_ir = calc_piecewise_exp_interest(self.target_util, next_util, next_rate_modifier)

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
