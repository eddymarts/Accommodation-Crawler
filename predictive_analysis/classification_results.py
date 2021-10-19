import pandas as pd
import matplotlib.pyplot as plt

nn_results = pd.read_csv("predictive_analysis/models/rent/classifiers/neural/SGDNetworkClassifier_params.csv", index_col=0)
dt_results = pd.read_csv("predictive_analysis/models/rent/classifiers/simple/DTClassifier_params.csv", index_col=0)
knn_results = pd.read_csv("predictive_analysis/models/rent/classifiers/simple/KNNClassifier_params.csv", index_col=0)
lr_results = pd.read_csv("predictive_analysis/models/rent/classifiers/simple/LRClassifier_params.csv", index_col=0)
rf_results = pd.read_csv("predictive_analysis/models/rent/classifiers/simple/RFClassifier_params.csv", index_col=0)

results_list = [knn_results, dt_results, rf_results, nn_results]
results = lr_results[["score", "fit_time", "tune_time"]]

for df in results_list:
    results = pd.concat([results, df[["score", "fit_time", "tune_time"]]], axis=0)

print(results)

x = results["tune_time"]
y = results["score"]

# plt.ylabel("validation F1 score")
# plt.xlabel("tune_time")
# plt.title("Tune Time vs Validation Score")

# plt.scatter(x, y, alpha=0.5)

# for i, model in enumerate(x.index):
#     plt.annotate(model, (x[i], y[i]))
# plt.show()

plt.ylabel("validation F1 score")
plt.title("F1 score per model")
plt.bar(y.index, y)
plt.show()