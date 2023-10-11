export default class StatusDisplay extends crs.classes.BindableElement {
    get shadowDom() {
        return true;
    }

    get html() {
        return import.meta.url.replace(".js", ".html");
    }

    async connectedCallback() {
        super.connectedCallback();
    }

    async getStatus() {
        const response = await fetch("/status");
        const status = await response.json();
        console.log(status)
    }
}

customElements.define("status-display", StatusDisplay);