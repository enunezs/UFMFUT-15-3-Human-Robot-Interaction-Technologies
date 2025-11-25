# Simple Rule-Based Chatbot

def chatbot_response(user_input):
    # Define a dictionary of responses
    responses = {
        "hi": "Hello! Welcome to our restaurant. How can I assist you today?",
        "how are you?": "I'm just a computer program, but thanks for asking!",
        "what is your name?": "I'm a simple restaurant chatbot.",
        "bye": "Goodbye! Have a great day!",
        "help": "I can assist you with our menu or take your order. Just ask!",
        "food": "We have a variety of dishes including pizza, pasta, and salads. What would you like?",
        "drink": "We offer a selection of drinks including soda, coffee, and juice. What would you like?",
    }

    # Normalize the input
    normalized_input = user_input.lower().strip()

    # Check if the input is in the responses dictionary
    return responses.get(normalized_input, "I'm sorry, I don't understand that.")

# Main loop to interact with the user
def chat():
    print("Welcome to the Restaurant Chatbot! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("Chatbot: Goodbye! Have a great day!")
            break
        response = chatbot_response(user_input)
        print(f"Chatbot: {response}")

# Run the chatbot
if __name__ == "__main__":
    chat()
