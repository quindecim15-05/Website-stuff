import{describe,it,expect}from'vitest';import{subjects,sources,topics,questions,flashcards}from'../src/content';
describe('Content integrity',()=>{
 it('contains all four subjects and eight source files',()=>{expect(subjects).toHaveLength(4);expect(sources).toHaveLength(8)});
 it('keeps question references in range',()=>{for(const q of questions)for(const s of q.sources){const source=sources.find(x=>x.id===s.sourceId);expect(source).toBeDefined();expect(s.page).toBeGreaterThanOrEqual(1);expect(s.page).toBeLessThanOrEqual(source!.pages)}});
 it('never duplicates question IDs and verifies four question types',()=>{expect(new Set(questions.map(x=>x.id)).size).toBe(questions.length);expect(new Set(questions.map(x=>x.type)).size).toBe(4)});
 it('has source-grounded lessons and flashcards for each topic',()=>{for(const t of topics){expect(t.summary.length).toBeGreaterThan(0);expect(t.sections.length).toBeGreaterThan(0);expect(flashcards.some(c=>c.topicId===t.id)).toBe(true)}});
});
