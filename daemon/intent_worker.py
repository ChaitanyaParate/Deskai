from queue import Queue
from threading import Thread
from intent.executo.executor import execute_intent

intent_queue = Queue()
result_queue = Queue()

def intent_worker():
    print("[deskai] intent worker started")
    while True:
        intent, context = intent_queue.get()
        print(f"[deskai] worker executing intent: {intent.name}")
        try:
            result = execute_intent(intent, context)
            print("[deskai] worker finished intent")
            result_queue.put(result)

        except Exception as e:
            result_queue.put({
                "type": "text",
                "content": str(e)
            })

def start_intent_worker():
    Thread(target=intent_worker, daemon=True).start()