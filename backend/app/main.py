from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk

app = FastAPI(title="Text Summarizer API")

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str
    num_sentences: int = 3

class SummaryOutput(BaseModel):
    summary: str

@app.post("/summarize", response_model=SummaryOutput)
async def summarize_text(text_input: TextInput):
    try:
        # Check if text is too short
        if len(text_input.text.split()) < 10:
            raise HTTPException(status_code=400, detail="Text is too short to summarize")

        # Parse the text
        parser = PlaintextParser.from_string(text_input.text, Tokenizer("english"))
        
        # Initialize the LSA summarizer
        stemmer = Stemmer("english")
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words("english")

        # Generate summary
        summary_sentences = summarizer(parser.document, text_input.num_sentences)
        summary = " ".join([str(sentence) for sentence in summary_sentences])

        return SummaryOutput(summary=summary)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 