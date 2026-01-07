# Future-Ralph

**A Heterogeneous Agent Wrapper exploring multiple possible futures.**

Future-Ralph is a developer tool that explores multiple possible futures of a codebase using heterogeneous AI agents. Inspired by the non-canonical future timelines of Ralph Wiggum in The Simpsons, the tool treats each agent run as a distinct possible future.

## Vision

Rather than retrying the same agent repeatedly, Future-Ralph embraces diversity of models, tools, and reasoning styles to reduce correlated failure modes and escape local minima. The user remains in the present (coding, sleeping, eating), while Future-Ralph explores futures asynchronously and returns with the best viable outcome.

## Core Design Principles

*   **Heterogeneous agents outperform homogeneous retries**
*   **Futures are exploratory, not predictive**
*   **Wrapper-enforced safety and budgets**
*   **Async-first, resumable execution**

## Installation

```bash
uv tool install future-ralph
```

## Quick Start

```bash
future-ralph run "Refactor the login logic"
```
