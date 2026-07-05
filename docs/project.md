---
type: 'Page'
title: Project Whatsup-Brain (PUBLIC)
aliases: null
description: null
icon: null
createdAt: '2026-07-05T15:48:22.753Z'
lastUpdated: '2026-07-05T16:31:27.976Z'
tags: []
coverImage: null
---

# Project Overview

"whatsup-brain" is a REST API for dumping thoughts into a database and pulling them back out later. You send it a note, it saves the note, you ask for it, it gives it back. That's the whole product.

I'm not solving a real problem here. Notion, Apple Notes, and a hundred other apps already do this better than whatsup-brain ever will. The real problem I'm solving is my own understanding of how things work.

I picked "notes" as the thing to build around because it's boring. Boring is good here. If the idea itself was interesting, I'd end up thinking about the idea instead of the plumbing underneath it.

# Objectives

## Product Objective

The API should let me:

- create a note

- view all notes

- view one specific note

- delete a note

That's it. No editing, no accounts, no folders. Four endpoints, and each one should work correctly and behave the same way every time.

## Learning Objective

I want to be able to explain, without looking anything up, what happens between a client sending a request and getting a response back. Specifically:

- how an API actually receives and routes a request

- what CRUD means in practice, not just as an acronym

- how request validation works, and why it happens before data touches the database

- how an ORM sits between my code and the actual database

- what's really going on when data turns into JSON and travels back to the client

- how FastAPI, Pydantic, SQLAlchemy, and SQLite are separate tools that all have to cooperate to make one request work

I don't want surface familiarity with these words. I want to have watched them work, break, and get fixed at least once each.

# Scope

## What I'm Building

- Create a note

- View all notes

- View one note

- Delete a note

Four endpoints. That's the entire feature list, and I kept it this small on purpose. Every extra feature is one more thing that could go wrong, and one more thing that pulls my attention away from the actual request flow. If I added tags or search right now, I'd spend my time thinking about tags and search instead of thinking about how FastAPI, Pydantic, and SQLAlchemy talk to each other. The point isn't to make something impressive. The point is to make something small enough that I can hold the whole system in my head at once.

## What I'm NOT Building

Intentionally out of scope:

- Authentication

- User accounts

- AI

- Search

- Tags

- File uploads

- Images

- Notifications

- Deployment

- Docker

- Cloud hosting

None of these are left out because they're too advanced for me. They're left out because they're extra surface area: more edge cases, more moving parts, more distance between me and the thing I'm here to learn. Keeping the scope this small is what lets me stay focused on the backend fundamentals instead of chasing features.

# Tech Stack

| Technology | Purpose                                                           | Why I Chose It                                                                                                                |
| :--------- | :---------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| FastAPI    | Receives requests and routes them to the right code               | Fast to write in, and it keeps routing, validation, and docs feeling like separate steps instead of one black box             |
| Uvicorn    | Actually runs the FastAPI app as a server                         | FastAPI needs something to serve it, and Uvicorn is the standard                                                              |
| SQLAlchemy | Lets Python talk to the database without raw SQL everywhere       | I want to understand ORMs properly, and this is the standard one in Python                                                    |
| SQLite     | Stores the notes                                                  | Zero setup. It's one file, not a service I need to install and run separately, which is exactly right for a project this size |
| Pydantic   | Checks that incoming data actually looks the way it's supposed to | FastAPI is built around it anyway, and it's a clean way to watch validation happen instead of just trusting whatever comes in |
| Git        | Tracks how the code changes over time                             | I want history of this project                                                                                                |
| GitHub     | Hosts the repo                                                    | Somewhere to point back to later, and a backup.                                                                               |

# High Level Architecture

```text
Client
    |
HTTP Request
    |
FastAPI
    |
Pydantic Validation
    |
SQLAlchemy
    |
SQLite Database
    |
JSON Response
    |
Client
```

Here's what happens, step by step, when someone hits one of these endpoints.

A client, probably just me testing through the FastAPI docs page, sends an HTTP request. That's just a message over the network saying what it wants done, like "save this note" or "give me note number 3."

FastAPI catches that request first. It looks at the URL and the method (GET, POST, DELETE) and figures out which piece of my code should handle it.

Before that code runs, Pydantic checks the data. If I'm creating a note, Pydantic makes sure the request actually contains something that looks like a note, not garbage or a missing field. If the data doesn't match what's expected, the request gets rejected before it ever reaches the database. This is the part I'm most curious to watch happen.s

Once the data passes validation, SQLAlchemy takes over. It turns my Python objects into actual SQL commands and talks to the database for me. I never write raw SQL myself. I write Python, and SQLAlchemy handles the translation.

SQLite is where the note actually lives. It's just a database sitting in a single file on my machine, but from the code's point of view it behaves like any other database.

After the database does its job, whether that's saving something, finding something, or deleting something, the result travels back the other way. SQLAlchemy hands it to FastAPI, FastAPI turns it into JSON, and that JSON goes back to the client as the response.

## Why FastAPI?

I wanted something where the request flow stays visible instead of hidden. FastAPI makes routing, validation, and documentation feel like separate, understandable steps.

## Why SQLite?

I don't need a real database server for something this small. SQLite is one file, needs no setup, and lets me focus on how the ORM and the database interact instead of fighting with installation.

## Why SQLAlchemy instead of raw SQL?

I could write raw SQL for something this size, maybe even faster. But the point of this project is to understand how an ORM works, not to avoid learning one. SQLAlchemy is the standard tool for this in Python, so better to learn what it's doing here, on something small, than fumble through it blind.

## Why Pydantic?

I wanted to watch validation happen instead of assuming every request is well formed. Pydantic makes bad data get rejected loudly and early, which is exactly the behavior I want to understand.

## Why keep the API intentionally small?

Because the goal isn't the app. Four endpoints are enough to see a full request and response cycle several times, in slightly different shapes: create, read one, read many, delete. That's plenty without adding complexity that has nothing to do with backend fundamentals.

## Why no authentication?

Authentication is its own topic, with its own things to learn: tokens, sessions, hashing, real security concerns. Mixing it into this project means learning two things badly instead of one thing well. It's left out on purpose.

## Why document before writing code?

Because I know myself. If I open the editor first, I'll start typing before I've actually decided what I'm building or why. Writing this first means the decisions are already made by the time I sit down to code, so I'm implementing a plan instead of discovering one as I go.

