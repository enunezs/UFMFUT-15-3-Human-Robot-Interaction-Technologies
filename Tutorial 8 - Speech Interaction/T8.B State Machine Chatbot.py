# Restaurant Chatbot with Dialogue Branches

def chatbot_response(user_input, state):
    # Define a dictionary of responses
    responses = {
        "greeting": {
            "hi": "Hello! Welcome to our restaurant. We have a food menu and a drink menu. Which one would you like to see?",
            "menu": "We have a food menu and a drink menu. Which one would you like to see?",
            "food": "Sure! Here is our food menu: Pizza, Pasta, Salad. What would you like to know more about?",
            "drink": "Sure! Here is our drink menu: Soda, Coffee, Juice. What would you like to know more about?",
            "bye": "Goodbye! Have a great day!",
            "help": "I can show you our food or drink menu. Just ask!",
        },
        "food_menu": {
            "pizza": "We have Margherita, Pepperoni, and Veggie pizzas available.",
            "pasta": "We offer Spaghetti, Lasagna, and Penne Alfredo.",
            "salad": "We have Caesar, Garden, and Greek salads.",
            "bye": "Goodbye! Have a great day!",
            "help": "You can choose from pizza, pasta, or salad. What would you like?",
        },
        "drink_menu": {
            "soda": "We have Coke, Sprite, and Fanta.",
            "coffee": "We offer Espresso, Latte, and Cappuccino.",
            "juice": "We have Orange, Apple, and Cranberry juice.",
            "bye": "Goodbye! Have a great day!",
            "help": "You can choose from soda, coffee, or juice. What would you like?",
        },
    }

    # Normalize the input
    normalized_input = user_input.lower().strip()

    # Get the appropriate response based on the state
    state_responses = responses.get(state, {})
    response = state_responses.get(normalized_input, "I'm sorry, I don't understand that.")

    # Determine the next state based on user input and current state
    if state == "greeting" and normalized_input in ["food menu", "food"]:
        next_state = "food_menu"
    elif state == "greeting" and normalized_input in ["drink menu", "drink"]:
        next_state = "drink_menu"
    else:
        next_state = "greeting"

    return response, next_state

# Main loop to interact with the user
def chat():
    print("Welcome to the Restaurant Chatbot! Type 'bye' to exit.")
    state = "greeting"
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("Chatbot: Goodbye! Have a great day!")
            break
        response, state = chatbot_response(user_input, state)
        print(f"Chatbot: {response}")

# Run the chatbot
if __name__ == "__main__":
    chat()
