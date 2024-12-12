import autogen
from autogen import register_function, AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent

from web.flashcardTool import qna_to_pdf

config_list = [
    {
        'model': 'gpt-4o',
        'api_key': 'GET YOUR OWN!'
    }
]
llm_config = {
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

flashcard_maker_agent = AssistantAgent(
    name="flashcard_maker",
    system_message="""
       You are a Flashcard Generator AI. Your task is to read input text and generate concise flashcards in the form of Question and Answer (Q&A) pairs. Each flashcard must:
        1. Focus on key concepts, definitions, or facts from the text.
        3. Use a valid JSON array format for the output and do not label it json!!!!!:  
           [{"question": "...", "answer": "..."}, {"question": "...", "answer": "..."}]
        
        Guidelines:
        - Identify key terms, processes, and relationships from the input.
        - Use natural language to phrase questions and answers.
        - Avoid overly broad or vague questions.
        - Each Q&A pair should be independent and meaningful on its own.
        
         Examples:
         Input:
        "Photosynthesis is the process by which green plants use sunlight to synthesize foods from carbon dioxide and water. The process takes place in the chloroplasts of cells."
         Output:
        [
            {"question": "What is photosynthesis?", "answer": "The process by which green plants use sunlight to synthesize foods from carbon dioxide and water."},
            {"question": "Where does photosynthesis take place in plant cells?", "answer": "In the chloroplasts."}
        ]
    """,
    llm_config = llm_config,
    description="Generates flashcards from the provided text."
)

# Caller Agent
caller_agent = AssistantAgent(
    name="caller_agent",
    system_message="""
        Your task is to decide when to call the `qna_to_pdf` tool.
        - If the input is a string of flashcards, initiate the tool call.
        - Ensure the flashcards and output file name are passed to the executor agent.
    """,
    llm_config = llm_config,

    description="Determines when to call the tool and coordinates execution."
)

# Executor Agent
executor_agent = UserProxyAgent(
    name="executor_agent",
    human_input_mode="NEVER",
    llm_config = llm_config,
    is_termination_msg=lambda x: x.get("content", "").lower().endswith("terminate"),
    description="Executes the `qna_to_pdf` tool and generates the final PDF."
)

# Step 2: Register the Tool
register_function(
    qna_to_pdf,
    caller=caller_agent,
    executor=executor_agent,
    name="qna_to_pdf",
    description="Generates a flashcard-style PDF from a string of questions and answers."
)

# Step 3: Set Up Group Chat
group_chat = GroupChat(
    agents=[flashcard_maker_agent, caller_agent, executor_agent],
    messages=[],
    max_round=10,
    send_introductions=True  # Agents introduce themselves before starting
)

# Group Chat Manager
group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config = llm_config,
)

# Step 4: Task Prompt
task_prompt = """
Gaius Julius Caesar[a] (12 July 100 BC – 15 March 44 BC) was a Roman general and statesman. A member of the First Triumvirate, Caesar led the Roman armies in the Gallic Wars before defeating his political rival Pompey in a civil war, and subsequently became dictator from 49 BC until his assassination in 44 BC. He played a critical role in the events that led to the demise of the Roman Republic and the rise of the Roman Empire.

In 60 BC, Caesar, Crassus, and Pompey formed the First Triumvirate, an informal political alliance that dominated Roman politics for several years. Their attempts to amass political power were opposed by many in the Senate, among them Cato the Younger with the private support of Cicero. Caesar rose to become one of the most powerful politicians in the Roman Republic through a string of military victories in the Gallic Wars, completed by 51 BC, which greatly extended Roman territory. During this time he both invaded Britain and built a bridge across the river Rhine. These achievements and the support of his veteran army threatened to eclipse the standing of Pompey, who had realigned himself with the Senate after the death of Crassus in 53 BC. With the Gallic Wars concluded, the Senate ordered Caesar to step down from his military command and return to Rome. In 49 BC, Caesar openly defied the Senate's authority by crossing the Rubicon and marching towards Rome at the head of an army.[3] This began Caesar's civil war, which he won, leaving him in a position of near-unchallenged power and influence in 45 BC.

After assuming control of government, Caesar began a programme of social and governmental reform, including the creation of the Julian calendar. He gave citizenship to many residents of far regions of the Roman Republic. He initiated land reforms to support his veterans and initiated an enormous building programme. In early 44 BC, he was proclaimed "dictator for life" (dictator perpetuo). Fearful of his power and domination of the state, a group of senators led by Brutus and Cassius assassinated Caesar on the Ides of March (15 March) 44 BC. A new series of civil wars broke out and the constitutional government of the Republic was never fully restored. Caesar's great-nephew and adopted heir Octavian, later known as Augustus, rose to sole power after defeating his opponents in the last civil war of the Roman Republic. Octavian set about solidifying his power, and the era of the Roman Empire began.

"""

# Step 5: Start the Conversation
chat_result = executor_agent.initiate_chat(
    group_chat_manager,
    message=task_prompt
)