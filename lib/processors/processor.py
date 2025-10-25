import re
from typing import List, Dict, Any




class DataProcessor:
    def __init__(self):
        self.article_pattern = re.compile(r'Статья\s+(\d+(?:\.\d+)?)\s*\n(.+?)(?=Статья\s+\d|Раздел|Глава|$)',re.DOTALL)
        self.chapter_pattern = re.compile(r'Глава\s+(\d+)\.\s*(.+?)\s*\n')
        self.section_pattern = re.compile(r'Раздел\s+[А-Яа-я]+\s*\n')
    def process(self, text) -> List[Dict[str, Any]]:
        chunks = []

        preambule_chunk = self.process_preamble(text=text)
        
        if preambule_chunk:
            chunks.append(preambule_chunk)

        article_chunks = self.process_articles(text=text)

        if article_chunks:
            chunks.extend(article_chunks)
        
        return chunks

    def process_preamble(self, text: str) -> Dict[str, Any]:
        preamble_end = text.find("Раздел первый")
        preamble_text = text[:preamble_end] if preamble_end != -1 else text

        preamble_clean = self.clean_data(self, text=preamble_text)

        return {
            "text": preamble_clean,
            "metadata":{
                "document": "RF Constitution",
                "document_part": "Preamble",
                "section": None,
                "artcile": None,
                "chapter": None
            }
        }
    
    def process_articles(self, text: str) -> List[Dict[str, Any]]:
        chunks = []
        sections = list(self.section_pattern.finditer(text))
        chapters = list(self.chapter_pattern.finditer(text))
        articles = list(self.article_pattern.finditer(text))
    
        

        for chapter_match in self.chapter_pattern.finditer(text):
            current_section = "Раздел первый"
            for section in sections:
                if section.start() < chapter_match.start():
                    current_section = self.clean_text(section.group(0))
                else:
                    break
            chapter_chunk = {"text": f"Глава {chapter_match.group(1)}. {self.clean_text(chapter_match.group(2))}",
                             "metadata": {
                                "document": "RF Constitution",
                                "document_part": "Chapter",
                                "chapter": chapter_match.group(1),
                                "article": None,
                                "section": current_section
                                }
                             }
            chunks.append(chapter_chunk)
            #chapter_chunks[match.group(1)] =  f"Глава {match.group(1)}. {self.clean_text(match.group(2))}",
                          

        for article_match in self.article_pattern.finditer(text):
        
        
            current_section = "Раздел первый"
            for section in sections:
                if section.start() < article_match.start():
                    current_section = self.clean_text(section.group(0))
                else:
                    break

            current_chapter = None
            for chapter in chapters:
                if chapter.start() < article_match.start():
                    current_chapter = self.clean_text(chapter.group(0))
                else:
                    break
            article_chunk = {"text": self.clean_text(article_match.group(2)),
                             "metadata": {
                                "document": "RF Constitution",
                                "document_part": "Article",
                                "chapter": current_chapter,
                                "article": article_match.group(1),
                                "section": current_section
                                }
                             }
            chunks.append(article_chunk)

        return chunks
    def clean_text(self, text:str) -> str:
        text = re.sub(r"\n+", ' ', text)
        text = re.sub (r"\s+", ' ', text)

        return text
    