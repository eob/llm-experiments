import pathlib
import time
from logging import Logger
from typing import Dict, List

from openai import NOT_GIVEN, NotGiven, OpenAI
from dotenv import load_dotenv
import hashlib

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
    cache: bool = False,
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
        cache=cache,
        model=model
    )


def generate_from_messages(
    messages: List[Dict],
    max_tokens: int | NotGiven = NOT_GIVEN,
    temperature: float | NotGiven = NOT_GIVEN,
    json_response: bool = True,
    model: str | None = 'gpt-4o',
    cache: bool = False,
) -> str:
    client = OpenAI()
    model = model or OPENAI_MODEL_DEFAULT
    response_format = {"type": "json_object"} if json_response else None

    # Create the folder .llm_cache if it doesn't exist
    pathlib.Path(".llm_cache").mkdir(parents=True, exist_ok=True)

    # Create the md5 of messages + model + response_format + max_tokens + temp
    m = hashlib.md5()
    m.update(str(messages).encode('utf-8'))
    m.update(model.encode('utf-8'))
    m.update(str(response_format).encode('utf-8'))
    m.update(str(max_tokens).encode('utf-8'))
    m.update(str(temperature).encode('utf-8'))
    cache_key = m.hexdigest()
    cache_path = pathlib.Path(".llm_cache") / cache_key

    start_time = time.perf_counter()

    if cache:
        # Check if cache_key exists in .llm_cache
        if cache_path.exists():
            with open(cache_path) as f:
                text_response = f.read()
            total_time = time.perf_counter() - start_time
            logger.info(f"Retrieved from cache: [{cache_key}] total time: [{total_time}s]")
            return text_response

    completion = client.chat.completions.create(
        messages=messages,
        model=model,
        response_format=response_format,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    text_response = completion.choices[0].message.content
    total_time = time.perf_counter() - start_time

    # Write to cache
    with open(cache_path, "w") as f:
        f.write(text_response)

    usage_part = ""
    if usage := completion.usage:
        usage_part = f"prompt: [{usage.prompt_tokens}] completion: [{usage.completion_tokens}] total: [{usage.total_tokens}]"
    logger.info(
        f"Completed OpenAI call to model: [{model}] total time: [{total_time}s] {usage_part}"
    )
    return text_response

