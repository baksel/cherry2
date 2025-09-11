#%%
import openai
import os
import json
import time
import tiktoken
from setup import RESULTS_DATE_PATH, PROJECT_ROOT, FUNERAL_DIRECTOR_NAMES


########### SETUP

prompt_path = f"{PROJECT_ROOT}/resources/prompt_20250412.txt"

deepseek_key = os.getenv("DEEPSEEK_API_KEY")
qwen_key     = os.getenv("QWEN_API_KEY")


example_input_path = f"{PROJECT_ROOT}/results/sample/output_cleaned_v2.json"

example_output = { 
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

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# Read prompt instructions
with open(prompt_path, "r", encoding = 'utf-8') as f:
  markdown_parse_instructions : str = f.read()
# Read sample learning markdown
with open(example_input_path, encoding = 'utf-8') as f:
  sample_input_kyllikki : dict= json.load(f)

prompt_instructions_and_examples = [
    {"role": "system", "content": markdown_parse_instructions}, 
    {"role": "user", "content": f"Example input: {json.dumps(sample_input_kyllikki, ensure_ascii = False)}"}, 
    {"role": "assistant", "content": f"Example output: {json.dumps(example_output, ensure_ascii = False)}"}           
]

client_deepseek = openai.Client(
    api_key = deepseek_key,
    base_url= "https://api.deepseek.com"
)

client_qwen    = openai.Client(
    api_key  = qwen_key,
    base_url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)



def ParseSingleMarkdown(funeral_director_name : str) -> None:

  funeral_director_results_path = f"{RESULTS_DATE_PATH}/{funeral_director_name}"
  
  # Default file we read
  extension = "output_cleaned"
  # We read _output.json file whenever markdown file is problematic, i.e., too large or doesn't have all data (sometimes the .markdown omits some elements from raw HTML)
  # if funeral_director_name in problematic_funeral_directors:
  #    extension = "_output"

  with open(f"{funeral_director_results_path}/{extension}.json", encoding = 'utf-8') as f:
    funeral_director_content : dict= json.load(f)

  instruction = prompt_instructions_and_examples.copy()  
  
  # Add markdown content to LLM's instructions
  instruction.append(
    {"role": "user", "content": f"Process this input: {json.dumps(funeral_director_content, ensure_ascii = False)}"}
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
    temperature     = 0.0
    )
  
  funeral_director_content_parsed = deepseek_response.choices[0].message.content
  funeral_director_content_parsed = json.loads(funeral_director_content_parsed)
  # Export parsed data
  with open(f"{funeral_director_results_path}/prices_raw_2.json", "w+", encoding = 'utf-8') as f:
      json.dump(funeral_director_content_parsed,f, ensure_ascii = False, indent = 4)


content_parsed = [ParseSingleMarkdown(funeral_director_name) for funeral_director_name in FUNERAL_DIRECTOR_NAMES]
