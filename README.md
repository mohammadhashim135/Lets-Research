# **Let's Research** 🔍  
**An AI-powered Research Assistant using Streamlit & Cohere API**

---

## **Overview**  
**Let's Research** is an intelligent web application built with **Streamlit**, designed to help users perform efficient online research. By leveraging Google Custom Search and AI-powered summarization via the **Cohere API**, this app searches, scrapes, and summarizes web content to deliver concise insights on any research topic.

---

## **Features** 🚀  
✅ **Smart Web Search** – Uses Google Custom Search API to find relevant sources.  
✅ **Automated Content Scraping** – Extracts and cleans text from multiple web pages.  
✅ **AI-Powered Summarization** – Summarizes lengthy articles using Cohere's advanced language models.  
✅ **Synthesized Reports** – Combines multiple summaries into a coherent overview.  
✅ **User-Friendly Interface** – Simple Streamlit UI to input topics and view results.  
✅ **Progress Tracking** – Visual progress bar showing search and summarization status.  

---

## 📸 Screenshot


![Image](/assets/1.png)
![Image](/assets/2.png)


## **Tech Stack** 🛠  
- **Frontend & Deployment:** Streamlit  
- **Backend & Scraping:** Python, Requests, BeautifulSoup  
- **AI & NLP:** Cohere API for summarization  
- **Libraries:** Requests, BeautifulSoup, Streamlit, dotenv  
- **Environment:** `.env` for storing API keys securely  

---

## **Installation & Setup** 🏗  

### 1. Clone the repository:

```bash
git clone https://github.com/mohammadhashim135/Lets-Research.git
cd Lets-Research
```
### **2. Create a Virtual Environment**
```bash
python -m venv .venv

# Activate it:

# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```


### **4. Start the Application**
```bash
streamlit run app.py
```
---

## **Usage Guide** 📝

🔹 **Enter your research topic in the input box.**  
🔹 **Select the number of search results to process.**  
🔹 **Click the "Start Research" button to begin the search, scrape, and summarization.**  
🔹 **View individual summaries for each source and the final synthesized report.**  
🔹 **Repeat with new topics as needed.**

---

## **Project Structure** 📂
```bash
Lets-Research/
│
├── app.py                    # Main Streamlit app file
├── synthesizer.py            # Module for summarization and synthesis functions
├── requirements.txt          # Python package dependencies
├── .env                      # Environment variables for API keys
├── README.md                 # Project documentation
└── .gitignore                # Git ignore file
```

---

---
## **Contributing** 🤝
Contributions are welcome! If you’d like to improve Let's Research, feel free to fork the repo and submit a pull request.

### **Steps to Contribute:**

### **1. Fork the repository**

### **2. Create a new branch:**

```bash
git checkout -b feature-branch
```

### **3. Make your changes and commit:**

```bash
git commit -m "Added new feature"
```
### **4. Push to the branch:**

```bash
git push origin feature-branch
```
### **5. Open a Pull Request**
---
## **License** 📜
This project is licensed under the MIT License.

💡 Developed with ❤️ by [Mohammad Hashim](https://github.com/mohammadhashim135/Lets-Research.git)

