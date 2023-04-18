import matplotlib.pyplot as plt

TARGET = 0.8
GOAL_IR = 0.05
RATE_MOD = 1
util_rates = [x / 10.0 for x in range(0, 1000, 1)]
low_vol_interest_rates = []
stable_interest_rates = []
vol_interest_rates = []

# # exponential rates
# for u_percentage in util_rates:
#     base_ir = 0.0
#     u_rate = float(u_percentage) / 1000.0
#     if u_rate <= TARGET:
#         base_ir = u_rate / TARGET * 0.04  # 4% IR at util
#     else:
#         # util is greater than target
#         base_ir = 0.04 + (((u_rate - TARGET) / (1 - TARGET)) ** 3)
#     interest_rates.append(base_ir * RATE_MOD * 100)

# 3 step rates
for u_percentage in util_rates:
    u_t = 0.75
    r_0 = 0.01
    r_1 = 0.05
    r_2 = 0.5
    r_3 = 1.5
    ir = 0.0
    u_rate = float(u_percentage) / 100.0
    if u_rate <= u_t:
        ir = RATE_MOD * (r_0 + (u_rate / u_t) * r_1)
    elif u_rate <= 0.95:
        ir = RATE_MOD * (r_0 + r_1 + ((u_rate - u_t) / (0.95 - u_t)) * r_2)
    else:
        ir = RATE_MOD * (r_0 + r_1 + r_2) + ((u_rate - 0.95) / (0.05)) * r_3
    low_vol_interest_rates.append(ir * 100)

# 3 step rates
for u_percentage in util_rates:
    u_t = 0.9
    r_0 = 0.01
    r_1 = 0.03
    r_2 = 0.2
    r_3 = 1
    ir = 0.0
    u_rate = float(u_percentage) / 100.0
    if u_rate <= u_t:
        ir = RATE_MOD * (r_0 + (u_rate / u_t) * r_1)
    elif u_rate <= 0.95:
        ir = RATE_MOD * (r_0 + r_1 + ((u_rate - u_t) / (0.95 - u_t)) * r_2)
    else:
        ir = RATE_MOD * (r_0 + r_1 + r_2) + ((u_rate - 0.95) / (0.05)) * r_3
    stable_interest_rates.append(ir * 100)

# 3 step rates
for u_percentage in util_rates:
    u_t = 0.6
    r_0 = 0.01
    r_1 = 0.07
    r_2 = 1
    r_3 = 2
    ir = 0.0
    u_rate = float(u_percentage) / 100.0
    if u_rate <= u_t:
        ir = RATE_MOD * (r_0 + (u_rate / u_t) * r_1)
    elif u_rate <= 0.95:
        ir = RATE_MOD * (r_0 + r_1 + ((u_rate - u_t) / (0.95 - u_t)) * r_2)
    else:
        ir = RATE_MOD * (r_0 + r_1 + r_2) + ((u_rate - 0.95) / (0.05)) * r_3
    vol_interest_rates.append(ir * 100)

fig, axs = plt.subplots(1, 1)

# IR graphs
axs.plot(util_rates, stable_interest_rates, label="low IR curve")
axs.plot(util_rates, low_vol_interest_rates, label="medium IR curve")
axs.plot(util_rates, vol_interest_rates, label="high IR curve")
axs.set_xlabel("Utilization rate (%)")
axs.set_ylabel("Interest rate (%)")
axs.set_title("Interest Rate Model")
axs.legend()
fig.tight_layout()
fig.set_tight_layout(True)
plt.show()
