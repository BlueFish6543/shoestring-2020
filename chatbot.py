import json

from flask import Flask, request

app = Flask(__name__)
error_threshold = 0.5


class State:
    # Stores the state of the program
    def __init__(self):
        self.intent = None
        self.intent_responses = []
        self.index = 0
        self.intents = {}
        self.responses_count = {}

    def reset(self):
        self.intent = None
        self.intent_responses = []
        self.index = 0

    def sort_responses(self):
        # Sort responses in descending order of occurrences
        count = self.responses_count[self.intent]
        sequence = sorted(range(len(count)),
                          key=lambda i: count[i],
                          reverse=True)
        responses = self.intents[self.intent]["responses"]
        self.intents[self.intent]["responses"] = [responses[i] for i in sequence]
        self.responses_count[self.intent] = [count[i] for i in sequence]


state = State()

with open('intents.json') as f:
    state.intents = json.load(f)['intents']

# Collate counts of which responses solved the problem
for i in range(len(state.intents)):
    state.responses_count[i] = [0] * len(state.intents[i]["responses"])


def is_yes(text):
    return text.strip().lower() in \
           ["y", "ye", "yep", "yes", "yea", "yeah"]


def is_no(text):
    return text.strip().lower() in \
           ["n", "no", "nah", "nope"]


def problem_solved():
    # Problem solved
    # Add to response tally
    state.responses_count[state.intent][state.index - 1] += 1
    state.sort_responses()
    state.reset()
    # TODO possibly
    return "<Great!>"


def could_not_solve():
    # Could not solve problem
    state.reset()
    # TODO possibly
    return "<Sorry!>"


def unknown_intent():
    # Couldn't figure out the intent
    # TODO possibly
    return "<Could not figure out intent>"


def greeting():
    # Greeting at the start
    # TODO possibly
    return "<Greeting>"


def predict_intent(input_text, current_intent):
    # TODO: Predict scores from model, e.g.
    # scores = model.predict(input_text)
    scores = []  # remove this line once we have the model working
    # Discard predictions below threshold
    results = [(index, score) for index, score in enumerate(scores)
               if score > error_threshold]

    if not results:
        # Didn't match any intents
        return "UNKNOWN"

    results.sort(key=lambda x: x[1], reverse=True)
    return results[0][0]  # top intent


def get_intent_response():
    if state.intent == "UNKNOWN":
        return unknown_intent()

    # Get intent response
    response = state.intent_responses[state.index]
    # Increment the index
    state.index += 1
    # return response
    return "<Lorem ipsum>"


@app.route('/get_output', methods=['POST'])
def get_output():
    # This function to be called from somewhere else e.g. JavaScript?
    data = request.json
    input_text = data["input_text"]
    startup = data["startup"]

    if startup:
        output = greeting()

    elif state.intent is None:
        # Figure out the intent
        intent = predict_intent(input_text, state.intent)
        # Update state intent and responses
        state.intent = intent
        if intent == "UNKNOWN":
            state.intent_responses = []
        else:
            state.intent_responses = state.intents[intent]["responses"]
        output = get_intent_response()

    elif is_yes(input_text):
        # Terminate
        output = problem_solved()

    elif is_no(input_text):
        if state.index == len(state.intent_responses):
            # Reached the end, could not solve problem
            output = could_not_solve()
        else:
            # Go to next question
            output = get_intent_response()

    else:
        output = unknown_intent()

    print(output)
    return output


if __name__ == '__main__':
    app.run()
