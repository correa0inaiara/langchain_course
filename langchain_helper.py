from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generate_pet_name(animal_type: str, pet_color: str):
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente criativo para dar nomes a animais de estimação."),
        ("user", "Eu tenho {animal_type} de cor {pet_color} e quero nomes legais para ele. Me sugira 5 nomes.")
    ])
    
    chain = prompt_template | llm | StrOutputParser()
    
    response = chain.invoke({
            "animal_type": animal_type, 
            "pet_color": pet_color
        })

    return {"pet_name": response}

if __name__ == "__main__":
    # print(generate_pet_name(animal_type="um cachorro"))
    # print(generate_pet_name(animal_type="uma cachorra"))
    # print(generate_pet_name(animal_type="um gato"))
    # print(generate_pet_name(animal_type="uma gata"))
    print(generate_pet_name(animal_type="uma vaca", pet_color="preta"))