import asyncio
from typing import Callable, Dict, List, Any, Type

# Global dictionary to store exception handlers.
_events: Dict[str, List[Callable[[Exception], None]]] = {}

def register_exception_handler(ex_type: Type[Exception], handler: Callable[[Exception], None]) -> None:
    """
    Register an exception handler for exceptions of the given type.
    """
    key = getattr(ex_type, "__qualname__", None) or getattr(ex_type, "__name__", None)
    if key is None:
        return
    if key not in _events:
        _events[key] = []
    _events[key].append(handler)

def trigger_exception_handler(exception: Exception) -> None:
    """
    Invoke all exception handlers registered for the type of the given exception.
    """
    key = exception.__class__.__qualname__
    if key is None or key not in _events:
        return
    for handler in _events[key]:
        handler(exception)

def _on_success(task: asyncio.Future, error_action: Callable[[Exception], None] = None) -> bool:
    """
    Returns True if the task completed successfully (i.e. without exceptions).
    If there is an exception, triggers the registered exception handlers and calls error_action if provided.
    """
    exc = task.exception()
    if exc is None:
        return True
    # If the task failed, print exception message, trigger exception handlers, and call error_action.
    print(str(exc))
    trigger_exception_handler(exc)
    if error_action:
        error_action(exc)
    return False

async def continue_with_on_success(task: asyncio.Future, continuation_action: Callable[[asyncio.Future], None],
                                   error_action: Callable[[Exception], None] = None) -> None:
    """
    Awaits 'task' and then, if it succeeded, calls 'continuation_action' with the task as an argument.
    If the task failed, triggers exception handlers and calls error_action if provided.
    """
    try:
        await task
        if _on_success(task, error_action):
            continuation_action(task)
    except Exception as e:
        trigger_exception_handler(e)
        if error_action:
            error_action(e)

async def continue_with_on_success_result(task: asyncio.Future, continuation_function: Callable[[asyncio.Future], Any],
                                            error_action: Callable[[Exception], None] = None) -> Any:
    """
    Awaits 'task' and then, if it succeeded, returns the result of 'continuation_function(task)'.
    If the task failed, triggers exception handlers and returns None.
    """
    try:
        await task
        if _on_success(task, error_action):
            return continuation_function(task)
        else:
            return None
    except Exception as e:
        trigger_exception_handler(e)
        if error_action:
            error_action(e)
        return None
