# api/ai_tools.py
"""
Vercel-compatible AI Tools Backend
"""

import json
import random

# ============================================
# TOOLS
# ============================================

class SemanticsAnalyzer:
    def __init__(self):
        self.positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'happy', 'love', 'best', 'fantastic'}
        self.negative_words = {'bad', 'terrible', 'awful', 'horrible', 'hate', 'worst', 'poor', 'sad', 'disappointing'}
    
    def process_query(self, text_input):
        text_lower = text_input.lower()
        words = set(text_lower.split())
        pos_count = len(words & self.positive_words)
        neg_count = len(words & self.negative_words)
        if pos_count > neg_count:
            label = "POSITIVE"
            confidence = min(0.95, 0.60 + (pos_count * 0.1))
        elif neg_count > pos_count:
            label = "NEGATIVE"
            confidence = min(0.95, 0.60 + (neg_count * 0.1))
        else:
            label = "NEUTRAL"
            confidence = 0.50
        return {"result": f"Sentiment: {label} (confidence: {confidence:.2%})"}

class ImageClassifier:
    def process_query(self, image_data):
        categories = [
            ("cat", 0.87), ("dog", 0.72), ("bird", 0.65),
            ("landscape", 0.78), ("food", 0.81), ("person", 0.69)
        ]
        selected = random.sample(categories, 3)
        result_text = "I see:\n"
        for label, score in sorted(selected, key=lambda x: x[1], reverse=True):
            result_text += f"- {label}: {score:.2%}\n"
        return {"result": result_text}

class TextSummarizer:
    def process_query(self, text_input):
        sentences = text_input.replace('!', '.').replace('?', '.').split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        summary_count = min(3, max(1, len(sentences)//3))
        summary = '. '.join(sentences[:summary_count]) + '.'
        return {"result": summary}

class JokeGenerator:
    def __init__(self):
        self.templates = [
            "Why did the {topic} cross the road? To get to the other side!",
            "What do you call a {topic} that can't stop talking? A chatter-{topic}!",
            "How many {topic}s does it take to change a lightbulb? Just one, but it takes forever!",
            "A {topic} walks into a bar. The bartender says, 'We don't serve {topic}s here!'",
            "What's a {topic}'s favorite type of music? Anything with a good beat!"
        ]
    def process_query(self, text_input):
        template = random.choice(self.templates)
        joke = template.format(topic=text_input)
        return {"result": f"Here's a funny joke about {text_input}:\n{joke}"}

class HaikuWriter:
    def __init__(self):
        self.templates = [
            "{topic} shines bright\nIn the quiet morning light\nPeace fills the new day",
            "Dancing {topic}\nWhispers secrets to the wind\nNature's gentle song",
            "{topic} stands tall\nSilent witness to the world\nTimeless and serene"
        ]
    def process_query(self, text_input):
        template = random.choice(self.templates)
        haiku = template.format(topic=text_input.capitalize())
        return {"result": f"Write a haiku (5-7-5 syllables) about {text_input}:\n{haiku}"}

class QuestionAnswerer:
    def __init__(self):
        self.answers = [
            "Because that's how nature designed it to work.",
            "Because it helps maintain balance in the system.",
            "Because of scientific principles we're still discovering.",
            "Because that's what makes it unique and special.",
            "Because evolution favored this adaptation over time."
        ]
    def process_query(self, text_input):
        answer = random.choice(self.answers)
        return {"result": f"Question: {text_input}\nAnswer: {answer}"}

# Tool registry
tools = {
    "semantics": SemanticsAnalyzer(),
    "image-classifier": ImageClassifier(),
    "summarizer": TextSummarizer(),
    "joke": JokeGenerator(),
    "haiku": HaikuWriter(),
    "question": QuestionAnswerer()
}

# ============================================
# Vercel handler
# ============================================

def handler(request):
    """
    Vercel serverless function entrypoint
    request has:
        - request.method
        - request.headers
        - request.body (bytes)
    """
    try:
        if request.method == "POST":
            body = json.loads(request.body.decode())
            tool_name = body.get("tool")
            user_input = body.get("input")
            
            if tool_name not in tools:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": f"Unknown tool: {tool_name}"})
                }
            
            tool = tools[tool_name]
            result = tool.process_query(user_input)
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(result)
            }
        
        elif request.method == "GET":
            # Health check
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"status": "ok", "available_tools": list(tools.keys())})
            }
        else:
            return {"statusCode": 405, "body": "Method Not Allowed"}
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
