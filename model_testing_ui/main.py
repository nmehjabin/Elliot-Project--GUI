
from nicegui import ui
import time
import asyncio
from sosmart.model_testing_ui.ui_model import UiModel
from sosmart.model_testing_ui.values import get_config


epoch_time=time.time()


#END CONVERSATION DATA FORMAT
'''
ENDCONVERSATION -- ROLE_CATEGORY: character, OVERALL: 10, HUMOR: 10, USEFULNESS: 10, CREATIVITY: 10, CHARACTER: 10, NOTES: Here are some notes about this role
'''


@ui.page('/')
def other_page():
    ui.label('Healthcheck')

@ui.page('/app')
def main():
  global epoch_time, max_context



  ui.add_body_html('''
  <script>
  controller_global = new AbortController();
  const { signal } = controller;
  listener_global = function (e) {
      var confirmationMessage = "You haven't saved yet, are you sure you want to exit?";
      e.returnValue = confirmationMessage; // Standard for some browsers
      return confirmationMessage; // Others
  }
  window.addEventListener("beforeunload", listener_global, { signal });
  </script>
  ''')

  provided_role=False
  provided_first_prompt=False
  model = UiModel()
  response_message_first_prompt = None
  first_prompt = None
  has_saved = False

  async def send() -> None:
    nonlocal provided_role, provided_first_prompt, response_message_first_prompt, first_prompt, has_saved, model

    try:
      if has_saved:
        return
      if text.value == '' and provided_role:
        return
      user_input_message = text.value
      text.value = ''

      if not provided_role:
        with message_container:
          response_message = ui.chat_message(name='Bot', sent=False)
          with response_message:
            name = get_config()["name"]
            ui.html(f"current model is {name} - please provide a role")
        provided_role=True
        return
      
      if not provided_first_prompt:
        with message_container:
          ui.chat_message(text=user_input_message, name='You', sent=True)
          response_message = ui.chat_message(name='Bot', sent=False)
          with response_message:
            ui.html("where should we begin?")
        
        provided_first_prompt=True
        model.input_role(user_input_message)
        return

      with message_container:
        if user_input_message.strip().startswith("ENDCONVERSATION"):
          
          model.end_conversation(user_input_message)

          ui.add_body_html('''
            <script>
                           
            controller_global.abort()
                           
            window.removeEventListener("beforeunload", 
                           listener_global);
            
            //TODO getEventListeners is browser specific, only works in chrome, for some reason removeEventListener isn't working
            for (listener in getEventListeners(window)["beforeunload"]) {
                    window.removeEventListener("beforeunload", 
                           listener.listener,
                           listener.useCapture);
            }
            </script>
          ''')
          has_saved = True

          print("\n\nCONVERSATION ENDED, DATA WRITTEN\n\n")

        model.input_user_message(user_input_message)

        ui.chat_message(text=user_input_message, name='You', sent=True)
        response_message = ui.chat_message(name='Bot', sent=False)
        spinner = ui.spinner(type='dots')


      # if time.time() - epoch_time > 20:
      #   raise ValueError("testing error handling")

      if user_input_message.strip().startswith("ENDCONVERSATION"):
        with response_message:
            ui.html('saved data, you may exit')
      else:
        await model.generate(response_message, ui)

      message_container.remove(spinner)

    except Exception as error:
        print("An exception occurred:", error)
        ui.run_javascript(f'document.body.innerHTML = "<h1>AN ERROR OCCURRED - send this text to elliot</h1><p>{error}</p>"', timeout=3)
        raise error
        


  ui.add_css(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}')

  ui.query('.q-page').classes('flex')
  ui.query('.nicegui-content').classes('w-full')

  with ui.tabs().classes('w-full') as tabs:
    chat_tab = ui.tab('Chat')
  with ui.tab_panels(tabs, value=chat_tab).classes('w-full max-w-2xl mx-auto flex-grow items-stretch'):
    message_container = ui.tab_panel(chat_tab).classes('items-stretch')


#POP UP Survey Code------------------------------------------------

  def create_survey():
    dialog = ui.dialog()
    with dialog:
      with ui.card().classes('w-96 p-4'):
          ui.label("Please rate your experience").classes('text-lg font-bold')

          # Role Input Field
          role_input = ui.input(label="Your Role").classes('w-full')

          # Dropdown for OVERALL rating
          overall_rating = ui.select(
              [str(i) for i in range(1, 11)],  # Dropdown options from 1 to 10
              label="Overall Rating"
          ).classes('w-full')

          # Submit button
          def submit_survey():
              print(f"Role: {role_input.value}, Overall Rating: {overall_rating.value}")
              ui.notify("Survey Submitted! Thank you.")  # Show a notification
              dialog.close()  # Close the pop-up

          ui.button("Submit", on_click=submit_survey).classes("mt-4")

    return dialog
  
  # Create the survey dialog
  survey_dialog = create_survey()


# Nm: This is the input box, where the user types their message, I am adding the "End Conversation" button here
# Define an asynchronous function for the button click
  # Define an asynchronous function for the button click
  async def end_conversation_click():
      print("END Conversation button clicked!")  # Debugging print statement
      text.value = "ENDCONVERSATION"

      survey_dialog.open()  # Open the survey dialog
  

# UI Layout -> Add the input field and button
  with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
      with ui.row().classes('w-full no-wrap items-center'):
          text = ui.input().props('rounded outlined input-class=mx-3') \
              .classes('w-full self-center').on('keydown.enter', send)
        
        # Fix: Define the button correctly
          def on_click():
              asyncio.create_task(end_conversation_click())  # Run the async function

          # Move the button OUTSIDE of on_click, so it actually gets rendered!
          end_convo_button = ui.button('END Conversation', on_click=on_click) \
              .props('color=red outlined') \
              .classes('ml-2')  # Adds spacing between the input field and the button



ui.run(title=get_config()["name"], port=80)





# Nm: This is the input box, where the user types their message, I am adding the "End Conversation" button here
# Define an asynchronous function for the button click
# async def end_conversation_click():
#     # Simulate typing "ENDCONVERSATION" in the input box
#     print("END Conversation button clicked!")  # Debugging print statement
#     text.value = "ENDCONVERSATION"
#     # Use the target slot to update the UI
#     # with message_container:  # Explicitly define the container for UI updates
#     #   await send()  # Properly await the asynchronous send function


# # UI Layout-> Add the input field and button
# with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
#     with ui.row().classes('w-full no-wrap items-center'):
#         text = ui.input().props('rounded outlined input-class=mx-3') \
#             .classes('w-full self-center').on('keydown.enter', send)
        
#         # Add the button and bind the async function using asyncio.create_task
#         def on_click():
#             asyncio.create_task(end_conversation_click())  # Create a task to run the async function

#         ui.button('END Conversation', on_click=on_click) \
#             .props('color=red outlined') \
#             .classes('ml-2')  # Adds spacing between the input field and the button



