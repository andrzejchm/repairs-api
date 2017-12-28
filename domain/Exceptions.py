from config import REPAIR_DURATION_SECONDS


class ApiException(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super(Exception, self).__init__(self.message)


class UserAlreadyExistsException(ApiException):
    def __init__(self, username):
        super().__init__(
            f"'{username}' already exists",
            1)


class InvalidDateRangeException(ApiException):
    def __init__(self, from_inclusive, to_exclusive):
        super().__init__(
            f"provided date range is invalid: <{from_inclusive},{to_exclusive})",
            2)


class InvalidRepairDurationException(ApiException):
    def __init__(self, duration):
        super().__init__(
            f"provided duration of a repair is {duration} seconds, while expected is {REPAIR_DURATION_SECONDS} seconds",
            3)


class RepairClashException(ApiException):
    def __init__(self, from_inclusive, to_exclusive):
        super().__init__(
            f"There can be only on repair on given time: <{from_inclusive}, {to_exclusive})",
            4)


class RepairNotFoundException(ApiException):
    def __init__(self, repair_id):
        super().__init__(
            f"There is no repair with id: {repair_id}",
            5)


class RepairAlreadyCompletedException(ApiException):
    def __init__(self, repair_id):
        super().__init__(
            f"Given repair is already completed. Repair id: {repair_id}",
            6)


class MustBeAtLeastManagerException(ApiException):
    def __init__(self):
        super().__init__(
            f"You must be at least manager to perform this operation",
            7)


class BodyValidationException(ApiException):
    def __init__(self, errors):
        super().__init__(
            f"{str(errors)}",
            8)


class CommentPostFailedException(ApiException):
    def __init__(self):
        super().__init__(
            f"Could not post the comment",
            9)


class CannotDeleteYourselfException(ApiException):
    def __init__(self):
        super().__init__(
            f"You cannot delete your own user",
            10)


class UserNotFoundException(ApiException):
    def __init__(self, username):
        super().__init__(
            f"'{username}' user does not exist",
            11)
