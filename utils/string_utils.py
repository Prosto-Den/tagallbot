import re


class StringUtils:
    @staticmethod
    def find_substring_by_re(text: str, pattern: str) -> re.Match[str] | None:
        return re.search(pattern, text)
