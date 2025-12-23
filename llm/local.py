import subprocess

#mistral
class LocalLLM:
    def __init__(self, model="mistral"):
        self.model = model
        subprocess.run(
            ["ollama", "run", self.model],
            input="warmup",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True
        )

    def generate(self, prompt: str) -> str:
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60
            )
        except subprocess.TimeoutExpired:
            return "[LLM ERROR] Timed out while generating response"

        if result.returncode != 0:
            return f"[LLM ERROR]\n{result.stderr.strip()}"

        return result.stdout.strip()
