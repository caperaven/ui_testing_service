import {textToJson} from "./text-to-json.js";
import {cleanTime} from "../utils/clean-time.js";
import "./../../packages/crs-framework/components/combo-box/combo-box.js";

const startText = [
    "#my_process",
    "process main",
    "navigate ${state.server}",
    ""
]

export default class ComposeTest extends crs.classes.BindableElement {

    #jobId = null;

    get shadowDom() {
        return true;
    }

    get html() {
        return import.meta.url.replace(".js", ".html");
    }

    async preLoad() {
        this.setProperty("browser", "chrome");
        await this.clearJobStatus();
    }

    load() {
        requestAnimationFrame(() => {
            this.markdownEditor.value = startText.join("\n");
        })
    }

    async #monitorJob() {
        const timeout = setTimeout(async () => {
            clearTimeout(timeout);
            const status = await fetch(`/test_status?job_id=${this.#jobId}`).then(result => result.json());

            const dateTime = cleanTime(status.start_time);
            status.date = dateTime.date;
            status.time = dateTime.time;

            this.setProperty("status", status);

            if (status.status != "complete" && status.status != "error") {
                await this.#monitorJob();
            }

        }, 100);
    }

    async runSchema() {
        const schema = this.schemaEditor.value;
        const json = JSON.parse(schema);

        const browser = this.getProperty("browser");
        const result = await fetch(`/test?browser=${browser}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(json)
        }).then(result => result.json());

        this.#jobId = result.job_id;
        await this.clearJobStatus();
        await this.#monitorJob();
    }

    async markdownEditorChange() {
        this.schemaEditor.value = textToJson(event.detail.split("\n"));
    }

    async clearJobStatus() {
        const status = {
            date: "",
            time: "",
            name: "",
            status: "",
            error_count: 0,
            duration: 0,
            memory_diff: 0
        }

        this.setProperty("status", status);
    }

    async showStatus() {
        if (this.#jobId == null) return;

        const status = this.getProperty("status");
        await crs.call("test_details", "show", { id: this.#jobId, name: status["id"] });
    }
}

customElements.define("compose-test", ComposeTest);