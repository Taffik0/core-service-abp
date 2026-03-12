from src.database.repository.outbox_repository import OutBoxRepository, OutBoxRepositoryPG

from src.database.unit_of_work import UoW


def build_outbox_repository(conn) -> OutBoxRepository:
    return OutBoxRepositoryPG(conn)

