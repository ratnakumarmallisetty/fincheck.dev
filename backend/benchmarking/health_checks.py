from msgqueue.model_registry import list_models
from msgqueue.connection import get_connection

def check_model_registry():
    models = list_models()
    return {
        "model_count": len(models),
        "models": models,
        "status": "OK" if models else "EMPTY"
    }


def check_message_queue():
    try:
        conn = get_connection()
        ch = conn.channel()
        q = ch.queue_declare(queue="model_queue", passive=True)
        message_count = q.method.message_count
        conn.close()

        return {"status": "OK", "messages_waiting": message_count}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}
