from __future__ import annotations

import json
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Set

import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Chunk:
    topic: str
    section: str
    text: str
    source: str


class _HTMLToText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: List[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self._skip_depth > 0:
            self._skip_depth -= 1
        if tag in {"p", "br", "li", "h1", "h2", "h3", "h4"}:
            self._parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth > 0:
            return
        text = data.strip()
        if text:
            self._parts.append(text)

    def text(self) -> str:
        raw = " ".join(self._parts)
        raw = re.sub(r"\s+", " ", raw)
        raw = raw.replace(" \n ", "\n").replace(" \n", "\n").replace("\n ", "\n")
        return raw.strip()


class CourseKnowledgeBase:
    # 404/无效页面的特征关键词列表
    INVALID_PAGE_MARKERS = [
        "未找到页面",
        "404",
        "没有找到",
        "页面不存在",
        "已删除",
        "404 NOT FOUND",
        "File Not Found",
        "Page Not Found",
    ]
    
    def __init__(self, cache_dir: str) -> None:
        self.cache_dir = Path(cache_dir)
        self.chunks: List[Chunk] = []
        self.vectorizer: TfidfVectorizer | None = None
        self.matrix = None
        # 本地课程资料路径（相对于项目根目录）
        self.local_materials_dir = Path(__file__).parent.parent / "course_materials"
        self.url_map = {
            # 本地课程资料文件（确保知识准确性）
            "stack_queue": "local://course_materials/stack_queue.md",
            "linked_list": "local://course_materials/linked_list.md",
            "tree": "local://course_materials/tree.md",
            "graph": "local://course_materials/graph.md",
            "sorting": "local://course_materials/sorting.md",
            "recursion_search": "local://course_materials/recursion_search.md",
            "hash_table": "local://course_materials/hash_table.md",
            "advanced_tree": "local://course_materials/advanced_tree.md",
            "advanced_graph": "local://course_materials/advanced_graph.md",
            "heap_storage": "local://course_materials/heap_storage.md",
            # 网页链接（作为补充资源）
            "web_linear": "https://www.runoob.com/data-structures/dsa-linear-data-structures.html",
            "web_hash": "https://www.runoob.com/data-structures/dsa-hash-table.html",
            "web_tree": "https://www.runoob.com/data-structures/dsa-tree.html",
            "web_graph": "https://www.runoob.com/data-structures/dsa-graph.html",
            "web_advanced_tree": "https://www.runoob.com/data-structures/dsa-advanced-tree.html",
            "web_advanced_graph": "https://www.runoob.com/data-structures/dsa-advanced-graph.html",
            "web_heap": "https://www.runoob.com/data-structures/heap-storage.html",
        }
        self.topic_keywords = {
            "stack_queue": ["栈", "队列", "递归", "括号"],
            "linked_list": ["链表", "结点", "指针"],
            "tree": ["树", "二叉树", "遍历", "前序", "中序", "后序"],
            "graph": ["图", "顶点", "边", "dfs", "bfs", "最短路径"],
            "sorting": ["排序", "快速排序", "归并", "冒泡", "稳定性"],
            "recursion_search": ["递归", "查找", "二分", "搜索", "哈希"],
            "hash_table": ["哈希", "散列", "哈希函数", "冲突", "链地址", "开放定址"],
            "advanced_tree": ["AVL", "红黑树", "B 树", "B+ 树", "平衡", "旋转"],
            "advanced_graph": ["Dijkstra", "最小生成树", "Prim", "拓扑排序", "网络流"],
            "heap_storage": ["堆", "优先队列", "完全二叉树", "最大堆", "最小堆"],
        }
        self.loaded_topics: Set[str] = set()
        self._load_local_materials()
        self._load_cache_only()
        self._rebuild_index()

    def _load_cache_only(self) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path = self.cache_dir / "web_kb_cache.json"
        if not cache_path.exists():
            return
        try:
            cached: Dict[str, Dict[str, str]] = json.loads(cache_path.read_text(encoding="utf-8"))
        except Exception:
            return
        for topic, page in cached.items():
            text = page.get("text", "")
            url = page.get("url", self.url_map.get(topic, ""))
            if not text:
                continue
            # 检查是否为无效页面（404 等错误页面）
            if self._is_invalid_page(text):
                continue
            self._append_topic_chunks(topic, text, url)
            self.loaded_topics.add(topic)

    def _load_local_materials(self) -> None:
        """加载本地课程资料文件"""
        if not self.local_materials_dir.exists():
            return
        
        for topic in self.url_map.keys():
            material_file = self.local_materials_dir / f"{topic}.md"
            if material_file.exists():
                try:
                    text = material_file.read_text(encoding="utf-8")
                    text = self._clean_text(text)
                    if text:
                        self._append_topic_chunks(topic, text, f"local://{topic}.md")
                        self.loaded_topics.add(topic)
                except Exception:
                    continue

    def _fetch_topic(self, topic: str, timeout_sec: int = 4, use_web: bool = True) -> None:
        """加载主题知识
        
        Args:
            topic: 主题名称
            timeout_sec: 网络请求超时时间
            use_web: 是否允许从网页抓取（默认 True）
        """
        if topic in self.loaded_topics:
            return
        
        # 首先尝试直接匹配
        if topic in self.url_map:
            self._load_topic_url(topic, self.url_map[topic], timeout_sec, use_web)
            return
        
        # 如果没有直接匹配，尝试查找 web_前缀的网页链接
        web_topic = f"web_{topic}"
        if web_topic in self.url_map:
            self._load_topic_url(web_topic, self.url_map[web_topic], timeout_sec, use_web)
    
    def _load_topic_url(self, topic: str, url: str, timeout_sec: int, use_web: bool) -> None:
        """加载指定 URL 的主题内容
        
        Args:
            topic: 主题名称
            url: URL 地址
            timeout_sec: 超时时间
            use_web: 是否允许网页抓取
        """
        # 如果是本地文件，直接从本地加载
        if url.startswith("local://"):
            material_file = self.local_materials_dir / f"{topic}.md"
            if not material_file.exists():
                # 尝试不带 web_前缀的文件
                if topic.startswith("web_"):
                    material_file = self.local_materials_dir / f"{topic[4:]}.md"
                if not material_file.exists():
                    return
            try:
                text = material_file.read_text(encoding="utf-8")
                text = self._clean_text(text)
                if not text or self._is_invalid_page(text):
                    return
                self._append_topic_chunks(topic, text, url)
                self.loaded_topics.add(topic)
            except Exception:
                return
            return
        
        # 如果禁用网页抓取，直接返回
        if not use_web:
            return
        
        # 否则从网络抓取
        try:
            response = requests.get(url, timeout=timeout_sec)
            if response.status_code != 200:
                return
            html = response.text
            extractor = _HTMLToText()
            extractor.feed(html)
            text = self._clean_text(extractor.text())
            if not text:
                return
            # 检查是否为无效页面（404 等错误页面）
            if self._is_invalid_page(text):
                return
            self._append_topic_chunks(topic, text, url)
            self.loaded_topics.add(topic)
            self._update_cache(topic, {"url": url, "text": text})
            self._rebuild_index()
        except Exception:
            return

    def _append_topic_chunks(self, topic: str, text: str, url: str) -> None:
        for i, chunk_text in enumerate(self._chunk_text(text, chunk_size=500, overlap=80), start=1):
            self.chunks.append(
                Chunk(
                    topic=topic,
                    section=f"web_chunk_{i}",
                    text=chunk_text,
                    source=url,
                )
            )

    def _rebuild_index(self) -> None:
        if not self.chunks:
            self.vectorizer = None
            self.matrix = None
            return
        corpus = [f"{chunk.topic} {chunk.section} {chunk.text}" for chunk in self.chunks]
        self.vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
        self.matrix = self.vectorizer.fit_transform(corpus)

    def _update_cache(self, topic: str, page: Dict[str, str]) -> None:
        cache_path = self.cache_dir / "web_kb_cache.json"
        cache: Dict[str, Dict[str, str]] = {}
        if cache_path.exists():
            try:
                cache = json.loads(cache_path.read_text(encoding="utf-8"))
            except Exception:
                cache = {}
        cache[topic] = page
        try:
            cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            return

    def _guess_topics(self, query: str) -> List[str]:
        q = query.lower()
        if q in self.url_map:
            return [q]
        hits: List[str] = []
        for topic, words in self.topic_keywords.items():
            if any(w.lower() in q for w in words):
                hits.append(topic)
        if hits:
            return hits[:2]
        return ["stack_queue", "tree"]

    @staticmethod
    def _clean_text(text: str) -> str:
        # 仅做轻量清洗：去除过短/明显导航类片段，保留正文可检索信息
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def _is_invalid_page(text: str) -> bool:
        """检查页面是否为无效页面（404 等错误页面）"""
        text_lower = text.lower()
        
        # 检查是否是 404 页面或导航页面
        # 必须是独立的错误提示，而不是内容中的普通词汇
        invalid_patterns = [
            "未找到页面",
            "404 not found",
            "404",
            "没有找到该页面",
            "页面不存在",
            "已删除，请返回",
            "page not found",
            "file not found",
        ]
        
        for pattern in invalid_patterns:
            if pattern.lower() in text_lower:
                # 进一步确认：如果是 404 等错误，通常会在文本开头或结尾
                if text_lower.index(pattern.lower()) < 200 or pattern in ["404", "404 not found", "page not found"]:
                    return True
        
        return False

    def clean_invalid_cache(self) -> int:
        """清理缓存中的无效页面，返回清理的数量"""
        cache_path = self.cache_dir / "web_kb_cache.json"
        if not cache_path.exists():
            return 0
        
        try:
            cached: Dict[str, Dict[str, str]] = json.loads(cache_path.read_text(encoding="utf-8"))
        except Exception:
            return 0
        
        cleaned_count = 0
        valid_cache = {}
        
        for topic, page in cached.items():
            text = page.get("text", "")
            if not text or self._is_invalid_page(text):
                cleaned_count += 1
            else:
                valid_cache[topic] = page
        
        # 只保留有效页面
        if cleaned_count > 0:
            try:
                cache_path.write_text(
                    json.dumps(valid_cache, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
            except Exception:
                pass
        
        return cleaned_count

    @staticmethod
    def _chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
        if chunk_size <= 0:
            return [text]
        if overlap >= chunk_size:
            overlap = max(0, chunk_size // 5)
        chunks: List[str] = []
        start = 0
        while start < len(text):
            end = min(len(text), start + chunk_size)
            piece = text[start:end].strip()
            if piece:
                chunks.append(piece)
            if end == len(text):
                break
            start = max(0, end - overlap)
        return chunks

    def retrieve(self, query: str, top_k: int = 4, use_web: bool = True) -> List[Chunk]:
        """检索相关知识片段
        
        Args:
            query: 查询问题
            top_k: 返回最相关的 k 个片段
            use_web: 是否启用实时网页检索（默认 True）
        
        Returns:
            相关的知识片段列表
        """
        # 按需加载：仅抓取与当前问题最相关的少量网页，避免启动或检索卡死
        for topic in self._guess_topics(query):
            self._fetch_topic(topic, use_web=use_web)
        
        if not self.vectorizer or self.matrix is None:
            return []
        
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix).flatten()
        ranked_indices = scores.argsort()[::-1][:top_k]
        return [self.chunks[i] for i in ranked_indices if scores[i] > 0]
    
    def retrieve_from_web(self, query: str, timeout_sec: int = 5) -> List[Chunk]:
        """直接从网页实时检索知识（不依赖缓存）
        
        Args:
            query: 查询问题
            timeout_sec: 网页请求超时时间（秒）
        
        Returns:
            从网页获取的知识片段列表
        """
        topics = self._guess_topics(query)
        web_chunks = []
        
        # 主题到网页链接的映射
        topic_to_web = {
            "stack_queue": "web_linear",
            "hash_table": "web_hash",
            "tree": "web_tree",
            "graph": "web_graph",
            "advanced_tree": "web_advanced_tree",
            "advanced_graph": "web_advanced_graph",
            "heap_storage": "web_heap",
        }
        
        for topic in topics:
            # 尝试查找对应的网页链接
            web_topic = topic_to_web.get(topic)
            if not web_topic or web_topic not in self.url_map:
                continue
            
            url = self.url_map[web_topic]
            
            try:
                # 实时抓取网页
                response = requests.get(url, timeout=timeout_sec)
                if response.status_code != 200:
                    continue
                
                html = response.text
                extractor = _HTMLToText()
                extractor.feed(html)
                text = self._clean_text(extractor.text())
                
                if not text or self._is_invalid_page(text):
                    continue
                
                # 创建临时片段（不保存到缓存）
                for i, chunk_text in enumerate(self._chunk_text(text, chunk_size=500, overlap=80), start=1):
                    web_chunks.append(
                        Chunk(
                            topic=web_topic,
                            section=f"web_realtime_{i}",
                            text=chunk_text,
                            source=url,
                        )
                    )
            except Exception:
                continue
        
        # 如果有网页内容，进行检索排序
        if web_chunks:
            try:
                corpus = [f"{chunk.topic} {chunk.section} {chunk.text}" for chunk in web_chunks]
                web_vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
                web_matrix = web_vectorizer.fit_transform(corpus)
                web_query_vector = web_vectorizer.transform([query])
                web_scores = cosine_similarity(web_query_vector, web_matrix).flatten()
                web_ranked_indices = web_scores.argsort()[::-1][:4]
                return [web_chunks[i] for i in web_ranked_indices if web_scores[i] > 0]
            except Exception:
                return web_chunks[:4]
        
        return []

    def all_topics(self) -> List[str]:
        return list(self.url_map.keys())
