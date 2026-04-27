import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import random
from io import BytesIO

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Sentiment Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# BLACK THEME CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.main {
    background-color: #0e1117;
}
div[data-testid="metric-container"] {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #333;
}
h1, h2, h3 {
    color: #00ffd5;
}
.stTextArea textarea {
    background-color: #1c1f26;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("🚀 Social Media Sentiment Intelligence Dashboard")
st.write("Premium Real-Time NLP Dashboard for GitHub Portfolio")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = pd.read_csv("data/tweets.csv")

# ---------------------------------------------------
# SIMPLE REAL PREDICTION LOGIC
# ---------------------------------------------------
positive_words = ["love", "great", "good", "amazing", "awesome", "best", "happy"]
negative_words = ["bad", "worst", "hate", "terrible", "slow", "poor", "angry"]

def predict_sentiment(text):
    text = text.lower()

    if any(word in text for word in positive_words):
        return "Positive"
    elif any(word in text for word in negative_words):
        return "Negative"
    else:
        return "Neutral"

# Predict sentiments for dataset
df["sentiment"] = df["text"].apply(predict_sentiment)

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------
total = len(df)
pos = sum(df["sentiment"] == "Positive")
neg = sum(df["sentiment"] == "Negative")
neu = sum(df["sentiment"] == "Neutral")

col1, col2, col3, col4 = st.columns(4)

col1.metric("📌 Total Posts", total)
col2.metric("😊 Positive", pos)
col3.metric("😡 Negative", neg)
col4.metric("😐 Neutral", neu)

st.markdown("---")

# ---------------------------------------------------
# USER INPUT PREDICTION BOX
# ---------------------------------------------------
st.subheader("🤖 Real-Time Sentiment Predictor")

user_text = st.text_area("Enter Tweet / Review / Comment")

if st.button("Analyze Sentiment"):
    result = predict_sentiment(user_text)
    st.success(f"Predicted Sentiment: {result}")

st.markdown("---")

# ---------------------------------------------------
# PIE CHART
# ---------------------------------------------------
col5, col6 = st.columns(2)

with col5:
    fig = px.pie(
        df,
        names="sentiment",
        title="📊 Sentiment Distribution",
        hole=0.45
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# TREND GRAPH
# ---------------------------------------------------
with col6:
    trend_data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Positive": [5, 7, 6, 8, 10, 9, 11]
    })

    fig2 = px.line(
        trend_data,
        x="Day",
        y="Positive",
        markers=True,
        title="📈 Weekly Positive Trend"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------
# WORD CLOUD
# ---------------------------------------------------
st.subheader("☁️ Trending Words")

text = " ".join(df["text"].astype(str))

wc = WordCloud(
    width=900,
    height=400,
    background_color="black",
    colormap="Set2"
).generate(text)

fig3, ax = plt.subplots(figsize=(12,5))
ax.imshow(wc, interpolation="bilinear")
ax.axis("off")

st.pyplot(fig3)

st.markdown("---")

# ---------------------------------------------------
# DOWNLOAD REPORT
# ---------------------------------------------------
st.subheader("📥 Download Sentiment Report")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV Report",
    data=csv,
    file_name="sentiment_report.csv",
    mime="text/csv"
)

st.markdown("---")

# ---------------------------------------------------
# LIVE TABLE
# ---------------------------------------------------
st.subheader("📢 Latest Social Media Posts")
st.dataframe(df, use_container_width=True)