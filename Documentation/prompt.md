# 📜 Prompt

Prompts are currently stored in `backend/app/llm/prompts.py`.\
The agent prompt is currently hard-coded in the codebase but can be moved to `prompts.py` for better modularity.\
**Last updated:** *2025-08-29*

- **System Prompt:** A hidden instruction provided by the system (OpenAI, developers, or applications) that defines the AI's role, behavior, and limitations.
- **User Prompt:** The message entered by the user during interaction.

**Note:** System prompts take precedence over user prompts. If there is a conflict between the two, the system prompt will override the user prompt.

## Reference
- [LangChain Prompts](https://python.langchain.com/api_reference/core/prompts.html)
