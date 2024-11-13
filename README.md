# Visual Search for E-Commerce Store 🛍️

## Overview 🔍
This project enables **visual search** for an e-commerce store, where users can upload an image and receive similar product recommendations. Instead of typing a text query, the user simply uploads an image (e.g., a pair of swimming trunks 🩳), and the system will analyze the image and return matching products from the catalog.

## Technologies Used ⚙️

1. **Frontend**:
   - **Tools**: HTML, CSS, JavaScript
   - **Function**: The user interface where users upload images. The frontend sends the image to the backend for processing and displays the results.

2. **Backend**:
   - **Tool**: Flask (Python)
   - **Function**: Handles incoming requests, processes the uploaded image, interacts with Pinecone to search for similar products, and sends results back to the frontend.

3. **Image Embedding**:
   - **Tool**: ResNet50 (Pre-trained deep learning model)
   - **Function**: Converts the uploaded image into an embedding (a vector of numbers) that captures its unique features, making it comparable with other product images.

4. **Embedding Storage & Similarity Search**:
   - **Tool**: Pinecone
   - **Function**: Stores embeddings for all catalog items, enabling fast similarity searches.
   - **Search Criteria**: The system retrieves the **top 5 similar items** based on **cosine similarity**, with a threshold score of **0.70** to ensure relevance.

5. **Metadata Storage**:
   - **Tool**: SQLite
   - **Function**: Stores metadata for each product (e.g., ID, name, price). After retrieving similar embeddings from Pinecone, Flask uses the product IDs to fetch complete details from SQLite.

6. **Result Display**:
   - **Function**: The backend sends the product details (name, price, etc.) and images back to the frontend, which displays the top-matching products.

## Project Structure 📁

```
Visual Search/
   ├── app.py               # Main Flask backend file
   ├── templates/
   │   └── index.html       # Frontend HTML file
   ├── static/
   │   ├── Images/          # Folder containing product images
   │   ├── script.js        # JavaScript for frontend functionality
   │   └── style.css        # CSS for frontend styling
   ├── catalogs/            # Product catalog images and metadata
   ├── Product.db           # SQLite database with product metadata
   ├── .env                 # Environment file with Pinecone API key
   └── requirements.txt     # List of required Python packages
```

## Getting Started 🚀

### Prerequisites 🛠️

1. **Python** (>= 3.6)
2. **Flask** (Web framework)
3. **ResNet50** (Pre-trained deep learning model)
4. **Pinecone** (Vector database for similarity search)
5. **SQLite** (Relational database for metadata)

### Setup 🧑‍💻

1. Clone the repository to your local machine.
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your **Pinecone API Key**:

   ```
   PINECONE_API_KEY=your_pinecone_api_key
   ```

### Running the Application 🚂

1. Start the Flask app:

   ```bash
   python app.py
   ```

2. Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000) to interact with the visual search.

---

### Demo

https://github.com/user-attachments/assets/e6559b14-92e1-433c-a02a-b6ce9408a3ee




