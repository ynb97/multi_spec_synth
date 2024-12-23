import streamlit as st
from utils import google_translate, generate_audio, play_audio, save_file, local_tts, create_graph, options, translate_text


# Streamlit app layout
st.title("Multilingual Speech Synthesizer with Voice Cloning")

main_container = st.container()

with main_container:

    top = st.container()
    middle = st.container()
    bottom = st.container()

    with top:
        st.header("Text Translation Unit")

        left_col, mid_left, mid_col, mid_right, right_col = st.columns([5,2,3,2,5])

        with left_col:
            st.subheader("Enter your text:")
            # Text input with clear label
            user_input = st.text_area('a', label_visibility="hidden", key="user_input")
        
        # Display arrows using Markdown for better visual consistency
        with mid_left:
            arrow_1 = st.markdown("<div style='text-align: center;align-items: center; height: 80px;display: grid'>➡️</div>", unsafe_allow_html=True)
        with mid_col:
            st.subheader("Select a language")
            # Dropdown selector with informative label
            selected_option = st.selectbox("a", label_visibility="hidden", options=options, key="selected_option")
        with mid_right:
            arrow_2 = st.markdown("<div style='text-align: center;align-items: center; height: 80px;display: grid'>➡️</div>", unsafe_allow_html=True)
        with right_col:
            st.subheader("Translated text")
            # Text display box with potential formatting options
            # text_display = st.markdown("Translated Text: ")  # Placeholder for text display
            
            # Update text display based on user input and selection (replace with your logic)
            if user_input and selected_option:
                translated_text = translate_text(user_input, target_language=selected_option)
                # translated_text = google_translate(user_input, language=selected_option)
                if translated_text:
                    processed_text = f"({selected_option}) {translated_text}"
                    st.markdown(processed_text)
                    st.success("Text translated successfully!")
            # else:
            #     st.markdown("Translated Text: ")

    with middle:
        st.header("Voice Generation Unit")
        # Audio player button with clear label and disabled state handling
        # generate_button = st.button("Generate Audio", key="generate_button")
        if st.button("Generate Audio", key="generate_button"):
            print("Generating audio.......")
            generate_audio(translated_text, selected_option)
            play_audio()
        else:
            generated_audio = None
        # if generated_audio:
    
    with bottom:
        st.header("Voice Cloning Unit")
        uploaded_file = st.file_uploader("Choose a file to upload:", type=["mp3", "wav"])
        if uploaded_file is not None:
            filename = "uploaded_voice_sample.mp3"
            save_file(uploaded_file, filename)
            local_tts(translated_text, language=selected_option)
    
    with st.container():


        # Define model names and performance metrics (replace with placeholder data)
        model_names = ["Model1", "Model2", "Model3", "Model4"]
        mos_scores = [4.02, 3.86, 3.61, 3.11]
        gpe_values = [0.025, 0.038, 0.032, 0.041]
        
        # Streamlit app
        st.title("Model Performance Evaluation")
        st.set_option('deprecation.showPyplotGlobalUse', False)

        # Display graphs for each metric
        st.subheader("Mean Opinion Score (MOS)")
        create_graph(model_names, "MOS Score", mos_scores)

        st.subheader("Gross Pitch Error (GPE)")
        create_graph(model_names, "GPE (unit)", gpe_values)  # Adjust unit label as needed


        # Hide matplotlib warnings from Streamlit output
        # st.beta_set_page_config(page_title="Model Performance Comparison", layout="wide")

