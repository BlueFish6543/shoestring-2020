from flask import Flask, request

app = Flask(__name__)
error_threshold = 0.5


class State:
    # Stores the state of the program
    def __init__(self):
        self.current_intent = None  # TODO possibly


state = State()


def unknown_intent():
    # Couldn't figure out the intent
    # TODO possibly
    return "<Could not figure out intent>"


def predict_intent(input_text, current_intent):
    # TODO: Predict scores from model, e.g.
    # scores = model.predict(input_text)
    scores = []  # remove this line once we have the model working
    # Discard predictions below threshold
    results = [(index, score) for index, score in enumerate(scores)
               if score > error_threshold]

    if not results:
        # Didn't match any intents
        return None  # TODO

    results.sort(key=lambda x: x[1], reverse=True)
    return results[0][0]  # top intent


def get_intent_response(intent):
    # Get intent response
    # TODO
    return "<Lorem ipsum>"


@app.route('/get_output', methods=['POST'])
def get_output():
    # This function to be called from somewhere else e.g. JavaScript?
    data = request.json
    input_text = data["input_text"]
    startup = data["startup"]

    if startup:
        output = "<Greeting on startup>"
    else:
        intent = predict_intent(input_text, state.current_intent)
        output = get_intent_response(intent)

        # Update state
        state.current_intent = intent

    print(output)
    return output


if __name__ == '__main__':
    app.run()
