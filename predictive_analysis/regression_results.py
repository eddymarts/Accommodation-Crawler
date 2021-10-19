import pandas as pd
import matplotlib.pyplot as plt

results = pd.read_csv("machine_learning/results.csv", index_col=0)

x = results["fitting_time"]
y = results["R_squared"]

# plt.ylabel("validation_r_squared")
# plt.xlabel("fit_time")
# plt.title("Fit Time vs Validation Score")

# plt.scatter(x, y, alpha=0.5)

# for i, model in enumerate(x.index):
#     plt.annotate(model, (x[i], y[i]))
# plt.show()

# plt.ylabel("validation_r_squared")
# plt.xlabel("fit_time")
plt.title("R squared per model")
plt.bar(y.index, y)
plt.show()