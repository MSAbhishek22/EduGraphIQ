import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(filepath):
    try:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text_chunks = []
            
            # Extract all text first with better structure preservation
            full_text = ""
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                # Add page markers for better section identification
                full_text += f"\n=== Page {page_num} ===\n{page_text}"
            
            # Define important section markers
            section_markers = [
                'introduction', 'overview', 'features', 'technology stack',
                'business model', 'key features', 'architecture',
                'implementation', 'conclusion', 'summary'
            ]
            
            # First pass: identify major sections
            sections = []
            current_section = {'title': '', 'content': []}
            
            for line in full_text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                    
                # Check if line is a section header
                is_header = (
                    line.isupper() or
                    any(marker in line.lower() for marker in section_markers) or
                    (len(line) < 50 and line.endswith(':')) or
                    line.startswith('•') or
                    line.startswith('-')
                )
                
                if is_header:
                    # Save previous section if it exists
                    if current_section['title'] and current_section['content']:
                        sections.append(current_section)
                    # Start new section
                    current_section = {'title': line, 'content': []}
                else:
                    current_section['content'].append(line)
            
            # Don't forget the last section
            if current_section['title'] and current_section['content']:
                sections.append(current_section)
            
            # Second pass: create structured chunks
            for section in sections:
                title = section['title'].strip('•-: ')
                content = '\n'.join(section['content'])
                
                # Split long content into sub-sections
                if len(content) > 1000:
                    sentences = content.split('. ')
                    chunk_size = max(3, len(sentences) // 3)  # At least 3 sentences per chunk
                    
                    for i in range(0, len(sentences), chunk_size):
                        chunk_sentences = sentences[i:i + chunk_size]
                        sub_title = f"{title} (Part {i//chunk_size + 1})"
                        text_chunks.append({
                            'title': sub_title,
                            'content': '. '.join(chunk_sentences)
                        })
                else:
                    text_chunks.append({
                        'title': title,
                        'content': content
                    })
            
            return text_chunks if text_chunks else None
            
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        return None