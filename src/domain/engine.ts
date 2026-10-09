import type { Answer, ExamAttempt, ExamConfig, ExamSession, Question } from './types';
export const normalize = (v:string) => v.normalize('NFKC').trim().replace(/\s+/g,' ').toLocaleLowerCase('en');
export function grade(question:Question, answer:Answer | undefined):boolean {
  if (answer === undefined || answer === '') return false;
  switch(question.type){
    case 'multiple-choice': case 'code-analysis': return typeof answer==='string' && answer===question.correctOptionId;
    case 'true-false': return typeof answer==='boolean' && answer===question.correctBoolean;
    case 'identification': return typeof answer==='string' && !!question.acceptedAnswers?.some(a=>normalize(a)===normalize(answer));
  }
}
export const answerText = (q:Question, answer:Answer|undefined):string => {
 if(answer===undefined||answer==='')return 'Not answered';
 if(typeof answer==='boolean')return answer?'True':'False';
 if(q.type==='identification')return answer;
 return q.options?.find(o=>o.id===answer)?.text ?? String(answer);
};
export const correctText = (q:Question):string => q.type==='true-false'?(q.correctBoolean?'True':'False'):q.type==='identification'?(q.acceptedAnswers?.join(' / ')??''):q.options?.find(o=>o.id===q.correctOptionId)?.text ?? '';
export function candidatePool(all:Question[], config:ExamConfig):Question[]{
 return all.filter(q=>q.verificationStatus==='verified' && config.types.includes(q.type) && (config.difficulty==='mixed'||q.difficulty===config.difficulty) && (config.coverage==='topic'?q.topicId===config.topicId:config.coverage==='subject'?q.subjectId===config.subjectIds[0]:config.subjectIds.includes(q.subjectId)));
}
function random(seed:number){ let a=seed>>>0; return ()=>{a+=0x6D2B79F5;let t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return ((t^(t>>>14))>>>0)/4294967296;}; }
function shuffle<T>(items:T[],rnd:()=>number):T[]{let a=[...items];for(let i=a.length-1;i>0;i--){let j=Math.floor(rnd()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
export function selectQuestions(pool:Question[],count:number,seed:number):Question[]{
 const rnd=random(seed);
 // Stable question IDs, broad subject/topic coverage before filling remaining slots.
 const byTopic=new Map<string,Question[]>();
 for(const q of shuffle(pool,rnd)){let group=byTopic.get(q.topicId)||[];group.push(q);byTopic.set(q.topicId,group);}
 const keys=shuffle([...byTopic.keys()],rnd);const chosen:Question[]=[];
 while(chosen.length<Math.min(count,pool.length)){
  let changed=false;
  for(const k of keys){let q=byTopic.get(k)?.shift();if(q){chosen.push(q);changed=true;if(chosen.length>=Math.min(count,pool.length))break;}}
  if(!changed)break;
 }
 return shuffle(chosen,rnd).map(q=>({...q,options:q.options?shuffle(q.options,rnd):undefined}));
}
export const isTimedOut=(session:ExamSession,now=Date.now())=>session.config.mode==='mock' && session.timing.deadlineAt!==null && now>=session.timing.deadlineAt;
export const elapsed=(s:ExamSession,now=Date.now())=>s.timing.elapsedBeforeMs+(s.timing.resumedAt!==null?Math.max(0,now-s.timing.resumedAt):0);
export function createSession(config:ExamConfig,chosen:Question[],now=Date.now()):ExamSession{
 const uuid=typeof crypto!=='undefined'&&'randomUUID'in crypto?crypto.randomUUID():`${now}-${Math.random().toString(36).slice(2)}`;
 return {schemaVersion:1,id:uuid,config,status:'active',reviewing:false,questions:chosen,answers:{},checked:[],flags:[],position:0,timing:{startedAt:now,deadlineAt:config.mode==='mock'&&config.timerMin>0?now+config.timerMin*60_000:null,elapsedBeforeMs:0,resumedAt:now},updatedAt:now};
}
export function finalize(s:ExamSession,reason:'submitted'|'timeout',now=Date.now()):ExamAttempt{
 const cutoff=reason==='timeout'&&s.timing.deadlineAt?Math.min(now,s.timing.deadlineAt):now;
 const correctIds=s.questions.filter(q=>(s.config.mode!=='practice'||s.checked.includes(q.id))&&grade(q,s.answers[q.id])).map(q=>q.id);
 return {id:s.id,sessionId:s.id,config:s.config,questions:s.questions,answers:{...s.answers},flags:[...s.flags],correctIds,score:correctIds.length,percent:s.questions.length?correctIds.length/s.questions.length*100:0,startedAt:s.timing.startedAt,submittedAt:cutoff,elapsedMs:Math.min(elapsed(s,cutoff),Math.max(0,cutoff-s.timing.startedAt)),reason};
}
export const initialConfig:ExamConfig={coverage:'subject',subjectIds:['dcit50'],topicId:'',mode:'mock',count:30,difficulty:'mixed',types:['multiple-choice','true-false','identification','code-analysis'],timerMin:30};
