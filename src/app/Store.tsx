import React,{createContext,useCallback,useContext,useEffect,useRef,useState} from 'react';
import type { Answer, ExamAttempt, ExamConfig, ExamSession, Mastery, Question } from '../domain/types';
import { createSession, elapsed, finalize, isTimedOut } from '../domain/engine';
import {loadActive,loadAttempts,loadMastery,saveActive,saveAttempt,saveMastery,clearProgress} from '../lib/persistence';
type Store={session:ExamSession|null;attempts:ExamAttempt[];mastery:Mastery;warning:string;clearWarning:()=>void;
 start:(config:ExamConfig,items:Question[])=>ExamSession|null; update:(f:(s:ExamSession)=>ExamSession)=>void; complete:(reason?:'submitted'|'timeout')=>ExamAttempt|null; abandon:()=>void; setCard:(id:string,status:'known'|'again')=>void; clearAll:()=>void};
const Context=createContext<Store|null>(null);
export const useStudy=()=>{const x=useContext(Context);if(!x)throw new Error('Study store not provided');return x;};
export function StudyProvider({children}:{children:React.ReactNode}){
 const [session,setSession]=useState<ExamSession|null>(()=>loadActive());const current=useRef(session);current.current=session;
 const [attempts,setAttempts]=useState<ExamAttempt[]>(()=>loadAttempts());
 const [mastery,setMastery]=useState<Mastery>(()=>loadMastery());
 const [warning,setWarning]=useState('');
 const clearWarning=useCallback(()=>setWarning(''),[]);
 const update=useCallback((f:(s:ExamSession)=>ExamSession)=>{
  const old=current.current;if(!old||isTimedOut(old))return;
  const next={...f(old),updatedAt:Date.now()};current.current=next;setSession(next);
  if(!saveActive(next))setWarning('Progress could not be saved in this browser. A refresh may lose your latest changes.');
 },[]);
 const start=useCallback((config:ExamConfig,items:Question[]):ExamSession|null=>{
  if(current.current){setWarning('Finish or abandon your current exam before starting another.');return null;}
  const s=createSession(config,items);current.current=s;setSession(s);
  if(!saveActive(s))setWarning('Your exam started, but this browser is not saving progress.');
  return s;
 },[]);
 const complete=useCallback((reason:'submitted'|'timeout'='submitted'):ExamAttempt|null=>{
  const s=current.current;if(!s)return null;
  const finalReason=isTimedOut(s)?'timeout':reason;
  const result=finalize(s,finalReason);
  if(!saveAttempt(result)){setWarning('Could not save your exam result. Free browser storage and retry.');return null;}
  setAttempts(loadAttempts());current.current=null;setSession(null);
  if(!saveActive(null))setWarning('Result saved, but could not clear the active session.');
  return result;
 },[]);
 const abandon=useCallback(()=>{current.current=null;setSession(null);if(!saveActive(null))setWarning('Unable to clear saved session.');},[]);
 const setCard=useCallback((id:string,status:'known'|'again')=>{setMastery(m=>{const next={...m,[id]:status};if(!saveMastery(next))setWarning('Could not save flashcard progress.');return next;});},[]);
 const clearAll=useCallback(()=>{if(clearProgress()){current.current=null;setSession(null);setAttempts([]);setMastery({});setWarning('');}else setWarning('Could not completely clear local data. Check your browser settings.');},[]);
 useEffect(()=>{
  const timer=window.setInterval(()=>{if(current.current&&isTimedOut(current.current))complete('timeout');},700);
  if(current.current&&isTimedOut(current.current))complete('timeout');
  const onStorage=(event:StorageEvent)=>{
   if(event.key==='studyspace:v1:attempts')setAttempts(loadAttempts());
   if(event.key==='studyspace:v1:flashcards')setMastery(loadMastery());
   if(event.key==='studyspace:v1:active-session'){
    const incoming=loadActive();if(incoming?.id!==current.current?.id || (incoming&&current.current&&incoming.updatedAt>current.current.updatedAt)){
      current.current=incoming;setSession(incoming);setWarning('This session was updated in another tab. Latest browser-saved version is now shown.');
    }
   }
  };
  window.addEventListener('storage',onStorage);
  return()=>{window.clearInterval(timer);window.removeEventListener('storage',onStorage);};
 },[complete]);
 return <Context.Provider value={{session,attempts,mastery,warning,clearWarning,start,update,complete,abandon,setCard,clearAll}}>{children}</Context.Provider>;
}
export function pauseSession(s:ExamSession):ExamSession{if(s.config.mode!=='practice'||s.status==='paused')return s;const now=Date.now();return {...s,status:'paused',timing:{...s.timing,elapsedBeforeMs:elapsed(s,now),resumedAt:null}};}
export function resumeSession(s:ExamSession):ExamSession{if(s.status!=='paused')return s;return {...s,status:'active',timing:{...s.timing,resumedAt:Date.now()}};}
