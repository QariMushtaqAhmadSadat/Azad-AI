import requests

url = "http://localhost:8000/chat"

while True:
    user_input = input("Enter your message (or type 'exit' to quit): ")
    
    if user_input.lower() == "exit":
        print("Chat ended. Goodbye!")
        break

    data = {"text": user_input}
    response = requests.post(url, json=data)

    print("AI Response:", response.json()["response"])
