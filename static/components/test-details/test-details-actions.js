import "./../../packages/crs-framework/components/dialogs/dialogs-actions.js";
import "./../../packages/crs-framework/components/tab-sheet/tab-sheet.js";
import "./../../packages/crs-framework/components/text-editor/text-editor.js";
import "./test-details.js";

export class TestDetailsActions {
    static async show(step, context, process, item) {
        const id = await crs.process.getValue(step.args.id, context, process, item);
        const name = await crs.process.getValue(step.args.name, context, process, item);

        const component = document.createElement("test-details");
        component.id = id;

        const header = document.createElement("h2");
        header.textContent = name;

        await crs.call("dialogs", "show", {
            id: "test-details",
            content: {
                header: header,
                body: component
            },
            options: {
                maximized: true
            }
        })
    }

    static async close(step, context, process, item) {
        await crs.call("dialogs", "close", {
            id: "test-details"
        })
    }
}

crs.intent.test_details = TestDetailsActions;