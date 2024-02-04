import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript import extract_transcript

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
print("this is api key",os.getenv("GOOGLE_API_KEY"))
def fetch_transcript(video_id):
    conn = sqlite3.connect('youtube_transcripts.db')
    c = conn.cursor()
    c.execute("SELECT transcript FROM transcripts WHERE video_id = ?", (video_id,))
    transcript_text = c.fetchone()[0]
    conn.close()
    return transcript_text


def generate_notes(transcript_text, subject):


    if subject == "Mathematics":
        prompt = """
            Title: Detailed Mathematics Notes from YouTube Video Transcript

            As a mathematics expert, your task is to provide detailed notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate comprehensive notes covering the key mathematical concepts discussed in the video.

            Your notes should:

            - Outline mathematical concepts, formulas, and problem-solving techniques covered in the video.
            - Provide step-by-step explanations for solving mathematical problems discussed.
            - Clarify any theoretical foundations or mathematical principles underlying the discussed topics.
            - Include relevant examples or practice problems to reinforce understanding.

            Please provide the YouTube video transcript, and I'll generate the detailed mathematics notes accordingly.
        """
    elif subject == "Data Science and Statistics":
        prompt = """
            Title: Comprehensive Notes on Data Science and Statistics from YouTube Video Transcript

            Subject: Here you should give the topic of the video

            Prompt:

            As an expert in Data Science and Statistics, your task is to provide comprehensive notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate detailed notes covering the key concepts discussed in the video.

            Your notes should:

            - Outline the fundamental concepts discussed in the video
            - Provide step-by-step explanations for the topics discussed in the video
            - Clarify any theoretical foundations or statistical principles underlying the discussed topics.
            - Include relevant examples or practice problems to reinforce understanding.

        """

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt + transcript_text)
    return response.text

def main():
    st.title("Generate notes from YouTube")
    

    subject = st.selectbox("Select Subject:", ["Mathematics", "Data Science and Statistics"])


    youtube_link = st.text_input("Enter YouTube Video Link:")


    if youtube_link:
        video_id = youtube_link.split("=")[-1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    if st.button("Get Detailed Notes"):
        # Call function to extract transcript
        transcript_text = extract_transcript(youtube_link)
        
        if transcript_text:
            st.success("Transcript extracted successfully!")
            # Generate detailed notes
            detailed_notes = generate_notes(transcript_text, subject)
            st.markdown("## Detailed Notes:")
            st.write(detailed_notes)
        else:
            st.error("Failed to extract transcript.")

if __name__ == "__main__":
    main()
