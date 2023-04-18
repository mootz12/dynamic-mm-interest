import csv
import jsons
import random
import matplotlib.pyplot as plt

from dynamic_mm_interest.chain import Chain

from dynamic_mm_interest.pool_token import PoolToken
from dynamic_mm_interest.market import Market

TARGET_IR: float = 0.05
TARGET_UTIL: float = 0.75
REACTIVITY_CONST: float = 0.00002
MARKET_CHANCE: float = 0.00002

print("Starting sim")

chain: Chain = Chain()
pool_token: PoolToken = PoolToken(chain, TARGET_UTIL, REACTIVITY_CONST, TARGET_UTIL, TARGET_IR, TARGET_IR)
market: Market = Market(pool_token)

print("Objects built...")

### quick spike test

# # ~ 7 days
# for i in range(0, 120960):
#     market.sim_block(MARKET_CHANCE, 0.1)

# # 21 days
# for i in range(0, 120960 * 3):
#     market.sim_block(MARKET_CHANCE, 2)

### stale rate drop test

# 2m period each, 1yr total
for i in range(0, 1_051_200):
    market.sim_block(MARKET_CHANCE, TARGET_IR)

for i in range(0, 1_051_200):
    market.sim_block(MARKET_CHANCE, 0.02)

for i in range(0, 1_051_200):
    market.sim_block(MARKET_CHANCE, 0.08)

for i in range(0, 1_051_200):
    market.sim_block(MARKET_CHANCE, 0.15)

for i in range(0, 1_051_200):
    market.sim_block(MARKET_CHANCE, 0.15)

# check reaction here
for i in range(0, 1_051_200):
    market.sim_block(MARKET_CHANCE, 0.05)


print("The market acting ", len(pool_token.updates), " times")
last_update = pool_token.updates[len(pool_token.updates) - 1]

# Log final loan amounts
print("Real Loan-------: ", last_update.example_loan_val)
print("Cont Real Loan--: ", last_update.cont_ex_loan_val)
print("Market Loan-----: ", last_update.market_loan_val)
print("Cont Market Loan: ", last_update.cont_market_loan_val)

# ## write results to a csv
# with open("sim_result.csv", "w", newline="") as csvfile:
#     spamwriter = csv.writer(csvfile)
#     for update in pool_token.updates:
#         spamwriter.writerow([jsons.dumps(update)])

market.graph_results()
