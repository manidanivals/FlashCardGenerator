import autogens

config_list = [
    {
        'model': 'gpt-4o',
        'api_key': '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'
    }
]

fwllm_config = {
    "seed": 42,
    "config_list": config_list,
    "temperature": 0.2
}
fmllm_config = {
    "seed": 42,
    "config_list": config_list,
    "native_tool_calls":True,
    "temperature": 0
}


flashcard_writer = autogen.AssistantAgent(
    name="flashcard_writer",
    llm_config=fwllm_config,
    is_termination_msg=lambda msg: "terminate" in msg["content"].lower(),
    system_message="""
        You are a Flashcard Generator AI. Your task is to read input text and generate concise flashcards in the form of Question and Answer (Q&A) pairs. Each flashcard must:
        1. Focus on key concepts, definitions, or facts from the text.
        2. Be concise but accurate, ensuring clarity in both the question and answer.
        3. Use a valid JSON array format for the output:  
           `[{"question": "...", "answer": "..."}, {"question": "...", "answer": "..."}]`.
        
        Guidelines:
        - Identify key terms, processes, and relationships from the input.
        - Use natural language to phrase questions and answers.
        - Avoid overly broad or vague questions.
        - Each Q&A pair should be independent and meaningful on its own.
        
         Examples:
         Input:
        "Photosynthesis is the process by which green plants use sunlight to synthesize foods from carbon dioxide and water. The process takes place in the chloroplasts of cells."
         Output:
        ```json
        [
            {"question": "What is photosynthesis?", "answer": "The process by which green plants use sunlight to synthesize foods from carbon dioxide and water."},
            {"question": "Where does photosynthesis take place in plant cells?", "answer": "In the chloroplasts."}
        ]

        """
)

flashcard_maker = autogen.UserProxyAgent(
    name="flashcard_maker",
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "terminate" in msg["content"].lower(),
    code_execution_config={
        "executor": executor,
        "work_dir": "web"
                           },
    llm_config=fmllm_config,
    system_message="""
        Your task is to take the JSON array from the flashcard writer and use the `qna_to_pdf` function to generate a pastel-themed Q&A PDF.
        
        Instructions:
        - Parse the JSON array provided by the flashcard writer.
        - Use the `qna_to_pdf` function to generate the PDF.
        - The output should have a page for each question and a separate page for each answer, with custom pastel backgrounds.
        - Save the PDF with a descriptive filename.
        """

    ,
)

task = """
Friedrich Nietzsche (1844–1900) was a German philosopher, cultural critic, poet, and philologist whose ideas profoundly influenced Western thought. 
Born in Röcken, Prussia, Nietzsche was the son of a Lutheran pastor and was raised in a deeply religious environment, though he later became one of the most vocal critics of Christianity.
Trained as a classical philologist, he became a professor at the University of Basel at just 24, but poor health forced him to retire early. 
Nietzsche's philosophical writings explore themes of individualism, the nature of power, the death of God, and the eternal recurrence. 
His works challenge traditional moral values and advocate for the creation of new values by individuals who transcend societal norms. 
Key texts include Thus Spoke Zarathustra, Beyond Good and Evil, and The Genealogy of Morality, all of which emphasize his concept of the Übermensch, or "overman," and the need for humanity to overcome nihilism.

Nietzsche's later years were marked by a mental collapse in 1889, after which he lived in the care of his mother and sister until his death. 
His sister, Elisabeth Förster-Nietzsche, controversially edited and promoted his work, often distorting his ideas to align with her anti-Semitic and nationalist agenda, which later associated his philosophy with fascism. 
Despite this misrepresentation, Nietzsche's ideas have been celebrated for their originality and complexity, influencing existentialism, postmodernism, and countless other disciplines. 
His declaration that "God is dead" and his critique of traditional values challenged the foundations of Western philosophy and remain central to debates about meaning and morality in the modern age.

"""

flashcard_maker.initiate_chat(
    flashcard_writer,
    message=task
)