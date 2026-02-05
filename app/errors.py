from dataclasses import dataclass

@dataclass
class AppError(Exception):
    message: str
    status_code: int = 500
    code: str = "internal_error"
    details: dict | None = None

    def to_dict(self) -> dict:
        return{
            "error":self.code,
            "message":self.message,
            "details": self.details
        }