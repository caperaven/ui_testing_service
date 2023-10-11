export default class ComponentManager extends crs.classes.BindableElement {
    get shadowDom() {
        return true;
    }

    get html() {
        return import.meta.url.replace(".js", ".html");
    }

    async connectedCallback() {
        super.connectedCallback();

        console.log("loaded");
    }
}

customElements.define("component-manager", ComponentManager);