var ft=Object.defineProperty;var pt=(t,e,s)=>e in t?ft(t,e,{enumerable:!0,configurable:!0,writable:!0,value:s}):t[e]=s;var W=(t,e,s)=>(pt(t,typeof e!="symbol"?e+"":e,s),s);(function(){const e=document.createElement("link").relList;if(e&&e.supports&&e.supports("modulepreload"))return;for(const r of document.querySelectorAll('link[rel="modulepreload"]'))n(r);new MutationObserver(r=>{for(const o of r)if(o.type==="childList")for(const i of o.addedNodes)i.tagName==="LINK"&&i.rel==="modulepreload"&&n(i)}).observe(document,{childList:!0,subtree:!0});function s(r){const o={};return r.integrity&&(o.integrity=r.integrity),r.referrerPolicy&&(o.referrerPolicy=r.referrerPolicy),r.crossOrigin==="use-credentials"?o.credentials="include":r.crossOrigin==="anonymous"?o.credentials="omit":o.credentials="same-origin",o}function n(r){if(r.ep)return;r.ep=!0;const o=s(r);fetch(r.href,o)}})();class x{constructor(e,s){W(this,"$target");W(this,"props");W(this,"state");this.$target=e,this.props=s,this.setup()}async setup(){await this.asyncInitialization(),this.setEvent(),this.render()}async asyncInitialization(){await new Promise(e=>setTimeout(e,1))}mounted(){}template(){return`
      <div id="Background">
        <img id="bubble1" src="/bubble.png" alt="bubble" class="absolute h-auto w-[800px] -bottom-[30%] -right-[20%] -z-10">
        <img id="bubble2" src="/bubble.png" alt="bubble" class="absolute h-auto w-[400px] top-1/3 left-[87%] -z-10">
        <img id="bubble3" src="/bubble.png" alt="bubble" class="absolute h-auto w-[300px] -top-[18%] left-[40%] -z-10">
        <img id="bubble4" src="/bubble.png" alt="bubble" class="absolute h-auto w-[1000px] top-1/3 -left-[20%] -z-10">
      </div>
    `}render(){this.$target.innerHTML=this.template(),this.mounted()}setEvent(){}setState(e){this.state={...this.state,...e},this.render()}addEvent(e,s,n){[...this.$target.querySelectorAll(s)],this.$target.addEventListener(e,r=>{if(!r.target.closest(s))return!1;r.stopImmediatePropagation(),n(r)})}}const m=t=>{const e=document.querySelector(t);return e instanceof HTMLElement?e:null};class Le{constructor(e){this.$target=e,this.render()}render(){const e=document.createElement("div");m("#app").appendChild(e),e.innerHTML=`
      <img alt='logo' src='logo.png' class=' absolute h-16 top-2 left-4' /> 
    `}}class ne extends x{constructor(e,s){super(e,s)}template(){return`
      <div class='bg-neutral-100 bg-opacity-60 shadow-md rounded-md w-[30vw] h-[60vh] hover:animate-pulse cursor-pointer group'>
        <div class='relative flex flex-col justify-center items-center h-full drop-shadow space-y-2'>
          <div class='text-7xl'>
            ${this.props.emoji}
          </div>
          <div class='text-2xl font-semibold group-hover:font-bold group-hover:text-purple-500'>
            ${this.props.title}
          </div>
          <img src="/bubble.png" alt="img" class="absolute bottom-2 right-2 pointer-events-none drop-shadow w-[25px] h-[25px]" />
        </div>
      </div>
    `}}const N=(t,e=!1)=>{const s=new CustomEvent("historychange",{detail:{to:t,isReplace:e}});dispatchEvent(s)};class ht extends x{template(){return`
      <form id="makeRoomForm" method="post">
      <div class='bg-white w-[500px] h-[600px] rounded-xl shadow-lg flex flex-col justify-between items-center'>
        <div class='ml-2 mt-2 self-start'>
          <span class='text-5xl'>🏡</span>
          <span class='text-2xl font-bold'>방 만들기</span>
        </div>
        <div class='flex flex-col justify-center items-center w-2/3 flex-1 space-y-8 drop-shadow'>
        <div class="input-group">
          <span class="input-group-text w-20 flex justify-center font-medium rounded-r-none">이름</span>
          <input type="text" class="form-control" id="roomName" placeholder="회원님의 방" aria-label="NickName" aria-describedby="input_nickname" required>
        </div>
        <div class="input-group w-full flex ">
          <label class="input-group-text w-20 flex justify-center font-medium rounded-r-none" for="inputGroupSelect01">타입</label>
          <select class="form-select flex-1 border px-[10px]" id="inputGroupSelect01" aria-label="Default select example" required>
            <option selected></option>
            <option value="1">1:1 대전</option>
            <option value="2">토너먼트</option>
          </select>
        </div>
        <div class="input-group w-full flex">
          <label class="input-group-text w-20 flex justify-center font-medium rounded-r-none" for="inputGroupSelect01">인원수</label>
          <select class="form-select flex-1 border px-[10px]" id="inputGroupSelect02" required>
            <option selected></option>
            <option value="1">4명</option>
            <option value="2">8명</option>
          </select>
        </div>
        <div class="w-full flex flex-col">
          <div class="input-group">
            <span class="input-group-text w-20 flex justify-center font-medium rounded-r-none">비밀번호</span>
            <input id="passwordInputBox" type="text" pattern="[0-9]+" class="form-control invalid:border-red-500" id="c" placeholder="비밀방 원하면 입력해" aria-label="NickName" aria-describedby="input_nickname">
          </div>
          <span class="mt-[5px] ml-20 flex text-sm">
            비밀번호는 숫자로만 입력해주세요.
          </span>
        </div>
        </div>
        <div class='mb-10 space-x-8'>
          <button type="button" id='cancelBtn' class="btn btn-secondary bg-gray-500 px-5 py-2">취소</button>
          <button type="submit" id='confirmBtn' class="btn btn-primary bg-blue-500 px-5 py-2">확인</button>
        </div>
      </div>
      </form>
    `}mounted(){this.addEvent("click","#cancelBtn",e=>{this.$target.remove()})}setEvent(){this.addEvent("change","#inputGroupSelect01",e=>{if(e.target.value==="1"){const s=m("#inputGroupSelect02");s.setAttribute("disabled",!0),s.value=""}else e.target.value==="2"&&m("#inputGroupSelect02").removeAttribute("disabled",!1)}),this.addEvent("submit","#makeRoomForm",e=>{console.log("room has been made"),this.$target.remove(),e.preventDefault()})}checkValid(e){const s=m("#roomName").value,n=m("#inputGroupSelect01").value,r=m("#inputGroupSelect02").value,o=m("#c").value;console.log("roomName: ",s),console.log("roomType: ",n),console.log("roomSize: ",r),console.log("roomPassword: ",o)}}class mt extends x{template(){return`
      <div class='fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-white rounded-3xl shadow-2xl flex flex-col justify-center items-center gap-6'>
        <img src="/eva--arrow-back-fill.svg" alt="close" id="goBack" class='h-8 absolute top-6 left-6 rounded-full p-1 hover:shadow-md'/>
        <div class='text-xl font-bold'>
          <span class='text-4xl mr-2'>🤝</span>1:1 랜덤 매칭
        </div>
        <img alt='logo' src='logo.png' class=' h-[150px]' /> 
        <div class='animate-pulse text-lg font-semibold text-gray-700'>
          상대를 찾을 때까지 숨참는 중...
        </div>
      </div>
    `}mounted(){this.addEvent("click","#goBack",e=>{this.$target.remove()})}}function $e(t,e){return function(){return t.apply(e,arguments)}}const{toString:gt}=Object.prototype,{getPrototypeOf:pe}=Object,Q=(t=>e=>{const s=gt.call(e);return t[s]||(t[s]=s.slice(8,-1).toLowerCase())})(Object.create(null)),A=t=>(t=t.toLowerCase(),e=>Q(e)===t),Y=t=>e=>typeof e===t,{isArray:M}=Array,D=Y("undefined");function yt(t){return t!==null&&!D(t)&&t.constructor!==null&&!D(t.constructor)&&k(t.constructor.isBuffer)&&t.constructor.isBuffer(t)}const Be=A("ArrayBuffer");function bt(t){let e;return typeof ArrayBuffer<"u"&&ArrayBuffer.isView?e=ArrayBuffer.isView(t):e=t&&t.buffer&&Be(t.buffer),e}const xt=Y("string"),k=Y("function"),Fe=Y("number"),Z=t=>t!==null&&typeof t=="object",wt=t=>t===!0||t===!1,V=t=>{if(Q(t)!=="object")return!1;const e=pe(t);return(e===null||e===Object.prototype||Object.getPrototypeOf(e)===null)&&!(Symbol.toStringTag in t)&&!(Symbol.iterator in t)},vt=A("Date"),_t=A("File"),Et=A("Blob"),St=A("FileList"),Rt=t=>Z(t)&&k(t.pipe),kt=t=>{let e;return t&&(typeof FormData=="function"&&t instanceof FormData||k(t.append)&&((e=Q(t))==="formdata"||e==="object"&&k(t.toString)&&t.toString()==="[object FormData]"))},Ct=A("URLSearchParams"),Ot=t=>t.trim?t.trim():t.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,"");function q(t,e,{allOwnKeys:s=!1}={}){if(t===null||typeof t>"u")return;let n,r;if(typeof t!="object"&&(t=[t]),M(t))for(n=0,r=t.length;n<r;n++)e.call(null,t[n],n,t);else{const o=s?Object.getOwnPropertyNames(t):Object.keys(t),i=o.length;let c;for(n=0;n<i;n++)c=o[n],e.call(null,t[c],c,t)}}function Me(t,e){e=e.toLowerCase();const s=Object.keys(t);let n=s.length,r;for(;n-- >0;)if(r=s[n],e===r.toLowerCase())return r;return null}const je=typeof globalThis<"u"?globalThis:typeof self<"u"?self:typeof window<"u"?window:global,Ie=t=>!D(t)&&t!==je;function le(){const{caseless:t}=Ie(this)&&this||{},e={},s=(n,r)=>{const o=t&&Me(e,r)||r;V(e[o])&&V(n)?e[o]=le(e[o],n):V(n)?e[o]=le({},n):M(n)?e[o]=n.slice():e[o]=n};for(let n=0,r=arguments.length;n<r;n++)arguments[n]&&q(arguments[n],s);return e}const Tt=(t,e,s,{allOwnKeys:n}={})=>(q(e,(r,o)=>{s&&k(r)?t[o]=$e(r,s):t[o]=r},{allOwnKeys:n}),t),At=t=>(t.charCodeAt(0)===65279&&(t=t.slice(1)),t),Pt=(t,e,s,n)=>{t.prototype=Object.create(e.prototype,n),t.prototype.constructor=t,Object.defineProperty(t,"super",{value:e.prototype}),s&&Object.assign(t.prototype,s)},Nt=(t,e,s,n)=>{let r,o,i;const c={};if(e=e||{},t==null)return e;do{for(r=Object.getOwnPropertyNames(t),o=r.length;o-- >0;)i=r[o],(!n||n(i,t,e))&&!c[i]&&(e[i]=t[i],c[i]=!0);t=s!==!1&&pe(t)}while(t&&(!s||s(t,e))&&t!==Object.prototype);return e},Lt=(t,e,s)=>{t=String(t),(s===void 0||s>t.length)&&(s=t.length),s-=e.length;const n=t.indexOf(e,s);return n!==-1&&n===s},$t=t=>{if(!t)return null;if(M(t))return t;let e=t.length;if(!Fe(e))return null;const s=new Array(e);for(;e-- >0;)s[e]=t[e];return s},Bt=(t=>e=>t&&e instanceof t)(typeof Uint8Array<"u"&&pe(Uint8Array)),Ft=(t,e)=>{const n=(t&&t[Symbol.iterator]).call(t);let r;for(;(r=n.next())&&!r.done;){const o=r.value;e.call(t,o[0],o[1])}},Mt=(t,e)=>{let s;const n=[];for(;(s=t.exec(e))!==null;)n.push(s);return n},jt=A("HTMLFormElement"),It=t=>t.toLowerCase().replace(/[-_\s]([a-z\d])(\w*)/g,function(s,n,r){return n.toUpperCase()+r}),ve=(({hasOwnProperty:t})=>(e,s)=>t.call(e,s))(Object.prototype),Ut=A("RegExp"),Ue=(t,e)=>{const s=Object.getOwnPropertyDescriptors(t),n={};q(s,(r,o)=>{let i;(i=e(r,o,t))!==!1&&(n[o]=i||r)}),Object.defineProperties(t,n)},Dt=t=>{Ue(t,(e,s)=>{if(k(t)&&["arguments","caller","callee"].indexOf(s)!==-1)return!1;const n=t[s];if(k(n)){if(e.enumerable=!1,"writable"in e){e.writable=!1;return}e.set||(e.set=()=>{throw Error("Can not rewrite read-only method '"+s+"'")})}})},Ht=(t,e)=>{const s={},n=r=>{r.forEach(o=>{s[o]=!0})};return M(t)?n(t):n(String(t).split(e)),s},qt=()=>{},zt=(t,e)=>(t=+t,Number.isFinite(t)?t:e),re="abcdefghijklmnopqrstuvwxyz",_e="0123456789",De={DIGIT:_e,ALPHA:re,ALPHA_DIGIT:re+re.toUpperCase()+_e},Wt=(t=16,e=De.ALPHA_DIGIT)=>{let s="";const{length:n}=e;for(;t--;)s+=e[Math.random()*n|0];return s};function Vt(t){return!!(t&&k(t.append)&&t[Symbol.toStringTag]==="FormData"&&t[Symbol.iterator])}const Jt=t=>{const e=new Array(10),s=(n,r)=>{if(Z(n)){if(e.indexOf(n)>=0)return;if(!("toJSON"in n)){e[r]=n;const o=M(n)?[]:{};return q(n,(i,c)=>{const h=s(i,r+1);!D(h)&&(o[c]=h)}),e[r]=void 0,o}}return n};return s(t,0)},Kt=A("AsyncFunction"),Gt=t=>t&&(Z(t)||k(t))&&k(t.then)&&k(t.catch),a={isArray:M,isArrayBuffer:Be,isBuffer:yt,isFormData:kt,isArrayBufferView:bt,isString:xt,isNumber:Fe,isBoolean:wt,isObject:Z,isPlainObject:V,isUndefined:D,isDate:vt,isFile:_t,isBlob:Et,isRegExp:Ut,isFunction:k,isStream:Rt,isURLSearchParams:Ct,isTypedArray:Bt,isFileList:St,forEach:q,merge:le,extend:Tt,trim:Ot,stripBOM:At,inherits:Pt,toFlatObject:Nt,kindOf:Q,kindOfTest:A,endsWith:Lt,toArray:$t,forEachEntry:Ft,matchAll:Mt,isHTMLForm:jt,hasOwnProperty:ve,hasOwnProp:ve,reduceDescriptors:Ue,freezeMethods:Dt,toObjectSet:Ht,toCamelCase:It,noop:qt,toFiniteNumber:zt,findKey:Me,global:je,isContextDefined:Ie,ALPHABET:De,generateString:Wt,isSpecCompliantForm:Vt,toJSONObject:Jt,isAsyncFn:Kt,isThenable:Gt};function g(t,e,s,n,r){Error.call(this),Error.captureStackTrace?Error.captureStackTrace(this,this.constructor):this.stack=new Error().stack,this.message=t,this.name="AxiosError",e&&(this.code=e),s&&(this.config=s),n&&(this.request=n),r&&(this.response=r)}a.inherits(g,Error,{toJSON:function(){return{message:this.message,name:this.name,description:this.description,number:this.number,fileName:this.fileName,lineNumber:this.lineNumber,columnNumber:this.columnNumber,stack:this.stack,config:a.toJSONObject(this.config),code:this.code,status:this.response&&this.response.status?this.response.status:null}}});const He=g.prototype,qe={};["ERR_BAD_OPTION_VALUE","ERR_BAD_OPTION","ECONNABORTED","ETIMEDOUT","ERR_NETWORK","ERR_FR_TOO_MANY_REDIRECTS","ERR_DEPRECATED","ERR_BAD_RESPONSE","ERR_BAD_REQUEST","ERR_CANCELED","ERR_NOT_SUPPORT","ERR_INVALID_URL"].forEach(t=>{qe[t]={value:t}});Object.defineProperties(g,qe);Object.defineProperty(He,"isAxiosError",{value:!0});g.from=(t,e,s,n,r,o)=>{const i=Object.create(He);return a.toFlatObject(t,i,function(h){return h!==Error.prototype},c=>c!=="isAxiosError"),g.call(i,t.message,e,s,n,r),i.cause=t,i.name=t.name,o&&Object.assign(i,o),i};const Xt=null;function ce(t){return a.isPlainObject(t)||a.isArray(t)}function ze(t){return a.endsWith(t,"[]")?t.slice(0,-2):t}function Ee(t,e,s){return t?t.concat(e).map(function(r,o){return r=ze(r),!s&&o?"["+r+"]":r}).join(s?".":""):e}function Qt(t){return a.isArray(t)&&!t.some(ce)}const Yt=a.toFlatObject(a,{},null,function(e){return/^is[A-Z]/.test(e)});function ee(t,e,s){if(!a.isObject(t))throw new TypeError("target must be an object");e=e||new FormData,s=a.toFlatObject(s,{metaTokens:!0,dots:!1,indexes:!1},!1,function(p,b){return!a.isUndefined(b[p])});const n=s.metaTokens,r=s.visitor||d,o=s.dots,i=s.indexes,h=(s.Blob||typeof Blob<"u"&&Blob)&&a.isSpecCompliantForm(e);if(!a.isFunction(r))throw new TypeError("visitor must be a function");function f(u){if(u===null)return"";if(a.isDate(u))return u.toISOString();if(!h&&a.isBlob(u))throw new g("Blob is not supported. Use a Buffer instead.");return a.isArrayBuffer(u)||a.isTypedArray(u)?h&&typeof Blob=="function"?new Blob([u]):Buffer.from(u):u}function d(u,p,b){let v=u;if(u&&!b&&typeof u=="object"){if(a.endsWith(p,"{}"))p=n?p:p.slice(0,-2),u=JSON.stringify(u);else if(a.isArray(u)&&Qt(u)||(a.isFileList(u)||a.endsWith(p,"[]"))&&(v=a.toArray(u)))return p=ze(p),v.forEach(function(O,se){!(a.isUndefined(O)||O===null)&&e.append(i===!0?Ee([p],se,o):i===null?p:p+"[]",f(O))}),!1}return ce(u)?!0:(e.append(Ee(b,p,o),f(u)),!1)}const l=[],y=Object.assign(Yt,{defaultVisitor:d,convertValue:f,isVisitable:ce});function _(u,p){if(!a.isUndefined(u)){if(l.indexOf(u)!==-1)throw Error("Circular reference detected in "+p.join("."));l.push(u),a.forEach(u,function(v,S){(!(a.isUndefined(v)||v===null)&&r.call(e,v,a.isString(S)?S.trim():S,p,y))===!0&&_(v,p?p.concat(S):[S])}),l.pop()}}if(!a.isObject(t))throw new TypeError("data must be an object");return _(t),e}function Se(t){const e={"!":"%21","'":"%27","(":"%28",")":"%29","~":"%7E","%20":"+","%00":"\0"};return encodeURIComponent(t).replace(/[!'()~]|%20|%00/g,function(n){return e[n]})}function he(t,e){this._pairs=[],t&&ee(t,this,e)}const We=he.prototype;We.append=function(e,s){this._pairs.push([e,s])};We.toString=function(e){const s=e?function(n){return e.call(this,n,Se)}:Se;return this._pairs.map(function(r){return s(r[0])+"="+s(r[1])},"").join("&")};function Zt(t){return encodeURIComponent(t).replace(/%3A/gi,":").replace(/%24/g,"$").replace(/%2C/gi,",").replace(/%20/g,"+").replace(/%5B/gi,"[").replace(/%5D/gi,"]")}function Ve(t,e,s){if(!e)return t;const n=s&&s.encode||Zt,r=s&&s.serialize;let o;if(r?o=r(e,s):o=a.isURLSearchParams(e)?e.toString():new he(e,s).toString(n),o){const i=t.indexOf("#");i!==-1&&(t=t.slice(0,i)),t+=(t.indexOf("?")===-1?"?":"&")+o}return t}class Re{constructor(){this.handlers=[]}use(e,s,n){return this.handlers.push({fulfilled:e,rejected:s,synchronous:n?n.synchronous:!1,runWhen:n?n.runWhen:null}),this.handlers.length-1}eject(e){this.handlers[e]&&(this.handlers[e]=null)}clear(){this.handlers&&(this.handlers=[])}forEach(e){a.forEach(this.handlers,function(n){n!==null&&e(n)})}}const Je={silentJSONParsing:!0,forcedJSONParsing:!0,clarifyTimeoutError:!1},es=typeof URLSearchParams<"u"?URLSearchParams:he,ts=typeof FormData<"u"?FormData:null,ss=typeof Blob<"u"?Blob:null,ns={isBrowser:!0,classes:{URLSearchParams:es,FormData:ts,Blob:ss},protocols:["http","https","file","blob","url","data"]},Ke=typeof window<"u"&&typeof document<"u",rs=(t=>Ke&&["ReactNative","NativeScript","NS"].indexOf(t)<0)(typeof navigator<"u"&&navigator.product),os=typeof WorkerGlobalScope<"u"&&self instanceof WorkerGlobalScope&&typeof self.importScripts=="function",is=Object.freeze(Object.defineProperty({__proto__:null,hasBrowserEnv:Ke,hasStandardBrowserEnv:rs,hasStandardBrowserWebWorkerEnv:os},Symbol.toStringTag,{value:"Module"})),T={...is,...ns};function as(t,e){return ee(t,new T.classes.URLSearchParams,Object.assign({visitor:function(s,n,r,o){return T.isNode&&a.isBuffer(s)?(this.append(n,s.toString("base64")),!1):o.defaultVisitor.apply(this,arguments)}},e))}function ls(t){return a.matchAll(/\w+|\[(\w*)]/g,t).map(e=>e[0]==="[]"?"":e[1]||e[0])}function cs(t){const e={},s=Object.keys(t);let n;const r=s.length;let o;for(n=0;n<r;n++)o=s[n],e[o]=t[o];return e}function Ge(t){function e(s,n,r,o){let i=s[o++];if(i==="__proto__")return!0;const c=Number.isFinite(+i),h=o>=s.length;return i=!i&&a.isArray(r)?r.length:i,h?(a.hasOwnProp(r,i)?r[i]=[r[i],n]:r[i]=n,!c):((!r[i]||!a.isObject(r[i]))&&(r[i]=[]),e(s,n,r[i],o)&&a.isArray(r[i])&&(r[i]=cs(r[i])),!c)}if(a.isFormData(t)&&a.isFunction(t.entries)){const s={};return a.forEachEntry(t,(n,r)=>{e(ls(n),r,s,0)}),s}return null}function ds(t,e,s){if(a.isString(t))try{return(e||JSON.parse)(t),a.trim(t)}catch(n){if(n.name!=="SyntaxError")throw n}return(s||JSON.stringify)(t)}const me={transitional:Je,adapter:["xhr","http"],transformRequest:[function(e,s){const n=s.getContentType()||"",r=n.indexOf("application/json")>-1,o=a.isObject(e);if(o&&a.isHTMLForm(e)&&(e=new FormData(e)),a.isFormData(e))return r?JSON.stringify(Ge(e)):e;if(a.isArrayBuffer(e)||a.isBuffer(e)||a.isStream(e)||a.isFile(e)||a.isBlob(e))return e;if(a.isArrayBufferView(e))return e.buffer;if(a.isURLSearchParams(e))return s.setContentType("application/x-www-form-urlencoded;charset=utf-8",!1),e.toString();let c;if(o){if(n.indexOf("application/x-www-form-urlencoded")>-1)return as(e,this.formSerializer).toString();if((c=a.isFileList(e))||n.indexOf("multipart/form-data")>-1){const h=this.env&&this.env.FormData;return ee(c?{"files[]":e}:e,h&&new h,this.formSerializer)}}return o||r?(s.setContentType("application/json",!1),ds(e)):e}],transformResponse:[function(e){const s=this.transitional||me.transitional,n=s&&s.forcedJSONParsing,r=this.responseType==="json";if(e&&a.isString(e)&&(n&&!this.responseType||r)){const i=!(s&&s.silentJSONParsing)&&r;try{return JSON.parse(e)}catch(c){if(i)throw c.name==="SyntaxError"?g.from(c,g.ERR_BAD_RESPONSE,this,null,this.response):c}}return e}],timeout:0,xsrfCookieName:"XSRF-TOKEN",xsrfHeaderName:"X-XSRF-TOKEN",maxContentLength:-1,maxBodyLength:-1,env:{FormData:T.classes.FormData,Blob:T.classes.Blob},validateStatus:function(e){return e>=200&&e<300},headers:{common:{Accept:"application/json, text/plain, */*","Content-Type":void 0}}};a.forEach(["delete","get","head","post","put","patch"],t=>{me.headers[t]={}});const ge=me,us=a.toObjectSet(["age","authorization","content-length","content-type","etag","expires","from","host","if-modified-since","if-unmodified-since","last-modified","location","max-forwards","proxy-authorization","referer","retry-after","user-agent"]),fs=t=>{const e={};let s,n,r;return t&&t.split(`
`).forEach(function(i){r=i.indexOf(":"),s=i.substring(0,r).trim().toLowerCase(),n=i.substring(r+1).trim(),!(!s||e[s]&&us[s])&&(s==="set-cookie"?e[s]?e[s].push(n):e[s]=[n]:e[s]=e[s]?e[s]+", "+n:n)}),e},ke=Symbol("internals");function j(t){return t&&String(t).trim().toLowerCase()}function J(t){return t===!1||t==null?t:a.isArray(t)?t.map(J):String(t)}function ps(t){const e=Object.create(null),s=/([^\s,;=]+)\s*(?:=\s*([^,;]+))?/g;let n;for(;n=s.exec(t);)e[n[1]]=n[2];return e}const hs=t=>/^[-_a-zA-Z0-9^`|~,!#$%&'*+.]+$/.test(t.trim());function oe(t,e,s,n,r){if(a.isFunction(n))return n.call(this,e,s);if(r&&(e=s),!!a.isString(e)){if(a.isString(n))return e.indexOf(n)!==-1;if(a.isRegExp(n))return n.test(e)}}function ms(t){return t.trim().toLowerCase().replace(/([a-z\d])(\w*)/g,(e,s,n)=>s.toUpperCase()+n)}function gs(t,e){const s=a.toCamelCase(" "+e);["get","set","has"].forEach(n=>{Object.defineProperty(t,n+s,{value:function(r,o,i){return this[n].call(this,e,r,o,i)},configurable:!0})})}class te{constructor(e){e&&this.set(e)}set(e,s,n){const r=this;function o(c,h,f){const d=j(h);if(!d)throw new Error("header name must be a non-empty string");const l=a.findKey(r,d);(!l||r[l]===void 0||f===!0||f===void 0&&r[l]!==!1)&&(r[l||h]=J(c))}const i=(c,h)=>a.forEach(c,(f,d)=>o(f,d,h));return a.isPlainObject(e)||e instanceof this.constructor?i(e,s):a.isString(e)&&(e=e.trim())&&!hs(e)?i(fs(e),s):e!=null&&o(s,e,n),this}get(e,s){if(e=j(e),e){const n=a.findKey(this,e);if(n){const r=this[n];if(!s)return r;if(s===!0)return ps(r);if(a.isFunction(s))return s.call(this,r,n);if(a.isRegExp(s))return s.exec(r);throw new TypeError("parser must be boolean|regexp|function")}}}has(e,s){if(e=j(e),e){const n=a.findKey(this,e);return!!(n&&this[n]!==void 0&&(!s||oe(this,this[n],n,s)))}return!1}delete(e,s){const n=this;let r=!1;function o(i){if(i=j(i),i){const c=a.findKey(n,i);c&&(!s||oe(n,n[c],c,s))&&(delete n[c],r=!0)}}return a.isArray(e)?e.forEach(o):o(e),r}clear(e){const s=Object.keys(this);let n=s.length,r=!1;for(;n--;){const o=s[n];(!e||oe(this,this[o],o,e,!0))&&(delete this[o],r=!0)}return r}normalize(e){const s=this,n={};return a.forEach(this,(r,o)=>{const i=a.findKey(n,o);if(i){s[i]=J(r),delete s[o];return}const c=e?ms(o):String(o).trim();c!==o&&delete s[o],s[c]=J(r),n[c]=!0}),this}concat(...e){return this.constructor.concat(this,...e)}toJSON(e){const s=Object.create(null);return a.forEach(this,(n,r)=>{n!=null&&n!==!1&&(s[r]=e&&a.isArray(n)?n.join(", "):n)}),s}[Symbol.iterator](){return Object.entries(this.toJSON())[Symbol.iterator]()}toString(){return Object.entries(this.toJSON()).map(([e,s])=>e+": "+s).join(`
`)}get[Symbol.toStringTag](){return"AxiosHeaders"}static from(e){return e instanceof this?e:new this(e)}static concat(e,...s){const n=new this(e);return s.forEach(r=>n.set(r)),n}static accessor(e){const n=(this[ke]=this[ke]={accessors:{}}).accessors,r=this.prototype;function o(i){const c=j(i);n[c]||(gs(r,i),n[c]=!0)}return a.isArray(e)?e.forEach(o):o(e),this}}te.accessor(["Content-Type","Content-Length","Accept","Accept-Encoding","User-Agent","Authorization"]);a.reduceDescriptors(te.prototype,({value:t},e)=>{let s=e[0].toUpperCase()+e.slice(1);return{get:()=>t,set(n){this[s]=n}}});a.freezeMethods(te);const P=te;function ie(t,e){const s=this||ge,n=e||s,r=P.from(n.headers);let o=n.data;return a.forEach(t,function(c){o=c.call(s,o,r.normalize(),e?e.status:void 0)}),r.normalize(),o}function Xe(t){return!!(t&&t.__CANCEL__)}function z(t,e,s){g.call(this,t??"canceled",g.ERR_CANCELED,e,s),this.name="CanceledError"}a.inherits(z,g,{__CANCEL__:!0});function ys(t,e,s){const n=s.config.validateStatus;!s.status||!n||n(s.status)?t(s):e(new g("Request failed with status code "+s.status,[g.ERR_BAD_REQUEST,g.ERR_BAD_RESPONSE][Math.floor(s.status/100)-4],s.config,s.request,s))}const bs=T.hasStandardBrowserEnv?{write(t,e,s,n,r,o){const i=[t+"="+encodeURIComponent(e)];a.isNumber(s)&&i.push("expires="+new Date(s).toGMTString()),a.isString(n)&&i.push("path="+n),a.isString(r)&&i.push("domain="+r),o===!0&&i.push("secure"),document.cookie=i.join("; ")},read(t){const e=document.cookie.match(new RegExp("(^|;\\s*)("+t+")=([^;]*)"));return e?decodeURIComponent(e[3]):null},remove(t){this.write(t,"",Date.now()-864e5)}}:{write(){},read(){return null},remove(){}};function xs(t){return/^([a-z][a-z\d+\-.]*:)?\/\//i.test(t)}function ws(t,e){return e?t.replace(/\/?\/$/,"")+"/"+e.replace(/^\/+/,""):t}function Qe(t,e){return t&&!xs(e)?ws(t,e):e}const vs=T.hasStandardBrowserEnv?function(){const e=/(msie|trident)/i.test(navigator.userAgent),s=document.createElement("a");let n;function r(o){let i=o;return e&&(s.setAttribute("href",i),i=s.href),s.setAttribute("href",i),{href:s.href,protocol:s.protocol?s.protocol.replace(/:$/,""):"",host:s.host,search:s.search?s.search.replace(/^\?/,""):"",hash:s.hash?s.hash.replace(/^#/,""):"",hostname:s.hostname,port:s.port,pathname:s.pathname.charAt(0)==="/"?s.pathname:"/"+s.pathname}}return n=r(window.location.href),function(i){const c=a.isString(i)?r(i):i;return c.protocol===n.protocol&&c.host===n.host}}():function(){return function(){return!0}}();function _s(t){const e=/^([-+\w]{1,25})(:?\/\/|:)/.exec(t);return e&&e[1]||""}function Es(t,e){t=t||10;const s=new Array(t),n=new Array(t);let r=0,o=0,i;return e=e!==void 0?e:1e3,function(h){const f=Date.now(),d=n[o];i||(i=f),s[r]=h,n[r]=f;let l=o,y=0;for(;l!==r;)y+=s[l++],l=l%t;if(r=(r+1)%t,r===o&&(o=(o+1)%t),f-i<e)return;const _=d&&f-d;return _?Math.round(y*1e3/_):void 0}}function Ce(t,e){let s=0;const n=Es(50,250);return r=>{const o=r.loaded,i=r.lengthComputable?r.total:void 0,c=o-s,h=n(c),f=o<=i;s=o;const d={loaded:o,total:i,progress:i?o/i:void 0,bytes:c,rate:h||void 0,estimated:h&&i&&f?(i-o)/h:void 0,event:r};d[e?"download":"upload"]=!0,t(d)}}const Ss=typeof XMLHttpRequest<"u",Rs=Ss&&function(t){return new Promise(function(s,n){let r=t.data;const o=P.from(t.headers).normalize();let{responseType:i,withXSRFToken:c}=t,h;function f(){t.cancelToken&&t.cancelToken.unsubscribe(h),t.signal&&t.signal.removeEventListener("abort",h)}let d;if(a.isFormData(r)){if(T.hasStandardBrowserEnv||T.hasStandardBrowserWebWorkerEnv)o.setContentType(!1);else if((d=o.getContentType())!==!1){const[p,...b]=d?d.split(";").map(v=>v.trim()).filter(Boolean):[];o.setContentType([p||"multipart/form-data",...b].join("; "))}}let l=new XMLHttpRequest;if(t.auth){const p=t.auth.username||"",b=t.auth.password?unescape(encodeURIComponent(t.auth.password)):"";o.set("Authorization","Basic "+btoa(p+":"+b))}const y=Qe(t.baseURL,t.url);l.open(t.method.toUpperCase(),Ve(y,t.params,t.paramsSerializer),!0),l.timeout=t.timeout;function _(){if(!l)return;const p=P.from("getAllResponseHeaders"in l&&l.getAllResponseHeaders()),v={data:!i||i==="text"||i==="json"?l.responseText:l.response,status:l.status,statusText:l.statusText,headers:p,config:t,request:l};ys(function(O){s(O),f()},function(O){n(O),f()},v),l=null}if("onloadend"in l?l.onloadend=_:l.onreadystatechange=function(){!l||l.readyState!==4||l.status===0&&!(l.responseURL&&l.responseURL.indexOf("file:")===0)||setTimeout(_)},l.onabort=function(){l&&(n(new g("Request aborted",g.ECONNABORTED,t,l)),l=null)},l.onerror=function(){n(new g("Network Error",g.ERR_NETWORK,t,l)),l=null},l.ontimeout=function(){let b=t.timeout?"timeout of "+t.timeout+"ms exceeded":"timeout exceeded";const v=t.transitional||Je;t.timeoutErrorMessage&&(b=t.timeoutErrorMessage),n(new g(b,v.clarifyTimeoutError?g.ETIMEDOUT:g.ECONNABORTED,t,l)),l=null},T.hasStandardBrowserEnv&&(c&&a.isFunction(c)&&(c=c(t)),c||c!==!1&&vs(y))){const p=t.xsrfHeaderName&&t.xsrfCookieName&&bs.read(t.xsrfCookieName);p&&o.set(t.xsrfHeaderName,p)}r===void 0&&o.setContentType(null),"setRequestHeader"in l&&a.forEach(o.toJSON(),function(b,v){l.setRequestHeader(v,b)}),a.isUndefined(t.withCredentials)||(l.withCredentials=!!t.withCredentials),i&&i!=="json"&&(l.responseType=t.responseType),typeof t.onDownloadProgress=="function"&&l.addEventListener("progress",Ce(t.onDownloadProgress,!0)),typeof t.onUploadProgress=="function"&&l.upload&&l.upload.addEventListener("progress",Ce(t.onUploadProgress)),(t.cancelToken||t.signal)&&(h=p=>{l&&(n(!p||p.type?new z(null,t,l):p),l.abort(),l=null)},t.cancelToken&&t.cancelToken.subscribe(h),t.signal&&(t.signal.aborted?h():t.signal.addEventListener("abort",h)));const u=_s(y);if(u&&T.protocols.indexOf(u)===-1){n(new g("Unsupported protocol "+u+":",g.ERR_BAD_REQUEST,t));return}l.send(r||null)})},de={http:Xt,xhr:Rs};a.forEach(de,(t,e)=>{if(t){try{Object.defineProperty(t,"name",{value:e})}catch{}Object.defineProperty(t,"adapterName",{value:e})}});const Oe=t=>`- ${t}`,ks=t=>a.isFunction(t)||t===null||t===!1,Ye={getAdapter:t=>{t=a.isArray(t)?t:[t];const{length:e}=t;let s,n;const r={};for(let o=0;o<e;o++){s=t[o];let i;if(n=s,!ks(s)&&(n=de[(i=String(s)).toLowerCase()],n===void 0))throw new g(`Unknown adapter '${i}'`);if(n)break;r[i||"#"+o]=n}if(!n){const o=Object.entries(r).map(([c,h])=>`adapter ${c} `+(h===!1?"is not supported by the environment":"is not available in the build"));let i=e?o.length>1?`since :
`+o.map(Oe).join(`
`):" "+Oe(o[0]):"as no adapter specified";throw new g("There is no suitable adapter to dispatch the request "+i,"ERR_NOT_SUPPORT")}return n},adapters:de};function ae(t){if(t.cancelToken&&t.cancelToken.throwIfRequested(),t.signal&&t.signal.aborted)throw new z(null,t)}function Te(t){return ae(t),t.headers=P.from(t.headers),t.data=ie.call(t,t.transformRequest),["post","put","patch"].indexOf(t.method)!==-1&&t.headers.setContentType("application/x-www-form-urlencoded",!1),Ye.getAdapter(t.adapter||ge.adapter)(t).then(function(n){return ae(t),n.data=ie.call(t,t.transformResponse,n),n.headers=P.from(n.headers),n},function(n){return Xe(n)||(ae(t),n&&n.response&&(n.response.data=ie.call(t,t.transformResponse,n.response),n.response.headers=P.from(n.response.headers))),Promise.reject(n)})}const Ae=t=>t instanceof P?t.toJSON():t;function F(t,e){e=e||{};const s={};function n(f,d,l){return a.isPlainObject(f)&&a.isPlainObject(d)?a.merge.call({caseless:l},f,d):a.isPlainObject(d)?a.merge({},d):a.isArray(d)?d.slice():d}function r(f,d,l){if(a.isUndefined(d)){if(!a.isUndefined(f))return n(void 0,f,l)}else return n(f,d,l)}function o(f,d){if(!a.isUndefined(d))return n(void 0,d)}function i(f,d){if(a.isUndefined(d)){if(!a.isUndefined(f))return n(void 0,f)}else return n(void 0,d)}function c(f,d,l){if(l in e)return n(f,d);if(l in t)return n(void 0,f)}const h={url:o,method:o,data:o,baseURL:i,transformRequest:i,transformResponse:i,paramsSerializer:i,timeout:i,timeoutMessage:i,withCredentials:i,withXSRFToken:i,adapter:i,responseType:i,xsrfCookieName:i,xsrfHeaderName:i,onUploadProgress:i,onDownloadProgress:i,decompress:i,maxContentLength:i,maxBodyLength:i,beforeRedirect:i,transport:i,httpAgent:i,httpsAgent:i,cancelToken:i,socketPath:i,responseEncoding:i,validateStatus:c,headers:(f,d)=>r(Ae(f),Ae(d),!0)};return a.forEach(Object.keys(Object.assign({},t,e)),function(d){const l=h[d]||r,y=l(t[d],e[d],d);a.isUndefined(y)&&l!==c||(s[d]=y)}),s}const Ze="1.6.7",ye={};["object","boolean","number","function","string","symbol"].forEach((t,e)=>{ye[t]=function(n){return typeof n===t||"a"+(e<1?"n ":" ")+t}});const Pe={};ye.transitional=function(e,s,n){function r(o,i){return"[Axios v"+Ze+"] Transitional option '"+o+"'"+i+(n?". "+n:"")}return(o,i,c)=>{if(e===!1)throw new g(r(i," has been removed"+(s?" in "+s:"")),g.ERR_DEPRECATED);return s&&!Pe[i]&&(Pe[i]=!0,console.warn(r(i," has been deprecated since v"+s+" and will be removed in the near future"))),e?e(o,i,c):!0}};function Cs(t,e,s){if(typeof t!="object")throw new g("options must be an object",g.ERR_BAD_OPTION_VALUE);const n=Object.keys(t);let r=n.length;for(;r-- >0;){const o=n[r],i=e[o];if(i){const c=t[o],h=c===void 0||i(c,o,t);if(h!==!0)throw new g("option "+o+" must be "+h,g.ERR_BAD_OPTION_VALUE);continue}if(s!==!0)throw new g("Unknown option "+o,g.ERR_BAD_OPTION)}}const ue={assertOptions:Cs,validators:ye},L=ue.validators;class G{constructor(e){this.defaults=e,this.interceptors={request:new Re,response:new Re}}async request(e,s){try{return await this._request(e,s)}catch(n){if(n instanceof Error){let r;Error.captureStackTrace?Error.captureStackTrace(r={}):r=new Error;const o=r.stack?r.stack.replace(/^.+\n/,""):"";n.stack?o&&!String(n.stack).endsWith(o.replace(/^.+\n.+\n/,""))&&(n.stack+=`
`+o):n.stack=o}throw n}}_request(e,s){typeof e=="string"?(s=s||{},s.url=e):s=e||{},s=F(this.defaults,s);const{transitional:n,paramsSerializer:r,headers:o}=s;n!==void 0&&ue.assertOptions(n,{silentJSONParsing:L.transitional(L.boolean),forcedJSONParsing:L.transitional(L.boolean),clarifyTimeoutError:L.transitional(L.boolean)},!1),r!=null&&(a.isFunction(r)?s.paramsSerializer={serialize:r}:ue.assertOptions(r,{encode:L.function,serialize:L.function},!0)),s.method=(s.method||this.defaults.method||"get").toLowerCase();let i=o&&a.merge(o.common,o[s.method]);o&&a.forEach(["delete","get","head","post","put","patch","common"],u=>{delete o[u]}),s.headers=P.concat(i,o);const c=[];let h=!0;this.interceptors.request.forEach(function(p){typeof p.runWhen=="function"&&p.runWhen(s)===!1||(h=h&&p.synchronous,c.unshift(p.fulfilled,p.rejected))});const f=[];this.interceptors.response.forEach(function(p){f.push(p.fulfilled,p.rejected)});let d,l=0,y;if(!h){const u=[Te.bind(this),void 0];for(u.unshift.apply(u,c),u.push.apply(u,f),y=u.length,d=Promise.resolve(s);l<y;)d=d.then(u[l++],u[l++]);return d}y=c.length;let _=s;for(l=0;l<y;){const u=c[l++],p=c[l++];try{_=u(_)}catch(b){p.call(this,b);break}}try{d=Te.call(this,_)}catch(u){return Promise.reject(u)}for(l=0,y=f.length;l<y;)d=d.then(f[l++],f[l++]);return d}getUri(e){e=F(this.defaults,e);const s=Qe(e.baseURL,e.url);return Ve(s,e.params,e.paramsSerializer)}}a.forEach(["delete","get","head","options"],function(e){G.prototype[e]=function(s,n){return this.request(F(n||{},{method:e,url:s,data:(n||{}).data}))}});a.forEach(["post","put","patch"],function(e){function s(n){return function(o,i,c){return this.request(F(c||{},{method:e,headers:n?{"Content-Type":"multipart/form-data"}:{},url:o,data:i}))}}G.prototype[e]=s(),G.prototype[e+"Form"]=s(!0)});const K=G;class be{constructor(e){if(typeof e!="function")throw new TypeError("executor must be a function.");let s;this.promise=new Promise(function(o){s=o});const n=this;this.promise.then(r=>{if(!n._listeners)return;let o=n._listeners.length;for(;o-- >0;)n._listeners[o](r);n._listeners=null}),this.promise.then=r=>{let o;const i=new Promise(c=>{n.subscribe(c),o=c}).then(r);return i.cancel=function(){n.unsubscribe(o)},i},e(function(o,i,c){n.reason||(n.reason=new z(o,i,c),s(n.reason))})}throwIfRequested(){if(this.reason)throw this.reason}subscribe(e){if(this.reason){e(this.reason);return}this._listeners?this._listeners.push(e):this._listeners=[e]}unsubscribe(e){if(!this._listeners)return;const s=this._listeners.indexOf(e);s!==-1&&this._listeners.splice(s,1)}static source(){let e;return{token:new be(function(r){e=r}),cancel:e}}}const Os=be;function Ts(t){return function(s){return t.apply(null,s)}}function As(t){return a.isObject(t)&&t.isAxiosError===!0}const fe={Continue:100,SwitchingProtocols:101,Processing:102,EarlyHints:103,Ok:200,Created:201,Accepted:202,NonAuthoritativeInformation:203,NoContent:204,ResetContent:205,PartialContent:206,MultiStatus:207,AlreadyReported:208,ImUsed:226,MultipleChoices:300,MovedPermanently:301,Found:302,SeeOther:303,NotModified:304,UseProxy:305,Unused:306,TemporaryRedirect:307,PermanentRedirect:308,BadRequest:400,Unauthorized:401,PaymentRequired:402,Forbidden:403,NotFound:404,MethodNotAllowed:405,NotAcceptable:406,ProxyAuthenticationRequired:407,RequestTimeout:408,Conflict:409,Gone:410,LengthRequired:411,PreconditionFailed:412,PayloadTooLarge:413,UriTooLong:414,UnsupportedMediaType:415,RangeNotSatisfiable:416,ExpectationFailed:417,ImATeapot:418,MisdirectedRequest:421,UnprocessableEntity:422,Locked:423,FailedDependency:424,TooEarly:425,UpgradeRequired:426,PreconditionRequired:428,TooManyRequests:429,RequestHeaderFieldsTooLarge:431,UnavailableForLegalReasons:451,InternalServerError:500,NotImplemented:501,BadGateway:502,ServiceUnavailable:503,GatewayTimeout:504,HttpVersionNotSupported:505,VariantAlsoNegotiates:506,InsufficientStorage:507,LoopDetected:508,NotExtended:510,NetworkAuthenticationRequired:511};Object.entries(fe).forEach(([t,e])=>{fe[e]=t});const Ps=fe;function et(t){const e=new K(t),s=$e(K.prototype.request,e);return a.extend(s,K.prototype,e,{allOwnKeys:!0}),a.extend(s,e,null,{allOwnKeys:!0}),s.create=function(r){return et(F(t,r))},s}const w=et(ge);w.Axios=K;w.CanceledError=z;w.CancelToken=Os;w.isCancel=Xe;w.VERSION=Ze;w.toFormData=ee;w.AxiosError=g;w.Cancel=w.CanceledError;w.all=function(e){return Promise.all(e)};w.spread=Ts;w.isAxiosError=As;w.mergeConfig=F;w.AxiosHeaders=P;w.formToJSON=t=>Ge(a.isHTMLForm(t)?new FormData(t):t);w.getAdapter=Ye.getAdapter;w.HttpStatusCode=Ps;w.default=w;const E=w.create({baseURL:"http://localhost:8000/api/"});E.interceptors.request.use(function(t){const e=localStorage.getItem("accessToken");return e!==null&&(t.headers.Authorization=`Bearer ${e}`),t},async function(t){return console.log(t),Promise.reject(t)});E.interceptors.response.use(function(t){return t},async function(t){const{config:e,data:s,status:n}=t.response;if(n===401){localStorage.removeItem("accessToken");const r={url:"/jwt/reissue",method:"POST",data:{refresh:localStorage.getItem("refreshToken")}},{data:o}=await E(r),{access:i}=o;return localStorage.setItem("accessToken",i),await E(e)}else if(n===403){N("/login");return}return Promise.reject(t.response)});class Ns extends x{async setup(){this.state=await this.getUserInfo(),this.setEvent(),this.render()}async getUserInfo(){const s=await E({url:"/main"}),{data:n}=s;return console.log(n),n}mounted(){const e=document.createElement("div"),s=document.createElement("div");e.id="category",e.className="flex justify-center items-center w-full h-full gap-6",e.innerHTML=`
    <div id='room-list'></div>
    <div id='make-room'></div>
    <div id='random-match'></div>
    `,m("#app").appendChild(e),s.id="info",s.className="",s.innerHTML=`
    <div id='info' class='absolute flex top-10 right-6 text-3xl font-bold items-center gap-2 cursor-pointer group'>
      <div class="w-10 h-10 rounded-full overflow-hidden shadow-md group-hover:w-11 group-hover:h-11">
        <img id='userAvatar' src="${this.state.picture}" alt="profile" class="w-[100%] h-[100%] object-cover">
      </div>
      <span class='underline decoration-indigo-500 decoration-solid underline-offset-3 decoration-2 font-semibold text-2xl group-hover:text-gray-500'>${this.state.username}</span>님
    </div>
    `,this.addEvent("click","#info",n=>{N("/mypage")}),m("#app").appendChild(s),new Le,new ne(m("#room-list"),{title:"방 목록",emoji:"🗒️"}),new ne(m("#make-room"),{title:"방 만들기",emoji:"🏡"}),new ne(m("#random-match"),{title:"랜덤 매칭",emoji:"🤝"}),this.addEvent("click","#make-room",n=>{const r=document.createElement("div");r.id="Modal_overlay",m("#app").appendChild(r),new ht(r)}),this.addEvent("click","#random-match",n=>{const r=document.createElement("div");r.id="Modal_overlay",m("#app").appendChild(r),new mt(r)}),this.addEvent("click","#room-list",n=>{N("/room-list")})}}class Ls extends x{mounted(){const e=document.createElement("div");e.id="TwoFA_form",this.$target.appendChild(e),this.set2FAWrapper(e),e.innerHTML=`
      <div id="TwoFA_form__wrapper"
        class="w-[640px] h-[380px] m-[100px] mt-[150px] flex flex-col items-center justify-center
          bg-white rounded-[30px] shadow-[5px_5px_10px_0px_rgba(0,0,0,0.2)] text-2xl"
      >
        <h1>2차 인증 코드</h1>
        <p id="InvalidCode" class="my-[10px] text-white text-sm">잘못된 코드입니다.</p>
        <form name="2FA">
          <input
            type="text" id="TwoFA_form__input"
            class="bg-transparent w-[300px] h-[100px] border-b border-black text-center text-5xl
              m-[20px] required:border-red-500"
          >
          <input type="text" style="display:none;">
        </form>
        <span class="text-sm text-center">
          2차 인증 코드를 42에 등록된 이메일로 발송하였습니다.<br />
          상단에 인증 코드를 입력해 주세요.
        </span>
      </div>
      <div
        id="TwoFA_form__submit"
        class="flex justify-center items-center text-2xl font-semibold hover:text-3xl hover:font-bold text-purple-400 w-[200px] h-[200px] bg-cover cursor-pointer"
        style="background-image: url(/bubble.png)"
      >
        Login
      </div>
    </div>
    `}setEvent(){this.$target.addEventListener("click",e=>{e.target.id==="TwoFA_form__submit"&&this.checkValid()}),this.$target.addEventListener("keydown",e=>{if(e.key==="Enter"&&e.target.id==="TwoFA_form__input"){if(e.isComposing)return;this.checkValid()}})}checkValid(){const e=m("#TwoFA_form__input");if(console.log("input.value: ",e.value),e.value===""){e.classList.add("border-red-500"),e.focus();return}this.handleCode(e)}set2FAWrapper(e){e.style.width="100vw",e.style.height="100vh",e.style.display="flex",e.style.flexDirection="column",e.style.justifyContent="center",e.style.alignItems="center"}async handleCode(e){try{const n={method:"POST",url:"/oauth/login/2FA",data:{code:e.value}};console.log(n);const r=await E(n);r&&r.status===200&&N("/")}catch(s){s.status===400&&(console.log("2차인증에 실패했습니다."),e.value="",m("#InvalidCode").classList.remove("text-white"),m("#InvalidCode").classList.add("text-red-500"),e.classList.add("border-red-500"),e.focus())}}}class xe extends x{constructor(e,s,n=null){super(e,s),this.$target=e,this.props=s,this.notFound=n,this.setup()}template(){return""}mounted(){const e=document.createElement("div");e.id="LoadingWrapper",this.$target.appendChild(e);for(let n=0;n<20;n++)this.createBubbles(n);const s=document.createElement("div");s.id="TitleWrapper",s.style.position="absolute",s.style.zIndex="100",this.$target.appendChild(s),this.notFound==404?this.setNotFound(s):this.setLoading(s)}createBubbles(e){const s=document.createElement("div");m("#LoadingWrapper").appendChild(s),s.classList.add("Loading"),this.setBubbleStyle(s,e),s.innerHTML=`
      <img src="/bubble.png" alt="bubbles" class="w-full h-full"/>
    `}setBubbleStyle(e,s){let n=(Math.floor(Math.random()*31)+10)*10,r=Math.random()*10+3,o=parseFloat(r.toFixed(3)),i=Math.random()*9+5;const c=Math.floor(Math.random()*4),h=5,f=Math.floor(100/h),l=Array.from({length:f},(_,u)=>u*h)[s];e.style.bottom=`-${n}px`,e.style.left=`${l}%`,e.style.width=`${n}px`,e.style.height=`${n}px`,e.style.animationDelay=`${c}s, ${c}s`,e.style.animationDuration=`${i}s, ${o}s`,e.style.opacity=`${n/400}`;const y=document.createElement("style");document.head.appendChild(y),y.sheet.insertRule(`@keyframes shaking {
      0% {
        transform: translateX(-${n*.05}%);
      }
      50% {
        transform: translateX(${n*.05}%);
      }
      100% {
        transform: translateX(-${n*.05}%);
      }
    }`),y.sheet.insertRule(`@keyframes goUp {
      0% {
        bottom: -${n}px;
      }
      100% {
        bottom: 100%;
      }
    }`)}setNotFound(e){e.innerHTML=`
    <div id="NotFound" class="w-[100vw] h-[100vh] flex flex-col justify-center item-center">
    <h1 id="NotFoundTitle"
      class="
        flex align-center item-center justify-center
        text-8xl text-gray-600 font-bold
        my-[20px]
      "
      >
      <img src="/bubbles_emoji.png" alt="bubbles"
        class="w-20 h-20 my-auto mx-[20px] flex justify-center item-center align-center"
      />
      404 Not Found
      <img src="/bubbles_emoji.png" alt="bubbles"
        class="w-20 h-20 my-auto mx-[20px] flex justify-center item-center align-center"
      />
    </h1>
    <p id="NotFoundDescription"
      class="
        flex align-center item-center justify-center
        text-3xl text-gray-600 font-semibold
        my-[20px]
      "
      >
      페이지를 찾을 수 없습니다.
    </p>
  </div>
    `}setLoading(e){e.innerHTML=`
    <div id="Loading" class="w-[100vw] h-[100vh] flex flex-col justify-center item-center">
      <h1 id="LoadingTitle"
        class="
          flex align-center item-center justify-center
          text-8xl text-gray-600 font-bold
          my-[20px]
        "
      >
        <img src="/bubbles_emoji.png" alt="bubbles"
          class="w-20 h-20 my-auto mx-[20px] flex justify-center item-center align-center"
        />
        Loading...
        <img src="/bubbles_emoji.png" alt="bubbles"
          class="w-20 h-20 my-auto mx-[20px] flex justify-center item-center align-center"
        />
      </h1>
    </div>
  `}}class $s extends x{template(){return`
    <div class="flex flex-col justify-center items-center h-full">
    <img
    src="/logo.png"
    alt="logo"
    class="pointer-events-none w-[500px] h-[500px] animate-bounce"
    />
    <div
    id="loginBtn"
    class="flex justify-center items-center text-2xl font-semibold hover:text-3xl hover:font-bold text-purple-400 w-[200px] h-[200px] bg-cover cursor-pointer"
    style="background-image: url(/bubble.png)"
    >
    
        <a
          href="https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-80593f2ca92d09f7d42166593b99cc335953a89bc775c0596ac93a9eb3bc4c44&redirect_uri=http%3A%2F%2F10.13.6.6%3A5173%2Flogin&response_type=code"
          class="w-full h-full justify-center hover:text-3xl hover:text-purple-400"
        >
          <span class="w-full h-full rounded-full flex items-center justify-center align-middle">
            Login
          </span>
        </a>
      </div>
      <div class="-z-10">
        <img
          src="/bubble.png"
          alt="img"
          class="pointer-events-none absolute -bottom-40 -left-40 w-[500px] h-[500px]"
        />
        <img
          src="/bubble.png"
          alt="img"
          class="pointer-events-none absolute -bottom-28 -right-40 w-[600px] h-[600px]"
        />
        <img
          src="/bubble.png"
          alt="img"
          class="pointer-events-none absolute bottom-80 -right-10 w-[200px] h-[200px]"
        />
      </div>
    </div>;
    `}mounted(){this.handleCode()}async handleCode(){const e=window.location.search,n=new URLSearchParams(e).get("code");if(!n)return;const r={method:"POST",url:"/oauth/login/",data:{code:n}};new xe(this.$target,this.state);const{data:o,status:i}=await E(r);localStorage.setItem("accessToken",o.access),localStorage.setItem("refreshToken",o.refresh),i===200?N("/"):i===201&&(E({url:"/oauth/login/2FA/email"}),N("/2FA"))}}class tt extends x{constructor(e,s,n,r){super(e,s),this.$target=e,this.props=s,this.icon1=n,this.icon2=r,this.iconID1="",this.iconID2="",this.setup(),this.setEvent(),this.render()}setIconID(){this.icon1==="/add_friend.svg"?this.iconID1="icon_add_friend":this.icon1==="/delete_friend.svg"&&(this.iconID1="icon_delete_friend"),this.icon2==="/edit.svg"?this.iconID2="edit_modal_open":this.icon2==="/block.svg"?this.iconID2="icon_block":this.icon2==="/unblock.svg"&&(this.iconID2="icon_unblock")}template(){return this.setIconID(),`
    
      <div class="w-[100px] h-[100px] rounded-full overflow-hidden">
        <img id="mypage_avatar" src="${this.props.picture}" alt="profile" class="w-[100%] h-[100%] object-cover">
      </div>
      <div id="mypage_profile__wrapper">
        <div id="mypage_name">${this.props.username}</div>
        <div id="mypage_winlose">${this.props.total_win}승 ${this.props.total_lose}패</div>
      </div>
      ${this.icon1!==""?this.createIcon1():""}
      <img id="${this.iconID2}" src="${this.icon2}" class="w-[40px] h-[40px] mx-[20px] cursor-pointer" alt="edit">
    `}createIcon1(){return`
      <img id="${this.iconID1}" src="${this.icon1}" class="w-[40px] h-[40px] ml-[20px] cursor-pointer" alt="edit">
    `}}class st extends x{template(){return`
      <table class="MyPage__table">
        <caption>
          경기 기록
        </caption>
        <tbody class="TableBody">
        </tbody>
      </table>
    `}mounted(){const e=this.$target.querySelector(".TableBody");m("#user_info_history")&&(e.style.height="410px"),e.innerHTML=this.generateHistoryTable()}generateHistoryTable(){const{matchHistories:e}=this.props;return e===void 0?"":e.map(s=>`
      <tr class="History_table">
        <td class="history_date">${s.scoreDate}</td>
        <td class="history_content">${this.props.userName} vs ${s.userName}</td>
        <td class="history_result">${s.winner===this.props.userName?"Win":"Lose"}</td>
      </tr>
    `).join("")}}const R={FRIEND:1,BLOCK:2};class H extends x{constructor(e,s,n,r){super(e,r),this.$target=e,this.props=r,this.title=s,this.n=n,this.setup()}async setup(){this.state=await this.getUserInfo(),this.setEvent(),this.render()}async getUserInfo(){const s=await E({url:"/mypage"}),{data:n}=s;return n}template(){let e="/arrow-left-disabled.svg",s="/arrow-right-enabled.svg";this.n===R.BLOCK&&(e="/arrow-left-enabled.svg",s="/arrow-right-disabled.svg");let n="Friend_table";return this.n===R.BLOCK&&(n="Block_table"),`
      <table class="MyPage__table" id=${n}>
        <caption>
          <img src="${e}" class="icon_left" id="icon_left${this.n}" alt="left-fill"></img>
          ${this.title}
          <img src="${s}" class="icon_right" id="icon_right${this.n}" alt="right-fill"></img>
        </caption>
        <tbody>
          ${this.generateUserTable()}
        </tbody>
      </table>
    `}generateUserTable(){let e="Friend_table",s=this.state.friends,n="display: inline",r="friend";return this.n===R.BLOCK&&(e="Block_table",s=this.state.ban_list,n="display: none",r="block"),s.map(o=>`
      <tr id="${e}">
        <td class="flex ml-[20px]">
          <div class="w-[40px] h-[40px] relative">
            
            ${this.n===R.FRIEND?'<div class="w-[10px] h-[10px] rounded-full bg-[#60D395] absolute right-0 bottom-0"></div>':""}
            
            <div class="w-[40px] h-[40px] rounded-full overflow-hidden">
              
              <img src="${o.picture}" alt="profile" id="${r}_avatar_${o.username}" class="user_avatar w-[100%] h-[100%] object-cover cursor-pointer">
            </div>
          </div>
        </td>
        
        <td id="${r}_name_${o.username}" class="user_name">${o.username}</td>
        
        <td><img class="user_dm" src="/eva--message-circle-fill.svg" style="${n}"></td>
        
        <td><img class="user_delete" src="/eva--close-fill.svg"></td>
      </tr>
    `).join("")}}class Bs extends x{template(){return`
      <form name="editInfo" class="w-[500px] h-[300px] flex justify-center
        px-[40px] bg-white rounded-[30px] flex-col">
        <div class="w-full h-[170px] flex flex-col mb-3">
          ${this.createImageEdit()}
          ${this.createInputNickName()}
        </div>
        <div class="w-full h-[40px] flex flex-row-reverse">
          ${this.createButtons()}
        </div>
      </form>
    `}createImageEdit(){return`
    <div class="w-full h-[120px] flex mb-[10px] p-[10px]">
      
      <div class="relative w-[100px] h-[100px]">
        <div class="absolute w-full h-full rounded-full overflow-hidden">
          <div class="flex w-full h-full justify-center items-center">
            <img src="${m("#mypage_avatar").getAttribute("src")}" id="edit_modal_avatar" alt="user avatar" class="w-[100%] h-[100%] object-cover"/>
          </div>
        </div>
        
        <div class="absolute w-full h-full bg-white opacity-70">
        <input type="file" id="avatar_upload" name="avatar_upload" style="display:none"
        accept="image/*"/>
          <img id="avatar_upload_entry" src="/edit.svg" alt="edit icon" class="w-full p-[28px] cursor-pointer">
        </div>
      </div>
      
      <div class="h-full flex grow flex-col justify-center ml-[20px]">
        <div class="text-2xl font-semibold">이미지 편집</div>
        <div class="text-lg mt-[8px]">최대 용량 1MB</div>
      </div>
    </div>`}createInputNickName(){return`
      <div class="input-group mb-3">
        <span class="input-group-text" id="input_nickname">이름 입력</span>
        <input type="text" id="nickname_upload" class="form-control" placeholder="input name" aria-label="NickName" aria-describedby="input_nickname">
        <input type="text" style="display:none;">
      </div>
    `}createButtons(){return`
      <button id="edit_submit" type="button" class="btn btn-primary" style="background-color:#007bff; margin-left:8px; border-radius: 8px; padding-left:30px; padding-right:30px">확인</button>
      <button type="button" id="edit_modal_close" class="btn btn-secondary" style="background-color:#6c757d; border-radius: 8px; padding-left:30px; padding-right:30px">취소</button>
    `}}function Fs(t){t.style.left="0",t.style.top="0",t.style.position="absolute",t.style.width="100%",t.style.height="100%",t.style.backgroundColor="rgba(0, 0, 0, 0.2)",t.style.display="flex",t.style.justifyContent="center",t.style.alignItems="center",t.style["backdrop-filter"]="blur(1.5px)"}class X extends x{constructor(e,s,n,r=""){super(e,n),this.$target=e,this.props=n,this.targetUser=r,this.stat=s,Fs(this.$target),this.setup(),this.setEvent(),this.render()}template(){return`
      <div class="w-[400px] h-[200px] flex justify-center flex-col bg-white rounded-[30px] px-[40px]">
        <div class="h-[76px] pb-[20px] text-lg font-medium">
        ${this.targetUser===""?"":this.targetUser+" 님을<br />"}
        ${this.stat==="friend"?this.targetUser===""?"친구 목록에서 삭제되었습니다.":"친구 목록에서 삭제하시겠습니까?":this.targetUser===""?"차단 목록에서 삭제되었습니다.":"차단 목록에서 삭제하시겠습니까?"}
        </div>
        <div class="w-full h-[40px] flex flex-row-reverse">
          ${this.createButtons()}
        </div>
      </div>
    `}createButtons(){let e="confirm_ok";return this.targetUser===""&&(e="modal_close"),`<button id="${e}" type="submit" class="btn btn-primary" style="background-color:#007bff; margin-left:8px; border-radius: 8px; padding-left:30px; padding-right:30px">확인</button>
    ${this.targetUser===""?"":'<button type="button" id="modal_close" class="btn btn-secondary" style="background-color:#6c757d; border-radius: 8px; padding-left:30px; padding-right:30px">취소</button>'}
    `}}class B extends x{constructor(e,s,n,r){super(e,s),this.$target=e,this.props=s,this.icon1=n,this.icon2=r,this.iconID1="",this.iconID2="",this.setup()}async setup(){this.state=await this.getUserInfo(),this.setEvent(),this.render()}async getUserInfo(){const e={url:"/users/info",params:{userName:this.props}},s=await E(e),{data:n}=s;return n}template(){return`
      <div class="w-[800px] h-[800px] relative justify-center
        bg-white rounded-[30px] flex-col p-[50px]">
        <img src="/eva--close-fill.svg" alt="icon close" id="modal_close"
          class="absolute top-[20px] right-[20px] w-[40px] h-[40px] cursor-pointer"
        />
        <div id="user_info_container"
          class="w-[100%] h-[100%]"
        >
        </div>
      </div>
    `}mounted(){const e=this.$target.querySelector("#user_info_container"),s=document.createElement("div");s.id="user_info_profile",this.setUserInfoContainer(s),this.setUserInfoProfile(s),e.appendChild(s),new tt(s,this.state,this.icon1,this.icon2);const n=document.createElement("div");n.id="user_info_history",this.setUserHistoryTable(n),e.appendChild(n),new st(n,this.state)}setUserInfoContainer(e){e.style.width="100%",e.style.height="100%",e.style.flexDirection="column",e.style.justifyContent="center",e.style.alignItems="center"}setUserInfoProfile(e){e.style.width="100%",e.style.height="200px",e.style["padding-left"]="50px",e.style["padding-right"]="50px",e.style.display="flex",e.style.flexDirection="row",e.style.justifyContent="center",e.style.alignItems="center"}setUserHistoryTable(e){e.style.width="100%",e.style.height="500px",e.style.display="flex",e.style.overflow="hidden",e.style.borderRadius="30px",e.style.boxShadow="5px 5px 10px 0px rgba(0, 0, 0, 0.2)"}}class Ms extends x{template(){return`
      <div id="chat_wrapper" class="w-[800px] h-[800px] relative justify-center
        bg-white rounded-[30px] flex-col px-[30px] py-[20px]">
        <div class="w-full h-full flex-col justify-center">
          <div class="w-100% h-[50px] mb-[10px] flex justify-center items-center">
            <span class="w-[720px] text-center text-[24px] font-bold">${this.props}</span>
            <img src="/game.svg" alt="icon game" id="chat_game"
              class="cursor-pointer mx-[10px]">
            <img src="/eva--close-fill.svg" alt="icon close" id="modal_close"
              class="cursor-pointer"/>
          </div>
          <div id="chat_content_wrapper"
            class="w-full h-[630px] mb-[10px] overflow-y-auto"
          >
            <div id="chat_content" class="w-full min-h-[630px] flex flex-col justify-end"></div>
          </div>
          <div class="w-full h-[60px] flex justify-center items-center">
            <input type="text" id="chat_input" class="w-full h-[40px] px-[15px] mr-[8px] rounded-[20px]
              focus:outline-none bg-[#e7eff8]"/>
            <img src="/bubble.png" alt="icon send" id="chat_send" class="w-[52px] h-[52px] cursor-pointer"/>
          </div>
        </div>
      </div>
    `}setEvent(){this.$target.addEventListener("keydown",e=>{if(e.key==="Enter"&&e.target.id==="chat_input"){if(e.isComposing||e.target.value==="")return;this.sendMessage(e.target.value),e.target.value=""}}),this.$target.addEventListener("click",e=>{if(e.target.id==="chat_send"){const s=this.$target.querySelector("#chat_input");if(s.value==="")return;this.sendMessage(s.value),s.value=""}})}sendMessage(e){const s=this.$target.querySelector("#chat_content"),n=document.createElement("div");n.class="my_chat_bubble",this.setMyChatBubbleStyle(n,e),s.appendChild(n),m("#chat_content_wrapper").scrollTo(0,s.scrollHeight);const r=n.previousElementSibling;r&&r.class==="my_chat_bubble"&&(r.style.borderBottomRightRadius="20px")}setMyChatBubbleStyle(e,s){e.style.width="fit-content",e.style.height="fit-content",e.style.maxWidth="60%",e.style.padding="10px",e.style.paddingLeft="20px",e.style.paddingRight="20px",e.style.borderRadius="20px",e.style.borderBottomRightRadius="0px",e.style.backgroundColor="#ABC2EF",e.style.marginBottom="2px",e.style.marginLeft="auto",e.style.overflowWrap="break-word",e.textContent=s}setSentChatBubbleStyle(e,s){e.style.width="fit-content",e.style.height="fit-content",e.style.maxWidth="60%",e.style.padding="10px",e.style.paddingLeft="20px",e.style.paddingRight="20px",e.style.borderRadius="20px",e.style.borderBottomLeftRadius="0px",e.style.backgroundColor="#E7E7E7",e.style.marginBottom="2px",e.style.marginRight="auto",e.style.overflowWrap="break-word",e.textContent=s}}let I="",$="",U="";async function Ne(t,e,s){if(m("#userAvatar")?I=m("#userAvatar").getAttribute("src"):I=m("#mypage_avatar").getAttribute("src"),s.classList.contains("icon_right")||s.classList.contains("icon_left"))js(t,e,s);else if(s.id==="edit_modal_open")Is(t,e);else if(s.id==="avatar_upload_entry")I=m("#mypage_avatar").getAttribute("src"),Us();else if(s.id==="edit_submit")await Hs(t,e),s.closest("#Modal_overlay").remove();else if(s.id==="edit_modal_close")qs(t,s,I);else if(s.classList.contains("user_avatar")||s.classList.contains("user_name"))zs(t,s);else if(s.id==="icon_add_friend"){const{res:r,target:o}=await Ws(t,e,s),i=s.closest("#Modal_overlay");console.log("modal: ",i),r.status===200&&(console.log("target: ",o),new B(i,o,"/delete_friend.svg","/block.svg"))}else if(s.id==="icon_delete_friend"){const{res:r,target:o}=await Vs(t,e,s),i=s.closest("#Modal_overlay");r.status===200&&(console.log("target: ",o),new B(i,o,"/add_friend.svg","/block.svg"))}else if(s.id==="icon_block"){const{res:r,target:o}=await Js(t,e,s),i=s.closest("#Modal_overlay");console.log("modal: ",i),r.status===200&&new B(i,o,"","/unblock.svg")}else if(s.id==="icon_unblock"){const{res:r,target:o}=await Ks(t,e,s),i=s.closest("#Modal_overlay");r.status===200&&new B(i,o,"/add_friend.svg","/block.svg")}else if(s.classList.contains("user_dm"))Gs(t,e,s);else if(s.classList.contains("user_delete"))Xs(t,e,s);else if(s.id==="confirm_ok"){const{res:r,flag:o}=await Qs(t,e,s),i=s.closest("#Modal_overlay");console.log("res: ",r),console.log("modal: ",i),console.log("flag: ",o),r.status===200&&(console.log("success"),o===R.FRIEND?new X(i,"friend",e.username):new X(i,"delete",e.username))}else if(s.id==="modal_close"){console.log("modal close"),s.closest("#Modal_overlay").remove();const r=m("#Friend_table");if(r)console.log("table: ",r),new H(r,"친구 목록",R.FRIEND,e);else{const o=m("#Block_table");console.log("table: ",o),new H(o,"차단 목록",R.BLOCK,e)}}}function js(t,e,s){if(t.querySelector("#Friend_table")){if(s.classList.contains("icon_right")){const n=t.querySelector("#MyPage_info__user_list");new H(n,"차단 목록",R.BLOCK,e)}}else if(t.querySelector("#Block_table")&&s.classList.contains("icon_left")){const n=t.querySelector("#MyPage_info__user_list");new H(n,"친구 목록",R.FRIEND,e)}}function Is(t,e,s){console.log("edit");const n=document.createElement("div");n.id="Modal_overlay",t.appendChild(n),new Bs(n,e.username)}function Us(t,e){console.log("avatar upload"),m("#avatar_upload").click(),m("#avatar_upload").addEventListener("change",Ds.bind(this))}function Ds(t){const s=t.target.files[0];if(s.size>1048576){alert("1MB 이하의 파일만 업로드 가능합니다.");return}const n=new FileReader;n.readAsDataURL(s),n.onload=r=>{$=r.target.result,m("#edit_modal_avatar").setAttribute("src",r.target.result)}}async function Hs(t,e,s){console.log("edit modal submit");const n=await Ys(e,$);return $!==""&&(m("#mypage_avatar").setAttribute("src",$),I=$),m("#nickname_upload").value!==""&&(m("#mypage_name").textContent=m("#nickname_upload").value),n}function qs(t,e,s){console.log("edit modal close"),s!==m("#mypage_avatar").src&&(m("#mypage_avatar").setAttribute("src",s),m("#edit_modal_avatar").setAttribute("src",s)),s!==$&&($=""),e.closest("#Modal_overlay").remove()}function zs(t,e){console.log("user info");const s=document.createElement("div");s.id="Modal_overlay",t.appendChild(s);let n="";e.id.includes("avatar")?n=e.id.slice(14):n=e.textContent,document.querySelector("#Friend_table")&&new B(s,n,"/delete_friend.svg","/block.svg"),document.querySelector("#Block_table")&&new B(s,n,"","/unblock.svg")}async function Ws(t,e,s){console.log("add friend");const r=s.closest("#Modal_overlay").querySelector("#mypage_name").textContent;return{res:await E({method:"POST",url:"/friend/add",data:{friend:r}}),target:r}}async function Vs(t,e,s){console.log("delete friend");const r=s.closest("#Modal_overlay").querySelector("#mypage_name").textContent;return{res:await E({method:"POST",url:"/friend/delete",data:{friendName:r}}),target:r}}async function Js(t,e,s){console.log("block user");const r=s.closest("#Modal_overlay").querySelector("#mypage_name").textContent,o={method:"POST",url:"/friend/ban-list/add",data:{userName:e.username,blockName:r}};return{res:await E(o),target:r}}async function Ks(t,e,s){console.log("unblock user");const r=s.closest("#Modal_overlay").querySelector("#mypage_name").textContent;return{res:await E({method:"POST",url:"/friend/ban-list/delete",data:{blockName:r}}),target:r}}function Gs(t,e,s){console.log("DM");const n=document.createElement("div");n.id="Modal_overlay",t.appendChild(n);const r=s.parentNode.previousSibling.previousSibling.textContent;console.log(r),new Ms(n,r)}function Xs(t,e,s){console.log("delete");const n=document.createElement("div");n.id="Modal_overlay",t.appendChild(n),U=s.parentNode.previousSibling.previousSibling.previousSibling.previousSibling.textContent,document.querySelector("#Friend_table")?new X(n,"friend",e.username,U):new X(n,"block",e.username,U)}async function Qs(t,e,s){const n=s.closest("#Modal_overlay");let r,o;return n&&n.id==="Modal_overlay"&&(document.querySelector("#Friend_table")?(console.log("confirm_ok: delete friend"),o=R.FRIEND,r={method:"POST",url:"/friend/delete",data:{friendName:U}}):(console.log("confirm_ok: delete block"),o=R.BLOCK,r={method:"POST",url:"/friend/ban-list/delete",data:{blockName:U}})),console.log(r),{res:await E(r),flag:o}}async function Ys(t,e){const n={method:"POST",url:"/mypage/editor",data:{newName:m("#nickname_upload").value,picture:e}},r=await E(n),{data:o}=r;return o}class Zs extends x{async getMyPageInfo(){const s=await E({url:"/mypage"}),{data:n}=s;return n}async setup(){this.state=await this.getMyPageInfo(),this.setEvent(),this.render()}mounted(){this.appendInfoWrapper();const e=this.$target.querySelector("#MyPage_profile"),s=this.$target.querySelector("#MyPage_info__history"),n=this.$target.querySelector("#MyPage_info__user_list");new tt(e,this.state,"","/edit.svg"),new st(s,this.state),new H(n,"친구 목록",R.FRIEND,this.state)}appendInfoWrapper(){const e=document.createElement("div");e.id="MyPage_wrapper",this.$target.appendChild(e),e.style.height="100vh",e.innerHTML=`
    <div class="w-full h-full flex flex-col overflow-auto">
      <img id='goBack' src="/eva--arrow-back-fill.svg" alt="close" class='h-8 absolute top-6 left-6 rounded-full p-1 hover:shadow-md'/>
      <div class="w-[calc(100% - 400px)] h-[870px] px-[100px] pb-[50px] min-w-[800px] max-w-[1200px] flex flex-col  m-auto">
          <div id="MyPage_profile_container">
            <div id="MyPage_profile"></div>
          </div>
          <div id="MyPage_info">
            <div id="MyPage_info__history"></div>
            <div id="MyPage_info__user_list"></div>
        </div>
      </div>
    </div>`,this.addEvent("click","#goBack",s=>{N("/")})}setEvent(){this.$target.classList.contains("MyPageEvents")||(this.$target.classList.add("MyPageEvents"),this.$target.addEventListener("click",this.handleButton.bind(this)),this.$target.addEventListener("keydown",e=>{if(e.key==="Enter"&&e.target.id==="nickname_upload"){if(e.isComposing)return;Ne(this.$target,this.state,m("#edit_submit"))}}))}handleButton(e){const s=e.target;Ne(this.$target,this.state,s)}}class en extends x{template(){return this.props.map(({name:e,type:s,max:n,enter:r,secret:o})=>`
    <div class='bg-zinc-100 h-[100px] rounded-xl shadow-md flex justify-between items-center px-4 hover:bg-zinc-200'>
      <div class='flex flex-col'>
        <span class='text-xl font-semibold text-gray-700'>${e}</span>
        <span class='text-sm text-gray-600'>${s===1?"1:1":"토너먼트"}</span>
      </div>
      <div class='flex flex-col items-end text-lg text-gray-800'>
        <div>
          <span>${r}</span> / <span>${n}</span>
        </div>
        ${o?'<svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 1024 1024"><path fill="currentColor" d="M832 464h-68V240c0-70.7-57.3-128-128-128H388c-70.7 0-128 57.3-128 128v224h-68c-17.7 0-32 14.3-32 32v384c0 17.7 14.3 32 32 32h640c17.7 0 32-14.3 32-32V496c0-17.7-14.3-32-32-32M540 701v53c0 4.4-3.6 8-8 8h-40c-4.4 0-8-3.6-8-8v-53a48.01 48.01 0 1 1 56 0m152-237H332V240c0-30.9 25.1-56 56-56h248c30.9 0 56 25.1 56 56z"/></svg>':'<svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 1024 1024"><path fill="currentColor" d="M832 464H332V240c0-30.9 25.1-56 56-56h248c30.9 0 56 25.1 56 56v68c0 4.4 3.6 8 8 8h56c4.4 0 8-3.6 8-8v-68c0-70.7-57.3-128-128-128H388c-70.7 0-128 57.3-128 128v224h-68c-17.7 0-32 14.3-32 32v384c0 17.7 14.3 32 32 32h640c17.7 0 32-14.3 32-32V496c0-17.7-14.3-32-32-32M540 701v53c0 4.4-3.6 8-8 8h-40c-4.4 0-8-3.6-8-8v-53a48.01 48.01 0 1 1 56 0"/></svg>'}
      </div>
    </div>
    `).join("")}mounted(){}}class tn extends x{template(){return`
      <div class='w-full h-[80%] flex flex-col justify-start items-center'>
        <img id='goBack' src="/eva--arrow-back-fill.svg" alt="close" class='h-8 absolute top-6 left-6 rounded-full p-1 hover:shadow-md'/>
        <div class='text-3xl font-bold mb-4'>
          <span class='text-4xl mr-2'>🗒</span>방 목록
        </div>
        <div id='room-list-detail' class='w-full px-6 grid grid-cols-2 gap-3'></div>
      </div>
    `}mounted(){this.addEvent("click","#goBack",e=>{N("/")}),this.props=[{name:"방 이름 1",type:1,max:2,enter:1,secret:!1},{name:"방 이름 2",type:2,max:8,enter:2,secret:!0},{name:"방 이름 3",type:1,max:2,enter:1,secret:!1}],new en(m("#room-list-detail"),this.props)}}class sn extends x{mounted(){const e=document.createElement("div");e.id="room-list",e.className="fixed top-1/2 left-1/2 transform -translate-x-1/2 flex justify-center items-center -translate-y-1/2 bg-white w-2/3 h-3/4 shadow-lg rounded-3xl",m("#app").appendChild(e),new Le,new tn(e)}}class nn extends x{constructor(e,s,n,r,o,i){super(e,s),this.$target=e,this.props=this.props,this.picture1=n,this.picture2=r,this.score1=o,this.score2=i,this.setup(),this.setEvent(),this.render()}template(){return`
      <div class="w-full h-1/5">
        <div id="gameScreenInfo">
          <div id="gameScreenPicture1"></div>
          <div id="gameScreenScore">
            <p id="gameScreenScoreNum">${this.score1} : ${this.score2}</p>
          </div>
          <div id="gameScreenPicture2"></div>
        </div>
      </div>

      <div id="pongScene" class="w-full h-4/5 bg-black">
        <canvas id="myCanvas" class="w-full h-full"></canvas>
      </div>
    `}}class rn extends x{constructor(e,s,n,r){super(e,s),this.$target=e,this.props=this.props,this.picture1=n,this.picture2=r,this.setup(),this.setEvent(),this.render()}template(){return`
      <div class="w-full h-full flex-col justify-center m-auto">
          <div class="w-full h-[90%] mb-[10px] overflow-y-auto">
          <div class="w-full min-h-[630px] flex flex-col justify-end"></div>
        </div>
        <div class="w-[95%] h-[60px] flex justify-center items-center m-auto">
          <input type="text" id="chat_input" class="w-full h-[40px] px-[15px] mr-[8px] rounded-[20px]
            focus:outline-none bg-[#e7eff8]"/>
          <img src="/bubble.png" alt="icon send" id="chat_send" class="w-[52px] h-[52px] cursor-pointer"/>
        </div>
      </div>`}}class on extends x{constructor(e,s){super(e,s),this.$target=e,this.props=this.props,this.pong(),this.render()}pong(){const e=m("#myCanvas"),s=e.getContext("2d");let n=e.width/2,r=e.height/2;const o=2;let i=3,c=10,h=0,f=30,d=5,l=(e.height-f)/2,y=!1,_=!1,u=.8,p=-.8,b=(e.height-f)/2,v=!1,S=!1;document.addEventListener("keydown",lt,!1),document.addEventListener("keyup",ct,!1),document.addEventListener("keydown",dt,!1),document.addEventListener("keyup",ut,!1);function O(){for(s.beginPath();h<720;)s.rect((e.width-i)/2,h,i,c),s.fillStyle="white",s.fill(),h+=20;h=0,s.closePath()}function se(){s.beginPath(),s.arc(n,r,o,0,Math.PI*2),s.fillStyle="white",s.fill(),s.closePath()}function nt(){s.beginPath(),s.rect(d+10,l,d,f),s.fillStyle="white",s.fill(),s.closePath(),y&&l<e.height-f?l+=3:_&&l>0&&(l-=3)}function rt(){s.beginPath(),s.rect(e.width-d-10,b,d,f),s.fillStyle="white",s.fill(),s.closePath(),v&&b<e.height-f?b+=3:S&&b>0&&(b-=3)}function ot(){n+u<o?(alert("USER2 WIN"),clearInterval(we),document.location.reload()):n+u>e.width-o-15&&r>b&&r<b+f&&n<e.width-o-5&&(u=-u)}function it(){n+u>e.width-o?(alert("USER1 WIN"),clearInterval(we),document.location.reload()):n+u<o+d+15&&r>l&&r<l+f&&n>o+5&&(u=-u)}function at(){s.clearRect(0,0,e.width,e.height),se(),O(),nt(),rt(),n+=u,r+=p,ot(),it(),(r+p>e.height-o||r+p<o)&&(p=-p)}function lt(C){C.keyCode==83?y=!0:C.keyCode==87&&(_=!0)}function ct(C){C.keyCode==83?y=!1:C.keyCode==87&&(_=!1)}function dt(C){C.keyCode==40?v=!0:C.keyCode==38&&(S=!0)}function ut(C){C.keyCode==40?v=!1:C.keyCode==38&&(S=!1)}let we=setInterval(at,10)}render(){}}class an extends x{constructor(e,s){super(e,s)}mounted(){this.appendInfoWrapper();const e=m("#gameScreenContainer"),s=m("#gameChatContainer");new nn(e,this.state,"","","2","1"),new rn(s,this.state,"","");const n=m("#gameScene");new on(n,this.state)}appendInfoWrapper(){const e=document.createElement("div");e.id="GameRoom_wrapper",this.$target.appendChild(e),e.style.height="100vh",e.innerHTML=`
      <div class="w-full h-full flex">
      <img id='goBack' src="/eva--arrow-back-fill.svg" alt="close" class='h-8 absolute top-6 left-6 rounded-full p-1 hover:shadow-md'/> 
        <div class="w-[1728px] h-[1117px] m-auto">
          <div class="w-full h-[100px] flex">
            <div class="w-[1485px] h-full"></div>
            <button class="w-[75px] h-[32px] mt-10  hover:bg-gray-300 font-bold rounded-xl shadow-md">초대</button>
            <div class="w-[6px] h-full"></div>
            <button class="w-[75px] h-[32px] mt-10  hover:bg-gray-300 font-bold rounded-xl shadow-md">강퇴</button>
          </div>
          <div class="w-full h-[917px] flex">
            <div id="gameScreenContainer"></div>
            <div id="gameChatContainer"></div>
          </div>
          <div class="w-full h-[100px] grid place-items-center">
            <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 border border-blue-700 rounded">준비</button>
          </div>
        </div>
      </div>`,this.addEvent("click","#goBack",s=>{N("/")})}setEvent(){this.$target.classList.contains("GameRoomEvents")||(this.$target.classList.add("GameRoomEvents"),this.$target.addEventListener("click",this.handleButton.bind(this)))}handleButton(e){e.target,this.$target,this.state}}const ln=[{path:/^\/api$/,element:Ns},{path:/^\/login$/,element:$s},{path:/^\/mypage$/,element:Zs},{path:/^\/room-list$/,element:sn},{path:/^\/game-room$/,element:an},{path:/^\/2FA$/,element:Ls},{path:/^\/loading$/,element:xe}];class cn extends x{template(){return""}mounted(){new xe(this.$target,null,404)}}function dn(t){this.$container=t;const e=()=>ln.find(r=>r.path.test(location.pathname)),s=()=>{var o;const r=((o=e())==null?void 0:o.element)||cn;new r(this.$container)};(()=>{window.addEventListener("historychange",({detail:r})=>{const{to:o,isReplace:i}=r;i||o===location.pathname?history.replaceState(null,"",o):history.pushState(null,"",o),s()}),window.addEventListener("popstate",()=>{s()})})(),s()}function un(t){this.$container=t,(()=>{new dn(t)})()}function fn(t){let e=-1;return()=>{cancelAnimationFrame(e),e=requestAnimationFrame(t)}}function pn(){const t={currentStateKey:0,states:[],root:null,rootComponent:null};function e(r){const{currentStateKey:o,states:i}=t;i.length===o&&i.push(r);const c=i[o],h=f=>{i[o]=f,s()};return t.currentStateKey+=1,[c,h]}const s=fn(()=>{const{root:r,rootComponent:o}=t;!r||!o||(r.innerHTML=new o(r),t.currentStateKey=0)});function n(r,o){t.root=o,t.rootComponent=r,s()}return{useState:e,render:n}}const{useState:gn,render:hn}=pn();hn(un,m("#app"));
