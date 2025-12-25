import ollama
from ollama import ChatResponse
import json
from pprint import pprint

def get_sky_color(time_of_day: str)->str:
    """
    Get the current sky color

    Args:
      time_of_day: The time of the day and it could be Dawn, Twilight, Sunrise, Morning, Afternoon,Evening, Dusk, Night.
    
    Returns:
      appropriate color for the time of the day  
    """

    l={
        "Dawn": 'white',
        "Twilight": 'orange',
        "Sunrise": 'yellow',
        "Morning": 'blue',
        "Afternoon": 'blue',
        "Evening": 'yellow',
        "Dusk": 'grey',
        "Night": 'black'
    }

    return l[time_of_day]

messages=[
  {
    'role': 'user',
    'content': 'Identify the color of the sky using tools and Why is the sky in that color? ANSWER in given format and fill theory, skills_involved, use_cases, identified_using, identified_by, proposed_by, spread_by, acknowledged_by',
  },
]

response: ChatResponse = ollama.chat(model='qwen3:1.7b', messages=messages, stream=False, think=True, 
  # format={
  #   'type': 'object',
  #   'properties':{
  #       'theory': {'type': 'string'},
  #       'skills_involved': {'type': 'array', "items": {"type": "string"}},
  #       'use_cases': {'type': 'array', "items": {"type": "string"}},
  #       'identified_using': {'type': 'string'},
  #       'identified_by': {'type': 'string'},
  #       'proposed_by': {'type': 'string'},
  #       'spread_by': {'type': 'string'},
  #       'acknowledged_by': {'type': 'string'},
  #   }
  # },
  #  options={'temperature':0},
     tools=[get_sky_color])

if response.message.tool_calls:
    print(response.message.tool_calls)
    for call in response.message.tool_calls:
        if call.function.name=="get_sky_color":
            result=get_sky_color(**call.function.arguments)
        else:
            result='Unknown color'
    
    messages.append({'role': 'tool', 'tool_name': call.function.name, 'content': result})

final_response: ChatResponse = ollama.chat(model='qwen3:1.7b', messages=messages, stream=False, think=True, format={
    'type': 'object',
    'properties':{
        'theory': {'type': 'string'},
        'skills_involved': {'type': 'array', "items": {"type": "string"}},
        'use_cases': {'type': 'array', "items": {"type": "string"}},
        'identified_using': {'type': 'string'},
        'identified_by': {'type': 'string'},
        'proposed_by': {'type': 'string'},
        'spread_by': {'type': 'string'},
        'acknowledged_by': {'type': 'string'},
    }
}, options={'temperature':0}, tools=[get_sky_color])



# for chunk in response:  
#   # pprint(chunk, indent=4)
#   print(chunk, end='', flush=True)
# pprint(dict(response.message), indent=4)
# print(response.message.thinking)

print("\n---------------------------------------------------\n")

print(json.dumps(json.loads(final_response.message.content), indent=4))