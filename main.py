from server import request_server
import requests

while True:

    def user_input_main():
        user_input = input("\nEnter: ")
        print("1. Word Segmenter & Auto-Corrector\n2. Word Predictor")
        task_no = int(input("Enter task number: "))

        try:
            if task_no == 1:
                response = request_server(model="gemma2:2b", stream=False, task="segncorrect", data=user_input)
                for i,j in enumerate(response["words"]):
                    if i == 0 and j == "words":
                        continue
                    else:
                        print(j,end=' ')

            elif task_no == 2:
                n = input("Enter n: ")
                response = request_server(model="gemma2:2b", stream=False, task="predict", data=user_input, n=n)
                for i in response['words']:
                    print(i,end=' ')

            else:
                print("Invalid task number")
                return

        except KeyboardInterrupt:
            exit()
        except requests.exceptions.ConnectionError:
            user_input_main()
    user_input_main()

    print("\n")