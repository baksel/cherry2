#%%
import openai
import os
import json
import time
import tiktoken
# Import constant vars
from setup import *
# import transformers
########### SETUP

funeral_provider_results = f"{PROJECT_ROOT}/results"

funeral_provider_output_path = f"{funeral_provider_results}/{DATE}"

deepseek_key = os.getenv("DEEPSEEK_API_KEY")
qwen_key     = os.getenv("QWEN_API_KEY")

funeral_provider_full_path = f"{funeral_provider_results}/2025_04_06/Kyllikki ja Petri Forsius/output_cleaned_v2.json"
sample_output_kyllikki = { 
  "total": 1840, 
  "contains_items": ["coffin", "urn", "flower_decoration", "clothes", "transportation", "admin_cost"], 
  "individual_prices": [
      {"items": ["coffin"], "price": 690},
      {"items": ["urn"], "price": 190},
      {"items": ["flower_decoration"], "price": 180},
      {"items": ["clothes", "body_maintenance"], "price": 295},
      {"items": ["transportation"], "price": 295},
      {"items": ["admin_cost"], "price": 190}
  ] 
}



root_tokenizer = "C:/Users/aksel/Desktop/project/funeral_services/app_development/deepseek_v3_tokenizer"
# chat_tokenizer_dir = f"{root_tokenizer}/"

# tokenizer = transformers.AutoTokenizer.from_pretrained( 
#         chat_tokenizer_dir, trust_remote_code=True
#         )

# result = len( tokenizer.encode("Hello! dgkdsgksdofgs") )


funeral_provider_names = os.listdir(funeral_provider_output_path)



def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# Read prompt instructions
with open(f"{PROJECT_ROOT}/python/prompts/20250412.txt", "r", encoding = 'utf-8') as f:
  markdown_parse_instructions : str = f.read()
# Read sample learning markdown
with open(funeral_provider_full_path, encoding = 'utf-8') as f:
  sample_input_kyllikki : dict= json.load(f)

prompt_instructions_and_examples = [
    {"role": "system", "content": markdown_parse_instructions}, 
    {"role": "user", "content": f"Example input: {json.dumps(sample_input_kyllikki, ensure_ascii = False)}"}, 
    {"role": "assistant", "content": f"Example output: {json.dumps(sample_output_kyllikki, ensure_ascii = False)}"}           
]

client_deepseek = openai.Client(
    api_key = deepseek_key,
    base_url= "https://api.deepseek.com"
)

client_qwen    = openai.Client(
    api_key  = qwen_key,
    base_url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)

# funeral_provider_full_paths = [
#   f"{funeral_provider_output_path}/{funeral_provider_name}" for funeral_provider_name in funeral_provider_names if funeral_provider_name not in funeral_providers_to_exclude
# ]

def ParseSingleMarkdown(funeral_provider_name : str) -> None:

  funeral_provider_results_path = f"{funeral_provider_output_path}/{funeral_provider_name}"
  
  # Default file we read
  extension = "output_cleaned_v2"
  # We read _output.json file whenever markdown file is problematic, i.e., too large or doesn't have all data (sometimes the .markdown omits some elements from raw HTML)
  # if funeral_provider_name in problematic_funeral_providers:
  #    extension = "_output"

  with open(f"{funeral_provider_results_path}/{extension}.json", encoding = 'utf-8') as f:
    funeral_provider_content : dict= json.load(f)

  instruction = prompt_instructions_and_examples.copy()  
  
  # Add markdown content to LLM's instructions
  instruction.append(
    {"role": "user", "content": f"Process this input: {json.dumps(funeral_provider_content, ensure_ascii = False)}"}
    )

  number_of_tokens = num_tokens_from_string(json.dumps(instruction, ensure_ascii = False), "cl100k_base")
  
  if ( number_of_tokens > 65536 ): 
    client = client_qwen
    model  = "qwen-turbo"
  
  else:
    client = client_deepseek
    model  = "deepseek-chat"
  
 
  # Parse price information from markdown contents
  deepseek_response = client.chat.completions.create(
    model           = model,
    messages        = instruction,
    response_format = { 'type' : "json_object" },
    temperature     = 0.7
    )
  
  funeral_provider_content_parsed = deepseek_response.choices[0].message.content
  funeral_provider_content_parsed = json.loads(funeral_provider_content_parsed)
  # Export parsed data
  with open(f"{funeral_provider_results_path}/prices_raw_2.json", "w+", encoding = 'utf-8') as f:
      json.dump(funeral_provider_content_parsed,f, ensure_ascii = False, indent = 4)



#funeral_provider_path = "C:/Users/aksel/Desktop/project/funeral_services/app_development/results/2025_04_06/Helsingin Hautaustoimisto"
#x = ParseSingleMarkdown(funeral_provider_path)

content_parsed = [ParseSingleMarkdown(funeral_provider_name) for funeral_provider_name in funeral_provider_names]


#%%


# Do HTML PROCESSING FOR LARGE FILES and TORO
print(1)