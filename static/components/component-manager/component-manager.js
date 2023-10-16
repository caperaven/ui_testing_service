import "./../status-display/status-display.js";
import "./../compose-test/compose-test.js";

export default class ComponentManager extends crs.classes.BindableElement {
    get shadowDom() {
        return true;
    }

    get html() {
        return import.meta.url.replace(".js", ".html");
    }

    async menu_selected(event) {
        const target = event.composedPath()[0];
        const component = target.dataset.component;
        const instance = document.createElement(component);
        const main = this.shadowRoot.querySelector("main");
        main.innerHTML = "";
        main.appendChild(instance);
    }
}

customElements.define("component-manager", ComponentManager);