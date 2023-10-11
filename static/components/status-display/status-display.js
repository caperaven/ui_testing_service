import "./../../packages/crs-framework/components/combo-box/combo-box.js";

export default class StatusDisplay extends crs.classes.BindableElement {
    #running = false;

    get shadowDom() {
        return true;
    }

    get html() {
        return import.meta.url.replace(".js", ".html");
    }

    async preLoad() {
        this.setProperty("refreshRate", 0);
    }

    async load() {
        const template = this.shadowRoot.querySelector("template");
        await crs.binding.inflation.manager.register("statuses", template);
        this.#running = true;
        await this.getStatus();
    }

    async disconnectedCallback() {
        this.#running = false;
        await crs.binding.inflation.manager.unregister("statuses");
        await super.disconnectedCallback();
    }

    async getStatus() {
        const response = await fetch("/status");
        const statuses = statusToArray(await response.json());

        const elements = await crs.binding.inflation.manager.get("statuses", statuses, this.collection.children);
        this.collection.innerHTML = "";
        this.collection.append(...elements);

        const refreshRate = Number(this.getProperty("refreshRate"));

        if (refreshRate == 0) {
            this.#running = false;
        }

        if (this.#running) {
            const timeout = setTimeout(() => {
                clearTimeout(timeout);
                this.getStatus();
            }, refreshRate);
        }
    }

    async refresh() {
        await this.getStatus();
    }

    async clearCache() {

    }
}

function statusToArray(statusObject) {
    const result = [{
        name: "Test Name",
        status: "Status",
        error_count: "Error Count",
        date: "Date",
        time: "Time",
        duration: "Duration"
    }];

    const keys = Object.keys(statusObject);

    for (const key of keys) {
        const newStatus = statusObject[key];
        const dateParts = cleanTime(newStatus.start_time);
        newStatus.error_count ||= 0;
        newStatus.uuid = key;
        newStatus.date = dateParts.date;
        newStatus.time = dateParts.time;
        result.push(newStatus);
    }

    return result;
}

function cleanTime(time) {
    if (time == null || time.trim().length == 0) return {date: "", time: ""};

    const parts = time.split("T");
    const date = parts[0];
    const time_stamp = parts[1].split(".")[0];
    return {date, time: time_stamp}
}

customElements.define("status-display", StatusDisplay);