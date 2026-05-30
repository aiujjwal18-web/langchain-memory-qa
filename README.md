\# LangChain Memory QA (CLI)



This project is a small command-line assistant built with LangChain and OpenAI.  

It focuses on two ideas:



\- Keeping the code and workflow as simple as possible

\- Practicing a full end‑to‑end loop: local project → LangChain → safe public GitHub repo



The assistant runs in your terminal, answers questions, and keeps a lightweight conversation history in memory so it can understand simple follow‑up questions.



\---



\## Features



\- \*\*Command-line interface\*\*  

&#x20; Run the assistant directly from your terminal and chat interactively.



\- \*\*LangChain + OpenAI Chat model\*\*  

&#x20; Uses `langchain-openai` and `ChatOpenAI` with the `gpt-4o-mini` model (configurable in code).



\- \*\*Simple conversation memory\*\*  

&#x20; Maintains a `conversation\_history` string and sends it along with each new question so the model can see previous Q\&A and handle follow‑ups more naturally.



\- \*\*Structured answer format\*\*  

&#x20; The prompt asks the model to:

&#x20; - Start with 2–3 short sentences answering the question directly.

&#x20; - Follow with 3–5 bullet points summarizing key takeaways or steps.



\- \*\*Environment-variable based API key\*\*  

&#x20; The OpenAI API key is read from the `OPENAI\_API\_KEY` environment variable and is \*\*not\*\* hard-coded anywhere in the repository.



> Note: At this stage, there is no dedicated `clear memory` command in the script. Conversation history persists for the duration of the process and resets when the script exits.



\---



\## How it works (high level)



1\. On startup, the script calls `build\_chain()`:

&#x20;  - Reads `OPENAI\_API\_KEY` from environment variables.

&#x20;  - Creates a `ChatOpenAI` instance.

&#x20;  - Builds a `ChatPromptTemplate` that includes:

&#x20;    - A system-style description of the assistant.

&#x20;    - A `{history}` placeholder for previous conversation.

&#x20;    - A `{question}` placeholder for the new user question.

&#x20;  - Wraps everything in a simple LangChain runnable pipeline with:

&#x20;    - `RunnablePassthrough()` to forward input fields.

&#x20;    - The prompt.

&#x20;    - The LLM.

&#x20;    - A `StrOutputParser` to return plain text.



2\. In `main()`:

&#x20;  - A `conversation\_history` string is initialized empty.

&#x20;  - The script enters an infinite loop, reading user input from `stdin`.

&#x20;  - For each non-empty, non-exit input:

&#x20;    - Calls `qa\_chain.invoke({"question": user\_question, "history": conversation\_history})`.

&#x20;    - Prints the model’s answer.

&#x20;    - Appends the new Q\&A to `conversation\_history`, which is sent on the next turn.



3\. When the user types `exit` or `quit`:

&#x20;  - The loop breaks.

&#x20;  - The process ends, and memory is lost (no persistence to disk).



This design keeps the code minimal while demonstrating how to add simple conversational context to a LangChain-based assistant.



\---



\## Requirements



\- Python 3.10+ (recommended)

\- A valid OpenAI API key

\- The following Python packages:

&#x20; - `langchain-openai`

&#x20; - `langchain-core`



\---



\## Setup and installation



1\. \*\*Clone the repository\*\*



&#x20;  ```bash

&#x20;  git clone https://github.com/aiujjwal18-web/langchain-memory-qa.git

&#x20;  cd langchain-memory-qa

&#x20;  ```



2\. \*\*Create and activate a virtual environment (Windows, PowerShell)\*\*



&#x20;  ```bash

&#x20;  python -m venv .venv

&#x20;  .\\.venv\\Scripts\\Activate.ps1

&#x20;  ```



3\. \*\*Install dependencies\*\*



&#x20;  ```bash

&#x20;  pip install langchain-openai langchain-core

&#x20;  ```



4\. \*\*Set your OpenAI API key (do not commit this)\*\*



&#x20;  ```bash

&#x20;  $env:OPENAI\_API\_KEY="sk-REPLACE-WITH-YOUR-KEY"

&#x20;  ```



&#x20;  The script reads this environment variable internally and will raise an error if it’s missing.



\---



\## Running the assistant



With the virtual environment active and `OPENAI\_API\_KEY` set:



```bash

python qa\_chain.py

```



You should see:



```text

Interactive LangChain QA with simple memory. Type 'exit' to quit.

```



Then you can type questions, for example:



\- `What is a Python virtual environment?`

\- `How does that help an operations manager?`



Because previous Q\&A is passed in the `{history}` prompt variable, the second question can implicitly refer to “that” and the model still understands the context.



Type `exit` or `quit` to end the session.



\---



\## Memory behavior



\- The script stores conversation context in a single string called `conversation\_history`.

\- After each answer, the script appends:



&#x20; ```text

&#x20; Q: <your question>

&#x20; A: <assistant answer>

&#x20; ```



\- On the next turn, this full history is sent to the model via the `{history}` placeholder in the prompt.

\- Memory exists \*\*only in RAM\*\*:

&#x20; - It resets when the script is restarted.

&#x20; - It is not written to any file or database.



This is intentionally simple and meant as a learning step before using more advanced LangChain memory utilities.



\---



\## Security and API key handling



This project is public. To avoid exposing secrets:



\- The OpenAI API key is \*\*never\*\* hard-coded in Python files.

\- The key is stored only in an environment variable (`OPENAI\_API\_KEY`) on the local machine.

\- `.gitignore` excludes:

&#x20; - The virtual environment directory: `.venv/`

&#x20; - Cached Python bytecode: `\_\_pycache\_\_/`

&#x20; - `.env` files (if you choose to use one locally)



Before pushing to GitHub, you can quickly scan for leaked OpenAI-style keys using:



```bash

git grep "sk-"

```



If this prints nothing, there is no committed string containing `sk-` in tracked files.



If a key is ever accidentally committed:



1\. Immediately rotate or revoke the API key in the OpenAI dashboard.

2\. Remove the key from the code, commit the cleanup, and push.

3\. Optionally, rewrite Git history to remove the secret completely.



\---



\## Future improvements (planned)



This repository is intentionally kept small and focused. Possible next steps:



\- Add a `clear memory` command (e.g., typing `"clear memory"` in the CLI resets `conversation\_history`).

\- Limit in-memory history to the last N turns to keep prompts compact.

\- Experiment with LangChain’s built-in memory utilities such as `ConversationBufferMemory` or `ConversationSummaryBufferMemory`.

\- Add additional tools (summarization, document Q\&A, etc.) and route between them based on user intent.



These improvements will build on the same pattern: environment-based secrets, simple LangChain primitives, and a clear end-to-end workflow.



\---



\## License



This project is for learning and experimentation.  

Choose and add a license if you plan to reuse or extend it in other contexts.

