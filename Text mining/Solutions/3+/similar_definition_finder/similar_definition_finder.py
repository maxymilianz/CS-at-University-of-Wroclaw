from definition import Definition

from collections.abc import Sequence


class SimilarDefinitionFinder:
    def get_similar_definitions(self, description: str) -> Sequence[Definition]:
        raise NotImplementedError
