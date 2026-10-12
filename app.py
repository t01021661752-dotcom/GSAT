import hashlib
import json

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="GSAT 시험창", page_icon="⏱️", layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
      .block-container {padding-top: 0.6rem; padding-bottom: 0; max-width: 1400px;}
      .block-container iframe {height: calc(100vh - 1.6rem) !important;}
      .block-container .stElementContainer:has(iframe),
      .block-container [data-testid="stElementContainer"]:has(iframe) {height: auto !important;}
      header[data-testid="stHeader"], [data-testid="stSidebar"],
      [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"],
      [data-testid="stToolbar"], [data-testid="stMainMenu"] {display: none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

SECTIONS = [
    {"name": "수리", "count": 20, "minutes": 30},
    {"name": "추리", "count": 30, "minutes": 30},
]

cfg = {"sections": SECTIONS, "sound": True}
cfg_key = hashlib.md5(json.dumps(SECTIONS, ensure_ascii=False).encode()).hexdigest()[:10]

TEMPLATE = r"""
<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=IBM+Plex+Mono:wght@500;600&display=swap">
<style>
:root{
  --bg:#f4f6f9; --panel:#ffffff; --ink:#1f2733; --muted:#6b7686; --line:#dde2ea;
  --navy:#1b2a44; --accent:#2563eb; --accent-soft:#e6eefc;
  --warn:#d97706; --crit:#dc2626; --ok:#16a34a; --flag:#eab308;
  --sans:"Noto Sans KR",-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:14px}
button{font:inherit;cursor:pointer;color:inherit}
button:focus-visible,textarea:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
html,body{height:100%;overflow:hidden}
.wrap{height:100%;display:flex;flex-direction:column;gap:10px;padding:2px}
.timer{flex:none}
.scroll{flex:1;min-height:0;overflow-y:auto;display:grid;gap:12px;align-content:start;padding:0 2px 16px 0}

/* timer */
.timer{background:var(--navy);color:#f3f6fb;border-radius:10px;padding:12px 16px;display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.chip{font-size:13px;padding:4px 10px;border-radius:5px;border:1px solid #ffffff33;color:#a9b6cc}
.chip.on{background:#f3f6fb;color:var(--navy);border-color:#f3f6fb;font-weight:700}
.chip.done{text-decoration:line-through;opacity:.7}
.clock{display:flex;flex-direction:column;align-items:flex-start;line-height:1.1}
.time{font-family:var(--mono);font-size:44px;font-weight:600;font-variant-numeric:tabular-nums;letter-spacing:.02em}
.time.warn{color:#fbbf24}.time.crit{color:#f87171}
.sub{font-size:12px;color:#a9b6cc;font-variant-numeric:tabular-nums}
.ctrl{display:flex;gap:8px;margin-left:auto;flex-wrap:wrap}
.tb{border:1px solid #ffffff44;background:transparent;color:#f3f6fb;border-radius:6px;padding:9px 16px;font-weight:500}
.tb:hover{background:#ffffff14}
.tb.go{background:#f3f6fb;color:var(--navy);border-color:#f3f6fb;font-weight:700;min-width:84px}
.tb.go.stop{background:#f87171;border-color:#f87171;color:#fff}
.prog{flex-basis:100%;height:4px;background:#ffffff1f;border-radius:2px;overflow:hidden}
.prog i{display:block;height:100%;width:0;background:#60a5fa}
.prog i.warn{background:#fbbf24}.prog i.crit{background:#f87171}
.banner{flex-basis:100%;font-size:13px;color:#fde68a}

/* omr: 10문항씩 세로 블록을 나란히 */
#omr{display:grid;gap:12px;justify-items:start}
.sec{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 12px;min-width:0}
.sec-h{display:flex;align-items:baseline;gap:10px;margin-bottom:8px}
.sec-h b{font-size:15px}
.sec-h span{color:var(--muted);font-size:12px;font-variant-numeric:tabular-nums}
.blocks{display:block}
.blk{border:1px solid #b8c1cf;border-radius:6px;overflow:hidden}
.r{display:grid;grid-template-columns:38px repeat(5,30px) 28px;align-items:center;border-bottom:1px solid var(--line);height:34px}
.r:last-child{border-bottom:0}
.r.cur{background:var(--accent-soft)}
.qn{height:100%;border:0;border-right:1px solid var(--line);background:#f7f8fb;font-family:var(--mono);font-weight:600;font-size:13px;padding:0}
.r.cur .qn{background:var(--accent);color:#fff}
.r.x .qn{background:#fee2e2;color:var(--crit)}
.r.o .qn{background:#dcfce7;color:var(--ok)}
.bub{justify-self:center;width:24px;height:24px;border-radius:50%;border:1.5px solid #9aa6b8;background:#fff;font-family:var(--mono);font-size:12px;font-weight:600;color:#6b7686;padding:0;display:grid;place-items:center}
.bub:hover{border-color:var(--accent);color:var(--accent)}
.bub.on{background:var(--accent);border-color:var(--accent);color:#fff}
.bub.key{box-shadow:0 0 0 2px var(--ok)}
.flag{height:100%;border:0;border-left:1px solid var(--line);background:transparent;color:#c3cad6;font-weight:700;padding:0}
.flag.on{color:#a16207;background:#fef9c3}

.hint{font-size:12px;color:var(--muted);display:flex;gap:14px;flex-wrap:wrap}
kbd{font-family:var(--mono);font-size:11px;border:1px solid var(--line);border-bottom-width:2px;border-radius:3px;padding:0 5px;background:#fff}

/* grading */
details{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px}
summary{font-weight:700;cursor:pointer}
.g{display:grid;gap:12px;margin-top:10px}
.g label{font-size:13px;color:var(--muted)}
.g textarea{width:100%;min-height:44px;font-family:var(--mono);font-size:14px;letter-spacing:.08em;padding:8px;border:1px solid var(--line);border-radius:6px;resize:vertical}
.score{display:flex;gap:16px;flex-wrap:wrap;font-size:14px;font-variant-numeric:tabular-nums}
.score .c{color:var(--ok);font-weight:700}.score .w{color:var(--crit);font-weight:700}
.wrong{font-size:13px;color:var(--muted)}
.gbtn{border:0;background:var(--accent);color:#fff;border-radius:6px;padding:8px 16px;font-weight:700;justify-self:start}
.ghost{border:1px solid var(--line);background:#fff;border-radius:6px;padding:8px 14px}
.row{display:flex;gap:8px;flex-wrap:wrap}
</style></head>
<body>
<div class="wrap">
  <div class="timer">
    <div class="chips" id="chips"></div>
    <div class="clock">
      <span class="time" id="time">30:00</span>
      <span class="sub" id="sub">경과 00:00 / 30:00</span>
    </div>
    <div class="ctrl">
      <button class="tb go" id="go" type="button">시작</button>
      <button class="tb" id="reset" type="button">리셋</button>
      <button class="tb" id="clearAns" type="button">답안 초기화</button>
    </div>
    <div class="prog"><i id="prog"></i></div>
    <div class="banner" id="banner" hidden></div>
  </div>

  <div class="scroll" id="scroll">
  <div id="omr"></div>

  <div class="hint"><span>현재 문항: <kbd>1</kbd>~<kbd>5</kbd> 마킹 후 다음 문항</span><span><kbd>↑</kbd><kbd>↓</kbd> 이동</span><span><kbd>Space</kbd> 체크(?)</span><span><kbd>Backspace</kbd> 지우기</span><span>같은 답을 다시 누르면 취소</span></div>

  <details id="gradeBox">
    <summary>정답 입력 · 채점</summary>
    <div class="g" id="grade"></div>
  </details>
  </div>
</div>

<script>
const CFG = __CFG__;
const KEY = "gsat-omr-" + "__KEY__";
const SECS = CFG.sections;
const $ = id => document.getElementById(id);

function fresh(){return{secIdx:0,running:false,startAt:0,acc:SECS.map(()=>0),done:SECS.map(()=>false),
  ans:SECS.map(s=>Array(s.count).fill(0)),flag:SECS.map(s=>Array(s.count).fill(false)),
  keys:SECS.map(()=>""),graded:false,cur:0,beeped:{}}}
let S; try{S=JSON.parse(localStorage.getItem(KEY))}catch(e){}
if(!S||!S.ans||S.ans.length!==SECS.length)S=fresh();
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}};

const fmt=s=>{s=Math.max(0,Math.ceil(s));return String(Math.floor(s/60)).padStart(2,"0")+":"+String(s%60).padStart(2,"0")};
const limit=i=>SECS[i].minutes*60;
const elapsed=i=>S.acc[i]+(S.running&&i===S.secIdx?(Date.now()-S.startAt)/1000:0);

let ac=null;
function audio(){try{ac=ac||new (window.AudioContext||window.webkitAudioContext)();ac.resume()}catch(e){}}
function beep(n){if(!CFG.sound||!ac)return;try{for(let k=0;k<n;k++){const o=ac.createOscillator(),g=ac.createGain();o.frequency.value=880;o.connect(g);g.connect(ac.destination);const t=ac.currentTime+k*.35;g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(.3,t+.02);g.gain.exponentialRampToValueAtTime(.0001,t+.25);o.start(t);o.stop(t+.27)}}catch(e){}}

/* ---------- timer ---------- */
function pause(){if(!S.running)return;S.acc[S.secIdx]=elapsed(S.secIdx);S.running=false}
function goToggle(){audio();if(S.done[S.secIdx]){const i=S.secIdx;S.acc[i]=0;S.done[i]=false;delete S.beeped[i+":5"];delete S.beeped[i+":1"];$("banner").hidden=true}if(S.running)pause();else{S.running=true;S.startAt=Date.now()}save();renderTimer()}
function finishSection(auto){
  pause();S.acc[S.secIdx]=Math.min(S.acc[S.secIdx],limit(S.secIdx));S.done[S.secIdx]=true;
  const last=S.secIdx>=SECS.length-1;
  if(!last){S.secIdx++;S.cur=0;}
  $("banner").hidden=false;
  $("banner").textContent=auto
    ?(last?"시간이 끝났습니다. 아래에서 정답을 입력해 채점하세요.":`${SECS[S.secIdx-1].name} 영역 시간이 끝났습니다. 준비되면 [시작]을 눌러 ${SECS[S.secIdx].name} 영역을 시작하세요.`)
    :(last?"시험을 마쳤습니다. 아래에서 채점하세요.":`${SECS[S.secIdx].name} 영역입니다. [시작]을 누르면 시간이 흐릅니다.`);
  if(last)$("gradeBox").open=true;
  save();renderAll();
}
function tick(){
  const i=S.secIdx,e=elapsed(i),rem=limit(i)-e;
  if(S.running){
    const b=i+":";
    if(rem<=300&&rem>298&&!S.beeped[b+5]){S.beeped[b+5]=1;beep(1)}
    if(rem<=60&&rem>58&&!S.beeped[b+1]){S.beeped[b+1]=1;beep(2)}
    if(rem<=0){beep(3);finishSection(true);return}
  }
  renderTimer();
}
function renderTimer(){
  const i=S.secIdx,e=elapsed(i),rem=limit(i)-e,cls=S.done[i]?"":rem<=60?"crit":rem<=300?"warn":"";
  $("time").textContent=fmt(rem);$("time").className="time "+cls;
  $("sub").textContent=`${SECS[i].name} · 경과 ${fmt(e)} / ${fmt(limit(i))}`;
  $("prog").style.width=Math.min(100,e/limit(i)*100)+"%";$("prog").className=cls;
  const g=$("go");g.textContent=S.running?"정지":"시작";g.classList.toggle("stop",S.running);
  $("chips").innerHTML=SECS.map((s,k)=>`<span class="chip ${k===i?"on":S.done[k]?"done":""}">${s.name} ${s.count}문항 · ${s.minutes}분</span>`).join("");
}

/* ---------- OMR ---------- */
function renderOMR(){
  const key=S.keys.map(parseKey);
  $("omr").innerHTML=SECS.map((s,i)=>{
    const a=S.ans[i],n=a.filter(Boolean).length,f=S.flag[i].filter(Boolean).length;
    let blocks="";
    {
      let rows="";
      for(let q=0;q<s.count;q++){
        const k=S.graded?key[i][q]:0,res=k?(a[q]===k?"o":"x"):"";
        rows+=`<div class="r ${i===S.secIdx&&q===S.cur?"cur":""} ${res}" id="c${i}_${q}">
          <button class="qn" type="button" data-s="${i}" data-q="${q}" data-a="cur">${q+1}</button>`;
        for(let v=1;v<=5;v++)rows+=`<button class="bub ${a[q]===v?"on":""} ${k===v&&a[q]!==v?"key":""}" type="button" data-s="${i}" data-q="${q}" data-a="mark" data-v="${v}" aria-label="${s.name} ${q+1}번 ${v}">${v}</button>`;
        rows+=`<button class="flag ${S.flag[i][q]?"on":""}" type="button" data-s="${i}" data-q="${q}" data-a="flag" aria-label="${q+1}번 체크">?</button></div>`;
      }
      blocks+=`<div class="blk">${rows}</div>`;
    }
    return `<div class="sec"><div class="sec-h"><b>${s.name}</b><span>응답 ${n}/${s.count} · 체크 ${f}${S.done[i]?" · 시간 종료":""}</span></div>
      <div class="blocks">${blocks}</div></div>`;
  }).join("");
  const c=$(`c${S.secIdx}_${S.cur}`);if(c)c.scrollIntoView({block:"nearest",inline:"nearest"});
}
function canMark(i){return true}
function mark(i,q,v){if(!canMark(i))return;S.ans[i][q]=S.ans[i][q]===v?0:v;save();renderOMR()}
$("omr").addEventListener("click",e=>{
  const b=e.target.closest("button");if(!b)return;
  const i=+b.dataset.s,q=+b.dataset.q;if(!canMark(i))return;
  if(i===S.secIdx)S.cur=q;
  if(b.dataset.a==="mark")mark(i,q,+b.dataset.v);
  else if(b.dataset.a==="flag"){S.flag[i][q]=!S.flag[i][q];save();renderOMR()}
  else{save();renderOMR()}
});
document.addEventListener("keydown",e=>{
  if(/TEXTAREA|INPUT/.test(e.target.tagName)||e.ctrlKey||e.metaKey||e.altKey)return;
  const i=S.secIdx,n=SECS[i].count;
  if(/^[1-5]$/.test(e.key)){e.preventDefault();if(!canMark(i))return;S.ans[i][S.cur]=+e.key;S.cur=Math.min(n-1,S.cur+1);save();renderOMR()}
  else if((e.key==="ArrowDown"||e.key==="ArrowRight")){e.preventDefault();S.cur=Math.min(n-1,S.cur+1);renderOMR()}
  else if((e.key==="ArrowUp"||e.key==="ArrowLeft")){e.preventDefault();S.cur=Math.max(0,S.cur-1);renderOMR()}
  else if(e.key===" "){e.preventDefault();if(canMark(i)){S.flag[i][S.cur]=!S.flag[i][S.cur];save();renderOMR()}}
  else if(e.key==="Backspace"||e.key==="Delete"){e.preventDefault();if(canMark(i)){S.ans[i][S.cur]=0;save();renderOMR()}}
});

/* ---------- grading ---------- */
const parseKey=t=>(t||"").replace(/[^1-5]/g,"").split("").map(Number);
function renderGrade(){
  const key=S.keys.map(parseKey);let totC=0,totN=0;
  const body=SECS.map((s,i)=>{
    let res="";
    if(S.graded&&key[i].length){
      let c=0;const w=[];
      for(let q=0;q<s.count;q++){if(!key[i][q])continue;if(S.ans[i][q]===key[i][q])c++;else w.push(`${q+1}번(내 답 ${S.ans[i][q]||"-"} / 정답 ${key[i][q]})`)}
      totC+=c;totN+=s.count;
      res=`<div class="score"><span>정답 <span class="c">${c}개</span></span><span>오답 <span class="w">${s.count-c}개</span></span><span>총 ${s.count}문항</span><span>사용 시간 ${fmt(elapsed(i))}</span></div>
        ${w.length?`<div class="wrong">틀린 문제: ${w.join(", ")}</div>`:""}`;
    }
    return `<div class="g" style="margin:0"><label for="k${i}">${s.name} 정답 ${s.count}개 (예: 1,2,3,4,5 또는 12345)</label>
      <textarea id="k${i}" data-i="${i}">${S.keys[i]}</textarea>${res}</div>`;
  }).join("");
  const total=S.graded&&totN?`<div class="score" style="font-size:16px"><b>총점 ${totC} / ${totN} (${Math.round(totC/totN*100)}점)</b></div>`:"";
  $("grade").innerHTML=body+total+`<div class="row"><button class="gbtn" id="doGrade" type="button">채점하기</button><button class="ghost" id="clearAll" type="button">답안 전체 초기화</button></div>`;
}
$("grade").addEventListener("input",e=>{if(e.target.dataset.i!==undefined){S.keys[+e.target.dataset.i]=e.target.value;save()}});
let confirmClear=false;
$("grade").addEventListener("click",e=>{
  if(e.target.id==="doGrade"){S.graded=true;save();renderGrade();renderOMR()}
  if(e.target.id==="clearAll"){
    if(!confirmClear){confirmClear=true;e.target.textContent="한 번 더 누르면 마킹·타이머가 모두 지워집니다";return}
    const keys=S.keys;S=fresh();S.keys=keys;confirmClear=false;$("banner").hidden=true;save();renderAll();
  }
});

/* ---------- controls ---------- */
$("go").onclick=goToggle;
let confirmAns=false;
$("clearAns").onclick=()=>{
  if(!confirmAns){confirmAns=true;$("clearAns").textContent="한 번 더 누르면 삭제";setTimeout(()=>{confirmAns=false;$("clearAns").textContent="답안 초기화"},2500);return}
  confirmAns=false;$("clearAns").textContent="답안 초기화";
  S.ans=SECS.map(s=>Array(s.count).fill(0));S.flag=SECS.map(s=>Array(s.count).fill(false));S.graded=false;S.cur=0;
  save();renderOMR();renderGrade();
};
let confirmReset=false;
$("reset").onclick=()=>{
  if(!confirmReset){confirmReset=true;$("reset").textContent="리셋 확인";setTimeout(()=>{confirmReset=false;$("reset").textContent="리셋"},2500);return}
  confirmReset=false;$("reset").textContent="리셋";
  S.running=false;S.acc[S.secIdx]=0;S.done[S.secIdx]=false;S.beeped={};$("banner").hidden=true;save();renderAll();
};

function renderAll(){renderTimer();renderOMR();renderGrade()}
renderAll();
setInterval(tick,250);
</script>
</body></html>
"""

html = TEMPLATE.replace("__CFG__", json.dumps(cfg, ensure_ascii=False)).replace("__KEY__", cfg_key)
height = 800  # 실제 높이는 위 CSS에서 브라우저 창 높이에 맞춤
if hasattr(st, "iframe"):
    st.iframe(html, height=height)
else:
    components.html(html, height=height, scrolling=True)
