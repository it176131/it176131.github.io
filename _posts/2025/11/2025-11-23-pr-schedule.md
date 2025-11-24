---
layout: "post"
title: "Assigning PR Reviews with Mixed Integer Linear Programming"
date: 2025-11-23
---

Earlier this year a colleague and I refactored a code base that created schedules for office staff.
The code used a technique called _Mixed Integer Linear Programming_, or _MILP_ (also sometimes abbreviated as _MIP_).
Most of the refactoring involved updating code to use the most up-to-date packages,
and bumping the Python version up to something that would still be supported in a few years.
Oh, and adding unit tests... story for another time,
but the original authors did **_NOT_** use [_TDD_]({{ site.baseurl }}{% link _posts/2024-03-24-contributing-pt2.md %}).