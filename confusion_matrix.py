import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Define fake data
true_classes = ["person", "car", "car", "dog", "bicycle", "person", "car", "person", "dog", "car", "person", "person", "boat", "boat", "boat", "truck", "truck","person", "car", "car", "dog", "person"]
predicted_classes = ["person", "car", "car","dog", "bicycle", "person", "truck", "person", "dog", "bicycle", "car", "person", "boat", "boat", "boat", "boat", "truck", "person", "car", "car","dog", "person"]

# Generate the confusion matrix
labels = sorted(set(true_classes + predicted_classes))  # Unique class labels
cm = confusion_matrix(true_classes, predicted_classes, labels=labels)

# Display the confusion matrix
df_cm = pd.DataFrame(cm, index=labels, columns=labels)

plt.figure(figsize=(8, 6))
sns.heatmap(df_cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
plt.xlabel("Predicted Classes")
plt.ylabel("True Classes")
plt.title("Confusion Matrix")
plt.show()
