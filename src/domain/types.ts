export type QuestionType = 'multiple-choice' | 'true-false' | 'identification' | 'code-analysis';
export type Difficulty = 'easy' | 'medium' | 'hard';
export type Answer = string | boolean;
export type Question = {
  id:string;subjectId:string;topicId:string;conceptId:string;type:QuestionType;difficulty:Difficulty;
  prompt:string;explanation:string;sources:{sourceId:string;page:number}[];
  verificationStatus:'verified';version:number;
  options?:{id:string;text:string}[];correctOptionId?:string;correctBoolean?:boolean;acceptedAnswers?:string[];code?:string;
};
export type Coverage = 'subject' | 'topic' | 'mixed';
export type Mode = 'practice' | 'mock';
export type ExamConfig = {coverage:Coverage;subjectIds:string[];topicId:string;mode:Mode;count:number;difficulty:Difficulty|'mixed';types:QuestionType[];timerMin:number};
export type Timing = {startedAt:number;deadlineAt:number|null;elapsedBeforeMs:number;resumedAt:number|null};
export type ExamSession = {
  schemaVersion:1;id:string;config:ExamConfig;status:'active'|'paused';reviewing:boolean;
  questions:Question[];answers:Record<string,Answer>;checked:string[];flags:string[];position:number;
  timing:Timing;updatedAt:number;
};
export type ExamAttempt = {
 id:string;sessionId:string;config:ExamConfig;questions:Question[];answers:Record<string,Answer>;flags:string[];correctIds:string[];
 score:number;percent:number;startedAt:number;submittedAt:number;elapsedMs:number;reason:'submitted'|'timeout';
};
export type Mastery = Record<string,'known'|'again'>;
