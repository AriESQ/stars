# Cline Memory Bank

This repository implements a memory feature for Cline editor using Obsidian as a knowledge management system. It provides a set of custom commands that allow Cline to maintain memory between sessions.

## Overview

Cline is an engineer with memory that resets between sessions. The Obsidian Memory Bank helps Cline work effectively by providing a structured way to store and retrieve knowledge about projects. When starting a new session, Cline must read all relevant files to regain context.

## Commands

* **`follow instructions`** - Read context from current repo's Obsidian vault
* **`init memory`** - Setup vault with auto-scanning and knowledge graph
* **`update memory`** - Review docs, update graphs and connections
* **`query [topic]`** - Search for specific information

## Core Structure

The memory bank creates focused knowledge using Obsidian's powerful features:

* **Backlinks & transclusion** - For creating connections between related concepts
* **YAML front matter** - For structured metadata
* **Tags** - For categorization and filtering
* **Dataview** - For dynamic queries and data aggregation
* **Mermaid** - For visualizations and diagrams
* **Templates** - For consistency across documentation

## Essential Documentation

The memory bank maintains these core files:

1. **`CodeMOC.md`** - Navigation map with component links
2. **`Overview.md`** - Project vision and requirements
3. **`Architecture.md`** - Design decisions and patterns
4. **`Components.md`** - Visual component map
5. **`Progress.md`** - Status and roadmap

## Knowledge Prioritization

The memory bank focuses on essence over exhaustiveness:

* Core architectural patterns
* Key interfaces between components
* Critical data and control flows
* Important design decisions
* Domain concepts and business logic

## Documentation Approach

The memory bank creates minimal, high-value knowledge:

* Clear visualizations over lengthy text
* Concise explanations of non-obvious patterns
* Relationship mapping for complex interactions
* Focus on "why" over "what" when possible
* Document only what's needed for understanding

## Auto-Generation

When running commands, the memory bank:

* Creates focused, essential documentation
* Generates only necessary diagrams
* Tracks only meaningful changes
* Optimizes for quick comprehension

After every reset, Cline starts fresh, documenting only what's necessary for understanding, maintaining, and extending the codebase, without verbosity.

## Getting Started

To use the Cline Memory Bank:

1. Add the custom instructions to your Cline configuration
2. Initialize a new memory vault with `init memory`
3. Use the commands to maintain and query your knowledge base
4. Start each session with `follow instructions` to load context

## Benefits

* **Persistent Knowledge** - Maintain context between sessions
* **Structured Documentation** - Organized, consistent documentation
* **Efficient Recall** - Quick access to critical information
* **Focus on Essentials** - Capture only what matters
* **Visual Understanding** - Diagrams and relationship maps
