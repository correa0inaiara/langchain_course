from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import LLMChain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

video_url = "https://www.youtube.com/watch?v=-Osca2Zax4Y"
def create_vector_db_from_youtube_url(video_url: str) -> FAISS:
    loader = YoutubeLoader.from_youtube_url(video_url)
    transcript = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)
    
    db = FAISS.from_documents(docs, embeddings)
    return db

print(create_vector_db_from_youtube_url(video_url))

def get_response_from_query(db, query, k=4):
    # have in mind the limit amount of tokens allowed by the library
    
    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])
    
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful YouTube assistant that answers questions about video transcripts."),
        ("human", """Answer this question: {question}
        
        Using only this transcript: {docs}
        
        Rules:
        - Use ONLY factual information from the transcript
        - If information is not in the transcript, say "I don't know"
        - Provide detailed answers""")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({
        "question": query,
        "docs": docs_page_content
    })
    
    return response.content