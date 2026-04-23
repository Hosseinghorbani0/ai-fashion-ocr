
# AI Fashion OCR – Yunika Smart Assistant

An intelligent fashion assistant web application developed for **Yunika Atelier**.  
It combines **GPT‑4o‑mini chatbot** with **custom CNN‑based image recognition** to provide a complete support experience for customers.  
Users can chat about products, pricing, sizing, and atelier policies, or **upload a garment photo** – the system will automatically extract fashion attributes using deep learning.

> A small note: this project was built for **Yunika** – a fashion atelier.

---

## Key Capabilities

### 🧠 Garment Analysis (OCR‑like understanding)
When a customer uploads a photo, the system predicts four attributes via dedicated CNN models:

- **Size** (atelier standard: size 1 ≈ EU 42, size 2 ≈ EU 48)
- **Length** (cm)
- **Price** (Iranian Toman)
- **Fabric type** (e.g., cotton, fleece, velvet)

The models are trained on a dataset of product images and use a uniform architecture (4 convolutional layers + dense layers, 35‑class softmax).

### 💬 AI Chatbot (GPT‑4o‑mini)
- Persian‑language assistant with a custom system prompt defining Yunika’s identity, location, working hours, product range, and ordering process.
- Maintains conversation history per user (SQLite).
- Can automatically send seasonal product images (winter / spring manteau collections) when the user asks for photos.
- HTML‑formatted answers with emojis.

### 🌐 Web Interface
- Responsive HTML/CSS (mobile‑friendly)
- Modal to enter mobile number (used as `user_id` for chat history)
- Floating chat button, preset questions, image upload button
- Typing indicator during AI response

### 🖧 Backend (Flask)
- `/chat` – handles text, calls GPT, stores conversation in `chat.db`
- `/upload` – processes image, runs four CNN models, returns JSON predictions
- CORS enabled for local development

---

## Technology Stack (Key Libraries)

| Library | Purpose |
|---------|---------|
| `flask` + `flask_cors` | Web server and cross‑origin requests |
| `openai` | GPT‑4o‑mini API |
| `tensorflow` / `keras` | Load and run CNN models |
| `opencv‑python` | Image loading, resizing, grayscale conversion |
| `numpy` | Array manipulation |
| `scikit‑learn` | Label encoding (inverse transform of predictions) |
| `sqlite3` | Chat history storage |
| `base64` | Image encoding for JSON responses |

---

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai-fashion-ocr.git
   cd ai-fashion-ocr
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-cors openai tensorflow opencv-python numpy scikit-learn pandas openpyxl
   ```

4. **Place trained model files** in the project root:
   - `modelsize.h5`
   - `modelghad.h5`
   - `modelgheymat.h5`
   - `modeljense.h5`

5. **Prepare demo product images** (optional for chatbot’s automatic replies):
   - `ax/winter/1.jpg` … `5.jpg`
   - `ax/spring/1.jpg` … `5.jpg`

6. **Set up API key** – **do not hardcode**.
   Create a `.env` file:
   ```ini
   OPENAI_API_KEY=your_actual_openai_key
   ```
   Modify `app.py` to load it:
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
   ```

7. **Run the Flask server**
   ```bash
   python app.py
   ```
   The server will start at `http://0.0.0.0:5000`.  
   Open `index.html` in a browser (or serve it via a simple HTTP server).

---

## API Endpoints

### `POST /chat`
Request JSON:
```json
{
  "phone": "0912xxxxxxx",
  "content": "قیمت مانتوهای زمستانه چقدر است؟"
}
```
Response:
```json
{
  "message": "... (HTML formatted answer)",
  "images": ["data:image/jpeg;base64,...", ...]
}
```
The `images` array contains Base64‑encoded product photos when the user asks for winter/spring manteau pictures.

### `POST /upload`
Multipart form with `image` file.  
Response:
```json
{
  "message": [
    {"سایز": 44},
    {"قیمت": 3600000},
    {"قد": 70},
    {"جنس": "فوتر آستردار"}
  ]
}
```

---

## CNN Model Architecture (identical for all four tasks)

- Input: 32×32×1 (grayscale, normalised)
- Conv2D 128 (3×3) → MaxPool → Dropout(0.3)
- Conv2D 256 (3×3) → MaxPool → Dropout(0.3)
- Conv2D 320 (3×3) → MaxPool → Dropout(0.3)
- Conv2D 256 (3×3) → Flatten
- Dense 128 → Dropout(0.3)
- Dense 35 (softmax)

Trained for 500 epochs – achieves near 100% training accuracy (dataset is limited; for production consider more varied data).

---

## Project Structure

```
.
├── app.py (or newfile.py)   # Flask application
├── index.html               # Frontend chat UI
├── styles.css               # Styling
├── modelsize.h5             # Size predictor
├── modelghad.h5             # Length predictor
├── modelgheymat.h5          # Price predictor
├── modeljense.h5            # Fabric predictor
├── chat.db                  # SQLite DB (auto‑created)
├── uploads/                 # Temporary uploaded images
├── ax/
│   ├── winter/
│   │   └── 1.jpg ... 5.jpg
│   └── spring/
│       └── 1.jpg ... 5.jpg
├── .env                     # Environment variables (never commit)
└── README.md
```

---

## Security & Production Notes

- **Never commit** `.env` or hardcoded API keys.
- Add `.env`, `uploads/`, `chat.db`, `__pycache__/`, `*.pyc` to `.gitignore`.
- Do not use `debug=True` in production; use a WSGI server (Gunicorn, Waitress).
- The current code stores chat history with only a mobile number as user ID – consider adding more robust user authentication if needed.

---

## License

 License – free to use, modify, and distribute with attribution.

---

## Author

Built for **Yunika Atelier**.  
Original implementation by [hosseinghorbani0](https://github.com/hosseinghorbani0) – 2024–2025.
