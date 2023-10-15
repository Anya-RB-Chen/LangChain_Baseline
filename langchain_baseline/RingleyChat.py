from util.query import chain_options
from rich.console import Console
from rich.prompt import Prompt

import argparse

class RingleyChat:
        
        """
            This class is used to chat with the RingleyChat interface.
            It can be used in two ways:
                1. As a module
                2. As a command line interface
            
            1. As a module:
                params: update_data (bool)
                default: update_data=False

                description: 
                    If update_data is True, the model will be updated with the latest data storing inside the directory of `data/update`.
                    If update_data is False, the model will use the existing FAISS embeddings inside `faiss`.
                    The model will be loaded from `util/query.chain_options.condense_prompt` by default.
            
            2. As a command line interface:
                params: model (str), update_data (bool)
                default: model="condense_prompt", update_data=False

                description:
                    model (str): to specify the model to be used, check `util/query.chain_options` for all available QA frameworks.
        """
    
        def __init__(self, model_name="condense_prompt", update_data=False):
            self.model_name = model_name
            self.update_data = update_data
            if self.update_data:
                self.chain = chain_options[self.model_name + "_update_data"]()
            else:
                self.chain = chain_options[self.model_name]()

        def __call__(self, input):
            question = input["question"]
            if question == "!!exit":
                return {"answer": "Bye!"}
            elif question == "!!help":
                return {"answer": "Type !!exit to exit"}
            else:
                return self.chat(question)
    
        def chat(self, question):
            # change this line if you're using RetrievalQA
            # input = query
            # output = result
            result = self.chain({"question": question})
            return result

def main(args):

    c = Console()
    if args.update_data:
        chain = chain_options["condense_prompt_update_data"]()
    else:
        chain = chain_options[args.model]()

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
        c.print("[bold red]---------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="condense_prompt")
    parser.add_argument("--update_data", action="store_true")
    args = parser.parse_args()
    print(args)
    main(args)

