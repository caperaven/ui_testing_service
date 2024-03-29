class p {
    static async perform(a, s, t, r) {
        await this[a.action](a, s, t, r)
    }

    static async observe(a, s, t, r) {
        const e = await crs.dom.get_element(a.args.element, s, t, r),
            c = await crs.process.getValue(a.args.properties, s, t, r),
            l = await crs.process.getValue(a.args.callback, s, t, r);
        e._dataId == null && (e._dataId = crs.binding.data.addObject(e.id));
        let n = e._dataId;
        e._processObserver = e._processObserver || {nextId: 0};
        const o = u(e), d = await g(e, c, o);
        e._processObserver[o] = {properties: c, eval: d, callback: l};
        for (let b of c) await crs.binding.data.addCallback(n, b, e._processObserver[o].eval);
        return o
    }

    static async unobserve(a, s, t, r) {
        const e = await crs.dom.get_element(a.args.element, s, t, r),
            c = await crs.process.getValue(a.args.ids, s, t, r);
        for (const l of c) {
            const n = e._processObserver[l];
            for (const o of n.properties) await crs.binding.data.removeCallback(e._dataId, o, n.eval);
            n.properties = null, n.eval = null, n.callback = null, delete e._processObserver[l]
        }
    }

    static async notify_ready(a, s, t, r) {
        const e = await crs.dom.get_element(a.args.element, s, t, r);
        e.dataset.ready = "true", e.dispatchEvent(new CustomEvent("ready", {bubbles: true, composed: true}))
    }

    static async on_ready(a, s, t, r) {
        const e = await crs.dom.get_element(a.args.element, s, t, r),
            c = await crs.process.getValue(a.args.callback, s, t, r),
            l = await crs.process.getValue(a.args.caller, s, t, r);
        if (e.dataset.ready == "true") return await c.call(l);
        const n = async () => {
            e.removeEventListener("ready", n), await c.call(l)
        };
        e.addEventListener("ready", n)
    }
}

function u(i) {
    const a = i._processObserver.nextId;
    return i._processObserver.nextId = a + 1, a
}

async function g(i, a, s) {
    let t = ["if ( "];
    for (const e of a) t.push(`(await crs.binding.data.getProperty(this._dataId, "${e}"))  != null && `);
    return t.push(`) { this._processObserver[${s}].callback.call(this) };`), t = t.join("").replace("&& )", ")"), await new crs.classes.AsyncFunction(t).bind(i)
}

crs.intent.component = p;
export {p as ComponentActions};
