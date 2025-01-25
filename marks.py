import streamlit as st
import pandas as pd

# Function to calculate grade point based on total marks
def calculate_grade_point(marks):
    if marks >= 90:
        return 10
    elif marks >= 80:
        return 9
    elif marks >= 70:
        return 8
    elif marks >= 60:
        return 7
    elif marks >= 50:
        return 6
    elif marks >= 40:
        return 5
    else:
        return 0

# Function to calculate CGPA
def calculate_cgpa(data):
    # Calculate Total Marks
    data['Total Marks'] = data['CIA'] + data['SEM']

    # Calculate Grade Points
    data['Grade Point'] = data['Total Marks'].apply(calculate_grade_point)

    # Filter passed subjects and exclude subjects with zero credits
    passed_data = data[(data['Result'] == 'P') & (data['Credits'] > 0)]

    # Calculate Weighted Grade Points
    passed_data['Weighted GP'] = passed_data['Credits'] * passed_data['Grade Point']

    # Calculate CGPA
    total_weighted_gp = passed_data['Weighted GP'].sum()
    total_credits = passed_data['Credits'].sum()

    cgpa = total_weighted_gp / total_credits if total_credits > 0 else 0
    return round(cgpa, 2), passed_data

# Streamlit App
def main():
    st.title("CGPA Calculator")

    st.write("Enter your subject details below:")

    # Input number of subjects
    num_subjects = st.number_input("Number of Subjects", min_value=1, step=1, value=5)

    # Initialize lists for input fields
    subjects = []
    cias = []
    sems = []
    results = []
    credits = []

    # Create input fields for each subject
    for i in range(num_subjects):
        st.subheader(f"Subject {i+1}")
        subjects.append(st.text_input(f"Subject Name {i+1}", key=f"subject_{i}"))
        cia = st.number_input(f"CIA Marks (out of 100) for Subject {i+1}", min_value=0, max_value=100, key=f"cia_{i}")
        cias.append(cia)

        if cia < 40:
            st.warning(f"CIA Marks for Subject {i+1} are below 40. Marking as Fail.")
            sems.append(0)  # Disable SEM field by setting it to 0
            results.append("F")  # Automatically mark as Fail
        else:
            sem = st.number_input(f"Semester Marks (out of 100) for Subject {i+1}", min_value=0, max_value=100, key=f"sem_{i}")
            sems.append(sem)
            results.append(st.selectbox(f"Result for Subject {i+1}", ["P", "F"], index=0 if cia >= 40 else 1, key=f"result_{i}"))

        credits.append(st.number_input(f"Credits for Subject {i+1}", min_value=0, step=1, key=f"credit_{i}"))

    # Submit button
    if st.button("Calculate CGPA"):
        # Create a DataFrame from inputs
        data = pd.DataFrame({
            'Paper Name': subjects,
            'CIA': cias,
            'SEM': sems,
            'Result': results,
            'Credits': credits
        })

        # Calculate CGPA
        cgpa, detailed_data = calculate_cgpa(data)

        # Display CGPA
        st.success(f"Your CGPA is: {cgpa}")

        # Display detailed table
        st.write("Detailed Breakdown:")
        st.dataframe(detailed_data)

if __name__ == "__main__":
    main()
