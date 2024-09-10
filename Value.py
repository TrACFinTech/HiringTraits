import pandas as pd
import matplotlib.pyplot as plt

# Load your data into a DataFrame
data = {
    'File': ['p10.vtt', 'p11.vtt', 'p12.vtt', 'p13.vtt', 'p14.vtt', 'p15.vtt', 'p16.vtt', 'p17.vtt', 'p20.vtt', 'p21.vtt', 'p22.vtt', 'p24.vtt', 'p25.vtt', 'p27.vtt', 'p29.vtt', 'p3.vtt', 'p30.vtt', 'p31.vtt', 'p4.vtt', 'p5.vtt', 'p6.vtt', 'p7.vtt', 'p8.vtt'],
    'Openness_Expert': [3, 4, 5, 5, 4, 2, 4, 3, 4, 5, 5, 5, 3, 2, 3, 5, 3, 3, 4, 4, 5, 5, 4],
    'Conscientiousness_Expert': [3, 4, 3, 4, 4, 5, 3, 4, 4, 4, 4, 4, 4, 5, 4, 4, 5, 4, 4, 3, 5, 4, 3],
    'Extraversion_Expert': [3, 5, 3, 4, 5, 4, 3, 2, 2, 5, 4, 5, 3, 4, 4, 4, 1, 5, 2, 3, 3, 4, 5],
    'Agreeableness_Expert': [2, 4, 2, 3, 4, 4, 2, 3, 5, 4, 4, 4, 3, 2, 5, 3, 4, 3, 2, 4, 3, 4, 4],
    'Neuroticism_Expert': [4, 1, 1, 1, 2, 3, 3, 4, 2, 3, 1, 1, 1, 3, 1, 1, 1, 3, 3, 2, 1, 3, 2],
    'Openness_LLM': [3, 3, 5, 4, 4, 4, 5, 4, 3, 3, 4, 5, 5, 4, 3, 5, 3, 4, 3, 5, 4, 4, 5],
    'Conscientiousness_LLM': [5, 5, 4, 5, 5, 5, 4, 5, 5, 5, 5, 4, 3, 5, 5, 4, 4, 5, 5, 4, 5, 5, 4],
    'Extraversion_LLM': [2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 3, 1, 2, 2, 3, 1, 2, 2, 2, 3, 3, 3],
    'Agreeableness_LLM': [4, 4, 3, 3, 2, 2, 2, 3, 4, 4, 2, 2, 4, 3, 4, 2, 5, 3, 4, 3, 2, 2, 2],
    'Neuroticism_LLM': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1]
}
df = pd.DataFrame(data)

# Print columns to verify their names
print("Columns in DataFrame:")
print(df.columns)

# Define a list of colors
colors = ['lightblue', 'lightgreen', 'gold', 'lightpink', 'Wheat']

# Plot LLM Scores and Expert Scores
plt.figure(figsize=(15, 6), facecolor='white')

# Create subplots for each trait
traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']

for i, trait in enumerate(traits):
    print(f"Processing trait: {trait}")
    plt.subplot(1, 5, i + 1)
    data_to_plot = pd.DataFrame({
        'LLM': df[f'{trait}_LLM'],
        'Expert': df[f'{trait}_Expert']
    })

    # Select color for current trait
    color = colors[i % len(colors)]  # Cycle through colors if more traits than colors

    # Plot boxplot with different colors for each trait
    data_to_plot.boxplot(
        boxprops=dict(facecolor=color, color='black', linewidth=1.5), 
        medianprops=dict(color='brown', linewidth=3),  # Bright orange and thicker line
        whiskerprops=dict(color='black', linewidth=1.5),
        capprops=dict(color='black', linewidth=2),
        patch_artist=True,  # Allows box filling
        showfliers=False,
        positions=[1, 2]  # Ensure each boxplot is placed correctly
    )

    # Set the Y-axis limits to be consistent across all subplots
    plt.ylim(0.9, 5.1)

    plt.title(f'{trait}')
    
    plt.ylabel('Scores between 1 and 5')

plt.tight_layout()
plt.show()
