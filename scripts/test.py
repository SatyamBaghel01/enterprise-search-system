from src.agents.orchestrator import SearchOrchestrator

orchestrator = SearchOrchestrator()

response = orchestrator.search(
    query="What is enterprise search and how does it work?"
)

print(response["answer"])
print(response["citations"])
