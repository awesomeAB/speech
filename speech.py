import random
import time

import pyttsx3 as ps
import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.
    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    print('How may I help you?\n\n')
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":

    NUM = 3
    PROMPT_LIMIT = 3

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    abhi = ps.init()

    print("\nHi! Welcome to ABC Airlines.")
    abhi.say('Hi! Welcome to ABC Airlines.')
    abhi.runAndWait()
    time.sleep(1)

    for i in range(NUM):
        # get the speech from the user
        # if a transcription is returned, break out of the loop and
        #     continue
        # if no transcription returned and API request failed, break
        #     loop and continue
        # if API request succeeded but no transcription was returned,
        #     re-prompt the user to say their guess again. Do this up
        #     to PROMPT_LIMIT times
        for j in range(PROMPT_LIMIT):
            msg = 'How may I help you?'
            abhi.say(msg)
            abhi.runAndWait()

            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        # if there was an error, stop
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        # show the user the transcription
        print("You said: {}\n".format(guess["transcription"]))


        user_has_more_attempts = i < NUM - 1


        if 'flight' in guess['transcription'].split():
            msg = "Your flight 6E 492 from Bangalore to New Delhi is scheduled to depart on 22 Feb 2019 at 10:30 AM"
            abhi.say(msg)
            abhi.runAndWait()
            print(msg+'\n\n')
            break
        elif user_has_more_attempts:
            msg = "I didn't catch that. What did you say?"
            abhi.say(msg)
            abhi.runAndWait()
            print(msg+'\n\n')
        else:
            msg = "Sorry, your call will now be redirected to an agent!"
            abhi.say(msg)
            abhi.runAndWait()
            print(msg+'\n\n')
            break