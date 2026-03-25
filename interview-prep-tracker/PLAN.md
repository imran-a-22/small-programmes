# Interview Prep Tracker — Plan of Action

This document breaks work into phases so development stays incremental and reviewable.

## Phase 0: Project setup
1. Create app skeleton and folder structure.
2. Add Flask app entrypoint and SQLite database bootstrap.
3. Add README, requirements, and run instructions.

## Phase 1: Authentication
1. Implement user registration.
2. Implement login/logout flows with sessions.
3. Restrict app routes to authenticated users.

## Phase 2: Card Management (Core CRUD)
1. Add create card form.
2. Add list page with search/filter by tag.
3. Add edit and delete card actions.
4. Save confidence score and next review date.

## Phase 3: Daily Review Workflow
1. Build “Today’s Review” queue for due cards.
2. Allow confidence update after each review.
3. Recompute next review date using spaced intervals.

## Phase 4: Dashboard + Insights
1. Show total cards, due cards, average confidence.
2. Show card counts by topic/tag.
3. Keep UI simple but clean for portfolio demos.

## Phase 5: Quality + Portfolio Packaging
1. Add automated tests for key routes and workflows.
2. Add sample data script (optional).
3. Add screenshots/GIF and architecture notes in README.
4. Add deployment notes (Render/Fly/Vercel + DB provider).

## Stretch goals (after MVP)
1. Guest mode and account conversion.
2. CSV import/export.
3. AI-generated hinting or answer evaluation.
4. Public read-only shared decks.
5. Mobile-first PWA support.
