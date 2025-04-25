from openai import OpenAI

class AiClient:
    def __init__(self, api_key, base_url, ia_model):
        """
        Initializes the AiClient with the provided API key, model, and optional base URL.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.ia_model = ia_model

        # Create OpenAI client instance using the new SDK structure
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def get_ai_client(self):
        """
        Displays information about the AI model and base URL.
        """
        print(f"The model used is: {self.ia_model} and the base URL is: {self.base_url}")
    
    def evaluate(self, discussion):
        """
        Evaluates a user's discussion as an IELTS examiner and returns detailed feedback.
        """
        evaluation_prompt = {
            "role": "system",
            "content": """You are an official IELTS examiner.
                            Evaluate the user's responses to your questions in the previous discussion.

                            Use the following IELTS to CEFR level comparison:

                            CEFR Level    IELTS Score
                            C2            9
                            C1            7.0 - 8.5
                            B2            5.5 - 6.5
                            B1            4.0 - 5.0
                            A2 and below  Below 4.0

                            Give a detailed band score (1-9) for each IELTS category:
                            - Fluency and Coherence
                            - Lexical Resource
                            - Grammatical Range and Accuracy
                            - Pronunciation

                            Then provide:
                            - An overall IELTS band score
                            - An approximate CEFR level based on that score
                            - Short, clear feedback for the student

                            Be concise but informative, and format the output clearly.
        """
        }

        messages = [evaluation_prompt] + discussion

        try:
            response = self.client.chat.completions.create(
                model=self.ia_model,
                messages=messages
            )
            result_text = response.choices[0].message.content
            return result_text
        except Exception as e:
            raise ValueError(f"Error while evaluating the discussion: {e}")
