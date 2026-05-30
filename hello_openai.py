import os
from openai import OpenAI


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")

    client = OpenAI(api_key=api_key)

    # Let the user ask a question
    user_question = input("Enter your question: ").strip()
    if not user_question:
        print("Please enter a non-empty question.")
        return

    system_message = (
        "You are a professional communication assistant. "
        "Tone: professional. "
        "Audience: Operations Manager or AI Manager. "
        "You must follow this output format:\n"
        "1) Start with 2 simple sentences that directly explain the answer.\n"
        "2) Then add 2–3 bullet points with key takeaways.\n"
        "3) End with one short, powerful closing statement."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_question},
        ],
        max_tokens=250,
    )

    message_content = response.choices[0].message.content
    print("\n--- Answer ---")
    print(message_content)
    print("--------------")


if __name__ == "__main__":
    main()