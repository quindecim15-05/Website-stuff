import {describe,expect,it} from 'vitest';
import {questions} from '../src/content';
import {candidatePool,createSession,elapsed,finalize,grade,isTimedOut,selectQuestions} from '../src/domain/engine';
import type {ExamConfig} from '../src/domain/types';
const config:ExamConfig={coverage:'subject',subjectIds:['dcit50'],topicId:'',mode:'mock',count:8,timerMin:10,difficulty:'mixed',types:['multiple-choice','true-false','identification','code-analysis']};
describe('StudySpace exam engine',()=>{
 it('supports all four formats and correct answer normalizations',()=>{
  for(const q of questions){let a:qAnswer;
   if(q.type==='true-false')a=q.correctBoolean!;
   else if(q.type==='identification')a='  '+q.acceptedAnswers![0].toUpperCase().replaceAll(' ','  ')+'  ';
   else a=q.correctOptionId!;
   expect(grade(q,a),q.id).toBe(true);
  }
 });
 it('selects unique, deterministic question IDs without changing original data',()=>{
  const pool=candidatePool(questions,config);const a=selectQuestions(pool,8,55);const b=selectQuestions(pool,8,55);
  expect(a.map(q=>q.id)).toEqual(b.map(q=>q.id));expect(new Set(a.map(q=>q.id)).size).toBe(8);
  expect(a.every(q=>q.subjectId==='dcit50')).toBe(true);
 });
 it('never changes the immutable selection on session creation',()=>{
  const picked=selectQuestions(candidatePool(questions,config),8,555);const s=createSession(config,picked,1000);
  expect(s.questions.map(q=>q.id)).toEqual(picked.map(q=>q.id));
 });
 it('enforces deadline at the exact cutoff',()=>{
  const s=createSession(config,selectQuestions(candidatePool(questions,config),8,14),1000);
  expect(isTimedOut(s,1000)).toBe(false);expect(isTimedOut(s,601000)).toBe(true);
  expect(elapsed(s,10000)).toBe(9000);
 });
 it('grades missing answers as zero and preserves frozen result snapshots',()=>{
  const picked=selectQuestions(candidatePool(questions,config),8,55);const s=createSession(config,picked,1000);
  const result=finalize(s,'submitted',10000);expect(result.score).toBe(0);expect(result.percent).toBe(0);expect(result.questions).toHaveLength(8);
 });
 it('does not score unchecked Practice Mode answers',()=>{
  const practice:ExamConfig={...config,mode:'practice',timerMin:0};
  const picked=selectQuestions(candidatePool(questions,practice),8,100);
  const s=createSession(practice,picked,1000);
  const q=picked.find(x=>x.type==='multiple-choice')!;
  s.answers[q.id]=q.correctOptionId!;
  expect(finalize(s,'submitted',9000).score).toBe(0);
  s.checked=[q.id];
  expect(finalize(s,'submitted',9000).score).toBe(1);
 });
 it('preserves accepted answers without fuzzy similarity',()=>{
  const q=questions.find(q=>q.type==='identification')!;
  expect(grade(q,'not-an-accepted-answer')).toBe(false);
 });
});
type qAnswer=string|boolean;
