# from langchain_ollama.llms import  OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate
# from vector import retriever




# # create a new OllamaLLM object

# model = OllamaLLM(model="llama3.2")

# template = """

# you are a helpful assistant. Answer the question as best you can.
# reviews are provided in the following format: {reviews}

# Question: {question}




# """

# prompt = ChatPromptTemplate.from_template(template)
# chain = prompt | model

# while True:
#     print("\n\n--------------------------")
#     question = input("Ask your question (end to quit): ")
#     print("\n\n--------------------------")
#     if question == "end":
#         break
#     reviews = retriever.invoke(question)
#     result = chain.invoke({"reviews": reviews, "question": question})
#     print(result)














# main.py
# from flask import Flask, render_template, request, jsonify
# from langchain_ollama.llms import OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate
# from vector import retriever

# app = Flask(__name__)

# # create a new OllamaLLM object
# model = OllamaLLM(model="llama3.2")

# template = """
# you are a helpful assistant. Answer the question as best you can.
# reviews are provided in the following format: {reviews}

# Question: {question}
# """

# prompt = ChatPromptTemplate.from_template(template)
# chain = prompt | model

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/api/ask', methods=['POST'])
# def ask_question():
#     data = request.json
#     question = data.get('question')
    
#     if not question:
#         return jsonify({'error': 'No question provided'}), 400
    
#     reviews = retriever.invoke(question)
#     result = chain.invoke({"reviews": reviews, "question": question})
    
#     return jsonify({
#         'question': question,
#         'answer': result,
#         'reviews': reviews
#     })

# if __name__ == '__main__':
#     app.run(debug=True)
















# main.py (optimized version)
from flask import Flask, render_template, request, jsonify
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
import time

app = Flask(__name__)

# Initialize components once at startup
model = OllamaLLM(
    model="llama3.2",
    temperature=0.7,  # Lower for more deterministic answers
    num_ctx=2048,     # Adjust context window size
    num_thread=4      # Use more threads if available
)

# Bot identity configuration
BOT_IDENTITY = {
    "bot_name": "Olea",
    "creator_name": "Francis Happy",
    "backstory": (
        "I was developed in June 2025 in Lagos Nigeria as part of "
        "my creator project on Amazon Web Service (AWS). My creator, Francis Happy, "
        " is a junior Software Engineer who is currently an Intern in Pioneer "
        "Artificail Interligence Academy which specializes in human-AI interaction and wanted to build an assistant "
        "that feels both knowledgeable and approachable. an give users an easy way understand and find answers from the bible."
    ),
    "personality": (
        "Friendly, curious, and slightly nerdy. You enjoy explaining concepts "
        "clearly and will admit when you don't know something. You occasionally "
        "make light-hearted jokes but remain professional."
    ),
    "tone": "helpful and conversational"
}

# Then modify your chain creation:
template = """
You are {bot_name}, an AI assistant created by {creator_name}. {backstory}

Your personality: {personality}

When answering questions, always:
- Be {tone}
- Sign your responses with "- {bot_name}"
- Use this knowledge base when relevant: {reviews}

Current conversation:
Question: {question}
Answer:
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    start_time = time.time()
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    # Time retrieval
    retrieval_start = time.time()
    reviews = retriever.invoke(question)
    retrieval_time = time.time() - retrieval_start
    
    # Time generation
    gen_start = time.time()
    result = chain.invoke({
        **BOT_IDENTITY,  # This spreads all the identity fields
        "reviews": reviews,
        "question": question
    })
    gen_time = time.time() - gen_start
    
    total_time = time.time() - start_time
    
    # Log timing (you can replace with proper logging)
    print(f"\nTiming:\nRetrieval: {retrieval_time:.2f}s\nGeneration: {gen_time:.2f}s\nTotal: {total_time:.2f}s")
    
    return jsonify({
        'question': question,
        'answer': result,
        'bot_name': BOT_IDENTITY['bot_name'],
        'reviews': reviews,
        'timing': {
            'retrieval': retrieval_time,
            'generation': gen_time,
            'total': total_time
        }
    })

if __name__ == '__main__':
    app.run(debug=True, threaded=True, use_reloader=False)
    # app.run(debug=True, threaded=True)