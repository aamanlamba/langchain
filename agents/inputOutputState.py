from typing_extensions import TypedDict 
from langgraph.graph import StateGraph, START, END

# Define the input and output types for the overall state 
class OverallState(TypedDict):
     partial_message: str 
     user_input: str 
     message_output: str

class InputState(TypedDict):
    user_input: str

class OutputState(TypedDict):
    message_output: str

class PrivateState(TypedDict):
    _private_message: str

def add_world(state: InputState) -> OverallState:
    partial_message = state["user_input"] + " World"
    print("Added World:", partial_message)
    return {"partial_message": partial_message, 
            "user_input": state["user_input"], 
            "message_output":""}

def add_exclamation(state: OverallState) -> PrivateState:
    _private_message = state["partial_message"] + "!"
    print("Added Exclamation:", _private_message)
    return {"_private_message": _private_message}

def finalize_message(state: PrivateState) -> OutputState:
    message_output = state["_private_message"]
    print("Finalized Message:", message_output)
    return {"message_output": message_output}   

# Build the state graph
builder = StateGraph(OverallState, input=InputState, output=OutputState)
builder.add_node("add_world", add_world)
builder.add_node("add_exclamation", add_exclamation)
builder.add_node("finalize_message", finalize_message)
builder.add_edge(START, "add_world")
builder.add_edge("add_world", "add_exclamation")
builder.add_edge("add_exclamation", "finalize_message")
builder.add_edge("finalize_message", END)
# compile and run the graph
graph = builder.compile()
initial_input: InputState = {"user_input": "Hello"}
final_output = graph.invoke(initial_input)
print("Final Output:", final_output)
# visualize the graph
mermaid_png = graph.get_graph(xray=1).draw_mermaid_png()
filename = "input_output_state_graph.png"
with open(filename, "wb") as f:
    f.write(mermaid_png)
print(f"Graph visualization saved to {filename}")  


