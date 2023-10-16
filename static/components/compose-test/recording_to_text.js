export function recordingToText(json) {
    const textCollection = [
        `#${json.title}`,
        `process main`
    ]

    for (const step of json.steps) {
        RecordingToText.perform(step, textCollection);
    }

    return textCollection.join("\n");
}

export function cleanSelector(selector) {
    // this does not have an attribute selector so return it
    if (selector.indexOf("[") != -1) {
        const startIndex = selector.indexOf("[");
        const endIndex = selector.indexOf("]", startIndex);
        const attribute = selector.substring(startIndex, endIndex);

        const parts = attribute.split("=");
        let value = parts[1];

        value = value.replaceAll("\\ ", " ");

        if (value.indexOf("\\3") != -1) {
            value = value.replaceAll("\\3", "").replaceAll(" ", "");
        }

        const newAttribute = `${parts[0]}='${value}'`;
        const newSelector = selector.replaceAll(attribute, newAttribute);

        if (newSelector.indexOf("=''")) {
            return newSelector.replaceAll("''", "'");
        }

        return newSelector;
    }

    if (selector.indexOf("\\") != -1) {

        let newSelector = selector.replaceAll("\\", "");

        if (newSelector.indexOf("\\3") !== -1) {
            newSelector = newSelector.replaceAll("\\3", "").replaceAll(" ", "");
        }

        if (newSelector.indexOf("=''")) {
            return newSelector.replaceAll("''", "'");
        }

        return newSelector;
    }
    else {
        return selector;
    }


}

/**
 * @method shortenSelector - shorten the selector by removing the unnecessary parts and give a shorter and precise selector.
 * @param selector
 */
export function shortenSelector(selector) {
    let str = selector;
    const substringsToRemove = ["html", "body", " main ", " nav ", " header "];

    for (let i = 0; i < substringsToRemove.length; i++) {
        const substring = substringsToRemove[i];
        str = str.replace(substring, "");
        str = str.replace(">", "");
    }

    let newStr = str.trim().replaceAll(">", "");
    newStr = newStr.trim().replaceAll("  ", " ");
    return newStr

}

/**
 * @method getElementQuery - returns a string that can be used to query the element
 * 1. replace "/" with " " (space)
 * 2. replace "// " with " " (space)
 * 3. replace "//3" with actual number thus "\\31 3" becomes "13".
 *
 * Only clean between [ and ] and replace all offending instances
 * @param step
 * @returns {string}
 */
function getElementQuery(step) {
    let result = "";

    if (step.selectors != null) {
        // flatten an array of arrays to a single array
        const flattened = [].concat.apply([], step.selectors);

        // filter the array to remove any items that contain a slash and thus not a valid selector
        const filtered = flattened.filter(item => item.indexOf("/") == -1);

        if (filtered.length == 1) {
            if (filtered[0].indexOf(" ") > -1) {
                result = `"${filtered[0]}"`;
            }
            else {
                result = filtered[0];
            }
        }
    }
    let shortSelector = shortenSelector(result)

    return cleanSelector(shortSelector)

}

class RecordingToText {
    static perform(step, textCollection) {
        this[step.type.toLowerCase()]?.(step, textCollection);
    }

    static navigate(step, textCollection) {
        textCollection.push(`navigate ${step.url}`);
    }

    static click(step, textCollection) {
        if(step.button === "secondary") {
            textCollection.push(`perform_context_click ${getElementQuery(step)}`);
        }
        else {
            textCollection.push(`perform_click ${getElementQuery(step)}`);
        }
    }

    static change(step, textCollection) {
        textCollection.push(`perform_type_text ${getElementQuery(step)} "${step.value}"`);
    }

    static keyup(step, textCollection) {
        textCollection.push(`perform_press_key ${getElementQuery(step)} ${step.key.toUpperCase()}`);
    }

}