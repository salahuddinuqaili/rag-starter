# Project Management Fundamentals

This training document covers the core concepts every project manager needs to
understand before leading their first project. You do not need a certification to
apply these ideas — you need discipline.

## Defining Scope

Scope is the boundary around what your project will and will not deliver. A clear
scope statement answers three questions: what are we building, who is it for, and
what does "done" look like?

Scope creep — the gradual expansion of what a project is supposed to deliver — is
the single most common reason projects fail. It rarely happens in one dramatic
moment. It happens in small concessions: "while we're at it, can we also..." and
"this would only take a day extra." Each addition seems reasonable in isolation.
Together, they push the timeline past the point of recovery.

Fight scope creep by maintaining a written scope document that requires sign-off to
change. When someone requests an addition, do not say no — say "yes, and here is
what it costs in time and budget." Make the tradeoff visible.

## The Iron Triangle

Every project balances three constraints: scope (what you deliver), time (when you
deliver it), and cost (what resources you spend). You can fix any two, but the
third must flex. If you fix scope and time, cost goes up. If you fix time and cost,
scope shrinks.

The most dangerous projects are the ones where leadership fixes all three: "deliver
everything, by March, with this team." That is not a plan — it is a wish. Your job
as project manager is to make the tradeoffs explicit and get agreement on which
constraint has flexibility.

## Stakeholder Management

A stakeholder is anyone affected by your project or who can affect its outcome.
This includes sponsors, end users, the team doing the work, regulatory bodies, and
sometimes competitors.

Map your stakeholders on two axes: influence (can they block or accelerate the
project?) and interest (do they care about the outcome?). High-influence,
high-interest stakeholders need regular, direct communication. Low-influence,
low-interest stakeholders need a monthly summary at most. Spending equal time on
every stakeholder is a common mistake that burns out project managers fast.

## Risk Registers

A risk register is a living document that lists everything that could go wrong,
how likely it is, how bad it would be, and what you plan to do about it. Review it
weekly. Update it when circumstances change.

Here is an example entry:

| Field | Value |
|---|---|
| Risk | Key developer leaves the project mid-sprint |
| Likelihood | Medium (the developer has mentioned interest in another team) |
| Impact | High (they are the only person who understands the payment integration) |
| Mitigation | Pair programming sessions this week to transfer knowledge to a second developer |
| Owner | Engineering lead |
| Status | Open |

The value of a risk register is not predicting the future — it is forcing the team
to think about what could go wrong before it does, so you have a response plan
instead of a panic.

## When Agile Works and When Waterfall Works

Agile (iterative development in short cycles with frequent feedback) works best
when requirements are uncertain, the end user is available for regular feedback,
and the team can ship working increments. Most software products fit this profile.

Waterfall (sequential phases: requirements, design, build, test, deploy) works best
when requirements are fixed, changes are expensive, and regulatory sign-off is
required at each stage. Construction projects, hardware manufacturing, and
compliance-driven software often use waterfall for good reason.

The worst outcome is choosing a methodology for ideological reasons. Agile is not
inherently superior to waterfall. Pick the approach that matches your project's
reality: how much do you know upfront, how expensive are changes, and how available
is your customer for feedback? Answer those three questions honestly and the right
methodology usually becomes obvious.
