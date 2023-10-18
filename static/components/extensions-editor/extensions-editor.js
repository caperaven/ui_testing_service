import {newTemplate} from "./template.js";

export default class ExtensionsEditor extends crs.classes.BindableElement {
    #selectedFile = null;

    get shadowDom() {
        return true;
    }

    get html() {
        return import.meta.url.replace(".js", ".html");
    }

    async load() {
        requestAnimationFrame(async () => {
            await this.getExtensions();
        })
    }

    async getExtensions() {
        const response = await fetch("/extensions").then(response => response.json());
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
        let value = prompt("Enter extension name");
        if (value == null) return;

        value = value.replace(" ", "_");

        this.#selectedFile = `${value}.py` ;
        this.editor.value = newTemplate.replace("__name__", value);

        this.setProperty("fileName", value);
    }

    async save() {
        if (this.#selectedFile == null) return;

        const content = this.editor.value;

        const result = await fetch(`/extension?name=${this.#selectedFile}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              content
          })
        }).then(result => result.json());

        console.log(result);

        await this.getExtensions();
        await crs.call("toast_notification", "show", { message: "SUCCESS: template was saved.", severity: "success" });
    }

    async select(event) {
        const target = event.composedPath()[0];
        if (target.nodeName != "LI") return;

        const name = target.textContent;

        const result = await fetch(`/extension?name=${name}`).then(result => result.json());
        this.editor.value = result.content;
        this.#selectedFile = name;

        this.setProperty("fileName", name);
    }
}

customElements.define("extensions-editor", ExtensionsEditor);