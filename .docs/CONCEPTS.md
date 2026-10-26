# Concepts

## Data

**Graph** A structure composed of nodes and edges. In this repo, we mean a directed, but not necessarily acyclic, graph. 
- A graph in LILA represents a repeatable workflow that can be executed, such as managing E-mails.
- A graph can be authored and shared, or it can be generated at run time (e.g. by another graph or loop).

**Workflow** An authored graph that is meant to be repeatable. This the user-facing language and is meant for non-technical users.

**Node** The primary objects on a graph. A node contains a unit of work to be done. In LILA, there are two types of nodes - a Tool node, and a Control node. 

**Edge** The glue connecting nodes on a graph. In this repo, edges are directed, and dictates the next steps for a graph, i.e. how one node transitions into the next.
- Edges may carry information on condition, such that a graph with a node spanning out to multiple possible next-step nodes can evaluate the out edges. The first edge whose condition passes is taken, so edge order matters.

## Engine

**Engine** Decides what gets run next. When there are multiple in-flight graphs, the engine decides which one is still blocked (e.g. awaiting response, awaiting approval) and therefore stays frozen, and which ones can have the next step queued.
- Interface include `submit(graph, input, priority)`, `handle(event)`, `onComplete(node, result)`, and `cancel(id)`.

**Execution** One run of a graph.

**Task** One run of a node, with idempotency key Execution ID + Node ID + attempt.

**Log** Append-only. This is the working memory. LogPath selectors like `$.nodeName.fieldName` resolve against it. Execution state can be derived from it.

**Event** Input source in LILA. EVents are what start a new graph execution or move a blocked execution forward (e.g. one waiting for approval).
- Could be a user message, a CRON event, a graph event (e.g. a node finished).

**Queue** Provides durability, at least once delivery, priority management for node execution. Nodes that are ready to be processed are pushed onto the queue.
- When many graphs are in-flight, queues are used to manage which ones take priority - runs someone is waiting on should run with higher priority over unattended ones.

**Policy** Evaluates what can automatically happen at runtime, what needs human review. This is the guardrail for LILA and is deterministic.

Q: In E-mail management, we want to dictate rules - X types of E-mails goes in A folder. Should this be a part of policy? No. If a dedicated engine, how general can this be?

## Extensibility

**Toolkit** A set of extensions and additional capabilities that extend the core harness. Contains one or more of *tools*, *specs*, and *workflows*.

**Tool** A piece of functionality written in code that the harness can delegate to. The tool is authored as a part of toolkit.
- A tool declares its effect (read-only, reversible, destructive).

**Precondition** A precondition is associated with a tool, and is run before a tool call is executed. A failed precondition will automatically result in a failed tool call without invoking that tool. This is useful to guard against irreversible actions that take place after the agent goes to sleep for a long time and then wake up.

**Secrets Store** Where credentials and other private data lives. They get injected into tools at execution. Access to items in the secrets store are configured by policy.

**Instance** An instance of a tool and the credentials needed.

**Spec** A named set of tool signatures, e.g. LLM spec, channel spec. A graph can declare a spec instead of a specific instance of a tool. 

**Sidecar** Processes (e.g. MCP servers, isolated processes, containers) to run the tools.

## Memory

**Memory** Multiple tiers representing all aspects of LILA operation.
- Working memory is an ordered log of a graph execution. The engine keeps it, not the agent's context. Authored selectors and agent memory tools read it, credentials should never enter it.
- Episodic memory is summarized from graph executions or checkpoints with provenance pointing to the exact graph or subgraph history.
- Procedural memory is represented by the graphs themselves. 
- Semantic memory stores preferences inferred (with provenance) from user feedback.