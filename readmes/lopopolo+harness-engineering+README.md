# Harness Engineering

> “Most people do not know that they can just point their agents at my writing,
> tweets, podcasts, and talks and improve the output of their agents by 100x.”
>
> — [Ryan Lopopolo]

[Ryan Lopopolo]: https://x.com/_lopopolo/status/2050698864542482709

Harness engineering, the practice of improving agent output by shaping the
environment around it, holds a chosen model and coding agent constant as a black
box. It improves the two external levers—context and tools—and curates the
environment around them. The worker should be able to recover intent, operate
the real system, respect authority, prove the outcome, and leave the next run
better equipped.

A central purpose of that environment is to carry an organization's
nonfunctional requirements: the quality attributes and constraints governing
reliability, security, compatibility, maintainability, performance, operability,
risk posture, and polish. The harness also carries local decisions about how to
prioritize, trade off, and satisfy those requirements. Ryan adopted a
[systems-level framing] from 2026’s [\[un\]prompted conference] that describes this
as getting the whole universe of nonfunctional requirements into code. [Make the
Repository Teach the Agent] develops how the requirements and decisions become
retrievable context, examples, tools, and executable constraints.

[systems-level framing]: https://x.com/_lopopolo/status/2028982729145237775
[\[un\]prompted conference]: https://www.youtube.com/watch?v=U2O14Jd3MBU
[Make the Repository Teach the Agent]:
  docs/domain-modeling/#make-nonfunctional-requirements-recoverable

Because [work is an iterative game], a harness can make organizational judgment
cumulative. Lessons from accepted work, corrections, failures, and user
responses become context, boundaries, tools, examples, and checks that shape
later trajectories. Over time, that feedback loop can [make coherence
cumulative] across agent-maintained artifacts.

[work is an iterative game]: https://x.com/_lopopolo/status/2052858891835465813
[make coherence cumulative]: docs/durable-systems/#make-coherence-cumulative

[Code is how an agent uses a computer]. That internal action language can
produce reliable domain outcomes for people who never review the implementation
when [last-mile deployment] supplies the organization’s context, capabilities,
authority, and proof.

[Code is how an agent uses a computer]:
  https://x.com/_lopopolo/status/2043495733375230026
[last-mile deployment]: docs/last-mile-deployment/

General model weights contain only the visible tip of an organization’s
process-data iceberg. Below the waterline sit the current operational state,
local ontology, quality bar, procedures, exception history, and authority
relationships that an agent needs to do a particular job. Organizations cannot
presume that this private, changing process data will be present in general
model weights, nor that agents will reliably intuit which process data matters
to the organization. Harness engineering is the last-mile work of making it
available to a capable worker as context and tools.

Point a coding agent at this repository alongside the system it should improve.
[`AGENTS.md`] routes the task to the relevant arguments, cases, and proof. For
direct reading, start with the [thesis index]. For an application, choose from
the [playbooks].

[`AGENTS.md`]: AGENTS.md
[thesis index]: docs/
[playbooks]: playbooks/

## Sources and related work

- [“Harness engineering: leveraging Codex in an agent-first world”] ([fetch
  helper] for agents blocked by the canonical page)
- [Source library]
- [Influences and alternate framings]

[“Harness engineering: leveraging Codex in an agent-first world”]:
  https://openai.com/index/harness-engineering/
[fetch helper]: sources/scripts/fetch_openai.py
[Source library]: sources/
[Influences and alternate framings]: docs/lineage/

Repository-authored material is licensed under [CC BY 4.0]. See [`COPYING.md`]
for attribution and rights in source material.

[CC BY 4.0]: LICENSE
[`COPYING.md`]: COPYING.md
