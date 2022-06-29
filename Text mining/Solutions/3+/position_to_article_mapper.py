import os


class PositionToArticleMapper:
    def set_first_position_for_article(self, article_id: int, position: int):
        raise NotImplementedError

    def save_first_positions(self):
        raise NotImplementedError

    def get_article_id_for_position(self, desired_position: int) -> int:
        raise NotImplementedError


class FilePositionToArticleMapper(PositionToArticleMapper):
    def __init__(self, first_positions_path: str):
        self.first_positions_path = first_positions_path
        self.first_positions = self.get_first_positions()

    @staticmethod
    def parse_article_id_and_first_position(line: str) -> tuple[int, int]:
        article_id, first_position = map(int, line.split())
        return article_id, first_position

    def load_first_positions(self) -> list[tuple[int, int]]:
        with open(self.first_positions_path, encoding='utf8') as file:
            return list(map(FilePositionToArticleMapper.parse_article_id_and_first_position,
                            file.readlines()))

    def get_first_positions(self) -> list[tuple[int, int]]:
        if os.path.isfile(self.first_positions_path):
            return self.load_first_positions()
        else:
            return []

    def set_first_position_for_article(self, article_id: int, position: int):
        self.first_positions.append((article_id, position))

    def first_positions_to_string(self) -> str:
        return '\n'.join(f'{article_id} {first_position}'
                         for article_id, first_position in self.first_positions)

    def save_first_positions(self):
        with open(self.first_positions_path, 'w', encoding='utf8') as file:
            file.write(self.first_positions_to_string())

    def get_article_id_for_position(self, desired_position: int) -> int:
        a = 0
        b = len(self.first_positions)

        while a < b - 1:
            mid = (a + b) // 2
            _, position = self.first_positions[mid]

            if desired_position < position:
                b = mid
            else:  # position <= desired_position
                a = mid

        return self.first_positions[a][0]
