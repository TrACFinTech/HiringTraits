import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Define the data
features = ['Agreeableness', 'Extraversion', 'Conscientiousness', 'Openness to Experience', 'Neuroticism']
importance = [0.34, 0.27, 0.18, 0.13, 0.07]

# Number of features
num_features = len(features)

# Compute angle for each feature
angles = np.linspace(0, 2 * np.pi, num_features, endpoint=False).tolist()

# The plot is circular, so we need to "complete the loop" and append the start value to the end.
importance += importance[:1]
angles += angles[:1]

# Create the plot
fig, ax = plt.subplots(figsize=(4, 8), subplot_kw=dict(polar=True))

# Set the range of the radar chart
ax.set_ylim(0, 0.4)  # Adjust the maximum value based on the data

# Draw one axe per feature and add labels only for the features
ax.set_xticks(angles[:-1])
ax.set_xticklabels(features, fontsize=12)

# Remove radial gridlines and ticks
ax.yaxis.grid(False)
ax.xaxis.grid(True)

# Draw the radar chart
ax.plot(angles, importance, color='blue', linewidth=2, linestyle='solid', label='Importance')
ax.fill(angles, importance, color='blue', alpha=0.25)

# Add a legend
plt.legend(loc='best')

# Show the plot
plt.title('Feature Importances Radar Chart', size=15, color='black', y=1.1)  # Adjust title position and size

# Display the plot
plt.show()
