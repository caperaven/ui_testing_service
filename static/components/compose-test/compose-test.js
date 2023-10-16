import {textToJson} from "./text-to-json.js";

const startText = [
    "#my_process",
    "process main",
    "navigate ${state.server}",
    ""
]

export default class ComposeTest extends crs.classes.BindableElement {

    get shadowDom() {
        return true;
    }

    get html() {
        return import.meta.url.replace(".js", ".html");
    }

    get load() {
        requestAnimationFrame(() => {
            this.markdownEditor.value = startText.join("\n");
        })
    }

    async runSchema() {
        const schema = this.schemaEditor.value;
        const json = JSON.parse(schema);

        await fetch("/test", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(json)
        })
    }

    async markdownEditorChange() {
        this.schemaEditor.value = textToJson(event.detail.split("\n"));
    }
}

customElements.define("compose-test", ComposeTest);