export default class StatusDisplay extends crs.classes.BindableElement {
    get shadowDom() {
        return true;
    }

    get html() {
        return import.meta.url.replace(".js", ".html");
    }

    async load() {
        const template = this.shadowRoot.querySelector("template");
        await crs.binding.inflation.manager.register("statuses", template);
        await this.getStatus();
    }

    async disconnectedCallback() {
        await crs.binding.inflation.manager.unregister("statuses");
        await super.disconnectedCallback();
    }

    async getStatus() {
        const response = await fetch("/status");
        const statuses = statusToArray(await response.json());

        const elements = await crs.binding.inflation.manager.get("statuses", statuses, this.collection.children);
        this.collection.innerHTML = "";
        this.collection.append(...elements);
    }
}

function statusToArray(statusObject) {
    const result = [];

    const keys = Object.keys(statusObject);

    for (const key of keys) {
        const new_status = statusObject[key]
        new_status.uuid = key;
        result.push(new_status);
    }

    return result;
}

customElements.define("status-display", StatusDisplay);