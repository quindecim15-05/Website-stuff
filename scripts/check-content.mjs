import fs from 'node:fs';import path from 'node:path';
const data=JSON.parse(fs.readFileSync('src/content/data.json','utf8'));
let errors=[];let ids=new Set();const sources=new Map(data.sources.map(s=>[s.id,s]));const topics=new Set(data.topics.map(t=>t.id));
for(const q of data.questions){if(ids.has(q.id))errors.push('duplicate '+q.id);ids.add(q.id);if(!topics.has(q.topicId))errors.push('missing topic '+q.id);if(!q.prompt||!q.explanation||q.verificationStatus!=='verified')errors.push('incomplete '+q.id);for(const r of q.sources){const s=sources.get(r.sourceId);if(!s||r.page<1||r.page>s.pages)errors.push('invalid source '+q.id);}
if(['multiple-choice','code-analysis'].includes(q.type)&&(q.options?.length!==4||!q.options.some(o=>o.id===q.correctOptionId)||new Set(q.options.map(o=>o.id)).size!==4))errors.push('invalid options '+q.id);
if(q.type==='true-false'&&typeof q.correctBoolean!=='boolean')errors.push('invalid boolean '+q.id);
if(q.type==='identification'&&!q.acceptedAnswers?.length)errors.push('invalid identification '+q.id);
}
for(const t of data.topics){const s=sources.get(t.sourceId);if(!s)errors.push('missing lesson source '+t.id);for(const sec of t.sections)if(sec.page<1||sec.page>s.pages)errors.push('invalid lesson page '+t.id);}
console.log(`Validated ${data.questions.length} questions, ${data.flashcards.length} flashcards, ${data.topics.length} topics, ${data.sources.length} sources`);
if(errors.length){console.error(errors.join('\n'));process.exitCode=1;}
