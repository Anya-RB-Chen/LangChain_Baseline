"""
    This file is for a test CLI interface for RingleyChat, which connects the local dataset storing in `data` directory.
    The models being used here are `OpenAIEmbeddings` and `gpt-3.5-turbo`. 
    This cli.py program is only for testing purpose, and it is not the final version of the CLI interface.

    The embeddings dataset is stored in 'embeddings' directory.
    The program will load the embeddings dataset from the 'embeddings' directory if it exists.

    Usage:
        python3 cli.py

    Model: OpenAIEmbeddings, gpt-3.5-turbo
"""

from util.config import Config
from util.query_pkl import chain_options

from rich.console import Console
from rich.prompt import Prompt

if __name__ == "__main__":
    c = Console()
    # model = Prompt.ask("Which QA model would you like to work with?",
    #                    choices=list(chain_options.keys()),
    #                    default="basic")
    chain = chain_options["condense_prompt_pkl"]()

    c.print("[bold]Chat with your docs!")
    c.print("[bold red]---------------")

    while True:
        question = Prompt.ask("Your Question: ")
        if question == "!!exit":
            break

        # change this line if you're using RetrievalQA
        # input = query
        # output = result
        result = chain({"question": question})
        c.print("[green]Answer: [/green]" + result['answer'])

        # # include a bit more if we're using `with_sources`
        # if model == "with_sources" and result.get('source_documents', None):
        #     c.print("[green]Sources: [/green]")
        #     for doc in result['source_documents']:
        #         c.print(f"[bold underline green]{doc.metadata['source']}")
        #         c.print("[green]" + doc.page_content)
        c.print("[bold red]---------------")