from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

#define graph state
class GreetingState(TypedDict):
    greeting: str

def normalize_greeting_node(state: GreetingState):
    state["greeting"] = state["greeting"].lower()
    return state

def hi_greeting_node(state):
    state["greeting"] = "Hi there" + state["greeting"]
    return state

def regular_greeting_node(state):
    state["greeting"] = "Hello "+ state["greeting"]
    return state

#conditional node
def choose_greeting_node(state):
    return "hi_greeting" if "hi" in state["greeting"] else "regular_greeting"

builder = StateGraph(GreetingState)

builder.add_node("normalize_greeting",normalize_greeting_node)
builder.add_node("hi_greeting",hi_greeting_node)
builder.add_node("regular_greeting",regular_greeting_node)


builder.add_edge(START,"normalize_greeting")
builder.add_conditional_edges("normalize_greeting", 
                              choose_greeting_node, 
                              ["hi_greeting", "regular_greeting"])

builder.add_edge("hi_greeting",END)
builder.add_edge("regular_greeting",END)

#compile and run the graph
graph = builder.compile()
result = graph.invoke({"greeting":"Hi There!"})
print(result)
result = graph.invoke({"greeting":"Good morning"})
print(result)

# visualize the graph
mermaid_png = graph.get_graph(xray=1).draw_mermaid_png()
filename = "conditional_greeting_graph.png"
with open(filename, "wb") as f:
    f.write(mermaid_png)
print(f"Graph visualization saved to {filename}")  

       