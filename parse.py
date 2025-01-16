from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
template = (
    "Extract the following information from this text: {dom_content}\n"
    "Description: {parse_description}\n"
    "Return only the extracted data, or an empty string if no match is found. make sure return all extracted data"
)

model = OllamaLLM(model= 'llama3')

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt|model
    parsed_results = []
    for i, chunk in enumerate(dom_chunks,start=1):
        response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
        print(f"parsed batch {i} of {len(dom_chunks)}")
        parsed_results.append(response)
    return "\n".join(parsed_results)