from .search import get_answer
import sys

def chat_cli():
    print("Bem-vindo ao Chat de Busca Semântica!")
    print("Digite 'sair' ou 'exit' para encerrar.")

    while True:
        try:
            user_question = input("Faça sua pergunta: ")
        except EOFError: # Handle Ctrl+D
            print("Encerrando o chat. Até logo!")
            break
        except KeyboardInterrupt: # Handle Ctrl+C
            print("Encerrando o chat. Até logo!")
            break

        if user_question.lower() in ["sair", "exit"]:
            print("Encerrando o chat. Até logo!")
            break

        # Only proceed if the question is not empty after stripping whitespace
        if user_question.strip():
            response = get_answer(user_question)

            print(f"PERGUNTA: {user_question}")
            print(f"RESPOSTA: {response}")
        else:
            print("Por favor, digite uma pergunta.")


if __name__ == "__main__":
    chat_cli()
