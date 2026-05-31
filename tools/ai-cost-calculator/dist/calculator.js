"use strict";var AICostCalculator=(()=>{var w=Object.defineProperty;var P=Object.getOwnPropertyDescriptor;var R=Object.getOwnPropertyNames;var D=Object.prototype.hasOwnProperty;var A=(t,n)=>{for(var r in n)w(t,r,{get:n[r],enumerable:!0})},K=(t,n,r,f)=>{if(n&&typeof n=="object"||typeof n=="function")for(let l of R(n))!D.call(t,l)&&l!==r&&w(t,l,{get:()=>n[l],enumerable:!(f=P(n,l))||f.enumerable});return t};var O=t=>K(w({},"__esModule",{value:!0}),t);var j={};A(j,{initCalculator:()=>G});var L=[{label:"Simple",inputK:15,outputK:1},{label:"Medium",inputK:35,outputK:3},{label:"Complex",inputK:60,outputK:8},{label:"Planning (Opus)",inputK:80,outputK:10}],M=[40,35,15],z=M.reduce((t,n)=>t+n,0),x=[{id:"cc",name:"Claude Code",color:"#4A90D9",baseCost:()=>0,includedCredits:()=>0,rates:[{input:1,output:5},{input:3,output:15,cachedInput:.3},{input:3,output:15,cachedInput:.3},{input:15,output:75,cachedInput:.5}],rateLabels:["Haiku","Sonnet","Sonnet","Opus (direct)"]},{id:"cop",name:"Copilot",color:"#E07B39",baseCost:t=>t*19,includedCredits:t=>t*19,rates:[{input:.25,output:2},{input:2,output:8},{input:3,output:15},{input:5,output:25}],rateLabels:["GPT-5 mini","GPT-4.1","Sonnet","Opus (Copilot \u2153 rate)"]},{id:"cur",name:"Cursor",color:"#5CB85C",baseCost:t=>t*40,includedCredits:t=>t*20,rates:[{input:1.25,output:6},{input:1.25,output:6},{input:3,output:15},{input:15,output:75}],rateLabels:["Auto","Auto","Max Sonnet","Max Opus (full rate)"]}];function B(t){let{opusPct:n}=t,r=1-n;return[M[0]/z*r,M[1]/z*r,M[2]/z*r,n]}function W(t,n){let{engineers:r,tasksPerDay:f,workingDays:l,cacheHitRate:g}=n,h=r*f*l,$=B(n),u=L.map((i,s)=>{let a=Math.round(h*$[s]),p=a*i.inputK/1e3,m=a*i.outputK/1e3,C=t.rates[s],E;if(C.cachedInput!==void 0&&t.id==="cc"&&s>0){let S=p*g*C.cachedInput,H=p*(1-g)*C.input;E=S+H+m*C.output}else E=p*C.input+m*C.output;return{tasks:a,inputM:p,outputM:m,tokenCost:E}}),c=u.reduce((i,s)=>i+s.tokenCost,0),b=t.baseCost(r),e=t.includedCredits(r),d=Math.max(0,c-e),o=b-e+c;return{tiers:u,tokenTotal:c,baseCost:b,credits:e,total:o}}function k(t){return"$"+Math.round(t).toLocaleString("en-GB")}function I(t){return Math.round(t*100)+"%"}function q(t,n){let r=Math.max(...t.map(c=>c.total))*1.1,f=320,l=140,g=64,h=24,$=(f-(x.length*g+(x.length-1)*h))/2,u=`<svg viewBox="0 0 ${f} ${l}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:${f}px;display:block;margin:0 auto;">`;for(let c=0;c<=4;c++){let b=10+c/4*(l-50),e=Math.round(r*(1-c/4));u+=`<line x1="0" y1="${b}" x2="${f}" y2="${b}" stroke="#2a2a2a" stroke-width="1"/>`,u+=`<text x="2" y="${b-3}" fill="#666" font-size="8" font-family="Montserrat,sans-serif">$${(e/1e3).toFixed(1)}k</text>`}t.forEach((c,b)=>{let e=x[b],d=r>0?c.total/r*(l-50):0,o=$+b*(g+h),i=l-38-d;u+=`<rect x="${o}" y="${i}" width="${g}" height="${d}" fill="${e.color}" rx="2" opacity="0.85"/>`,u+=`<text x="${o+g/2}" y="${i-5}" fill="${e.color}" font-size="9" font-weight="bold" font-family="Montserrat,sans-serif" text-anchor="middle">${k(c.total)}</text>`,u+=`<text x="${o+g/2}" y="${l-20}" fill="#969696" font-size="8" font-family="Montserrat,sans-serif" text-anchor="middle">${e.name}</text>`}),u+="</svg>",n.innerHTML=u}function T(t){return`text-align:${t};padding:10px 14px;color:#969696;font-family:'Montserrat',sans-serif;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;font-weight:400;background:#111;`}function y(t,n){return`text-align:${t};padding:10px 14px;background:${n};vertical-align:middle;`}function v(t){return`
    <div style="margin-bottom:20px;">
      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px;">
        <label for="${t.id}" style="color:#969696;font-family:'Montserrat',sans-serif;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;">${t.label}</label>
        <span id="${t.id}-val" style="color:#e2e2e2;font-size:15px;font-weight:600;">${t.format(t.value)}</span>
      </div>
      <input type="range" id="${t.id}" min="${t.min}" max="${t.max}" step="${t.step}" value="${t.value}"
        style="width:100%;accent-color:#4A90D9;cursor:pointer;"/>
      ${t.note?`<p style="margin:4px 0 0;color:#555;font-size:11px;">${t.note}</p>`:""}
    </div>`}function G(t){let n=document.getElementById(t);if(!n)return;let r={engineers:10,tasksPerDay:20,workingDays:22,opusPct:.1,cacheHitRate:.4};n.style.cssText="background:#161616;border:1px solid #2a2a2a;padding:28px 28px 20px;font-family:'Georgia','Times New Roman',serif;color:#e2e2e2;",n.innerHTML=`
    <h2 style="font-family:'Playfair Display',Georgia,serif;font-weight:400;font-size:22px;color:#e2e2e2;margin:0 0 6px;">AI Coding Tool Cost Estimator</h2>
    <p style="color:#969696;font-size:14px;margin:0 0 28px;">Real-time cost comparison across GitHub Copilot, Claude Code, and Cursor. Adjust the inputs to match your team's usage pattern.</p>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:8px;">
      ${v({id:"cc-engineers",label:"Engineers",min:1,max:50,step:1,value:r.engineers,format:e=>String(e)})}
      ${v({id:"cc-tasks",label:"Tasks / engineer / day",min:5,max:50,step:1,value:r.tasksPerDay,format:e=>String(e)})}
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px;">
      ${v({id:"cc-opus",label:"Opus planning tasks",min:0,max:.3,step:.01,value:r.opusPct,format:I,note:"Share of tasks using Opus for design / architecture"})}
      ${v({id:"cc-cache",label:"Claude Code cache hit rate",min:0,max:.8,step:.05,value:r.cacheHitRate,format:I,note:"Repeated file reads within a session billed at ~10% of standard rate"})}
    </div>

    <div style="border-top:1px solid #2a2a2a;padding-top:24px;margin-bottom:20px;">
      <p style="font-family:'Montserrat',sans-serif;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#969696;margin:0 0 16px;">Estimated monthly cost</p>
      <div id="cc-chart" data-chart style="margin-bottom:20px;"></div>
      <div id="cc-results"></div>
    </div>

    <details style="border-top:1px solid #2a2a2a;padding-top:16px;margin-top:4px;">
      <summary style="cursor:pointer;color:#555;font-family:'Montserrat',sans-serif;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;list-style:none;">Model assumptions</summary>
      <div id="cc-assumptions" style="margin-top:14px;"></div>
    </details>

    <p style="margin:20px 0 0;font-size:11px;color:#444;">
      Estimates only. Task mix: 40% simple / 35% medium / 15% complex + Opus planning %. Context per task: 15k\u201380k input tokens, 1k\u201310k output tokens. Working days: ${r.workingDays}/month.
    </p>
  `;let f=n.querySelector("#cc-results"),l=n.querySelector("#cc-chart"),g=n.querySelector("#cc-assumptions"),h={...r};function $(){let e=`<table style="width:100%;border-collapse:collapse;font-size:12px;">
      <thead><tr style="border-bottom:1px solid #2a2a2a;">
        <th style="${T("left")}">Tier</th>
        <th style="${T("right")}">Claude Code</th>
        <th style="${T("right")}">Copilot</th>
        <th style="${T("right")}">Cursor</th>
      </tr></thead><tbody>`;L.forEach((d,o)=>{let i=o%2===0?"#1a1a1a":"#1e1e1e";e+=`<tr><td style="${y("left",i)};color:#969696;">${d.label}</td>`,x.forEach(s=>{let a=s.rates[o],p=s.rateLabels[o],m=a.cachedInput&&s.id==="cc"?` (cached $${a.cachedInput})`:"";e+=`<td style="${y("right",i)};color:#666;font-size:11px;">${p}<br>$${a.input}/$${a.output}/M${m}</td>`}),e+="</tr>"}),e+="</tbody></table>",g.innerHTML=e}function u(){let e=x.map(i=>W(i,h)),d=Math.min(...e.map(i=>i.total));q(e,l);let o=c(e,d);f.innerHTML=o,$()}function c(e,d){let o=`<div style="overflow-x:auto;margin-bottom:16px;">
      <table style="width:100%;border-collapse:collapse;font-size:13px;">
        <thead><tr style="border-bottom:2px solid #2a2a2a;">
          <th style="${T("left")}">Tier</th>`;x.forEach((s,a)=>{let p=e[a].total===d;o+=`<th style="${T("right")}"><span style="color:${s.color};font-weight:600;">${s.name}</span>${p?' <span style="color:#f0ad4e;font-size:10px;">\u2605</span>':""}</th>`}),o+="</tr></thead><tbody>",L.forEach((s,a)=>{let p=a%2===0?"#1e1e1e":"#242424";o+=`<tr style="border-bottom:1px solid #2a2a2a;">
        <td style="${y("left",p)}">
          <span style="color:#e2e2e2;">${s.label}</span>
          <br><span style="color:#444;font-size:11px;">${x.map(m=>m.rateLabels[a]).join(" \xB7 ")}</span>
        </td>`,e.forEach(m=>{o+=`<td style="${y("right",p)}">${k(m.tiers[a].tokenCost)}</td>`}),o+="</tr>"});let i="#1a1a1a";return o+=`<tr style="border-top:1px solid #444;">
      <td style="${y("left",i)};color:#555;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Token total</td>`,e.forEach(s=>{o+=`<td style="${y("right",i)};color:#555;">${k(s.tokenTotal)}</td>`}),o+="</tr>",o+=`<tr><td style="${y("left","#1e1e1e")};color:#555;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Plan / credits</td>`,e.forEach((s,a)=>{let p=s.baseCost-s.credits,m=p>0?`+${k(p)} platform`:s.credits>0?`\u2212${k(s.credits)} credits`:"API billing only";o+=`<td style="${y("right","#1e1e1e")};color:#555;font-size:11px;">${m}</td>`}),o+="</tr>",o+=`<tr><td style="${y("left","#111")};font-weight:700;font-size:13px;text-transform:uppercase;letter-spacing:1px;">Total / month</td>`,e.forEach((s,a)=>{let m=s.total===d?"#f0ad4e":x[a].color;o+=`<td style="${y("right","#111")};font-weight:700;font-size:16px;color:${m};">${k(s.total)}</td>`}),o+="</tr></tbody></table></div>",o+='<p style="font-size:11px;color:#444;margin:0;">\u2605 lowest cost at current settings &nbsp;\xB7&nbsp; Copilot Opus rate is ~\u2153 of direct API price &nbsp;\xB7&nbsp; Claude Code costs reflect prompt caching</p>',o}[{id:"cc-engineers",key:"engineers"},{id:"cc-tasks",key:"tasksPerDay"},{id:"cc-opus",key:"opusPct"},{id:"cc-cache",key:"cacheHitRate"}].forEach(({id:e,key:d})=>{let o=n.querySelector(`#${e}`),i=n.querySelector(`#${e}-val`),s=d==="engineers"||d==="tasksPerDay"?String:I;o.addEventListener("input",()=>{let a=parseFloat(o.value);h[d]=a,i.textContent=s(a),u()})}),$(),u()}return O(j);})();
