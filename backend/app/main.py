from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
import os

app = FastAPI(title="Text Summarizer API")

# Ensure NLTK data directory exists and set it explicitly
nltk_data_dir = os.path.join(os.path.expanduser('~'), 'nltk_data')
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)
nltk.data.path.append(nltk_data_dir)

# Download required NLTK data
required_packages = ['punkt', 'stopwords', 'averaged_perceptron_tagger']
for package in required_packages:
    try:
        if not nltk.data.find(f'tokenizers/{package}' if package == 'punkt' 
                             else f'corpora/{package}' if package == 'stopwords'
                             else f'taggers/{package}'):
            nltk.download(package, download_dir=nltk_data_dir, quiet=True)
    except Exception as e:
        print(f"Warning: Could not find/download {package}: {str(e)}")
        try:
            nltk.download(package, download_dir=nltk_data_dir, quiet=True)
        except Exception as e:
            print(f"Error downloading {package}: {str(e)}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3002", "http://localhost:3003", "http://localhost:3004"],
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
        # Input validation
        if not text_input.text or len(text_input.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        if len(text_input.text.split()) < 10:
            raise HTTPException(status_code=400, detail="Text must contain at least 10 words")
        
        if text_input.num_sentences < 1:
            raise HTTPException(status_code=400, detail="Number of sentences must be at least 1")

        # Parse the text
        parser = PlaintextParser.from_string(text_input.text, Tokenizer("english"))
        
        # Initialize the LSA summarizer
        stemmer = Stemmer("english")
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words("english")

        # Get the number of sentences in the original text
        num_sentences = len(parser.document.sentences)
        
        # Adjust num_sentences if it's larger than the input text
        requested_sentences = min(text_input.num_sentences, num_sentences)
        
        # Generate summary
        summary_sentences = summarizer(parser.document, requested_sentences)
        
        if not summary_sentences:
            raise HTTPException(status_code=400, detail="Could not generate summary. Text might be too short or invalid.")
            
        summary = " ".join([str(sentence) for sentence in summary_sentences])
        
        if not summary:
            raise HTTPException(status_code=400, detail="Generated summary is empty. Please try with different text.")

        return SummaryOutput(summary=summary)

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        print(f"Error generating summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 