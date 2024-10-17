import time
from logging import Logger
from typing import Dict, List

from openai import NOT_GIVEN, NotGiven, OpenAI
from dotenv import load_dotenv

load_dotenv()

logger = Logger(__name__)


OPENAI_MODEL_DEFAULT = 'gpt-4o'


def generate(
    prompt: str,
    system_prompt: str | None = None,
    history: List[Dict] | None = None,
    max_tokens: int | NotGiven = NOT_GIVEN,
    temperature: float | NotGiven = NOT_GIVEN,
    json_response: bool = False,
    model: str | None = None,
):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt, "type": "text"})
    
    if history:
        messages.extend(history)
    
    messages.append({"role": "user", "content": prompt, "type": "text"})

    return generate_from_messages(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        json_response=json_response,
        model=model
    )


def generate_from_messages(
    messages: List[Dict],
    max_tokens: int | NotGiven = NOT_GIVEN,
    temperature: float | NotGiven = NOT_GIVEN,
    json_response: bool = True,
    model: str | None = 'gpt-4o',
) -> str:
    client = OpenAI()
    model = model or OPENAI_MODEL_DEFAULT

    response_format = {"type": "json_object"} if json_response else None
    start_time = time.perf_counter()

    completion = client.chat.completions.create(
        messages=messages,
        model=model,
        response_format=response_format,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    text_response = completion.choices[0].message.content
    total_time = time.perf_counter() - start_time

    usage_part = ""
    if usage := completion.usage:
        usage_part = f"prompt: [{usage.prompt_tokens}] completion: [{usage.completion_tokens}] total: [{usage.total_tokens}]"
    logger.info(
        f"Completed OpenAI call to model: [{model}] total time: [{total_time}s] {usage_part}"
    )
    return text_response

