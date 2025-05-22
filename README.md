# ChatTell: Systems Biology Chatbot

ChatTell is a conversational assistant that integrates a large language model with the Tellurium systems biology toolkit, allowing you to run simulations, query models, and visualize results directly from a chat interface.

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/adelhpour/tellurium_chatbot.git
   cd tellurium_chatbot
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\\Scripts\\activate      # Windows
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the LLM**

   You have two options:

   * **Local LLM (Ollama)**
     Install Ollama by following the instructions on the official download page: [https://ollama.com/download](https://ollama.com/download)

     Once installed, pull the model of your choice (e.g., llama3.2):

     ```bash
     ollama pull llama3.2
     ```

   * **OpenAI API**
     Obtain an API key from OpenAI and set it in a `.env` file or as an environment variable:

     * **.env file**
       Create a `.env` in the project root:

       ```ini
       OPENAI_API_KEY=your_openai_api_key_here
       ```
     * **Shell environment (macOS/Linux)**

       ```bash
       export OPENAI_API_KEY="your_openai_api_key_here"
       ```
     * **Windows environment**
       For details on setting environment variables in Windows, see: [https://phoenixnap.com/kb/windows-set-environment-variable](https://phoenixnap.com/kb/windows-set-environment-variable)

## Execution

Run the chatbot with one of the following commands:

* **Defaults**

  ```bash
  python main.py
  ```

* **Specify a different model**

  ```bash
  python main.py -m gpt-4o
  ```

* **Use CLI interface**

  ```bash
  python main.py -m gpt-4o -i cli
  ```

* **Use web (UI) interface**

  ```bash
  python main.py -m llama3.2 -i ui
  ```

**Flag definitions:**

* `-m <model>`: LLM model to use. Defaults to `llama3.2`.
* `-i <ui|cli>`: Interface type. Defaults to `cli`.

Noe that you only need to include flags when changing from the defaults.
