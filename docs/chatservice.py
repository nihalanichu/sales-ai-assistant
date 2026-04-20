from google import genai
from dotenv import load_dotenv
from docs.models import ChatHistory, Product
from typing import List
load_dotenv()  

class ChatService:
    def __init__(self, model="gemini-3-flash-preview"):
        self.model = model
        self.client = genai.Client()   
        self.company_name = "U Commerce"
        self.bot_name = "U Commerce Bot"

    def get_response(self, prompt):
        response = self.client.models.generate_content(
            model=self.model, contents=prompt
        )
        return response.text
    
    def get_chat_history_context(self, chat_history: List[ChatHistory], limit=10):
        chat_context = ""

        if not chat_history:
            return "No previous chat history."

        # Take last 10 records if count is more than 10
        recent_chat_history = chat_history[-limit:] if len(chat_history) > limit else chat_history
        
        for chat in reversed(recent_chat_history):
            sender_label = "User" if chat.sender == "user" else self.bot_name
            chat_context += f"{sender_label}: {chat.message}\n"
        return chat_context
    
    def get_products_context(self, products: List[Product]):
        
        # {"Electronics":[], "Fashion": []}

        if not products:
            return "Currently, there are no products available."
        
        categories = {}        
        for product in products:
            if product.category not in categories:
                categories[product.category] = []
            categories[product.category].append(product.name)
        
        products_context = ""
        for category, category_products in categories.items():
            products_context += f"{category}:\n"
            for product in category_products:
                stock_status = f"In Stock({product.current_stock})" if product.current_stock > 0 else "Out of Stock"
                products_context += f"- {product.title}: {product.description} : Price is {product.price} : {stock_status}\n"
        return products_context
        
    # get_products list
    # get user name
    # get user email
    # get user phone number
    # get user address
    # system instructions
    # get user order history
    # get user orders details
    # get user order status

    def generate_prompt(self, user_input, user_name, products_context, chat_context):
        prompt = f"""You are {self.bot_name}, a helpful assistant for {self.company_name}.
        your task is to assist users find their products and answer their questions.
        you are not allowed to ask for user information.
        Here is some information about the user:
        Current user name is {user_name}.
        Available products are: {products_context}
        Previous chat history: {chat_context}
        Instructions: 
        - Always greet the user by their name at the beginning of the conversation {{user_name}}.
        - Provide accurate product information from available products list above.
        - check product stock availability before suggesting any product.
        - if a product is out of stock, inform user politely and suggest alternative products if available.
        - Be friendly and helpful in your responses.
        - Keep responses short and to the point(2-4 sentences typically)
        - if user asks about products not in the list, politely inform them that you don't have information about that product and suggest they contact customer support for more details.
        - Focus on being a sales support assistant - help users find products, check availability, and provide information.

        User's question: {user_input}
        bot: """
        return prompt
    
    def chat(self, user_name, user_input, products:List[Product], chat_history:List[ChatHistory]):
        products_context = self.get_products_context(products)
        print("products context:", products_context)
        chat_context = self.get_chat_history_context(chat_history)
        print("chat context:", chat_context)
        prompt = self.generate_prompt(user_input, user_name, products_context, chat_context)
        print("prompt:", prompt)
        response = self.get_response(prompt)
        return response
    
chatbot_service = ChatService()
