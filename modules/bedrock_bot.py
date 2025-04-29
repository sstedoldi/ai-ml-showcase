# import boto3
# import json
# import uuid

# class AgentBedrockRAGBot:
#     """
#     Bedrock RAG Bot using Amazon Bedrock Agents Runtime.
#     """
#     def __init__(self, api_key=None, secret_key=None, region="us-east-2", agent_id=None, alias_id=None, kb_id=None):
#         self.api_key      = api_key
#         self.secret_key   = secret_key
#         self.region       = region
#         self.agent_id     = agent_id
#         self.alias_id     = alias_id
#         self.kb_id = kb_id
#         self.client       = None
#         self.session_id   = str(uuid.uuid4())
#         if all([self.api_key, self.secret_key]):
#             self._init_agent_client()

#     def _init_agent_client(self):
#         """Inicializa el cliente de Bedrock Agents Runtime."""
#         self.client = boto3.client(
#             "bedrock-agent-runtime",
#             aws_access_key_id     = self.api_key,
#             aws_secret_access_key = self.secret_key,
#             region_name           = self.region
#         )
#         # Si no especificaste agent_id, podrías listar y elegir uno:
#         # agents = self.client.list_agents()["agentSummaries"]
#         # self.agent_id = agents[0]["agentId"]
    
#     def update_credentials(self, api_key: str, secret_key: str, region: str = None):
#         """Actualiza credenciales y reinitializa el cliente."""
#         self.api_key    = api_key
#         self.secret_key = secret_key
#         if region:
#             self.region = region
#         self._init_agent_client()

#     def retrieve(self,
#                  query: str,
#                  knowledge_base_id: str,
#                  top_k: int = 5,
#                  filter_expression: dict = None) -> list:
#         """
#         Consulta la knowledge base en AWS Bedrock y devuelve los top_k resultados.
        
#         :param query: texto de la consulta del usuario
#         :param knowledge_base_id: ID de la KB en Bedrock
#         :param top_k: número de fragmentos a recuperar
#         :param filter_expression: (opcional) diccionario para filtrar metadata
#         :returns: lista de dicts {'text','score','metadata'}
#         """
#         if not self.client:
#             self._init_agent_client()

#         request_payload = {
#             "knowledgeBaseId": knowledge_base_id,
#             "retrievalConfiguration": {
#                 "vectorSearchConfiguration": {
#                     "numberOfResults": top_k
#                 }
#             },
#             "retrievalQuery": {"text": query}
#         }

#         # Si definiste un filtro metadata, lo inyectas:
#         if filter_expression:
#             request_payload["retrievalConfiguration"]["vectorSearchConfiguration"]["filter"] = filter_expression

#         response = self.client.retrieve(**request_payload)

#         results = []
#         for item in response.get("retrievalResults", []):
#             content = item.get("content", {})
#             text    = content.get("text") or ""
#             score   = item.get("score")
#             metadata= item.get("metadata", {})

#             results.append({
#                 "text": text,
#                 "score": score,
#                 "metadata": metadata
#             })

#         return results

#     def generate_with_agent(self, text: str, enable_trace: bool = False, end_session: bool = False) -> str:
#         """
#         Invoca el agente de Bedrock.
#         """
#         if not self.client:
#             self._init_agent_client()

#         response = self.client.invoke_agent(
#             agentId       = self.agent_id,
#             agentAliasId  = self.alias_id, 
#             sessionId     = self.session_id,
#             enableTrace   = enable_trace,
#             inputText     = text,
#             endSession    = end_session
#         )
#         print(response)
#         # Extraemos el texto de la respuesta:
#         chunks = response.get("chunks", [])
#         if not chunks:
#             return ""
#         # Suponemos un solo chunk con la respuesta final:
#         output_bytes = chunks[-1].get("bytes", b"")
#         return output_bytes.decode("utf-8")

#     def rag_query(self, user_query: str, top_k: int = 5) -> str:
#         # 1. Recupero top_k fragmentos del KB:
#         docs = self.retrieve(
#             query=user_query,
#             knowledge_base_id=self.kb_id,
#             top_k=top_k
#         )
#         # 2. Construyo contexto:
#         context = "\n".join([d["text"] for d in docs])
#         prompt  = f"Context:\n{context}\n\nUser: {user_query}\nAssistant:"
#         # 3. Invoco al agente para generar respuesta:
#         return self.generate_with_agent(prompt, enable_trace=True, end_session=True)
    
import boto3
import uuid

class AgentBedrockRAGBot:
    """
    Bedrock RAG Bot using a single retrieve_and_generate call.
    """
    def __init__(
        self,
        api_key: str,
        secret_key: str,
        agent_id: str,
        alias_id: str,
        region: str = "us-east-1",
        kb_id: str = None,
        llm_id: str = None,
    ):
        self.api_key     = api_key
        self.secret_key  = secret_key
        self.agent_id = agent_id
        self.alias_id = alias_id
        self.region      = region
        self.kb_id       = kb_id
        self.llm_id   = llm_id
        self.client      = None
        self.session_id  = str(uuid.uuid4())
        if api_key and secret_key:
            self._init_client()

    def _init_client(self):
        """Getting LLM ARN to """
        bedrock = boto3.client("bedrock", self.region)
        models  = bedrock.list_foundation_models()["modelSummaries"]
        self.llm_arn = next(
            (m["modelArn"] for m in models 
            if m["modelId"] == "meta.llama3-3-70b-instruct-v1:0"),
            None
        )

        """Initialize the Bedrock Agents Runtime client."""
        self.client = boto3.client(
            "bedrock-agent-runtime",
            aws_access_key_id     = self.api_key,
            aws_secret_access_key = self.secret_key,
            region_name           = self.region
        )

    def update_credentials(self, api_key: str, secret_key: str, region: str = None):
        """Update credentials and re‐initialize the client."""
        self.api_key    = api_key
        self.secret_key = secret_key
        if region:
            self.region = region
        self._init_client()

    def retrieve_and_generate(
        self,
        query: str,
        top_k: int = 5,
        filter_expression: dict = None,
        inference_config: dict = None,
        prompt_template: str = None
    ) -> dict:
        """
        Single API call to retrieve relevant KB chunks and generate a response.

        :param query: the user's question
        :param top_k: how many chunks to fetch
        :param filter_expression: optional metadata filter
        :param inference_config: optional {'maxTokens':…, 'temperature':…, etc.}
        :param prompt_template: optional template string (must include $search_results$ and/or $input$)
        :returns: the raw response dict from retrieve_and_generate
        """
        if not self.client:
            self._init_client()

        # Build vector‐search portion
        vector_cfg = {"numberOfResults": top_k}
        if filter_expression:
            vector_cfg["filter"] = filter_expression

        # Build knowledgeBaseConfiguration
        kb_cfg = {
            "knowledgeBaseId": self.kb_id,
            "modelArn": self.llm_arn,
            "retrievalConfiguration": {
                "vectorSearchConfiguration": vector_cfg
            }
        }

        # Optionally add generation settings
        gen_cfg = {}
        if inference_config:
            gen_cfg.setdefault("inferenceConfig", {})["textInferenceConfig"] = inference_config
        if prompt_template:
            gen_cfg.setdefault("promptTemplate", {})["textPromptTemplate"] = prompt_template

        if gen_cfg:
            kb_cfg["generationConfiguration"] = gen_cfg

        response = self.client.retrieve_and_generate(
            input={"text": query},
            retrieveAndGenerateConfiguration={
                "knowledgeBaseConfiguration": kb_cfg
            },
            # reuse the same session to preserve context
            sessionId=self.session_id
        )

        return response

    def rag_query(
        self,
        user_query: str,
        top_k: int = 5,
        filter_expression: dict = None,
        inference_config: dict = None,
        prompt_template: str = None
    ) -> str:
        """
        Wrapper that returns just the generated text from retrieve_and_generate.
        """
        resp = self.retrieve_and_generate(
            query=user_query,
            top_k=top_k,
            filter_expression=filter_expression,
            inference_config=inference_config,
            prompt_template=prompt_template,
        )
        # The generated answer lives under resp['output']['text']
        return resp.get("output", {}).get("text", "").strip()
