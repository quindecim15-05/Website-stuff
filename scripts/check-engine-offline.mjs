import fs from 'node:fs';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const ts=require('typescript');
const src=fs.readFileSync('src/domain/engine.ts','utf8');
const transpiled=ts.transpileModule(src,{compilerOptions:{module:ts.ModuleKind.ESNext,target:ts.ScriptTarget.ES2022}}).outputText;
const engine=await import('data:text/javascript;base64,'+Buffer.from(transpiled).toString('base64'));
const {questions}=JSON.parse(fs.readFileSync('src/content/data.json','utf8'));
let assertions=0;
function assert(test,label){assertions++;if(!test)throw Error('Failed: '+label);}
for(const q of questions){let answer=q.type==='true-false'?q.correctBoolean:q.type==='identification'?('   '+q.acceptedAnswers[0].toUpperCase().replaceAll(' ','  ')+'   '):q.correctOptionId;
assert(engine.grade(q,answer),q.id+' correct');assert(!engine.grade(q,undefined),q.id+' unanswered');}
const config={coverage:'mixed',subjectIds:['dcit50','gned07','gned10','pathfit3'],topicId:'',mode:'mock',count:50,timerMin:30,difficulty:'mixed',types:['multiple-choice','true-false','identification','code-analysis']};
const pool=engine.candidatePool(questions,config);const one=engine.selectQuestions(pool,50,12345);const two=engine.selectQuestions(pool,50,12345);
assert(one.length===50,'50 selected');assert(new Set(one.map(x=>x.id)).size===50,'unique');assert(JSON.stringify(one)===JSON.stringify(two),'deterministic');
assert(new Set(one.map(q=>q.subjectId)).size===4,'all subjects');
const s=engine.createSession(config,one,1000);assert(!engine.isTimedOut(s,1000),'not expired');assert(engine.isTimedOut(s,1801000),'expired');
const a=engine.finalize(s,'timeout',1802000);assert(a.id===s.id,'idempotent attempt id');assert(a.score===0,'unanswered zero');assert(a.submittedAt===1801000,'timeout cutoff');
console.log(`PASS: ${assertions} offline assertions across ${questions.length} questions and mock exam lifecycle`);
