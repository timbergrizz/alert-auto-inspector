from typing import Dict, Any, List, TypedDict
from langgraph.graph import StateGraph, END
from models.canonical import CanonicalAlert
from services.vector_db_service import VectorDBService
from core.llm import get_explanation

class GraphState(TypedDict):
    alert: CanonicalAlert
    context_documents: List[str]
    explanation: str

class GraphService:
    def __init__(self, vector_db_service: VectorDBService):
        self.vector_db_service = vector_db_service
        self.workflow = self._build_graph()

    def _retrieve_context(self, state: GraphState) -> dict:
        query_text = f"{state['alert'].title} {state['alert'].service}"
        context_results = self.vector_db_service.query_documents(query_texts=[query_text])
        documents = context_results.get('documents', [[]])[0]
        return {"context_documents": documents}

    def _generate_explanation(self, state: GraphState) -> dict:
        explanation = get_explanation(state['alert'], state['context_documents'])
        return {"explanation": explanation}

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(GraphState)
        graph.add_node("retrieve_context", self._retrieve_context)
        graph.add_node("generate_explanation", self._generate_explanation)
        graph.set_entry_point("retrieve_context")
        graph.add_edge("retrieve_context", "generate_explanation")
        graph.add_edge("generate_explanation", END)
        return graph.compile()

    def run(self, alert: CanonicalAlert) -> str:
        initial_state: GraphState = {"alert": alert, "context_documents": [], "explanation": ""}
        final_state = self.workflow.invoke(initial_state)
        return final_state["explanation"]