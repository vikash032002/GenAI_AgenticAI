#install tiktoken
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o-mini")

text = "Hi, How are you?"

print(enc.encode(text)) #[12194, 11, 3253, 553, 481, 30]

print("Decode",enc.decode([12194, 11, 3253, 553, 481, 30]))