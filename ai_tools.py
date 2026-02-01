"""
AI Tools Backend for Club Session
Each tool follows the same protocol:
- init_model(): Load/initialize the AI model
- process_query(input): Process the input and return results

Students will implement ONE tool each, then we'll combine them!
"""

from transformers import pipeline
import base64
from PIL import Image
import io

# ============================================
# TOOL 1: SEMANTICS ANALYZER
# ============================================
class SemanticsAnalyzer:
    def __init__(self):
        self.model = None
    
    def init_model(self):
        """Load the sentiment analysis model"""
        print("Loading Semantics Analyzer...")
        self.model = pipeline("sentiment-analysis")
        print("✓ Semantics Analyzer ready!")
    
    def process_query(self, text_input):
        """
        Analyze the sentiment/semantics of text
        
        Args:
            text_input: string to analyze
        
        Returns:
            dict with 'result' key containing the analysis
        """
        if self.model is None:
            self.init_model()
        
        # TODO: STUDENT IMPLEMENTS THIS!
        # Hint: Use self.model(text_input) and format the output
        result = self.model(text_input)[0]
        
        return {
            "result": f"Sentiment: {result['label']} (confidence: {result['score']:.2%})"
        }


# ============================================
# TOOL 2: IMAGE CLASSIFIER
# ============================================
class ImageClassifier:
    def __init__(self):
        self.model = None
    
    def init_model(self):
        """Load the image classification model"""
        print("Loading Image Classifier...")
        self.model = pipeline("image-classification", model="google/vit-base-patch16-224")
        print("✓ Image Classifier ready!")
    
    def process_query(self, image_data):
        """
        Classify what's in an image
        
        Args:
            image_data: base64 encoded image string
        
        Returns:
            dict with 'result' key containing top predictions
        """
        if self.model is None:
            self.init_model()
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # TODO: STUDENT IMPLEMENTS THIS!
        # Hint: Use self.model(image) and format the top 3 results
        predictions = self.model(image, top_k=3)
        
        result_text = "I see:\n"
        for pred in predictions:
            result_text += f"- {pred['label']}: {pred['score']:.2%}\n"
        
        return {"result": result_text}


# ============================================
# TOOL 3: TEXT SUMMARIZER
# ============================================
class TextSummarizer:
    def __init__(self):
        self.model = None
    
    def init_model(self):
        """Load the summarization model"""
        print("Loading Text Summarizer...")
        self.model = pipeline("summarization", model="facebook/bart-large-cnn")
        print("✓ Text Summarizer ready!")
    
    def process_query(self, text_input):
        """
        Summarize long text
        
        Args:
            text_input: long text to summarize
        
        Returns:
            dict with 'result' key containing the summary
        """
        if self.model is None:
            self.init_model()
        
        # TODO: STUDENT IMPLEMENTS THIS!
        # Hint: Use self.model(text_input, max_length=130, min_length=30)
        summary = self.model(text_input, max_length=130, min_length=30, do_sample=False)
        
        return {"result": summary[0]['summary_text']}


# ============================================
# TOOL 4: JOKE GENERATOR
# ============================================
class JokeGenerator:
    def __init__(self):
        self.model = None
    
    def init_model(self):
        """Load the text generation model"""
        print("Loading Joke Generator...")
        self.model = pipeline("text-generation", model="gpt2")
        print("✓ Joke Generator ready!")
    
    def process_query(self, text_input):
        """
        Generate a joke based on a topic
        
        Args:
            text_input: topic for the joke
        
        Returns:
            dict with 'result' key containing the joke
        """
        if self.model is None:
            self.init_model()
        
        # TODO: STUDENT IMPLEMENTS THIS!
        # Hint: Create a prompt like "Here's a funny joke about {topic}:"
        prompt = f"Here's a funny joke about {text_input}:\n"
        joke = self.model(prompt, max_length=100, num_return_sequences=1)
        
        return {"result": joke[0]['generated_text']}


# ============================================
# TOOL 5: HAIKU WRITER
# ============================================
class HaikuWriter:
    def __init__(self):
        self.model = None
    
    def init_model(self):
        """Load the haiku generation model"""
        print("Loading Haiku Writer...")
        self.model = pipeline("text-generation", model="gpt2")
        print("✓ Haiku Writer ready!")
    
    def process_query(self, text_input):
        """
        Write a haiku about a topic
        
        Args:
            text_input: topic for the haiku
        
        Returns:
            dict with 'result' key containing the haiku
        """
        if self.model is None:
            self.init_model()
        
        # TODO: STUDENT IMPLEMENTS THIS!
        # Hint: Create a prompt that asks for a haiku format
        prompt = f"Write a haiku (5-7-5 syllables) about {text_input}:\n"
        haiku = self.model(prompt, max_length=80, num_return_sequences=1)
        
        return {"result": haiku[0]['generated_text']}


# ============================================
# TOOL 6: QUESTION ANSWERER (Why?)
# ============================================
class QuestionAnswerer:
    def __init__(self):
        self.model = None
    
    def init_model(self):
        """Load the question-answering model"""
        print("Loading Question Answerer...")
        self.model = pipeline("text-generation", model="gpt2")
        print("✓ Question Answerer ready!")
    
    def process_query(self, text_input):
        """
        Answer "why" questions
        
        Args:
            text_input: the question to answer
        
        Returns:
            dict with 'result' key containing the answer
        """
        if self.model is None:
            self.init_model()
        
        # TODO: STUDENT IMPLEMENTS THIS!
        # Hint: Create a prompt that formats the question properly
        prompt = f"Question: {text_input}\nAnswer: Because"
        answer = self.model(prompt, max_length=100, num_return_sequences=1)
        
        return {"result": answer[0]['generated_text']}


# ============================================
# FLASK API (for testing locally)
# ============================================
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to connect

# Initialize all tools
tools = {
    "semantics": SemanticsAnalyzer(),
    "image-classifier": ImageClassifier(),
    "summarizer": TextSummarizer(),
    "joke": JokeGenerator(),
    "haiku": HaikuWriter(),
    "question": QuestionAnswerer()
}

@app.route('/api/process', methods=['POST'])
def process_request():
    """
    Main API endpoint
    Expects JSON: {"tool": "tool_name", "input": "text or image data"}
    """
    try:
        data = request.json
        tool_name = data.get('tool')
        user_input = data.get('input')
        
        if tool_name not in tools:
            return jsonify({"error": f"Unknown tool: {tool_name}"}), 400
        
        # Get the tool and process the query
        tool = tools[tool_name]
        result = tool.process_query(user_input)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if server is running"""
    return jsonify({"status": "ok", "available_tools": list(tools.keys())})

if __name__ == '__main__':
    print("🚀 Starting AI Tools Backend...")
    print("\nAvailable tools:")
    for tool_name in tools.keys():
        print(f"  - {tool_name}")
    print("\nServer running on http://localhost:5000")
    app.run(debug=True, port=5000)
