#  call RingleyChat.py as a module
from RingleyChat import RingleyChat

def main():
    ringley_chat = RingleyChat(update_data=False)
    while True:
        question = input("Your Question: ")
        if question == "!!exit":
            break
        result = ringley_chat.chat(question)
        print("Answer: " + result['answer'])

if __name__ == "__main__":
    main()