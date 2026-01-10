from pydantic import BaseModel, Field


class StringsModel(BaseModel):
    """
    Модель для строковых констант приложения
    """
    too_large_number: str = Field(alias="tooLargeNumber", frozen=True)
    forget: str = Field(alias="forget", frozen=True)
    incorrect_message_amount: str = Field(alias="incorrectMessageAmount", frozen=True)
    incorrect_command_use: str = Field(alias="incorrectCommandUse", frozen=True)
    gif_settings: str = Field(alias="gifSettings", frozen=True)
    enter_width: str = Field(alias="enterWidth", frozen=True)
    enter_height: str = Field(alias="enterHeight", frozen=True)
    enter_speed: str = Field(alias="enterSpeed", frozen=True)
    incorrect_value: str = Field(alias="incorrectValue", frozen=True)
    something_went_wrong: str = Field(alias="somethingWentWrong", frozen=True)
    applied_successful: str = Field(alias="appliedSuccessful", frozen=True)
    go_to_private: str = Field(alias='goToPrivate', frozen=True)
    send_photo_error: str = Field(alias='sendPhotoError', frozen=True)
    how_to_answer: str = Field(alias='howToAnswer', frozen=True)
    sosal: str = Field(alias='sosal', frozen=True)
    yes: str = Field(alias='yes', frozen=True)
    no: str = Field(alias='no', frozen=True)
    ok: str = Field(alias='ok', frozen=True)
    prekl1: str = Field(alias='prekl1', frozen=True)
    prekl2: str = Field(alias='prekl2', frozen=True)
    prekl3: str = Field(alias='prekl3', frozen=True)
    prekl4: str = Field(alias='prekl4', frozen=True)
    kok: str = Field(alias='kok', frozen=True)


class LoggerStringsModel(BaseModel):
    """
    Модель для строковых констант логгера
    """
    incorrect_message_amount: str = Field(alias="incorrectMessageAmount", frozen=True)
    incorrect_message_use: str = Field(alias="incorrectMessageUse", frozen=True)
    try_to_set_reaction: str = Field(alias="tryToSetReaction", frozen=True)
    set_reaction_error: str = Field(alias="setReactionError", frozen=True)
    command_error: str = Field(alias="commandError", frozen=True)
    callback_error: str = Field(alias="callbackError", frozen=True)
    error_value: str = Field(alias="errorValue", frozen=True)
    settings_update_error: str = Field(alias="settingsUpdateError", frozen=True)
    incorrect_value: str = Field(alias="incorrectValue", frozen=True)
    search_file_error: str = Field(alias='searchFileError', frozen=True)
    answer_error: str = Field(alias='answerError', frozen=True)
