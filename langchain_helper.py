from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_classic import hub
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.agent_toolkits import load_tools
from langchain_community.tools import Tool
import numexpr


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

def safe_calculator(expression: str) -> str:
    """Avalia uma expressão matemática de forma segura usando numexpr."""
    try:
        # Limpa espaços em branco e tenta avaliar diretamente
        expr = expression.strip()
        
        # Se a expressão começa com '=' (como planilhas), remove
        if expr.startswith('='):
            expr = expr[1:]
            
        # Avalia a expressão com numexpr
        # O numexpr já é seguro para expressões matemáticas básicas
        result = numexpr.evaluate(expr)
        return f"Result: {result}"
    except Exception as e:
        # Se falhar, tenta uma regex mais permissiva
        try:
            import re
            # Tenta encontrar qualquer sequência que pareça matemática
            # Captura números, operadores, parênteses, pontos decimais
            match = re.search(r'\(?[\d\+\-\*\/\.\s]+\)?', expression)
            if match:
                expr = match.group(0).strip()
                result = numexpr.evaluate(expr)
                return f"Result: {result}"
        except:
            pass
        return f"Error calculating '{expression}': {e}"
    

def langchain_agent():
    
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    
    wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    
    math_tool = Tool(
        name="Calculator",
        func=safe_calculator,
        description="Útil para quando você precisa responder perguntas de matemática. A entrada deve ser uma expressão matemática simples, como '(10+15)/2'."
    )
    
    # llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    # math_tool = Tool(
    #     name="Calculator",
    #     func=llm_math_chain.run,
    #     description="Useful for when you need to answer questions about math"
    # )
    
    tools = [wikipedia_tool, math_tool]
    
    prompt = hub.pull("hwchase17/react")
    
    agent = create_react_agent(llm, tools, prompt)
    
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True,
        handle_parsing_errors=True
    )
    result = agent_executor.invoke({"input": "What is the average age of a dog? Multiply the age by 3"})

    print(result["output"])
    return result

if __name__ == "__main__":
    # print(generate_pet_name(animal_type="um cachorro"))
    # print(generate_pet_name(animal_type="uma cachorra"))
    # print(generate_pet_name(animal_type="um gato"))
    # print(generate_pet_name(animal_type="uma gata"))
    # print(generate_pet_name(animal_type="uma vaca", pet_color="preta"))
    langchain_agent()