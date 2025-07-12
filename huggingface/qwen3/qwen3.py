# Qwen3-0.6B model inference example
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen3-0.6B"

# load the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

# prepare the model input
prompt = "Give me a short introduction to large language model."
messages = [
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=True # Switches between thinking and non-thinking modes. Default is True.
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

# conduct text completion
generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=32768
)
output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

# parsing thinking content
try:
    # rindex finding 151668 (</think>)
    index = len(output_ids) - output_ids[::-1].index(151668)
except ValueError:
    index = 0

thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

breakpoint()
print("thinking content:", thinking_content)
print("content:", content)

# Qwen3ForCausalLM(
#   (model): Qwen3Model(
#     (embed_tokens): Embedding(151936, 1024)
#     (layers): ModuleList(
#       (0-27): 28 x Qwen3DecoderLayer(
#         (self_attn): Qwen3Attention(
#           (q_proj): Linear(in_features=1024, out_features=2048, bias=False)
#           (k_proj): Linear(in_features=1024, out_features=1024, bias=False)
#           (v_proj): Linear(in_features=1024, out_features=1024, bias=False)
#           (o_proj): Linear(in_features=2048, out_features=1024, bias=False)
#           (q_norm): Qwen3RMSNorm((128,), eps=1e-06)
#           (k_norm): Qwen3RMSNorm((128,), eps=1e-06)
#         )
#         (mlp): Qwen3MLP(
#           (gate_proj): Linear(in_features=1024, out_features=3072, bias=False)
#           (up_proj): Linear(in_features=1024, out_features=3072, bias=False)
#           (down_proj): Linear(in_features=3072, out_features=1024, bias=False)
#           (act_fn): SiLU()
#         )
#         (input_layernorm): Qwen3RMSNorm((1024,), eps=1e-06)
#         (post_attention_layernorm): Qwen3RMSNorm((1024,), eps=1e-06)
#       )
#     )
#     (norm): Qwen3RMSNorm((1024,), eps=1e-06)
#     (rotary_emb): Qwen3RotaryEmbedding()
#   )
#   (lm_head): Linear(in_features=1024, out_features=151936, bias=False)
# )