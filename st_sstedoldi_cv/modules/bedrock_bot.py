# -*- coding: utf-8 -*-
# Bedrock RAG Bot using a single retrieve_and_generate call
import boto3

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
        llm_arn: str = None,
        rag_type: str = "KNOWLEDGE_BASE", # instead of "EXTERNAL_SOURCES"
    ):
        self.api_key     = api_key
        self.secret_key  = secret_key
        self.agent_id = agent_id
        self.alias_id = alias_id
        self.region      = region
        self.kb_id       = kb_id
        self.llm_id   = llm_id
        self.llm_arn     = llm_arn
        self.rag_type     = rag_type
        self.client      = None
        # self.session_id  = str(uuid.uuid4())
        # if api_key and secret_key:
        #     self._init_client()

    def _init_client(self):
        """Getting LLM ARN of a AWS managed LLM istance"""
        bedrock = boto3.client("bedrock", 
                               region_name=self.region,
                               aws_access_key_id=self.api_key,
                               aws_secret_access_key=self.secret_key)
        
        profiles = bedrock.list_inference_profiles(typeEquals="SYSTEM_DEFINED")["inferenceProfileSummaries"]
        for p in profiles:
            for m in p["models"]:
                if m["modelArn"].endswith("meta.llama3-3-70b-instruct-v1:0"):
                    self.llm_arn = p["inferenceProfileArn"]

        # print(f"Using LLM ARN: {self.llm_arn}")

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
                "type": self.rag_type,
                "knowledgeBaseConfiguration": kb_cfg
            },
            # commented out to avoid session reuse, context is handled by streamlit app
            # sessionId=self.session_id
        )
        # print(response)

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
