class State:
    # Stores the state of the program
    def __init__(self):
        self.startup = True
        self.current_intent = None


state = State()
# Map of current intent to next allowable intents
# Basically the flowchart logic
intent_map = {

}
error_threshold = 0.5


def unknown_intent():
    # Couldn't figure out the intent
    return "<Could not figure out intent>"


def predict_intent(input_text, current_intent):
    next_intents = intent_map[current_intent]

    # Predict scores from model, e.g.
    # scores = model.predict(input_text)
    scores = []  # uncomment this line once we have the model working
    # Discard predictions below threshold and if intent is not
    # in the list of next allowable intents
    results = [(index, score) for index, score in enumerate(scores)
               if score > error_threshold and index in next_intents]

    if not results:
        # Didn't match any intents
        return unknown_intent()

    results.sort(key=lambda x: x[1], reverse=True)
    return results[0][0]  # top intent


def get_output(input_text=None):
    # This function to be called from somewhere else e.g. JavaScript?
    if state.startup:
        output = "<Greeting on startup>"
        state.startup = False
    else:
        intent = predict_intent(input_text, state.current_intent)
        # Obtain output from intent
        # output = obtain_output_from_intent(intent)  # function to be implemented
        output = "<Lorem ipsum>"  # uncomment this line once we have stuff working
        state.current_intent = intent

    print(output)
    return output
