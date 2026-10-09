/** Serialize the study position in the URL, so Back and refresh can restore it. */
export type FlashcardNavigationState = {
  subject: string;
  topic: string;
  status: string;
  cardId?: string;
  shuffle: number;
  flipped: boolean;
};

export function flashcardsPath(state: FlashcardNavigationState): string {
  const params = new URLSearchParams();
  if (state.subject !== 'all') params.set('subject', state.subject);
  if (state.topic !== 'all') params.set('topic', state.topic);
  if (state.status !== 'all') params.set('status', state.status);
  if (state.cardId) params.set('card', state.cardId);
  if (state.shuffle > 0) params.set('shuffle', String(state.shuffle));
  if (state.flipped) params.set('side', 'answer');
  return '/flashcards' + (params.size ? '?' + params.toString() : '');
}

/** Accept only an internal flashcards path as a return destination. */
export function safeFlashcardsReturnPath(value: string | null): string | null {
  if (!value || !value.startsWith('/flashcards')) return null;
  try {
    const target = new URL(value, 'https://studyspace.local');
    if (target.origin !== 'https://studyspace.local' || target.pathname !== '/flashcards' || target.hash) return null;
    return target.pathname + target.search;
  } catch {
    return null;
  }
}

export function sourceWithReturn(sourcePath: string, returnPath: string): string {
  const separator = sourcePath.includes('?') ? '&' : '?';
  return `${sourcePath}${separator}returnTo=${encodeURIComponent(returnPath)}`;
}
