import "./../../components/reference-component/reference-component.js";
import "./../../packages/crs-framework/components/combo-box/combo-box.js";
import "./../../packages/crs-framework/components/dialogs/dialogs-actions.js";
import "./../test-details/test-details-actions.js";
import {cleanTime} from "../utils/clean-time.js";

export default class HistoryDisplay extends crs.classes.BindableElement {
    get shadowDom() {
        return true;
    }

    get html() {
        return import.meta.url.replace(".js", ".html");
    }

    async preLoad() {
        this.setProperty("summary", {
            total: 0, passed: 0, failed: 0
        })
    }

    async load() {
        const template = this.shadowRoot.querySelector("template");
        await crs.binding.inflation.manager.register("history_status", template);
    }

    async loadDates() {
        // get the dates for the combo box
        const dates = await fetch("/history").then(response => response.json());
        if (dates.length === 0) return;

        const items = [];
        for (const date of dates) {
            items.push({value: date, text: date});
        }

        const lastDate = items[dates.length - 1];
        const combobox = this.shadowRoot.querySelector("combo-box");
        combobox.items = items;
        combobox.value = lastDate.value;
        await this.currentDateChanged(lastDate.value);
    }

    async disconnectedCallback() {
        await crs.binding.inflation.manager.unregister("history_status");
        await super.disconnectedCallback();
    }

    async currentDateChanged(newValue) {
        const summary = await fetch(`/history?date=${newValue}`).then(response => response.json());
        const summary_array = statusToArray(summary);
        const elements = await crs.binding.inflation.manager.get("history_status", summary_array, this.collection.children);
        this.collection.innerHTML = "";
        this.collection.append(...elements);

        // we must remove the header row from the total
        const total = summary_array.length - 1;
        let passed = 0;
        let failed = 0;

        for (const summary of summary_array) {
            switch (summary.status) {
                case "complete": {
                    passed++;
                    break;
                }
                case "error": {
                    failed++;
                    break;
                }
            }
        }

        this.setProperty("summary", {
            total, passed, failed
        })
    }

    async listExecute(event) {
        const target = event.composedPath()[0];
        const id = target.dataset.id;
        const name = target.dataset.name;

        if (id == null) return;

        await crs.call("test_details", "show", { id, name });
    }
}

function statusToArray(summary) {
    const result = [{
        name: "Test Name",
        status: "Status",
        error_count: "Error Count",
        date: "Date",
        time: "Time",
        duration: "Duration",
        memory_diff: "Memory Diff",
    }];

    for (const status of summary) {
        const dateParts = cleanTime(status.start_time);
        status.date = dateParts.date;
        status.time = dateParts.time;
        result.push(status);
    }

    return result;
}

customElements.define("history-display", HistoryDisplay);