import streamlit as st

def qa_functionality(input_values):
    st.header("Ask a Question")
    question = st.text_input("Type your question here:")
    
    if st.button("Get Answer"):
        # Combine the question with the input values
        combined_text = f"Question: {question}\n"
        combined_text += "Input Values:\n"
        for key, value in input_values.items():
            combined_text += f"{key}: {value}\n"
        
        # Display the combined text
        st.write(combined_text) 