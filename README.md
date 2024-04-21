# SDG Analyzer

### Introduction
SDG Analyzer is a tool designed to analyze text documents and classify them according to the United Nations Sustainable Development Goals (SDGs). It extracts keywords from the input text, matches them with the SDG categories, and provides a weighted distribution of SDG relevance based on the extracted keywords.

### Features
- Keyword Extraction: Utilizes CKIP Transformers for Chinese text and KeyBERT for English text to extract relevant keywords from input documents.
- SDG Classification: Matches extracted keywords with pre-defined SDG categories using SentenceTransformer for word embeddings and cosine similarity for classification.
- Web Interface: Provides a user-friendly web interface powered by Flask framework for easy interaction.
- Visualization: Utilizes Highcharts for graphical representation of SDG distribution.

### Installation
1. Set up a clean environment.
2. Navigate to the `code` directory.
3. Install the required dependencies by running:
   ```
   pip install -r requirement.txt
   ```
4. Run the build script to download necessary models:
   ```
   python build.py
   ```
   This will create a `model` directory containing required model files.

### Usage
1. Navigate to the `flask` directory.
2. Run the Flask server by executing:
   ```
   python test_fast.py
   ```
3. Access the web interface by opening a browser and visiting [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Notes
- For faster performance, use `test_fast.py`. This loads pre-downloaded models locally.
- If you prefer slower execution but don't want to download models, use `test.py`.
- Ensure a stable internet connection for model downloads and updates.


### Demo
Watch the demo video on YouTube: [SDG Analyzer Demo](https://youtu.be/dgrzvQBPfAA)

