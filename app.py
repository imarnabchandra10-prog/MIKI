import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Create 20 Sample Employee Records

np.random.seed(42)

data = {
    "Employee_ID": range(1, 21),
    "Name": [f"Employee_{i}" for i in range(1, 21)],
    "Department": np.random.choice(["HR", "Finance", "Sales", "IT", "Marketing"], 20),
    "Experience_Years": np.random.randint(1, 15, 20),
    "Monthly_Salary": np.random.randint(30000, 100000, 20),
    "Performance_Score": np.random.randint(1, 10, 20),
    "Leaves_Taken": np.random.randint(0, 12, 20)
}

df = pd.DataFrame(data)


# Export to CSV

df.to_csv("employee_data.csv", index=False)
print("✅ Sample data exported to employee_data.csv")


# Data Cleaning + Transformation


# Load again (simulate real-world workflow)
df = pd.read_csv("employee_data.csv")

# Check for missing values
print("\nMissing Values:\n", df.isnull().sum())

# Clean: Add column for Annual Salary
df["Annual_Salary"] = df["Monthly_Salary"] * 12

# Transformation: Create performance category
df["Performance_Level"] = pd.cut(df["Performance_Score"],
                                 bins=[0, 3, 6, 10],
                                 labels=["Low", "Medium", "High"])

# Clean: Remove any duplicate rows
df.drop_duplicates(inplace=True)

print("\nCleaned & Transformed Data:\n", df.head())

# Analysis & Visualization

# 1. Average salary by department
dept_salary = df.groupby("Department")["Monthly_Salary"].mean()
print("\nAverage Salary by Department:\n", dept_salary)

# 2. Experience vs Performance scatter plot
plt.figure()
plt.scatter(df["Experience_Years"], df["Performance_Score"], s=100, alpha=0.7)
plt.title("Experience vs Performance Score")
plt.xlabel("Experience (Years)")
plt.ylabel("Performance Score")
plt.grid(True)
plt.show()

# 3. Bar chart of average salary by department
dept_salary.plot(kind="bar", figsize=(8, 5))
plt.title("Average Salary by Department")
plt.xlabel("Department")
plt.ylabel("Average Monthly Salary")
plt.show()

# 4. Pie chart for Performance Level Distribution
performance_counts = df["Performance_Level"].value_counts()
plt.figure(figsize=(5, 5))
plt.pie(performance_counts, labels=performance_counts.index, autopct="%1.1f%%", startangle=90)
plt.title("Performance Level Distribution")
plt.show()