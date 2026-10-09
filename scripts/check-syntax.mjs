import fs from 'node:fs';import path from 'node:path';import{createRequire}from'node:module';
const require=createRequire(import.meta.url);const ts=require('typescript');
let count=0;const failures=[];
function scan(folder){for(const f of fs.readdirSync(folder)){const p=path.join(folder,f),st=fs.statSync(p);if(st.isDirectory())scan(p);else if(/\.tsx?$/.test(f)&&!f.endsWith('.d.ts')){count++;const out=ts.transpileModule(fs.readFileSync(p,'utf8'),{fileName:p,compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.ESNext,jsx:ts.JsxEmit.ReactJSX},reportDiagnostics:true});for(const d of out.diagnostics||[])if(d.category===ts.DiagnosticCategory.Error)failures.push(p+': '+ts.flattenDiagnosticMessageText(d.messageText,' '));}}}
for(const f of ['src','tests'])scan(f);console.log(`Syntax parsing: ${count} TypeScript/TSX files, ${failures.length} errors`);if(failures.length){console.error(failures.join('\n'));process.exit(1)}
