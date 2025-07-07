## RAG Pipeline with OpenAI API (Flask + Vue)

This project connects a Vue frontend with a Flask backend that implements a basic RAG (Retrieval-Augmented Generation) pipeline using the OpenAI API.

### Setup

**Backend**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

Create a `.env` file inside the `backend` folder with your OpenAI key:

```
OPENAI_API_KEY=your-openai-key
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

In the `frontend/.env` file, set the backend API URL:

```
VITE_API_URL=http://127.0.0.1:5000
```

