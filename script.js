(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const menu = document.querySelector('.menu-toggle');
  const nav = document.getElementById('site-nav');
  const closeMenu = () => { menu.setAttribute('aria-expanded','false'); nav.classList.remove('is-open'); };
  menu.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') !== 'true'; menu.setAttribute('aria-expanded',String(open)); nav.classList.toggle('is-open',open); });
  nav.querySelectorAll('a').forEach(a => a.addEventListener('click',closeMenu));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { closeMenu(); menu.focus(); } });
  const themes = {
    consistent: {number:'C / Consistency & introspection',title:'From evidence to reliable decisions.',description:'How can an agent revise its beliefs when evidence changes, explain what influenced its decisions, and carry what it knows into consistent actions?',topics:['Factual and behavioral consistency','Context attribution and provenance','Memory, belief revision, and action alignment'],connection:'Consistency gives adaptation a foundation: new experience should change the right beliefs without erasing valid commitments.'},
    adaptive: {number:'A / Learning through interaction',title:'Experience that becomes learning.',description:'When does feedback lead to genuine improvement? I study learning from teachers, other agents, and experience—and whether those gains transfer and persist.',topics:['Textual feedback and post-training','Teacher–student and multi-agent learning','Transfer, retention, and continual adaptation'],connection:'Adaptation must earn its gains: learning should be distinguished from extra search, selection, or overfitting an evaluator.'},
    strategic: {number:'S / Reasoning & interaction',title:'Thinking beyond the next step.',description:'How can agents investigate, plan, and collaborate under uncertainty? My work connects reasoning with persuasion, debate, and decisions over long interactions.',topics:['Evidence-grounded reasoning and exploration','Collaborative reasoning and cross teaching','Persuasion, debate, and strategic interaction'],connection:'Strategic capability should support truthful, useful cooperation and preserve the interests and agency of the people involved.'},
    trustworthy: {number:'T / AI auditability & safety',title:'Capability with accountability.',description:'How do we know when an agent can be trusted to act? I study auditing, adversarial robustness, and evaluation that examines behavior across an entire interaction.',topics:['Prompt-injection defense and robust tool use','Trajectory auditing and evaluator reliability','Safety, recoverability, and human control'],connection:'Trustworthiness connects the whole system: its evidence, memory, decisions, tools, and ability to recognize and recover from failure.'}
  };
  const nodes = [...document.querySelectorAll('[data-theme]')];
  function selectTheme(button) {
    const theme = themes[button.dataset.theme];
    if (!theme) return;
    nodes.forEach(n => { const active=n===button; n.classList.toggle('is-active',active); n.setAttribute('aria-pressed',String(active)); });
    document.getElementById('theme-number').textContent=theme.number;
    document.getElementById('theme-title').textContent=theme.title;
    document.getElementById('theme-description').textContent=theme.description;
    document.getElementById('theme-connection').textContent=theme.connection;
    document.getElementById('theme-topics').replaceChildren(...theme.topics.map(t=>{const li=document.createElement('li');li.textContent=t;return li;}));
  }
  nodes.forEach((node,index) => {
    node.addEventListener('click',()=>selectTheme(node));
    node.addEventListener('keydown', e => {
      let next;
      if (e.key==='ArrowRight'||e.key==='ArrowDown') next=(index+1)%nodes.length;
      if (e.key==='ArrowLeft'||e.key==='ArrowUp') next=(index+nodes.length-1)%nodes.length;
      if (e.key==='Home') next=0;
      if (e.key==='End') next=nodes.length-1;
      if(next!==undefined){e.preventDefault();nodes[next].focus();selectTheme(nodes[next]);}
    });
  });
  const map=document.querySelector('.cast-visual');
  const motionButton=document.getElementById('motion-toggle');
  const preference=window.matchMedia('(prefers-reduced-motion: reduce)');
  if (map && motionButton) {
  let userPaused=false;
  function updateMotion(){
    const paused=userPaused||preference.matches;
    map.classList.toggle('motion-paused',paused);
    motionButton.setAttribute('aria-pressed',String(paused));
    motionButton.textContent=preference.matches?'Reduced motion enabled':paused?'Play motion ▷':'Pause motion Ⅱ';
    motionButton.disabled=preference.matches;
  }
  motionButton.addEventListener('click',()=>{userPaused=!userPaused;updateMotion();});
  preference.addEventListener('change',updateMotion); updateMotion();
  }
  const journey=document.querySelector('.journey-widget');
  if(journey){
    const buttons=[...journey.querySelectorAll('[data-stage]')];
    const descriptions=['Ask a question worth pursuing.','Build understanding through study and feedback.','Test ideas through practice and observation.','Create something new—and ask the next question.'];
    const detail=document.getElementById('journey-detail');
    const control=document.getElementById('journey-motion');
    const ball=journey.querySelector('.journey-ball');
    let paused=false;
    let activeStage=0;
    function highlight(stage,announce=false){
      activeStage=stage;
      buttons.forEach(b=>{const on=Number(b.dataset.stage)===stage;b.classList.toggle('is-active',on);b.setAttribute('aria-pressed',String(on));});
      detail.setAttribute('aria-live',announce?'polite':'off');
      detail.textContent=descriptions[stage];
    }
    function motion(){
      const stopped=paused||preference.matches;
      journey.classList.toggle('journey-paused',stopped);
      control.setAttribute('aria-pressed',String(stopped));
      control.textContent=preference.matches?'Reduced motion enabled':stopped?'Play motion ▷':'Pause motion Ⅱ';
      control.disabled=preference.matches;
      if(preference.matches){ball.style.left=activeStage===1||activeStage===2?'86%':'14%';ball.style.top=activeStage>=2?'82%':'18%';}
    }
    function selectStage(button){
      const stage=Number(button.dataset.stage);
      highlight(stage,true);
      ball.style.animation='none';
      void ball.offsetHeight;
      ball.style.animation='';
      ball.style.animationDelay=`-${stage*3}s`;
      paused=true;motion();
    }
    buttons.forEach((b,i)=>{b.addEventListener('click',()=>selectStage(b));b.addEventListener('keydown',e=>{let n;if(e.key==='ArrowRight'||e.key==='ArrowDown')n=(i+1)%4;if(e.key==='ArrowLeft'||e.key==='ArrowUp')n=(i+3)%4;if(n!==undefined){e.preventDefault();buttons[n].focus();selectStage(buttons[n]);}});});
    control.addEventListener('click',()=>{paused=!paused;detail.setAttribute('aria-live','off');motion();});
    preference.addEventListener('change',motion);motion();
    const synchronize=()=>{
      if(paused||preference.matches||document.hidden||typeof ball.getAnimations!=='function')return;
      const animation=ball.getAnimations()[0];
      const progress=animation?.effect?.getComputedTiming().progress;
      if(progress===undefined||progress===null)return;
      const stage=Math.min(3,Math.floor(progress*4));
      if(stage!==activeStage)highlight(stage);
    };
    const timer=window.setInterval(synchronize,250);
    window.addEventListener('pagehide',()=>window.clearInterval(timer),{once:true});
  }
  document.getElementById('year').textContent=String(new Date().getFullYear());
})();
