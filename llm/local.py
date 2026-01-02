import subprocess

class LocalLLM:
    def __init__(self, model="mistral"):
        self.model = model
        print("[deskai] Model Initialized", flush=True)

    def generate_stream(self, prompt: str):
        proc = subprocess.Popen(
            ["ollama", "run", self.model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        proc.stdin.write(prompt)
        proc.stdin.close()

        for line in iter(proc.stdout.readline, ""):
            yield line

        proc.stdout.close()
        proc.wait()
