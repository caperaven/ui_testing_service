import "/packages/crs-framework/packages/crs-binding/crs-binding.js";
import "/packages/crs-framework/packages/crs-binding/events/event-emitter.js";
import "/packages/crs-framework/packages/crs-binding/classes/view-base.js";
import "/packages/crs-framework/packages/crs-binding/classes/bindable-element.js";
import "/packages/crs-framework/packages/crs-binding/classes/observable.js";
import "/packages/crs-framework/packages/crs-binding/expressions/code-factories/if.js";
import "/packages/crs-framework/packages/crs-binding/expressions/code-factories/case.js";
import "/packages/crs-framework/packages/crs-binding/managers/inflation-manager.js";
import "/packages/crs-framework/packages/crs-binding/classes/perspective-element.js";
import "/packages/crs-framework/packages/crs-binding/managers/static-inflation-manager.js";

import "/packages/crs-framework/packages/crs-modules/crs-modules.js";
import {initialize} from "/packages/crs-framework/packages/crs-process-api/crs-process-api.js";
await initialize("/packages/crs-framework/packages/crs-process-api");

export class IndexViewModel {
    #bid;

    get bid() {
        return this.#bid;
    }

    constructor() {
        this.#bid = crs.binding.data.addObject(this.constructor.name);
        crs.binding.data.addContext(this.#bid, this);
        crs.binding.dom.enableEvents(this);
        crs.binding.parsers.parseElements(document.body.children, this).catch(error => console.error(error));

        import("/components/component-manager/component-manager.js");
    }

    dispose() {
        this.#bid = null;
    }
}

globalThis.indexViewModel = new IndexViewModel();