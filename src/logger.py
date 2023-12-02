import logging
import functools
from aiogram.types import Message, CallbackQuery


class Logger:
    def __init__(self, name, log_file, level=logging.INFO):
        """Setup as many loggers as you want"""

        formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")

        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.addHandler(handler)

    def log_function_call(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.info(
                f"Calling function {func.__name__} with arguments {args} and keyword arguments {kwargs}"
            )
            try:
                result = func(*args, **kwargs)
                self.logger.info(f"Function {func.__name__} completed successfully")
                return result
            except Exception as e:
                self.logger.error(f"Function {func.__name__} raised an error: {str(e)}")
                raise e  # re-raise the caught exception after logging it

        return wrapper

    def log_message(self, func):
        """Decorator to log text messages sent and received by the bot."""

        @functools.wraps(func)
        async def wrapper(message: Message, *args, **kwargs):
            if message:
                user_id = message.from_user.id if message.from_user else "Unknown"
                user_name = (
                    message.from_user.full_name if message.from_user else "Unknown User"
                )
                text = message.text or "No Text"
                self.logger.info(
                    f"Received message from {user_id} ({user_name}): {text}"
                )
            else:
                self.logger.info("Received a message object that is None")

            result = await func(message, *args, **kwargs)

            if isinstance(result, Message) and result.text:
                response_text = result.text
                self.logger.info(f"Sent response: {response_text}")
            elif result is None:
                self.logger.info("No response sent")

            return result

        return wrapper

    def log_callback(self, func):
        """Decorator to log callback queries handled by the bot."""

        @functools.wraps(func)
        async def wrapper(callback_query: CallbackQuery, *args, **kwargs):
            if callback_query:
                user_id = (
                    callback_query.from_user.id
                    if callback_query.from_user
                    else "Unknown"
                )
                user_name = (
                    callback_query.from_user.full_name
                    if callback_query.from_user
                    else "Unknown User"
                )
                data = callback_query.data or "No Data"
                self.logger.info(
                    f"Received callback from {user_id} ({user_name}): {data}"
                )
            else:
                self.logger.info("Received a callback query object that is None")

            result = await func(callback_query, *args, **kwargs)

            if result is None:
                self.logger.info("No action taken for the callback")

            return result

        return wrapper

    def class_log(self, cls):
        for name, method in cls.__dict__.items():
            if callable(method):
                if "message" in method.__annotations__:
                    setattr(cls, name, self.log_message(method))
                elif "callback_query" in method.__annotations__:
                    setattr(cls, name, self.log_callback(method))
                else:
                    setattr(cls, name, self.log_function_call(method))
        return cls
