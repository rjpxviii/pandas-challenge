# Import necessary libraries
import pandas as pd

# Load the CSV files using absolute paths
students_file_path = '/Users/ryanpope/pandas-challenge/PyCitySchools/Resources/students_complete.csv'
schools_file_path = '/Users/ryanpope/pandas-challenge/PyCitySchools/Resources/schools_complete.csv'

# Read the CSV data into DataFrames
students_df = pd.read_csv(students_file_path)
schools_df = pd.read_csv(schools_file_path)

# Merge the students and schools dataframes on 'school_name'
merged_df = pd.merge(students_df, schools_df, on="school_name")

# ---- District Summary ----

# Total number of unique schools (provided code - starter code)
total_schools = schools_df['school_name'].nunique()

# Total number of students (provided code - starter code)
total_students = students_df['Student ID'].count()

# Total budget (sum of school budgets) (provided code - starter code)
total_budget = schools_df['budget'].sum()

# Average math score (provided code - starter code)
avg_math_score = students_df['math_score'].mean()

# Average reading score (provided code - starter code)
avg_reading_score = students_df['reading_score'].mean()

# Percentage of students passing math (score >= 70) (provided code - starter code)
passing_math = (students_df[students_df['math_score'] >= 70]['Student ID'].count() / total_students) * 100

# Percentage of students passing reading (score >= 70) (provided code - starter code)
passing_reading = (students_df[students_df['reading_score'] >= 70]['Student ID'].count() / total_students) * 100

# Percentage of students passing both math and reading (provided code - starter code)
overall_passing = (students_df[(students_df['math_score'] >= 70) & (students_df['reading_score'] >= 70)]['Student ID'].count() / total_students) * 100

# Create a DataFrame to summarize district performance
district_summary = pd.DataFrame({
    "Total Schools": [total_schools],
    "Total Students": [total_students],
    "Total Budget": [total_budget],
    "Average Math Score": [avg_math_score],
    "Average Reading Score": [avg_reading_score],
    "% Passing Math": [passing_math],
    "% Passing Reading": [passing_reading],
    "% Overall Passing": [overall_passing]
})

# ---- School Summary ----

# Group by school and calculate metrics for each school (provided code - starter code)
school_summary = merged_df.groupby('school_name').agg({
    'Student ID': 'count',
    'budget': 'mean',
    'math_score': 'mean',
    'reading_score': 'mean',
    'type': 'first'
}).rename(columns={
    'Student ID': 'Total Students',
    'budget': 'Total School Budget',
    'math_score': 'Average Math Score',
    'reading_score': 'Average Reading Score',
    'type': 'School Type'
})

# Calculate per student budget (provided code - starter code)
school_summary['Per Student Budget'] = school_summary['Total School Budget'] / school_summary['Total Students']

# Calculate passing percentages for math, reading, and overall for each school
school_summary['% Passing Math'] = merged_df[merged_df['math_score'] >= 70].groupby('school_name')['Student ID'].count() / school_summary['Total Students'] * 100
school_summary['% Passing Reading'] = merged_df[merged_df['reading_score'] >= 70].groupby('school_name')['Student ID'].count() / school_summary['Total Students'] * 100
school_summary['% Overall Passing'] = merged_df[(merged_df['math_score'] >= 70) & (merged_df['reading_score'] >= 70)].groupby('school_name')['Student ID'].count() / school_summary['Total Students'] * 100

# ---- Highest and Lowest Performing Schools ----

# Sort schools by overall passing percentage (provided code - starter code)
top_schools = school_summary.sort_values('% Overall Passing', ascending=False).head(5)
bottom_schools = school_summary.sort_values('% Overall Passing', ascending=True).head(5)

# ---- Math and Reading Scores by Grade ----

# Group by school and grade to calculate average math and reading scores for each grade level (provided code - starter code)
math_scores_by_grade = merged_df.groupby(['school_name', 'grade'])['math_score'].mean().unstack()
reading_scores_by_grade = merged_df.groupby(['school_name', 'grade'])['reading_score'].mean().unstack()

# ---- Scores by School Spending ----

# Categorize schools into spending ranges (provided code - starter code)
spending_bins = [0, 585, 630, 645, 680]
spending_labels = ["<$585", "$585-630", "$630-645", "$645-680"]
school_summary['Spending Ranges (Per Student)'] = pd.cut(school_summary['Per Student Budget'], bins=spending_bins, labels=spending_labels)

# Group by spending ranges and calculate average scores and passing percentages (provided code - starter code)
spending_summary = school_summary.groupby('Spending Ranges (Per Student)').agg({
    'Average Math Score': 'mean',
    'Average Reading Score': 'mean',
    '% Passing Math': 'mean',
    '% Passing Reading': 'mean',
    '% Overall Passing': 'mean'
})

# ---- Scores by School Size ----

# Categorize schools by size (provided code - starter code)
size_bins = [0, 1000, 2000, 5000]
size_labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
school_summary['School Size'] = pd.cut(school_summary['Total Students'], bins=size_bins, labels=size_labels)

# Group by school size and calculate averages (provided code - starter code)
size_summary = school_summary.groupby('School Size').agg({
    'Average Math Score': 'mean',
    'Average Reading Score': 'mean',
    '% Passing Math': 'mean',
    '% Passing Reading': 'mean',
    '% Overall Passing': 'mean'
})

# ---- Scores by School Type ----

# Group by school type and calculate averages (provided code - starter code)
type_summary = school_summary.groupby('School Type').agg({
    'Average Math Score': 'mean',
    'Average Reading Score': 'mean',
    '% Passing Math': 'mean',
    '% Passing Reading': 'mean',
    '% Overall Passing': 'mean'
})

# Writing output to a Python file
output_path = '/Users/ryanpope/pandas-challenge/PyCitySchools/PyCitySchools Analysis.py'

with open(output_path, 'w') as f:
    f.write('# District Summary\n')
    f.write(district_summary.to_string())
    f.write('\n\n# School Summary\n')
    f.write(school_summary.to_string())
    f.write('\n\n# Top Performing Schools\n')
    f.write(top_schools.to_string())
    f.write('\n\n# Lowest Performing Schools\n')
    f.write(bottom_schools.to_string())
    f.write('\n\n# Math Scores by Grade\n')
    f.write(math_scores_by_grade.to_string())
    f.write('\n\n# Reading Scores by Grade\n')
    f.write(reading_scores_by_grade.to_string())
    f.write('\n\n# Scores by School Spending\n')
    f.write(spending_summary.to_string())
    f.write('\n\n# Scores by School Size\n')
    f.write(size_summary.to_string())
    f.write('\n\n# Scores by School Type\n')
    f.write(type_summary.to_string())
