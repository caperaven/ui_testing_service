import "./../status-display/status-display.js";
import "./../compose-test/compose-test.js";
import "./../history-display/history-display.js";
import "../templates-editor/templates-editor.js";
import "../extensions-editor/extensions-editor.js";
import "./../../packages/crs-framework/components/toast-notification/toast-notification-actions.js";

export default class ComponentManager extends crs.classes.BindableElement {
    get shadowDom() {
        return true;
    }

    get html() {
        return import.meta.url.replace(".js", ".html");
    }

    async load() {
        await crs.call("toast_notification", "enable", { position: "bottom-center", margin: 10 });
        await this.set_component("compose-test");
    }

    async disconnectedCallback() {
        await crs.call("toast_notification", "disable", {});
        await super.disconnectedCallback();
    }

    async menu_selected(event) {
        const target = event.composedPath()[0];
        const component = target.dataset.component;
        await this.set_component(component);
    }

    async set_component(component) {
        const instance = document.createElement(component);
        const main = this.shadowRoot.querySelector("main");
        main.innerHTML = "";
        main.appendChild(instance);
    }
}

customElements.define("component-manager", ComponentManager);