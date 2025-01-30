

def format_role(role):
    assistant_role = role.lower().replace("you're", "you are")

    a_an = ' an ' if 'you are an' in assistant_role else ' a '

    conversation_clause = ". Engage as though you are having a conversation, and include only the dialog. Do not include anything surrounded in asterisks."
    # brief_clause = " - Please make your responses fairly brief."
    brief_clause = " - Make your responses fairly brief."
    if 'helpful assistant' not in assistant_role:
        assistant_role = f"""
        You are a helpful assistant pretending to be {a_an}
        {assistant_role.replace('you are an', '', 1).replace('you are a', '', 1).replace('you are', '', 1)}
        {conversation_clause}
        {brief_clause}
        """
    else:
        assistant_role = f"""
        You are a helpful assistant
        {brief_clause}, and your responses should feel conversational
        """

        # assistant_role = "You are a helpful assistant pretending to be"
        # + a_an 
        # + assistant_role.replace('you are an', '', 1).replace('you are a', '', 1).replace('you are', '', 1)
        # + conversation_clause
    # assistant_role = str(assistant_role) + brief_clause
    return assistant_role

