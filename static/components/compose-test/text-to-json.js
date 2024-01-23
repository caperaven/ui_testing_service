import { tokenize } from "./tokenize.js";

export function textToJson(textCollection) {
    const breakdown = [];

    let processName = "";

    for (let i = 0; i < textCollection.length; i++) {
        const line = textCollection[i];
        if (line.length == 0) continue;

        const parts = line.indexOf(" ") != -1 ? tokenize(line) : [line];

        // check for process id value
        if (parts.length === 1 && line.indexOf("#") === 0) {
            processName = line;
            continue;
        }

        let name = "";

        // remove blank spaces at the front to prevent errors
        while (parts[0].length === 0) {
            parts.shift();
        }

        if (parts[0].indexOf("#") === 0) {
            name = parts[0].replace("#", "");
            parts.shift();
        }

        const key = parts[0];

        const struct = {
            key, parts, name
        }

        breakdown.push(struct);
    }

    setNextStep(breakdown);

    const result = breakdownToJson(breakdown, processName);
    return JSON.stringify(result, null, 4);
}

function setNextStep(breakdown) {
    for (let i = 0; i < breakdown.length; i++) {
        if (breakdown[i].key == "process") continue;

        const nextItem = breakdown[i + 1];
        if (nextItem != null) {
            breakdown[i].nextStep = nextItem.name;
        }
    }
}

function breakdownToJson(breakdown, processName) {
    const result = {
        id: processName
    };
    let currentObj = result;

    const state = {
        name: "",
        nextName: ""
    }

    for (let i = 0; i < breakdown.length; i++) {
        if (breakdown[i].key == "process") {
            currentObj = result;
        }

        currentObj = Actions.parseParts(breakdown[i], currentObj, state);
    }

    return result;
}

class Actions {
    static parseParts(obj, result, state) {
        if (obj.key === "process") {
            state.count = 0;
        }

        state.nextName = obj.nextStep || `step_${state.count++}`;

        const struct = {};
        const resultObj = this[obj.key]?.(struct, obj, result, state);

        if (obj.nextStep != null) {
            struct["next_step"] = state.nextName;
        }

        state.name = state.nextName;

        return resultObj || result;
    }

    static process(struct, obj, result, state) {
        const steps = struct["steps"] = {};
        result[obj.parts[1]] = struct;
        state.nextName = "start";
        return steps;
    }

    static sequence(struct, obj, result, state) {
        result.sequences ||= [];

        result.sequences.push({
            "caption": obj.parts[2] || "",
            "process": obj.parts[1] || ""
        })

        return result;
    }

    /*-------------- Perform Functions --------------*/
    //ToDo : change to perform_navigate and check initial start up is correct

    static navigate(struct, obj, result, state) {
        struct.type = "perform";
        struct.action = "navigate";
        struct.args = {
            url: obj.parts[1]
        }

        result[state.name] = struct;
        return result;
    }

    static perform_click(struct, obj, result, state) {
        obj.parts.shift();

        struct.type = "perform";
        struct.action = obj.parts.length == 1 ? "click" : "click_sequence";
        struct.args = {}

        let property = "query";
        let value = obj.parts[0];

        if (obj.parts.length > 1) {
            property = "sequence";
            value = [...obj.parts];
        }

        struct.args[property] = value;

        result[state.name] = struct;
        return result;
    }

    static perform_close_window(struct, obj, result, state) {
        struct.type = "perform";
        struct.action = "close_window";
        struct.args = { index: obj.parts[1] };
        result[state.name] = struct;
        return result;
    }

    static perform_refresh(struct, obj, result, state) {
        struct.type = "perform";
        struct.action = "refresh";
        result[state.name] = struct;
        return result;
    }

    static perform_type_text(struct, obj, result, state) {
        struct.type = "perform";
        struct.action = "type_text";
        struct.args = {
            query: obj.parts[1],
            value: obj.parts[3]
        };
        result[state.name] = struct;
        return result;
    }

    static perform_dbl_click(struct, obj, result, state) {
        obj.parts.shift();

        struct.type = "perform";
        struct.action = "dbl_click";
        struct.args = {}

        let property = "query";
        let value = obj.parts[0];


        struct.args[property] = value;

        result[state.name] = struct;
        return result;
    }

    static perform_context_click(struct, obj, result, state) {
        obj.parts.shift();

        struct.type = "perform";
        struct.action = "context_click";
        struct.args = {}

        let property = "query";
        let value = obj.parts[0];


        struct.args[property] = value;

        result[state.name] = struct;
        return result;
    }

    static perform_press_key(struct, obj, result, state) {
        // obj.parts.shift();
        struct.type = "perform";
        struct.action = "press_key";
        struct.args = {
            query: obj.parts[1],
            key: obj.parts[2]
        }

        result[state.name] = struct;
        return result;
    }

    static perform_print_screen(struct, obj, result, state) {
        // ask about when obj.parts.shift should be used and when not
        obj.parts.shift();

        struct.type = "perform";
        struct.action = "print_screen";
        struct.args = {}

        let property = "file";
        let value = obj.parts[0];


        struct.args[property] = value;

        result[state.name] = struct;
        return result;
    }

    static perform_select_option(struct, obj, result, state) {
        struct.type = "perform";
        struct.action = "select_option";
        struct.args = {
            query: obj.parts[1],
            value: obj.parts[2]
        }

        result[state.name] = struct;
        return result;
    }

    static perform_switch_to_frame(struct, obj, result, state) {
        struct.type = "perform";
        struct.action = "switch_to_frame";
        struct.args = {}

        let property = "query";
        let value = obj.parts[1];


        struct.args[property] = value;

        result[state.name] = struct;
        return result;
    }

    static perform_switch_to_default(struct, obj, result, state) {
        //find out how this functions
        struct.type = "perform";
        struct.action = "switch_to_tab";
        struct.args = {
        }

        result[state.name] = struct;
        return result;
    }

    static perform_switch_to_tab(struct, obj, result, state) {
        struct.type = "perform";
        struct.action = "switch_to_tab";
        struct.args = {
            index : Number(obj.parts[1])
        }

        // let property = "index";
        // let value = Number(obj.parts[2]);


        // struct.args[property] = value;

        result[state.name] = struct;
        return result;
    }

    // ask what data type pixels should be
    static perform_drag_by(struct, obj, result, state) {
        struct.type = "perform";
        struct.action = "drag_by";
        struct.args = {
            query: obj.parts[1],
            x: `${obj.parts[2]}px`,
            y: `${obj.parts[3]}px`
        }

        result[state.name] = struct;
        return result;
    }

    static perform_hover_over_element(struct, obj, result, state) {
        obj.parts.shift();

        struct.type = "perform";
        struct.action = "hover_over_element";
        struct.args = {}

        let property = "query";
        let value = obj.parts[0];


        struct.args[property] = value;

        result[state.name] = struct;
        return result;
    }
    //typo in documentation?
    // not yet completed
    static perform_mouse_drag(struct, obj, result, state) {
        struct.type = "perform";
        struct.action = "mouse_drag";
        struct.args = {
            start_at: {
                x: value,
                y: value
            },
            move_too:{}
        };

        obj.parts.shift();
        for (const part of obj.parts) {
            const attrParts = part.split("=");

            if (attrParts.length < 2) continue;

            const attr = attrParts[0];
            const value = attrParts[1].split('"').join("");
            struct.args.start_at[attr] = value;
        }

        obj.parts.shift();
        for (const part of obj.parts) {
            const attrParts = part.split("=");

            if (attrParts.length < 2) continue;

            const attr = attrParts[0];
            const value = attrParts[1].split('"').join("");
            struct.args.move_too[attr] = value;
        }

        result[state.name] = struct;
        return result;
    }

    /*-------------- Assert Functions --------------*/

    static assert_attributes(struct, obj, result, state) {
        struct.type = "assert";
        struct.action = "attributes";
        struct.args = {
            query: obj.parts[1],
            attributes: {}
        };

        obj.parts.shift();
        obj.parts.shift();

        for (const part of obj.parts) {
            const attrParts = part.split("=");

            if (attrParts.length < 2) continue;

            const attr = attrParts[0];
            const value = attrParts[1].split('"').join("");
            struct.args.attributes[attr] = value;
        }

        result[state.name] = struct;
        return result;
    }

    static assert_attribute_eq(struct, obj, result, state) {
        struct.type = "assert";
        struct.action = "attribute_eq";
        struct.args = {
            query: obj.parts[1],
            attr: obj.parts[2],
            value: obj.parts[3]
        }

        result[state.name] = struct;
        return result;
    }

    static assert_attribute_neq(struct, obj, result, state) {
        struct.type = "assert";
        struct.action = "attribute_neq";
        struct.args = {
            query: obj.parts[1],
            attr: obj.parts[2],
            value: obj.parts[3]
        }

        result[state.name] = struct;
        return result;
    }


    static assert_child_count_eq(struct, obj, result, state){
        struct.type = "assert";
        struct.action = "child_count_eq";
        struct.args = {
            query: obj.parts[1],
            count: Number(obj.parts[2])
        }

        result[state.name] = struct;
        return result;
    }

    static assert_child_count_neq(struct, obj, result, state){
        struct.type = "assert";
        struct.action = "child_count_neq";
        struct.args = {
            query: obj.parts[1],
            count: Number(obj.parts[2])
        }

        result[state.name] = struct;
        return result;
    }

    static assert_style_property_eq(struct, obj, result, state){
        struct.type = "assert";
        struct.action = "style_property_eq";
        // struct.args = {
        //     query: obj.parts[1],
        //     property: obj.parts[2],
        //     value: obj.parts[3]
        // }
        struct.args = {}

        // let query = "query";
        // let value = obj.parts[0];


        struct.args.query = obj.parts[1];
        struct.args.property = obj.parts[2];
        struct.args.value = obj.parts[3];

        result[state.name] = struct;
        return result;
    }

    static assert_style_property_neq(struct, obj, result, state){
        struct.type = "assert";
        struct.action = "style_property_neq";
        struct.args = {
            query: obj.parts[1],
            property: obj.parts[2],
            value: obj.parts[3]
        }

        result[state.name] = struct;
        return result;
    }

    static assert_element_property_eq(struct, obj, result, state){
        struct.type = "assert";
        struct.action = "element_property_eq";
        struct.args = {
            query: obj.parts[1],
            property: obj.parts[2],
            value: obj.parts[3]
        }

        result[state.name] = struct;
        return result;
    }

    static assert_element_property_neq(struct, obj, result, state){
        struct.type = "assert";
        struct.action = "element_property_neq";
        struct.args = {
            query: obj.parts[1],
            property: obj.parts[2],
            value: obj.parts[3]
        }

        result[state.name] = struct;
        return result;
    }

    static assert_tag_name_eq(struct, obj, result, state){
        struct.type = "assert";
        struct.action = "tag_name_eq";
        struct.args = {
            query: obj.parts[1],
            value: obj.parts[2]
        }

        result[state.name] = struct;
        return result;
    }

    static assert_tag_name_neq(struct, obj, result, state){
        struct.type = "assert";
        struct.action = "tag_name_neq";
        struct.args = {
            query: obj.parts[1],
            value: obj.parts[2]
        }

        result[state.name] = struct;
        return result;
    }

    static assert_text_content_eq (struct, obj, result, state){
        struct.type = "assert";
        struct.action = "text_content_eq";
        struct.args = {
            query: obj.parts[1],
            value: obj.parts[2]
        }

        result[state.name] = struct;
        return result;
    }

    static assert_text_content_neq (struct, obj, result, state){
        struct.type = "assert";
        struct.action = "text_content_neq";
        struct.args = {
            query: obj.parts[1],
            value: obj.parts[2]
        }

        result[state.name] = struct;
        return result;
    }

    static assert_value_eq (struct, obj, result, state){
        struct.type = "assert";
        struct.action = "value_eq";
        struct.args = {
            query: obj.parts[1],
            value: obj.parts[2]
        }

        result[state.name] = struct;
        return result;
    }

    static assert_value_neq (struct, obj, result, state){
        struct.type = "assert";
        struct.action = "value_neq";
        struct.args = {
            query: obj.parts[1],
            value: obj.parts[2]
        }

        result[state.name] = struct;
        return result;
    }

    static assert_element_exists (struct, obj, result, state){
        struct.type = "assert";
        struct.action = "element_exists";
        struct.args = {
            query: obj.parts[1],
        }

        result[state.name] = struct;
        return result;
    }

    static assert_element_not_exists (struct, obj, result, state){
        struct.type = "assert";
        struct.action = "element_not_exists ";
        struct.args = {
            query: obj.parts[1],
        }

        result[state.name] = struct;
        return result;
    }

    //toDo
    // add to JSON to Text
    // add to test
    static assert_variables_eq(struct, obj, result, state){
        struct.type = "assert";
        struct.action = "variables_eq";
        struct.args = {
            query: obj.parts[1],
            variables: {}
        };

        obj.parts.shift();
        obj.parts.shift();

        for (const part of obj.parts) {
            const varParts = part.split("=");

            if (varParts.length < 2) continue;

            const variable = varParts[0];
            const value = varParts[1].split('"').join("");
            struct.args.variables[variable] = value;
        }

        result[state.name] = struct;
        return result;
    }

    //toDo
    // add to JSON to Text
    // add to test

    static assert_variables_neq(struct, obj, result, state){
        struct.type = "assert";
        struct.action = "variables_neq";
        struct.args = {
            query: obj.parts[1],
            variables: {}
        };

        obj.parts.shift();
        obj.parts.shift();

        for (const part of obj.parts) {
            const varParts = part.split("=");

            if (varParts.length < 2) continue;

            const variable = varParts[0];
            const value = varParts[1].split('"').join("");
            struct.args.variables[variable] = value;
        }

        result[state.name] = struct;
        return result;
    }

    //toDo
    // add to JSON to Text
    // add to test

    static assert_has_class(struct, obj, result, state){
        struct.type = "assert";
        struct.action = "has_class";
        struct.args = {
            query: obj.parts[1],
            class: obj.parts[2]
        }

        result[state.name] = struct;
        return result;
    }

    //toDo
    // add to JSON to Text
    // add to test

    static assert_has_not_class(struct, obj, result, state){
        struct.type = "assert";
        struct.action = "has_not_class";
        struct.args = {
            query: obj.parts[1],
            class: obj.parts[2]
        }

        result[state.name] = struct;
        return result;
    }

    //toDo
    // add to JSON to Text
    // add to test

    static assert_has_attribute (struct, obj, result, state){
        struct.type = "assert";
        struct.action = "has_attribute";
        struct.args = {
            query: obj.parts[1],
            attr: obj.parts[2]
        }

        result[state.name] = struct;
        return result;
    }

    //toDo
    // add to JSON to Text
    // add to test

    static assert_has_not_attribute (struct, obj, result, state){
        struct.type = "assert";
        struct.action = "has_not_attribute";
        struct.args = {
            query: obj.parts[1],
            attr: obj.parts[2]
        }

        result[state.name] = struct;
        return result;
    }


    /*-------------- System Functions --------------*/

    static system_sleep(struct, obj, result, state) {
        struct.type = "system";
        struct.action = "sleep";
        struct.args = {
            duration: Number(obj.parts[1])
        };

        result[state.name] = struct;
        return result;
    }

    //not yet completed
    static perform_set_uuid_variables(struct, obj, result, state) {
        // obj.parts.shift();

        struct.type = "perform";
        struct.action = "set_uuid_variables"
        struct.args = {
            variables : []
        }

        obj.parts.shift();

        struct.args.variables.push(obj.parts[0])

        if (obj.parts.length > 1) {
            struct.args.variables.pop()
            struct.args.variables.push(...obj.parts);
        }

        result[state.name] = struct;
        return result;
    }

    static system_attributes_to_variables(struct, obj, result, state){
        // - create variables from element attribute values for future use
        struct.type = "system";
        struct.action = "attributes_to_variables";
        struct.args = {
            step: state.name
        };

        let query = obj.parts[1];
        struct.args[query] = {}

        obj.parts.shift();
        obj.parts.shift();

        for (const part of obj.parts) {
            const attrParts = part.split("=");

            if (attrParts.length < 2) continue;

            const attr = attrParts[0];
            const value = attrParts[1].split('"').join("");
            struct.args[query][attr] = value;
        }

        result[state.name] = struct;
        return result;
    }

    static perform_properties_to_variables(struct, obj, result, state){
        // - create variables from element properties for future use
        struct.type = "perform";
        struct.action = "properties_to_variables";
        struct.args = {
            step: state.name
        };

        let query = obj.parts[1];
        struct.args[query] = {}

        obj.parts.shift();
        obj.parts.shift();

        for (const part of obj.parts) {
            const propParts = part.split("=");

            if (propParts.length < 2) continue;

            const prop = propParts[0];
            const value = propParts[1].split('"').join("");
            struct.args[query][prop] = value;
        }

        result[state.name] = struct;
        return result;
    }

    static system_dimensions_to_variables(struct, obj, result, state){
        struct.type = "system";
        struct.action = "dimensions_to_variables";
        struct.args = {
            step: state.name,
            query: obj.parts[1],
            variable: obj.parts[2]
        };

        result[state.name] = struct;
        return result;
    }

    //toDo
    // add to JSON to Text
    // add to test

    static system_audit(struct, obj, result, state) {
        // - audit an element to see if it has all the required aria
        struct.type = "system";
        struct.action = "audit";
        struct.args = {
            "query": obj.parts[2]
        };

        result[state.name] = struct;
        return result;
    }

    //ToDo : Process System action ?
    //toDo
    // add to JSON to Text
    // add to test

    static system_process(struct, obj, result, state){
        struct.type = "system";
        struct.action = "process";
        struct.args = {
            "query": obj.parts[2]
        };

        result[state.name] = struct;
        return result;
    }

    //ToDo : Process System action ?
    //toDo
    // add to JSON to Text
    // add to test

    static system_process(struct, obj, result, state){
        struct.type = "system";
        struct.action = "process";
        struct.args = {};

        result[state.name] = struct;
        return result;
    }

    //ToDo : template System action,
    // HAve to kae more dynamic
    // test

    static system_template (struct, obj, result, state){
        struct.type = "system";
        struct.action = "template";
        struct.args = {
            step: state.name,
        };

        let schema_name = obj.parts[1];
        struct.args.schema = schema_name;
        let process_name = obj.parts[2];
        struct.args.process = process_name;

        struct.args.parameters = {}

        for (const part of obj.parts) {
            const paramParts = part.split("=");

            if (paramParts.length < 2) continue;

            const parameter = paramParts[0];
            const value = paramParts[1].split('"').join("");
            struct.args.parameters[parameter] = value;
        }



        result[state.name] = struct;
        return result;
    }

    //toDo
    // add to JSON to Text
    // add to test

    static system_add_to_variables(struct, obj, result, state){
        struct.type = "system";
        struct.action = "add_to_variables";
        struct.args = {
            // query: obj.parts[1],
            variables:{}
        };

        // obj.parts.shift();
        obj.parts.shift();

        for (const part of obj.parts) {
            const varParts = part.split("=");

            if (varParts.length < 2) continue;

            const variable = varParts[0];
            const value = varParts[1].split('"').join("");
            struct.args.variables[variable] = value;
        }

        result[state.name] = struct;
        return result;
    }

    //toDo
    // add to JSON to Text
    // add to test

    static system_set_variables(struct, obj, result, state){
        struct.type = "system";
        struct.action = "set_variables";
        struct.args = {
            // query: obj.parts[1],
            variables:{}
        };

        // obj.parts.shift();
        obj.parts.shift();

        for (const part of obj.parts) {
            const varParts = part.split("=");

            if (varParts.length < 2) continue;

            const variable = varParts[0];
            const value = varParts[1].split('"').join("");
            struct.args.variables[variable] = value;
        }

        result[state.name] = struct;
        return result;
    }


    /*-------------- Wait Functions --------------*/

    static wait_time(struct, obj, result, state){
        struct.type = "wait";
        struct.action = "time";
        struct.args = {
            timeout: Number(obj.parts[1])
        };

        result[state.name] = struct;
        return result;
    }

    static wait_is_ready(struct, obj, result, state){
        struct.type = "wait";
        struct.action = "is_ready";
        struct.args = {
            query: obj.parts[1]
        };

        result[state.name] = struct;
        return result;
    }

    static wait_element(struct, obj, result, state){
        struct.type = "wait";
        struct.action = "element";
        struct.args = {
            query: obj.parts[1]
        };

        result[state.name] = struct;
        return result;
    }

    static wait_attribute(struct, obj, result, state){
        struct.type = "wait";
        struct.action = "attribute";
        struct.args = {
            query: obj.parts[1],
            attr: obj.parts[2],
            value: obj.parts[3],
        };

        result[state.name] = struct;
        return result;
    }

    static wait_attributes(struct, obj, result, state){
        struct.type = "wait";
        struct.action = "attributes";
        struct.args = {
            query: obj.parts[1],
            attributes: {}
        };


        obj.parts.shift();
        for (const part of obj.parts) {
            const attrParts = part.split("=");

            if (attrParts.length < 2) continue;

            const attr = attrParts[0];
            const value = attrParts[1].split('"').join("");
            struct.args.attributes[attr] = value;
        }

        result[state.name] = struct;
        return result;
    }

    static wait_style_property(struct, obj, result, state){
        struct.type = "wait";
        struct.action = "style_property";
        struct.args = {
            query: obj.parts[1],
            property: obj.parts[2],
            value: obj.parts[3],
        };

        result[state.name] = struct;
        return result;
    }

    // According to actions this only searches for one property and has : "query, property, value"

    static wait_element_properties (struct, obj, result, state){
        struct.type = "wait";
        struct.action = "element_properties";
        struct.args = {
            query: obj.parts[1],
            properties: {}
        };


        obj.parts.shift();
        for (const part of obj.parts) {
            const propertyParts = part.split("=");

            if (propertyParts.length < 2) continue;

            const prop = propertyParts[0];
            const value = propertyParts[1].split('"').join("");
            struct.args.properties[prop] = value;
        }

        result[state.name] = struct;
        return result;
    }


    //not sure how it works V //

    static wait_text_content(struct, obj, result, state){
        //need to type string "" if more than 1 word
        struct.type = "wait";
        struct.action = "text_content";
        struct.args = {
            query: obj.parts[1],
            value: obj.parts.slice(2).join(' ')
        };


        result[state.name] = struct;
        return result;
    }

    static wait_text_value (struct, obj, result, state){
        // What is meant by value? What if difference between above?
        struct.type = "wait";
        struct.action = "text_value";
        struct.args = {
            query: obj.parts[1],
            value: obj.parts[2]
        };


        result[state.name] = struct;
        return result;
    }


    //not sure how it works V //
    // documentation requires "value" property
    static wait_selected (struct, obj, result, state){
        struct.type = "wait";
        struct.action = "selected";
        struct.args = {
            query: obj.parts[1],
        };


        result[state.name] = struct;
        return result;
    }


    //======= How exactly does counts work ? ==========//

    static wait_child_count(struct, obj, result, state){
        struct.type = "wait";
        struct.action = "child_count";
        struct.args = {
            query: obj.parts[1],
            count: Number(obj.parts[2])
        };


        result[state.name] = struct;
        return result;
    }

    static wait_element_count (struct, obj, result, state){
        struct.type = "wait";
        struct.action = "element_count";
        struct.args = {
            query: obj.parts[1],
            count: Number(obj.parts[2])
        };


        result[state.name] = struct;
        return result;
    }

    static wait_window_count (struct, obj, result, state){
        struct.type = "wait";
        struct.action = "window_count";
        struct.args = {
            query: obj.parts[1],
            count: Number(obj.parts[2])
        };


        result[state.name] = struct;
        return result;
    }

    static wait_idle (struct, obj, result, state){
        struct.type = "wait";
        struct.action = "idle";

        result[state.name] = struct;
        return result;
    }


    // documentation requires 'attr' field that is required

    static wait_has_attribute (struct, obj, result, state){
        struct.type = "wait";
        struct.action = "has_attribute";
        struct.args = {
            query: obj.parts[1],
            attr: obj.parts[2]
        };


        result[state.name] = struct;
        return result;
    }

    static wait_has_not_attribute (struct, obj, result, state){
        struct.type = "wait";
        struct.action = "has_not_attribute";
        struct.args = {
            query: obj.parts[1],
            attr: obj.parts[2]
        };

        result[state.name] = struct;
        return result;
    }

    //toDo
    // add to JSON to Text
    // add to test
    static wait_style_properties(struct, obj, result, state){
        struct.type = "wait";
        struct.action = "style_properties";
        struct.args = {
            query: obj.parts[1],
            styles: {}
        };


        obj.parts.shift();
        for (const part of obj.parts) {
            const styleParts = part.split("=");

            if (styleParts.length < 2) continue;

            const prop = styleParts[0];
            const value = styleParts[1].split('"').join("");
            struct.args.styles[prop] = value;
        }

        result[state.name] = struct;
        return result;
    }

    //toDo
    // add to JSON to Text
    // add to test
    static wait_element_property(struct, obj, result, state){
        struct.type = "wait";
        struct.action = "element_property";
        struct.args = {
            query: obj.parts[1],
            property: obj.parts[2],
            value: obj.parts[3],
        };

        result[state.name] = struct;
        return result;
    }

    //toDo
    // add to JSON to Text
    // add to test

    static wait_has_class(struct, obj, result, state){
        struct.type = "wait";
        struct.action = "has_class";
        struct.args = {
            query: obj.parts[1],
            class: obj.parts[2]
        };

        result[state.name] = struct;
        return result;
    }

    static wait_has_not_class(struct, obj, result, state) {
        struct.type = "wait";
        struct.action = "has_not_class";
        struct.args = {
            query: obj.parts[1],
            class: obj.parts[2]
        };

        result[state.name] = struct;
        return result;
    }
}


// To Add
// wait - style-properties
// wait - element-properties

//To Do
// Check documentation on process actions

