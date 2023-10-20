export default class TestDetails extends crs.classes.BindableElement {
    get shadowDom() {
        return true;
    }

    get html() {
        return import.meta.url.replace(".js", ".html");
    }

    async load() {
        const template = this.shadowRoot.querySelector("template");
        await crs.binding.inflation.manager.register("memory", template);

        await this.#loadLog();
        await this.#loadMemory();
        await this.#loadSchema();
    }

    async disconnectedCallback() {
        await crs.binding.inflation.manager.unregister("memory");
        await super.disconnectedCallback();
    }

    async #loadLog() {
        const log = await fetch(`/log?job_id=${this.id}`);
        const logCollection = await log.json();
        const logHtml = createLogHTML(logCollection);
        this.logContainer.innerHTML = logHtml;
    }

    async #loadMemory() {
        const log = await fetch(`/memory_data?job_id=${this.id}`);
        const logCollection = parseCollection(await log.json());
        const elements = await crs.binding.inflation.manager.get("memory", logCollection, this.memoryContainer.children);
        this.memoryContainer.innerHTML = "";
        this.memoryContainer.append(...elements);

        const blob = await fetch(`/memory_graph?job_id=${this.id}`).then(result => result.blob());
        const url = URL.createObjectURL(blob);
        this.graphContainer.src = url;
    }

    async #loadSchema() {
        requestAnimationFrame(async () => {
            this.schema = await fetch(`/test_schema?job_id=${this.id}`).then(result => result.json());
            this.schemaContainer.value = JSON.stringify(this.schema, null, 4);
        })
    }

    async runSchema() {
        await fetch("/test", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.schema)
        })

        await crs.call("test_details", "close", {})
    }
}

function createLogHTML(logCollection) {
    let html = [];

    for (const row of logCollection) {
        if (
            row.trim().length === 0 ||
            row.indexOf("(No symbol)") > -1 ||
            row.indexOf("GetHandleVerifier") > -1 ||
            row.indexOf("BaseThreadInitThunk ") > -1 ||
            row.indexOf("RtlUserThreadStart ") > -1 ||
            row.indexOf("Traceback ") > -1 ||
            row.indexOf("Stacktrace:") > -1) {
            continue;
        }

        let line = row.replace(" - process_api - ", " ");

        if (line.indexOf(" INFO ") > -1) {
            line = `<em class='green'>${line}</em>`
        }
        else if (line.indexOf(" ERROR ") > -1) {
            line = `<em class='red'>${line}</em>`
        }
        else if (line.indexOf("Exception") > -1) {
            line = `<em class='red'>${line}</em>`
        }
        else {
            line = `<em class='grey'>${line}</em>`
        }

        html.push(`${line}</br>`)
    }

    return html.join("");
}

function parseCollection(collection) {
    const result = [
        {
            date: "Date",
            time: "Time",
            name: "Step",
            value: "Memory"
        }
    ];

    for (let i = 1; i < collection.length; i++) {
        const line = collection[i];
        const parts = line.split(",");
        const date = parseDate(parts[0]);

        result.push({
            date: date.date,
            time: date.time,
            name: parts[1],
            value: parts[2]
        })
    }

    if (result.length === 1) {
        return result.push({
            date: "",
            time: "",
            name: "DIFFERENCE",
            value: 0
        });
    }

    const startMemory = result[1].value;
    const endMemory = result[result.length - 1].value;
    const memoryChange = endMemory - startMemory;

    return result.push({
        date: "",
        time: "",
        name: "DIFFERENCE",
        value: memoryChange
    });
}

function parseDate(dateStr) {
    const parts = dateStr.split(" ");
    const date = parts[0];
    const time = parts[1].split(".")[0];
    return {date, time};
}

customElements.define("test-details", TestDetails);