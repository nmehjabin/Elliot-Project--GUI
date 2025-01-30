

from sosmart.felix.llm.llm_formatters import stop_generation_strings_llama as stop_generation_strings, llama_formatters
from sosmart.felix.llm.llm_utils import format_role, MAX_CONTEXT_SIZE, MAX_RESPONSE_TOKENS
from llama_cpp import Llama
import asyncio
import random
import time 

from sosmart.model_testing_ui.values import get_config
from sosmart.model_testing_ui.data_helpers import get_id_number, write_data, write_conversation_end_data

format_messages = llama_formatters['format_messages']
format_role = get_config()["formatter"]

epoch_time=time.time()


#END CONVERSATION DATA FORMAT
'''
ENDCONVERSATION -- ROLE_CATEGORY: character, OVERALL: 10, HUMOR: 10, USEFULNESS: 10, CREATIVITY: 10, CHARACTER: 10, NOTES: Here are some notes about this role
'''

# Helper function to convert a sync generator to an async generator
async def async_generator(sync_gen):
    for item in sync_gen:
        await asyncio.sleep(0)  # Yield control to the event loop
        yield item

def get_context_size(llm, message):
    context_size = len(llm.tokenize(str.encode(message)))
    return context_size

class UiModel():
    def __init__(self):
        self.llm = Llama(
            model_path='models/llama/Llama-3.2-3B-Instruct-Q4_0.gguf',
            # seed=random.randint(1, 1000000),
            seed=1,
            n_threads=4,
            n_ctx=MAX_CONTEXT_SIZE + MAX_RESPONSE_TOKENS,
            verbose=False,
        )
        self.messages = []
    
    def input_role(self, role):
        self.user_input_role = role
        self.messages.append({"role": "system", "content": format_role(self.user_input_role)})
        self.id_number = get_id_number()
        self.conversation_id = f"{self.id_number}-{self.user_input_role[:50].replace(' ', '-')}"
    
    def input_user_message(self, message):
        self.messages.append({"role": "user", "content": message})
    
    def end_conversation(self, end_conversation_string):
        
        user_message_lengths = []
        assistant_message_lengths = []
        for message in self.messages:
            if message["role"] == "user":
                user_message_lengths.append(get_context_size(self.llm, message["content"]))
            elif message["role"] == "assistant":
                assistant_message_lengths.append(get_context_size(self.llm, message["content"]))


        write_conversation_end_data(
            self.id_number,
            self.conversation_id,
            end_conversation_string,
            self.user_input_role, 
            len(self.messages),
            get_context_size(self.llm, format_messages(self.messages)), 
            get_context_size(self.llm, self.user_input_role),
            get_context_size(self.llm, format_role(self.user_input_role)),
            user_message_lengths,
            assistant_message_lengths,
        )

    async def generate(self, ui_response_message_element, ui):

        response = ''

        async for output in async_generator(
            self.llm(
                format_messages(self.messages), 
                seed=random.randint(1, 1000000),
                stream=True, 
                max_tokens=MAX_RESPONSE_TOKENS,
                stop=stop_generation_strings(),

                #Model output parameters that change token probabilities
                temperature=get_config()["temperature"],
                top_p=get_config()["top_p"],
                top_k=get_config()["top_k"],
                frequency_penalty=get_config()["frequency_penalty"],
                repeat_penalty=get_config()["repeat_penalty"],
                presence_penalty=get_config()["presence_penalty"],
                typical_p=get_config()["typical_p"],
                mirostat_mode=get_config()["mirostat_mode"],
                mirostat_tau=get_config()["mirostat_tau"],
                mirostat_eta=get_config()["mirostat_eta"],
                logit_bias=get_config()["logit_bias"],
            )
        ):
            response += output['choices'][0]['text']
            ui_response_message_element.clear()
            with ui_response_message_element:
                ui.html(response)
            
            #todo - allow scrolling up during message generation
            await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)', timeout=3)
        
        self.messages.append({"role": "assistant", "content": response})
        write_data(self.conversation_id, self.messages, format_messages(self.messages))
