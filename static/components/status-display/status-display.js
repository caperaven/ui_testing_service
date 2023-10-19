import "./../../packages/crs-framework/components/combo-box/combo-box.js";
import "./../../packages/crs-framework/components/context-menu/context-menu-actions.js";
import "./../test-details/test-details-actions.js";
import {cleanTime} from "../utils/clean-time.js";

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
        this.setProperty("browser", "chrome");
    }

    async load() {
        const template = this.shadowRoot.querySelector("template");
        await crs.binding.inflation.manager.register("statuses", template);
        this.#running = true;
        await this.#getStatus();
    }

    async disconnectedCallback() {
        this.#running = false;
        await crs.binding.inflation.manager.unregister("statuses");
        await super.disconnectedCallback();
    }

    async #clearStatus(args) {
        const detail = args.detail;
        let url = "/status";

        if (detail == "completed") {
            url = "/status?status_filter=complete"
        }

        await fetch(url, { method: "DELETE" });
        await this.refresh();
    }

    async #getStatus() {
        const response = await fetch("/status");
        const statuses = statusToArray(await response.json());

        const elements = await crs.binding.inflation.manager.get("statuses", statuses, this.collection.children);
        this.collection.innerHTML = "";
        this.collection.append(...elements);
    }

    async #getStatusTimer(){
        const refreshRate = Number(this.getProperty("refreshRate"));

        // don't run
        if (refreshRate == 0) {
            return this.#running = false;
        }

        const timeout = setTimeout(async () => {
            clearTimeout(timeout);
            await this.#getStatus();

            const refreshRate = Number(this.getProperty("refreshRate"));

            if (refreshRate > 0) {
                await this.#getStatusTimer();
            }
        }, refreshRate);
    }

    async refreshRateChanged(newValue) {
        newValue = Number(newValue);

        if (newValue == 0) {
            return this.#running = false;
        }

        this.#running = true;
        await this.#getStatusTimer();
    }

    async refresh() {
        await this.#getStatus();
    }

    async clearCache(event) {
        const options = [
            { icon:"", id: "completed", title: "Clear Completed" },
            { icon:"", id: "all", title: "Clear All" }
        ];

        const target = event.composedPath()[0];
        await crs.call("context_menu", "show", {
            element: target,
            callback: this.#clearStatus.bind(this),
            options
        })
    }

    async listExecute(event) {
        const target = event.composedPath()[0];
        const id = target.dataset.id;
        const name = target.dataset.name;

        if (id == null) return;

        await crs.call("test_details", "show", { id, name });
    }

    async loadBundles() {
        const result = await fetch("/test_bundles").then(result => result.json());
        const bundles = result.map(name => {
            return {
                text: name,
                value: name
            }
        })

        this.cbBundles.items = bundles;
        this.cbBundles.value = bundles[0].value;
        this.setProperty("testBundle", bundles[0].value);
    }

    async add() {
        const bundle = this.getProperty("testBundle");
        const browser = this.getProperty("browser");

        await fetch(`/queue_bundle?bundle=${bundle}&browser=${browser}`, { method: "POST" });
        this.setProperty("refreshRate", 500);
    }
}

function statusToArray(statusObject) {
    const result = [{
        name: "Test Name",
        status: "Status",
        error_count: "Error Count",
        date: "Date",
        time: "Time",
        duration: "Duration",
        memory_diff: "Memory Diff",
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

customElements.define("status-display", StatusDisplay);