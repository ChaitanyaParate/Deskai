import subprocess

class LocalLLM:
    def __init__(self, model="phi3:mini"):
        self.model = model
        print("[deskai] Model Initialized", flush=True)

    def generate_stream(self, prompt: str):
        try:
            proc = subprocess.Popen(
                ["ollama", "run", self.model],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            # send prompt
            proc.stdin.write(prompt)
            proc.stdin.close()

            # stream output line by line
            for line in proc.stdout:
                yield line

            proc.wait()

        except Exception as e:
            yield f"[LLM ERROR] {e}\n"

# import subprocess

# #mistral
# class LocalLLM:
#     def __init__(self, model="mistral"):
#         self.model = model
#         print("[deskai] Model Initialized", flush=True)

#     def generate(self, prompt: str) -> str:
#         try:
#             print("OK", flush=True)
#             result = subprocess.run(
#                 ["ollama", "run", self.model],
#                 input=prompt,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True,
#                 timeout=120
#             )
#         except subprocess.TimeoutExpired:
#             return "[LLM ERROR] Timed out while generating response"

#         if result.returncode != 0:
#             return f"[LLM ERROR]\n{result.stderr.strip()}"

#         return result.stdout.strip()


