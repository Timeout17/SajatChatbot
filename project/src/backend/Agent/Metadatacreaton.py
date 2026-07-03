from project.src.backend.models.Metadata import Metadata

class MetadataCreatonClass:

    @staticmethod
    def create_metadata(response):
        return Metadata(
            model=response.model,
            tokens_prompt=response.usage.prompt_tokens,
            tokens_completion=response.usage.completion_tokens,
            tokens_total=response.usage.total_tokens,
            response_id=response.id,
            created=response.created
        )