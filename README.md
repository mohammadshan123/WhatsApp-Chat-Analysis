# 📊 WhatsApp Chat Analyzer

Analyze your WhatsApp chats using insightful statistics and visualizations. This project supports both a **web interface (Flask)** and a **Streamlit dashboard** to explore user behavior, message activity, emoji usage, and more.

---

## 🚀 Features

- 📈 **Message Statistics**: Total messages, words, media, and links.
- 📅 **Monthly & Daily Activity**: Visualize chat frequency over time.
- 📊 **Busy Days & Months**: Identify the most active times.
- 🗺️ **Weekly Heatmap**: Understand daily chat patterns.
- ☁️ **Word Cloud**: Most frequently used words (after removing Hinglish stopwords).
- 📝 **Top Words**: Bar graph of common words.
- 😂 **Emoji Usage**: See your most-used emojis and their count.
- 👥 **Most Active Users**: In group chats, view who chats the most.
- 🖥️ **Dual Interface**: Web version with Flask + GUI version with Streamlit.

---

## 🧰 Tech Stack

- **Frontend**: HTML (Flask `index.html`), Streamlit UI
- **Backend**: Python, Flask, Streamlit
- **Data Analysis & Visualization**: Pandas, Matplotlib, Seaborn, WordCloud, Emoji, URLExtract

---

## 📂 Project Structure


---

## 📥 How to Use

### 1. Export WhatsApp Chat

- Go to any chat in WhatsApp
- Tap **More > Export Chat > Without Media**
- Save the `.txt` file to your PC

### 2. Setup


git clone [https://github.com/your-repo/whatsapp-analyzer](https://github.com/mohammadshan123/WhatsApp-Chat-Analysis)
cd whatsapp-analyzer
pip install -r requirements.txt


### 3. Run the App

streamlit run app1.py

### Flask Web App

python "app (4).py"

