import google.generativeai as genai

genai.configure(api_key='AIzaSyC94uxPEVP-YTthUIafedlZ6uqUZ_NhUOY')
models = genai.list_models()
print([m.name for m in models if 'generateContent' in m.supported_generation_methods])
