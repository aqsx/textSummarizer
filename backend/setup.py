from setuptools import setup, find_packages

setup(
    name="text-summarizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sumy",
        "python-multipart",
        "pydantic",
        "python-dotenv",
        "nltk"
    ],
) 