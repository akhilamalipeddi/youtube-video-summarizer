import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai

# 1. Page Setup
st.title("YouTube Video Summarizer")
st.write("Paste a YouTube link below to get instant bullet-point notes.")

# 2. User Inputs
api_key = st.text_input("Enter your Gemini API Key:", type="password")
video_url = st.text_input("Enter YouTube Video URL:")

def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

# 3. Summarize Button
if st.button("Summarize Video"):
    if not api_key or not video_url:
        st.warning("Please enter both your API key and a YouTube URL.")
    else:
        video_id = extract_video_id(video_url)
        if not video_id:
            st.error("Invalid YouTube URL. Please check the link and try again.")
        else:
            try:
                with st.spinner("Fetching transcript and generating summary..."):
                    # Fetch transcript
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                    full_text = " ".join([item["text"] for item in transcript_list])

                    # Initialize Gemini and summarize
                    client = genai.Client(api_key=api_key)
                    prompt = (
                        "Summarize the following YouTube video transcript into "
                        "clear, concise key takeaways using bullet points:\n\n"
                        f"{full_text}"
                    )
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    # Display output
                    st.subheader("Video Summary")
                    st.markdown(response.text)

            except Exception as e:
                st.error(f"Could not summarize video. Error: {e}")
