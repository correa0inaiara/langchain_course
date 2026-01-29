from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq


def generate_pet_name():
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    
    response = llm.invoke("Eu tenho um cachorro, uma cachorra, um gato e uma gata, e quero nomes legais para todos. Me sugira 5 nomes para cada um.")

    return response.content

if __name__ == "__main__":
    print(generate_pet_name())