import math
import random
from .pool_token import PoolToken
import matplotlib.pyplot as plt


class Market:
    def __init__(self, pool_token: PoolToken) -> None:
        self.pool_token: PoolToken = pool_token

    def sim_block(self, market_action_chance: float, market_rate: float) -> None:
        self.pool_token.chain.mine()
        # Exit the block early if the block will not be acted on by the market
        if not random.random() < market_action_chance:
            return

        # Market is acting - pick a reasonable action on a
        # gaussian function to add some randomness
        rate_dif = market_rate - self.pool_token.ir
        # rate_dif is negative if the rate is too high
        # which will mean util_effect is likely negative (withdraw) and vice versa
        util_effect = random.gauss(rate_dif / 10, 0.005)
        self.pool_token.update(max(min(self.pool_token.util_rate + util_effect, 0.99), 0.01), market_rate)

    def graph_results(self) -> None:
        # build arrays from Update object
        time_series = []
        block_series = []
        # IR series
        ir_series = []
        market_rate = []
        # Loans
        loan_series = []
        cont_loan_series = []
        market_loan_series = []
        cont_market_loan_series = []
        # Util
        util_series = []
        # extra
        rate_mod_series = []

        for update in self.pool_token.updates:
            time_series.append(update.timestamp)
            block_series.append(update.block)
            # IR series
            ir_series.append(update.ir)
            market_rate.append(update.market_rate)
            # Loans
            loan_series.append(update.example_loan_val)
            cont_loan_series.append(update.cont_ex_loan_val)
            market_loan_series.append(update.market_loan_val)
            cont_market_loan_series.append(update.cont_market_loan_val)
            # Util
            util_series.append(update.util_rate)
            # extra
            rate_mod_series.append(update.rate_modifier)

        # Log final loan amounts
        print("Real Loan-------: ", loan_series[len(loan_series) - 1])
        print("Cont Real Loan--: ", cont_loan_series[len(cont_loan_series) - 1])
        print("Market Loan-----: ", market_loan_series[len(market_loan_series) - 1])
        print("Cont Market Loan: ", cont_market_loan_series[len(cont_market_loan_series) - 1])

        # Graphs interest rates, loan values, and utilization rates
        fig, axs = plt.subplots(3, 1)

        # IR graphs
        axs[0].plot(time_series, ir_series, label="Interest Rate")
        axs[0].plot(time_series, market_rate, label="Market Rate")
        axs[0].set_xlabel("time")
        axs[0].set_ylabel("rate")
        axs[0].set_title("Interest")
        axs[0].legend()

        # loan graphs
        # axs[1].plot(time_series, loan_series, label="Loan")
        # axs[1].plot(time_series, cont_loan_series, label="Cont Loan")
        # axs[1].plot(time_series, loan_series, label="Market Loan")
        # axs[1].plot(time_series, cont_loan_series, label="Cont Market Loan")
        # axs[1].set_xlabel("time")
        # axs[1].set_ylabel("Value ($)")
        # axs[1].set_title("Loan Accrual")
        # axs[1].legend()
        axs[1].plot(time_series, rate_mod_series, label="Rate Modifier")
        axs[1].set_xlabel("time")
        axs[1].set_ylabel("Value")
        axs[1].set_title("Rate Modifier")
        axs[1].legend()

        # util graphs
        axs[2].plot(time_series, util_series, label="Util Rate")
        axs[2].plot(time_series, [self.pool_token.target_util for i in range(len(time_series))], label="Target Rate")
        axs[2].set_xlabel("time")
        axs[2].set_ylabel("rate")
        axs[2].set_title("Utilization Rate")
        axs[2].legend()

        fig.tight_layout()
        fig.set_tight_layout(True)
        plt.show()
