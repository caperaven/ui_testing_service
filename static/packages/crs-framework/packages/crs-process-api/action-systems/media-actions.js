class n{static async perform(t,e,s,c){await this[t.action](t,e,s,c)}static async render_camera(t,e,s,c){const a=await crs.dom.get_element(t,e,s,c);let i=await crs.process.getValue(t.args.constraints,e,s,c);i==null&&(i={video:!0});const r=await navigator.mediaDevices.getUserMedia(i);a.srcObject=r,a.setAttribute("autoplay","autoplay")}static async capture_image(t,e,s,c){const a=await crs.dom.get_element(t.args.target),i=await crs.dom.get_element(t.args.source);a.getContext("2d").drawImage(i,0,0,a.width,a.height)}}crs.intent.media=n;export{n as MediaActions};