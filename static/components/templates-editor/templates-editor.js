import {newTemplate} from "./template.js";

export default class TemplatesEditor extends crs.classes.BindableElement {
    #selectedFile = null;

    get shadowDom() {
        return true;
    }

    get html() {
        return import.meta.url.replace(".js", ".html");
    }

    async load() {
        requestAnimationFrame(async () => {
            await this.getTemplates();
        })
    }

    async getTemplates() {
        const response = await fetch("/templates").then(response => response.json());
        this.itemsContainer.innerHTML = "";

        const fragment = document.createDocumentFragment()
        for (const item of response) {
            const li = document.createElement("li");
            li.textContent = item;
            fragment.appendChild(li);
        }
        this.itemsContainer.appendChild(fragment);
    }

    async new() {
        let value = prompt("Enter template name");
        if (value == null) return;

        value = value.replace(" ", "_");

        this.#selectedFile = `${value}.json` ;
        this.editor.value = newTemplate.replace("new_template", value);

        this.setProperty("fileName", value);
    }

    async save() {
        if (this.#selectedFile == null) return;

        const content = this.editor.value;

        await fetch(`/template?name=${this.#selectedFile}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: content
        }).then(result => result.json());

        await this.getTemplates();
        await crs.call("toast_notification", "show", { message: "SUCCESS: template was saved.", severity: "success" });
    }

    async select(event) {
        const target = event.composedPath()[0];
        if (target.nodeName != "LI") return;

        const name = target.textContent;

        const result = await fetch(`/template?name=${name}`).then(result => result.json());
        this.editor.value = JSON.stringify(result, null, 2);
        this.#selectedFile = name;

        this.setProperty("fileName", name);
    }
}

customElements.define("templates-editor", TemplatesEditor);