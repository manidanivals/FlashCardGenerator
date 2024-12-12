# Flashcard PDF Generator

This project implements a multi-agent system to generate a PDF of flashcards from a given text prompt. It uses the **AutoGen** framework to define agents that collaborate to perform distinct tasks like generating flashcards, deciding when to invoke a tool, and executing the tool to create the final PDF.

## Project Structure

### Agents

1. **Flashcard Maker Agent**
   - Reads the input prompt and generates structured flashcards (questions and answers).
   - Passes the generated flashcards to the next agent in the workflow.

2. **Caller Agent**
   - Determines when the `qna_to_pdf` tool should be called.
   - Passes the flashcards and output file name to the Executor Agent for processing.

3. **Executor Agent**
   - Executes the `qna_to_pdf` tool to generate the final PDF.
   - Returns the result of the execution.

4. **Group Chat Manager**
   - Orchestrates the interaction between agents.
   - Ensures agents collaborate effectively and selects the next agent to speak based on the configured strategy.

### Tool

#### `qna_to_pdf`
- Function to generate a PDF from a string of flashcards (questions and answers).
- Simulates tool execution and returns a success message.

```python
# Example
qna_to_pdf("[{'question': 'What is Python?', 'answer': 'A programming language.'}]", "output.pdf")
# Output: "PDF generated successfully: output.pdf"
```

## Workflow

1. **Prompt Input**:
   - The user provides a text prompt (e.g., a biography of Friedrich Nietzsche).

2. **Flashcard Generation**:
   - The Flashcard Maker Agent reads the prompt and creates structured flashcards.

3. **Tool Call Decision**:
   - The Caller Agent decides when to invoke the `qna_to_pdf` tool.

4. **PDF Generation**:
   - The Executor Agent executes the `qna_to_pdf` tool to create the flashcard PDF.

5. **Orchestration**:
   - The Group Chat Manager coordinates communication between agents.

## Setup and Installation

### Prerequisites
- Python 3.12+
- **AutoGen** framework

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### API Key
This project uses OpenAI's GPT-4o model. Set your API key as an environment variable:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

## Usage

### Running the Project

Execute the main script:
```bash
python main.py
```

### Example Task
Given the following input prompt:
```text
Friedrich Nietzsche (1844–1900) was a German philosopher, cultural critic, poet, and philologist whose ideas profoundly influenced Western thought.....
```
The system will:
1. Generate flashcards like:
   ```json
   [
       {"question": "Who was Friedrich Nietzsche?", "answer": "A German philosopher, cultural critic, poet, and philologist who influenced Western thought."},
       {"question": "What is Nietzsche's famous declaration about God?", "answer": "He declared that 'God is dead,' challenging traditional values."}
   ]
   ```
2. Create a PDF named `Nietzsche_QA_Flashcards.pdf` with these flashcards.

### Output
The generated PDF will have a page for each question and its corresponding answer, styled with pastel backgrounds.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- [AutoGen Framework](https://github.com/microsoft/autogen) for multi-agent orchestration.
- OpenAI for GPT-4 API.

