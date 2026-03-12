from aiokafka.structs import ConsumerRecord


class MessageHandler:
    _topic = ""

    def __init__(self, topic: str | None = ""):
        if topic:
            self.topic = topic
        else:
            self.topic = self._get_static_topic()

    @classmethod
    def _get_static_topic(cls):
        return cls._topic

    def get_topic(self) -> str:
        return self.topic

    async def process_message(self, msg: ConsumerRecord):
        pass