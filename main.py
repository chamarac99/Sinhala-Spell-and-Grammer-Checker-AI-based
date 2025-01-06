import streamlit as st
import openai
import os

from dotenv import load_dotenv

load_dotenv()

openai.api_base = "https://models.inference.ai.azure.com"
openai.api_key = os.getenv("GITHUB_TOKEN")


def check_grammar(user_input):
    try:
        # Call the Azure OpenAI API to correct grammar and spelling
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Verify the model name with your Azure deployment
            messages=[
                {"role": "system",
                 "content": "Correct the grammar and spelling of Sinhala sentences. Ensure the ending matches the subject appropriately."},
                {"role": "user",
                 "content": f"""
                 Correct the following sentence s an example, if the subject is 'මම', the ending mustuse 'මි'.Also if there is a spelling mistakes corrcect that also": {user_input}\n\n
                 
                 """}
            ],
            temperature=1,
            max_tokens=4096,
            top_p=1
        )

        # Return the corrected sentence
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"The program encountered an error: {str(e)}"


def main():
    st.title("Sinhala Grammar Checker")

    # Input text area
    user_input = st.text_area("Enter a sentence in Sinhala for grammar and spelling correction:")

    # Check grammar button
    if st.button("Check Grammar"):
        if user_input:
            with st.spinner("Checking grammar..."):
                result = check_grammar(user_input)

                # Display results
                st.subheader("Results:")
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Original Text:**")
                    st.text(user_input)

                with col2:
                    st.markdown("**Corrected Text:**")
                    st.text(result)
        else:
            st.warning("Please enter some text to check.")


if __name__ == "__main__":
    main()
