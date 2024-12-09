import config, openai

class GPT():
    '''GPT_Chat'''
    def __init__(self):
        self.setup_base()

    def setup_base(self):
        '''Setup base setting for openai.'''
        openai.api_key = config.settings["openai"]

    def get_response(self, request):
        '''Get response from OpenAI, return text.'''
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You're an assistant."},
                    {"role": "user", "content": request}
                ]
            )
            message = response['choices'][0]['message']['content']
            return message
        except openai.error.RateLimitError as e:
            print(f"The request limit has been exceeded: {e}")
            return "The request limit has been reached. Try again later."
        except openai.error.APIError as e:
            print(f"Openapi API Error: {e}")
            return "An error occurred on the Open AI server. Try again later."
        except openai.error.AuthenticationError as e:
            print(f"Authentication error: {e}")
            return "Authentication error. Check the API key."
        except openai.error.PermissionError as e:
            print(f"Access error: {e}")
            return "There are no permissions to access this resource."
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")
            return "An error occurred while processing the request."
        except Exception as e:
            print(f"Error in get_response: {e}")
            return "An error occurred while receiving a response from the AI."

    def get_img_gen(self, request):
        '''Get response from OpenAI, return image URL.'''
        try:
            if not request or len(request.strip()) == 0:
                return "❌ Enter a description of the image after the command !img."

            # We are sending a request for image generation
            response = openai.Image.create(
                prompt=request,  
                n=1,             
                size="1024x1024" 
            )

            image_url = response['data'][0]['url']
            return image_url
        except openai.error.RateLimitError as e:
            print(f"The request limit has been exceeded: {e}")
            return "❌ The request limit has been reached. Try again later."
        except openai.error.APIError as e:
            print(f"Openapi API Error: {e}")
            return "❌ An error occurred on the Open AI server. Try again later."
        except openai.error.AuthenticationError as e:
            print(f"Authentication error: {e}")
            return "❌ Authentication error. Check the API key."
        except openai.error.PermissionError as e:
            print(f"Access error: {e}")
            return "❌ There are no permissions to access this resource."
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")
            return "❌ An error occurred while generating the image."
