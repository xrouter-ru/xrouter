Quick Start
OpenRouter provides an OpenAI-compatible completion API to 290 models & providers that you can call directly, or using the OpenAI SDK. Additionally, some third-party SDKs are available.

In the examples below, the OpenRouter-specific headers are optional. Setting them allows your app to appear on the OpenRouter leaderboards.

Using the OpenAI SDK
typescript
python

Copy
import OpenAI from "openai"

const openai = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: $OPENROUTER_API_KEY,
  defaultHeaders: {
    "HTTP-Referer": $YOUR_SITE_URL, // Optional, for including your app on openrouter.ai rankings.
    "X-Title": $YOUR_APP_NAME, // Optional. Shows in rankings on openrouter.ai.
  }
})

async function main() {
  const completion = await openai.chat.completions.create({
    model: "openai/gpt-3.5-turbo",
    messages: [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  })

  console.log(completion.choices[0].message)
}
main()
Using the OpenRouter API directly
typescript
python
shell

Copy
fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
    "HTTP-Referer": `${YOUR_SITE_URL}`, // Optional, for including your app on openrouter.ai rankings.
    "X-Title": `${YOUR_SITE_NAME}`, // Optional. Shows in rankings on openrouter.ai.
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    "model": "openai/gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  })
});
Using third-party SDKs
For information about using third-party SDKs and frameworks with OpenRouter, please see our frameworks documentation.Principles
OpenRouter helps developers source and optimize AI usage. We believe the future is multi-model and multi-provider.

How will you source your intelligence?

OpenRouter Provides
Price and Performance. OpenRouter scouts for the best prices, the lowest latencies, and the highest throughput across dozens of providers, and lets you choose how to prioritize them.

Standardized API. No need to change your code when switching between models or providers. You can even let users your choose and pay for their own.

Real-World Insights. Be the first to take advantage of new models. See real-world data of how often models are used for different purposes. Learn from your peers in our Discord channel.

Consolidated Billing. Simple and transparent billing, regardless of how many providers you use.

Higher Availability. Fallback providers, and automatic, smart routing means your requests still work even when providers go down.

Higher Rate Limits. OpenRouter works directly with providers to provide better rate limits and more throughput.

Models
OpenRouter strives to provide access to every potentially useful text-based AI model. In practice there are constraints on where models are reliably hosted, and on our ability to be aware of every new, useful model. If there are models you are interested in that OpenRouter doesn't have, please tell us about in our Discord channel.

Explore and browse 290 models via the website, or via our API:

OpenRouter Models API
 1.0.0
OAS 3.1
This API lets you query models supported by OpenRouter.


Authorize
default


GET
/api/v1/models

Parameters
Try it out
Name	Description
supported_parameters
string
(query)
temperature,top_p,tools
Responses
Code	Description	Links
200
200 OK

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "data": [
    {
      "id": "string",
      "name": "string",
      "created": 0,
      "description": "string",
      "pricing": {
        "prompt": "string",
        "completion": "string",
        "request": "string",
        "image": "string"
      },
      "context_length": 0,
      "architecture": {
        "tokenizer": "Router",
        "instruct_type": "none",
        "modality": "text->text"
      },
      "top_provider": {
        "context_length": 0,
        "max_completion_tokens": 0,
        "is_moderated": true
      },
      "per_request_limits": {
        "prompt_tokens": null,
        "completion_tokens": null
      }
    }
  ]
}
No links
400
400 Bad Request

Media type

application/json
Example Value
Schema
{
  "error": {
    "code": 0,
    "message": "string"
  }
}
No links
Note: Different models tokenize text in different ways. Some models break up text into chunks of multiple characters (GPT, Claude, Llama, etc) while others tokenize by character (PaLM). This means that token counts (and therefore costs) will vary between models, even when inputs and outputs are the same. Costs are displayed and billed according to the tokenizer for the model in use.

Available authorizations

apiKey  (http, Bearer)
An API token created in the keys page.

Value:
Authorize
CloseProvider Routing
OpenRouter routes requests to the best available providers for your model, given your preferences, including prompt size and output length. By default, requests are load balanced across the top providers to maximize uptime, but you can customize how this works using the provider object in the request body.

Load Balancing
For each model in your request, OpenRouter's default behavior is to load balance requests across providers with the following strategy:

Prioritize providers that have not seen significant outages in the last 10 seconds.
For the stable providers, look at the lowest-cost candidates and select one weighted by inverse square of the price (example below).
Use the remaining providers as fallbacks.
Here's an example. Let's say Provider A is $1/million tokens, Provider B is $2/million, and Provider C is $3/million. Provider B recently saw a few outages.

Your request is 9x more likely to be first routed to Provider A than Provider C.
If Provider A is tried first and fails, then Provider C will be tried next.
If both providers fail, Provider B will be tried last.
Custom Routing
You can set the providers that OpenRouter will prioritize for your request using the order field. The router will prioritize providers in this list, and in this order, for the model you're using. If you don't set this field, the router will load balance across the top providers to maximize uptime.

OpenRouter will try try them one at a time and proceed to other providers if none are operational. If you don't want to allow any other providers, you should disable fallbacks as well.

Here's an example, which will end up skipping over OpenAI (which doesn't host Mixtral), try Together, and then fall back to the normal list of providers on OpenRouter:

typescript

Copy
fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
    "HTTP-Referer": `${YOUR_SITE_URL}`, // Optional, for including your app on openrouter.ai rankings.
    "X-Title": `${YOUR_SITE_NAME}`, // Optional. Shows in rankings on openrouter.ai.
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    "model": "mistralai/mixtral-8x7b-instruct",
    "messages": [

      {"role": "user", "content": "Hello"},

    ],
    "provider": {
      "order": [
        "OpenAI",
        "Together"
      ]
    },
  })
});
Here's an example that will end up skipping over OpenAI, try Together, and then fail if Together fails:

typescript

Copy
fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
    "HTTP-Referer": `${YOUR_SITE_URL}`, // Optional, for including your app on openrouter.ai rankings.
    "X-Title": `${YOUR_SITE_NAME}`, // Optional. Shows in rankings on openrouter.ai.
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    "model": "mistralai/mixtral-8x7b-instruct",
    "messages": [

      {"role": "user", "content": "Hello"},

    ],
    "provider": {
      "order": [
        "OpenAI",
        "Together"
      ],
      "allow_fallbacks": false
    },
  })
});
Required Parameters (beta)
By default, providers that don't support a given LLM parameter will ignore them. But you can change this and only filter for providers that support the parameters in your request.

For example, to only use providers that support JSON formatting:

typescript

Copy
fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
    "HTTP-Referer": `${YOUR_SITE_URL}`, // Optional, for including your app on openrouter.ai rankings.
    "X-Title": `${YOUR_SITE_NAME}`, // Optional. Shows in rankings on openrouter.ai.
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    "model": "mistralai/mixtral-8x7b-instruct",
    "messages": [

      {"role": "user", "content": "Hello"},

    ],
    "provider": {
      "require_parameters": true
    },
    "response_format": {
      "type": "json_object"
    },
  })
});
Tool Use (beta)
When you send a request with tools or tool_choice, OpenRouter will only route to providers that natively support tool use.

Data Privacy
Some model providers may log prompts, so we display them with a Data Policy tag on model pages. This is not a definitive source of third party data policies, but represents our best knowledge.

OpenRouter's data policy is managed in your privacy settings. You can disable third party model providers that store inputs for training. Alternatively, you can skip or allow them on a per-request basis:

typescript

Copy
fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
    "HTTP-Referer": `${YOUR_SITE_URL}`, // Optional, for including your app on openrouter.ai rankings.
    "X-Title": `${YOUR_SITE_NAME}`, // Optional. Shows in rankings on openrouter.ai.
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    "model": "mistralai/mixtral-8x7b-instruct",
    "messages": [

      {"role": "user", "content": "Hello"},

    ],
    "provider": {
      "data_collection": "deny"
    },
  })
});
Disabling a provider causes the router to skip over it and proceed to the next best one.

Disabling Fallbacks
To guarantee that your request is only served by the top (lowest-cost) provider, you can disable fallbacks.

You can also combine this with the order field from Custom Routing to restrict the providers that OpenRouter will prioritize to just your chosen list.

typescript

Copy
fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
    "HTTP-Referer": `${YOUR_SITE_URL}`, // Optional, for including your app on openrouter.ai rankings.
    "X-Title": `${YOUR_SITE_NAME}`, // Optional. Shows in rankings on openrouter.ai.
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    "model": "mistralai/mixtral-8x7b-instruct",
    "messages": [

      {"role": "user", "content": "Hello"},

    ],
    "provider": {
      "allow_fallbacks": false
    },
  })
});
Ignoring Providers
Ignore Providers for a Request
You can ignore providers for a request by setting the ignore field in the provider object.

Here's an example that will ignore Azure for a request calling GPT-4 Omni:

typescript

Copy
fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
    "HTTP-Referer": `${YOUR_SITE_URL}`, // Optional, for including your app on openrouter.ai rankings.
    "X-Title": `${YOUR_SITE_NAME}`, // Optional. Shows in rankings on openrouter.ai.
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    "model": "openai/gpt-4o",
    "messages": [

      {"role": "user", "content": "Hello"},

    ],
    "provider": {
      "ignore": [
        "Azure"
      ]
    },
  })
});
Ignore Providers for Account-Wide Requests
You can ignore providers for all account requests by configuring your preferences. This configuration applies to all API requests and chatroom messages.

Warning: Ignoring multiple providers may significantly reduce fallback options and limit request recovery.

When you ignore providers for a request, the list of ignored providers is merged with your account-wide ignored providers.

Quantization
Quantization reduces model size and computational requirements while aiming to preserve performance. However, quantized models may exhibit degraded performance for certain prompts, depending on the method used.

Providers can support various quantization levels for open-weight models.

Quantization Levels
By default, requests are load-balanced across all available providers, ordered by price. To filter providers by quantization level, specify the quantizations field in the provider parameter with the following values:

int4: Integer (4 bit)
int8: Integer (8 bit)
fp6: Floating point (6 bit)
fp8: Floating point (8 bit)
fp16: Floating point (16 bit)
bf16: Brain floating point (16 bit)
unknown: Unknown
Example Request with Quantization
typescript

Copy
fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
    "HTTP-Referer": `${YOUR_SITE_URL}`, // Optional, for including your app on openrouter.ai rankings.
    "X-Title": `${YOUR_SITE_NAME}`, // Optional. Shows in rankings on openrouter.ai.
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    "model": "meta-llama/llama-3.1-8b-instruct",
    "messages": [

      {"role": "user", "content": "Hello"},

    ],
    "provider": {
      "quantizations": [
        "fp8"
      ]
    },
  })
});
JSON Schema for Provider Preferences
For a complete list of options, see this JSON schema:

javascript

Copy
{
  "$ref": "#/definitions/ProviderPreferences",
  "definitions": {
    "ProviderPreferences": {
      "type": "object",
      "properties": {
        "allow_fallbacks": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to allow backup providers to serve requests\n- true: (default) when the primary provider (or your custom providers in \"order\") is unavailable, use the next best provider.\n- false: use only the primary/custom provider, and return the upstream error if it's unavailable.\n"
        },
        "require_parameters": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to filter providers to only those that support the parameters you've provided. If this setting is omitted or set to false, then providers will receive only the parameters they support, and ignore the rest."
        },
        "data_collection": {
          "anyOf": [
            {
              "type": "string",
              "enum": [
                "deny",
                "allow"
              ]
            },
            {
              "type": "null"
            }
          ],
          "description": "Data collection setting. If no available model provider meets the requirement, your request will return an error.\n- allow: (default) allow providers which store user data non-transiently and may train on it\n- deny: use only providers which do not collect user data.\n"
        },
        "order": {
          "anyOf": [
            {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "OpenAI",
                  "Anthropic",
                  "Google",
                  "Google AI Studio",
                  "Amazon Bedrock",
                  "Groq",
                  "SambaNova",
                  "Cohere",
                  "Mistral",
                  "Together",
                  "Together 2",
                  "Fireworks",
                  "DeepInfra",
                  "Lepton",
                  "Novita",
                  "Avian",
                  "Lambda",
                  "Azure",
                  "Modal",
                  "AnyScale",
                  "Replicate",
                  "Perplexity",
                  "Recursal",
                  "OctoAI",
                  "DeepSeek",
                  "Infermatic",
                  "AI21",
                  "Featherless",
                  "Inflection",
                  "xAI",
                  "Cloudflare",
                  "SF Compute",
                  "01.AI",
                  "HuggingFace",
                  "Mancer",
                  "Mancer 2",
                  "Hyperbolic",
                  "Hyperbolic 2",
                  "Lynn 2",
                  "Lynn",
                  "Reflection"
                ]
              }
            },
            {
              "type": "null"
            }
          ],
          "description": "An ordered list of provider names. The router will attempt to use the first provider in the subset of this list that supports your requested model, and fall back to the next if it is unavailable. If no providers are available, the request will fail with an error message."
        },
        "ignore": {
          "anyOf": [
            {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "OpenAI",
                  "Anthropic",
                  "Google",
                  "Google AI Studio",
                  "Amazon Bedrock",
                  "Groq",
                  "SambaNova",
                  "Cohere",
                  "Mistral",
                  "Together",
                  "Together 2",
                  "Fireworks",
                  "DeepInfra",
                  "Lepton",
                  "Novita",
                  "Avian",
                  "Lambda",
                  "Azure",
                  "Modal",
                  "AnyScale",
                  "Replicate",
                  "Perplexity",
                  "Recursal",
                  "OctoAI",
                  "DeepSeek",
                  "Infermatic",
                  "AI21",
                  "Featherless",
                  "Inflection",
                  "xAI",
                  "Cloudflare",
                  "SF Compute",
                  "01.AI",
                  "HuggingFace",
                  "Mancer",
                  "Mancer 2",
                  "Hyperbolic",
                  "Hyperbolic 2",
                  "Lynn 2",
                  "Lynn",
                  "Reflection"
                ]
              }
            },
            {
              "type": "null"
            }
          ],
          "description": "List of provider names to ignore. If provided, this list is merged with your account-wide ignored provider settings for this request."
        },
        "quantizations": {
          "anyOf": [
            {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "int4",
                  "int8",
                  "fp6",
                  "fp8",
                  "fp16",
                  "bf16",
                  "unknown"
                ]
              }
            },
            {
              "type": "null"
            }
          ],
          "description": "A list of quantization levels to filter the provider by."
        }
      },
      "additionalProperties": false
    }
  },
  "$schema": "http://json-schema.org/draft-07/schema#"
}Model Routing
Multi-model routing is under development 👀

In the meantime, OpenRouter provides two options:

The Auto router, a special model ID that you can use to choose between selected high-quality models based on heuristics applied to your prompt.

The models array, which lets you automatically try other models if the primary model's providers are down, rate-limited, or refuse to reply due to content moderation required by all providers:

json

{
  "models": ["anthropic/claude-2.1", "gryphe/mythomax-l2-13b"],
  "route": "fallback",
  ... // Other params
}
If the model you selected returns an error, OpenRouter will try to use the fallback model instead. If the fallback model is down or returns an error, OpenRouter will return that error.

By default, any error can trigger the use of a fallback model, including context length validation errors, moderation flags for filtered models, rate-limiting, and downtime.

Requests are priced using the model that was used, which will be returned in the model attribute of the response body.

If no fallback model is specified but route: "fallback" is still included, OpenRouter will try the most appropriate open-source model available, with pricing less than the primary model (or very close to it).OAuth PKCE
Users can connect to OpenRouter in one click using Proof Key for Code Exchange (PKCE). Here's an example, and here's a step-by-step:

Step 1: Send your user to OpenRouter
Send your user to https://openrouter.ai/auth?callback_url=YOUR_SITE_URL

You can optionally include a code_challenge (random password up to 256 digits) for extra security.
For maximum security, we recommend also setting code_challenge_method to S256, and then setting code_challenge to the base64 encoding of the sha256 hash of code_verifier, which you will submit in Step 2. More info in Auth0's docs.
Example URLs
OAuth without code challenge: https://openrouter.ai/auth?callback_url=YOUR_SITE_URL

With code challenge (Plain method): https://openrouter.ai/auth?callback_url=YOUR_SITE_URL&code_challenge=5f6525766c064480ac25bd493d121377e6b57d2fa52c0245fbbd51e9&code_challenge_method=plain

With code challenge (S256 method, Recommended): https://openrouter.ai/auth?callback_url=YOUR_SITE_URL&code_challenge=17T2L7LU0IJwCoMiyYkRjTGk4b73xzc309jM2t--AfA&code_challenge_method=S256

Step 2: Exchange the code for a user-controlled API key
Once logged in, they'll be redirected back to your site with a code in the URL. Make an API call (can be frontend or backend) to exchange the code for a user-controlled API key. And that's it for PKCE!

Look for the code query parameter, e.g. ?code=....
typescript

fetch('https://openrouter.ai/api/v1/auth/keys', {
  method: 'POST',
  body: JSON.stringify({
    code: $CODE_FROM_QUERY_PARAM,
    code_verifier: $CODE_VERIFIER, // Only needed if you sent a code_challenge in Step 1
    code_challenge_method: $CODE_CHALLENGE_METHOD, // Only needed if you sent a code_challenge_method in Step 1
  }),
});
Step 3: Use the API key
A fresh API key will be in the result under "key". Store it securely and make OpenAI-style requests (supports streaming as well):

typescript

Copy
fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
    "HTTP-Referer": `${YOUR_SITE_URL}`, // Optional, for including your app on openrouter.ai rankings.
    "X-Title": `${YOUR_SITE_NAME}`, // Optional. Shows in rankings on openrouter.ai.
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    "model": "openai/gpt-4o",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"},

    ],
  })
});
You can use JavaScript or any server-side framework, like Streamlit. The linked example shows multiple models and file Q&A.

Appendix: Generating
code_challenge
for S256
code_challenge_method

In JavaScript, you can use crypto API to generate a code challenge for the S256 method:

typescript

export async function sha256CodeChallenge(input: string) {
  return crypto.createHash('sha256').update(input).digest('base64url');
}
// ...

const generatedCodeChallenge = await sha256CodeChallenge(code_verifier);

// ...
Error Codes
400 Invalid code_challenge_method: Make sure you're using the same code challenge method in step 1 as in step 2.
403 Invalid code or code_verifier: Make sure your user is logged in to OpenRouter, and that code_verifier and code_challenge_method are correct.
405 Method Not Allowed: Make sure you're using POST and HTTPS for your request.
External Tools
PKCE Tools
Online PKCE Generator ToolAPI Keys
Users or developers can cover model costs with normal API keys. This allows you to use curl or the OpenAI SDK directly with OpenRouter. Just create an API key, set the api_base, and optionally set a referrer header to make your app discoverable to others on OpenRouter.

Note: API keys on OpenRouter are more powerful than keys used directly for model APIs. They allow users to set credit limits for apps, and they can be used in OAuth flows.

Example code:

python
typescript
shell

Copy
import openai

openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = $OPENROUTER_API_KEY

response = openai.ChatCompletion.create(
  model="openai/gpt-3.5-turbo",
  messages=[...],
  headers={
    "HTTP-Referer": $YOUR_SITE_URL, # Optional, for including your app on openrouter.ai rankings.
      "X-Title": $YOUR_APP_NAME, # Optional. Shows in rankings on openrouter.ai.
  },
)

reply = response.choices[0].message
To stream with Python, see this example from OpenAI.

If your key has been exposed
You must protect your API keys and never commit them to public repositories.

OpenRouter is a GitHub secret scanning partner, and has other methods to detect exposed keys. If we determine that your key has been compromised, you will receive an email notification.

If you receive such a notification or suspect your key has been exposed, immediately visit:

https://openrouter.ai/settings/keys

to delete the compromised key and create a new one. Using environment variables and keeping keys out of your codebase is strongly recommended.API Keys
Users or developers can cover model costs with normal API keys. This allows you to use curl or the OpenAI SDK directly with OpenRouter. Just create an API key, set the api_base, and optionally set a referrer header to make your app discoverable to others on OpenRouter.

Note: API keys on OpenRouter are more powerful than keys used directly for model APIs. They allow users to set credit limits for apps, and they can be used in OAuth flows.

Example code:

python
typescript
shell

Copy
import openai

openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = $OPENROUTER_API_KEY

response = openai.ChatCompletion.create(
  model="openai/gpt-3.5-turbo",
  messages=[...],
  headers={
    "HTTP-Referer": $YOUR_SITE_URL, # Optional, for including your app on openrouter.ai rankings.
      "X-Title": $YOUR_APP_NAME, # Optional. Shows in rankings on openrouter.ai.
  },
)

reply = response.choices[0].message
To stream with Python, see this example from OpenAI.

If your key has been exposed
You must protect your API keys and never commit them to public repositories.

OpenRouter is a GitHub secret scanning partner, and has other methods to detect exposed keys. If we determine that your key has been compromised, you will receive an email notification.

If you receive such a notification or suspect your key has been exposed, immediately visit:

https://openrouter.ai/settings/keys

to delete the compromised key and create a new one. Using environment variables and keeping keys out of your codebase is strongly recommended.Requests
OpenRouter's request and response schemas are very similar to the OpenAI Chat API, with a few small differences. At a high level, OpenRouter normalizes the schema across models and providers so you only need to learn one.

Request Body
Here is the request schema as a TypeScript type. This will be the body of your POST request to the /api/v1/chat/completions endpoint (see the quick start above for an example).

typescript

// Definitions of subtypes are below
type Request = {
  // Either "messages" or "prompt" is required
  messages?: Message[];
  prompt?: string;

  // If "model" is unspecified, uses the user's default
  model?: string; // See "Supported Models" section

  // Allows to force the model to produce specific output format.
  // See models page and note on this docs page for which models support it.
  response_format?: { type: 'json_object' };

  stop?: string | string[];
  stream?: boolean; // Enable streaming

  // See LLM Parameters (openrouter.ai/docs/parameters)
  max_tokens?: number; // Range: [1, context_length)
  temperature?: number; // Range: [0, 2]

  // Tool calling
  // Will be passed down as-is for providers implementing OpenAI's interface.
  // For providers with custom interfaces, we transform and map the properties.
  // Otherwise, we transform the tools into a YAML template. The model responds with an assistant message.
  // See models supporting tool calling: openrouter.ai/models?supported_parameters=tools
  tools?: Tool[];
  tool_choice?: ToolChoice;

  // Advanced optional parameters
  seed?: number; // Integer only
  top_p?: number; // Range: (0, 1]
  top_k?: number; // Range: [1, Infinity) Not available for OpenAI models
  frequency_penalty?: number; // Range: [-2, 2]
  presence_penalty?: number; // Range: [-2, 2]
  repetition_penalty?: number; // Range: (0, 2]
  logit_bias?: { [key: number]: number };
  top_logprobs: number; // Integer only
  min_p?: number; // Range: [0, 1]
  top_a?: number; // Range: [0, 1]

  // Reduce latency by providing the model with a predicted output
  // https://platform.openai.com/docs/guides/latency-optimization#use-predicted-outputs
  prediction?: { type: 'content'; content: string; };

  // OpenRouter-only parameters
  // See "Prompt Transforms" section: openrouter.ai/docs/transforms
  transforms?: string[];
  // See "Model Routing" section: openrouter.ai/docs/model-routing
  models?: string[];
  route?: 'fallback';
  // See "Provider Routing" section: openrouter.ai/docs/provider-routing
  provider?: ProviderPreferences;
};

// Subtypes:

type TextContent = {
  type: 'text';
  text: string;
};

type ImageContentPart = {
  type: 'image_url';
  image_url: {
    url: string; // URL or base64 encoded image data
    detail?: string; // Optional, defaults to 'auto'
  };
};

type ContentPart = TextContent | ImageContentPart;

type Message =
  | {
      role: 'user' | 'assistant' | 'system';
      // ContentParts are only for the 'user' role:
      content: string | ContentPart[];
      // If "name" is included, it will be prepended like this
      // for non-OpenAI models: `{name}: {content}`
      name?: string;
    }
  | {
      role: 'tool';
      content: string;
      tool_call_id: string;
      name?: string;
    };

type FunctionDescription = {
  description?: string;
  name: string;
  parameters: object; // JSON Schema object
};

type Tool = {
  type: 'function';
  function: FunctionDescription;
};

type ToolChoice =
  | 'none'
  | 'auto'
  | {
      type: 'function';
      function: {
        name: string;
      };
    };
The response_format parameter ensures you receive a structured response from the LLM. The parameter is only supported by OpenAI models, Nitro models, and some others - check the providers on the model page on openrouter.ai/models to see if it's supported, and set require_parameters to true in your Provider Preferences. See openrouter.ai/docs/provider-routing

Request Headers
OpenRouter allows you to specify an optional HTTP-Referer header to identify your app and make it discoverable to users on openrouter.ai. You can also include an optional X-Title header to set or modify the title of your app. Example:

javascript

Copy
fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
    "HTTP-Referer": `${YOUR_SITE_URL}`, // Optional, for including your app on openrouter.ai rankings.
    "X-Title": `${YOUR_SITE_NAME}`, // Optional. Shows in rankings on openrouter.ai.
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    "model": "mistralai/mixtral-8x7b-instruct",
    "messages": [

      {"role": "user", "content": "Who are you?"},

    ],
  })
});
Model routing: If the model parameter is omitted, the user or payer's default is used. Otherwise, remember to select a value for model from the supported models or API, and include the organization prefix. OpenRouter will select the least expensive and best GPUs available to serve the request, and fall back to other providers or GPUs if it receives a 5xx response code or if you are rate-limited.

Streaming: Server-Sent Events (SSE) are supported as well, to enable streaming for all models. Simply send stream: true in your request body. The SSE stream will occasionally contain a "comment" payload, which you should ignore (noted below).

Non-standard parameters: If the chosen model doesn't support a request parameter (such as logit_bias in non-OpenAI models, or top_k for OpenAI), then the parameter is ignored. The rest are forwarded to the underlying model API.

Assistant Prefill: OpenRouter supports asking models to complete a partial response. This can be useful for guiding models to respond in a certain way.

To use this features, simply include a message with role: "assistant" at the end of your messages array. Example:

javascript

Copy
fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
    "HTTP-Referer": `${YOUR_SITE_URL}`, // Optional, for including your app on openrouter.ai rankings.
    "X-Title": `${YOUR_SITE_NAME}`, // Optional. Shows in rankings on openrouter.ai.
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    "model": "mistralai/mixtral-8x7b-instruct",
    "messages": [

      {"role": "user", "content": "Who are you?"},
      {"role": "assistant", "content": "I'm not sure, but my best guess is"},
    ],
  })
});
Images & Multimodal Requests
Multimodal requests are only available via the /api/v1/chat/completions API with a multi-part messages parameter. The image_url can either be a URL or a data-base64 encoded image. Example:

javascript

Copy
...
"messages": [
  {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": "What's in this image?"
      },
      {
        "type": "image_url",
        "image_url": {
          "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
        }
      }
    ]
  }
]
Sample LLM's response:

json

{
  "choices": [
    {
      "role": "assistant",
      "content": "This image depicts a scenic natural landscape featuring a long wooden boardwalk that stretches out through an expansive field of green grass. The boardwalk provides a clear path and invites exploration through the lush environment. The scene is surrounded by a variety of shrubbery and trees in the background, indicating a diverse plant life in the area."
    }
  ]
}
Uploading base64 encoded images
For locally stored images, you can send them to the model using base64 encoding. Here's an example:

typescript

import { readFile } from 'fs/promises';

const getFlowerImage = async (): Promise<string> => {
  const imagePath = new URL('flower.jpg', import.meta.url);
  const imageBuffer = await readFile(imagePath);
  const base64Image = imageBuffer.toString('base64');
  return `data:image/jpeg;base64,${base64Image}`;
};

...

'messages': [
  {
    role: 'user',
    content: [
      {
        type: 'text',
        text: "What's in this image?",
      },
      {
        type: 'image_url',
        image_url: {
          url: `${await getFlowerImage()}`,
        },
      },
    ],
  },
];
When sending data-base64 string, ensure it contains the content-type of the image. Example:

javascript

Copy
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII
Supported content types are:

image/png
image/jpeg
image/webp
Tool Calls
Tool calls (also known as function calling) allow you to give an LLM access to external tools. The LLM does not call the tools directly. Instead, it suggests the tool to call. The user then calls the tool separately and provides the results back to the LLM. Finally, the LLM formats the response into an answer to the user's original question.

An example of the five-turn sequence:

The user asks a question, while supplying a list of available tools in a JSON schema format:
json

Copy
...
"messages": [{
  "role": "user",
  "content": "What is the weather like in Boston?"
}],
"tools": [{
"type": "function",
"function": {
    "name": "get_current_weather",
    "description": "Get the current weather in a given location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city and state, e.g. San Francisco, CA"
        },
        "unit": {
          "type": "string",
          "enum": [
            "celsius",
            "fahrenheit"
          ]
        }
      },
      "required": [
        "location"
      ]
    }
  }
}],
The LLM responds with tool suggestion, together with appropriate arguments:
json

Copy
// Some models might include their reasoning in content
"message": {
  "role": "assistant",
  "content": null,
  "tool_calls": [
    {
      "id": "call_9pw1qnYScqvGrCH58HWCvFH6",
      "type": "function",
      "function": {
        "name": "get_current_weather",
        "arguments": "{ \"location\": \"Boston, MA\"}"
      }
    }
  ]
},
The user calls the tool separately:
typescript

const weather = await getWeather({ location: 'Boston, MA' });
console.log(weather); // { "temperature": "22", "unit": "celsius", "description": "Sunny"}
The user provides the tool results back to the LLM:
json

Copy
...
"messages": [
  {
    "role": "user",
    "content": "What is the weather like in Boston?"
  },
  {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_9pw1qnYScqvGrCH58HWCvFH6",
        "type": "function",
        "function": {
          "name": "get_current_weather",
          "arguments": "{ \"location\": \"Boston, MA\"}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "name": "get_current_weather",
    "tool_call_id": "call_9pw1qnYScqvGrCH58HWCvFH6",
    "content": "{\"temperature\": \"22\", \"unit\": \"celsius\", \"description\": \"Sunny\"}"
  }
],
The LLM formats the tool result into a natural language response:
json

...
"message": {
  "role": "assistant",
  "content": "The current weather in Boston, MA is sunny with a temperature of 22°C."
}
OpenRouter standardizes the tool calling interface. However, different providers and models may support less tool calling features and arguments. (ex: tool_choice, tool_use, tool_result)

Stream Cancellation
For some providers, streaming requests can be canceled by aborting the connection or simply disconnecting.

When aborting the connection to a provider that supports stream cancellation, the model will stop processing the request, and billing will stop as soon as the upstream provider detects the disconnection.

If you're using the Fetch API, you can use the AbortController to cancel the stream. Here's an example:

typescript

const controller = new AbortController();

fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: ...,
  body: ...,
  signal: controller.signal
})

...

// Later, to cancel the stream:
controller.abort();
NOTE: Aborting/disconnecting from a non-stream request or a stream request to a provider that does not support stream cancellation will not halt the model's processing in the background. You will still be billed for the rest of the completion.Responses
Responses are largely consistent with the OpenAI Chat API. This means that choices is always an array, even if the model only returns one completion. Each choice will contain a delta property if a stream was requested and a message property otherwise. This makes it easier to use the same code for all models.

At a high level, OpenRouter normalizes the schema across models and providers so you only need to learn one.

Response Body
Note that finish_reason will vary depending on the model provider. The model property tells you which model was used inside the underlying API.

Here's the response schema as a TypeScript type:

typescript

// Definitions of subtypes are below

type Response = {
  id: string;
  // Depending on whether you set "stream" to "true" and
  // whether you passed in "messages" or a "prompt", you
  // will get a different output shape
  choices: (NonStreamingChoice | StreamingChoice | NonChatChoice)[];
  created: number; // Unix timestamp
  model: string;
  object: 'chat.completion' | 'chat.completion.chunk';

  system_fingerprint?: string; // Only present if the provider supports it

  // Usage data is always returned for non-streaming.
  // When streaming, you will get one usage object at
  // the end accompanied by an empty choices array.
  usage?: ResponseUsage;
};
typescript

Copy
// If the provider returns usage, we pass it down
// as-is. Otherwise, we count using the GPT-4 tokenizer.

type ResponseUsage = {
  /** Including images and tools if any */
  prompt_tokens: number;
  /** The tokens generated */
  completion_tokens: number;
  /** Sum of the above two fields */
  total_tokens: number;
}
typescript

// Subtypes:
type NonChatChoice = {
  finish_reason: string | null;
  text: string;
  error?: ErrorResponse;
};

type NonStreamingChoice = {
  finish_reason: string | null; // Depends on the model. Ex: 'stop' | 'length' | 'content_filter' | 'tool_calls'
  message: {
    content: string | null;
    role: string;
    tool_calls?: ToolCall[];
  };
  error?: ErrorResponse;
};

type StreamingChoice = {
  finish_reason: string | null;
  delta: {
    content: string | null;
    role?: string;
    tool_calls?: ToolCall[];
  };
  error?: ErrorResponse;
};

type ErrorResponse = {
  code: number; // See "Error Handling" section
  message: string;
  metadata?: Record<string, unknown>; // Contains additional error information such as provider details, the raw error message, etc.
};

type ToolCall = {
  id: string;
  type: 'function';
  function: FunctionCall;
};
Here's an example:

json

{
  "id": "gen-xxxxxxxxxxxxxx",
  "choices": [
    {
      "finish_reason": "stop", // Different models provide different reasons here
      "message": {
        // will be "delta" if streaming
        "role": "assistant",
        "content": "Hello there!"
      }
    }
  ],
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 4,
    "total_tokens": 4
  },
  "model": "openai/gpt-3.5-turbo" // Could also be "anthropic/claude-2.1", etc, depending on the "model" that ends up being used
}
Querying Cost and Stats
The token counts that are returned in the completions API response are NOT counted with the model's native tokenizer. Instead it uses a normalized, model-agnostic count.

For precise token accounting using the model's native tokenizer, use the /api/v1/generation endpoint.

You can use the returned id to query for the generation stats (including token counts and cost) after the request is complete. This is how you can get the cost and tokens for all models and requests, streaming and non-streaming.

javascript

const generation = await fetch(
  "https://openrouter.ai/api/v1/generation?id=$GENERATION_ID",
  { headers }
)

await generation.json()
// OUTPUT:
{
  data: {
    "id": "gen-nNPYi0ZB6GOK5TNCUMHJGgXo",
    "model": "openai/gpt-4-32k",
    "streamed": false,
    "generation_time": 2,
    "created_at": "2023-09-02T20:29:18.574972+00:00",
    "tokens_prompt": 24,
    "tokens_completion": 29,
    "native_tokens_prompt": 24,
    "native_tokens_completion": 29,
    "num_media_prompt": null,
    "num_media_completion": null,
    "origin": "https://localhost:47323/",
    "total_cost": 0.00492,
    "cache_discount": null,
    ...
  }
};
Note that token counts are also available in the usage field of the response body for non-streaming completions.

SSE Streaming Comments
For SSE streams, we occasionally need to send an SSE comment to indicate that OpenRouter is processing your request. This helps prevent connections from timing out. The comment will look like this:


Copy
: OPENROUTER PROCESSING
Comment payload can be safely ignored per the SSE specs. However, you can leverage it to improve UX as needed, e.g. by showing a dynamic loading indicator.

Some SSE client implementations might not parse the payload according to spec, which leads to an uncaught error when you JSON.stringify the non-JSON payloads. We recommend the following clients:

eventsource-parser
OpenAI SDK
Vercel AI SDKParameters
Sampling parameters shape the token generation process of the model. You may send any parameters from the following list, as well as others, to OpenRouter.

OpenRouter will default to the values listed below if certain parameters are absent from your request (for example, temperature to 1.0). We will also transmit some provider-specific parameters, such as safe_prompt for Mistral or raw_mode for Hyperbolic directly to the respective providers if specified.

Please refer to the model’s provider section to confirm which parameters are supported. For detailed guidance on managing provider-specific parameters, click here.

Temperature
Key: temperature

Optional, float, 0.0 to 2.0

Default: 1.0

Explainer Video: Watch

This setting influences the variety in the model's responses. Lower values lead to more predictable and typical responses, while higher values encourage more diverse and less common responses. At 0, the model always gives the same response for a given input.

Top P
Key: top_p

Optional, float, 0.0 to 1.0

Default: 1.0

Explainer Video: Watch

This setting limits the model's choices to a percentage of likely tokens: only the top tokens whose probabilities add up to P. A lower value makes the model's responses more predictable, while the default setting allows for a full range of token choices. Think of it like a dynamic Top-K.

Top K
Key: top_k

Optional, integer, 0 or above

Default: 0

Explainer Video: Watch

This limits the model's choice of tokens at each step, making it choose from a smaller set. A value of 1 means the model will always pick the most likely next token, leading to predictable results. By default this setting is disabled, making the model to consider all choices.

Frequency Penalty
Key: frequency_penalty

Optional, float, -2.0 to 2.0

Default: 0.0

Explainer Video: Watch

This setting aims to control the repetition of tokens based on how often they appear in the input. It tries to use less frequently those tokens that appear more in the input, proportional to how frequently they occur. Token penalty scales with the number of occurrences. Negative values will encourage token reuse.

Presence Penalty
Key: presence_penalty

Optional, float, -2.0 to 2.0

Default: 0.0

Explainer Video: Watch

Adjusts how often the model repeats specific tokens already used in the input. Higher values make such repetition less likely, while negative values do the opposite. Token penalty does not scale with the number of occurrences. Negative values will encourage token reuse.

Repetition Penalty
Key: repetition_penalty

Optional, float, 0.0 to 2.0

Default: 1.0

Explainer Video: Watch

Helps to reduce the repetition of tokens from the input. A higher value makes the model less likely to repeat tokens, but too high a value can make the output less coherent (often with run-on sentences that lack small words). Token penalty scales based on original token's probability.

Min P
Key: min_p

Optional, float, 0.0 to 1.0

Default: 0.0

Represents the minimum probability for a token to be considered, relative to the probability of the most likely token. (The value changes depending on the confidence level of the most probable token.) If your Min-P is set to 0.1, that means it will only allow for tokens that are at least 1/10th as probable as the best possible option.

Top A
Key: top_a

Optional, float, 0.0 to 1.0

Default: 0.0

Consider only the top tokens with "sufficiently high" probabilities based on the probability of the most likely token. Think of it like a dynamic Top-P. A lower Top-A value focuses the choices based on the highest probability token but with a narrower scope. A higher Top-A value does not necessarily affect the creativity of the output, but rather refines the filtering process based on the maximum probability.

Seed
Key: seed

Optional, integer

If specified, the inferencing will sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed for some models.

Max Tokens
Key: max_tokens

Optional, integer, 1 or above

This sets the upper limit for the number of tokens the model can generate in response. It won't produce more than this limit. The maximum value is the context length minus the prompt length.

Logit Bias
Key: logit_bias

Optional, map

Accepts a JSON object that maps tokens (specified by their token ID in the tokenizer) to an associated bias value from -100 to 100. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.

Logprobs
Key: logprobs

Optional, boolean

Whether to return log probabilities of the output tokens or not. If true, returns the log probabilities of each output token returned.

Top Logprobs
Key: top_logprobs

Optional, integer

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. logprobs must be set to true if this parameter is used.

Response Format
Key: response_format

Optional, map

Forces the model to produce specific output format. Setting to { "type": "json_object" } enables JSON mode, which guarantees the message the model generates is valid JSON.

Note: when using JSON mode, you should also instruct the model to produce JSON yourself via a system or user message.

Structured Outputs
Key: structured_outputs

Optional, boolean

If the model can return structured outputs using response_format json_schema.

Stop
Key: stop

Optional, array

Stop generation immediately if the model encounter any token specified in the stop array.

Tools
Key: tools

Optional, array

Tool calling parameter, following OpenAI's tool calling request shape. For non-OpenAI providers, it will be transformed accordingly. Click here to learn more about tool calling

Tool Choice
Key: tool_choice

Optional, array

Controls which (if any) tool is called by the model. 'none' means the model will not call any tool and instead generates a message. 'auto' means the model can pick between generating a message or calling one or more tools. 'required' means the model must call one or more tools. Specifying a particular tool via {"type": "function", "function": {"name": "my_function"}} forces the model to call that tool.Structured Outputs
OpenRouter supports structured outputs for compatible models, ensuring responses follow a specific JSON Schema format. This feature is particularly useful when you need consistent, well-formatted responses that can be reliably parsed by your application.

Overview
Structured outputs allow you to:

Enforce specific JSON Schema validation on model responses
Get consistent, type-safe outputs
Avoid parsing errors and hallucinated fields
Simplify response handling in your application
Using Structured Outputs
To use structured outputs, include a response_format parameter in your request, with type set to json_schema and the json_schema object containing your schema:

typescript

{
  "messages": [
    { "role": "user", "content": "What's the weather like in London?" }
  ],
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "weather",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "City or location name"
          },
          "temperature": {
            "type": "number",
            "description": "Temperature in Celsius"
          },
          "conditions": {
            "type": "string",
            "description": "Weather conditions description"
          }
        },
        "required": ["location", "temperature", "conditions"],
        "additionalProperties": false
      }
    }
  }
}
The model will respond with a JSON object that strictly follows your schema:

json

{
  "location": "London",
  "temperature": 18,
  "conditions": "Partly cloudy with light drizzle"
}
Model Support
Structured outputs are supported by select models, including:

You can find a list of models that support structured outputs on the models page.

OpenAI models (GPT-4o and later versions) Docs
All Fireworks provided models Docs
To ensure your chosen model supports structured outputs:

Check the model's supported parameters on the models page
Set require_parameters: true in your provider preferences (see Provider Routing)
Include ResponseFormat and set type: json_schema in the required parameters
Best Practices
Include descriptions: Add clear descriptions to your schema properties to guide the model

Use strict mode: Always set strict: true to ensure the model follows your schema exactly

Example Implementation
Here's a complete example using the Fetch API:

typescript

const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Authorization: 'Bearer YOUR_API_KEY',
    'HTTP-Referer': 'https://your-app.com',
  },
  body: JSON.stringify({
    model: 'openai/gpt-4',
    messages: [
      { role: 'user', content: 'What is the weather like in London?' },
    ],
    response_format: {
      type: 'json_schema',
      json_schema: {
        name: 'weather',
        strict: true,
        schema: {
          type: 'object',
          properties: {
            location: {
              type: 'string',
              description: 'City or location name',
            },
            temperature: {
              type: 'number',
              description: 'Temperature in Celsius',
            },
            conditions: {
              type: 'string',
              description: 'Weather conditions description',
            },
          },
          required: ['location', 'temperature', 'conditions'],
          additionalProperties: false,
        },
      },
    },
  }),
});

const data = await response.json();
const weatherInfo = data.choices[0].message.content;
Streaming with Structured Outputs
Structured outputs are also supported with streaming responses. The model will stream valid partial JSON that, when complete, forms a valid response matching your schema.

To enable streaming with structured outputs, simply add stream: true to your request:

typescript

{
  "stream": true,
  "response_format": {
    "type": "json_schema",
    // ... rest of your schema
  }
}
Error Handling
When using structured outputs, you may encounter these scenarios:

Model doesn't support structured outputs: The request will fail with an error indicating lack of support
Invalid schema: The model will return an error if your JSON Schema is invalidParameters API
You can use the Parameter API to get the list of supported parameters and a sample value for a model.

OpenRouter Parameters API
 1.0.0
OAS 3.1
This API lets you query the top LLM sampling parameter configurations used by users on OpenRouter.


Authorize
default


GET
/api/v1/parameters/{modelId}


Parameters
Try it out
Name	Description
modelId *
string
(path)
Specify a model ID, since optimal parameters vary between models. To see a list of available models, click here.

mistralai/mixtral-8x7b-instruct
provider
string
(query)
Specify a provider name to filter supported parameters for a given model by provider.

Available values : OpenAI, Anthropic, Google, Google AI Studio, Amazon Bedrock, Groq, SambaNova, SambaNova 2, Cohere, Mistral, Together, Together 2, Fireworks, DeepInfra, Lepton, Novita, Avian, Lambda, Azure, Modal, AnyScale, Replicate, Perplexity, Recursal, OctoAI, DeepSeek, Infermatic, AI21, Featherless, Inflection, xAI, Cloudflare, SF Compute, 01.AI, HuggingFace, Mancer, Mancer 2, Hyperbolic, Hyperbolic 2, Lynn 2, Lynn, Reflection


OpenAI
Responses
Code	Description	Links
200
200 OK

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "data": {
    "model": "string",
    "supported_parameters": [
      "temperature"
    ],
    "frequency_penalty_p10": 0,
    "frequency_penalty_p50": 0,
    "frequency_penalty_p90": 0,
    "min_p_p10": 0,
    "min_p_p50": 0,
    "min_p_p90": 0,
    "presence_penalty_p10": 0,
    "presence_penalty_p50": 0,
    "presence_penalty_p90": 0,
    "repetition_penalty_p10": 0,
    "repetition_penalty_p50": 0,
    "repetition_penalty_p90": 0,
    "temperature_p10": 0,
    "temperature_p50": 0,
    "temperature_p90": 0,
    "top_a_p10": 0,
    "top_a_p50": 0,
    "top_a_p90": 0,
    "top_k_p10": 0,
    "top_k_p50": 0,
    "top_k_p90": 0,
    "top_p_p10": 0,
    "top_p_p50": 0,
    "top_p_p90": 0
  }
}
No links
404
404 Not Found

Media type

application/json
Example Value
Schema
{
  "error": {
    "code": 0,
    "message": "string"
  }
}
No links
Prompt Caching
To save on inference costs, you can enable prompt caching on supported providers and models.

Most providers automatically enable prompt caching, but note that some (see Anthropic below) require you to enable it on a per-message basis. Note that prompt caching does not work when switching between providers. In order to cache the prompt, LLM engines must store a memory snapshot of the processed prompt, which is not shared with other providers.

Inspecting cache usage
To see how much caching saved on each generation, you click the detail button on the Activity page, or you can use the /api/v1/generation API, documented here.

The cache_discount field in the response body will tell you how much the response saved on cache usage. Some providers, like Anthropic, will have a negative discount on cache writes, but a positive discount (which reduces total cost) on cache reads.

OpenAI
Caching price changes:

Cache writes: no cost
Cache reads: charged at 0.5x the price of the original input pricing on average
Supported models

openai/gpt-4o
openai/gpt-4o-2024-08-06
openai/gpt-4o-2024-11-20
openai/gpt-4o-mini
openai/gpt-4o-mini-2024-07-18
openai/o1-preview
openai/o1-preview-2024-09-12
openai/o1-mini
openai/o1-mini-2024-09-12
openai/o1-2024-12-17
Prompt caching with OpenAI is automated and does not require any additional configuration. There is a minimum prompt size of 1024 tokens.

Click here to read more about OpenAI prompt caching and its limitation.

Anthropic Claude
Caching price changes:

Cache writes: charged at 1.25x the price of the original input pricing
Cache reads: charged at 0.1x the price of the original input pricing
Supported models:

anthropic/claude-3-opus
anthropic/claude-3-sonnet
anthropic/claude-3.5-sonnet
anthropic/claude-3.5-sonnet-20240620
anthropic/claude-3-haiku
anthropic/claude-3-5-haiku
anthropic/claude-3-5-haiku-20241022
anthropic/claude-3-opus:beta
anthropic/claude-3-sonnet:beta
anthropic/claude-3.5-sonnet:beta
anthropic/claude-3.5-sonnet-20240620:beta
anthropic/claude-3-haiku:beta
anthropic/claude-3-5-haiku:beta
anthropic/claude-3-5-haiku-20241022:beta
Prompt caching with Anthropic requires the use of cache_control breakpoints. There is a limit of four breakpoints, and the cache will expire within five minutes. Therefore, it is recommended to reserve the cache breakpoints for large bodies of text, such as character cards, CSV data, RAG data, book chapters, etc.

Click here to read more about Anthropic prompt caching and its limitation.

The cache_control breakpoint can only be inserted into the text part of a multipart message.

System message caching example:

json

Copy
{
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are a historian studying the fall of the Roman Empire. You know the following book very well:"
        },
        {
          "type": "text",
          "text": "HUGE TEXT BODY",
          "cache_control": {
            "type": "ephemeral"
          }
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What triggered the collapse?"
        }
      ]
    }
  ]
}
User message caching example:

json

Copy
{
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Given the book below:"
        },
        {
          "type": "text",
          "text": "HUGE TEXT BODY",
          "cache_control": {
            "type": "ephemeral"
          }
        },
        {
          "type": "text",
          "text": "Name all the characters in the above book"
        }
      ]
    }
  ]
}
DeepSeek
Caching price changes:

Cache writes: charged at the same price as the original input pricing
Cache reads: charged at 0.1x the price of the original input pricing
Prompt caching with DeepSeek is automated and does not require any additional configuration.Transforms
OpenRouter has a simple rule for choosing between sending a prompt and sending a list of ChatML messages:

Choose messages if you want to have OpenRouter apply a recommended instruct template to your prompt, depending on which model serves your request. Available instruct modes include:
alpaca: docs
llama2: docs
airoboros: docs
Choose prompt if you want to send a custom prompt to the model. This is useful if you want to use a custom instruct template or maintain full control over the prompt submitted to the model.
To help with prompts that exceed the maximum context size of a model, OpenRouter supports a custom parameter called transforms:

typescript

{
  transforms: ["middle-out"], // Compress prompts > context size. This is the default for endpoints with context length <= 8k
  messages: [...], // "prompt" works as well
  model // Works with any model
}
The transforms param is an array of strings that tell OpenRouter to apply a series of transformations to the prompt before sending it to the model. Transformations are applied in-order. Available transforms are:

middle-out: compress prompts and message chains to the context size. This helps users extend conversations in part because LLMs pay significantly less attention to the middle of sequences anyway. Works by compressing or removing messages in the middle of the prompt. Additionally, it reduces the number of messages to adhere to the model's limit. For instance, Anthropic's Claude models enforce a maximum of 1000 messages. This transform will only be applied to prompts that is up to twice the context size of the model.
Note: All OpenRouter endpoints with 8k or less context length will default to using middle-out. To disable this, set transforms: [] in the request body.Errors
For errors, OpenRouter returns a JSON response with the following shape:

typescript

type ErrorResponse = {
  error: {
    code: number;
    message: string;
    metadata?: Record<string, unknown>;
  };
};
The HTTP Response will have the same status code as error.code, forming a request error if:

Your original request is invalid
Your API key/account is out of credits
Otherwise, the returned HTTP response status will be 200 and any error occured while the LLM is producing the output will be emitted in the response body or as an SSE data event.

Example code for printing errors in JavaScript:

javascript

const request = await fetch('https://openrouter.ai/...');
console.log(request.status); // Will be an error code unless the model started processing your request
const response = await request.json();
console.error(response.error?.status); // Will be an error code
console.error(response.error?.message);
Error Codes
400: Bad Request (invalid or missing params, CORS)
401: Invalid credentials (OAuth session expired, disabled/invalid API key)
402: Your account or API key has insufficient credits. Add more credits and retry the request.
403: Your chosen model requires moderation and your input was flagged
408: Your request timed out
429: You are being rate limited
502: Your chosen model is down or we received an invalid response from it
503: There is no available model provider that meets your routing requirements
Moderation Errors
If your input was flagged, the error.metadata will contain information about the issue. The shape of the metadata is as follows:

typescript

type ModerationErrorMetadata = {
  reasons: string[]; // Why your input was flagged
  flagged_input: string; // The text segment that was flagged, limited to 100 characters. If the flagged input is longer than 100 characters, it will be truncated in the middle and replaced with ...

  provider_name: string; // The name of the provider that requested moderation
  model_slug: string;
};
Provider Errors
If the model provider encounters an error, the error.metadata will contain information about the issue. The shape of the metadata is as follows:

typescript

type ProviderErrorMetadata = {
  provider_name: string; // The name of the provider that encountered the error
  raw: unknown; // The raw error from the provider
};
When No Content is Generated
Occasionally, the model may not generate any content. This typically occurs when:

The model is warming up from a cold start
The system is scaling up to handle more requests
Warm-up times usually range from a few seconds to a few minutes, depending on the model and provider.

If you encounter persistent no-content issues, consider implementing a simple retry mechanism or trying again with a different provider or model that has more recent activity.

Additionally, be aware that in some cases, you may still be charged for the prompt processing cost by the upstream provider, even if no content is generated.Limits
Rate Limits and Credits Remaining
To check the rate limit or credits left on an API key, make a GET request to https://openrouter.ai/api/v1/auth/key.

javascript

fetch('https://openrouter.ai/api/v1/auth/key', {
  method: 'GET',
  headers: {
    Authorization: 'Bearer $OPENROUTER_API_KEY',
  },
});
If you submit a valid API key, you should get a response of the form:

typescript

type Key = {
  data: {
    label: string;
    usage: number; // Number of credits used
    limit: number | null; // Credit limit for the key, or null if unlimited
    is_free_tier: boolean; // Whether the user has paid for credits before
    rate_limit: {
      requests: number; // Number of requests allowed...
      interval: string; // in this interval, e.g. "10s"
    };
  };
};
There are a few rate limits that apply to certain types of requests, regardless of account status:

Free limit: If you are using a free model variant (with an ID ending in :free), then you will be limited to 20 requests per minute and 200 requests per day.

DDoS protection: Cloudflare's DDoS protection will block requests that dramatically exceed reasonable usage.

For all other requests, rate limits are a function of the number of credits remaining on the key or account. Partial credits round up in your favor. For the credits available on your API key, you can make 1 request per credit per second up to the surge limit (typically 500 requests per second, but you can go higher).

For example:

0.5 credits → 1 req/s (minimum)
5 credits → 5 req/s
10 credits → 10 req/s
500 credits → 500 req/s
1000 credits → Contact us if you see ratelimiting from OpenRouter
If your account has a negative credit balance, you may see 402 errors, including for free models. Adding credits to put your balance above zero allows you to use those models again.ntegrations
Bring your own provider API Keys
OpenRouter supports both OpenRouter credits and the option to bring your own provider keys (BYOK).

When you use OpenRouter credits, your rate limits for each provider are managed by OpenRouter.

Using provider keys enables direct control over rate limits and costs via your provider account.

Your provider keys are securely encrypted and used for all requests routed through the specified provider.

Manage keys in your account settings.

The cost of using custom provider keys on OpenRouter is 5% of the upstream provider's cost.

Automatic Fallback
You can configure individual keys to act as fallbacks.

When "Use this key as a fallback" is enabled for a key, OpenRouter will prioritize using your credits. If it hits a rate limit or encounters a failure, it will then retry with your key.

Conversely, if "Use this key as a fallback" is disabled for a key, OpenRouter will prioritize using your key. If it hits a rate limit or encounters a failure, it will then retry with your credits.
Embeddings
OpenRouter does not currently provide an embeddings API.Frameworks
You can find a few examples of using OpenRouter with other frameworks in this Github repository. Here are some examples:

Using OpenAI SDK
Using npm i openai: github.

Tip: You can also use Grit to automatically migrate your code. Simply run npx @getgrit/launcher openrouter.
Using pip install openai: github.

typescript
python

Copy
import OpenAI from "openai"

const openai = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: $OPENROUTER_API_KEY,
  defaultHeaders: {
    "HTTP-Referer": $YOUR_SITE_URL, // Optional, for including your app on openrouter.ai rankings.
      "X-Title": $YOUR_SITE_NAME, // Optional. Shows in rankings on openrouter.ai.
  },
})

async function main() {
  const completion = await openai.chat.completions.create({
    model: "openai/gpt-4o",
    messages: [
      { role: "user", content: "Say this is a test" }
    ],
  })

  console.log(completion.choices[0].message)
}

main()
Using LangChain
Using LangChain for Python: github

Using LangChain.js: github

Using Streamlit: github

typescript
python

Copy
const chat = new ChatOpenAI({
  modelName: "anthropic/claude-3.5-sonnet",
  temperature: 0.8,
  streaming: true,
  openAIApiKey: $OPENROUTER_API_KEY,
}, {
  basePath: $OPENROUTER_BASE_URL + "/api/v1",
  baseOptions: {
    headers: {
      "HTTP-Referer": "https://yourapp.com/", // Optional, for including your app on openrouter.ai rankings.
        "X-Title": "Langchain.js Testing", // Optional. Shows in rankings on openrouter.ai.
    },
  },
});
Using PydanticAI
PydanticAI provides a high-level interface for working with various LLM providers, including OpenRouter.

Installation
bash

pip install 'pydantic-ai-slim[openai]'
Configuration
You can use OpenRouter with PydanticAI through its OpenAI-compatible interface:

python

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

model = OpenAIModel(
    'anthropic/claude-3.5-sonnet',  # or any other OpenRouter model
    base_url='https://openrouter.ai/api/v1',
    api_key='sk-or-...',
)

agent = Agent(model)
result = await agent.run("What is the meaning of life?")
print(result)
For more details about using PydanticAI with OpenRouter, see the PydanticAI documentation.

Vercel AI SDK
You can use the Vercel AI SDK to integrate OpenRouter with your Next.js app. To get started, install @openrouter/ai-sdk-provider:

bash

npm install @openrouter/ai-sdk-provider
And then you can use streamText() API to stream text from OpenRouter.

typescript

import { createOpenRouter } from '@openrouter/ai-sdk-provider';
import { streamText } from 'ai';
import { z } from 'zod';

export const getLasagnaRecipe = async (modelName: string) => {
  const openrouter = createOpenRouter({
    apiKey: process.env.OPENROUTER_API_KEY,
  });

  const result = await streamText({
    model: openrouter(modelName),
    prompt: 'Write a vegetarian lasagna recipe for 4 people.',
  });
  return result.toAIStreamResponse();
};

export const getWeather = async (modelName: string) => {
  const openrouter = createOpenRouter({
    apiKey: process.env.OPENROUTER_API_KEY,
  });

  const result = await streamText({
    model: openrouter(modelName),
    prompt: 'What is the weather in San Francisco, CA in Fahrenheit?',
    tools: {
      getCurrentWeather: {
        description: 'Get the current weather in a given location',
        parameters: z.object({
          location: z
            .string()
            .describe('The city and state, e.g. San Francisco, CA'),
          unit: z.enum(['celsius', 'fahrenheit']).optional(),
        }),
        execute: async ({ location, unit = 'celsius' }) => {
          // Mock response for the weather
          const weatherData = {
            'Boston, MA': {
              celsius: '15°C',
              fahrenheit: '59°F',
            },
            'San Francisco, CA': {
              celsius: '18°C',
              fahrenheit: '64°F',
            },
          };

          const weather = weatherData[location];
          if (!weather) {
            return `Weather data for ${location} is not available.`;
          }

          return `The current weather in ${location} is ${weather[unit]}.`;
        },
      },
    },
  });
  return result.toAIStreamResponse();
};Uptime
OpenRouter continuously monitors the health and availability of AI providers to ensure maximum uptime for your applications. We track response times, error rates, and availability across all providers in real-time, and route based on this feedback.

How It Works
OpenRouter tracks response times, error rates, and availability across all providers in real-time. This data helps us make intelligent routing decisions and provides transparency about service reliability.

Uptime Example: Claude 3.5 Sonnet

Uptime Example: Llama 3.3 70B Instruct

Customizing Provider Selection
While our smart routing helps maintain high availability, you can also customize provider selection using request parameters. This gives you control over which providers handle your requests while still benefiting from automatic fallback when needed.

Learn more about customizing provider selection in our Provider Routing documentation.
