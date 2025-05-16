import os
import time
import requests
import string

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

def chunk_text(text, max_length=3500):
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_length
        if end < len(text):
            newline_pos = text.rfind('\n', start, end)
            space_pos = text.rfind(' ', start, end)
            boundary = max(newline_pos, space_pos)
            if boundary > start:
                end = boundary
        chunks.append(text[start:end].strip())
        start = end
    return chunks

def summarize_with_cohere(text, retries=3, timeout=30, depth=0, max_depth=2):
    if not COHERE_API_KEY:
        return "[Error: Missing COHERE_API_KEY]"

    url = "https://api.cohere.ai/v1/summarize"
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }

    chunks = chunk_text(text, max_length=3500)
    chunk_summaries = []

    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        for attempt in range(retries):
            try:
                response = requests.post(url, json={
                    "text": chunk,
                    "length": "medium",
                    "format": "paragraph",
                    "model": "summarize-xlarge",
                    "extractiveness": "auto",
                    "temperature": 0.3
                }, headers=headers, timeout=timeout)

                if response.status_code == 429:
                    wait_time = 2 ** attempt
                    print(f"Rate limited by API. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                result = response.json()
                summary = result.get("summary")
                if summary:
                    chunk_summaries.append(summary)
                else:
                    chunk_summaries.append("[Error: No summary returned]")
                break

            except requests.exceptions.Timeout:
                if attempt < retries - 1:
                    print("Request timed out. Retrying...")
                    time.sleep(3)
                    continue
                else:
                    return "[Summarization error]: Request timed out."
            except Exception as e:
                return f"[Summarization error]: {e}"

        else:
            return "[Summarization error]: Exceeded retries due to rate limiting."

    if len(chunk_summaries) > 1 and depth < max_depth:
        print(f"Summarizing combined chunk summaries (recursion depth {depth+1})...")
        combined_summary = summarize_with_cohere("\n".join(chunk_summaries), depth=depth+1)
        return combined_summary
    elif len(chunk_summaries) > 1 and depth >= max_depth:
        return "\n".join(chunk_summaries)
    elif chunk_summaries:
        return chunk_summaries[0]
    else:
        return "[No text to summarize]"

def synthesize_information(summaries):
    combined_text = "\n".join(summaries)
    summary = summarize_with_cohere(combined_text)

    pros = []
    cons = []
    contradictions = []

    def clean_text(t):
        # Lowercase and remove punctuation safely
        return t.lower().translate(str.maketrans('', '', string.punctuation))

    # Broader keyword lists for pros/cons detection
    pros_keywords = ["connect", "benefit", "positive", "advantage", "strength", "improve", "help"]
    cons_keywords = ["misinformation", "negative", "harm", "risk", "problem", "weakness", "issue"]

    for s in summaries:
        text = clean_text(s)
        if any(word in text for word in pros_keywords):
            pros.append(s)
        if any(word in text for word in cons_keywords):
            cons.append(s)

    if pros and cons:
        contradictions.append("Some sources highlight benefits, while others warn of dangers.")

    final_report = (
        f"**Synthesized Summary:**\n{summary}\n\n"
        f"**Pros Identified:**\n" + ("\n".join(f"- {p}" for p in pros[:3]) if pros else "None") + "\n\n"
        f"**Cons Identified:**\n" + ("\n".join(f"- {c}" for c in cons[:3]) if cons else "None") + "\n\n"
        f"**Contradictions:**\n" + ("\n".join(f"- {c}" for c in contradictions) if contradictions else "None") + "\n\n"
        f"**Conclusion:**\nBalanced research with multiple perspectives helps make informed decisions."
    )
    return final_report

