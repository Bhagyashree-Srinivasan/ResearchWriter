"""Markdown processing utilities."""

from typing import Dict, List, Tuple

def markdown_collapsible(title: str, body: str) -> str:
    """Return a markdown collapsible block using <details> / <summary>."""
    return f"<details>\n<summary>{title}</summary>\n\n{body.strip()}\n\n</details>\n"

def get_first_line_title(markdown: str) -> str:
    """
    Get the 1st non-empty line of markdown, remove the leading '#' and whitespace.
    If not found, return 'Untitled'.
    """
    for line in markdown.splitlines():
        line = line.strip()
        if line:
            return line.lstrip("#").strip() or "Untitled"
    return "Untitled"

def build_research_results_section(grouped_queries: Dict[str, List[str]]) -> str:
    """
    Build the Research Results section from grouped perplexity query results.
    
    Args:
        grouped_queries: Dict mapping query strings to lists of result blocks.
        
    Returns:
        Formatted markdown string for research results section
    """
    research_results_blocks: List[str] = []
    for query, blocks in grouped_queries.items():
        body = "\n\n-----\n\n".join(blocks)
        research_results_blocks.append(
            markdown_collapsible(query, body))
    
    if research_results_blocks:
        return "## Research Results\n\n" + "\n\n".join(research_results_blocks)
    else:
        return "## Research Results\n\n_No accepted research results found._\n"
    
def build_sources_section(section_title: str, sources: List[Tuple[str, str]], empty_message: str) -> str:
    """
    Build a sources section from a list of title-body pairs.
    
    Args:
        section_title: The title of the section (e.g. "## Code Sources").
        sources: List of tuples (title, body) for each source.
        empty_message: Message to display if there are no sources.
        
    Returns:
        Formatted markdown string for the sources section.
    """
    if sources:
        blocks = [markdown_collapsible(title, body) for title, body in sources]
        return f"{section_title}\n\n" + "\n".join(blocks)
    else:
        return f"{section_title}\n\n_{empty_message}_\n"
    
def combine_research_sections(
    research_results_section: str,
    sources_scraped_section: str,
    code_sources_section: str,
    youtube_transcripts_section: str,
    additional_sources_section: str,
    additional_sources_section: str
) -> str:
    """
    Combine all research sections into a single markdown string.
    
    Args:
        research_results_section: Markdown for the Research Results section.
        sources_scraped_section: Markdown for the Sources Scraped section.
        code_sources_section: Markdown for the Code Sources section.
        youtube_transcripts_section: Markdown for the YouTube Transcripts section.
        additional_sources_section: Markdown for the Additional Sources section.
        
    Returns:
        Combined markdown string for all research sections.
    """
    return "\n\n".join([
        "# Research", # Main header for the entire research section
        research_results_section,
        sources_scraped_section,
        code_sources_section,
        youtube_transcripts_section,
        additional_sources_section
    ])
                                            
    
    