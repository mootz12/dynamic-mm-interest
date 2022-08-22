import matplotlib.pyplot as plt

TARGET = 0.75
RATE_MOD = 1
util_rates = range(0, 100)
interest_rates = []

for u_percentage in util_rates:
    base_ir = 0.0
    u_rate = float(u_percentage) / 100.0
    if u_rate <= TARGET:
        base_ir = u_rate / TARGET * 0.04  # 4% IR at util
    else:
        # util is greater than target
        base_ir = 0.04 + (((u_rate - TARGET) / (1 - TARGET)) ** 3)
    interest_rates.append(base_ir * RATE_MOD * 100)

fig, axs = plt.subplots(1, 1)

# IR graphs
axs.plot(util_rates, interest_rates)
axs.set_xlabel("Utilization rate (%)")
axs.set_ylabel("Interest rate (%)")
axs.set_title("Interest Rate")
fig.tight_layout()
fig.set_tight_layout(True)
plt.show()
