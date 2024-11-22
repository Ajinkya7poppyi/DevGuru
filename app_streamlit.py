# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.cortex import Complete

# Set the page configuration to wide
st.set_page_config(layout="wide")

# Add a trendy title to the Streamlit page
st.title("🔥 Dev Guru: Optimize Your Code! 🔥")

# List of programming languages and their standards, optimization guidelines, and naming conventions
languages = {
    "Python": {
        "standards": [
            "PEP8",
            "Google Python Style Guide",
            "Black Code Style",
            "PyLint",
            "Flake8",
        ],
        "optimization": [
            "Python Performance Tips",
            "NumPy Best Practices",
            "Memory Management in Python",
        ],
        "naming": ["PEP8 Naming Conventions", "Google Python Naming Guide"],
    },
    "C++": {
        "standards": [
            "C++ Core Guidelines",
            "Google C++ Style Guide",
            "LLVM Coding Standards",
            "MISRA C++",
            "JSF C++ Coding Standards",
        ],
        "optimization": [
            "C++ Performance Tips",
            "Effective C++",
            "High Performance C++",
        ],
        "naming": ["C++ Naming Conventions", "Google C++ Naming Guide"],
    },
    "Java": {
        "standards": [
            "Google Java Style Guide",
            "Oracle Java Code Conventions",
            "Spring Framework Code Style",
            "Android Code Style",
            "Checkstyle",
        ],
        "optimization": [
            "Java Performance Tips",
            "Effective Java",
            "Java Memory Management",
        ],
        "naming": ["Java Naming Conventions", "Google Java Naming Guide"],
    },
    "JavaScript": {
        "standards": [
            "Airbnb JavaScript Style Guide",
            "Google JavaScript Style Guide",
            "StandardJS",
            "Idiomatic.js",
            "JavaScript Standard Style",
        ],
        "optimization": [
            "JavaScript Performance Tips",
            "JavaScript Optimization Techniques",
            "Memory Management in JavaScript",
        ],
        "naming": ["JavaScript Naming Conventions", "Google JavaScript Naming Guide"],
    },
    "Ruby": {
        "standards": [
            "Ruby Style Guide",
            "Shopify Ruby Style Guide",
            "BBatsov Ruby Style Guide",
            "GitHub Ruby Style Guide",
            "Airbnb Ruby Style Guide",
        ],
        "optimization": [
            "Ruby Performance Tips",
            "Ruby Optimization Techniques",
            "Memory Management in Ruby",
        ],
        "naming": ["Ruby Naming Conventions", "Shopify Ruby Naming Guide"],
    },
    "Go": {
        "standards": [
            "Effective Go",
            "Uber Go Style Guide",
            "Go Code Review Comments",
            "GoLint",
            "Go Style Guide",
        ],
        "optimization": [
            "Go Performance Tips",
            "Go Optimization Techniques",
            "Memory Management in Go",
        ],
        "naming": ["Go Naming Conventions", "Uber Go Naming Guide"],
    },
    "Swift": {
        "standards": [
            "Swift API Design Guidelines",
            "Ray Wenderlich Swift Style Guide",
            "LinkedIn Swift Style Guide",
            "Google Swift Style Guide",
            "SwiftLint",
        ],
        "optimization": [
            "Swift Performance Tips",
            "Swift Optimization Techniques",
            "Memory Management in Swift",
        ],
        "naming": ["Swift Naming Conventions", "Ray Wenderlich Swift Naming Guide"],
    },
    "SQL": {
        "standards": [
            "SQL Style Guide",
            "SQL Server Coding Standards",
            "Oracle SQL Guidelines",
        ],
        "optimization": [
            "SQL Performance Tips",
            "Query Optimization Techniques",
            "Indexing Best Practices",
        ],
        "naming": ["SQL Naming Conventions", "Database Naming Standards"],
    },
}


# Sidebar for model selection
with st.sidebar:
    st.sidebar.title("Dev Guru Settings")
    selected_language = st.selectbox(
        "Select Programming Language", list(languages.keys()), key="language"
    )
    selected_standard = st.selectbox(
        "Select Coding Standard",
        languages[selected_language]["standards"],
        key="standard",
    )
    selected_optimization = st.selectbox(
        "Select Optimization Guideline",
        languages[selected_language]["optimization"],
        key="optimization",
    )
    selected_naming = st.selectbox(
        "Select Naming Convention", languages[selected_language]["naming"], key="naming"
    )


# Get the current credentials
session = get_active_session()

# Display the selected options as chips
st.markdown(
    f"""
    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
        <div style="background-color: #e0e0e0; padding: 5px 10px; border-radius: 15px;">{selected_language}</div>
        <div style="background-color: #e0e0e0; padding: 5px 10px; border-radius: 15px;">{selected_standard}</div>
        <div style="background-color: #e0e0e0; padding: 5px 10px; border-radius: 15px;">{selected_optimization}</div>
        <div style="background-color: #e0e0e0; padding: 5px 10px; border-radius: 15px;">{selected_naming}</div>
    </div>
""",
    unsafe_allow_html=True,
)

st.write("")


def extract_code_block(text):
    import re

    pattern = rf"```{selected_language.lower()}(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


# Create two columns for code editors
col1, col2 = st.columns(2)
with col1:
    st.write(f"Input {selected_language} Code")
    code1 = st.text_area(
        label="", height=400, key="code1", label_visibility="collapsed"
    )
    # Format button
    if st.button("Format Code"):
        prompt = f"""
        Act as a proficient programmer and optimize the following code according to the specified parameters:
        
        Language: {selected_language}
        Standards: {selected_standard}
        Optimization Guidelines: {selected_optimization}
        Naming Conventions: {selected_naming}
        
        Input Code:
        
        {code1}
        
        Enhanced Code:
        # Please provide the optimized and enhanced version of the code following the specified standards, optimization guidelines, and naming conventions.
        
        Explanation of Changes:
        # Please provide a detailed explanation of the changes made to the code.
        """

        # Call the LLM model to get the enhanced code and explanation of changes
        response = Complete("mistral-large2", prompt)

        # Split the response into enhanced code and explanation
        enhanced_code, explanation = response.split("Explanation of Changes:")
        _, enhanced_code = enhanced_code.split("Enhanced Code:")
        with col2:
            st.write(f"Enhanced {selected_language} Code")
            # Display the enhanced code in a code block
            st.code(
                extract_code_block(enhanced_code.strip()),
                language=selected_language.lower(),
                line_numbers=True,
            )

        # Display the explanation of changes
        st.write("Explanation of Changes:")
        st.write(explanation.strip())
    else:
        with col2:
            st.write(f"Enhanced {selected_language} Code")
            st.code(body=code1, language=selected_language.lower(), line_numbers=True)
