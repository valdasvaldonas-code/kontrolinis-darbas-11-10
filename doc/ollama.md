# Ollama Python Library

The Ollama Python library provides a straightforward interface for integrating Python applications with Ollama, an open-source platform for running large language models locally. It enables developers to interact with LLMs through simple Python APIs, supporting chat conversations, text generation, embeddings, streaming responses, and model management. The library is built on httpx for robust HTTP communication and Pydantic for type-safe data validation.

This library abstracts the complexity of the Ollama REST API into intuitive Python methods, offering both synchronous (`Client`) and asynchronous (`AsyncClient`) implementations. It handles response parsing, error management, image encoding for multimodal models, and provides streaming capabilities for real-time token generation. The library supports advanced features including function calling (tools), structured outputs via JSON schemas, thinking modes for reasoning models, and web search/fetch capabilities through the Ollama API.

## API Reference

### Chat Completion

Create conversational responses using a chat model with message history.

```python
from ollama import chat, ChatResponse

# Basic chat
response: ChatResponse = chat(
    model='gemma3',
    messages=[
        {'role': 'user', 'content': 'Why is the sky blue?'}
    ]
)
print(response.message.content)
# Access via dictionary notation
print(response['message']['content'])

# Chat with system prompt and options
response = chat(
    model='llama3.1',
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': 'Explain quantum computing'}
    ],
    options={'temperature': 0.7, 'top_p': 0.9},
    keep_alive='5m'
)
print(response.message.content)

# Streaming chat
stream = chat(
    model='gemma3',
    messages=[{'role': 'user', 'content': 'Tell me a story'}],
    stream=True
)
for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
```

### Text Generation

Generate text from a prompt without maintaining conversation history.

```python
from ollama import generate, GenerateResponse

# Basic generation
response: GenerateResponse = generate(
    model='gemma3',
    prompt='Why is the sky blue?'
)
print(response.response)

# Generation with system prompt and context
response = generate(
    model='llama3.1',
    prompt='Continue the story',
    system='You are a creative writer.',
    context=[1, 2, 3],  # Token context from previous generation
    options={'temperature': 0.8}
)
print(response.response)
print(f"Tokens: {response.eval_count}")
print(f"Duration: {response.total_duration}ns")

# Streaming generation
stream = generate(
    model='gemma3',
    prompt='Write a poem about the ocean',
    stream=True
)
for chunk in stream:
    print(chunk.response, end='', flush=True)
```

### Function Calling (Tools)

Enable models to call Python functions with automatic schema generation.

```python
from ollama import chat, ChatResponse

def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers

    Args:
        a (int): The first number
        b (int): The second number

    Returns:
        int: The sum of the two numbers
    """
    return int(a) + int(b)

def subtract_two_numbers(a: int, b: int) -> int:
    """
    Subtract two numbers
    """
    return int(a) - int(b)

# Manual tool definition
subtract_tool = {
    'type': 'function',
    'function': {
        'name': 'subtract_two_numbers',
        'description': 'Subtract two numbers',
        'parameters': {
            'type': 'object',
            'required': ['a', 'b'],
            'properties': {
                'a': {'type': 'integer', 'description': 'The first number'},
                'b': {'type': 'integer', 'description': 'The second number'},
            },
        },
    },
}

messages = [{'role': 'user', 'content': 'What is three plus one?'}]
available_functions = {
    'add_two_numbers': add_two_numbers,
    'subtract_two_numbers': subtract_two_numbers,
}

response: ChatResponse = chat(
    model='llama3.1',
    messages=messages,
    tools=[add_two_numbers, subtract_tool]
)

if response.message.tool_calls:
    for tool in response.message.tool_calls:
        if function_to_call := available_functions.get(tool.function.name):
            print(f'Calling: {tool.function.name}')
            print(f'Arguments: {tool.function.arguments}')
            output = function_to_call(**tool.function.arguments)
            print(f'Output: {output}')

            # Continue conversation with tool result
            messages.append(response.message)
            messages.append({
                'role': 'tool',
                'content': str(output),
                'tool_name': tool.function.name
            })

    final_response = chat(model='llama3.1', messages=messages)
    print(f'Final: {final_response.message.content}')
```

### Structured Outputs

Generate JSON responses conforming to Pydantic schemas or JSON schemas.

```python
from pydantic import BaseModel
from ollama import chat

class FriendInfo(BaseModel):
    name: str
    age: int
    is_available: bool

class FriendList(BaseModel):
    friends: list[FriendInfo]

response = chat(
    model='llama3.1:8b',
    messages=[{
        'role': 'user',
        'content': 'I have two friends. The first is Ollama 22 years old busy saving the world, and the second is Alonso 23 years old and wants to hang out. Return a list of friends in JSON format'
    }],
    format=FriendList.model_json_schema(),
    options={'temperature': 0}
)

# Validate and parse response
friends_response = FriendList.model_validate_json(response.message.content)
print(friends_response)
# Output: friends=[FriendInfo(name='Ollama', age=22, is_available=False), FriendInfo(name='Alonso', age=23, is_available=True)]

for friend in friends_response.friends:
    print(f"{friend.name} is {friend.age} and {'available' if friend.is_available else 'busy'}")
```

### Embeddings

Generate vector embeddings for text inputs.

```python
from ollama import embed, EmbedResponse

# Single text embedding
response: EmbedResponse = embed(
    model='llama3.2',
    input='Hello, world!'
)
print(response.embeddings[0][:5])  # First 5 dimensions
# Output: [0.123, -0.456, 0.789, ...]

# Batch embeddings
response = embed(
    model='llama3.2',
    input=[
        'The sky is blue because of rayleigh scattering',
        'Grass is green because of chlorophyll'
    ]
)
print(f"Number of embeddings: {len(response.embeddings)}")
print(f"Embedding dimension: {len(response.embeddings[0])}")

# With custom dimensions
response = embed(
    model='llama3.2',
    input='Reduce my dimensions',
    dimensions=512
)
print(f"Reduced dimension: {len(response.embeddings[0])}")
```

### Multimodal Inputs

Process images alongside text in chat conversations.

```python
from ollama import chat
from pathlib import Path

# Using file path
response = chat(
    model='gemma3',
    messages=[{
        'role': 'user',
        'content': 'What is in this image? Be concise.',
        'images': ['/path/to/image.jpg']
    }]
)
print(response.message.content)

# Using raw bytes
image_bytes = Path('/path/to/image.jpg').read_bytes()
response = chat(
    model='gemma3',
    messages=[{
        'role': 'user',
        'content': 'Describe this image',
        'images': [image_bytes]
    }]
)
print(response.message.content)

# Using base64 encoded string
import base64
image_b64 = base64.b64encode(Path('/path/to/image.jpg').read_bytes()).decode()
response = chat(
    model='gemma3',
    messages=[{
        'role': 'user',
        'content': 'Analyze this image',
        'images': [image_b64]
    }]
)
print(response.message.content)
```

### Thinking Mode

Enable reasoning and chain-of-thought for supported models.

```python
from ollama import chat

# Basic thinking mode
response = chat(
    model='deepseek-r1',
    messages=[{'role': 'user', 'content': 'What is 10 + 23?'}],
    think=True
)
print('Thinking:\n' + response.message.thinking)
print('\nResponse:\n' + response.message.content)

# Thinking with levels
response = chat(
    model='qwen3',
    messages=[{'role': 'user', 'content': 'Solve this logic puzzle'}],
    think='high'  # Options: 'low', 'medium', 'high'
)
print(response.message.thinking)
```

### Custom Client Configuration

Create clients with custom hosts, headers, and timeouts.

```python
from ollama import Client, AsyncClient

# Synchronous client
client = Client(
    host='http://localhost:11434',
    headers={'x-api-key': 'secret'},
    timeout=30.0
)
response = client.chat(
    model='gemma3',
    messages=[{'role': 'user', 'content': 'Hello'}]
)
print(response.message.content)

# Custom host with path
client = Client(host='https://example.com:8080/ollama')
response = client.generate(model='gemma3', prompt='Test')

# Asynchronous client
import asyncio

async def main():
    client = AsyncClient(
        host='http://localhost:11434',
        follow_redirects=True
    )
    response = await client.chat(
        model='gemma3',
        messages=[{'role': 'user', 'content': 'Async hello'}]
    )
    print(response.message.content)

asyncio.run(main())
```

### Async Operations

Perform non-blocking operations with AsyncClient.

```python
import asyncio
from ollama import AsyncClient

async def main():
    client = AsyncClient()

    # Async chat
    response = await client.chat(
        model='gemma3',
        messages=[{'role': 'user', 'content': 'Why is the sky blue?'}]
    )
    print(response.message.content)

    # Async streaming
    async for chunk in await client.chat(
        model='gemma3',
        messages=[{'role': 'user', 'content': 'Tell me a story'}],
        stream=True
    ):
        print(chunk.message.content, end='', flush=True)

    # Async generation
    response = await client.generate(
        model='gemma3',
        prompt='Explain async programming'
    )
    print(response.response)

    # Async embeddings
    response = await client.embed(
        model='llama3.2',
        input='Async embeddings'
    )
    print(response.embeddings[0][:5])

asyncio.run(main())
```

### Web Search and Fetch

Perform web searches and fetch web content (requires OLLAMA_API_KEY).

```python
import os
from ollama import web_search, web_fetch, chat

# Set API key
os.environ['OLLAMA_API_KEY'] = 'your_api_key'

# Web search
search_results = web_search(
    query="ollama new features",
    max_results=3
)
for result in search_results.results:
    print(f"{result.title}")
    print(f"URL: {result.url}")
    print(f"Content: {result.content[:100]}")

# Web fetch
fetch_result = web_fetch(url="https://example.com")
print(f"Title: {fetch_result.title}")
print(f"Content: {fetch_result.content[:200]}")
print(f"Links: {fetch_result.links}")

# Using web tools in chat
response = chat(
    model='qwen3',
    messages=[{'role': 'user', 'content': 'What is the latest news about AI?'}],
    tools=[web_search, web_fetch],
    think=True
)
if response.message.tool_calls:
    for tool_call in response.message.tool_calls:
        if tool_call.function.name == 'web_search':
            results = web_search(**tool_call.function.arguments)
            print(results.results[0].content)
```

### Model Management

List, pull, push, create, delete, copy, and show model information.

```python
from ollama import list, pull, push, create, delete, copy, show, ps

# List available models
models = list()
for model in models.models:
    print(f"{model.model} - {model.size} - {model.modified_at}")

# Pull a model
for progress in pull(model='gemma3', stream=True):
    print(f"{progress.status}: {progress.completed}/{progress.total}")

# Show model information
info = show(model='gemma3')
print(f"Template: {info.template}")
print(f"Parameters: {info.parameters}")
print(f"Capabilities: {info.capabilities}")

# List running models
running = ps()
for model in running.models:
    print(f"{model.name} - {model.size_vram}")

# Copy a model
status = copy(source='gemma3', destination='my-gemma3')
print(status.status)  # 'success' or 'error'

# Create custom model
for progress in create(
    model='my-model',
    from_='gemma3',
    system="You are Mario from Super Mario Bros.",
    stream=True
):
    print(progress.status)

# Delete a model
status = delete(model='my-model')
print(status.status)

# Push model to registry
for progress in push(model='user/model', stream=True):
    print(f"{progress.status}: {progress.completed}/{progress.total}")
```

### Error Handling

Handle connection errors, response errors, and request errors.

```python
from ollama import chat, ResponseError, generate

# Handle missing model
try:
    response = chat(model='nonexistent-model', messages=[{'role': 'user', 'content': 'test'}])
except ResponseError as e:
    print(f'Error: {e.error}')
    print(f'Status code: {e.status_code}')
    if e.status_code == 404:
        from ollama import pull
        pull('nonexistent-model')

# Handle connection errors
try:
    response = generate(model='gemma3', prompt='test')
except ConnectionError as e:
    print(f'Connection failed: {e}')
    print('Make sure Ollama is running: ollama serve')

# Streaming error handling
try:
    stream = chat(
        model='gemma3',
        messages=[{'role': 'user', 'content': 'test'}],
        stream=True
    )
    for chunk in stream:
        print(chunk.message.content, end='')
except ResponseError as e:
    print(f'Streaming error: {e.error}')
```

### Options Configuration

Configure model behavior with runtime and load-time options.

```python
from ollama import chat, Options

# Using dictionary
response = chat(
    model='gemma3',
    messages=[{'role': 'user', 'content': 'Be creative'}],
    options={
        'temperature': 0.9,
        'top_p': 0.95,
        'top_k': 50,
        'num_predict': 200,
        'seed': 42,
        'num_ctx': 4096,
        'repeat_penalty': 1.1
    }
)

# Using Options object
options = Options(
    temperature=0.3,
    num_predict=500,
    num_ctx=8192,
    seed=123
)
response = chat(
    model='llama3.1',
    messages=[{'role': 'user', 'content': 'Be precise'}],
    options=options
)

# JSON format enforcement
response = chat(
    model='llama3.1',
    messages=[{'role': 'user', 'content': 'Return a JSON object with name and age'}],
    format='json',
    options={'temperature': 0}
)
import json
data = json.loads(response.message.content)
print(data)
```

## Integration Patterns

The Ollama Python library integrates seamlessly into various application architectures. For conversational AI systems, maintain message history across turns and leverage tool calling to extend model capabilities with custom functions. When building RAG (Retrieval-Augmented Generation) pipelines, use the embed API to generate vector representations of documents and queries, then combine with chat for context-aware responses. The streaming APIs enable real-time user interfaces where tokens appear progressively, improving perceived latency.

For production deployments, use AsyncClient in async web frameworks like FastAPI or aiohttp to handle concurrent requests efficiently without blocking. Configure custom hosts and headers for authentication and routing in multi-service architectures. Leverage structured outputs with Pydantic schemas to ensure type-safe data exchange between services. Handle errors gracefully with try-except blocks, implementing retry logic for transient failures. The library's support for multimodal inputs, thinking modes, and web search capabilities enables sophisticated AI applications ranging from document analysis to research assistants with real-time web context.
