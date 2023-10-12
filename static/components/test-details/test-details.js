export default class TestDetails extends crs.classes.BindableElement {
    get shadowDom() {
        return true;
    }

    get html() {
        return import.meta.url.replace(".js", ".html");
    }

    async load() {
        const log = await fetch(`/log?job_id=${this.id}`);
        const logCollection = await log.json();
        const logHtml = createLogHTML(logCollection);
        this.logContainer.innerHTML = logHtml;
    }


}

function createLogHTML(logCollection) {
    let html = [];

    for (const row of logCollection) {
        if (
            row.trim().length === 0 ||
            row.indexOf("(No symbol)") > -1 ||
            row.indexOf("GetHandleVerifier") > -1 ||
            row.indexOf("BaseThreadInitThunk ") > -1 ||
            row.indexOf("RtlUserThreadStart ") > -1 ||
            row.indexOf("Traceback ") > -1 ||
            row.indexOf("Stacktrace:") > -1) {
            continue;
        }

        let line = row.replace(" - process_api - ", " ");

        if (line.indexOf(" INFO ") > -1) {
            line = `<em class='green'>${line}</em>`
        }
        else if (line.indexOf(" ERROR ") > -1) {
            line = `<em class='red'>${line}</em>`
        }
        else if (line.indexOf("Exception") > -1) {
            line = `<em class='red'>${line}</em>`
        }
        else {
            line = `<em class='grey'>${line}</em>`
        }

        html.push(`${line}</br>`)
    }

    return html.join("");
}

customElements.define("test-details", TestDetails);