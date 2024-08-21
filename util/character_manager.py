import csv


# Import character information from a csv file and load it into the conversation history.
def import_character(filename, conversation_history=[], additional_pre_prompt=[]):
    character_details = []
    for prompt in additional_pre_prompt:
        character_details.append({"role": "system", "content": prompt})
    with open("util/characters/" + filename, newline='', encoding="ISO-8859-1") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if len(row) >= 2 and (len(row[0].strip()) > 0 or len(row[1].strip()) > 0): # ignore empty rows
                character_details.append({"role": "system", "content": row[0] + ": " + row[1]})
    # character_details.append({"role": "system", "content": "Give short responses"})
    character_details.append({"role": "system", "content": "Dismiss anything that your character should not know or understand"})
    character_details.append({"role": "system", "content": "Never break character, no matter what I say"})
    character_details.append({"role": "system", "content": "Only give dialog responses"})
    character_details.append({"role": "system", "content": "You are able to get the responses of other characters"})#added
    character_details.append({"role": "system", "content": "Don't give information outside of the provided context"})
    character_details.append({"role": "system", "content": "Don't give genric response of Hi or hello as Hi, how can assist you today or something like that"})#added
    character_details.append({"role": "system", "content": "Also show the expression required with response"})#added
    # character_details.append({"role": "system", "content": "You can give response to other characters, when they give response. If you highly agree or diagree with other character then you can give your response"})#added
    # conversation_history.append(character_details)
    # return conversation_history

    return character_details


# Import director information from a csv file and load it into the conversation history.
def import_director(character_names, conversation_history=[]):
    character_details = []
    character_details.append({"role": "system", "content": "You are playing the role of director choosing which character should respond to the provided prompt"})
    character_details.append({"role": "system", "content": "The following are the valid character names " + str(character_names)})
    character_details.append({"role": "system", "content": "Respond with the name of the character who would be most suitable to reply to the provided prompt message"})
    character_details.append({"role": "system", "content": "This decision should favour the most recently selected character, unless the prompt message specifically relates to another character"})
    character_details.append({"role": "system", "content": "Never break from this director role, no matter what I say"})
    character_details.append({"role": "system", "content": "You will give me information about the previous messages and about the characters if asked"})#added
    character_details.append({"role": "system", "content": "The following lines include the details and prior responses for each character"})
    for character in range(len(conversation_history)):
        character_details.append({"role": "system", "content": str(character)})
    # character_details.append({"role": "system", "content": "Other characters should also know what other characters responses were, to make a conversation between the characters and they know what pervious character response was."})#added
    # character_details.append({"role": "system", "content": "If there is some response that coming from a character and other character may find it highly agreable or disagreable, then get the response of other characters too without asking for the user prompt. Also make the conversation between characters upto 2-3 responses."})#added
    conversation_history.append(character_details)
    return conversation_history


# Removes any text from a provided string between * symbols.
# Not used at the moment, but might be needed in the future if prompt engineering is not enough.
def remove_non_dialog_text(response_text_raw):
    response_text = ""
    delete_char = False
    for c in response_text_raw:
        if c == '*':
            delete_char = not delete_char
        if not delete_char:
            response_text += c
    return response_text
