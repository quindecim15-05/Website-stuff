import fs from 'node:fs';
if(process.env.SOURCE_PERMISSION!=='confirmed'){
 fs.rmSync('dist/materials',{recursive:true,force:true});
 console.log('Copyright safety: removed original course PDFs from production build. To publish them, obtain distribution permission and run npm run build:with-documents.');
}else console.log('Publishing source documents at user-confirmed request.');
