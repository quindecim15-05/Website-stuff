import { describe,expect,it } from 'vitest';
import { flashcardsPath,safeFlashcardsReturnPath,sourceWithReturn } from '../src/lib/flashcardNavigation';

describe('flashcard source return navigation',()=>{
 it('preserves filters, exact card, shuffle order and flipped state',()=>{
  const path=flashcardsPath({subject:'pathfit3',topic:'pickleball',status:'known',cardId:'card-003',shuffle:1234,flipped:true});
  expect(path).toBe('/flashcards?subject=pathfit3&topic=pickleball&status=known&card=card-003&shuffle=1234&side=answer');
  const source=sourceWithReturn('/materials/pickleball?page=3',path);
  const parsed=new URL(source,'https://studyspace.local');
  expect(safeFlashcardsReturnPath(parsed.searchParams.get('returnTo'))).toBe(path);
 });
 it('rejects external and misleading return destinations',()=>{
  expect(safeFlashcardsReturnPath('https://example.com/flashcards')).toBeNull();
  expect(safeFlashcardsReturnPath('//example.com/flashcards')).toBeNull();
  expect(safeFlashcardsReturnPath('/flashcards/elsewhere')).toBeNull();
  expect(safeFlashcardsReturnPath('/subjects/pathfit3')).toBeNull();
 });
});
