from abc import ABC, abstractmethod
from models.canonical import CanonicalAlert

class BaseNotificationAdapter(ABC):
    @abstractmethod
    def send(self, alert: CanonicalAlert, explanation: str):
        pass
