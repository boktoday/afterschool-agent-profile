---
name: afterschool-checkin
description: Use when generating the afternoon Afterschool Check-In for the Afterschool Agent student. Short text message: how the day went, the one small action tomorrow, and a single question to sit with overnight.
version: 1.0.0
author: Afterschool Agent contributors
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - afterschool
    - checkin
    - cron
    - eight-essentials
    related_skills:
    - morning-minute
    - eight-essentials-curriculum
    - afterschool-agent-onboarding
---
# Afterschool Check-In

The **Afterschool Check-In** is the afternoon companion to the
Morning Minute. It runs once a day at the student's chosen time
(default 5 pm) and lands as a short text message in the same
channel as the Morning Minute. Audio is not required here — the
check-in is meant to be read and answered, not listened to.

The check-in has three jobs:

1. **Reflect on today.** What happened with the day's one small
   action? Did it get done? Did something get in the way? Hold
   this lightly — no scolding, no moralising.
2. **Plan tomorrow.** Pick one small action for tomorrow, ideally
   the same essential if it needs a second day, or the next
   essential in the rotation.
3. **Carry forward.** Save a short note in memory so tomorrow's
   Morning Minute can open with a callback.

## Input contract

1. **Tradition** — `christian` or `universal` (from onboarding).
2. **Delivery channel** — `telegram` or `whatsapp`.
3. **Today's essential and action** — what the Morning Minute
   told the student to do.
4. **Memory** — read any recent check-ins to maintain continuity.

## Output contract (text only)

A short text message (3 to 6 short paragraphs), ending with one
gentle question. Not a quiz. Not a form. A conversation.

```
Hey, Sam.

Quick check-in. The day's action was sit in the chair for two
minutes before dinner. How did it go? If it didn't happen, what
got in the way? (No judgment — most days it won't.)

For tomorrow, here's one small thing: same chair, three minutes
this time. The two-minute practice is building. You can feel
the difference by the end of the week.

One thing to sit with overnight: what did you hear in the
quiet? Anything? Nothing? Both are fine.
```

Note the structure. No em dashes. No lecturing. No bullet-point
checklists. The student reads this on their phone between classes
or after homework. It needs to feel like a friend checking in,
not a teacher marking homework.

## Step 1 — Read today's plan

Look up the most recent Morning Minute text from the archive:

```bash
tail -50 ~/.hermes/profiles/afterschool/morning-minute-archive.md
```

The essential and the day's action are in the header. Use them.

## Step 2 — Read memory for continuity

If memory has prior check-ins for this student, scan the last few
to keep continuity. Don't repeat the same phrasing. Don't pretend
the conversation didn't happen.

## Step 3 — Compose the message

Three parts:

### Reflection prompt (1 to 2 short paragraphs)

Ask how the day's action went. Hold it lightly. Most days it
won't have happened — that's normal. The student is in the early
weeks of forming a habit. Don't scold, don't diagnose, don't
moralise. Just ask.

### Plan tomorrow (1 to 2 short paragraphs)

One small action. Singular. Concrete. Under five minutes.

If the day's essential was Silence and the action was a two-minute
chair, tomorrow's action is the same chair for three minutes. Build
slowly. Don't jump ahead.

If the day's essential was Digital Self-Defence and the action was
"check your screen-time report", tomorrow's action might be "set a
six-hour daily limit on Instagram."

Phrase as a verb the student can do tomorrow.

### One thing to sit with (1 sentence)

A question or a short prompt the student can hold overnight.
Examples:

- **Silence:** "What did you hear in the quiet?"
- **Body:** "Did you notice when you were most tired today?"
- **Skills:** "What did your hands make today?"
- **Digital Self-Defence:** "What did you choose not to look at?"
- **Real Community:** "Who did you listen to today?"
- **Knowledge:** "What did you remember from memory today?"
- **Nature:** "When did you last feel the wind?"
- **Faith (Christian):** "Where did you see God today?"
- **Faith (Universal):** "What did you believe in today?"

Pick the right one for the day's essential.

## Step 4 — Save to memory

Write a one-line summary to Mnemosyne:

```
<date> — Essential: <name>. Action: <what was done>. Status: <done / partial / missed>. Tomorrow: <next action>.
```

This is what tomorrow's Morning Minute will read for the callback.

## Step 5 — Deliver

Send the text to the student's channel (Telegram or WhatsApp). No
audio. No file attachment. Plain text.

```python
telegram(
    chat_id=os.environ["TELEGRAM_CHAT_ID"],
    text=checkin_text,
)
```

## Pitfalls

- **Don't scold.** Most days the action won't get done. That's the
  rule, not the exception. Holding it lightly is the skill.
- **Don't moralise.** "You should have…" is the wrong voice. The
  student is here to build a life, not to feel guilty.
- **Don't repeat the same phrasing.** Read recent check-ins from
  memory and vary the wording. The student will notice.
- **Don't add new essential content.** This is a check-in, not a
  lesson. Save the teaching for the Morning Minute and the
  curriculum skill.
- **Don't ask too many questions.** One question to sit with is
  enough. Two is too many.

## Cron configuration

Schedule format depends on the student's choice. Common options:

- `0 17 * * *` — every day at 5 pm
- `0 16 * * 1-5` — school days at 4 pm
- `0 18 * * 0,6` — weekends at 6 pm

**Pinned model:** `deepseek-v4-flash` via the `deepseek` provider.

**Delivery target:** `origin` (Telegram or WhatsApp).

## Related skills

- `morning-minute` — the morning plan that pairs with this
  check-in.
- `eight-essentials-curriculum` — the deeper teaching skill.
- `afterschool-agent-onboarding` — sets the check-in time and
  channel.