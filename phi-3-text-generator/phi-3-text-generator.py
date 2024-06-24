# %%
from datetime import datetime
from pathlib import Path

import spacy
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama
from spacy.language import Language
from spacy.tokens.doc import Doc

LANGUAGE_MODEL_NAME = "phi3:14b"
SPACY_PIPELINE = "en_core_web_sm"
TARGET_SENTENCE_COUNT = 100
OUTPUT_FILE_COUNT = 10
OUTPUT_DIRECTORY = "out"
OLLAMA_BASE_URL = "http://host.docker.internal:11434"

# %%
spacy.cli.download(SPACY_PIPELINE)

# %%
streaming_handler = StreamingStdOutCallbackHandler()


# %%
def generate_article(target_sentence_count: int) -> str:
    llm = Ollama(
        model=LANGUAGE_MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        callbacks=[streaming_handler],
    )
    memory = ConversationBufferMemory()
    conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

    first_prompt_template = PromptTemplate(
        template="Generate a {target_sentence_count}-sentence fictitious article.",
        input_variables=["target_sentence_count"],
    )
    continuation_prompt_template = PromptTemplate(
        template="Write a {target_sentence_count}-sentence sequel to the previous article.",
        input_variables=["target_sentence_count"],
    )

    result: str = conversation.predict(
        input=first_prompt_template.format(
            target_sentence_count=target_sentence_count,
        )
    )

    nlp: Language = spacy.load(name=SPACY_PIPELINE)
    doc: Doc = nlp(result)
    sentence_count: int = len(list(doc.sents))
    print(
        f"---\n⌛ Current sentence count: {sentence_count} / {target_sentence_count}\n---"
    )

    while sentence_count < target_sentence_count:
        response: str = conversation.predict(
            input=continuation_prompt_template.format(
                target_sentence_count=target_sentence_count,
            )
        )

        result = "\n\n".join(
            (
                result,
                response,
            )
        )
        doc = nlp(result)
        sentence_count = len(tuple(doc.sents))
        print(
            f"---\n⌛ Current sentence count: {sentence_count} / {target_sentence_count}\n---"
        )

    return result


# %%
parent_dir_path: Path = Path(__file__).parent
output_dir_path: Path = parent_dir_path.joinpath(OUTPUT_DIRECTORY)
output_dir_path.mkdir(parents=True, exist_ok=True)

for i in range(OUTPUT_FILE_COUNT):
    print("---\n📝 Generating new article... Please wait for a while.\n---")
    result: str = generate_article(target_sentence_count=TARGET_SENTENCE_COUNT)

    current_time: str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename: str = f"article_{current_time}.txt"
    filepath: Path = output_dir_path.joinpath(filename)
    with open(file=filepath, mode="w", encoding="UTF8") as f:
        f.write(result)
    print(f"---\n✨ Generated article saved to:\n{filepath.resolve()}\n---")
