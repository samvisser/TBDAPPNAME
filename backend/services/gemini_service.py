"""
Gemini AI service for text processing.
"""
import logging
from typing import Dict, List
from google import genai
from google.genai import types

from config import API_KEY, GEMINI_MODEL, GEMINI_TEMPERATURE, GEMINI_MAX_TOKENS, GEMINI_TOP_P, GEMINI_TOP_K

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for interacting with Google Gemini API."""
    
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)
        self.model = GEMINI_MODEL
    
    async def process_text(self, text: str) -> Dict[str, any]:
        """
        Process text and return summary and insights.
        
        Args:
            text: The text to process
            
        Returns:
            Dict containing 'summary' and 'insights' keys
        """
        try:
            prompt = f"""You are a professional meeting note analyzer. Analyze this text and provide a clear summary and key insights.

Format your response EXACTLY like this, replacing the placeholders with actual content:

SUMMARY: Write a clear and concise 2-3 sentence summary that captures the main points and key decisions.

INSIGHTS:
• Extract a specific, actionable insight about the main topic or decision
• Identify a key detail or important context that was discussed
• Highlight a significant challenge or opportunity mentioned
• Note any specific action items or next steps discussed
• Conclude with an important implication or recommendation

Text to analyze:
{text}"""

            model = "gemini-2.5-flash"
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=prompt)
                    ],
                ),
            ]
            generate_content_config = types.GenerateContentConfig(
                temperature=GEMINI_TEMPERATURE,
                thinking_config=types.ThinkingConfig(
                    thinking_budget=-1,
                ),
            )

            response = ""
            for chunk in self.client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                if chunk.text:
                    response += chunk.text
            response_text = response
            logger.info(f"Generated response successfully: {response_text[:100]}...")

            # Parse the response
            logger.info(f"Raw response: {response_text}")
            parsed_result = self._parse_response(response_text, text)
            
            return parsed_result

        except Exception as e:
            logger.error(f"Error in process_text: {str(e)}")
            return {
                "summary": f"Error processing text: {str(e)}",
                "insights": [
                    "Unable to process text due to an error",
                    "Please check your input and try again",
                    "If the problem persists, contact support",
                    "Make sure your text is clear and well-formatted",
                    "Consider breaking down longer texts into smaller chunks"
                ]
            }
    
    def _parse_response(self, response: str, original_text: str) -> Dict[str, any]:
        """
        Parse the Gemini response to extract summary and insights.
        
        Args:
            response: Raw response from Gemini
            original_text: Original input text for retry if needed
            
        Returns:
            Dict with 'summary' and 'insights' keys
        """
        lines = response.strip().split('\n')
        summary = ""
        insights = []
        
        current_section = None
        for line in lines:
            line = line.strip()
            if line.upper().startswith('SUMMARY:'):
                current_section = 'summary'
                summary = line.split(':', 1)[1].strip() if ':' in line else ""
            elif line.upper().startswith('INSIGHTS:'):
                current_section = 'insights'
            elif (line.startswith('•') or line.startswith('-') or line.startswith('*')) and current_section == 'insights':
                insight_text = line.lstrip('•-*').strip()
                if insight_text:  # Only add non-empty insights
                    insights.append(insight_text)
            elif current_section == 'summary' and line and not line.upper().startswith('INSIGHTS'):
                # Continue adding to summary if we're in summary section
                if summary:
                    summary += " " + line
                else:
                    summary = line
        
        logger.info(f"Parsed summary: {summary}")
        logger.info(f"Parsed insights: {insights}")
        
        # If we don't have enough insights, try a retry
        if len(insights) < 5:
            logger.info(f"Only got {len(insights)} insights, trying retry...")
            insights = self._retry_for_insights(summary, original_text, insights)
        
        # Ensure we have exactly 5 insights
        while len(insights) < 5:
            insights.append(f"Additional insight {len(insights) + 1} not available")
        
        # Take only first 5 if more than 5
        insights = insights[:5]
        
        return {
            "summary": summary or "No summary available",
            "insights": insights
        }
    
    def _retry_for_insights(self, summary: str, original_text: str, current_insights: List[str]) -> List[str]:
        """
        Retry to get more insights if we didn't get enough.
        
        Args:
            summary: Current summary
            original_text: Original input text
            current_insights: Currently parsed insights
            
        Returns:
            Updated list of insights
        """
        try:
            retry_prompt = f"""
            You MUST provide exactly 5 insights from this text. Use this exact format:

            SUMMARY: {summary}

            INSIGHTS:
            • [First insight about the main topic]
            • [Second insight about key details] 
            • [Third insight about important points]
            • [Fourth insight about notable aspects]
            • [Fifth insight about conclusions or implications]

            Text: {original_text}
            """
            
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=retry_prompt)],
                ),
            ]
            
            generate_content_config = types.GenerateContentConfig(
                temperature=GEMINI_TEMPERATURE,
                max_output_tokens=GEMINI_MAX_TOKENS,
                top_p=GEMINI_TOP_P,
                top_k=GEMINI_TOP_K,
            )
            
            retry_response = ""
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            ):
                if chunk.text:
                    retry_response += chunk.text
            
            logger.info(f"Retry response: {retry_response}")
            
            # Parse retry response
            retry_insights = []
            for line in retry_response.strip().split('\n'):
                line = line.strip()
                if line.startswith('•'):
                    insight_text = line.replace('•', '').strip()
                    if insight_text:
                        retry_insights.append(insight_text)
            
            if len(retry_insights) > len(current_insights):
                logger.info(f"Retry gave us {len(retry_insights)} insights")
                return retry_insights
            else:
                return current_insights
                
        except Exception as e:
            logger.error(f"Error in retry: {str(e)}")
            return current_insights
