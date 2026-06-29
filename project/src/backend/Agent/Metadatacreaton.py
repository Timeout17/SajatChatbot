from project.src.backend.Agent.LLMService import LLMServiceClass


class MetadataCreatonClass():
    @staticmethod
    def create_metadata(response):
        metadata = {
                "model": response.model,
                "tokens_prompt": response.usage.prompt_tokens,
                "tokens_completion": response.usage.completion_tokens,
                "tokens_total": response.usage.total_tokens,
                "response_id": response.id,
                "created": response.created
            }
        
        return metadata