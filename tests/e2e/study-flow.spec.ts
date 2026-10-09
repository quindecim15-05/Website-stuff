import { test, expect } from '@playwright/test';
test.beforeEach(async ({page})=>{await page.goto('/');});
test('subjects and source-based reviewer are navigable',async ({page})=>{
 await page.getByRole('link',{name:/Explore subjects/}).click();
 await expect(page.getByRole('heading',{name:'All subjects'})).toBeVisible();
 await page.getByRole('link',{name:/DCIT 50/}).first().click();
 await page.getByRole('link',{name:/Java Constructors/}).click();
 await expect(page.getByRole('heading',{name:'Java Constructors'})).toBeVisible();
 await page.getByRole('tab',{name:'Detailed lesson'}).click();
 await expect(page.getByText(/Source-based lessons/)).toBeVisible();
});
test('mock exam loads, navigates, saves answers and scores',async ({page})=>{
 await page.getByRole('link',{name:/Start a mock exam/}).click();
 await page.getByRole('button',{name:/Quick review/}).click();
 await page.getByRole('button',{name:/Start mock exam/}).click();
 await expect(page.getByText(/QUESTION 01/)).toBeVisible();
 await page.locator('.answer-option').first().click();
 await page.getByRole('button',{name:/Next question/}).click();
 await page.reload();
 await expect(page.getByText(/QUESTION 02/)).toBeVisible();
 await page.getByRole('button',{name:/Review & submit/}).last().click();
 await page.getByRole('button',{name:/Submit exam/}).click();
 await expect(page.getByRole('heading',{name:/Another step forward/})).toBeVisible();
});

test('multiple-choice labels are A–D and exam topbar stays visible on scroll',async ({page})=>{
 await page.setViewportSize({width:1280,height:480});
 await page.goto('/exams/new');
 await page.getByRole('button',{name:'Subject',exact:true}).click();
 await page.getByRole('checkbox',{name:/True \/ False/i}).uncheck();
 await page.getByRole('checkbox',{name:/Identification/i}).uncheck();
 await page.getByRole('checkbox',{name:/Java code analysis/i}).uncheck();
 await page.getByRole('spinbutton',{name:/Number of questions/i}).fill('4');
 await page.getByRole('button',{name:/Start mock exam/i}).click();
 await expect(page.locator('.answer-marker')).toHaveText(['A','B','C','D']);
 await page.evaluate(()=>window.scrollTo(0,document.documentElement.scrollHeight));
 await expect.poll(()=>page.evaluate(()=>window.scrollY)).toBeGreaterThan(0);
 await expect(page.locator('.exam-topbar')).toBeInViewport();
});

test('a flashcard source opens the correct PDF page and returns to the same card',async ({page})=>{
 await page.goto('/flashcards?subject=pathfit3');
 await page.getByRole('button',{name:'Next',exact:true}).click();
 await page.getByRole('button',{name:'Next',exact:true}).click();
 await page.getByRole('button',{name:'Reveal flashcard answer'}).click();
 const cardNumber=await page.locator('.flash-head h2').textContent();
 const answer=await page.locator('.flip-text').textContent();
 await page.getByRole('link',{name:/Source page/}).click();
 await expect(page).toHaveURL(/\/materials\/[^?]+\?page=/);
 const back=page.getByRole('link',{name:'Back to Flashcards'});
 await expect(back).toBeVisible();
 await page.getByRole('button',{name:'Next page'}).click();
 await page.reload();
 await expect(back).toBeVisible();
 await back.click();
 await expect(page.locator('.flash-head h2')).toHaveText(cardNumber||'Card 3 of 54');
 await expect(page.locator('.flip-text')).toHaveText(answer||'');
 await expect(page.getByRole('button',{name:'Show flashcard question'})).toBeVisible();
 await page.goBack();
 await expect(page.getByRole('link',{name:'Back to Flashcards'})).toBeVisible();
});

test('flashcards open on the question side unless restoring a specific card',async ({page})=>{
 await page.goto('/flashcards?side=answer');
 await expect(page.locator('.flip-tag')).toHaveText('QUESTION');
 await expect(page.getByRole('button',{name:'Reveal flashcard answer'})).toBeVisible();
});

test('direct PDF visits keep subject navigation instead of an invalid flashcard return',async ({page})=>{
 await page.goto('/materials/pickleball?page=3&returnTo=https%3A%2F%2Fexample.com');
 await expect(page.getByRole('link',{name:'Back to PATHFIT 3'})).toBeVisible();
 await expect(page.getByRole('link',{name:'Back to Flashcards'})).toHaveCount(0);
});
