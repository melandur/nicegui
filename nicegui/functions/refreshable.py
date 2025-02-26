from typing import Any, Callable, Dict, List, Tuple

from typing_extensions import Self

from .. import background_tasks, globals
from ..dependencies import register_component
from ..element import Element
from ..helpers import is_coroutine

register_component('refreshable', __file__, 'refreshable.js')


class refreshable:

    def __init__(self, func: Callable) -> None:
        """Refreshable UI functions

        The `@ui.refreshable` decorator allows you to create functions that have a `refresh` method.
        This method will automatically delete all elements created by the function and recreate them.
        """
        self.func = func
        self.instance = None
        self.containers: List[Tuple[Element, List[Any], Dict[str, Any]]] = []

    def __get__(self, instance, _) -> Self:
        self.instance = instance
        return self

    def __call__(self, *args, **kwargs) -> None:
        self.prune()
        with Element('refreshable') as container:
            self.containers.append((container, args, kwargs))
        if is_coroutine(self.func):
            async def wait_for_result():
                with container:
                    await self.func(*args, **kwargs) if self.instance is None else self.func(self.instance, *args, **kwargs)
            return wait_for_result()
        else:
            with container:
                self.func(*args, **kwargs) if self.instance is None else self.func(self.instance, *args, **kwargs)

    def refresh(self) -> None:
        self.prune()
        for container, args, kwargs in self.containers:
            container.clear()
            if is_coroutine(self.func):
                async def wait_for_result(container: Element, args, kwargs):
                    with container:
                        if self.instance is None:
                            await self.func(*args, **kwargs)
                        else:
                            await self.func(self.instance, *args, **kwargs)
                if globals.loop and globals.loop.is_running():
                    background_tasks.create(wait_for_result(container=container, args=args, kwargs=kwargs))
                else:
                    globals.app.on_startup(wait_for_result(container=container, args=args, kwargs=kwargs))
            else:
                with container:
                    if self.instance is None:
                        self.func(*args, **kwargs)
                    else:
                        self.func(self.instance, *args, **kwargs)

    def prune(self) -> None:
        self.containers = [
            (container, args, kwargs)
            for container, args, kwargs in self.containers
            if container.client.id in globals.clients
        ]
