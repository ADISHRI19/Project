FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .

# Install build tools and libraries for wordcloud/matplotlib
RUN apt-get update && apt-get install -y gcc g++ build-essential python3-dev libfreetype6-dev libpng-dev libopenblas-dev liblapack-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Install additional dependencies for Streamlit
RUN pip install streamlit pandas plotly matplotlib wordcloud

EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]