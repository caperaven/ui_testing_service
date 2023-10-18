export default class TemplatesEditor extends crs.classes.BindableElement {
    get shadowDom() {
        return true;
    }

    get html() {
        return import.meta.url.replace(".js", ".html");
    }
}

customElements.define("templates-editor", TemplatesEditor);