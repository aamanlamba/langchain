from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables.graph import MermaidDrawMethod
import random
import os
import subprocess
import sys

# define state
class HelloAgentState(TypedDict):
    greeting: str

def hello_agent_node(state:HelloAgentState =  "Hello from HelloAgent!") -> HelloAgentState:
    print(state["greeting"])
    return state

def exclamation_node(state:HelloAgentState) -> HelloAgentState:
    state["greeting"] += "!!!"
    return state

# initialize graph
builder = StateGraph(HelloAgentState)
builder.add_node("greet",hello_agent_node)
builder.add_node("exclaim",exclamation_node)

builder.add_edge(START, "greet")
builder.add_edge("greet","exclaim")
builder.add_edge("exclaim",END)

# compile and run the graph
graph = builder.compile()
result = graph.invoke({"greeting": "from LangGraph!"})

print(result)

mermaid_png = graph.get_graph(xray=1).draw_mermaid_png(draw_method=MermaidDrawMethod.API)
filename = os.path.join(os.path.dirname(__file__), "hello_agent_graph.png")
with open(filename, "wb") as f:
    f.write(mermaid_png)
if sys.platform.startswith('darwin'): 
    subprocess.call(('open', filename)) 
elif sys.platform.startswith('linux'): 
    subprocess.call(('xdg-open', filename)) 
elif sys.platform.startswith('win'): 
    os.startfile(filename)


