import os
from pathlib import Path
from typing import List
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import markdown
from datetime import datetime

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for the PDF"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#2c3e50'),
            alignment=1  # Center alignment
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=HexColor('#34495e'),
            leftIndent=0
        ))
        
        # Subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=15,
            textColor=HexColor('#7f8c8d'),
            leftIndent=20
        ))
        
        # Body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            leading=14,
            leftIndent=0,
            rightIndent=0
        ))
        
        # Insight style
        self.styles.add(ParagraphStyle(
            name='InsightStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            spaceBefore=8,
            leftIndent=30,
            rightIndent=20,
            leading=14,
            borderColor=HexColor('#3498db'),
            borderWidth=0,
            backColor=HexColor('#ecf0f1'),
            borderPadding=10
        ))
    
    async def create_pdf(self, summary: str, insights: List[str], output_path: Path):
        """Create PDF with summary and insights"""
        
        # Create document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build content
        story = []
        
        # Add title page
        story.extend(self._create_title_page())
        
        # Add summary section
        story.extend(self._create_summary_section(summary))
        
        # Add page break
        story.append(PageBreak())
        
        # Add insights section
        story.extend(self._create_insights_section(insights))
        
        # Build PDF
        doc.build(story)
    
    def _create_title_page(self):
        """Create the title page"""
        story = []
        
        # Main title
        story.append(Paragraph("CS300 Lecture Analysis", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.5 * inch))
        
        # Subtitle
        story.append(Paragraph("Automated Summary & Educational Insights", self.styles['Heading2']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Date
        current_date = datetime.now().strftime("%B %d, %Y")
        story.append(Paragraph(f"Generated on: {current_date}", self.styles['Normal']))
        story.append(Spacer(1, 1 * inch))
        
        # Description
        description = """
        This document contains an automated analysis of a CS300 lecture recording. 
        The summary provides key concepts and topics covered during the lecture, 
        while the insights section offers educational feedback and recommendations 
        for instructional improvement.
        """
        story.append(Paragraph(description, self.styles['Normal']))
        
        story.append(PageBreak())
        return story
    
    def _create_summary_section(self, summary: str):
        """Create the summary section"""
        story = []
        
        # Section title
        story.append(Paragraph("📚 Lecture Summary", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Convert markdown to paragraphs
        lines = summary.split('\n')
        current_paragraph = []
        
        for line in lines:
            line = line.strip()
            
            if not line:
                if current_paragraph:
                    story.append(Paragraph(' '.join(current_paragraph), self.styles['CustomBody']))
                    story.append(Spacer(1, 0.1 * inch))
                    current_paragraph = []
                continue
            
            # Handle headers
            if line.startswith('# '):
                if current_paragraph:
                    story.append(Paragraph(' '.join(current_paragraph), self.styles['CustomBody']))
                    current_paragraph = []
                story.append(Paragraph(line[2:], self.styles['CustomHeading']))
                story.append(Spacer(1, 0.1 * inch))
            elif line.startswith('## '):
                if current_paragraph:
                    story.append(Paragraph(' '.join(current_paragraph), self.styles['CustomBody']))
                    current_paragraph = []
                story.append(Paragraph(line[3:], self.styles['CustomSubHeading']))
                story.append(Spacer(1, 0.05 * inch))
            elif line.startswith('### '):
                if current_paragraph:
                    story.append(Paragraph(' '.join(current_paragraph), self.styles['CustomBody']))
                    current_paragraph = []
                story.append(Paragraph(line[4:], self.styles['CustomSubHeading']))
                story.append(Spacer(1, 0.05 * inch))
            elif line.startswith('- ') or line.startswith('* '):
                if current_paragraph:
                    story.append(Paragraph(' '.join(current_paragraph), self.styles['CustomBody']))
                    current_paragraph = []
                story.append(Paragraph(f"• {line[2:]}", self.styles['CustomBody']))
            elif line.startswith(('1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. ')):
                if current_paragraph:
                    story.append(Paragraph(' '.join(current_paragraph), self.styles['CustomBody']))
                    current_paragraph = []
                story.append(Paragraph(line, self.styles['CustomBody']))
            else:
                current_paragraph.append(line)
        
        # Handle remaining paragraph
        if current_paragraph:
            story.append(Paragraph(' '.join(current_paragraph), self.styles['CustomBody']))
        
        return story
    
    def _create_insights_section(self, insights: List[str]):
        """Create the insights section"""
        story = []
        
        # Section title
        story.append(Paragraph("💡 Educational Insights", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Introduction
        intro_text = """
        The following insights are generated through analysis of the lecture content, 
        student interactions, and educational patterns. These recommendations can help 
        improve future lectures and student learning outcomes.
        """
        story.append(Paragraph(intro_text, self.styles['CustomBody']))
        story.append(Spacer(1, 0.2 * inch))
        
        # Add insights
        for i, insight in enumerate(insights, 1):
            # Insight number and content
            insight_title = f"Insight #{i}"
            story.append(Paragraph(insight_title, self.styles['CustomSubHeading']))
            story.append(Paragraph(insight, self.styles['InsightStyle']))
            story.append(Spacer(1, 0.15 * inch))
        
        # Add recommendations section
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph("📈 Recommendations", self.styles['CustomHeading']))
        story.append(Spacer(1, 0.1 * inch))
        
        recommendations = [
            "Review areas where students showed confusion and prepare additional examples",
            "Consider interactive elements for complex topics to improve engagement",
            "Provide supplementary materials for concepts that generated many questions",
            "Use the insights to adjust pacing and depth of coverage in future lectures",
            "Follow up with students on challenging concepts in the next class session"
        ]
        
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", self.styles['CustomBody']))
        
        # Footer
        story.append(Spacer(1, 0.5 * inch))
        footer_text = "Generated by CS300 Lecture Processor - An automated educational analysis tool"
        story.append(Paragraph(footer_text, self.styles['Normal']))
        
        return story 