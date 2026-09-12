from langgraph.graph import StateGraph

from agents.state import ProductWorkflowState

from agents.nodes import (
    review_node,
    description_node,
    tags_node,
    save_node,
    should_generate_content
)


workflow = StateGraph(
    ProductWorkflowState
)

workflow.add_node(
    "review",
    review_node
)

workflow.add_node(
    "description",
    description_node
)

workflow.add_node(
    "tags",
    tags_node
)

workflow.add_node(
    "save",
    save_node
)

workflow.set_entry_point(
    "review"
)

workflow.add_conditional_edges(
    "review",
    should_generate_content,
    {
        "description": "description",
        "save": "save"
    }
)

workflow.add_edge(
    "description",
    "tags"
)

workflow.add_edge(
    "tags",
    "save"
)

workflow.set_finish_point(
    "save"
)

graph = workflow.compile()