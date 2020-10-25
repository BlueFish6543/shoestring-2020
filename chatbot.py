import json
import os.path
import pickle

from flask import Flask, request
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf

app = Flask(__name__)
error_threshold = 0.5

best_model_path = os.path.join(os.path.dirname(__file__), '{}-best_val_loss.h5'.format("nlp_test4newmodelaugrand"))
tokenizer_path = os.path.join(os.path.dirname(__file__), "tokenizer.pickle")

with open(tokenizer_path, 'rb') as handle:
    tokenizer = pickle.load(handle)
model = tf.keras.models.load_model(best_model_path)


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

with open('intents_reduced.json') as f:
    state.intents = json.load(f)['intents']

# Collate counts of which responses solved the problem
for i in range(len(state.intents)):
    state.responses_count[i] = [0] * len(state.intents[i]["responses"])


def is_yes(text):
    return text.strip().lower() in \
           ["y", "ye", "yep", "yes", "yea", "yeah", "ok", "okay"]


def is_no(text):
    return text.strip().lower() in \
           ["n", "no", "nah", "nope"]


def problem_solved():
    # Problem solved
    # Add to response tally
    state.responses_count[state.intent][state.index - 1] += 1
    state.sort_responses()
    state.reset()
    return "Great! Glad that helped. Have a nice day!"


def could_not_solve():
    # Could not solve problem
    state.reset()
    return "Hmm, it seems like you have a complex problem there. Please contact the supplier " \
           "to continue troubleshooting your device. Sorry!"


def unknown_intent(message=""):
    # Couldn't figure out the intent
    return ("Sorry, I did not understand what you typed. Please try again. "
            + "\n" + message).strip()


def predict_intent(input_text):
    sequence = tokenizer.texts_to_sequences([input_text])
    data = pad_sequences(sequence, maxlen=100, padding="post")
    scores = model.predict(data)[0]
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
        state.reset()
        return unknown_intent()

    # Get intent response
    response = state.intent_responses[state.index]
    # Increment the index
    state.index += 1
    return response


@app.route('/reset', methods=['POST'])
def reset():
    state.reset()
    return ""


@app.route('/get_output', methods=['POST'])
def get_output():
    # This function to be called from somewhere else e.g. JavaScript?
    data = request.json
    input_text = data["input_text"]

    if state.intent is None:
        # Figure out the intent
        intent = predict_intent(input_text)
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
        output = unknown_intent(state.intent_responses[state.index - 1])

    print(output)
    return output


if __name__ == '__main__':
    app.run()
