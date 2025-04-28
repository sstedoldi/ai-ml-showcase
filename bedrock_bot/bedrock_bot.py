import boto3

class BedrockRAGBot:
    """
    A simple Bedrock RAG Bot using AWS Bedrock with Llama 3.3 70B Instruct.
    """
    def __init__(self, api_key=None, region="us-east-2", model_id="meta-llama-3-70b-instruct"):
        self.api_key = api_key
        self.region = region
        self.model_id = model_id
        self.client = None
        if self.api_key:
            self._init_client()

    def _init_client(self):
        """Initialize the Bedrock Runtime client."""
        self.client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=self.api_key,
            region_name=self.region
        )

    def update_credentials(self, api_key: str, region: str):
        """Update AWS credentials and reinitialize client."""
        self.api_key = api_key
        self.region = region
        self._init_client()

    def retrieve(self, query: str, top_k: int = 5) -> list:
        """
        Retrieve relevant documents from your vector store or knowledge base.
        Stub: replace with your retrieval engine logic.
        """
        return []

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Invoke the Llama 3.3 70B Instruct model via AWS Bedrock.
        """
        if not self.client:
            self._init_client()
        # Bedrock expects JSON body with 'prompt'
        payload = {"prompt": prompt}
        payload.update(kwargs)
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=payload
        )
        output = response["body"].read().decode("utf-8")
        return output

    def rag_query(self, user_query: str, top_k: int = 5) -> str:
        """
        Perform a Retrieval-Augmented Generation query:
          1. Retrieve context docs
          2. Build augmented prompt
          3. Generate completion using Llama Instruct
        """
        docs = self.retrieve(user_query, top_k)
        context = "\n".join([d.get("text", "") for d in docs])
        augmented_prompt = f"Context:\n{context}\n\nUser: {user_query}\nAssistant:"
        return self.generate(augmented_prompt)