# Part 3

- Why does the request use a client-generated id rather than a server-generated one?
What problem does this solve in distributed systems?

A: Using a client-generated id rather than a server-generated one is so the request can be identified. If it was a server-generated one, there might be a case where the client doesn't receive a response and so the client can just retry with the same request id, instead of creating a new one.

- The status.state can be 'working'. Under what circumstances would a server return this
state in a non-streaming call, and how should a client react?

A: A server can return the state 'working' when the agent is taking longer, like handling a large input or requesting an outside tool. The client should wait and have another endpoint that is a follow up to the request.

- What is the purpose of the sessionId field? Give a concrete example of two related tasks
that should share a session.

A: A sessionId is meant for two or more related tasks in order to group them into the same session. Two related tasks that might need to share a sessionId could be "generate code" and "summarize the functions of the code".

- The parts array supports types text, file, and data. Describe a realistic multi-agent
workflow where all three part types appear in a single conversation.

A: A workflow could be a request that says "convert this txt file which has a numbered list of foods into a csv file". In this case, the text type is the instruction/prompt, the file type is the txt file, and the data type is csv format.  


# Part 4

- Describe what the --allow-unauthenticated flag does and its security implications.

A: This flag allows unauthenticated access to the Cloud Run service. Now the only security problem this has right now is that my service can be requested excessively by anyone and my tokens/credits will be wasted. Now, if this service had sensitive information, that information could be access withouted authentication.

- Describe how Cloud Run scales to zero and what cold start latency means for A2A clients.

A: Basically, when no one is using/requesting the A2A service, it powers down a certain amount of running containers so they are not being wasteful, even scaling down to 0 running containers. A cold starts happens when the service has scaled down to 0 and now a container must be spun up for that incoming request, resulting in a significantly delayed response.

# Part 5

- Explain the difference between deploying to Cloud Run vs Agent Engine in terms of operational burden and use-case fit.

A: Cloud Run is used more for general HTTP apps like FastAPI servers, where the operational burden is on containers. Deploying to agent engine is used for more agent specific tasks like having a wrapped agent class and the operational burden is on the engine to deploy and execute agent workloads.

- Explain why the wrapper class uses a synchronous query() method even though the underlying handler is async.

A: A synchronous query() method is what the Vertex AI agent engine expects when deploying an agent. the FastAPI server has async logic, but the wrapper makes it synchronous.

# Part 6

client/demo.py log output:
[REQUEST] GET https://echo-a2a-agent-741297514794.us-central1.run.app/.well-known/agent.json [RESPONSE] 200 https://echo-a2a-agent-741297514794.us-central1.run.app/.well-known/agent.json Agent name: Echo Agent Skills:  
Echo  
Summarise [REQUEST] POST https://echo-a2a-agent-741297514794.us-central1.run.app/tasks/send payload={'id': 'a94265b6-cccf-43d0-a51c-bfh71s7gjh12', 'text': 'Hello from the client!'} [RESPONSE] 200 https://echo-a2a-agent-741297514794.us-central1.run.app/tasks/send status={'state': 'completed'}  
Response: Hello from the client!

UML diagram:

![alt text](uml.png)

- If a client loses the network connection after sending the POST but before receiving the response, how could it safely retry? What field in the A2A protocol helps with idempotency?

A: It can retry the POST request with the same Client-generated ID instead of creating a new POST request. This helps with idempotency because the server processing the POST request can recognize the ID and perform the operation without performing it multiple times unnecessarily because of differing ID's. 
