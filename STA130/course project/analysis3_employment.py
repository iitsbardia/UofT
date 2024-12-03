import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f_oneway

# Sample Data
data = {
    'Employment_Status': ['Employed', 'Unemployed', 'Retired'] * 100,
    'Age_Group': np.random.choice(['18-24', '25-44', '45-64', '65+'], 300),
    'Mental_Wellbeing_Score': (
        [np.random.normal(8.2, 1, 100)] +  # Employed
        [np.random.normal(5.6, 1.5, 100)] +  # Unemployed
        [np.random.normal(7.1, 1.2, 100)]  # Retired
    )
}
df = pd.DataFrame(data)

# Preprocessing
df['Mental_Wellbeing_Score'] = np.clip(df['Mental_Wellbeing_Score'], 1, 10)  # Winsorizing

# ANOVA Test for Statistical Significance
groups = [df[df['Employment_Status'] == status]['Mental_Wellbeing_Score'] for status in df['Employment_Status'].unique()]
anova_result = f_oneway(*groups)

print("ANOVA Results:")
print(f"F-statistic: {anova_result.statistic:.2f}")
print(f"P-value: {anova_result.pvalue:.4f}")

# Visualization
avg_scores = df.groupby('Employment_Status')['Mental_Wellbeing_Score'].mean()

plt.bar(avg_scores.index, avg_scores, color=['skyblue', 'salmon', 'lightgreen'])
plt.title("Mental Well-being by Employment Status")
plt.ylabel("Average Well-being Score (1-10)")
plt.xlabel("Employment Status")
plt.ylim(0, 10)
plt.savefig("employment_vs_mental_wellbeing.png")
plt.show()
