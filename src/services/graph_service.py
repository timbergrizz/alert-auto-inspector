from typing import Dict, Any, List, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from models.canonical import CanonicalAlert
from services.vector_db_service import VectorDBService
from core.llm import generate_response, get_plan

class GraphState(TypedDict):
    alert: CanonicalAlert
    plan: List[Dict[str, Any]]
    context_documents: List[str]
    response: str

class GraphService:
    def __init__(self, vector_db_service: VectorDBService):
        self.vector_db_service = vector_db_service
        self.workflow = self._build_graph()

    def _generate_plan(self, state: GraphState) -> dict:
        plan = get_plan(state['alert'])
        return {"plan": plan}

    def _retrieve_context(self, state: GraphState) -> dict:
        plan_str = " ".join([msg['content'] for msg in state['plan'] if msg['content'] is not None])
        query_text = f"{state['alert'].title} {state['alert'].service} {plan_str}"
        context_results = self.vector_db_service.query_documents(query_texts=[query_text])
        documents = context_results.get('documents', [[]])[0]
        return {"context_documents": documents}

    def _generate_response(self, state: GraphState) -> dict:
        response = generate_response(state['alert'], state['context_documents'], state['plan'])
        return {"response": response}

    def _build_graph(self) -> CompiledStateGraph:
        graph = StateGraph(GraphState)
        graph.add_node("generate_plan", self._generate_plan)
        graph.add_node("retrieve_context", self._retrieve_context)
        graph.add_node("generate_response", self._generate_response)
        graph.set_entry_point("generate_plan")
        graph.add_edge("generate_plan", "retrieve_context")
        graph.add_edge("retrieve_context", "generate_response")
        graph.add_edge("generate_response", END)

        return graph.compile()

    def run(self, alert: CanonicalAlert) -> str:
        initial_state: GraphState = {"alert": alert, "plan": [], "context_documents": [], "response": ""}
        final_state = self.workflow.invoke(initial_state)
        return final_state["response"]
