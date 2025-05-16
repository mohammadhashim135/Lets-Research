import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import time
from dotenv import load_dotenv
from synthesizer import synthesize_information, summarize_with_cohere

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

def google_search(query, num_results=5):
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        st.error("Google API Key or Search Engine ID missing.")
        return []

    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
        "num": num_results
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        results = [item.get("link") for item in data.get("items", []) if item.get("link")]
        return results
    except Exception as e:
        st.error(f"[Search Error]: {e}")
        return []

def scrape_content(url, retries=3, delay=2):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    for attempt in range(retries):
        try:
            page = requests.get(url, headers=headers, timeout=10)
            page.raise_for_status()
            soup = BeautifulSoup(page.content, "html.parser")
            texts = soup.stripped_strings
            clean_text = " ".join(texts)
            return clean_text[:4000]
        except requests.exceptions.HTTPError as http_err:
            if page.status_code == 403:
                st.warning(f"Access forbidden (403) for {url}. Site may block scraping.")
                return ""
            else:
                st.error(f"HTTP error for {url}: {http_err}")
                return ""
        except requests.exceptions.Timeout:
            st.warning(f"Timeout while scraping {url}. Retrying...")
            time.sleep(delay)
        except Exception as e:
            st.error(f"[Scraping error at {url}]: {e}")
            return ""
    st.error(f"Failed to scrape {url} after {retries} retries.")
    return ""

def main():
    st.set_page_config(page_title="Let's Research", layout="wide")
    st.title("Let's do some research!")
    st.markdown("This app uses AI to search, scrape, and summarize web content.")

    query = st.text_input("Enter your research topic:")
    num_results = st.slider("Number of search results to process:", 1, 10, 5)

    st.markdown("### Instructions:")
    st.markdown("1. Enter a topic above.")
    st.markdown("2. Select how many results to summarize.")
    st.markdown("3. Click 'Start Research' to begin.")

    if st.button("Start Research"):
        if not query:
            st.warning("Please enter a topic.")
            return
        if not COHERE_API_KEY:
            st.error("COHERE_API_KEY not found in environment variables.")
            return

        with st.spinner("Searching and analyzing..."):
            urls = google_search(query, num_results)
            if not urls:
                st.error("No URLs found.")
                return

            summaries = []
            progress_bar = st.progress(0)
            total = len(urls)

            for i, url in enumerate(urls):
                st.markdown(f"### [{i+1}] Scraping: {url}")
                content = scrape_content(url)
                if not content:
                    st.info(f"Skipping URL {i+1} due to no content.")
                    progress_bar.progress((i+1)/total)
                    continue

                st.markdown(f"Summarizing content from source {i+1}...")
                summary = summarize_with_cohere(content)
                summaries.append((url, summary))
                time.sleep(2)  
                progress_bar.progress((i+1)/total)

        if summaries:
            st.success("Research Completed!")

            st.subheader("Individual Source Summaries:")
            for i, (url, summary) in enumerate(summaries, 1):
                st.markdown(f"### Source {i}: [{url}]({url})")
                with st.expander("View Summary"):
                    st.write(summary)

            st.subheader("Synthesized Report:")
            final_report = synthesize_information([s for _, s in summaries])
            st.markdown(final_report)
        else:
            st.error("No relevant summaries found.")

if __name__ == "__main__":
    main()