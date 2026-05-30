import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def build_chain():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        api_key=api_key,
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are a helpful assistant.

Tone: professional.
Audience: Operations Manager or AI Manager.

Here is the previous conversation so far (it may be empty):
{history}

You must always:
- Answer clearly and concisely.
- Use simple language suitable for the audience.
- Follow the output format strictly.

Question:
{question}

Output format:
1) Start with 2–3 short sentences that directly answer the question.
2) Then add 3–5 bullet points with key takeaways or steps.

Answer:
"""
    )

    parser = StrOutputParser()

    chain = (
        {
            "question": RunnablePassthrough(),
            "history": RunnablePassthrough(),
        }
        | prompt
        | llm
        | parser
    )

    return chain


def main():
    qa_chain = build_chain()

    print("Interactive LangChain QA with simple memory. Type 'exit' to quit.\n")

    conversation_history = ""

    while True:
        try:
            user_question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not user_question:
            continue

        if user_question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        try:
            answer = qa_chain.invoke(
                {
                    "question": user_question,
                    "history": conversation_history,
                }
            )

            print("\n--- Answer ---")
            print(answer)
            print("--------------\n")

            conversation_history += f"\nQ: {user_question}\nA: {answer}\n"

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()