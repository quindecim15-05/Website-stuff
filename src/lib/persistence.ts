import type { ExamAttempt, ExamSession, Mastery } from '../domain/types';
const prefix='studyspace:v1:';
const get=<T,>(key:string,fallback:T):T=>{try{const raw=localStorage.getItem(prefix+key);return raw?JSON.parse(raw) as T:fallback;}catch{return fallback;}};
const put=(key:string,data:unknown):boolean=>{try{localStorage.setItem(prefix+key,JSON.stringify(data));return true;}catch{return false;}};
export const loadActive=():ExamSession|null=>{
 const s=get<ExamSession|null>('active-session',null);
 return s&&s.schemaVersion===1&&typeof s.id==='string'&&Array.isArray(s.questions)&&Array.isArray(s.checked)&&Array.isArray(s.flags)&&s.timing&&typeof s.timing.startedAt==='number'&&typeof s.timing.elapsedBeforeMs==='number'&&s.answers&&typeof s.answers==='object'?s:null;
};
export const saveActive=(s:ExamSession|null):boolean=>s?put('active-session',s):remove('active-session');
const remove=(key:string)=>{try{localStorage.removeItem(prefix+key);return true;}catch{return false;}};
export const loadAttempts=():ExamAttempt[]=>{const attempts=get<ExamAttempt[]>('attempts',[]);return Array.isArray(attempts)?attempts.filter(a=>a&&typeof a.id==='string'&&Array.isArray(a.questions)&&Array.isArray(a.correctIds)&&a.answers&&typeof a.answers==='object'):[];};
export const saveAttempt=(a:ExamAttempt):boolean=>{const attempts=loadAttempts();if(attempts.some(x=>x.id===a.id))return true;return put('attempts',[a,...attempts]);};
export const loadMastery=():Mastery=>{const m=get<Mastery>('flashcards',{});return m&&typeof m==='object'&&!Array.isArray(m)?m:{};};
export const saveMastery=(m:Mastery)=>put('flashcards',m);
export const clearProgress=()=>['active-session','attempts','flashcards','preferences'].map(k=>remove(k)).every(Boolean);
