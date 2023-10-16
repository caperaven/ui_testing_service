export function processToText(json) {
    const textCollection = [
        `#${json.id}`
    ]

    processProcesses(json, textCollection);
    return textCollection.join("\n");
}

export function processProcesses(json, textCollection) {
    const processNames = Object.keys(json);

    for (const processName of processNames) {
        if (processName == "id") continue;

        if (processName == "sequences") {
            for (const sequence of json["sequences"]) {
                textCollection.push(`sequence ${sequence.process} "${sequence.caption}"`);
            }

            continue;
        }

        textCollection.push("");
        textCollection.push(`process ${processName}`);
        const processObj = json[processName];
        processSteps(processObj.steps, textCollection);
    }
}

export function processSteps(process, textCollection) {
    const stepNames = Object.keys(process);

    for (const stepName of stepNames) {
        const obj = process[stepName];
        ProcessToText.process(stepName, obj, textCollection);
    }
}

class ProcessToText {
    static process(name, obj, textCollection) {
        const key = `${obj.type}_${obj.action}`;
        this[key]?.(name, obj, textCollection);
    }

    //--- Perform Actions ---//

    static perform_navigate(name, obj, textCollection) {
        textCollection.push(`navigate ${obj.args.url}`);
    }

    static perform_click(name, obj, textCollection) {
        textCollection.push(`perform_click ${obj.args.query}`);
    }

    static perform_click_sequence(name, obj, textCollection) {
        textCollection.push(`perform_click ${obj.args.sequence.join(" ")}`);
    }

    static perform_type_text(name, obj, textCollection) {
        textCollection.push(`perform_type_text ${obj.args.query} "${obj.args.value}"`);
    }

    static perform_dbl_click(name, obj, textCollection) {
        textCollection.push(`perform_dbl_click ${obj.args.query}`);
    }

    static perform_context_click(name, obj, textCollection) {
        textCollection.push(`perform_context_click ${obj.args.query}`);
    }

    static perform_press_key(name, obj, textCollection) {
        textCollection.push(`perform_press_key ${obj.args.query} "${obj.args.key}"`);
    }

    static perform_print_screen(name, obj, textCollection) {
        textCollection.push(`perform_print_screen ${obj.args.file}`);
    }

    static perform_select_option(name, obj, textCollection) {
        textCollection.push(`perform_select_option ${obj.args.query} ${obj.args.value}`);
    }

    static perform_switch_to_frame(name, obj, textCollection) {
        textCollection.push(`perform_switch_to_frame ${obj.args.query}`);
    }

    //not sure how it works
    static perform_switch_to_default(name, obj, textCollection) {
        textCollection.push(`perform_switch_to_default`);
    }

    static perform_switch_to_tab(name, obj, textCollection) {
        textCollection.push(`perform_switch_to_tab ${obj.args.index}`);
    }

    static perform_drag_by(name, obj, textCollection) {
        textCollection.push(`perform_drag_by ${obj.args.query} ${obj.args.x}px ${obj.args.y}px`);
    }

    static perform_hover_over_element(name, obj, textCollection) {
        textCollection.push(`perform_hover_over_element ${obj.args.query}`);
    }

    static perform_close_window(name, obj, textCollection) {
        textCollection.push(`perform_close_window ${obj.args.index}`);
    }

    static perform_refresh(name, obj, textCollection) {
        textCollection.push(`perform_refresh`);
    }

    // to do
    // Mouse Drag Action


    //--- Assert Actions ---//

    //ToDo: attributes action with dictionary (review)

    static assert_attributes(name, obj, textCollection) {
        textCollection.push(`assert_attributes ${obj.args.query} ${Object.entries(obj.args.attributes).reduce((str, [key, value]) => str + `${key}="${value}" `, '')}`);
    }

    static assert_attribute_eq(name, obj, textCollection) {
        textCollection.push(`assert_attribute_eq ${obj.args.query} ${obj.args.attr} ${obj.args.value}`);
    }

    static assert_attribute_neq(name, obj, textCollection) {
        textCollection.push(`assert_attribute_neq ${obj.args.query} ${obj.args.attr} ${obj.args.value}`);
    }

    static assert_child_count_eq(name, obj, textCollection) {
        textCollection.push(`assert_child_count_eq ${obj.args.query} ${obj.args.count}`);
    }

    static assert_child_count_neq(name, obj, textCollection) {
        textCollection.push(`assert_child_count_neq ${obj.args.query} ${obj.args.count}`);
    }

    static assert_style_property_eq(name, obj, textCollection) {
        textCollection.push(`assert_style_property_eq ${obj.args.query} ${obj.args.property} ${obj.args.value}`);
    }

    static assert_style_property_neq(name, obj, textCollection) {
        textCollection.push(`assert_style_property_neq ${obj.args.query} ${obj.args.property} ${obj.args.value}`);
    }

    static assert_element_property_eq(name, obj, textCollection) {
        textCollection.push(`assert_element_property_eq ${obj.args.query} ${obj.args.property} ${obj.args.value}`);
    }

    static assert_element_property_neq(name, obj, textCollection) {
        textCollection.push(`assert_element_property_neq ${obj.args.query} ${obj.args.property} ${obj.args.value}`);
    }

    static assert_tag_name_eq(name, obj, textCollection) {
        textCollection.push(`assert_tag_name_eq  ${obj.args.query} ${obj.args.value}`);
    }

    static assert_tag_name_neq(name, obj, textCollection) {
        textCollection.push(`assert_tag_name_neq  ${obj.args.query} ${obj.args.value}`);
    }

    static assert_text_content_eq(name, obj, textCollection) {
        textCollection.push(`assert_text_content_eq  ${obj.args.query} ${obj.args.value}`);
    }

    static assert_text_content_neq(name, obj, textCollection) {
        textCollection.push(`assert_text_content_neq  ${obj.args.query} ${obj.args.value}`);
    }

    static assert_value_eq(name, obj, textCollection) {
        textCollection.push(`assert_value_eq  ${obj.args.query} ${obj.args.value}`);
    }

    static assert_value_neq(name, obj, textCollection) {
        textCollection.push(`assert_value_neq  ${obj.args.query} ${obj.args.value}`);
    }

    static assert_element_exists(name, obj, textCollection) {
        textCollection.push(`assert_element_exists ${obj.args.query}`);
    }

    static assert_element_not_exists(name, obj, textCollection) {
        textCollection.push(`assert_element_not_exists ${obj.args.query}`);
    }

    //ToDo

    static assert_variables_eq(name, obj, textCollection) {
        textCollection.push(`assert_element_not_exists ${obj.args.query} ${Object.entries(obj.args.variables).reduce((str, [key, value]) => str + `${key}="${value}" `, '')}`);
    }

    static assert_variables_neq(name, obj, textCollection) {
        textCollection.push(`assert_element_not_exists ${obj.args.query} ${Object.entries(obj.args.variables).reduce((str, [key, value]) => str + `${key}="${value}" `, '')}`);
    }

    static assert_has_class(name, obj, textCollection) {
        textCollection.push(`assert_element_not_exists ${obj.args.query} ${obj.args.class}`);
    }

    static assert_has_not_class(name, obj, textCollection) {
        textCollection.push(`assert_element_not_exists ${obj.args.query} ${obj.args.class}`);
    }


    //--- Wait Actions ---//


    static wait_time(name, obj, textCollection) {
        textCollection.push(`wait_time  ${obj.args.query} ${obj.args.timeout}`);
    }

    static wait_is_ready(name, obj, textCollection) {
        textCollection.push(`wait_is_ready  ${obj.args.query}`);
    }

    static wait_element(name, obj, textCollection) {
        textCollection.push(`wait_element  ${obj.args.query}`);
    }

    static wait_attribute(name, obj, textCollection) {
        textCollection.push(`wait_attribute ${obj.args.query} ${obj.args.attr} ${obj.args.value}`);
    }

    //todo : static function for multiple attributes
    static wait_attributes(name, obj, textCollection) {
        textCollection.push(`wait_attributes ${obj.args.query} ${Object.entries(obj.args.attributes).reduce((str, [key, value]) => str + `${key}="${value}" `, '')}`);
    }


    static wait_style_property(name, obj, textCollection) {
        textCollection.push(`wait_style_property ${obj.args.query} ${obj.args.property} ${obj.args.value}`);
    }

    //todo : static function for multiple styles (review + documentation)
    static wait_style_properties(name, obj, textCollection) {
        textCollection.push(`wait_style_properties ${obj.args.query} ${Object.entries(obj.args.styles).reduce((str, [key, value]) => str + `${key}="${value}" `, '')}`);
    }

    static wait_element_property(name, obj, textCollection) {
        textCollection.push(`wait_element_property ${obj.args.query} ${obj.args.property} ${obj.args.value}`);
    }

    //todo : static function for multiple elements (review + documentation)
    static wait_element_properties(name, obj, textCollection) {
        textCollection.push(`wait_element_properties ${obj.args.query} ${Object.entries(obj.args.properties).reduce((str, [key, value]) => str + `${key}="${value}" `, '')}`);
    }


    static wait_text_content(name, obj, textCollection) {
        textCollection.push(`wait_text_content ${obj.args.query} ${obj.args.value}`);
    }

    static wait_text_value(name, obj, textCollection) {
        textCollection.push(`wait_text_value ${obj.args.query} ${obj.args.value}`);
    }

    static wait_selected(name, obj, textCollection) {
        textCollection.push(`wait_selected  ${obj.args.query} ${obj.args.value}`);
    }

    static wait_child_count(name, obj, textCollection) {
        textCollection.push(`wait_child_count  ${obj.args.query} ${obj.args.count}`);
    }

    static wait_element_count(name, obj, textCollection) {
        textCollection.push(`wait_element_count ${obj.args.query} ${obj.args.count}`);
    }

    static wait_window_count(name, obj, textCollection) {
        textCollection.push(`wait_window_count ${obj.args.query} ${obj.args.count}`);
    }

    static wait_idle(name, obj, textCollection) {
        textCollection.push(`wait_idle ${obj.args.query} ${obj.args.count}`);
    }

    static wait_has_attribute(name, obj, textCollection) {
        textCollection.push(`wait_has_attribute ${obj.args.query} ${obj.args.attr}`);
    }

    static wait_has_not_attribute(name, obj, textCollection) {
        textCollection.push(`wait_has_not_attribute ${obj.args.query} ${obj.args.attr}`);
    }

    //ToDo

    static wait_has_class(name, obj, textCollection) {
        textCollection.push(`wait_has_class ${obj.args.query} ${obj.args.class}`);
    }

    static wait_has_not_class(name, obj, textCollection) {
        textCollection.push(`wait_has_not_class ${obj.args.query} ${obj.args.class}`);
    }

    //--- System Actions ---//

    static system_sleep(name, obj, textCollection) {
        textCollection.push(`system_sleep ${obj.args.duration}`);
    }

    static system_set_uuid_variables(name, obj, textCollection) {
        textCollection.push(`system_set_uuid_variables ${obj.args.variables.join(" ")}`);
    }

    static system_attributes_to_variables(name, obj, textCollection) {
        let attributesString = '';
        for (const [query, attributes] of Object.entries(obj.args)) {
            attributesString += ` ${query}`;
            for (const [attr, value] of Object.entries(attributes)) {
                attributesString += ` ${attr}="${value}"`;
            }
        }
        textCollection.push(`system_attributes_to_variables${attributesString}`);
    }

    static system_properties_to_variables(name, obj, textCollection) {
        let attributesString = '';
        for (const [query, properties] of Object.entries(obj.args)) {
            attributesString += ` ${query}`;
            for (const [attr, value] of Object.entries(properties)) {
                attributesString += ` ${attr}="${value}"`;
            }
        }
        textCollection.push(`system_properties_to_variables${attributesString}`);
    }

    static system_dimensions_to_variables(name, obj, textCollection) {
        textCollection.push(`system_dimensions_to_variables ${obj.args.query} ${obj.args.variable}`);
    }

    static system_audit(name, obj, textCollection) {
        textCollection.push(`system_audit ${obj.args.query}`);
    }

    //ToDo = System Process

    static system_process(name, obj, textCollection) {
        textCollection.push(`system_process ${obj.args.query}`);
    }

    static system_set_variables(name, obj, textCollection) {
        textCollection.push(`system_set_variables ${Object.entries(obj.args.variables).reduce((str, [key, value]) => str + `${key}="${value}" `, '')}`)
    }

    static system_add_to_variables(name, obj, textCollection) {
        textCollection.push(`system_add_to_variables ${Object.entries(obj.args.variables).reduce((str, [key, value]) => str + `${key}="${value}" `, '')}`)
    }

    static system_template(name, obj, textCollection) {
        let str = `system_template `
        for (const [key, value] of Object.entries(obj.args.parameters)) {
            str += `${key}="${value}" `
        }
        textCollection.push(str)
        return textCollection;
    }
}