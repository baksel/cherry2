#%%
import openai
import os
import json
import time
import tiktoken
from setup import RESULTS_DATE_PATH, PROJECT_ROOT, FDS_TO_CLEAN, DATE
import glob
import re

########### SETUP

prompt_path = f"{PROJECT_ROOT}/resources/prompt_20251026.txt"
   
example_input_path = f"{PROJECT_ROOT}/results/sample/output_cleaned_v2.json"


last_prices_instruction = """See below the results we obtained last time for the funeral director. 
Use it as your reference, to cross-check whether the prices you have extracted are of the same magnitude / make sense given the past prices,
to guide selection"""

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


def ReadFile( path : str) -> str:
  with open(path, "r", encoding = 'utf-8') as f:
      file_contents: str = f.read()

  return file_contents

 
markdown_parse_instructions = ReadFile(prompt_path)
sample_input_kyllikki = ReadFile(example_input_path)

prompt_instructions_and_examples = [
    {"role": "system", "content": markdown_parse_instructions}, 
    {"role": "user", "content": f"Example input: {json.dumps(sample_input_kyllikki, ensure_ascii = False)}"}, 
    {"role": "assistant", "content": f"Example output: {json.dumps(example_output, ensure_ascii = False)}"}           
]


client_deepseek : openai.Client = openai.Client(
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url= "https://api.deepseek.com"
)

client_qwen : openai.Client    = openai.Client(
    api_key  = os.getenv("QWEN_API_KEY"),
    base_url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)



def ParseMarkdownFiles(fd_name : str) -> None:


  funeral_director_results_path = f"{RESULTS_DATE_PATH}/{fd_name}"

  def GetPricesExtractedLastTime() -> str:
     # list of all price folders where the funeral director was included
     all_prices_paths = glob.glob(
         f"{PROJECT_ROOT}/results/*/{fd_name}"
      )
    
     # Extracts the DATE part from the path; "dirty" result w/ back- and forwardslashes
     dates_extracted_dirty = [ path.partition("results")[2].partition(fd_name)[0] for path in all_prices_paths ]
     
     dates_extracted = [ date_dirty.replace("\\", "").replace("/", "") for date_dirty in dates_extracted_dirty]

     dates_extracted.sort()

    # Get the index of the current date 
     curr_date_idx = dates_extracted.index(
        DATE
        
     )
     
    
     prices_extracted_last_time_path = all_prices_paths[ curr_date_idx - 1 ]
        
     return prices_extracted_last_time_path

  path_of_last_results : str = GetPricesExtractedLastTime()

  last_extracted_prices : str = ReadFile( f"{path_of_last_results}/prices_raw_2.json" )

  last_extracted_prices : dict = json.loads( last_extracted_prices )
  
  
  
  # Default file we read
  extension = "raw_response_cleaned"
  # We read raw_response_cleaned.json file whenever markdown file is problematic, i.e., too large or doesn't have all data (sometimes the .markdown omits some elements from raw HTML)
  # if funeral_director_name in problematic_funeral_directors:
  #    extension = "_output"

  funeral_director_content : str = ReadFile( f"{funeral_director_results_path}/{extension}.json")
  funeral_director_content : dict = json.loads( funeral_director_content )


  instruction = prompt_instructions_and_examples.copy()  
  
# Add last results as background to prompt for reference
  instruction.append(
    {"role": "user", "content": f"{last_prices_instruction}: {json.dumps(last_extracted_prices, ensure_ascii = False)}"}
    )

  # Add markdown content to LLM's instructions
  instruction.append(
    {"role": "user", "content": f"Process this input: {json.dumps(funeral_director_content, ensure_ascii = False)}"}
    )
  
  

  number_of_tokens = num_tokens_from_string(json.dumps(instruction, ensure_ascii = False), "cl100k_base")
  
  if ( number_of_tokens > 65536 ): 
    client : openai.client = client_qwen
    model  = "qwen-turbo"
  
  else:
    client : openai.client = client_deepseek
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
  with open(f"{funeral_director_results_path}/prices_raw.json", "w+", encoding = 'utf-8') as f:
      json.dump(funeral_director_content_parsed,f, ensure_ascii = False, indent = 4)

content_parsed = [ParseMarkdownFiles(funeral_director_name) for funeral_director_name in FDS_TO_CLEAN]


#ParseMarkdownFiles("eHautaus") 
# %%
