import {textToJson} from "./text-to-json.js";
import {cleanTime} from "../utils/clean-time.js";
import {processToText} from "./process-to-text.js";
import "./../../components/reference-component/reference-component.js";
import "./../../packages/crs-framework/components/combo-box/combo-box.js";
import "./../../packages/crs-framework/components/dialogs/dialogs-actions.js";

const startText = [
    "#my_process",
    "process main",
    "navigate ${state.server}",
    ""
]

export default class ComposeTest extends crs.classes.BindableElement {

    #jobId = null;
    #loading = false;

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
        requestAnimationFrame(async () => {
            await this.newTest()
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

            if (status.status != "complete" && status.status != "error" && status.status != "skipped") {
                await this.#monitorJob();
            }

        }, 100);
    }

    async runSchema() {
        const schema = this.schemaEditor.value;

        let json;

        try {
            json = JSON.parse(schema);
        }
        catch (error) {
            return alert("Invalid JSON");
        }

        const server = this.getProperty("server");
        const browser = this.getProperty("browser");
        const result = await fetch(`/test?browser=${browser}&server=${server}`, {
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
        if (this.#loading === true) return;
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

    async newTest() {
        this.markdownEditor.value = startText.join("\n");
    }

    async openTest() {
        this.#loading = true;
        try {
            const [fileHandle] = await window.showOpenFilePicker();
            const file = await fileHandle.getFile();
            const contents = await file.text();

            const json = JSON.parse(contents);

            const text = processToText(json);
            this.schemaEditor.value = contents;
            this.markdownEditor.value = text;
        }
        catch (error) {
            alert(error.message)
        }
        finally {
            this.#loading = false;
        }
    }

    async saveTest() {
        await this.saveTestAs();
    }

    async saveTestAs() {
        const content = this.schemaEditor.value;
        let json;

        try {
            json = JSON.parse(content);
        }
        catch (error) {
            alert("Invalid JSON");
            return;
        }

        try {
            const fileHandle = await window.showSaveFilePicker({
                suggestedName: this.suggestedName ?? `${json.id}.json`,
                types: [{
                    description: 'Schema Files',
                    accept: {
                        'application/json': ['.json']
                    }
                }]
            });

            // Write the content to the chosen file
            const writable = await fileHandle.createWritable();
            await writable.write(content);
            await writable.close();
        }
        catch (error) {
            alert(error.message)
        }
    }

    async importRecording() {
        this.#loading = true;
        try {
            const [fileHandle] = await window.showOpenFilePicker();
            const file = await fileHandle.getFile();
            const contents = await file.text();

            const result = await fetch("/convert_recording", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: contents
            }).then(result => result.text());

            const json = JSON.parse(result);
            const text = processToText(json);
            this.schemaEditor.value = JSON.stringify(json, null, 4);
            this.markdownEditor.value = text;
        }
        catch (error) {
            alert(error.message)
        }
        finally {
            this.#loading = false;
        }
    }

    async showHelp() {
        const body = document.createElement("reference-component");
        const header = document.createElement("h2");
        header.textContent = "Test Actions";

        await crs.call("dialogs", "show", {
            id: "test-details",
            content: {
                header, body
            },
            options: {
                maximized: true,
                modal: false
            }
        })
    }

    async loadServers() {
        const servers = await fetch("/server_list").then(result => result.json());
        const cb = this.shadowRoot.querySelector("#cbServers");
        cb.items = servers;

        requestAnimationFrame(() => {
            cb.value = servers[0].value;
            this.setProperty("server", servers[0].value);
        })
    }

    async loadBefore() {
        let before = await fetch("/before_bundles").then(result => result.json());
        const cb = this.shadowRoot.querySelector("#cbBefore");

        before = before.map(item => {
            return {
                value: item,
                text: item
            }
        })

        cb.items = before;

        requestAnimationFrame(() => {
            cb.value = before[0].value;
            this.setProperty("before", before[0].value);
        })
    }
}

customElements.define("compose-test", ComposeTest);