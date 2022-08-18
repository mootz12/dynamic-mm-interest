import csv
import jsons
import random
import matplotlib.pyplot as plt

from dynamic_mm_interest.chain import Chain

from dynamic_mm_interest.pool_token import PoolToken
from dynamic_mm_interest.market import Market

TARGET_IR: float = 0.07
TARGET_UTIL: float = 0.75
REACTIVITY_CONST: float = 0.0001
MARKET_CHANCE: float = 0.05

print("Starting sim")

chain: Chain = Chain()
pool_token: PoolToken = PoolToken(chain, TARGET_UTIL, REACTIVITY_CONST, TARGET_UTIL, TARGET_IR, TARGET_IR)
market: Market = Market(pool_token)

print("Objects built...")

# 2m period
for i in range(0, 1_051_200):
    market.sim_block(MARKET_CHANCE, TARGET_IR)

for i in range(0, 1_051_200):
    market.sim_block(MARKET_CHANCE, 0.03)

for i in range(0, 1_051_200):
    market.sim_block(MARKET_CHANCE, 0.25)

for i in range(0, 1_051_200):
    market.sim_block(MARKET_CHANCE, 0.10)

for i in range(0, 1_051_200):
    market.sim_block(MARKET_CHANCE, 0.07)

for i in range(0, 1_051_200):
    market.sim_block(MARKET_CHANCE, 0.1)

print("The market acting ", len(pool_token.updates), " times")

# ## write results to a csv
# with open("sim_result.csv", "w", newline="") as csvfile:
#     spamwriter = csv.writer(csvfile)
#     for update in pool_token.updates:
#         spamwriter.writerow([jsons.dumps(update)])

market.graph_results()
