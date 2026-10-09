import {spawnSync} from 'node:child_process';
console.log('Requires prior permission from source copyright holders to share course materials publicly.');
if(process.env.SOURCE_PERMISSION!=='confirmed') {console.error('Set SOURCE_PERMISSION=confirmed explicitly after obtaining permission.');process.exit(1);}
const result=spawnSync('npm',['run','build'],{stdio:'inherit',env:{...process.env,SOURCE_PERMISSION:'confirmed',VITE_ENABLE_SOURCE_DOCS:'true'},shell:process.platform==='win32'});process.exit(result.status??1);
