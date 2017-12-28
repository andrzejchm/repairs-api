from abc import ABC, abstractmethod


class RepairEntityGateway(ABC):
    @abstractmethod
    def get_repairs_in_date_range(self, from_timestamp_inclusive, to_timestamp_exclusive):
        pass

    @abstractmethod
    def create_repair(self, repair):
        pass

    @abstractmethod
    def get_repair_by_id(self, repair_id):
        pass

    @abstractmethod
    def delete_repair_by_id(self, repair_id):
        pass

    @abstractmethod
    def propose_repair_completion(self, repair_id):
        pass

    @abstractmethod
    def mark_repair_completed(self, repair_id):
        pass

    @abstractmethod
    def update_repair(self, repair):
        pass

    @abstractmethod
    def get_repair_comments(self, repair_id):
        pass

    @abstractmethod
    def add_comment(self, comment):
        pass

