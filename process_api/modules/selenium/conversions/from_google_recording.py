import copy

class GoogleRecording:
    def __init__(self, recording_json):
        self.recording_json = recording_json
        self.steps = []

        for step in recording_json["steps"]:
            key = step["type"]
            if key in selenium_lookup_table:
                selenium_step = selenium_lookup_table[key]
                if selenium_step is not None:
                    copy_step = copy.deepcopy(selenium_step)
                    self.steps.append(inflate_step(copy_step, step))

    def clean_recording(self, recording_json):
        pass

    def to_json(self):
        next_step_name = "step_1"

        result = {
            "id": self.recording_json["title"],
            "main": {
                "steps": {}
            }
        }

        step = result["main"]["steps"]["start"] = self.steps[0]

        for i in range(1, len(self.steps)):
            step["next_step"] = next_step_name
            step = result["main"]["steps"][next_step_name] = copy.deepcopy(self.steps[i])
            next_step_name = f"step_{i + 1}"

        return result


selenium_lookup_table = {
    "navigate": {
        "type": "perform",
        "action": "navigate",
        "args": {
            "url": "${url}"
        }
    },
    "click": {
        "type": "perform",
        "action": "click",
        "args": {
            "query": "${selectors}"
        }
    },
    "doubleClick": {
        "type": "perform",
        "action": "dbl_click",
        "args": {
            "query": "${selectors}"
        }
    },
    "clickSequence": {
        "type": "perform",
        "action": "click_sequence",
        "args": {
            "sequence": "${sequence}"
        }
    },
    "doubleClickSequence": {
        "type": "perform",
        "action": "dbl_click_sequence",
        "args": {
            "sequence": "${sequence}"
        }
    },
    "contextClick": {
        "type": "perform",
        "action": "context_click",
        "args": {
            "query": "${selectors}"
        }
    },
    "change": {
        "type": "perform",
        "action": "type_text",
        "args": {
            "query": "${selectors}",
            "value": "${value}"
        }
    },
    "keyPress": {
        "type": "perform",
        "action": "press_key",
        "args": {
            "query": "${selectors}",
            "key": "${key}"
        }
    }
}


def inflate_step(selenium_step, step):
    for arg in selenium_step["args"]:
        s_arg_value = selenium_step["args"][arg]

        if isinstance(s_arg_value, str) and s_arg_value.startswith("${"):
            property_name = s_arg_value[2:-1]
            if property_name == "selectors":
                selenium_step["args"][arg] = parse_selectors(step)
            else:
                selenium_step["args"][arg] = step[property_name]

    return selenium_step


def parse_selectors(step):
    if "selectors" not in step:
        return "body"

    return " ".join(step["selectors"][0])
