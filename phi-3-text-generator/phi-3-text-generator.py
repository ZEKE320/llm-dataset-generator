# %%
from datetime import datetime
from pathlib import Path

import spacy
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama
from spacy.language import Language
from spacy.tokens.doc import Doc

TARGET_SENTENCE_COUNT = 100
OUTPUT_FILE_COUNT = 10
OUTPUT_DIRECTORY = "out"

# %%
spacy.cli.download("en_core_web_sm")


# %%
def generate_article(target_sentence_count: int) -> str:
    llm = Ollama(model="phi3:14b", base_url="http://host.docker.internal:11434")
    memory = ConversationBufferMemory()
    conversation = ConversationChain(llm=llm, memory=memory)

    first_prompt_template = PromptTemplate(
        template="Generate a {target_sentence_count}-sentence fictitious article.",
        input_variables=["target_sentence_count"],
    )
    continuation_prompt_template = PromptTemplate(
        template="Write a {target_sentence_count}-sentence sequel to the previous article.",
        input_variables=["target_sentence_count"],
    )

    result = conversation.predict(
        input=first_prompt_template.format(
            target_sentence_count=target_sentence_count,
        )
    )
    print(result)

    nlp: Language = spacy.load(name="en_core_web_sm")
    doc = nlp(result)
    sentence_count = len(list(doc.sents))
    print(f"---\nCurrent sentence count: {sentence_count}\n---")

    while sentence_count < target_sentence_count:
        response: str = conversation.predict(
            input=continuation_prompt_template.format(
                target_sentence_count=target_sentence_count,
            )
        )
        print(response)

        result: str = "\n\n".join(
            (
                result,
                response,
            )
        )
        doc: Doc = nlp(result)
        sentence_count: int = len(tuple(doc.sents))
        print(f"---\nCurrent sentence count: {sentence_count}\n---")

    return result


# %%
cwd: Path = Path.cwd()
output_dir_path = Path(cwd, OUTPUT_DIRECTORY)
output_dir_path.mkdir(parents=True, exist_ok=True)

for i in range(OUTPUT_FILE_COUNT):
    result: str = generate_article(target_sentence_count=TARGET_SENTENCE_COUNT)

    current_time: str = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    filename: str = f"article_{current_time}.txt"
    filepath: Path = output_dir_path.joinpath(filename)
    with open(file=filepath, mode="w") as f:
        f.write(result)
